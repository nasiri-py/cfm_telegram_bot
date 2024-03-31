tel:
	python main.py runtel
	watchmedo auto-restart --patterns="*.py" --recursive --directory "./" python main.py runtel

env:
	source env.sh