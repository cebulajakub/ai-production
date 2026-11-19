from database import get_connection


def get_order_by_id(order_id: int):
    query = """
        SELECT
            o.OrderId,
            o.Status,
            o.OrderDate,
            c.Name AS CustomerName
        FROM Orders o
        INNER JOIN Customers c
            ON o.CustomerId = c.CustomerId
        WHERE o.OrderId = ?
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, order_id)

        row = cursor.fetchone()

        if row is None:
            return None
        
        items_query = """
            SELECT
                p.SKU,
                p.Name AS ProductName,
                oi.Quantity
            FROM OrderItems oi
            INNER JOIN Products p
                ON oi.ProductId = p.ProductId
            WHERE oi.OrderId = ?
        """
        
        cursor.execute(items_query, order_id)
        items = cursor.fetchall()

        result = []

        for item in items:
            result.append({
                "sku": item.SKU,
                "product_name": item.ProductName,
                "quantity": item.Quantity,
            })
        return {
            "order_id": row.OrderId,
            "status": row.Status,
            "order_date": row.OrderDate.isoformat(),
            "customer_name": row.CustomerName,
            "items": result
        }
        
def get_delayed_orders(limit: int = 10, offset: int = 0):    
    query = """
        SELECT
            o.OrderId,
            o.Status,
            o.ExpectedDeliveryDate,
            c.Name AS CustomerName
        FROM Orders o
        INNER JOIN Customers c
            ON o.CustomerId = c.CustomerId
        WHERE o.ExpectedDeliveryDate < CAST(GETDATE() AS DATE)
          AND o.Status = 'Pending'
        ORDER BY o.ExpectedDeliveryDate
        OFFSET ? ROWS
        FETCH NEXT ? ROWS ONLY
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, offset, limit)

        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({
                "order_id": row.OrderId,
                "customer_name": row.CustomerName,
                "status": row.Status,
                "expected_delivery_date": row.ExpectedDeliveryDate.isoformat()
            })

        return result