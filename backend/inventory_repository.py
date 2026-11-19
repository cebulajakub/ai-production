from database import get_connection


def get_inventory_shortages():
    query = """
            SELECT
                p.SKU,
                p.Name AS ProductName,
                SUM(oi.Quantity) AS TotalDemand,
                i.QuantityOnHand,
                SUM(oi.Quantity) - i.QuantityOnHand AS Shortage
            FROM OrderItems oi
            INNER JOIN Orders o
                ON oi.OrderId = o.OrderId
            INNER JOIN Products p
                ON oi.ProductId = p.ProductId
            INNER JOIN Inventory i
                ON p.ProductId = i.ProductId
            WHERE o.Status = 'Pending'
            GROUP BY
                p.SKU,
                p.Name,
                i.QuantityOnHand
            HAVING SUM(oi.Quantity) > i.QuantityOnHand
            ORDER BY Shortage DESC;
        """
    
    with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query)

            return [
                {
                    "sku": row.SKU,
                    "product_name": row.ProductName,
                    "total_demand": row.TotalDemand,
                    "quantity_on_hand": row.QuantityOnHand,
                    "shortage": row.Shortage,
                }
                for row in cursor.fetchall()
            ]
            
def get_low_stock_products():
    query = """
        SELECT
            p.ProductId,
            p.SKU,
            p.Name AS ProductName,
            i.QuantityOnHand
        FROM Inventory i
        INNER JOIN Products p
            ON i.ProductId = p.ProductId
        WHERE i.QuantityOnHand < ?
        ORDER BY i.QuantityOnHand ASC
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query, 100)

        rows = cursor.fetchall()

        result = []

        for row in rows:
            result.append({
                "product_id": row.ProductId,
                "sku": row.SKU,
                "product_name": row.ProductName,
                "quantity_on_hand": row.QuantityOnHand
            })

        return result