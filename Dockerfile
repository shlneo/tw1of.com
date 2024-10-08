FROM python:3.11-slim

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "-m", "waitress", "--host", "--port=80", "main:app"]