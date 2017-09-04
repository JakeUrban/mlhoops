ACTIVATE := .venv/bin/activate

TEST_OPTS := --cov=mlhoops --cov-fail-under=100 \
	--cov-report term-missing

venv: $(ACTIVATE)
$(ACTIVATE): requirements.txt setup.py
	@pip3 install virtualenv
	@virtualenv -p python3 .venv
	@. $(ACTIVATE); python3 -m pip install -r requirements.txt
	@. $(ACTIVATE); python3 setup.py develop
	@touch $(ACTIVATE)

install:
	pip3 install --target /usr/lib/python3/dist-packages -r requirements.txt

uninstall:
	pip3 uninstall -y -r requirements.txt

style: venv
	@. $(ACTIVATE); flake8 --exclude=.venv,migrations .

test: venv
	@. $(ACTIVATE); PYTHONPATH=. py.test -v $(TEST_OPTS)

clean:
	git clean -fdx --exclude=".*"
