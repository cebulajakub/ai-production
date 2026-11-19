from orders_repository import get_order_by_id, get_delayed_orders


def get_order_details(order_id: int):
    return get_order_by_id(order_id)


def get_delayed_orders_list(limit: int = 10, offset: int = 0):
    return get_delayed_orders(limit=limit, offset=offset)