# Development workflow

Use this workflow for each new financial feature.

1. Derive the required mathematics in notes (do not code yet).
2. Write the function signature and expected inputs/outputs in code.
3. Add failing tests for deterministic examples.
4. Implement with explicit Python first.
5. Keep only one formula in one place.
6. Compare behaviour with any intermediate NumPy/Pandas alternatives if useful.
7. Review for readability and edge cases.
8. Commit with a clear message.

## Running tests

```bash
pytest -q
```

## Current structure notes

- `src/finance_data_project/analytics.py` → core calculations.
- `src/finance_data_project/market_data.py` → market-data loading + schema checks.
- `src/finance_data_project/cli.py` → command-line workflow.
- `src/finance_data_project/validation.py` → shared validation helpers.
- `src/finance_data_project/models.py` → typed result containers.

## Review expectations

- keep functions focused and explicit
- prefer clear names over short cleverness
- avoid changing existing formula semantics
- keep tests updated with each behaviour change
