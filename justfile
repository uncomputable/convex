# Run type checker
type:
    mypy convex.py fuzz.py

# Run code linter
lint:
    pylint convex.py fuzz.py

# Run unit tests
test:
    python -m unittest convex.TestConvex

# Check code (CI)
check:
    just type
    just lint
    just test

# Run fuzzer with dev profile
fuzz:
    python fuzz.py

# Run fuzzer with CI profile
fuzz-ci:
    HYPOTHESIS_PROFILE="ci" python fuzz.py
