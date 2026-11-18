from fastapi import FastAPI
from fastapi import HTTPException
from database import get_connection

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-production-copilot"
    }
    

@app.get("/inventory/shortages")
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

    try:
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

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )