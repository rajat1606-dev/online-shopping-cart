# Online Shopping Cart - CLI Application
Name - Rajat Rakesh 
PRN - 20240802728

A complete Python project for an Online Shopping Cart with Command Line Interface.

## Project Overview

This is a college-level Python project demonstrating:
- Object-Oriented Programming (OOP)
- File Handling (CSV, Text files)
- Exception Handling
- Menu-driven Interface
- Dictionary and List data structures
- Functions and Loops

## Features

1. **Product Display** - View available products with prices (8 products)
2. **Add to Cart** - Add items with quantity
3. **Remove from Cart** - Remove specific items
4. **View Cart** - See all items in cart with details
5. **Checkout** - Process order and generate receipt
6. **Order History** - View past orders (using Pandas if available)
7. **Discount System** - 10% discount on orders > ₹10,000
8. **Bill Receipt** - Generate text file receipt

## Running the Project

```bash
python shopping_cart.py
```

## Menu Options

```
1. View Products    - Display all available products
2. Add to Cart      - Add item(s) to shopping cart
3. View Cart       - Display cart contents
4. Remove from Cart - Remove item from cart
5. Checkout        - Process payment and complete order
6. View Order History - View past orders
7. Clear Cart      - Empty the cart
8. Exit            - Exit the application
```

## Code Structure

### 1. Data Structures (Lines 20-35)
```python
PRODUCTS = {
    "1": {"name": "Laptop", "price": 50000, "category": "Electronics"},
    ...
}
```
- Dictionary stores product details (name, price, category)
- Each product has unique ID as key

### 2. ShoppingCart Class (Lines 41-150)
**Attributes:**
- `items` - List to store product names added to cart
- `quantities` - Dictionary mapping product name to quantity

**Methods:**
- `__init__()` - Initialize empty cart
- `add_to_cart(product_id, quantity)` - Add item with quantity
- `remove_from_cart(product_name)` - Remove specific item
- `view_cart()` - Display cart contents in table format
- `calculate_total()` - Calculate bill without discount
- `apply_discount()` - Apply 10% discount if total > ₹10,000
- `clear_cart()` - Empty the cart

### 3. File Handling Functions (Lines 153-250)

**save_order_to_file()** - Saves order to CSV file
- Creates/opens order_history.csv
- Writes product details, quantity, price
- Handles IOError with exception handling

**save_receipt()** - Generates text file receipt
- Creates timestamped receipt file
- Includes all items, quantities, prices
- Shows discount and final total

**read_order_history()** - Reads past orders
- Uses Pandas if available
- Falls back to standard CSV reader

### 4. Display Functions (Lines 253-280)

**display_products()** - Shows all products in table format
**display_menu()** - Shows main menu options

### 5. Input Functions with Exception Handling (Lines 283-330)

**get_valid_choice()** - Validates menu choice (1-8)
**get_valid_product_id()** - Validates product ID exists
**get_quantity()** - Ensures positive quantity
**get_product_to_remove()** - Validates cart item selection

### 6. Main Logic Functions (Lines 333-400)

These functions handle user interactions and use if-else conditions for validation.

### 7. Main Function (Lines 403-430)

Uses while loop to keep program running until user exits.

## Sample Output

```
==================================================
           SHOPPING CART - MAIN MENU
==================================================
  1. View Products
  2. Add to Cart
  3. View Cart
  4. Remove from Cart
  5. Checkout
  6. View Order History
  7. Clear Cart
  8. Exit
==================================================

Enter your choice (1-8): 1

======================================================================
                    AVAILABLE PRODUCTS
======================================================================
ID    Product                   Category              Price       
----------------------------------------------------------------------
1    Laptop                    Electronics          ₹50000      
2    Smartphone               Electronics          ₹25000      
...
```

## Order History CSV Format

```csv
Order ID,Date,Product,Quantity,Price,Total
ORD20260424120000,Laptop,1,50000,50000
ORD20260424120000,Headphones,2,2000,4000
```

## Bonus Features Implemented

1. ✓ Quantity support for each item
2. ✓ 10% discount if total > ₹10,000
3. ✓ Bill receipt generation (text file)
4. ✓ Order history with Pandas (falls back to CSV reader)

## Requirements Mapping

| Requirement | Implementation |
|-------------|---------------|
| 1. Display products | `display_products()` function |
| 2. Add items | `add_to_cart()` method |
| 2. Remove items | `remove_from_cart()` method |
| 2. View cart | `view_cart()` method |
| 2. Checkout | `checkout()` function |
| 3. Dictionary | `PRODUCTS` dictionary |
| 4. List | `self.items` list in class |
| 5. Input/Output | `input()` and `print()` functions |
| 6. If-else | Validation in all functions |
| 7. While/for loops | Main menu loop |
| 8. Functions | Multiple functions defined |
| 9. OOP Class | `ShoppingCart` class |
| 10. Total bill | `calculate_total()` method |
| 11. File handling | CSV and text file functions |
| 12. Exception handling | try-except blocks |
| 13. Menu-driven | `display_menu()` and main loop |

## Files Generated

1. `shopping_cart.py` - Main application
2. `order_history.csv` - Order records (created after checkout)
3. `receipt_TIMESTAMP.txt` - Bill receipt (created after checkout)

## Error Handling Examples

```python
try:
    choice = int(input("Enter choice: "))
except ValueError:
    print("Please enter a valid number")

try:
    with open(filename, mode='a') as file:
        writer = csv.writer(file)
except IOError as e:
    print(f"Error saving file: {e}")
```

## For Viva Questions

1. **What data structure is used for products?**
   - Dictionary (PRODUCTS with ID as key)

2. **How is cart stored?**
   - List for items, Dictionary for quantities

3. **What OOP concept is used?**
   - Class with methods (encapsulation)

4. **How is discount calculated?**
   - If total > 10000, apply 10% discount

5. **What files are created?**
   - order_history.csv and receipt_*.txt

6. **Exception handling?**
   - ValueError for invalid input
   - IOError for file operations
