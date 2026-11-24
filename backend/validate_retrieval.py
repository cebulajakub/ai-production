import evaluate_retrieval


VALIDATION_CASES = [
    (
        "Jakie czynności wykonać po zatrzymaniu uszkodzonej maszyny?",
        "cnc_safety_procedure.txt"
    ),
    (
        "Kogo powiadomić o usterce CNC?",
        "cnc_safety_procedure.txt"
    ),
    (
        "Czy niezgodny produkt należy odseparować?",
        "quality_control.txt"
    ),
    (
        "Czy partia może trafić do magazynu bez kontroli?",
        "quality_control.txt"
    ),
    (
        "Kto analizuje wpływ niedoboru na zamówienia?",
        "warehouse_procedure.txt"
    ),
    (
        "Kto weryfikuje terminy dostaw brakujących materiałów?",
        "warehouse_procedure.txt"
    ),
    (
        "Jak często należy wymieniać olej w maszynie CNC?",
        None
    ),
    (
        "Jaka temperatura powinna panować w magazynie?",
        None
    ),
    (
        "Jak obliczyć wynagrodzenie operatora?",
        None
    ),
    (
        "Jakie są wymagane tolerancje wymiarowe produktów?",
        None
    )
]


if __name__ == "__main__":
    evaluate_retrieval.evaluate(VALIDATION_CASES)