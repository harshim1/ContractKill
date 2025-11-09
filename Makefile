.PHONY: dev backend frontend seed lint test

BACKEND_DIR=backend
FRONTEND_DIR=frontend

backend:
cd $(BACKEND_DIR) && uvicorn app.main:app --reload --port 8000

frontend:
cd $(FRONTEND_DIR) && npm run dev -- --host

dev:
@echo "Starting backend and frontend"
@$(MAKE) -j2 backend frontend

seed:
cd $(BACKEND_DIR) && python -m scripts.seed

lint:
cd $(BACKEND_DIR) && ruff check app
cd $(FRONTEND_DIR) && npm run lint

test:
cd $(BACKEND_DIR) && pytest
