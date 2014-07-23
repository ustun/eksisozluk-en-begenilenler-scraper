
init_venv:
	virtualenv --no-site-packages venv
	venv/bin/pip install -r requirements.txt

fetch_entries:
	venv/bin/python fetch_entries.py

http_server:
	npm install -g http-server
	http-server


clean:
	rm -rf data
