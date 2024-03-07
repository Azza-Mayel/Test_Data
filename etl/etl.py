import csv
import os
import requests
import psycopg2

class ETL:
    def __init__(self):
        self.headers = {
            'authority': 'www.e.leclerc',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            '#cookie': '_cs_mk=0.6985130207180748_1709560984645; OptanonAlertBoxClosed=2024-03-04T14:03:07.521Z; _gcl_au=1.1.175852746.1709560988; _ga=GA1.1.584790246.1709560988; s_muid=ebe596be-a0d9-469e-b6f1-161e258e7e52; _gid=GA1.2.1144513384.1709560988; _cs_c=0; FPID=FPID2.2.vok6VyhI%2BtPMHM1LeGM2iMTacEzUoUTvscgPOlz%2B1q0%3D.1709560988; FPLC=k0Z0hS79CbguSONdIhoEGRWy6aCcV2TWf3LU%2FVCCksJKw5Gbi%2FReoCsekSNovIQ%2FmaR98uZEC2ahwqOBQ5U6DvFFyOhaZTY%2FbOSAwNUD9wkPFxLi7Dt3P2DmioJKlA%3D%3D; FPAU=1.1.175852746.1709560988; _scid=e1095309-e5b7-4cc2-feb8-0bd524522857; _fbp=fb.1.1709560988190.1961962724; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Mar+04+2024+15%3A04%3A04+GMT%2B0100+(UTC%2B01%3A00)&version=6.27.0&isIABGlobal=false&hosts=&consentId=8c86a039-7788-4c02-879c-92e80abd0ff2&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C4%3A1%2C3%3A1%2C2%3A1&geolocation=GB%3B&AwaitingReconsent=false; _uetsid=eda2ae70da2f11ee9a1d130e9aed57a2; _uetvid=eda2dab0da2f11ee8faea9902d1b6195; cto_bundle=WwtyCl9Kb25mS2w0aldHUzlBTGdlc3NkVld5JTJCUDV2ZDBnUDQxUFhqQ3Zoa01hbnhxZ0RkenpOdG10czd6MG12cUF4b0ZtdzlKY3R1U1pOWWFDMHRpTFNFb2lSQ2NYNjE3eTF3Q1JoVEJiTlJHenh0ejJMemt2NlhtdXhiTFlha1JEYTRUREFUM2dEakpJOVQlMkZ0ZFlNdjNyVDl3JTNEJTNE; _cs_id=f1b08cdd-8a74-ab20-8204-da35c3049214.1709560988.1.1709561933.1709560988.1707406892.1743724988138.1; _cs_s=11.5.0.1709563733743; _ga_NCQNKB4YT9=GS1.1.1709560987.1.1.1709561933.0.0.0; ABTastySession=mrasn=&lp=https%253A%252F%252Fwww.e.leclerc%252F; ABTasty=uid=a6vmxcbc6etgvp0p&fst=1709560984555&pst=-1&cst=1709560984555&ns=1&pvt=15&pvis=15&th=951906.1186386.9.9.1.1.1709560985595.1709561932521.1.1_1146393.1420567.11.11.1.1.1709560991087.1709561932468.1.1_1149244.1424377.12.12.1.1.1709560985036.1709561932490.1.1&eas=azltaWZPdjF8RW1vdGl2ZXM=',
            'referer': 'https://www.e.leclerc/cat/coiffure?page=2',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        }

    def scrape_data(self):
        response = requests.get(
            'https://www.e.leclerc/api/rest/live-api/product-search?language=fr-FR&size=32&sorts=%5B%5D&page=2&categories=%7B%22code%22:%5B%22NAVIGATION_coiffure%22%5D%7D&filters=%7B%22oaf-sign-code%22:%7B%22value%22:%5B%220100%22,%220000%22%5D%7D%7D&pertimmContexts=%5B%5D',
            headers=self.headers,
        )
        data = response.json()
        return data

    def save_to_csv(self, data, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'price'])
            writer.writeheader()
            for product in data['items']:
                name = product['label']
                price = product['variants'][0]['offers'][0]['basePrice']['price']['price']
                writer.writerow({'name': name, 'price': price})

    def extract_from_csv(self, filename):
        data = []
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    def transform(self, data):
        transformed_data = []
        for item in data[:10]:
            transformed_data.append({
                'name': item['name'],
                'price': float(item['price'])
            })
        return transformed_data

    def load_to_database(self, data):
        try:
            DB_USERNAME = os.getenv('DB_USERNAME')
            DB_PASSWORD = os.getenv('DB_PASSWORD')
            DB_HOST = os.getenv('DB_HOST')  
            DB_PORT = os.getenv('DB_PORT')        
            DB_NAME = os.getenv('DB_NAME')
            con = psycopg2.connect(
                database=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                price NUMERIC
            );''')

            for product in data:
                cur.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (product['name'], product['price']))

            con.commit()
            print("Data loaded successfully.")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if con:
                cur.close()
                con.close()
