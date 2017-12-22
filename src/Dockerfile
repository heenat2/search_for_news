FROM python:2
WORKDIR /app
ADD . /app
RUN apt-get update && pip install -r requirements.txt
RUN export PYTHONPATH=/app
EXPOSE 5000
CMD ["python", "-m", "app"]
