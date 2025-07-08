run:
	@uvicorn store.app:app --reload

precommit-install:
	@pre-commit install

test:
	@pytest
