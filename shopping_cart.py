"""
Online Shopping Cart - Command Line Interface Application
=========================================================

A menu-driven CLI application for an online shopping cart system.
This project demonstrates core Python programming concepts including:
- Object-Oriented Programming (OOP)
- File Handling
- Exception Handling
- Menu-driven Interface
- Data Structures (Dictionary, List)
- Functions and Loops

Author: Rajat Rakesh
PRN: 20240802728
"""

import csv
import os
from datetime import datetime


# =============================================================================
# PRODUCT DATA - Using Dictionary to store product details
# =============================================================================

PRODUCTS = {
    "1": {"name": "Laptop", "price": 50000, "category": "Electronics"},
    "2": {"name": "Smartphone", "price": 25000, "category": "Electronics"},
    "3": {"name": "Headphones", "price": 2000, "category": "Electronics"},
    "4": {"name": "T-Shirt", "price": 999, "category": "Fashion"},
    "5": {"name": "Jeans", "price": 1499, "category": "Fashion"},
    "6": {"name": "Running Shoes", "price": 3500, "category": "Footwear"},
    "7": {"name": "Watch", "price": 5000, "category": "Accessories"},
    "8": {"name": "Backpack", "price": 1500, "category": "Accessories"},
}

DISCOUNT_THRESHOLD = 10000
DISCOUNT_RATE = 0.10


# =============================================================================
# SHOPPING CART CLASS - OOP Implementation
# =============================================================================

class ShoppingCart:
    """
    ShoppingCart Class
    =================
    A class to manage shopping cart operations.
    
    Attributes:
        items (list): List to store cart items
        quantities (dict): Dictionary to store quantities
    """
    
    def __init__(self):
        """Initialize empty shopping cart"""
        self.items = []
        self.quantities = {}
    
    def add_to_cart(self, product_id, quantity=1):
        """
        Add item to cart
        
        Args:
            product_id (str): Product ID to add
            quantity (int): Quantity of the product
        """
        if product_id not in PRODUCTS:
            raise ValueError(f"Invalid product ID: {product_id}")
        
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        product = PRODUCTS[product_id]
        
        if product["name"] in self.items:
            self.quantities[product["name"]] += quantity
        else:
            self.items.append(product["name"])
            self.quantities[product["name"]] = quantity
        
        print(f"\n✓ Added {quantity} x '{product['name']}' to cart!")
    
    def remove_from_cart(self, product_name):
        """
        Remove item from cart
        
        Args:
            product_name (str): Name of product to remove
        """
        if product_name not in self.items:
            raise ValueError(f"'{product_name}' not in cart")
        
        self.items.remove(product_name)
        del self.quantities[product_name]
        
        print(f"\n✓ Removed '{product_name}' from cart!")
    
    def view_cart(self):
        """
        Display all items in cart
        
        Returns:
            list: List of tuples (name, quantity, price, total)
        """
        if not self.items:
            print("\nCart is empty!")
            return []
        
        cart_details = []
        print("\n" + "=" * 70)
        print("                         SHOPPING CART")
        print("=" * 70)
        print(f"{'No.':<5} {'Product':<20} {'Qty':<8} {'Price':<12} {'Total':<12}")
        print("-" * 70)
        
        for i, item_name in enumerate(self.items, 1):
            quantity = self.quantities[item_name]
            price = self.get_product_price(item_name)
            total = price * quantity
            cart_details.append((item_name, quantity, price, total))
            print(f"{i:<5} {item_name:<20} {quantity:<8} ₹{price:<11} ₹{total:<11}")
        
        print("-" * 70)
        
        total_bill = self.calculate_total()
        print(f"{'TOTAL':<33} {'₹' + str(total_bill):<12}")
        print("=" * 70)
        
        return cart_details
    
    def get_product_price(self, product_name):
        """Get price of a product by name"""
        for product in PRODUCTS.values():
            if product["name"] == product_name:
                return product["price"]
        return 0
    
    def calculate_total(self):
        """Calculate total bill without discount"""
        total = 0
        for item_name in self.items:
            price = self.get_product_price(item_name)
            quantity = self.quantities[item_name]
            total += price * quantity
        return total
    
    def apply_discount(self):
        """
        Apply discount if total exceeds threshold
        
        Returns:
            tuple: (discount_amount, final_total)
        """
        total = self.calculate_total()
        
        if total > DISCOUNT_THRESHOLD:
            discount = total * DISCOUNT_RATE
            final_total = total - discount
            return discount, final_total
        else:
            return 0, total
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.items = []
        self.quantities = {}
        print("\n✓ Cart cleared!")
    
    def get_item_count(self):
        """Get total number of items in cart"""
        return sum(self.quantities.values())


# =============================================================================
# FILE HANDLING FUNCTIONS
# =============================================================================

