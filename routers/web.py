from fastapi import APIRouter, Request, Form, Depends, Cookie
from sqlmodel import Session
from starlette.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from db import get_session
from routers.recipes import search_recipes_by_ingredients
from routers.recipes import search_recipes_by_vegetarian
from routers.recipes import search_recipes_by_rating
from routers.recipes import search_recipes

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request, recipes_cookie: str | None = Cookie(None) ):
    print(recipes_cookie)
    return templates.TemplateResponse("home.html", {"request": request})

#combined search
@router.post("/search", response_class=HTMLResponse)
def search(
    *,
    request: Request,
    ingredients: str = Form(None),
    rating: float = Form(None),
    vegetarian: str = Form(None),
    session: Session = Depends(get_session)
):
    # Convert rating to float if provided
    rating_float = float(rating) if rating else None
    
    # Convert vegetarian input to boolean if provided
    vegetarian_bool = None
    if vegetarian:
        vegetarian_bool = vegetarian.lower() == "yes"
    
    # Call the search function
    recipes = search_recipes(
        ingredients=ingredients,
        rating=rating_float,
        vegetarian=vegetarian_bool,
        session=session
    )
    
    return templates.TemplateResponse(
        "search_results.html", 
        {"request": request, "recipes": recipes}
    )

@router.post("/ingresearch", response_class=HTMLResponse)
def search_ingredients(
    *, ingredients: str = Form(...), request: Request, session: Session = Depends(get_session)
):
    # Call search_recipes with other parameters set to None
    recipes = search_recipes(ingredients=ingredients, rating=None, vegetarian=None, session=session)
    
    return templates.TemplateResponse("search_results.html", {"request": request, "recipes": recipes})



@router.post("/vegsearch", response_class=HTMLResponse)
def search_vegetarian(
    *, vegetarian: str = Form(...), request: Request, session: Session = Depends(get_session)
):
    # Convert vegetarian input to a boolean
    is_vegetarian = vegetarian.lower() == "yes"
    
    # Call search_recipes with other parameters set to None
    recipes = search_recipes(ingredients=None, rating=None, vegetarian=is_vegetarian, session=session)
    
    return templates.TemplateResponse("search_results.html", {"request": request, "recipes": recipes})

@router.post("/ratesearch", response_class=HTMLResponse)
def search_rating(
    *, rating: float = Form(...), request: Request, session: Session = Depends(get_session)
):
    # Call search_recipes with other parameters set to None
    recipes = search_recipes(ingredients=None, rating=rating, vegetarian=None, session=session)
    
    return templates.TemplateResponse("search_results.html", {"request": request, "recipes": recipes})


