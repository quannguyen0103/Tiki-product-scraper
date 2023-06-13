#!/usr/bin/env python
# coding: utf-8

import sqlalchemy as db
from bs4 import BeautifulSoup
import pymongo
import re
import json

#1. Create a MySQL database
engine = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306")
connection = engine.connect()
engine.execute("CREATE DATABASE tiki_product;")

#2. Create a table in MySQL database
engine = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306/tiki_product")
connection = engine.connect()
metadata = db.MetaData()

product_data = db.Table("product_data",
                         metadata,
                         db.Column("id", db.Integer(), primary_key = True, unique = True),
                         db.Column("name", db.Text()),
                         db.Column("category_id", db.Integer()),
                         db.Column("category_name", db.Text()),
                         db.Column("subcategory_id", db.Integer()),
                         db.Column("subcategory_name", db.Text()),
                         db.Column("short_description", db.Text()),
                         db.Column("description", db.Text()),
                         db.Column("url", db.Text()),
                         db.Column("price", db.Float()),
                         db.Column("rating", db.Float()),
                        db.Column("quantity_sold", db.Integer()),
                        db.Column("origin", db.Text()))
metadata.create_all(engine)


#3. Find specific data from MongoDB database and insert into MySQL database
insert_query = "INSERT INTO product_data (id, name, category_id, category_name, subcategory_id, subcategory_name, short_description, description, url, price, rating, quantity_sold, origin) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["tiki_product"]
collection = database["tiki_data"]

mongo_documents = collection.find({})

for document in mongo_documents:
    id = document.get("id")
    name = document.get("name")
    category_id = document.get("breadcrumbs", [{}])[0].get("category_id")
    category_name = document.get("breadcrumbs", [{}])[0].get("name")
    subcategory_id = document.get("categories", {}).get("id")
    subcategory_name = document.get("categories", {}).get("name")
    short_description = document.get("short_description")
    description_data = document.get("description")
    if description_data is not None:
        soup = BeautifulSoup(description_data, "html.parser")
        description_list = [p.get_text(strip=True).strip("- ").rstrip(".") for p in soup.find_all('p')]
        description = "; ".join(description_list)
    else:
        description = None
    url = document.get("short_url")
    price = document.get("list_price")
    rating = document.get("rating_average")
    quantity_sold = document.get("all_time_quantity_sold")
    specifications = document.get("specifications", [{}])
    if len(specifications) > 0:
        attributes = specifications[0].get("attributes")
    if attributes is not None and len(attributes) > 0:
        for att in attributes:
            if "origin" in att.values():
                origin = att["value"]
    
    connection.execute(insert_query, (id, name, category_id, category_name, subcategory_id, subcategory_name,
                                      short_description, description, url, price, rating, quantity_sold, origin))
    print(f"Insert data successfully for product {id}")
print("Insert data completely.")