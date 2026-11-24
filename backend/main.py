from fastapi import FastAPI, Query
from fastapi import HTTPException
from database import get_connection
from inventory_service import get_shortages, get_shortages_summary, get_production_context, get_low_stock
from orders_service import get_order_details, get_delayed_orders_list
from rag_service import answer_from_knowledge
from pydantic import BaseModel, Field
from ai_service import get_ai_response
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)

app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-production-copilot"
    }
    

@app.get("/inventory/shortages")
def inventory_shortages():
    try:
        return get_shortages()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )
        
@app.get("/inventory/summary")
def inventory_summary():
    try:
        return get_shortages_summary()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Database query failed"
        )
        
@app.get("/ai/context")
def ai_context():
    try:
        return get_production_context()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve production context"
        )
        
@app.get("/orders/delayed")
def get_delayed_orders(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    try:
        return get_delayed_orders_list(
            limit=limit,
            offset=offset
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve delayed orders"
        )
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    try:
        order = get_order_details(order_id)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found"
            )

        return order

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve order"
        )

@app.get("/inventory/low-stock")
def get_inventory_low_stock():
    try:
        return get_low_stock()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve low-stock products"
        )
        
@app.post("/ai/chat")
def chat_with_ai(request: ChatRequest):
    try:
        answer = get_ai_response(request.message)
        return {"answer": answer}

    except Exception:
        logger.exception("AI chat request failed")

        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable"
        )
        
@app.post("/ai/knowledge")
def ask_knowledge(request: ChatRequest):
    try:
        return answer_from_knowledge(request.message)
    except Exception:
        logger.exception("RAG request failed")
        raise HTTPException(
            status_code=503,
            detail="Knowledge service is temporarily unavailable"
        )