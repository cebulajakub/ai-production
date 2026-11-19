from inventory_repository import get_inventory_shortages, get_low_stock_products


def get_shortages():
    shortages = get_inventory_shortages()

    for item in shortages:
        shortage = item["shortage"]

        if shortage >= 500:
            item["severity"] = "HIGH"
        elif shortage >= 100:
            item["severity"] = "MEDIUM"
        else:
            item["severity"] = "LOW" 
    shortages.sort(
    key=lambda item: item["shortage"],
    reverse=True
)

    return shortages

def get_shortages_summary():
    shortages = get_shortages()
    return build_shortages_summary(shortages)

def get_production_context():
    shortages = get_shortages()

    return {
        "summary": build_shortages_summary(shortages),
        "shortages": shortages,
    }
    
def build_shortages_summary(shortages):
    summary = {
        "total_products_with_shortages": len(shortages),
        "high_priority": 0,
        "medium_priority": 0,
        "low_priority": 0,
    }

    for item in shortages:
        severity = item["severity"]

        if severity == "HIGH":
            summary["high_priority"] += 1
        elif severity == "MEDIUM":
            summary["medium_priority"] += 1
        else:
            summary["low_priority"] += 1

    return summary

def get_low_stock():
    return get_low_stock_products()