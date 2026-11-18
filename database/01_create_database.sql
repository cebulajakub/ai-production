IF DB_ID('ProductionCopilotDB') IS NULL
    BEGIN
        CREATE DATABASE ProductionCopilotDB;
    END