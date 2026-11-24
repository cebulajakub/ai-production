from rag_service import (
    search_knowledge,
    EMBEDDING_MODEL,
    COLLECTION_NAME,
    RAG_SCORE_THRESHOLD
)


TEST_CASES = [
    ("Co zrobić w przypadku awarii obrabiarki?",
     "cnc_safety_procedure.txt"),

    ("Kto musi wyrazić zgodę na ponowne uruchomienie CNC?",
     "cnc_safety_procedure.txt"),

    ("Czy operator może samodzielnie naprawić maszynę?",
     "cnc_safety_procedure.txt"),

    ("Jak postępować z wadliwą partią produktów?",
     "quality_control.txt"),

    ("Kiedy należy przeprowadzić kontrolę jakości?",
     "quality_control.txt"),

    ("Kto decyduje o odrzuceniu wadliwego produktu?",
     "quality_control.txt"),

    ("Komu zgłosić brak materiałów?",
     "warehouse_procedure.txt"),

    ("Kto sprawdza dostępność materiałów?",
     "warehouse_procedure.txt"),

    ("Jak postępować z niedoborem o wysokim priorytecie?",
     "warehouse_procedure.txt"),

    ("Jak przygotować spaghetti carbonara?", None),

    ("Jaka jest stolica Japonii?", None),

    ("Jak skonfigurować router Wi-Fi?", None),

    ("Jakie są zasady przyznawania urlopu pracownikom?", None),

    ("Jaki jest harmonogram konserwacji maszyn CNC?", None),

    ("Ile kosztuje wymiana silnika obrabiarki?", None)
]

def evaluate(test_cases=TEST_CASES):
    positive_count = 0
    negative_count = 0

    hit_at_1 = 0
    hit_at_3 = 0
    reciprocal_rank_sum = 0
    correct_rejections = 0

    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Threshold: {RAG_SCORE_THRESHOLD}")

    for question, expected_source in test_cases:
        
        results = search_knowledge(question)

        sources = [
            item["payload"]["source"]
            for item in results
        ]

        if expected_source is None:
            negative_count += 1

            passed = not results

            if passed:
                correct_rejections += 1

        else:
            positive_count += 1

            if sources and sources[0] == expected_source:
                hit_at_1 += 1

            if expected_source in sources[:3]:
                hit_at_3 += 1

            if expected_source in sources:
                rank = sources.index(expected_source) + 1
                reciprocal_rank_sum += 1 / rank

            passed = expected_source in sources

        status = "PASS" if passed else "FAIL"

        print(f"\n[{status}] {question}")

        for item in results:
            print(
                f"  {item['score']:.4f} | "
                f"{item['payload']['source']}"
            )

    print("\n========== EVALUATION RESULTS ==========")

    print(f"Hit Rate@1: {hit_at_1 / positive_count:.2%}")
    print(f"Hit Rate@3: {hit_at_3 / positive_count:.2%}")
    print(f"MRR: {reciprocal_rank_sum / positive_count:.4f}")

    print(
        f"Rejection Rate: "
        f"{correct_rejections / negative_count:.2%}"
    )
    
    return {
        "hit_rate_at_1": hit_at_1 / positive_count,
        "hit_rate_at_3": hit_at_3 / positive_count,
        "mrr": reciprocal_rank_sum / positive_count,
        "rejection_rate": correct_rejections / negative_count
    }


if __name__ == "__main__":
    evaluate()