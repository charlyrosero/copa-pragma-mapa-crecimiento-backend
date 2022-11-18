install:
	#install commands
	pip install --upgrade pip &&\
		pip install -r requirements.txt
format:
	#format code
	black *.py library/*.py
lint:
	#flake8 ir #pylint
	pylint --disable=R,C *.py library/*.py
test:
	#test
	python -m pytest -vv --cov=library test_logic.py test_*.py
run:
	docker run -p 127.0.0.1:8080:8080 mapa-crecimiento-backend:latest
build:
	#build container
	docker build -t mapa-crecimiento-backend .
deploy:
	#deploy
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 107714303354.dkr.ecr.us-east-1.amazonaws.com
	docker build -t mapa-crecimiento-backend .
	docker tag mapa-crecimiento-backend:latest 107714303354.dkr.ecr.us-east-1.amazonaws.com/mapa-crecimiento-backend:latest
	docker push 107714303354.dkr.ecr.us-east-1.amazonaws.com/mapa-crecimiento-backend:latest
	
all: install lint test deploy