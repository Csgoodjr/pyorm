# pyorm

A lightweight Python ORM for simplified database interactions.

## Features

- Easy model definition
- Automatic table creation
- Query building with Python syntax
- Support for SQLite and PostgreSQL

## Installation

```bash
pip install pyorm
```

## Usage

```python
from pyorm import Model, StringField

class User(Model):
    name = StringField()
    email = StringField()

User.create_table()
user = User(name="Alice", email="alice@example.com")
user.save()
```

## License

MIT