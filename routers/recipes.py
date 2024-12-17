from fastapi import Depends, HTTPException, APIRouter, Query
from sqlmodel import Session, select
from db import get_session 
from schemas import Recipe, RecipeOutput, RecipeInput

router = APIRouter(prefix="/recipes")

#get all recipes
@router.get("/", response_model=list[RecipeOutput])
def get_recipes(session: Session = Depends(get_session)):
    recipes = session.exec(select(Recipe)).all()
    return [
        RecipeOutput(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients_list,
            method=recipe.method,
            rating=recipe.rating,
            img=recipe.img,
            vegetarian=recipe.vegetarian
        )
        for recipe in recipes
    ]


#search recipes by ingredients
@router.get("/ingresearch", response_model=list[RecipeOutput])
def search_recipes_by_ingredients(keyword: str, session: Session = Depends(get_session)):
    query = select(Recipe).where(Recipe.ingredients.contains(keyword))
    recipes = session.exec(query).all()
    return [
        RecipeOutput(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients_list,  # Convert to list
            method=recipe.method,
            rating=recipe.rating,
            img=recipe.img,
            vegetarian=recipe.vegetarian
        )
        for recipe in recipes
    ]

# Search recipes by rating
@router.get("/ratesearch", response_model=list[RecipeOutput])
def search_recipes_by_rating(rating: float, session: Session = Depends(get_session)):
    query = select(Recipe).where(Recipe.rating >= rating)
    recipes = session.exec(query).all()
    return [
        RecipeOutput(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients_list,  # Convert to list
            method=recipe.method,
            rating=recipe.rating,
            img=recipe.img,
            vegetarian=recipe.vegetarian
        )
        for recipe in recipes
    ]

# Search recipes by vegetarian status
@router.get("/vegsearch", response_model=list[RecipeOutput])
def search_recipes_by_vegetarian(vegetarian: bool, session: Session = Depends(get_session)):
    query = select(Recipe).where(Recipe.vegetarian == vegetarian)
    recipes = session.exec(query).all()
    return [
        RecipeOutput(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients_list,  # Convert to list
            method=recipe.method,
            rating=recipe.rating,
            img=recipe.img,
            vegetarian=recipe.vegetarian
        )
        for recipe in recipes
    ]

#combined search
@router.get("/search", response_model=list[RecipeOutput])
def search_recipes(
    ingredients: str | None = Query(None),
    rating: float | None = Query(None),
    vegetarian: bool | None = Query(None),
    session: Session = Depends(get_session)
):
    query = select(Recipe)

    # Add filters dynamically only if parameters are provided
    if ingredients:
        query = query.where(Recipe.ingredients.contains(ingredients))
    if rating is not None:
        query = query.where(Recipe.rating >= rating)
    if vegetarian is not None:
        query = query.where(Recipe.vegetarian == vegetarian)

    recipes = session.exec(query).all()
    return [
        RecipeOutput(
            id=recipe.id,
            title=recipe.title,
            ingredients=recipe.ingredients_list,
            method=recipe.method,
            rating=recipe.rating,
            img=recipe.img,
            vegetarian=recipe.vegetarian
        )
        for recipe in recipes
    ]

# Get a recipe by ID
@router.get("/{recipe_id}", response_model=RecipeOutput)
def get_recipe_by_id(recipe_id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Convert `ingredients` to a list using the property
    return RecipeOutput(
        id=recipe.id,
        title=recipe.title,
        ingredients=recipe.ingredients_list,  # Convert to list
        method=recipe.method,
        rating=recipe.rating,
        img=recipe.img,
        vegetarian=recipe.vegetarian
    )

# Add a new recipe
@router.post("/", response_model=RecipeOutput)
def create_recipe(recipe_input: RecipeInput, session: Session = Depends(get_session)):
    new_recipe = Recipe(
        title=recipe_input.title,
        method=recipe_input.method,
        rating=recipe_input.rating,
        img=recipe_input.img,
        vegetarian=recipe_input.vegetarian,
    )
    # Use the setter to populate the `ingredients` field
    new_recipe.ingredients_list = recipe_input.ingredients

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)
    return RecipeOutput(
        id=new_recipe.id,
        title=new_recipe.title,
        ingredients=new_recipe.ingredients_list,
        method=new_recipe.method,
        rating=new_recipe.rating,
        img=new_recipe.img,
        vegetarian=new_recipe.vegetarian
    )

# Update an existing recipe
@router.put("/{recipe_id}", response_model=RecipeOutput)
def update_recipe(recipe_id: int, recipe_data: RecipeInput, session: Session = Depends(get_session)):
    # Fetch the existing recipe
    recipe = session.get(Recipe, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update fields (convert ingredients list to a string)
    recipe.title = recipe_data.title
    recipe.method = recipe_data.method
    recipe.rating = recipe_data.rating
    recipe.img = recipe_data.img
    recipe.vegetarian = recipe_data.vegetarian
    recipe.ingredients_list = recipe_data.ingredients  # Use the setter to handle conversion

    # Commit the changes
    session.add(recipe)
    session.commit()
    session.refresh(recipe)
    
    # Return the updated recipe
    return RecipeOutput(
        id=recipe.id,
        title=recipe.title,
        ingredients=recipe.ingredients_list,  # Convert back to list for output
        method=recipe.method,
        rating=recipe.rating,
        img=recipe.img,
        vegetarian=recipe.vegetarian
    )

# Delete a recipe
@router.delete("/{id}", status_code=204)
def remove_recipe(id: int, session: Session = Depends(get_session)):
    recipe = session.get(Recipe, id)
    if recipe:
        session.delete(recipe)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No recipe with id={id}.")
