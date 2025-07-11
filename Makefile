run:
	@uvicorn store.app:app --reload

precommit-install:
	@pre-commit install

test:
	@pytest

specific-test:
	@pytest -s -rx -k $(K) --pdb ./tests/
