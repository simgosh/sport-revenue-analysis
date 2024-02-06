import pandas as pd 
import numpy as np 

# Reading in and formatting the data

brands = pd.read_csv("brands.csv")
finance = pd.read_csv("finance.csv")
info = pd.read_csv("info.csv")
reviews = pd.read_csv("reviews.csv")

# Formatting the datasets for analysis
print(brands.head(5))
print(finance.head(5))
print(info.head(5))
print(reviews.head(5))

#Merged all datas 
merged = brands.merge(finance, on="product_id")
merged = merged.merge(info, on="product_id")
merged = merged.merge(reviews, on="product_id")
merged.dropna(inplace=True)
print(merged)

# Add price labels based on listing_price quartiles
merged["price_label"]=pd.qcut(merged["listing_price"], q=4, labels=["Budget", "Average", "Expensive", "Elite"])

# Group by brand and price_label to get volume and mean revenue
adidas_vs_nike = merged.groupby(["brand", "price_label"], as_index=False).agg(
    num_products=("price_label", "count"),
    mean_revenue = ("revenue", "mean")
).round(2)
print(adidas_vs_nike.head())

# Store the length of each description
merged["description_length"] = merged["description"].str.len()

# Upper description length limits
lengths= [0, 100, 200, 300, 400 ,500, 600, 700]

# Description length labels
labels = ["100", "200" ,"300" ,"400" ,"500", "600", "700"]

# Cut into bins
merged["description_length"]=pd.cut(merged["description_length"], bins=lengths, labels=labels)

# Group by the bins
description_lengths = merged.groupby(["rating", "reviews"], as_index=False).agg(
    mean_rating = ("rating", "mean"),
    num_reviews = ("reviews", "count")
).round(2)
print(description_lengths.head())

# List of footwear keywords
mylist = "shoe*|trainer*|foot*"

# Filter for footwear products
shoe = merged[merged["description"].str.contains(mylist)]

## Filter for footwear products
clothing = merged[~merged.isin(shoe["product_id"])]

# Remove null product_id values from clothing DataFrame
clothing.dropna(inplace=True)
print(clothing.head)

# Create product_types DataFrame
product_types = pd.DataFrame({"num_clothing_products" : len(clothing),
                              "median_clothing_revenue" : clothing["revenue"].median(),
                              "num_footwear_products" : len(shoe),
                              "median_footwear_revenue" : shoe["revenue"].median()
}, index=[0])

print(product_types)
