FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
# Пользователь для celery и права на рабочую директорию, в целях безопасности,
#чтобы не запускать его от суперюзера
RUN useradd -m celery && chown -R celery /code
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
USER celery
COPY . .
EXPOSE 8000
