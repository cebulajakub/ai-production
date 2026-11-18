USE ProductionCopilotDB;


GO
-- ==========================================
-- 1. CUSTOMERS
-- ==========================================
INSERT INTO Customers (
    Name,
    Email
)
SELECT v.Name,
       v.Email
FROM   (VALUES (N'Fabryka Alfa', N'kontakt@alfa.example'), (N'MetalTech', N'biuro@metaltech.example'), (N'AutoParts', N'orders@autoparts.example'), (N'Industrial Solutions', N'office@industrial.example'), (N'PolSteel', N'kontakt@polsteel.example')) AS v(Name, Email)
WHERE  NOT EXISTS (SELECT 1
                   FROM   Customers AS c
                   WHERE  c.Email = v.Email);

-- ==========================================
-- 2. PRODUCTS
-- ==========================================
INSERT INTO Products (
    SKU,
    Name,
    UnitPrice
)
SELECT v.SKU,
       v.Name,
       v.UnitPrice
FROM   (VALUES (N'SRUBA-M8', N'Śruba M8', 2.50), (N'NAKRETKA-M8', N'Nakrętka M8', 1.20), (N'PODKLADKA-M8', N'Podkładka M8', 0.50), (N'LOZYSKO-6204', N'Łożysko 6204', 45.00), (N'WAL-STAL-20', N'Wał stalowy 20 mm', 120.00), (N'BLACHA-2MM', N'Blacha stalowa 2 mm', 85.00), (N'SILNIK-1KW', N'Silnik elektryczny 1 kW', 950.00), (N'PASEK-A100', N'Pasek napędowy A100', 35.00)) AS v(SKU, Name, UnitPrice)
WHERE  NOT EXISTS (SELECT 1
                   FROM   Products AS p
                   WHERE  p.SKU = v.SKU);

-- ==========================================
-- 3. INVENTORY
-- ==========================================
INSERT INTO Inventory (
    ProductId,
    QuantityOnHand
)
SELECT p.ProductId,
       v.QuantityOnHand
FROM   (VALUES (N'SRUBA-M8', 500), (N'NAKRETKA-M8', 350), (N'PODKLADKA-M8', 1000), (N'LOZYSKO-6204', 12), (N'WAL-STAL-20', 8), (N'BLACHA-2MM', 45), (N'SILNIK-1KW', 2), (N'PASEK-A100', 25)) AS v(SKU, QuantityOnHand)
       INNER JOIN
       Products AS p
       ON p.SKU = v.SKU
WHERE  NOT EXISTS (SELECT 1
                   FROM   Inventory AS i
                   WHERE  i.ProductId = p.ProductId);

-- ==========================================
-- 4. ORDERS
-- ==========================================
-- Numery zamówień identyfikujemy przez
-- klientów i daty testowe, a nie zakładamy,
-- że ID zaczynają się od 1.
DECLARE @SeedOrders TABLE (
    CustomerEmail NVARCHAR (255),
    OrderDate     DATETIME2     ,
    Status        NVARCHAR (50) );

INSERT  INTO @SeedOrders
VALUES (N'kontakt@alfa.example', '2026-11-01', N'Completed'),
       (N'biuro@metaltech.example', '2026-11-03', N'InProgress'),
       (N'orders@autoparts.example', '2026-11-05', N'Pending'),
       (N'office@industrial.example', '2026-11-07', N'Pending'),
       (N'kontakt@polsteel.example', '2026-11-10', N'InProgress'),
       (N'kontakt@alfa.example', '2026-11-12', N'Pending'),
       (N'biuro@metaltech.example', '2026-11-14', N'Pending'),
       (N'orders@autoparts.example', '2026-11-16', N'Pending');

INSERT INTO Orders (
    CustomerId,
    OrderDate,
    Status,
    TotalAmount
)
SELECT c.CustomerId,
       s.OrderDate,
       s.Status,
       0
FROM   @SeedOrders AS s
       INNER JOIN
       Customers AS c
       ON c.Email = s.CustomerEmail
WHERE  NOT EXISTS (SELECT 1
                   FROM   Orders AS o
                   WHERE  o.CustomerId = c.CustomerId
                          AND o.OrderDate = s.OrderDate);

