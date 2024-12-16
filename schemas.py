from sqlmodel import SQLModel, Field
from typing import List


class RecipeInput(SQLModel):
    title: str
    ingredients: List[str] 
    method: str
    rating: float | None = None
    img: str
    vegetarian: bool

    class Config:
        schema_extra = {
            "example": {
                "title": "Best Chocolate Cake",
                "ingredients": "flour, sugar, cocoa powder, eggs, milk",
                "method": "Mix all ingredients and bake at 180°C for 30 minutes.",
                "rating": 4.8,
                "img": "https://example.com/cake.jpg",
                "vegetarian": True
            }
        }


class Recipe(RecipeInput, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ingredients: str = Field(sa_column_kwargs={"nullable": False})
    
    @property
    def ingredients_list(self) -> List[str]:
        """Convert the comma-separated string back to a list."""
        return self.ingredients.split(", ")

    @ingredients_list.setter
    def ingredients_list(self, value: List[str]):
        """Convert a list to a comma-separated string for storage."""
        self.ingredients = ", ".join(value)

class RecipeOutput(SQLModel):
    id: int
    title: str
    ingredients: List[str]  # Output as a list for consistency
    method: str
    rating: float | None
    img: str
    vegetarian: bool