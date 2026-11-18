USE ProductionCopilotDB;


GO
CREATE TABLE Customers (
    CustomerId INT            IDENTITY (1, 1) PRIMARY KEY,
    Name       NVARCHAR (200) NOT NULL,
    Email      NVARCHAR (255) NULL,
    CreatedAt  DATETIME2      DEFAULT SYSUTCDATETIME() NOT NULL
);