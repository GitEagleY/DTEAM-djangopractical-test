from django.db import models
from django.core.exceptions import ValidationError
from typing import Any, Dict, List

class ModelCV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.JSONField()
    projects = models.JSONField()
    contacts = models.JSONField()

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

def validate_list_of_strings(value: Any) -> None:
    """
    Validate that the value is a list of non-empty strings.
    
    Args:
        value: The value to validate
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, list):
        raise ValidationError(f"Expected a list, got {type(value).__name__}")
    
    for idx, item in enumerate(value):
        if not isinstance(item, str):
            raise ValidationError(f"Item at index {idx} must be a string, got {type(item).__name__}")
        if not item.strip():
            raise ValidationError(f"Item at index {idx} cannot be empty or just whitespace")

def validate_dict_of_strings(value: Any) -> None:
    """
    Validate that the value is a dictionary with non-empty string keys and values.
    
    Args:
        value: The value to validate
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, dict):
        raise ValidationError(f"Expected a dictionary, got {type(value).__name__}")
    
    for key, val in value.items():
        if not isinstance(key, str):
            raise ValidationError(f"Key '{key}' must be a string, got {type(key).__name__}")
        if not key.strip():
            raise ValidationError("Dictionary keys cannot be empty or just whitespace")
        if not isinstance(val, str):
            raise ValidationError(f"Value for key '{key}' must be a string, got {type(val).__name__}")
        if not val.strip():
            raise ValidationError(f"Value for key '{key}' cannot be empty or just whitespace")