FROM python:3.8-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y libpq-dev gcc

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the Flask API and ETL scripts when the container launches
CMD ["python", "api/app.py"]
