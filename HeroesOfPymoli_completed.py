#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----
# 
# * Three of the most popular items are also the most profitable. The ones that are not are 1. Extraction and 2. Pursuit.
# 
# * Women appear to purchase more per person than men, but because their sample size is 1/6 of the men, it's hard to conclude that it's significant.
# 
# 

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[27]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)

purchase_data.head(20)


# ## Player Count

# * Display the total number of players
# 

# In[28]:


# get the length of the Screen Names
total_players = len(purchase_data["SN"].unique())

# Create DataFrame
tp_df = pd.DataFrame({"Total Players":total_players}, index=[0])
tp_df


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[29]:


# Calculate the items
unique_items = len(purchase_data["Item ID"].value_counts())

average_price = purchase_data["Price"].mean()

num_purchases = len(purchase_data["Purchase ID"].value_counts())

total_revenue = purchase_data["Price"].sum()

# Create the data frame
summary_df = pd.DataFrame({"Number of Unique Items": unique_items,
                              "Average Price": average_price,
                              "Number of Purchases": num_purchases,
                              "Total Revenue": total_revenue}, index=[0])
# format the values
pd.options.display.float_format = '${:.2f}'.format


summary_df


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[30]:


# Create grouping for Gender
gender_group = purchase_data.groupby('Gender')

total_gender_values = gender_group.nunique()["SN"]
total_gender_values

percentage_players = total_gender_values / total_gender_values.sum() * 100
percentage_players

gender_summary_table = pd.DataFrame({"Total Count": total_gender_values,
                                    "Percentage of Players": percentage_players})

# sort Z - A and format
gender_summary_table.sort_values(["Total Count"], ascending = False).style.format({"Percentage of Players":"{:.2f}"})




# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[31]:


# Count purchases by Gender
purchase_count = gender_group['Purchase ID'].count()

# Get average purchase price
avg_purchase_price = gender_group['Price'].mean()

# total purchase value
total_purchase_value = gender_group['Price'].sum()

# Get average purchase per person
avg_total_purchase_per_person = total_purchase_value / total_gender_values

gender_purchases = pd.DataFrame({"Purchase Count": purchase_count, 
                                    "Average Purchase Price": avg_purchase_price,
                                    "Average Purchase Value":total_purchase_value,
                                    "Avg Purchase Total per Person": avg_total_purchase_per_person})


# Create Index
gender_purchases.index.name = "Gender"

#Format
gender_purchases.style.format({"Average Purchase Value":"${:,.2f}",
                                  "Average Purchase Price":"${:,.2f}",
                                  "Avg Purchase Total per Person":"${:,.2f}"})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[32]:


# Create age bins 
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Segment and sort age values into above bins
purchase_data["Age Group"] = pd.cut(purchase_data["Age"],age_bins, labels=group_names)
purchase_data

# Create new data frame with the added "Age Group" and group it
age_grouped = purchase_data.groupby("Age Group")

# Count total players by age category
total_count_age = age_grouped["SN"].nunique()

# Calculate percentages by age category 
percentage_by_age = (total_count_age/total_players) * 100

# Create data frame with obtained values
age_demographics = pd.DataFrame({"Percentage of Players": percentage_by_age, "Total Count": total_count_age})

# Format the data frame with no index name in the corner
age_demographics.index.name = None

# Format percentage with two decimal places 
age_demographics.style.format({"Percentage of Players":"{:,.2f}"})


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[33]:


# Count purchases by age group
purchase_count_age = age_grouped["Purchase ID"].count()

# Obtain average purchase price by age group 
avg_purchase_price_age = age_grouped["Price"].mean()

# Calculate total purchase value by age group 
total_purchase_value = age_grouped["Price"].sum()

# Calculate the average purchase per person in the age group 
avg_purchase_per_person_age = total_purchase_value/total_count_age

# Create data frame with obtained values
age_data_table = pd.DataFrame({"Purchase Count": purchase_count_age,
                                 "Average Purchase Price": avg_purchase_price_age,
                                 "Total Purchase Value":total_purchase_value,
                                 "Average Purchase Total per Person": avg_purchase_per_person_age})

# Format the data frame with no index name in the corner
age_data_table.index.name = None

# Format with currency style
age_data_table.style.format({"Average Purchase Price":"${:,.2f}",
                               "Total Purchase Value":"${:,.2f}",
                               "Average Purchase Total per Person":"${:,.2f}"})


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[34]:


# Group purchases by screen names
spender_data = purchase_data.groupby("SN")

# Count the total purchases by name
purchase_count_spender = spender_data["Purchase ID"].count()

# Calculate the average purchase by name 
avg_purchase_price_spender = spender_data["Price"].mean()

# Calculate purchase total 
purchase_total_spender = spender_data["Price"].sum()

# Create data frame with obtained values
top_spenders = pd.DataFrame({"Purchase Count": purchase_count_spender,
                             "Average Purchase Price": avg_purchase_price_spender,
                             "Total Purchase Value":purchase_total_spender})

# Sort in descending order to obtain top 5 spender names 
formatted_spenders = top_spenders.sort_values(["Total Purchase Value"], ascending=False).head()

# Format with currency style
formatted_spenders.style.format({"Average Purchase Total":"${:,.2f}",
                                 "Average Purchase Price":"${:,.2f}", 
                                 "Total Purchase Value":"${:,.2f}"})


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[35]:


# Create new data frame with items related information 
items = purchase_data[["Item ID", "Item Name", "Price"]]

# Group the item data by item id and item name 
item_stats = items.groupby(["Item ID","Item Name"])

# Count the number of times an item has been purchased 
purchase_count_item = item_stats["Price"].count()

# Calcualte the purchase value per item 
purchase_value = (item_stats["Price"].sum()) 

# Find individual item price
item_price = purchase_value/purchase_count_item

# Create data frame with obtained values
most_popular_items = pd.DataFrame({"Purchase Count": purchase_count_item, 
                                   "Item Price": item_price,
                                   "Total Purchase Value":purchase_value})

# Sort in descending order to obtain top spender names and provide top 5 item names
popular_formatted = most_popular_items.sort_values(["Purchase Count"], ascending=False).head()

# Format with currency style
popular_formatted.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[36]:


# Take the most_popular items data frame and change the sorting to find highest total purchase value
popular_formatted = most_popular_items.sort_values(["Total Purchase Value"],
                                                   ascending=False).head()
# Format with currency style
popular_formatted.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# In[ ]:




