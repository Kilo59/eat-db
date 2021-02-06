"""
eat-db
~~~~~~
Tell me what I can eat.
"""
import logging

from .models import Item

logging.basicConfig()


__all__ = ["api", "database", "Item"]
