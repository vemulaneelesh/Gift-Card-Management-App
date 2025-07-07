import os
import shutil
from datetime import datetime
from PyQt6.QtWidgets import QFileDialog, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageHandler:
    def __init__(self, image_dir="card_images"):
        self.image_dir = image_dir
        self.selected_image_path = ""
        self.ensure_image_directory()
    
    def ensure_image_directory(self):
        """Create the image directory if it doesn't exist"""
        if not os.path.exists(self.image_dir):
            os.makedirs(self.image_dir)
    
    def upload_image(self, parent_widget):
        """Open file dialog to select an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            parent_widget, "Select Card Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.selected_image_path = file_path
            return True, os.path.basename(file_path)
        return False, ""
    
    def save_image(self, card_number):
        """Save the selected image to the card_images directory"""
        if not self.selected_image_path:
            return ""
        
        try:
            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{card_number}_{timestamp}.jpg"
            destination = os.path.join(self.image_dir, filename)
            
            # Copy image to destination
            shutil.copy2(self.selected_image_path, destination)
            return destination
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")
    
    def show_preview(self, image_path, preview_label):
        """Show image preview in the given label"""
        if image_path and os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Get original image dimensions
                original_width = pixmap.width()
                original_height = pixmap.height()
                
                # Calculate optimal preview size based on image aspect ratio
                max_width = 180
                max_height = 240
                
                # Calculate scaling factor to fit within bounds while maintaining aspect ratio
                scale_factor = min(max_width / original_width, max_height / original_height)
                
                # Calculate new dimensions
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                
                # Scale the image
                scaled_pixmap = pixmap.scaled(
                    new_width, new_height,
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                
                # Set the pixmap
                preview_label.setPixmap(scaled_pixmap)
                
                # Adjust label size to fit the image with some padding
                preview_label.setFixedSize(new_width + 20, new_height + 20)
                
                preview_label.setStyleSheet("""
                    QLabel {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #ffffff, stop:0.5 #f8f9fa, stop:1 #e9ecef);
                        border: 3px solid #28a745;
                        border-radius: 15px;
                        padding: 10px;
                        margin: 5px;
                    }
                """)
                return True
        return False
    
    def clear_preview(self, preview_label):
        """Clear the image preview"""
        preview_label.clear()
        preview_label.setText("📱\n\nNo Image\n\nClick to Upload")
        # Reset to default size
        preview_label.setMinimumSize(150, 200)
        preview_label.setMaximumSize(250, 300)
        preview_label.setFixedSize(180, 220)  # Set a smaller default size
        preview_label.setStyleSheet("""
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
    
    def reset(self):
        """Reset the image handler state"""
        self.selected_image_path = ""
    
    def get_image_path(self):
        """Get the currently selected image path"""
        return self.selected_image_path 