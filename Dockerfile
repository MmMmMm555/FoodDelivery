FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements/base.txt  ./requirements/base.txt

RUN pip install -r requirements/base.txt

COPY . .

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

