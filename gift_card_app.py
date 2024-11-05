from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt
import sys
import sqlite3

# Database setup function
def init_db():
    conn = sqlite3.connect("giftcards.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_number TEXT UNIQUE NOT NULL,
        card_holder TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Main Application Class
class GiftCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gift Card Management")
        self.setGeometry(100, 100, 500, 400)

        # Main layout and tabs
        self.tabs = QTabWidget()
        
        # Add tabs
        self.add_tab = QWidget()
        self.view_tab = QWidget()
        
        # Set up the Add Card tab
        self.setup_add_tab()

        # Set up the View Cards tab
        self.setup_view_tab()

        # Add the tabs to the main tab widget
        self.tabs.addTab(self.add_tab, "Add Card")
        self.tabs.addTab(self.view_tab, "View Cards")

        # Set central widget
        self.setCentralWidget(self.tabs)

    def setup_add_tab(self):
        # Use a form layout for a more compact look
        layout = QFormLayout()

        # Input fields
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter Card Number")
        
        self.card_holder_input = QLineEdit()
        self.card_holder_input.setPlaceholderText("Enter Card Holder Name")
        
        self.balance_input = QLineEdit()
        self.balance_input.setPlaceholderText("Enter Balance")
        
        # Add Button
        self.add_button = QPushButton("Add Card")
        self.add_button.clicked.connect(self.add_card)
        
        # Add widgets to layout
        layout.addRow(QLabel("<b>Add New Gift Card</b>"))  # Bold for emphasis
        layout.addRow("Card Number:", self.card_number_input)
        layout.addRow("Card Holder:", self.card_holder_input)
        layout.addRow("Balance:", self.balance_input)
        layout.addRow(self.add_button)

        # Reduce margins and spacing
        layout.setContentsMargins(20, 10, 20, 10)  # left, top, right, bottom
        layout.setSpacing(10)

        # Set layout to add_tab
        self.add_tab.setLayout(layout)

    def setup_view_tab(self):
        # Layout for View Cards tab
        layout = QVBoxLayout()

        # View Button
        self.view_button = QPushButton("Refresh Cards")
        self.view_button.clicked.connect(self.view_cards)

        # Save Button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)

        # Table to display cards
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Card Number", "Card Holder", "Balance"])

        # Add widgets to layout
        layout.addWidget(self.view_button)
        layout.addWidget(self.save_button)
        layout.addWidget(QLabel("All Gift Cards"))
        layout.addWidget(self.table)

        # Set layout to view_tab
        self.view_tab.setLayout(layout)

    def add_card(self):
        card_number = self.card_number_input.text()
        card_holder = self.card_holder_input.text()
        balance = self.balance_input.text()

        # Input validation
        if not card_number or not card_holder or not balance:
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            balance = float(balance)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Balance must be a number.")
            return

        # Database insertion
        try:
            conn = sqlite3.connect("giftcards.db")
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO cards (card_number, card_holder, balance) 
            VALUES (?, ?, ?)
            """, (card_number, card_holder, balance))
            conn.commit()
            conn.close()
            
            QMessageBox.information(self, "Success", "Gift Card added successfully!")
            self.card_number_input.clear()
            self.card_holder_input.clear()
            self.balance_input.clear()

        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Card Number must be unique.")
    
    def view_cards(self):
        # Clear the table before adding new data
        self.table.setRowCount(0)

        # Fetch data from the database
        conn = sqlite3.connect("giftcards.db")
        cursor = conn.cursor()
        cursor.execute("SELECT card_number, card_holder, balance FROM cards")
        rows = cursor.fetchall()
        conn.close()

        # Populate the table
        for row_number, row_data in enumerate(rows):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled) if column_number == 0 else item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)  # Make Card Number non-editable
                self.table.setItem(row_number, column_number, item)

    def save_changes(self):
        # Loop through each row and update the database
        conn = sqlite3.connect("giftcards.db")
        cursor = conn.cursor()

        for row in range(self.table.rowCount()):
            card_number = self.table.item(row, 0).text()
            card_holder = self.table.item(row, 1).text()
            balance = self.table.item(row, 2).text()

            try:
                balance = float(balance)  # Ensure balance is a valid number
                cursor.execute("""
                UPDATE cards SET card_holder = ?, balance = ? WHERE card_number = ?
                """, (card_holder, balance, card_number))
            except ValueError:
                QMessageBox.warning(self, "Input Error", f"Invalid balance for card {card_number}")
                conn.rollback()
                conn.close()
                return

        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Changes saved successfully!")

# Run the application
if __name__ == "__main__":
    init_db()  # Ensure the database and table are initialized
    app = QApplication(sys.argv)
    window = GiftCardApp()
    window.show()
    sys.exit(app.exec())
