run:
	@uvicorn store.app:app --reload

precommit-install:
	@pre-commit install

test:
	@pytest -v ./tests/schemas/test_product.py
	@pytest -v ./tests/controllers/test_product.py
	@pytest -v ./tests/usecases/test_product.py

specific-test:
	@pytest -s -rx -k $(K) --pdb ./tests/
