-- ============================================================
-- ShifaMind Platform — Initial Schema
-- Run against your Supabase project via the SQL editor or CLI
-- ============================================================

-- ── Doctors ──────────────────────────────────────────────────
CREATE TABLE doctors (
    id          UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    full_name   TEXT NOT NULL,
    specialty   TEXT,
    institution TEXT,
    email       TEXT UNIQUE NOT NULL,
    role        TEXT NOT NULL DEFAULT 'doctor'
                     CHECK (role IN ('doctor', 'admin')),
    is_active   BOOLEAN NOT NULL DEFAULT true,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER doctors_updated_at
    BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Protect Role and Status fields
CREATE OR REPLACE FUNCTION protect_doctor_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- If current user is not service role (backend admin calls bypass this)
    IF current_setting('request.jwt.claims', true)::jsonb->>'role' != 'service_role' THEN
        -- Prevent modification of role or is_active
        IF NEW.role IS DISTINCT FROM OLD.role OR NEW.is_active IS DISTINCT FROM OLD.is_active THEN
            RAISE EXCEPTION 'Not allowed to update role or is_active fields';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_doctor_updates
    BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION protect_doctor_fields();


-- ── Sample Notes ─────────────────────────────────────────────
CREATE TABLE sample_notes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title           TEXT NOT NULL,
    category        TEXT NOT NULL,
    text            TEXT NOT NULL,
    note_length     INT GENERATED ALWAYS AS (LENGTH(text)) STORED,
    expected_codes  TEXT[],
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- ── Predictions ───────────────────────────────────────────────
CREATE TABLE predictions (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id           UUID NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    note_source         TEXT CHECK (note_source IN ('sample', 'custom')),
    sample_note_id      UUID REFERENCES sample_notes(id) ON DELETE SET NULL,
    input_text          TEXT NOT NULL,
    predicted_codes     JSONB NOT NULL DEFAULT '[]',
    activated_concepts  JSONB NOT NULL DEFAULT '[]',
    thresholds_used     JSONB,
    inference_time_ms   INT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX predictions_doctor_id_idx ON predictions(doctor_id);
CREATE INDEX predictions_created_at_idx ON predictions(created_at DESC);


-- ── Chat Sessions ─────────────────────────────────────────────
CREATE TABLE chat_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doctor_id       UUID NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    prediction_id   UUID REFERENCES predictions(id) ON DELETE SET NULL,
    llm_provider    TEXT NOT NULL DEFAULT 'openrouter',
    llm_model       TEXT NOT NULL DEFAULT 'meta-llama/llama-3.3-70b-instruct',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER chat_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE INDEX chat_sessions_doctor_id_idx ON chat_sessions(doctor_id);


-- ── Chat Messages ─────────────────────────────────────────────
CREATE TABLE chat_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  UUID NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role        TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content     TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX chat_messages_session_id_idx ON chat_messages(session_id);


-- ── Reviews ───────────────────────────────────────────────────
CREATE TABLE reviews (
    id                       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prediction_id            UUID NOT NULL REFERENCES predictions(id) ON DELETE CASCADE,
    doctor_id                UUID NOT NULL REFERENCES doctors(id) ON DELETE CASCADE,
    rating                   INT CHECK (rating BETWEEN 1 AND 5),
    accuracy_rating          INT CHECK (accuracy_rating BETWEEN 1 AND 5),
    interpretability_rating  INT CHECK (interpretability_rating BETWEEN 1 AND 5),
    comment                  TEXT,
    corrections              JSONB,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (prediction_id, doctor_id)
);

CREATE INDEX reviews_prediction_id_idx ON reviews(prediction_id);
CREATE INDEX reviews_doctor_id_idx ON reviews(doctor_id);


-- ============================================================
-- Row Level Security
-- ============================================================

ALTER TABLE doctors        ENABLE ROW LEVEL SECURITY;
ALTER TABLE predictions    ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions  ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages  ENABLE ROW LEVEL SECURITY;
ALTER TABLE reviews        ENABLE ROW LEVEL SECURITY;
ALTER TABLE sample_notes   ENABLE ROW LEVEL SECURITY;

-- Doctors: each doctor sees and can update only their own row
CREATE POLICY "doctors_own_select" ON doctors
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "doctors_own_update" ON doctors
    FOR UPDATE USING (auth.uid() = id);

-- Admins can read all doctors
CREATE POLICY "doctors_admin_read" ON doctors
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM doctors d WHERE d.id = auth.uid() AND d.role = 'admin'
        )
    );

-- Predictions: own rows only
CREATE POLICY "predictions_own" ON predictions
    FOR ALL USING (auth.uid() = doctor_id);

-- Chat sessions: own rows only
CREATE POLICY "chats_own" ON chat_sessions
    FOR ALL USING (auth.uid() = doctor_id);

-- Chat messages: accessible via owned sessions
CREATE POLICY "messages_own" ON chat_messages
    FOR ALL USING (
        session_id IN (
            SELECT id FROM chat_sessions WHERE doctor_id = auth.uid()
        )
    );

-- Reviews: own rows only
CREATE POLICY "reviews_own" ON reviews
    FOR ALL USING (auth.uid() = doctor_id);

-- Sample notes: any authenticated user can read active notes
CREATE POLICY "notes_read" ON sample_notes
    FOR SELECT USING (is_active = true AND auth.uid() IS NOT NULL);

-- Admins can manage sample notes
CREATE POLICY "notes_admin_write" ON sample_notes
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM doctors d WHERE d.id = auth.uid() AND d.role = 'admin'
        )
    );
