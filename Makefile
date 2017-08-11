install:
	pip3 install virtualenv
	virtualenv -p python3 .venv
	. .venv/bin/activate
	pip3 install -r requirements.txt

sysinstall:
	pip3 install -r requirements.txt

sysuninstall:
	pip3 uninstall -r requirements.txt
