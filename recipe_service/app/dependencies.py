from collections.abc import Generator
from typing import Annotated

from fastapi import Depends

from .config import Settings
from .repository import RecipeRepository

# Singletons (one per process)
_settings = Settings()
_repository = RecipeRepository()


def get_settings() -> Settings:
    return _settings


def get_repository() -> Generator[RecipeRepository, None, None]:
    # Using a generator makes it easy to swap to DB sessions later
    yield _repository


# Type aliases for cleaner endpoint signatures
SettingsDep = Annotated[Settings, Depends(get_settings)]
RepositoryDep = Annotated[RecipeRepository, Depends(get_repository)]
