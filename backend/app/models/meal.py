from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .meal_item_meal_association import meal_item_meal_association
from .base import Base


class Meal(Base):
    __tablename__ = "meals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # Relation many-to-many avec MealItem
    meal_items: Mapped[list["MealItem"]] = relationship(  # type: ignore
        secondary=meal_item_meal_association, back_populates="meals"
    )
