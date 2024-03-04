# FACILITY Management System

## Introduction
This is a simple facility management system 

## Features

## Technologies
- Python
- Django
- HTML
- CSS
- Bootstrap
- SQLite

## Setup
- Clone the repository
- Install the requirements by running `pip install -r requirements.txt`
- Run the application by running `python manage.py runserver`

## Author

## License
MIT
```

### 2. Create a new Django project
```bash
django-admin startproject facility_management_system
```

### 3. Create a new Django app
```bash
python manage.py startapp facility
```

### 4. Create the models
```python
# facility/models.py
from django.db import models

class Facility(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```


### 5. Create the views
```python
# facility/views.py
from django.shortcuts import render
from .models import Facility
```