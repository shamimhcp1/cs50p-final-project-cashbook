# Cashbook Management System

#### Video Demo
[Watch the Demo](https://youtu.be/Iye9pf_X6rU)

#### Description
The Cashbook Management System is a Python program that allows you to track income and expenses, add cash-in and cash-out entries, manage entries and categories, and view your overall cash flow and balance instantly. It utilizes CSV files to store data, making it a simple and easy-to-use tool for personal finance management.

## Features
- Add cash-in and cash-out entries with details such as amount, remarks, category, and date.
- Edit and delete existing entries.
- Manage categories for better organization.
- View all entries and categories.
- Calculate and display your net balance, total income, and total expenses.

## How to Use
1. Run the Python script in your terminal.
2. Choose from the available menu options:
   - Add Cash In: Record income entries.
   - Add Cash Out: Record expense entries.
   - Manage Entries: Edit or delete existing entries.
   - Manage Categories: Add, edit, or delete categories.
   - Show Balance: View your net balance and financial summary.

## Requirements
- Python 3.x
- The following Python packages:
  - `csv`
  - `tabulate`
  - `datetime`
  - `re`
  - `sys`
  - `pandas`

## Installation
1. Clone the repository or download the script.
2. Ensure you have the required packages installed using `pip install tabulate pandas`.

## Usage
1. Run the script: `python project.py`.
2. Follow the on-screen instructions to navigate the menu and manage your cashbook entries.

## Data Storage
- Categories are stored in the `categories.csv` file.
- Cashbook entries are stored in the `entries.csv` file.
- Entry types (Cash In and Cash Out) are stored in the `types.csv` file.

Please note that this project is a basic implementation of a cashbook management system and can be further customized and expanded based on your needs.

Feel free to contribute, report issues, or suggest improvements to make this tool even better for personal finance management.
