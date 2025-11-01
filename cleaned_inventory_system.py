"""
Inventory Management System

A simple inventory tracking system that allows adding, removing,
and querying stock levels. Includes persistence to JSON files.
"""

import json
from datetime import datetime


class InventoryManager:
    """Manages inventory stock levels with persistence capabilities."""

    def __init__(self):
        """Initialize an empty inventory."""
        self.stock_data = {}

    def add_item(self, item, qty, logs=None):
        """
        Add quantity to an item's stock.

        Args:
            item (str): Name of the item to add
            qty (int): Quantity to add (must be non-negative)
            logs (list, optional): List to append log entries to

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If item is empty or qty is negative or wrong type
            TypeError: If arguments are of incorrect types
        """
        # Initialize logs if not provided (fixes mutable default argument)
        if logs is None:
            logs = []

        # Input validation - check types first
        if not isinstance(item, str):
            raise TypeError(
                f"Item must be a string, got {type(item).__name__}")

        if not item.strip():
            raise ValueError("Item name cannot be empty")

        if not isinstance(qty, int):
            raise TypeError(
                f"Quantity must be an integer, got {type(qty).__name__}")

        if qty < 0:
            raise ValueError(f"Quantity cannot be negative, got {qty}")

        # Add or update item
        self.stock_data[item] = self.stock_data.get(item, 0) + qty

        # Log the action with f-string (fixes old string formatting)
        log_entry = f"{datetime.now()}: Added {qty} of {item}"
        logs.append(log_entry)

        return True

    def remove_item(self, item, qty):
        """
        Remove quantity from an item's stock.

        Args:
            item (str): Name of the item to remove
            qty (int): Quantity to remove

        Returns:
            bool: True if successful, False if item not found

        Raises:
            KeyError: If item doesn't exist in inventory
            ValueError: If quantity is invalid
        """
        # Input validation
        if not isinstance(qty, int) or qty < 0:
            raise ValueError("Quantity must be a non-negative integer")

        # Specific exception handling (fixes bare except)
        if item not in self.stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        self.stock_data[item] -= qty

        # Remove item if stock reaches zero or below
        if self.stock_data[item] <= 0:
            del self.stock_data[item]

        return True

    def get_qty(self, item):
        """
        Get the current quantity of an item.

        Args:
            item (str): Name of the item to query

        Returns:
            int: Current quantity of the item, or 0 if not found

        Raises:
            KeyError: If item doesn't exist in inventory
        """
        if item not in self.stock_data:
            raise KeyError(f"Item '{item}' not found in inventory")

        return self.stock_data[item]

    def load_data(self, file="inventory.json"):
        """
        Load inventory data from a JSON file.

        Args:
            file (str): Path to the JSON file to load

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        # Use context manager and encoding (fixes file handling issues)
        try:
            with open(file, "r", encoding="utf-8") as f:
                self.stock_data = json.load(f)
        except FileNotFoundError:
            print(f"Warning: File '{file}' not found. "
                  f"Starting with empty inventory.")
            self.stock_data = {}
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in file '{file}': {e}")
            raise

    def save_data(self, file="inventory.json"):
        """
        Save inventory data to a JSON file.

        Args:
            file (str): Path to the JSON file to save to

        Raises:
            IOError: If there's an error writing to the file
        """
        # Use context manager and encoding (fixes file handling issues)
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.stock_data, f, indent=2)
        except IOError as e:
            print(f"Error saving to file '{file}': {e}")
            raise

    def print_data(self):
        """Print a formatted report of all items in inventory."""
        print("\n=== Items Report ===")
        if not self.stock_data:
            print("Inventory is empty")
        else:
            for item, quantity in self.stock_data.items():
                print(f"{item} -> {quantity}")
        print("====================\n")

    def check_low_items(self, threshold=5):
        """
        Find items with stock below a threshold.

        Args:
            threshold (int): Minimum stock level (default: 5)

        Returns:
            list: Names of items below the threshold
        """
        result = []
        for item, quantity in self.stock_data.items():
            if quantity < threshold:
                result.append(item)
        return result


def main():
    """
    Main function demonstrating the inventory system.

    Demonstrates adding items, error handling, querying stock,
    and persistence operations.
    """
    # Create inventory manager instance (fixes global variable issue)
    inventory = InventoryManager()

    print("=== Inventory System Demo ===\n")

    # Add items with proper error handling
    try:
        inventory.add_item("apple", 10)
        print("✓ Added 10 apples")
    except (ValueError, TypeError) as e:
        print(f"✗ Error adding apples: {e}")

    # Demonstrate validation: negative quantity
    try:
        inventory.add_item("banana", -2)
        print("✓ Added -2 bananas")
    except ValueError as e:
        print(f"✗ Error adding bananas: {e}")

    # Demonstrate validation: invalid types
    try:
        inventory.add_item(123, "ten")
        print("✓ Added invalid item")
    except (ValueError, TypeError) as e:
        print(f"✗ Error adding item with invalid types: {e}")

    # Remove items with error handling
    try:
        inventory.remove_item("apple", 3)
        print("✓ Removed 3 apples")
    except (KeyError, ValueError) as e:
        print(f"✗ Error removing apples: {e}")

    # Try to remove non-existent item
    try:
        inventory.remove_item("orange", 1)
        print("✓ Removed 1 orange")
    except KeyError as e:
        print(f"✗ Error removing orange: {e}")

    # Query stock levels
    try:
        apple_qty = inventory.get_qty("apple")
        print(f"✓ Apple stock: {apple_qty}")
    except KeyError as e:
        print(f"✗ Error getting apple quantity: {e}")

    # Check low stock items
    low_items = inventory.check_low_items()
    print(f"✓ Low stock items: {low_items if low_items else 'None'}")

    # Save and load data
    try:
        inventory.save_data()
        print("✓ Saved inventory to file")
    except IOError as e:
        print(f"✗ Error saving: {e}")

    try:
        inventory.load_data()
        print("✓ Loaded inventory from file")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"✗ Error loading: {e}")

    # Print final inventory state
    inventory.print_data()

    # Demonstrate direct print instead of eval() (fixes security issue)
    print("Direct execution (safe - no eval used)")


# Standard Python entry point
if __name__ == "__main__":
    main()
