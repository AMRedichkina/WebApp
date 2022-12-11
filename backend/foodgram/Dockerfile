FROM python:3.8-slim
COPY requirements.txt /
RUN pip install -r requirements.txt
WORKDIR /backend
COPY . /
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000