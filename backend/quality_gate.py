from evaluate_retrieval import evaluate
from validate_retrieval import VALIDATION_CASES


QUALITY_REQUIREMENTS = {
    "hit_rate_at_1": 0.80,
    "hit_rate_at_3": 0.90,
    "mrr": 0.85,
    "rejection_rate": 0.75
}


def run_quality_gate() -> bool:
    metrics = evaluate(VALIDATION_CASES)

    all_passed = True

    print("\n========== QUALITY GATE ==========")

    for metric, minimum in QUALITY_REQUIREMENTS.items():

        actual = metrics[metric]
        passed = actual >= minimum

        status = "PASS" if passed else "FAIL"

        print(
            f"[{status}] {metric}: "
            f"{actual:.4f} | required: {minimum:.4f}"
        )

        if not passed:
            all_passed = False

    return all_passed


if __name__ == "__main__":
    if run_quality_gate():
        print("\nQUALITY GATE PASSED")
        raise SystemExit(0)

    print("\nQUALITY GATE FAILED")
    raise SystemExit(1)