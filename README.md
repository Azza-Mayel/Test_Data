# Beauty Store API with ETL Pipeline
This project is a Flask API that scrapes data from the beautystore.tn website, performs an ETL (Extract, Transform, Load) process on the data, and exposes it through an API endpoint. The ETL process extracts product information, transforms it into a structured format, and loads it into a PostgreSQL database. Additionally, the project includes unit tests for the API endpoints.

# Project Structure
The project is structured as follows:

app.py: Contains the Flask application with API endpoints. etl.py: Defines the ETL class responsible for extracting, transforming, and loading data. Dockerfile: Defines the Docker image for the Flask application. app_dep.yaml: Kubernetes deployment configuration for deploying the Flask application. app_test.py: Unit tests for the Flask application.

# Usage
Run the Flask application: python app.py

Once the Flask application is running, you can access the API endpoints at http://localhost:5000.
The API provides a /read/first-chunk endpoint that returns the first 10 products from the database.
# Testing
Run the unit tests: python -m unittest app_test

Note: Environment Variables (.env) You must create a .env file with the database credentials mentioned above before running the application or tests.
