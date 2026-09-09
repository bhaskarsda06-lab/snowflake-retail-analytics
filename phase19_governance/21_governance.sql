/*CREATE MASKING POLICY EMAIL_MASK
AS (VAL STRING)
RETURNS STRING ->
CASE
    WHEN CURRENT_ROLE()='ACCOUNTADMIN'
    THEN VAL
    ELSE '********'
END;

ALTER TABLE CURATED.CUSTOMERS
MODIFY COLUMN EMAIL
SET MASKING POLICY EMAIL_MASK;*/


-- Governance features not available in current Snowflake edition

SELECT
'Governance phase skipped - Masking Policies not supported in this account'
AS STATUS;