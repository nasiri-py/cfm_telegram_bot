tel:
	watchmedo auto-restart --patterns="*.py" --recursive --directory "./" python main.py runtel

env:
	source env.sh

upload:
	python main.py upload $(file)
