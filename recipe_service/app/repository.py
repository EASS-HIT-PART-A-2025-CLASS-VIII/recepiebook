from __future__ import annotations

from typing import Dict

from .models import Recipe, RecipeCreate


class RecipeRepository:
    """In-memory storage for recipes."""

    def __init__(self) -> None:
        self._items: Dict[int, Recipe] = {}
        self._next_id: int = 1

    def list(self) -> list[Recipe]:
        return list(self._items.values())

    def create(self, payload: RecipeCreate) -> Recipe:
        recipe = Recipe(id=self._next_id, **payload.model_dump())
        self._items[recipe.id] = recipe
        self._next_id += 1
        return recipe

    def get(self, recipe_id: int) -> Recipe | None:
        return self._items.get(recipe_id)

    def delete(self, recipe_id: int) -> None:
        self._items.pop(recipe_id, None)

    def clear(self) -> None:
        """Used by tests to reset state."""
        self._items.clear()
        self._next_id = 1
