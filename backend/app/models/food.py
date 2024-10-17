from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Food(Base):
    """Class Food"""

    __tablename__ = "foods"

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

    def to_dict(self):
        """Method to transform the object into a dict"""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "brands": self.brands,
            "serving_quantity": self.serving_quantity,
            "unit": self.unit,
            "raw": self.raw,
            "energy_serving": self.energy_serving,
            "energy_100g": self.energy_100g,
            "fiber_serving": self.fiber_serving,
            "fiber_100g": self.fiber_100g,
            "salt_serving": self.salt_serving,
            "salt_100g": self.salt_100g,
            "carbohydrates_serving": self.carbohydrates_serving,
            "carbohydrates_100g": self.carbohydrates_100g,
            "fat_serving": self.fat_serving,
            "fat_100g": self.fat_100g,
            "proteins_serving": self.proteins_serving,
            "proteins_100g": self.proteins_100g,
        }
