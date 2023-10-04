
test:
	pytest --cov-report term-missing --cov=src -v --disable-warnings --random-order ./tests
