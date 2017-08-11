install:
	pip3 install virtualenv
	virtualenv -p python3 .venv
	. .venv/bin/activate
	pip3 install -r requirements.txt
	python3 mlhoops/mlhoops.py
