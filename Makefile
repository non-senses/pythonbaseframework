startdev:
	docker run -it --rm --volume `pwd`:/code --name flaskpoc --publish 5000:5000 flask_poc make startdevindocker

startdevindocker:
	FLASK_ENV=development FLASK_APP=wsgi flask run --host=0.0.0.0

startprod:
	FLASK_ENV=production python wsgi.py

