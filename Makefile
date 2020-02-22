.SILENT: watch

rm:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -type d -iname '*egg-info' -exec rm -rdf {} +
	rm -f .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf proxy.py.egg-info
	rm -rf .pytest_cache
	rm -rf .hypothesis
	rm -rdf assets
	

test: rm
	pytest -s -v  tests/

coverage-html:
	# --cov where you want to cover
	#  tests  where your test code is 
	pytest --cov=iproxy/ --cov-report=html tests/
	open htmlcov/index.html

coverage:
	pytest --cov=iproxy/ tests/

proxy: get check haproxy

check_down:
	./check_down.sh


watch:
	while :; do  make proxy; sleep 360; done

get:
	echo "The first start you need to proxy!"
	proxychains4 python3 -m iproxy -g


check: 
	python3 -m iproxy -c ./candidates.txt

haproxy:
	haproxy -f ./haproxy.cfg -p ./haproxy.pid -D -sf `cat ./haproxy.pid`


install: uninstall
	pip install . 

uninstall:
	pip uninstall iproxy


all: rm uninstall install run 


pure-all: env-rm rm env install test run


	
upload-to-test: clean
	python3 setup.py bdist_wheel --universal
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*


upload-to-prod: clean
	python3 setup.py bdist_wheel --universal
	twine upload dist/*


freeze:
	# pipreqs will find the module the project really depneds
	pipreqs . --force

freeze-global:
	#  pip will find all the module not belong to standard  library
	pip freeze > requirements.txt


env-rm:
	rm -rdf env


env:
	python3 -m venv env
	source env/bin/activate

