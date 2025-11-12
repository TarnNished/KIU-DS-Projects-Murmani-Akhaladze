# Introduction to Data Science with Python – Project 2  

## Pandas Data Manipulation  

---

##  Project Description  

This project applies **Python**, **Pandas**, and **NumPy** for comprehensive data exploration, cleaning, and quality control.  
The dataset simulates an e-commerce environment with three interrelated files:

- **customers.csv** – Customer demographic and contact information  
- **products.csv** – Product catalog with prices and stock levels  
- **transactions.csv** – Purchase records linking customers and products  

The main objective is to identify and correct data quality issues such as **missing values, duplicates, inconsistent text formats, outliers, and invalid data types**, ensuring that the resulting datasets are clean, standardized, and ready for downstream analysis.

---

##  Student Information  

**Name:** Murmani Akhaladze  
**Date:** November 2025  
**Course:** Introduction to Data Science with Python  

---

## ️ How to Run the Code  

### Steps  

1. **Open the notebook**  
   - Launch **Jupyter Notebook** or **VS Code**  
   - Open the file `task.ipynb`

2. **Run all cells sequentially**  
   - From the menu, select → `Cell → Run All`  
   - The notebook automatically performs data exploration, cleaning, and validation  

3. **Outputs produced**  
   - `customers_clean.csv`  
   - `products_clean.csv`  
   - `transactions_clean.csv`  

---

##  Brief Summary of Cleaning Decisions  

### Customers  
- Removed rows with missing emails  
- Dropped duplicate entries  
- Extracted numeric values from `age` strings and converted them to integers  
- Standardized country names (`us`, `usa` → `United States`)  
- Lowercased all email addresses  

### Products  
- Converted `price` to numeric and replaced negative values with `NaN`  
- Filled missing prices using the **median** within each category  
- Capped extreme `stock` values at **500**  
- Standardized category names and trimmed whitespace  
- Removed duplicate records  

### Transactions  
- Filled missing `quantity` values with the **mode**  
- Removed duplicate `transaction_id`s  
- Ensured all `customer_id`s exist in the Customers table  
- Converted `transaction_date` to datetime and removed future dates  
- Standardized payment method capitalization  

 **After cleaning:** All datasets contain **no missing values**, **no duplicates**, and **consistent formats** across all fields.  

---
