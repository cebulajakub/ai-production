USE ProductionCopilotDB;


GO
SELECT   o.OrderId,
         c.Name AS CustomerName,
         o.Status,
         o.TotalAmount
FROM     Orders AS o
         INNER JOIN
         Customers AS c
         ON o.CustomerId = c.CustomerId
ORDER BY o.OrderId;

SELECT   o.OrderId,
         c.Name AS CustomerName,
         p.SKU,
         p.Name AS ProductName,
         oi.Quantity,
         oi.UnitPrice,
         oi.Quantity * oi.UnitPrice AS LineTotal
FROM     Orders AS o
         INNER JOIN
         Customers AS c
         ON o.CustomerId = c.CustomerId
         INNER JOIN
         OrderItems AS oi
         ON o.OrderId = oi.OrderId
         INNER JOIN
         Products AS p
         ON oi.ProductId = p.ProductId
ORDER BY o.OrderId, p.Name;

SELECT   o.OrderId,
         c.Name AS CustomerName,
         p.SKU,
         p.Name AS ProductName,
         oi.Quantity,
         oi.UnitPrice,
         oi.Quantity * oi.UnitPrice AS LineTotal
FROM     Orders AS o
         INNER JOIN
         Customers AS c
         ON o.CustomerId = c.CustomerId
         INNER JOIN
         OrderItems AS oi
         ON o.OrderId = oi.OrderId
         INNER JOIN
         Products AS p
         ON oi.ProductId = p.ProductId
WHERE    o.Status = 'Pending'
         AND oi.Quantity > 100
ORDER BY o.OrderId, p.Name;

SELECT   o.OrderId,
         p.Name AS ProductName,
         oi.Quantity AS OrderedQuantity,
         i.QuantityOnHand,
         oi.Quantity - i.QuantityOnHand AS MissingQuantity
FROM     Orders AS o
         INNER JOIN
         OrderItems AS oi
         ON o.OrderId = oi.OrderId
         INNER JOIN
         Products AS p
         ON oi.ProductId = p.ProductId
         INNER JOIN
         Inventory AS i
         ON p.ProductId = i.ProductId
WHERE    o.Status = 'Pending'
         AND oi.Quantity > i.QuantityOnHand
ORDER BY MissingQuantity DESC;

SELECT   p.SKU,
         p.Name AS ProductName,
         SUM(oi.Quantity) AS TotalDemand,
         i.QuantityOnHand,
         SUM(oi.Quantity) - i.QuantityOnHand AS Shortage
FROM     OrderItems AS oi
         INNER JOIN
         Orders AS o
         ON oi.OrderId = o.OrderId
         INNER JOIN
         Products AS p
         ON oi.ProductId = p.ProductId
         INNER JOIN
         Inventory AS i
         ON p.ProductId = i.ProductId
WHERE    o.Status = 'Pending'
GROUP BY p.SKU, p.Name, i.QuantityOnHand
HAVING   SUM(oi.Quantity) > i.QuantityOnHand
ORDER BY Shortage DESC;