-- 004_chat_model_default.sql
-- The chat_sessions.llm_model default still named a model that is no longer
-- used. In practice chat.py always writes settings.OPENROUTER_MODEL explicitly,
-- so the default never fired -- but a column default that lies is a trap for
-- anyone reading the schema to find out what the system runs.
ALTER TABLE chat_sessions
    ALTER COLUMN llm_model SET DEFAULT 'nvidia/nemotron-3-super-120b-a12b:free';
