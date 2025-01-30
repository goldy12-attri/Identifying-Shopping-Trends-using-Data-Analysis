import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the dataset with the full path using a raw string
try:
    data = pd.read_csv(r'C:\Users\pkkhu\Documents\python\shopping_data.csv')
    print("File loaded successfully.")
except FileNotFoundError as e:
    print("Error: File not found. Please check the path.")
    print(e)
    exit()

# Print the columns and the first few rows of the DataFrame
print("Columns in DataFrame:", data.columns)
print("First few rows of the DataFrame:")
print(data.head())

# Strip any leading/trailing spaces from column names
data.columns = data.columns.str.strip()

# Convert 'Date' to datetime format with dayfirst=True
data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)

# Extract year and month for trend analysis
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Group by year and month to get total spending per month
monthly_trends = data.groupby(['Year', 'Month']).agg({'Amount': 'sum'}).reset_index()

# Create a 'Date' column for plotting
monthly_trends['Date'] = pd.to_datetime(monthly_trends[['Year', 'Month']].assign(DAY=1))

# Plotting the trends
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_trends, x='Date', y='Amount', marker='o')
plt.title('Monthly Shopping Trends')
plt.xlabel('Date')
plt.ylabel('Total Amount Spent')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

# Analyzing trends by category
category_trends = data.groupby(['Category', 'Year', 'Month']).agg({'Amount': 'sum'}).reset_index()

# Create a pivot table for better visualization
category_pivot = category_trends.pivot_table(index=['Year', 'Month'], columns='Category', values='Amount', fill_value=0)

# Plotting category trends
plt.figure(figsize=(12, 6))
category_pivot.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Shopping Trends by Category')
plt.xlabel('Year, Month')
plt.ylabel('Total Amount Spent')
plt.xticks(rotation=45)
plt.legend(title='Category')
plt.tight_layout()
plt.show()