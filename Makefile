.PHONY: test test-offline test-backend-api run-backend

test: test-offline

test-offline:
	cd backend && python -m unittest discover -s tests -p '*unittest.py' -v

# Runs API integration tests when dependencies exist; otherwise reports skipped tests.
test-backend-api:
	cd backend && python -m unittest -v tests/test_api.py

run-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
