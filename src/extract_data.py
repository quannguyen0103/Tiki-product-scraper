#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pymongo
import re
import csv

# Defind a function to extract ingredient data
def extract_ingredient(collection):
    pattern = re.compile("thành phần:", re.IGNORECASE)
    query = {"description": {"$regex": pattern}}
    mongo_documents = collection.find(query)

    for document in mongo_documents:
        product_id = document.get("id")
        soup = BeautifulSoup(document["description"], "html.parser")
        description = []
        for tag in soup.find_all():
            if tag.string:
                description.append(tag.string.strip("- "))
        for desc in description:
            if 'thành phần:' in desc.lower():
                ingredient = desc.lower().find('thành phần:')
                if ingredient != -1:
                    ingredient = "thành phần: " + desc[ingredient + len('thành phần:'):].strip()
        if ingredient.strip() == "thành phần:":
            continue
        else:
            data = str(product_id) + ', ' + ingredient.rstrip(".")
            with open("ingredient.csv", "a", newline="", encoding="utf-16") as f:
                writer = csv.writer(f)
                writer.writerow([data])
            print(f"product {product_id} written to ingredient.csv successfully.")

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tiki_product"]
collection = db["tiki_data"]
extract_ingredient(collection)
