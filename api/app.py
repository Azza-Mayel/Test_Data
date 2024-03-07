import sys
import os
from flask import Flask, jsonify
import psycopg2
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)
from etl import ETL

app = Flask(__name__)

def get_database_connection():
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')  
    DB_PORT = os.getenv('DB_PORT')        
    DB_NAME = os.getenv('DB_NAME')        
    return psycopg2.connect(
        database=DB_NAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route('/read/first-chunk')
def read_first_chunk():
    try:
        etl = ETL()
        scraped_data = etl.scrape_data()
        etl.save_to_csv(scraped_data, 'products.csv')
        extracted_data = etl.extract_from_csv('products.csv')
        transformed_data = etl.transform(extracted_data)
        etl.load_to_database(transformed_data)
        con = get_database_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM products LIMIT 10")
        rows = cur.fetchall()
        result = [{'name': row[1], 'price': float(row[2])} for row in rows]
        return jsonify(result)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        if 'con' in locals():
            cur.close()
            con.close()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
