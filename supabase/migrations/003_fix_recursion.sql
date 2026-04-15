-- 003_fix_recursion.sql
-- Drop the recursive admin read policy to fix the infinite loop error "42P17"

DROP POLICY IF EXISTS "doctors_admin_read" ON doctors;
