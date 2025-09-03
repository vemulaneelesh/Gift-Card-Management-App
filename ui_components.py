from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QTabWidget, QFormLayout, QDateEdit, 
    QComboBox, QDoubleSpinBox, QMessageBox, QDialog
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QColor
import os

class AddCardTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the Add Card tab UI"""
        # Main layout
        main_layout = QHBoxLayout()
        
        # Left side - Form
        form_widget = QWidget()
        form_layout = QFormLayout()
        
        # Create input fields
        self.create_input_fields()
        
        # Add widgets to form layout
        form_layout.addRow(QLabel("<b>Add New Gift Card</b>"))
        form_layout.addRow("Card Number:", self.card_number_input)
        form_layout.addRow("Brand:", self.brand_input)
        form_layout.addRow("PIN:", self.pin_input)
        form_layout.addRow("Denomination:", self.denomination_input)
        form_layout.addRow("Purchase Price:", self.purchase_price_input)
        # Add toggle for expected price input mode
        self.expected_price_mode = QComboBox()
        self.expected_price_mode.addItems(["Amount ($)", "Percent (%)"])
        self.expected_price_mode.setCurrentIndex(0)
        self.expected_price_mode.currentIndexChanged.connect(self.on_expected_price_mode_changed)
        # Add both widgets to the form
        expected_price_row = QHBoxLayout()
        expected_price_row.addWidget(self.expected_price_input)
        expected_price_row.addWidget(self.expected_price_mode)
        form_layout.addRow("Expected Price:", expected_price_row)
        # Add percent input (hidden by default)
        self.expected_percent_input = QDoubleSpinBox()
        self.expected_percent_input.setRange(0, 100)
        self.expected_percent_input.setSuffix("%")
        self.expected_percent_input.setDecimals(2)
        self.expected_percent_input.setVisible(False)
        expected_price_row.addWidget(self.expected_percent_input)
        self.expected_percent_input.valueChanged.connect(self.on_expected_percent_changed)
        self.expected_price_input.valueChanged.connect(self.on_expected_price_changed)
        form_layout.addRow("Profit:", self.profit_label)
        form_layout.addRow("Source:", self.source_input)
        form_layout.addRow("Purchase Date:", self.purchase_date_input)
        form_layout.addRow("Pending:", self.pending_input)
        form_layout.addRow("Sold Date:", self.sold_date_input)
        form_layout.addRow("Payment Received:", self.payment_received_input)
        form_layout.addRow("Payment Mode:", self.payment_mode_input)
        form_layout.addRow("Card Image:", self.upload_button)
        form_layout.addRow("", self.image_path_label)
        form_layout.addRow(self.add_button)
        

        
        form_layout.setContentsMargins(20, 10, 20, 10)
        form_layout.setSpacing(10)
        form_widget.setLayout(form_layout)
        
        # Right side - Image preview
        preview_widget = self.create_preview_widget()
        
        # Add both widgets to main layout
        main_layout.addWidget(form_widget, 2)
        main_layout.addWidget(preview_widget, 1)
        
        self.layout = main_layout
        self.on_pending_changed("Yes")
    
    def create_input_fields(self):
        """Create all input fields"""
        self.card_number_input = QLineEdit()
        self.card_number_input.setPlaceholderText("Enter Card Number")
        
        self.brand_input = QLineEdit()
        self.brand_input.setPlaceholderText("e.g., Amazon, Walmart, Target")
        
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("Enter PIN (if applicable)")
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.denomination_input = QDoubleSpinBox()
        self.denomination_input.setRange(0, 10000)
        self.denomination_input.setPrefix("$")
        self.denomination_input.setDecimals(2)
        
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setRange(0, 10000)
        self.purchase_price_input.setPrefix("$")
        self.purchase_price_input.setDecimals(2)
        
        self.expected_price_input = QDoubleSpinBox()
        self.expected_price_input.setRange(0, 10000)
        self.expected_price_input.setPrefix("$")
        self.expected_price_input.setDecimals(2)
        
        self.profit_label = QLabel("$0.00")
        self.profit_label.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")
        
        self.source_input = QComboBox()
        self.source_input.addItems(["Online Purchase", "Physical Store", "Gift", "Trade", "Other"])
        self.source_input.setEditable(True)
        
        self.purchase_date_input = QDateEdit()
        self.purchase_date_input.setDate(QDate.currentDate())
        self.purchase_date_input.setCalendarPopup(True)
        
        # Pending status
        self.pending_input = QComboBox()
        self.pending_input.addItems(["Yes", "No"])
        self.pending_input.setCurrentText("Yes")
        self.pending_input.currentTextChanged.connect(self.on_pending_changed)
        
        # Sold date (initially hidden)
        self.sold_date_input = QDateEdit()
        self.sold_date_input.setDate(QDate.currentDate())
        self.sold_date_input.setCalendarPopup(True)
        self.sold_date_input.setVisible(False)
        
        # Payment received (initially hidden)
        self.payment_received_input = QDoubleSpinBox()
        self.payment_received_input.setRange(0, 10000)
        self.payment_received_input.setPrefix("$")
        self.payment_received_input.setDecimals(2)
        self.payment_received_input.setVisible(False)
        
        # Payment mode (initially hidden)
        self.payment_mode_input = QComboBox()
        self.payment_mode_input.addItems(["Cash", "Bank Transfer", "PayPal", "Venmo", "Zelle", "Credit Card", "Other"])
        self.payment_mode_input.setEditable(True)
        self.payment_mode_input.setVisible(False)
        
        # Image upload section
        self.image_path_label = QLabel("No image selected")
        self.upload_button = QPushButton("Upload Card Image")
        
        # Add Button
        self.add_button = QPushButton("Add Card")
        self.add_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
    
    def create_preview_widget(self):
        """Create the image preview widget"""
        preview_widget = QWidget()
        preview_layout = QVBoxLayout()
        
        # Title with better styling
        title_label = QLabel("📷 Card Image Preview")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ecf0f1, stop:1 #bdc3c7);
                border-radius: 8px;
                margin-bottom: 10px;
            }
        """)
        
        # Enhanced image preview label
        self.image_preview_label = QLabel()
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setMinimumSize(150, 200)
        self.image_preview_label.setMaximumSize(250, 300)
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.5 #f8f9fa, stop:1 #e9ecef);
                border: 3px dashed #6c757d;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
            }
        """)
        
        # Set default preview content
        self.set_default_preview()
        
        # Info text
        info_label = QLabel("Click 'Upload Card Image' to add a photo")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-style: italic;
                padding: 3px;
            }
        """)
        
        preview_layout.addWidget(title_label)
        preview_layout.addWidget(self.image_preview_label, 1)  # Give it stretch priority
        preview_layout.addWidget(info_label)
        preview_layout.addStretch(0)  # Minimal stretch at bottom
        
        preview_widget.setLayout(preview_layout)
        return preview_widget
    
    def set_default_preview(self):
        """Set the default preview content with icon and text"""
        self.image_preview_label.setText("📱\n\nNo Image\n\nClick to Upload")
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.5 #f8f9fa, stop:1 #e9ecef);
                border: 3px dashed #6c757d;
                border-radius: 15px;
                padding: 10px;
                margin: 5px;
                font-size: 12px;
                color: #6c757d;
                font-weight: bold;
            }
        """)
    
    def get_form_data(self):
        """Get all form data as a dictionary"""
        data = {
            'card_number': self.card_number_input.text().strip(),
            'brand': self.brand_input.text().strip(),
            'pin': self.pin_input.text().strip(),
            'denomination': self.denomination_input.value(),
            'purchase_price': self.purchase_price_input.value(),
            'expected_price': self.expected_price_input.value(),
            'expected_percent': self.expected_percent_input.value(),
            'source': self.source_input.currentText(),
            'purchase_date': self.purchase_date_input.date().toString("yyyy-MM-dd"),
            'pending': self.pending_input.currentText(),
            'sold_date': self.sold_date_input.date().toString("yyyy-MM-dd") if self.pending_input.currentText() == "No" else "",
            'payment_received': self.payment_received_input.value() if self.pending_input.currentText() == "No" else 0.0,
            'payment_mode': self.payment_mode_input.currentText() if self.pending_input.currentText() == "No" else "",
            'card_image_path': self.image_path_label.text() if self.image_path_label.text() != "No image selected" else self.card_data.get('card_image_path', '')
        }
        return data
    
    def clear_form(self):
        """Clear all form fields"""
        self.card_number_input.clear()
        self.brand_input.clear()
        self.pin_input.clear()
        self.denomination_input.setValue(0)
        self.purchase_price_input.setValue(0)
        self.expected_price_input.setValue(0)
        self.source_input.setCurrentIndex(0)
        self.purchase_date_input.setDate(QDate.currentDate())
        self.pending_input.setCurrentText("Yes")
        self.on_pending_changed("Yes")
        self.sold_date_input.setDate(QDate.currentDate())
        self.payment_received_input.setValue(0)
        self.payment_mode_input.setCurrentIndex(0)
        self.image_path_label.setText("No image selected")
        self.set_default_preview()
    
    def on_pending_changed(self, value):
        """Handle pending status change - show/hide sold fields"""
        if value == "No":  # Card is sold, show sold details
            self.sold_date_input.setVisible(True)
            self.payment_received_input.setVisible(True)
            self.payment_mode_input.setVisible(True)
            # Set payment received to expected price by default
            self.payment_received_input.setValue(self.expected_price_input.value())
        else:  # Card is still pending, hide sold details
            self.sold_date_input.setVisible(False)
            self.payment_received_input.setVisible(False)
            self.payment_mode_input.setVisible(False)
    
    def update_profit(self):
        """Update the profit calculation"""
        purchase_price = self.purchase_price_input.value()
        expected_price = self.expected_price_input.value()
        profit = expected_price - purchase_price
        self.profit_label.setText(f"${profit:.2f}")
        if profit >= 0:
            self.profit_label.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")
        else:
            self.profit_label.setStyleSheet("font-weight: bold; color: red; font-size: 14px;")

    def on_expected_price_mode_changed(self, idx):
        if idx == 0:  # Amount
            self.expected_price_input.setVisible(True)
            self.expected_percent_input.setVisible(False)
            # Update expected price from percent if needed
            if self.expected_percent_input.value() > 0:
                purchase_price = self.purchase_price_input.value()
                percent = self.expected_percent_input.value()
                self.expected_price_input.setValue(purchase_price * percent / 100)
        else:  # Percent
            self.expected_price_input.setVisible(False)
            self.expected_percent_input.setVisible(True)
            # Update percent from expected price if needed
            if self.expected_price_input.value() > 0 and self.purchase_price_input.value() > 0:
                percent = (self.expected_price_input.value() / self.purchase_price_input.value()) * 100
                self.expected_percent_input.setValue(percent)
    def on_expected_percent_changed(self, value):
        if self.expected_price_mode.currentIndex() == 1:  # Percent mode
            purchase_price = self.purchase_price_input.value()
            self.expected_price_input.setValue(purchase_price * value / 100)
            self.update_profit()
    def on_expected_price_changed(self, value):
        if self.expected_price_mode.currentIndex() == 0 and self.purchase_price_input.value() > 0:
            percent = (value / self.purchase_price_input.value()) * 100
            self.expected_percent_input.setValue(percent)
            self.update_profit()

class EditCardDialog(QDialog):
    """Dialog for editing an existing card"""
    
    def __init__(self, parent, card_data, image_handler):
        super().__init__(parent)
        self.card_data = card_data
        self.image_handler = image_handler
        self.setup_ui()
        self.populate_form()
        self.setup_connections()
    
    def setup_ui(self):
        """Setup the edit dialog UI"""
        self.setWindowTitle("Edit Gift Card")
        self.setModal(True)
        self.resize(600, 700)
        
        layout = QVBoxLayout()
        
        # Create form layout
        form_layout = QFormLayout()
        
        # Card Number (read-only)
        self.card_number_input = QLineEdit()
        self.card_number_input.setReadOnly(True)
        self.card_number_input.setStyleSheet("background-color: #f8f9fa; color: #6c757d;")
        form_layout.addRow("Card Number:", self.card_number_input)
        
        # Brand
        self.brand_input = QLineEdit()
        form_layout.addRow("Brand:", self.brand_input)
        
        # PIN
        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("PIN:", self.pin_input)
        
        # Denomination
        self.denomination_input = QDoubleSpinBox()
        self.denomination_input.setMaximum(999999.99)
        self.denomination_input.setPrefix("$")
        form_layout.addRow("Denomination:", self.denomination_input)
        
        # Purchase Price
        self.purchase_price_input = QDoubleSpinBox()
        self.purchase_price_input.setMaximum(999999.99)
        self.purchase_price_input.setPrefix("$")
        form_layout.addRow("Purchase Price:", self.purchase_price_input)
        
        # Expected Price
        self.expected_price_input = QDoubleSpinBox()
        self.expected_price_input.setMaximum(999999.99)
        self.expected_price_input.setPrefix("$")
        # Add toggle for expected price input mode
        self.expected_price_mode = QComboBox()
        self.expected_price_mode.addItems(["Amount ($)", "Percent (%)"])
        self.expected_price_mode.setCurrentIndex(0)
        self.expected_price_mode.currentIndexChanged.connect(self.on_expected_price_mode_changed)
        # Add both widgets to the form
        expected_price_row = QHBoxLayout()
        expected_price_row.addWidget(self.expected_price_input)
        expected_price_row.addWidget(self.expected_price_mode)
        form_layout.addRow("Expected Price:", expected_price_row)
        # Add percent input (hidden by default)
        self.expected_percent_input = QDoubleSpinBox()
        self.expected_percent_input.setRange(0, 100)
        self.expected_percent_input.setSuffix("%")
        self.expected_percent_input.setDecimals(2)
        self.expected_percent_input.setVisible(False)
        expected_price_row.addWidget(self.expected_percent_input)
        self.expected_percent_input.valueChanged.connect(self.on_expected_percent_changed)
        self.expected_price_input.valueChanged.connect(self.on_expected_price_changed)
        form_layout.addRow("Profit:", self.profit_label)
        
        # Source
        self.source_input = QComboBox()
        self.source_input.addItems(["", "Online", "Store", "Friend", "Family", "Other"])
        self.source_input.setEditable(True)
        form_layout.addRow("Source:", self.source_input)
        
        # Purchase Date
        self.purchase_date_input = QDateEdit()
        self.purchase_date_input.setCalendarPopup(True)
        form_layout.addRow("Purchase Date:", self.purchase_date_input)
        
        # Pending Status
        self.pending_input = QComboBox()
        self.pending_input.addItems(["No", "Yes"])
        form_layout.addRow("Pending:", self.pending_input)
        
        # Sold Date (initially hidden)
        self.sold_date_input = QDateEdit()
        self.sold_date_input.setCalendarPopup(True)
        self.sold_date_input.setVisible(False)
        form_layout.addRow("Sold Date:", self.sold_date_input)
        
        # Payment Received (initially hidden)
        self.payment_received_input = QDoubleSpinBox()
        self.payment_received_input.setMaximum(999999.99)
        self.payment_received_input.setPrefix("$")
        self.payment_received_input.setVisible(False)
        form_layout.addRow("Payment Received:", self.payment_received_input)
        
        # Payment Mode (initially hidden)
        self.payment_mode_input = QComboBox()
        self.payment_mode_input.addItems(["", "Cash", "Bank Transfer", "PayPal", "Credit Card", "Other"])
        self.payment_mode_input.setEditable(True)
        self.payment_mode_input.setVisible(False)
        form_layout.addRow("Payment Mode:", self.payment_mode_input)
        
        # Image section
        image_layout = QHBoxLayout()
        
        # Image path label
        self.image_path_label = QLabel("No image selected")
        self.image_path_label.setStyleSheet("color: #6c757d; font-style: italic;")
        
        # Upload button
        self.upload_button = QPushButton("Upload Image")
        self.upload_button.clicked.connect(self.upload_image)
        
        image_layout.addWidget(QLabel("Card Image:"))
        image_layout.addWidget(self.image_path_label, 1)
        image_layout.addWidget(self.upload_button)
        
        # Image preview
        self.image_preview_label = QLabel()
        self.image_preview_label.setFixedSize(120, 80)
        self.image_preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.5 #f8f9fa, stop:1 #e9ecef);
                border: 2px dashed #6c757d;
                border-radius: 10px;
                padding: 5px;
                margin: 3px;
            }
        """)
        self.set_default_preview()
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save Changes")
        self.save_button.setStyleSheet("background-color: #28a745; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold;")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("background-color: #6c757d; color: white; padding: 8px 15px; border-radius: 5px;")
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        # Add all layouts to main layout
        layout.addLayout(form_layout)
        layout.addLayout(image_layout)
        layout.addWidget(self.image_preview_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def setup_connections(self):
        """Setup signal connections"""
        self.purchase_price_input.valueChanged.connect(self.update_profit)
        self.expected_price_input.valueChanged.connect(self.update_profit)
        self.pending_input.currentTextChanged.connect(self.on_pending_changed)
        self.expected_price_input.valueChanged.connect(self.on_expected_price_changed)
        
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def populate_form(self):
        """Populate form with existing card data"""
        self.card_number_input.setText(self.card_data.get('card_number', ''))
        self.brand_input.setText(self.card_data.get('brand', ''))
        self.pin_input.setText(self.card_data.get('pin', ''))
        self.denomination_input.setValue(float(self.card_data.get('denomination', 0)))
        self.purchase_price_input.setValue(float(self.card_data.get('purchase_price', 0)))
        self.expected_price_input.setValue(float(self.card_data.get('expected_price', 0)))
        
        # Set source
        source = self.card_data.get('source', '')
        index = self.source_input.findText(source)
        if index >= 0:
            self.source_input.setCurrentIndex(index)
        else:
            self.source_input.setCurrentText(source)
        
        # Set purchase date
        purchase_date = self.card_data.get('purchase_date', '')
        if purchase_date:
            try:
                date = QDate.fromString(purchase_date, "yyyy-MM-dd")
                self.purchase_date_input.setDate(date)
            except:
                self.purchase_date_input.setDate(QDate.currentDate())
        else:
            self.purchase_date_input.setDate(QDate.currentDate())
        
        # Set pending status
        pending = self.card_data.get('is_pending', 'No')
        index = self.pending_input.findText(pending)
        if index >= 0:
            self.pending_input.setCurrentIndex(index)
        
        # Set sold date
        sold_date = self.card_data.get('sold_date', '')
        if sold_date:
            try:
                date = QDate.fromString(sold_date, "yyyy-MM-dd")
                self.sold_date_input.setDate(date)
            except:
                self.sold_date_input.setDate(QDate.currentDate())
        else:
            self.sold_date_input.setDate(QDate.currentDate())
        
        # Set payment received
        self.payment_received_input.setValue(float(self.card_data.get('payment_received', 0)))
        
        # Set payment mode
        payment_mode = self.card_data.get('payment_mode', '')
        index = self.payment_mode_input.findText(payment_mode)
        if index >= 0:
            self.payment_mode_input.setCurrentIndex(index)
        else:
            self.payment_mode_input.setCurrentText(payment_mode)
        
        # Set image
        image_path = self.card_data.get('card_image_path', '')
        if image_path:
            # Check if it's a full path or just filename
            if os.path.exists(image_path):
                self.image_path_label.setText(os.path.basename(image_path))
                self.load_image_preview(image_path)
            elif os.path.exists(os.path.join("card_images", image_path)):
                full_path = os.path.join("card_images", image_path)
                self.image_path_label.setText(image_path)
                self.load_image_preview(full_path)
            else:
                self.image_path_label.setText("No image selected")
                self.set_default_preview()
        else:
            self.image_path_label.setText("No image selected")
            self.set_default_preview()
        
        # Update profit and pending fields visibility
        self.update_profit()
        self.on_pending_changed(pending)
    
    def upload_image(self):
        """Upload a new image for the card"""
        success, filename = self.image_handler.upload_image(self)
        if success:
            self.image_path_label.setText(filename)
            self.load_image_preview(self.image_handler.get_image_path())
    
    def load_image_preview(self, image_path):
        """Load and display image preview"""
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(120, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.image_preview_label.setPixmap(scaled_pixmap)
                self.image_preview_label.setStyleSheet("""
                    QLabel {
                        border: 2px solid #28a745;
                        border-radius: 10px;
                        padding: 2px;
                        margin: 3px;
                    }
                """)
                return
        
        self.set_default_preview()
    
    def set_default_preview(self):
        """Set the default preview content"""
        self.image_preview_label.setText("📱\n\nNo Image")
        self.image_preview_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.5 #f8f9fa, stop:1 #e9ecef);
                border: 2px dashed #6c757d;
                border-radius: 10px;
                padding: 5px;
                margin: 3px;
                font-size: 10px;
                color: #6c757d;
                font-weight: bold;
            }
        """)
    
    def get_form_data(self):
        """Get all form data as a dictionary"""
        data = {
            'card_number': self.card_number_input.text().strip(),
            'brand': self.brand_input.text().strip(),
            'pin': self.pin_input.text().strip(),
            'denomination': self.denomination_input.value(),
            'purchase_price': self.purchase_price_input.value(),
            'expected_price': self.expected_price_input.value(),
            'expected_percent': self.expected_percent_input.value(),
            'source': self.source_input.currentText(),
            'purchase_date': self.purchase_date_input.date().toString("yyyy-MM-dd"),
            'pending': self.pending_input.currentText(),
            'sold_date': self.sold_date_input.date().toString("yyyy-MM-dd") if self.pending_input.currentText() == "No" else "",
            'payment_received': self.payment_received_input.value() if self.pending_input.currentText() == "No" else 0.0,
            'payment_mode': self.payment_mode_input.currentText() if self.pending_input.currentText() == "No" else "",
            'card_image_path': self.image_path_label.text() if self.image_path_label.text() != "No image selected" else self.card_data.get('card_image_path', '')
        }
        return data
    
    def on_pending_changed(self, value):
        """Handle pending status change - show/hide sold fields"""
        if value == "No":  # Card is sold, show sold details
            self.sold_date_input.setVisible(True)
            self.payment_received_input.setVisible(True)
            self.payment_mode_input.setVisible(True)
        else:  # Card is still pending, hide sold details
            self.sold_date_input.setVisible(False)
            self.payment_received_input.setVisible(False)
            self.payment_mode_input.setVisible(False)
    
    def on_expected_price_changed(self, value):
        """Update payment received when expected price changes"""
        if self.pending_input.currentText() == "No":  # Only update if card is sold
            self.payment_received_input.setValue(value)
    
    def update_profit(self):
        """Update the profit calculation"""
        purchase_price = self.purchase_price_input.value()
        expected_price = self.expected_price_input.value()
        profit = expected_price - purchase_price
        self.profit_label.setText(f"${profit:.2f}")
        if profit >= 0:
            self.profit_label.setStyleSheet("font-weight: bold; color: green; font-size: 14px;")
        else:
            self.profit_label.setStyleSheet("font-weight: bold; color: red; font-size: 14px;")

class ViewCardsTab:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the View Cards tab UI"""
        layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        self.view_button = QPushButton("Refresh Cards")
        self.save_button = QPushButton("Save Changes")
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.setStyleSheet("background-color: #f44336; color: white;")
        
        # Export to Excel button
        self.export_button = QPushButton("📊 Export to Excel")
        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        
        button_layout.addWidget(self.view_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.export_button)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(15)  # Reduced by one column
        self.table.setHorizontalHeaderLabels([
            "Card Number", "Brand", "PIN", "Denomination", 
            "Purchase Price", "Expected Price", "Profit", "Source", "Purchase Date", 
            "Pending", "Sold Date", "Payment Received", "Payment Mode", "Image", "Actions"
        ])
        
        # Set column widths for better display
        column_widths = [
            180,  # Card Number (increased for better cross-platform appearance)
            80,   # Brand
            60,   # PIN
            90,   # Denomination
            100,  # Purchase Price
            100,  # Expected Price
            80,   # Profit
            80,   # Source
            100,  # Purchase Date
            70,   # Pending
            100,  # Sold Date
            120,  # Payment Received
            100,  # Payment Mode
            60,   # Image
            80    # Actions
        ]
        
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        
        # Enable horizontal scrolling
        self.table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Additional table improvements
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setWordWrap(False)  # Prevent text wrapping in cells
        
        # Set table style
        self.table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                background-color: #232323;
                alternate-background-color: #2c2c2c;
                selection-background-color: #007bff;
                selection-color: white;
                color: #222;
            }
            QTableWidget::viewport {
                background: #232323;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #232323;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
                color: #fff;
            }
        """)
        
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("All Gift Cards"))
        layout.addWidget(self.table)
        
        self.layout = layout
    
    def populate_table(self, cards_data):
        """Populate the table with card data"""
        self.table.setRowCount(0)
        
        if not cards_data:
            return
        
        for row_number, row_data in enumerate(cards_data):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                try:
                    if column_number == 2:  # PIN column (was 3)
                        display_text = "*" * len(str(data)) if data else ""
                        item = QTableWidgetItem(display_text)
                    elif column_number in [3, 4, 5, 6, 11]:  # Money columns (shifted indices)
                        if data is not None:
                            item = QTableWidgetItem(f"${float(data):.2f}")
                        else:
                            item = QTableWidgetItem("$0.00")
                    elif column_number == 13:  # Image column (was 14)
                        item = QTableWidgetItem("Yes" if data else "No")
                    else:
                        item = QTableWidgetItem(str(data) if data is not None else "")
                    
                    # Make Card Number non-editable, others editable
                    if column_number == 0:
                        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
                    else:
                        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                    
                    self.table.setItem(row_number, column_number, item)
                except Exception as e:
                    item = QTableWidgetItem(str(data) if data is not None else "")
                    self.table.setItem(row_number, column_number, item)
            
            # Highlight row if Pending == 'No', else set text color to white
            pending_col_index = 10
            pending_value = str(row_data[pending_col_index]).strip().lower()
            if pending_value.startswith('no'):
                for col in range(self.table.columnCount()):
                    cell_item = self.table.item(row_number, col)
                    if cell_item:
                        cell_item.setBackground(QColor('#2e4736'))
                        cell_item.setData(Qt.ItemDataRole.BackgroundRole, QColor('#2e4736'))
                        cell_item.setForeground(QColor('#7CFC98'))  # Light green font for No
            else:
                for col in range(self.table.columnCount()):
                    cell_item = self.table.item(row_number, col)
                    if cell_item:
                        cell_item.setForeground(QColor('#fff'))
            
            # Add edit button in the last column
            edit_button = QPushButton("✏️ Edit")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            edit_button.clicked.connect(lambda checked, row=row_number: self.edit_card(row))
            self.table.setCellWidget(row_number, 14, edit_button) # Adjusted column index
    
    def get_table_data(self):
        """Get all data from the table"""
        data = []
        for row in range(self.table.rowCount()):
            row_data = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    text = item.text()
                    if col in [4, 5, 6, 7, 12]:  # Money columns (including Payment Received)
                        text = text.replace("$", "")
                    row_data.append(text)
                else:
                    row_data.append("")
            data.append(row_data)
        return data
    
    def get_selected_rows(self):
        """Get selected row indices"""
        return set(item.row() for item in self.table.selectedItems())
    
    def edit_card(self, row):
        """Open edit dialog for the specified row"""
        def safe_float(item):
            text = item.text() if item else ''
            text = text.replace('$', '').strip()
            return float(text) if text else 0.0
        # Get card data from the row
        card_data = {}
        card_data['card_number'] = self.table.item(row, 0).text()
        card_data['brand'] = self.table.item(row, 1).text()
        card_data['pin'] = self.table.item(row, 2).text()  # This will be masked, need to get from database
        card_data['denomination'] = safe_float(self.table.item(row, 3))
        card_data['purchase_price'] = safe_float(self.table.item(row, 4))
        card_data['expected_price'] = safe_float(self.table.item(row, 5))
        card_data['profit'] = card_data['expected_price'] - card_data['purchase_price']
        card_data['source'] = self.table.item(row, 7).text()
        card_data['purchase_date'] = self.table.item(row, 8).text()
        card_data['pending'] = self.table.item(row, 9).text()
        card_data['sold_date'] = self.table.item(row, 10).text()
        card_data['payment_received'] = safe_float(self.table.item(row, 11))
        card_data['payment_mode'] = self.table.item(row, 12).text()
        card_data['card_image_path'] = self.table.item(row, 13).text()  # This will be "Yes" or "No", need to get actual path
        
        # Get the actual card data from database (including PIN and image path)
        if hasattr(self.parent, 'db_manager'):
            full_card_data = self.parent.db_manager.get_card_by_number(card_data['card_number'])
            if full_card_data:
                card_data.update(full_card_data)
        
        # Create and show edit dialog
        if hasattr(self.parent, 'image_handler'):
            dialog = EditCardDialog(self.parent, card_data, self.parent.image_handler)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Get updated data from dialog
                updated_data = dialog.get_form_data()
                # Ensure profit is recalculated
                updated_data['profit'] = updated_data['expected_price'] - updated_data['purchase_price']
                # Ensure all required fields are present
                for key in ['brand','pin','denomination','purchase_price','expected_price','profit','source','purchase_date','pending','sold_date','payment_received','payment_mode','card_image_path']:
                    if key not in updated_data:
                        updated_data[key] = ''
                # Update the card in database
                if hasattr(self.parent, 'db_manager'):
                    success = self.parent.db_manager.update_card(card_data['card_number'], updated_data)
                    if success:
                        # Refresh the table
                        if hasattr(self.parent, 'refresh_cards'):
                            self.parent.refresh_cards()
                        QMessageBox.information(self.parent, "Success", "Card updated successfully!")
                    else:
                        QMessageBox.warning(self.parent, "Error", "Failed to update card!") 