def save_order_to_file(cart, discount=0, final_total=0):
    """
    Save order details to CSV file
    
    Args:
        cart (ShoppingCart): ShoppingCart object
        discount (float): Discount applied
        final_total (float): Final total after discount
    """
    filename = "order_history.csv"
    file_exists = os.path.exists(filename)
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["Order ID", "Date", "Product", "Quantity", "Price", "Total"])
            
            order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for item_name in cart.items:
                quantity = cart.quantities[item_name]
                price = cart.get_product_price(item_name)
                total = price * quantity
                writer.writerow([order_id, date, item_name, quantity, price, total])
            
            if discount > 0:
                writer.writerow(["", "", "DISCOUNT", "", "", -discount])
                writer.writerow(["", "", "FINAL TOTAL", "", "", final_total])
                writer.writerow(["", "", "---", "", "", "---"])
        
        print(f"\n✓ Order saved to '{filename}'")
        return True
    
    except IOError as e:
        print(f"\n✗ Error saving order: {e}")
        return False


def save_receipt(cart, discount=0, final_total=0):
    """
    Generate and save bill receipt as text file
    
    Args:
        cart (ShoppingCart): ShoppingCart object
        discount (float): Discount applied
        final_total (float): Final total after discount
    """
    filename = f"receipt_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    
    try:
        with open(filename, mode='w', encoding='utf-8') as file:
            file.write("=" * 70 + "\n")
            file.write("                    BILL RECEIPT\n")
            file.write("=" * 70 + "\n")
            file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write("-" * 70 + "\n")
            file.write(f"{'Product':<25} {'Qty':<8} {'Price':<12} {'Total':<12}\n")
            file.write("-" * 70 + "\n")
            
            for item_name in cart.items:
                quantity = cart.quantities[item_name]
                price = cart.get_product_price(item_name)
                total = price * quantity
                file.write(f"{item_name:<25} {quantity:<8} ₹{price:<11} ₹{total:<11}\n")
            
            file.write("-" * 70 + "\n")
            
            subtotal = cart.calculate_total()
            file.write(f"{'Subtotal':<45} ₹{subtotal:<11}\n")
            
            if discount > 0:
                file.write(f"{'Discount (10%)':<45} -₹{discount:<11}\n")
            
            file.write("=" * 70 + "\n")
            file.write(f"{'GRAND TOTAL':<45} ₹{final_total:<11}\n")
            file.write("=" * 70 + "\n")
            file.write("\nThank you for shopping with us!\n")
            file.write("-" * 70 + "\n")
        
        print(f"✓ Receipt saved to '{filename}'")
        return True
    
    except IOError as e:
        print(f"\n✗ Error saving receipt: {e}")
        return False


def read_order_history():
    """
    Read order history from CSV file using Pandas if available
    Falls back to standard CSV if Pandas not available
    """
    filename = "order_history.csv"
    
    if not os.path.exists(filename):
        print("\nNo order history found!")
        return
    
    try:
        import pandas as pd
        print("\n" + "=" * 70)
        print("                      ORDER HISTORY")
        print("=" * 70)
        df = pd.read_csv(filename)
        print(df.to_string(index=False))
        print("=" * 70)
    
    except ImportError:
        print("\nPandas not available. Using standard CSV reader:")
        try:
            with open(filename, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                print("\n" + "=" * 70)
                print("                      ORDER HISTORY")
                print("=" * 70)
                for row in reader:
                    print(row)
                print("=" * 70)
        except IOError as e:
            print(f"\n✗ Error reading order history: {e}")


# =============================================================================
# DISPLAY FUNCTIONS
# =============================================================================

def display_products():
    """Display available products"""
    print("\n" + "=" * 70)
    print("                    AVAILABLE PRODUCTS")
    print("=" * 70)
    print(f"{'ID':<5} {'Product':<25} {'Category':<20} {'Price':<12}")
    print("-" * 70)
    
    for pid, product in PRODUCTS.items():
        print(f"{pid:<5} {product['name']:<25} {product['category']:<20} ₹{product['price']:<11}")
    
    print("=" * 70)


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 50)
    print("           SHOPPING CART - MAIN MENU")
    print("=" * 50)
    print("  1. View Products")
    print("  2. Add to Cart")
    print("  3. View Cart")
    print("  4. Remove from Cart")
    print("  5. Checkout")
    print("  6. View Order History")
    print("  7. Clear Cart")
    print("  8. Exit")
    print("=" * 50)


# =============================================================================
# USER INPUT FUNCTIONS WITH EXCEPTION HANDLING
# =============================================================================

def get_valid_choice():
    """
    Get valid menu choice from user
    
    Returns:
        int: Valid choice
    """
    while True:
        try:
            choice = int(input("\nEnter your choice (1-8): "))
            if 1 <= choice <= 8:
                return choice
            else:
                print("✗ Invalid choice! Please enter a number between 1 and 8.")
        except ValueError:
            print("✗ Invalid input! Please enter a number.")


