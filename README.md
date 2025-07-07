# Gift Card Management System

A simple PyQt6 application for managing gift cards with profit tracking and image storage.

## Features
- Add gift cards with brand, PIN, denomination, purchase price, expected price, and automatic profit calculation
- Upload and store card images
- View, edit, and delete cards in a table format
- SQLite database for persistent storage

## Project Structure

```
Gift_Card_Management_App/
├── gift_card_app.py
├── main_app.py
├── database.py
├── image_handler.py
├── ui_components.py
├── card_images/         # (ignored in git)
├── requirements.txt
├── setup.py
├── pyproject.toml
├── Makefile             # (ignored in git)
├── .gitignore
└── README.md
```

> **Note:**
> The following are ignored and not tracked in version control: `card_images/`, `Makefile`, all database files (`*.db`), the `LICENSE` file, and the `tests/` directory.

## .gitignore

```
__pycache__/
*.pyc
.env
.DS_Store
.vscode/
card_images/
Makefile
*.db
LICENSE
tests/
```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python gift_card_app.py
   ```

## Basic Usage
- Use the "Add Card" tab to add new gift cards and upload images.
- Use the "View Cards" tab to view, edit, or delete existing cards.

---

For more details, see the source code files. 