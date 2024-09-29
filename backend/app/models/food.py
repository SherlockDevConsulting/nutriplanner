from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Food(Base):
    __tablename__ = 'foods'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brands: Mapped[str] = mapped_column(String)
    serving_quantity: Mapped[int] = mapped_column(Integer)
    unit: Mapped[str] = mapped_column(String)
    raw: Mapped[bool] = mapped_column(Boolean)
    energy_serving: Mapped[int] = mapped_column(Integer)
    energy_100g: Mapped[int] = mapped_column(Integer)
    fiber_serving: Mapped[float] = mapped_column(Float)
    fiber_100g: Mapped[float] = mapped_column(Float)
    salt_serving: Mapped[float] = mapped_column(Float)
    salt_100g: Mapped[float] = mapped_column(Float)
    carbohydrates_100g: Mapped[float] = mapped_column(Float)
    carbohydrates_serving: Mapped[float] = mapped_column(Float)
    fat_100g: Mapped[float] = mapped_column(Float)
    fat_serving: Mapped[float] = mapped_column(Float)
    proteins_100g: Mapped[float] = mapped_column(Float)
    proteins_serving: Mapped[float] = mapped_column(Float)
