USE ProductionCopilotDB;


GO
CREATE TABLE Products (
    ProductId INT             IDENTITY (1, 1) PRIMARY KEY,
    SKU       NVARCHAR (50)   NOT NULL UNIQUE,
    Name      NVARCHAR (200)  NOT NULL,
    UnitPrice DECIMAL (18, 2) NOT NULL,
    CreatedAt DATETIME2       DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT CK_Products_UnitPrice CHECK (UnitPrice >= 0)
);

CREATE TABLE Orders (
    OrderId     INT             IDENTITY (1, 1) PRIMARY KEY,
    CustomerId  INT             NOT NULL,
    OrderDate   DATETIME2       DEFAULT SYSUTCDATETIME() NOT NULL,
    TotalAmount DECIMAL (18, 2) NOT NULL,
    Status      NVARCHAR (50)   DEFAULT 'Pending' NOT NULL,
    CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerId) REFERENCES Customers (CustomerId),
    CONSTRAINT CK_Orders_TotalAmount CHECK (TotalAmount >= 0),
    CONSTRAINT CK_Orders_Status CHECK (Status IN ('Pending', 'InProgress', 'Completed'))
);

CREATE TABLE OrderItems (
    OrderItemId INT             IDENTITY (1, 1) PRIMARY KEY,
    OrderId     INT             NOT NULL,
    ProductId   INT             NOT NULL,
    Quantity    INT             NOT NULL,
    UnitPrice   DECIMAL (18, 2) NOT NULL,
    CONSTRAINT FK_OrderItems_Orders FOREIGN KEY (OrderId) REFERENCES Orders (OrderId),
    CONSTRAINT FK_OrderItems_Products FOREIGN KEY (ProductId) REFERENCES Products (ProductId),
    CONSTRAINT CK_OrderItems_Quantity CHECK (Quantity > 0),
    CONSTRAINT CK_OrderItems_UnitPrice CHECK (UnitPrice >= 0)
);

CREATE TABLE Inventory (
    InventoryId    INT       IDENTITY (1, 1) PRIMARY KEY,
    ProductId      INT       NOT NULL,
    QuantityOnHand INT       DEFAULT 0 NOT NULL,
    LastUpdated    DATETIME2 DEFAULT SYSUTCDATETIME() NOT NULL,
    CONSTRAINT FK_Inventory_Products FOREIGN KEY (ProductId) REFERENCES Products (ProductId),
    CONSTRAINT CK_Inventory_Quantity CHECK (QuantityOnHand >= 0),
    CONSTRAINT UQ_Inventory_ProductId UNIQUE (ProductId)
);