ACTIVATE := .venv/bin/activate

venv: requirements.txt
	@pip3 install virtualenv
	@virtualenv -p python3 .venv
	@. $(ACTIVATE); python3 -m pip install -r requirements.txt
	@touch $(ACTIVATE)

install:
	@pip3 install --target /usr/lib/python3/dist-packages -r requirements.txt

uninstall:
	@pip3 uninstall --target /usr/lib/python3/dist-packages -r requirements.txt
