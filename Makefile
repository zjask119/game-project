pep:
	find . -name "*.pyc" -delete
	-find . -name __pycache__ -not -path "./.tox/*" -delete
	-autopep8 -ri .
	-isort -rc .
	-flake8 . --ignore=C901,E128,E731,E302,E305,W503,W504