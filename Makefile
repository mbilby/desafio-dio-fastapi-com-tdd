run:
	@uvicorn store.app:app --reload

precommit-install:
	@poetry run pre-commit install