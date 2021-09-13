.PHONEY: build, run, clean, zip, comp

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)/bin/activate
	$(PYTHON) main.py $(file)

build: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt


clean:
	rm -rf __pycache__
	rm -rf $(VENV)

comp: 
	compare -fuzz 2% $(file) test/correct_files/$(file) ae.png

zip: 
	tar -czvf submission.tar.gz src implemented.txt requirements.txt Makefile