def get_valid_product_id():
    """
    Get valid product ID from user
    
    Returns:
        str: Valid product ID
    """
    display_products()
    
    while True:
        try:
            product_id = input("\nEnter product ID to add: ")
            if product_id in PRODUCTS:
                return product_id
            else:
                print("✗ Invalid product ID! Please try again.")
        except ValueError:
            print("✗ Invalid input! Please enter a valid product ID.")


def get_quantity():
    """
    Get valid quantity from user
    
    Returns:
        int: Valid quantity
    """
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            if quantity > 0:
                return quantity
            else:
                print("✗ Quantity must be greater than 0!")
        except ValueError:
            print("✗ Invalid input! Please enter a number.")


def get_product_to_remove(cart):
    """
    Get valid product name to remove from cart
    
    Args:
        cart (ShoppingCart): ShoppingCart object
    
    Returns:
        str: Product name to remove
    """
    if not cart.items:
        return None
    
    print("\nItems in cart:")
    for i, item in enumerate(cart.items, 1):
        print(f"  {i}. {item}")
    
    while True:
        try:
            choice = int(input("\nEnter item number to remove: "))
            if 1 <= choice <= len(cart.items):
                return cart.items[choice - 1]
            else:
                print("✗ Invalid choice! Please try again.")
        except ValueError:
            print("✗ Invalid input! Please enter a number.")


# =============================================================================
# MAIN FUNCTIONS
# =============================================================================

def add_item_to_cart(cart):
    """Add item to cart"""
    print("\n--- ADD TO CART ---")
    display_products()
    
    product_id = get_valid_product_id()
    quantity = get_quantity()
    
    try:
        cart.add_to_cart(product_id, quantity)
    except ValueError as e:
        print(f"✗ Error: {e}")


def remove_item_from_cart(cart):
    """Remove item from cart"""
    print("\n--- REMOVE FROM CART ---")
    
    if not cart.items:
        print("Cart is empty! Nothing to remove.")
        return
    
    product_name = get_product_to_remove(cart)
    
    if product_name:
        try:
            cart.remove_from_cart(product_name)
        except ValueError as e:
            print(f"✗ Error: {e}")


def view_cart_details(cart):
    """View cart details"""
    print("\n--- VIEW CART ---")
    cart.view_cart()


def checkout(cart):
    """Process checkout"""
    print("\n--- CHECKOUT ---")
    
    if not cart.items:
        print("Cart is empty! Add items before checkout.")
        return
    
    cart.view_cart()
    
    discount, final_total = cart.apply_discount()
    
    print("\n" + "-" * 50)
    
    if discount > 0:
        print(f"✓ Congratulations! You get ₹{discount:.2f} discount (10%)!")
        print(f"  Discount applied on total > ₹{DISCOUNT_THRESHOLD}")
        print(f"  Subtotal: ₹{cart.calculate_total()}")
        print(f"  Discount: -₹{discount:.2f}")
        print(f"  Final Total: ₹{final_total:.2f}")
    else:
        final_total = cart.calculate_total()
        print(f"  Total: ₹{final_total}")
        print(f"\n  Note: Add ₹{DISCOUNT_THRESHOLD - cart.calculate_total()} more for 10% discount!")
    
    print("-" * 50)
    
    while True:
        confirm = input("\nConfirm checkout? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            save_order_to_file(cart, discount, final_total)
            save_receipt(cart, discount, final_total)
            print("\n" + "=" * 50)
            print("     ✓ ORDER PLACED SUCCESSFULLY!")
            print("     Thank you for shopping with us!")
            print("=" * 50)
            cart.clear_cart()
            break
        elif confirm == "no":
            print("\nCheckout cancelled!")
            break
        else:
            print("✗ Invalid input! Please enter 'yes' or 'no'.")


# =============================================================================
# MAIN PROGRAM
# =============================================================================

def main():
    """
    Main function to run the shopping cart application
    """
    print("\n" + "=" * 50)
    print("   Welcome to Online Shopping Cart!")
    print("=" * 50)
    print("   A CLI-based Shopping Application")
    print("   RAJAT RAKESH (20240802728)")
    print("=" * 50)
    
    cart = ShoppingCart()
    
    while True:
        display_menu()
        choice = get_valid_choice()
        
        if choice == 1:
            display_products()
        elif choice == 2:
            add_item_to_cart(cart)
        elif choice == 3:
            view_cart_details(cart)
        elif choice == 4:
            remove_item_from_cart(cart)
        elif choice == 5:
            checkout(cart)
        elif choice == 6:
            read_order_history()
        elif choice == 7:
            cart.clear_cart()
        elif choice == 8:
            print("\n" + "=" * 50)
            print("   Thank you for using Shopping Cart!")
            print("   Goodbye!")
            print("=" * 50)
            break


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()