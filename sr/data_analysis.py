#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import sqlalchemy as db
import pandas as pd

# Connect to MySQL
engine = db.create_engine("mysql+mysqlconnector://root:password@localhost:3306/tiki_product")
connection = engine.connect()


# Load table to Python
query = "select id, name, category_name, subcategory_name, origin, quantity_sold, rating, price from product_data"
data_raw = pd.read_sql_query(query, engine)
data = data_raw.copy()


#1. Count products based on Category
data.category_name.fillna("unknown", inplace = True)
category_data = data.groupby("category_name").category_name.size().reset_index(name = "num_product")
sort_category_data = category_data.sort_values("num_product", ascending = False).head(6)

fig, ax = plt.subplots(figsize = (16, 8))
ax.bar(sort_category_data.category_name,
       sort_category_data.num_product,
       color = "g")

category_value = sort_category_data.category_name.tolist()[:6]
ax.set_xticklabels(category_value, fontsize = 12, rotation=45)
ax.set_yticks([])
for i, v in enumerate(sort_category_data.num_product):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontsize = 12)
ax.set_title("Number of products in each Category", fontsize = 20)


#2. Count products based on Origin
data.origin.fillna("unknown", inplace = True)
origin_data = data.groupby("origin").size().reset_index(name = "num_product")
sort_origin_data = origin_data.sort_values("num_product", ascending = False).head(10)
labels = sort_origin_data.origin.tolist()[:10]
fig, ax = plt.subplots(figsize = (16, 8))
ax.pie(sort_origin_data.num_product,
       labels = labels,
       autopct='%1.1f%%',
       textprops={'fontsize': 5})


#3. Top 10 products with the highest quantity sold, highest rating, and lowest price
top_10 = data.sort_values(["quantity_sold", "rating", "price"], ascending = [False, False, True]).head(10)
top10_series = top_10[["name", "quantity_sold", "rating", "price"]].reset_index(drop = True)
top10_series.index = range(1, 11)