FROM python:3.10-slim
RUN apt-get update
RUN python3 -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY museum_news/ .
LABEL author='mv_rogozov'
CMD ["gunicorn", "museum_news.wsgi:application", "--bind", "0:8000"]
