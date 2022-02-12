test:
	pytest -W=ignore::DeprecationWarning -vv



flake:
	flake8 src