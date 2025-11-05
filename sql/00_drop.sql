DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'openmind') THEN
            PERFORM pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = 'openmind' AND pid <> pg_backend_pid();
        END IF;
    END$$;

DROP DATABASE IF EXISTS openmind;

DROP OWNED BY openmind_user CASCADE;
DROP ROLE IF EXISTS openmind_user;
