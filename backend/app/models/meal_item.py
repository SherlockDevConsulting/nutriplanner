from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Float, Integer, ForeignKey, String
from .base import Base
from .meal_item_meal_association import meal_item_meal_association
from .food import Food


class MealItem(Base):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[String] = mapped_column(String)
    note: Mapped[String] = mapped_column(String)

    food_id: Mapped[int] = mapped_column(ForeignKey("foods.id"))
    food: Mapped[Food] = relationship()

    # Relation many-to-many avec Meal
    meals: Mapped[list["Meal"]] = relationship(  # type: ignore
        secondary=meal_item_meal_association, back_populates="meal_items"
    )
