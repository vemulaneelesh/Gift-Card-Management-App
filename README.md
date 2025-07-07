# Gift Card Management System

A comprehensive PyQt6 application for managing gift cards with profit tracking, image storage, and detailed card information.

## Features

- **Add Gift Cards**: Store detailed information including brand, PIN, denomination, purchase price, expected price, and profit calculation
- **Image Upload**: Upload and store card images with preview functionality
- **View & Edit**: Display all cards in a table format with inline editing capabilities
- **Delete Cards**: Select and delete multiple cards with confirmation
- **Profit Tracking**: Automatic profit calculation based on purchase and expected prices
- **Database Management**: SQLite database with automatic migration and backup
- **Debug Tools**: Built-in database debugging and validation tools

## Project Structure

The application follows Python packaging standards and is organized into modular components:

```
Gift_Card_Management_App/
├── gift_card_app.py     # Main entry point
├── main_app.py          # Main application class and logic
├── database.py          # Database operations and management
├── image_handler.py     # Image upload and preview functionality
├── ui_components.py     # UI components and widgets
├── tests/               # Unit tests
│   ├── __init__.py
│   └── test_database.py
├── card_images/         # Directory for stored card images
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup script
├── pyproject.toml      # Modern Python packaging config
├── Makefile            # Development tasks
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # This documentation
```

## Modules

### 1. `database.py` - DatabaseManager
Handles all database operations:
- Database initialization and migration
- CRUD operations (Create, Read, Update, Delete)
- Card existence validation
- Debug information retrieval

### 2. `image_handler.py` - ImageHandler
Manages image-related functionality:
- Image upload and file selection
- Image preview and scaling
- Image storage with unique naming
- Directory management

### 3. `ui_components.py` - UI Components
Contains reusable UI components:
- `AddCardTab`: Form for adding new cards
- `ViewCardsTab`: Table for viewing and editing cards
- Form validation and data handling

### 4. `main_app.py` - Main Application
Orchestrates all components:
- Main window setup
- Signal connections
- Business logic coordination
- Error handling

## Installation

### Option 1: Direct Installation
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python gift_card_app.py
   ```

### Option 2: Package Installation
1. **Install as a package**:
   ```bash
   pip install -e .
   ```

2. **Run using the command**:
   ```bash
   gift-card-app
   ```

### Development Setup
For development, install additional tools:
```bash
make install-dev
```

## Development

### Available Commands
```bash
make help          # Show all available commands
make install       # Install dependencies
make test          # Run tests
make lint          # Run linting
make format        # Format code
make clean         # Clean generated files
make run           # Run the application
make build         # Build package
```

## Database Schema

The application uses SQLite with the following schema:

```sql
CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    card_number TEXT UNIQUE NOT NULL,
    card_holder TEXT NOT NULL,
    brand TEXT,
    pin TEXT,
    denomination REAL,
    purchase_price REAL,
    expected_price REAL,
    profit REAL,
    source TEXT,
    card_image_path TEXT,
    purchase_date TEXT,
    balance REAL NOT NULL,  -- Legacy column for compatibility
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage

### Adding a Card
1. Go to the "Add Card" tab
2. Fill in the required fields:
   - **Card Number**: Unique identifier (required)
   - **Card Holder**: Name of the card holder (required)
   - **Brand**: Gift card brand (required)
   - **PIN**: Security PIN (optional)
   - **Denomination**: Face value of the card
   - **Purchase Price**: How much you paid
   - **Expected Price**: How much you expect to receive
   - **Source**: Where you got the card
   - **Purchase Date**: When you purchased it
3. Optionally upload a card image
4. Click "Add Card"

### Viewing and Editing Cards
1. Go to the "View Cards" tab
2. Click "Refresh Cards" to load current data
3. Edit any field directly in the table (except Card Number)
4. Click "Save Changes" to persist your edits

### Deleting Cards
1. Select one or more cards in the table
2. Click "Delete Selected"
3. Confirm the deletion

### Debugging
- Use the "Debug: Check Database" button to inspect database contents
- Check for duplicate card numbers
- Verify data integrity

## Error Handling

The application includes comprehensive error handling:
- **Database Errors**: Connection timeouts, constraint violations
- **Input Validation**: Required fields, numeric validation
- **Image Errors**: File format, storage issues
- **User Feedback**: Clear error messages and confirmations

## Benefits of Modular Design

1. **Maintainability**: Each module has a single responsibility
2. **Testability**: Components can be tested independently
3. **Reusability**: UI components can be reused in other applications
4. **Scalability**: Easy to add new features or modify existing ones
5. **Debugging**: Easier to isolate and fix issues
6. **Packaging**: Follows Python packaging standards for distribution
7. **Development**: Standard development tools and workflows

## Future Enhancements

Potential improvements for the modular system:
- **Export/Import**: CSV/Excel export functionality
- **Search/Filter**: Advanced search and filtering capabilities
- **Reports**: Profit/loss reports and analytics
- **Backup**: Automatic database backup functionality
- **Settings**: User preferences and configuration
- **API Integration**: Connect to external gift card services
- **Testing**: Comprehensive test coverage
- **CI/CD**: Automated testing and deployment
- **Documentation**: API documentation and user guides

## Troubleshooting

### Common Issues

1. **"Database is locked"**: Close any other instances of the app
2. **"Card Number must be unique"**: Check for existing cards using debug function
3. **Image upload fails**: Ensure the card_images directory has write permissions
4. **PyQt6 not found**: Install with `pip install PyQt6`

### Debug Mode

Use the debug button to:
- View all cards in the database
- Check for specific card numbers
- Verify data integrity
- Identify duplicate entries

## License

This project is open source and available under the MIT License. 