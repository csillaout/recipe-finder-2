
from fastapi import FastAPI, HTTPException
import uvicorn
from schemas import load_db, save_db, RecipeInput, RecipeOutput

app = FastAPI(title="Recipe Finder")

recipes_db = load_db()


#read item
@app.get("/recipes/")
def get_recipes():
    return recipes_db

#filter the recipes by ingredients
@app.get("/recipes/ingresearch")
def search_recipes_by_ingredients(keyword: str) -> list:
    print(f"Loaded recipes: {recipes_db}")  # Check the content of recipes_db
    matching_recipes = [
        recipe for recipe in recipes_db if any(keyword.lower() in ingredient.lower() for ingredient in recipe.ingredients)
    ]
    return matching_recipes

#filter the recipes by ratings
@app.get("/recipes/ratesearch")
def search_recipes_by_rating(rating: float|None=None):
        result = [recipe.title for recipe in recipes_db if recipe.rating>= rating]
        return result

#filter the recipes by vegetarian = True
@app.get("/recipes/vegsearch")
def search_recipes_by_vegetarian(vegetarian: bool)->list:
    result = [recipe.title for recipe in recipes_db if recipe.vegetarian == vegetarian]
    return result

#add item to the list
@app.post("/recipes/", response_model=RecipeOutput)
def create_recipe(recipe: RecipeInput)->RecipeOutput: 
    new_recipe = RecipeOutput(id=len(recipes_db)+1,title=recipe.title,ingredients=recipe.ingredients, method=recipe.method, rating=recipe.rating, img=recipe.img, vegetarian=recipe.vegetarian)

    """the new recipe"""
    recipes_db.append(new_recipe)
    save_db(recipes_db)
    return new_recipe
   
@app.delete("/recipes/{id}", status_code=204)
def remove_recipe(id: int)-> None:
    matches = [recipe for recipe in recipes_db if recipe.id==id]
    if matches:
        recipe = matches[0]
        recipes_db.remove(recipe)
        save_db(recipes_db)
    else:
        raise HTTPException(status_code=404, detail=f"No recipe with id={id}")

@app.put("/recipes/{id}", response_model=RecipeOutput)
def change_recipe(id: int, new_data: RecipeInput) -> RecipeOutput:
    matches = [recipe for recipe in recipes_db if recipe.id==id]
    if matches:
        recipe = matches[0]
        recipe.title = new_data.title
        recipe.ingredients = new_data.ingredients
        recipe.method = new_data.method
        recipe.rating = new_data.rating
        recipe.img = new_data.img
        recipe.vegetarian = new_data.vegetarian 
        save_db(recipes_db)
        return recipe 
    else:
        raise HTTPException(status_code=404, detail=f"No recipe with id={id}")

    
    



#search recipes by id
@app.get("/recipes/{id}")
def recipe_by_id(id: int)-> list:
    result= [recipe for recipe in recipes_db if recipe.id ==id]
    if result:
        return result[0]
    else:
        raise HTTPException(status_code=404, detail=f"No recipe with id={id}.")




if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)