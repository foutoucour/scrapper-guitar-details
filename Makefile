build:
	poetry build
test:
	poetry run pytest --cov-report lcov --cov-report term-missing --cov=src -v --disable-warnings --random-order ./tests
