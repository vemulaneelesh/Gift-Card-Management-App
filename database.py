import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="giftcards.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT UNIQUE NOT NULL,
            card_holder TEXT NOT NULL,
            balance REAL NOT NULL
        )
        """)
        
        # Check if we need to migrate the database
        cursor.execute("PRAGMA table_info(cards)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add new columns if they don't exist
        if 'brand' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN brand TEXT")
        if 'pin' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN pin TEXT")
        if 'denomination' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN denomination REAL")
        if 'purchase_price' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN purchase_price REAL")
        if 'expected_price' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN expected_price REAL")
        if 'profit' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN profit REAL")
        if 'source' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN source TEXT")
        if 'card_image_path' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN card_image_path TEXT")
        if 'purchase_date' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN purchase_date TEXT")
        if 'created_at' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        if 'pending' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN pending TEXT DEFAULT 'No'")
        if 'sold_date' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN sold_date TEXT")
        if 'payment_received' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN payment_received REAL DEFAULT 0")
        if 'payment_mode' not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN payment_mode TEXT")
        
        # Update existing records to have default values for new columns
        cursor.execute("UPDATE cards SET brand = 'Unknown' WHERE brand IS NULL")
        cursor.execute("UPDATE cards SET denomination = balance WHERE denomination IS NULL")
        cursor.execute("UPDATE cards SET purchase_price = balance WHERE purchase_price IS NULL")
        cursor.execute("UPDATE cards SET expected_price = balance WHERE expected_price IS NULL")
        cursor.execute("UPDATE cards SET profit = 0 WHERE profit IS NULL")
        cursor.execute("UPDATE cards SET source = 'Unknown' WHERE source IS NULL")
        cursor.execute("UPDATE cards SET purchase_date = date('now') WHERE purchase_date IS NULL")
        cursor.execute("UPDATE cards SET pending = 'No' WHERE pending IS NULL")
        
        conn.commit()
        conn.close()
    
    def add_card(self, card_data):
        """Add a new gift card to the database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            
            # Check for existing card number
            cursor.execute("SELECT card_number FROM cards WHERE card_number = ?", (card_data['card_number'],))
            if cursor.fetchone():
                return False, "Card number already exists"
            
            # Insert new card
            cursor.execute("""
            INSERT INTO cards (card_number, card_holder, brand, pin, denomination, 
                              purchase_price, expected_price, profit, source, card_image_path, purchase_date, 
                              pending, sold_date, payment_received, payment_mode, balance) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                card_data['card_number'], card_data['card_holder'], card_data['brand'],
                card_data['pin'], card_data['denomination'], card_data['purchase_price'],
                card_data['expected_price'], card_data['profit'], card_data['source'],
                card_data['card_image_path'], card_data['purchase_date'], card_data['pending'],
                card_data['sold_date'], card_data['payment_received'], card_data['payment_mode'],
                card_data['denomination']
            ))
            conn.commit()
            return True, "Card added successfully"
            
        except Exception as e:
            if conn:
                conn.rollback()
            return False, str(e)
        finally:
            if conn:
                conn.close()
    
    def get_all_cards(self):
        """Get all cards from the database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT card_number, card_holder, brand, pin, denomination, 
                   purchase_price, expected_price, profit, source, purchase_date, 
                   pending, sold_date, payment_received, payment_mode, card_image_path
            FROM cards ORDER BY created_at DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            return []
        finally:
            if conn:
                conn.close()
    
    def update_card(self, card_number, card_data):
        """Update an existing card"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE cards SET card_holder = ?, brand = ?, pin = ?, denomination = ?,
                            purchase_price = ?, expected_price = ?, profit = ?, 
                            source = ?, purchase_date = ?, pending = ?, sold_date = ?,
                            payment_received = ?, payment_mode = ?, card_image_path = ? WHERE card_number = ?
            """, (
                card_data['card_holder'], card_data['brand'], card_data['pin'],
                card_data['denomination'], card_data['purchase_price'],
                card_data['expected_price'], card_data['profit'], card_data['source'],
                card_data['purchase_date'], card_data['pending'], card_data['sold_date'],
                card_data['payment_received'], card_data['payment_mode'], 
                card_data.get('card_image_path', ''), card_number
            ))
            conn.commit()
            return True
        except Exception as e:
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def delete_card(self, card_number):
        """Delete a card from the database"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cards WHERE card_number = ?", (card_number,))
            conn.commit()
            return True, "Card deleted successfully"
        except Exception as e:
            if conn:
                conn.rollback()
            return False, str(e)
        finally:
            if conn:
                conn.close()
    
    def check_card_exists(self, card_number):
        """Check if a card number already exists"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("SELECT card_number FROM cards WHERE card_number = ?", (card_number,))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conn:
                conn.close()
    
    def get_card_by_number(self, card_number):
        """Get a specific card by card number"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=20.0)
            cursor = conn.cursor()
            cursor.execute("""
            SELECT card_number, card_holder, brand, pin, denomination, 
                   purchase_price, expected_price, profit, source, purchase_date, 
                   card_image_path, pending, sold_date, payment_received, payment_mode
            FROM cards WHERE card_number = ?
            """, (card_number,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'card_number': row[0],
                    'card_holder': row[1],
                    'brand': row[2],
                    'pin': row[3],
                    'denomination': row[4],
                    'purchase_price': row[5],
                    'expected_price': row[6],
                    'profit': row[7],
                    'source': row[8],
                    'purchase_date': row[9],
                    'card_image_path': row[10],
                    'pending': row[11],
                    'sold_date': row[12],
                    'payment_received': row[13],
                    'payment_mode': row[14]
                }
            return None
        except Exception as e:
            return None
        finally:
            if conn:
                conn.close()
    
 