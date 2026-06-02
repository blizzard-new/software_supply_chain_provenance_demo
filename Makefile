PYTHON ?= python

.PHONY: install test build manifest verify tamper clean

install:
	$(PYTHON) -m pip install -q build
	$(PYTHON) -m pip install -q -e .

test:
	$(PYTHON) -m unittest discover -s tests

build:
	$(PYTHON) -m build

manifest:
	$(PYTHON) scripts/create_local_manifest.py

verify:
	$(PYTHON) scripts/verify_artifact.py --mode local

tamper:
	$(PYTHON) scripts/tamper_demo.py --mode local

clean:
	$(PYTHON) -c "import shutil, pathlib; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dist', '.demo']]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').glob('**/*.egg-info')]"
