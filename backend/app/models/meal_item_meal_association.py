from sqlalchemy import Table, Column, ForeignKey
from .base import Base

meal_item_meal_association = Table(
    'meal_item_meal_association',
    Base.metadata,
    Column('meal_id', ForeignKey('meals.id'), primary_key=True),
    Column('meal_item_id', ForeignKey('meal_items.id'), primary_key=True)
)
