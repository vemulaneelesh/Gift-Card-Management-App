import sys
import os
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox, QWidget, QFileDialog
from PyQt6.QtCore import Qt

from database import DatabaseManager
from image_handler import ImageHandler
from ui_components import AddCardTab, ViewCardsTab, EditCardDialog

class GiftCardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gift Card Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.image_handler = ImageHandler()
        
        # Setup UI
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Setup the main application UI"""
        # Main layout and tabs
        self.tabs = QTabWidget()
        
        # Create tabs
        self.add_tab_widget = QWidget()
        self.view_tab_widget = QWidget()
        
        # Setup tab components
        self.add_tab = AddCardTab(self)
        self.view_tab = ViewCardsTab(self)
        
        # Set layouts
        self.add_tab_widget.setLayout(self.add_tab.layout)
        self.view_tab_widget.setLayout(self.view_tab.layout)
        
        # Add tabs to main widget
        self.tabs.addTab(self.add_tab_widget, "Add Card")
        self.tabs.addTab(self.view_tab_widget, "View Cards")
        
        # Set central widget
        self.setCentralWidget(self.tabs)
    
    def connect_signals(self):
        """Connect all signal handlers"""
        # Add card tab signals
        self.add_tab.purchase_price_input.valueChanged.connect(self.calculate_profit)
        self.add_tab.expected_price_input.valueChanged.connect(self.calculate_profit)
        self.add_tab.upload_button.clicked.connect(self.upload_image)
        self.add_tab.add_button.clicked.connect(self.add_card)
        
        # View cards tab signals
        self.view_tab.view_button.clicked.connect(self.view_cards)
        self.view_tab.save_button.clicked.connect(self.save_changes)
        self.view_tab.delete_button.clicked.connect(self.delete_selected)
        self.view_tab.export_button.clicked.connect(self.export_to_excel)
        
        # Tab change signal - auto-load data when View Cards tab is selected
        self.tabs.currentChanged.connect(self.on_tab_changed)
    
    def on_tab_changed(self, index):
        """Handle tab changes - auto-load data when View Cards tab is selected"""
        if index == 1:  # View Cards tab (index 1)
            self.view_cards()
    
    def calculate_profit(self):
        """Calculate and update profit display"""
        self.add_tab.update_profit()
    
    def upload_image(self):
        """Handle image upload"""
        success, filename = self.image_handler.upload_image(self)
        if success:
            self.add_tab.image_path_label.setText(filename)
            self.image_handler.show_preview(
                self.image_handler.get_image_path(), 
                self.add_tab.image_preview_label
            )
    
    def add_card(self):
        """Add a new gift card"""
        # Get form data
        card_data = self.add_tab.get_form_data()
        
        # Input validation
        if not card_data['card_number'] or not card_data['brand']:
            QMessageBox.warning(self, "Input Error", "Card Number and Brand are required!")
            return
        
        if card_data['denomination'] <= 0 or card_data['purchase_price'] <= 0 or card_data['expected_price'] <= 0:
            QMessageBox.warning(self, "Input Error", "Denomination, Purchase Price, and Expected Price must be greater than 0.")
            return
        
        # Calculate profit
        card_data['profit'] = card_data['expected_price'] - card_data['purchase_price']
        
        # Handle image upload (optional)
        card_data['card_image_path'] = ""
        try:
            if self.add_tab.image_path_label.text() != "No image selected":
                card_data['card_image_path'] = self.image_handler.save_image(card_data['card_number'])
        except Exception as e:
            QMessageBox.warning(self, "Image Error", f"Failed to save image: {str(e)}")
            card_data['card_image_path'] = ""
        
        # Add to database
        success, message = self.db_manager.add_card(card_data)
        
        if success:
            QMessageBox.information(self, "Success", message)
            self.clear_form()
            # Auto-refresh the view cards tab if it's currently visible
            if self.tabs.currentIndex() == 1:
                self.view_cards()
        else:
            QMessageBox.warning(self, "Error", message)
    
    def clear_form(self):
        """Clear the add card form"""
        self.add_tab.clear_form()
        self.image_handler.reset()
    
    def view_cards(self):
        """Load and display all cards"""
        cards_data = self.db_manager.get_all_cards()
        self.view_tab.populate_table(cards_data)
    
    def refresh_cards(self):
        """Refresh the cards table (alias for view_cards)"""
        self.view_cards()
    
    def save_changes(self):
        """Save changes made in the table"""
        table_data = self.view_tab.get_table_data()
        
        for row_data in table_data:
            card_number = row_data[0]
            if not card_number:
                continue
            
            try:
                card_data = {
                    'card_holder': row_data[1],
                    'brand': row_data[2],
                    'pin': row_data[3],
                    'denomination': float(row_data[4]),
                    'purchase_price': float(row_data[5]),
                    'expected_price': float(row_data[6]),
                    'profit': float(row_data[7]),
                    'source': row_data[8],
                    'purchase_date': row_data[9],
                    'pending': row_data[10],
                    'sold_date': row_data[11],
                    'payment_received': float(row_data[12]) if row_data[12] else 0.0,
                    'payment_mode': row_data[13]
                }
                
                success, message = self.db_manager.update_card(card_number, card_data)
                if not success:
                    QMessageBox.warning(self, "Update Error", f"Failed to update card {card_number}: {message}")
                    return
                    
            except ValueError:
                QMessageBox.warning(self, "Input Error", f"Invalid number format for card {card_number}")
                return
        
        QMessageBox.information(self, "Success", "Changes saved successfully!")
        # Refresh the table to show updated data
        self.view_cards()
    
    def delete_selected(self):
        """Delete selected cards"""
        selected_rows = self.view_tab.get_selected_rows()
        if not selected_rows:
            QMessageBox.warning(self, "Selection Error", "Please select cards to delete.")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete {len(selected_rows)} card(s)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            deleted_count = 0
            for row in sorted(selected_rows, reverse=True):
                card_number = self.view_tab.table.item(row, 0).text()
                success, message = self.db_manager.delete_card(card_number)
                if success:
                    deleted_count += 1
                else:
                    QMessageBox.warning(self, "Delete Error", f"Failed to delete card {card_number}: {message}")
                    return
            
            QMessageBox.information(self, "Success", f"Deleted {deleted_count} card(s) successfully!")
            # Refresh the table to show updated data
            self.view_cards()
    
    def export_to_excel(self):
        """Export card data to Excel file"""
        try:
            # Get all cards from database
            cards_data = self.db_manager.get_all_cards()
            
            if not cards_data:
                QMessageBox.warning(self, "Export Error", "No cards found to export.")
                return
            
            # Create default filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"gift_cards_export_{timestamp}.csv"
            
            # Open file dialog for save location
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "Export Gift Cards Data", 
                default_filename,
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:
                return  # User cancelled
            
            # Write data to CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                # Write header
                csvfile.write("Card Number,Card Holder,Brand,PIN,Denomination,Purchase Price,Expected Price,Profit,Source,Purchase Date,Pending,Sold Date,Payment Received,Payment Mode,Image Path\n")
                
                # Write data rows
                for card in cards_data:
                    # Format the data properly
                    card_number = str(card[0]).replace(',', ';')  # Replace commas to avoid CSV issues
                    card_holder = str(card[1]).replace(',', ';')
                    brand = str(card[2]).replace(',', ';')
                    pin = str(card[3]).replace(',', ';') if card[3] else ""
                    denomination = f"${card[4]:.2f}" if card[4] else "$0.00"
                    purchase_price = f"${card[5]:.2f}" if card[5] else "$0.00"
                    expected_price = f"${card[6]:.2f}" if card[6] else "$0.00"
                    profit = f"${card[7]:.2f}" if card[7] else "$0.00"
                    source = str(card[8]).replace(',', ';') if card[8] else ""
                    purchase_date = str(card[9]) if card[9] else ""
                    pending = str(card[10]) if card[10] else "No"
                    sold_date = str(card[11]) if card[11] else ""
                    payment_received = f"${card[12]:.2f}" if card[12] else "$0.00"
                    payment_mode = str(card[13]).replace(',', ';') if card[13] else ""
                    image_path = str(card[14]) if card[14] else ""
                    
                    # Write row
                    csvfile.write(f"{card_number},{card_holder},{brand},{pin},{denomination},{purchase_price},{expected_price},{profit},{source},{purchase_date},{pending},{sold_date},{payment_received},{payment_mode},{image_path}\n")
            
            # Show success message
            QMessageBox.information(
                self, 
                "Export Successful", 
                f"Successfully exported {len(cards_data)} cards to:\n{file_path}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Export Error", 
                f"Failed to export data: {str(e)}"
            )


def main():
    app = QApplication(sys.argv)
    window = GiftCardApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 