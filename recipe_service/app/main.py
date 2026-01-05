from __future__ import annotations

import logging

from fastapi import FastAPI, HTTPException, status

from .dependencies import RepositoryDep, SettingsDep
from .models import Recipe, RecipeCreate

logger = logging.getLogger("recipe-service")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

app = FastAPI(title="Recipe Service", version="0.1.0")


@app.get("/health", tags=["diagnostics"])
def health(settings: SettingsDep) -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "app": settings.app_name}


@app.get("/recipes", response_model=list[Recipe], tags=["recipes"])
def list_recipes(repository: RepositoryDep) -> list[Recipe]:
    """Get all recipes."""
    return repository.list()


@app.post(
    "/recipes",
    response_model=Recipe,
    status_code=status.HTTP_201_CREATED,
    tags=["recipes"],
)
def create_recipe(
    payload: RecipeCreate,
    repository: RepositoryDep,
) -> Recipe:
    """Create a new recipe."""
    recipe = repository.create(payload)
    logger.info("recipe.created id=%s title=%s", recipe.id, recipe.title)
    return recipe


@app.get("/recipes/{recipe_id}", response_model=Recipe, tags=["recipes"])
def read_recipe(recipe_id: int, repository: RepositoryDep) -> Recipe:
    """Get a specific recipe by ID."""
    recipe = repository.get(recipe_id)
    if recipe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    return recipe


@app.delete(
    "/recipes/{recipe_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["recipes"],
)
def delete_recipe(recipe_id: int, repository: RepositoryDep) -> None:
    """Delete a recipe by ID."""
    if repository.get(recipe_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found",
        )
    repository.delete(recipe_id)
    logger.info("recipe.deleted id=%s", recipe_id)
