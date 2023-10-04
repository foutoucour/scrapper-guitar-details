build:
	poetry build
test:
	poetry run pytest --cov-report xml --cov-report term-missing --cov=src -v --disable-warnings --random-order ./tests
