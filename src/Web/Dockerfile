FROM python:3.10
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT ["gunicorn", "app:app"]