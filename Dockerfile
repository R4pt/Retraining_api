FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

Copy . /app

EXPOSE 8000

CMD ["uvicorn","endpoints:app", "--host", "0.0.0.0", "--port", "8000"]