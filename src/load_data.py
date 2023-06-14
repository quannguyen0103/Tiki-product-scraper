#!/usr/bin/env python
# coding: utf-8

import requests
import json
import pymongo
import time
import csv

#1. Import the Category_id list to Python
error_product_id = set()
error_category_id = set()
existed_id = set()
category_id = []
with open("category_id.csv", 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    for row in csv_reader:
        category_id.extend(row)

#2. Loop through category api to scrape and insert data into MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tiki_product"]
collection = db["tiki_test"]

product_counter = 0

headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
}

for cat_id in category_id:
    for page in range(1, 21):
        url = f"https://tiki.vn/api/v2/products?limit=100&include=advertisement&aggregations=1&category={cat_id}&page={page}"
        try:
            response = requests.get(url, headers=headers)
            data = json.loads(response.text)
        except Exception as e:
            error_category_id.add((cat_id, page))
            print(f"Fail to scrape data for category {cat_id}: {page}, skip. Errror: {e}")
            continue
            
        for product_data in data["data"]:
            if "id" in product_data:
                product_id = product_data["id"]
                url = f"https://tiki.vn/api/v2/products/{product_id}"
                
                # Skip if the product_id is already existed to avoid duplicate
                if product_id in existed_id:
                    print(f"Skipping duplicate product_id: {product_id}")
                else:
                    try:
                        response = requests.get(url, headers=headers)
                        json_data = json.loads(response.text)
                        collection.insert_one(json_data)
                        existed_id.add(product_id)
                        print(f"Insert data successfully for product {product_id}")
                    except Exception as e:
                        error_product_id.add(product_id)
                        print(f"Fail to insert data for product {product_id}, skip. Errror: {e}")
                        continue
                    
                    # Randomly sleep after 50 or 100 requests to avoid blocking IP
                    product_counter += 1
                    if product_counter % 100 == 50:
                        time.sleep(3)
                    elif product_counter % 100 == 0:
                        time.sleep(3)
                        
print("Inserting complete.")