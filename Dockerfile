FROM python:3.9

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app
# Copy the .env file to the project directory


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]