-- ==========================================
-- 5. ORDER ITEMS
-- ==========================================
DECLARE @SeedItems TABLE (
    CustomerEmail NVARCHAR (255),
    OrderDate     DATETIME2     ,
    SKU           NVARCHAR (50) ,
    Quantity      INT           );

INSERT  INTO @SeedItems
VALUES (N'kontakt@alfa.example', '2026-11-01', N'SRUBA-M8', 100),
       (N'kontakt@alfa.example', '2026-11-01', N'NAKRETKA-M8', 100),
       (N'kontakt@alfa.example', '2026-11-01', N'PODKLADKA-M8', 200),
       (N'biuro@metaltech.example', '2026-11-03', N'LOZYSKO-6204', 20),
       (N'biuro@metaltech.example', '2026-11-03', N'WAL-STAL-20', 5),
       (N'orders@autoparts.example', '2026-11-05', N'SILNIK-1KW', 5),
       (N'orders@autoparts.example', '2026-11-05', N'PASEK-A100', 10),
       (N'office@industrial.example', '2026-11-07', N'BLACHA-2MM', 60),
       (N'office@industrial.example', '2026-11-07', N'SRUBA-M8', 200),
       (N'kontakt@polsteel.example', '2026-11-10', N'WAL-STAL-20', 10),
       (N'kontakt@polsteel.example', '2026-11-10', N'LOZYSKO-6204', 8),
       (N'kontakt@alfa.example', '2026-11-12', N'NAKRETKA-M8', 400),
       (N'kontakt@alfa.example', '2026-11-12', N'PODKLADKA-M8', 400),
       (N'biuro@metaltech.example', '2026-11-14', N'SILNIK-1KW', 3),
       (N'biuro@metaltech.example', '2026-11-14', N'PASEK-A100', 15),
       (N'orders@autoparts.example', '2026-11-16', N'SRUBA-M8', 600),
       (N'orders@autoparts.example', '2026-11-16', N'NAKRETKA-M8', 600);

INSERT INTO OrderItems (
    OrderId,
    ProductId,
    Quantity,
    UnitPrice
)
SELECT o.OrderId,
       p.ProductId,
       si.Quantity,
       p.UnitPrice
FROM   @SeedItems AS si
       INNER JOIN
       Customers AS c
       ON c.Email = si.CustomerEmail
       INNER JOIN
       Orders AS o
       ON o.CustomerId = c.CustomerId
          AND o.OrderDate = si.OrderDate
       INNER JOIN
       Products AS p
       ON p.SKU = si.SKU
WHERE  NOT EXISTS (SELECT 1
                   FROM   OrderItems AS oi
                   WHERE  oi.OrderId = o.OrderId
                          AND oi.ProductId = p.ProductId);

-- ==========================================
-- 6. UPDATE ORDER TOTALS
-- ==========================================
UPDATE o
SET    TotalAmount = COALESCE ((SELECT SUM(oi.Quantity * oi.UnitPrice)
                                FROM   OrderItems AS oi
                                WHERE  oi.OrderId = o.OrderId), 0)
FROM   Orders AS o
WHERE  EXISTS (SELECT 1
               FROM   @SeedOrders AS s
                      INNER JOIN
                      Customers AS c
                      ON c.Email = s.CustomerEmail
               WHERE  c.CustomerId = o.CustomerId
                      AND s.OrderDate = o.OrderDate);

-- ==========================================
-- 7. VERIFY DATA
-- ==========================================
SELECT 'Customers' AS TableName,
       COUNT(*) AS [RowCount]
FROM   Customers
UNION ALL
SELECT 'Products',
       COUNT(*)
FROM   Products
UNION ALL
SELECT 'Orders',
       COUNT(*)
FROM   Orders
UNION ALL
SELECT 'OrderItems',
       COUNT(*)
FROM   OrderItems
UNION ALL
SELECT 'Inventory',
       COUNT(*)
FROM   Inventory;

-- ==========================================
-- 8. ORDER REPORT
-- ==========================================
SELECT   o.OrderId,
         c.Name AS Customer,
         o.OrderDate,
         o.Status,
         o.TotalAmount
FROM     Orders AS o
         INNER JOIN
         Customers AS c
         ON c.CustomerId = o.CustomerId
ORDER BY o.OrderDate;