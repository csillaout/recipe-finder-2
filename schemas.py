from pydantic import BaseModel
import json

class RecipeInput(BaseModel):
    title: str
    ingredients: list
    method: str
    rating: float | None = None
    img: str
    vegetarian: bool

    class Config:
        schema_extra = {
            "example":{
                 "title": "the best recipe",
                 "ingredients": "yummi ingredients",
                 "method": "the finest method",
                 "rating": 5,
                 "img" : "www.thebestrecipe.com",
                 "vegetarian": True
            }
        }

class RecipeOutput(RecipeInput):
    id:int


def load_db()-> list[RecipeOutput]:
    with open('recipes.json') as f:
        return [RecipeOutput.parse_obj(obj) for obj in json.load(f)]

def save_db(recipes: list[RecipeOutput]):
    with open("recipes.json", 'w') as f:
        json.dump([recipe.dict() for recipe in recipes], f, indent=4)