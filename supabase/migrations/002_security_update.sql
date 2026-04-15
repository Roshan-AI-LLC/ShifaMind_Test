-- 002_security_update.sql
-- Run this in your Supabase SQL Editor to enforce the new security changes
-- without trying to recreate existing tables.

-- ==========================================
-- 1. Lock down Row Level Security (RLS)
-- ==========================================

-- Remove the old overly permissive policy
DROP POLICY IF EXISTS "doctors_own" ON doctors;
DROP POLICY IF EXISTS "doctors_own_select" ON doctors;
DROP POLICY IF EXISTS "doctors_own_update" ON doctors;
DROP POLICY IF EXISTS "doctors_admin_read" ON doctors;

-- Create granular policies for safety
CREATE POLICY "doctors_own_select" ON doctors
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "doctors_own_update" ON doctors
    FOR UPDATE USING (auth.uid() = id);

-- Keep the admin-read policy
CREATE POLICY "doctors_admin_read" ON doctors
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM doctors d WHERE d.id = auth.uid() AND d.role = 'admin'
        )
    );

-- ==========================================
-- 2. Add the Privilege Escalation Trigger
-- ==========================================

CREATE OR REPLACE FUNCTION protect_doctor_fields()
RETURNS TRIGGER AS $$
BEGIN
    -- If current user is not service role (backend Admin keys bypass this)
    IF current_setting('request.jwt.claims', true)::jsonb->>'role' != 'service_role' THEN
        -- Prevent arbitrary endpoints or frontend users from modifying role or is_active
        IF NEW.role IS DISTINCT FROM OLD.role OR NEW.is_active IS DISTINCT FROM OLD.is_active THEN
            RAISE EXCEPTION 'Not allowed to update role or is_active fields directly';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Securely attach the trigger
DROP TRIGGER IF EXISTS check_doctor_updates ON doctors;
CREATE TRIGGER check_doctor_updates
    BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION protect_doctor_fields();
