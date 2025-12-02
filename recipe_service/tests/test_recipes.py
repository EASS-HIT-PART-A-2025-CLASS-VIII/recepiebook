def test_health_includes_app_name(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Recipe" in data["app"]


def test_create_recipe_returns_201_and_payload(client):
    response = client.post(
        "/recipes",
        json={
            "title": "pancakes",
            "description": "Fluffy pancakes",
            "ingredients": ["Flour", "Eggs"],
            "steps": ["Mix", "Cook"],
            "prep_minutes": 15,
        },
    )
    assert response.status_code == 201
    recipe = response.json()
    assert recipe["title"] == "Pancakes"
    assert recipe["prep_minutes"] == 15
    assert recipe["id"] == 1


def test_list_recipes_returns_created_recipe(client):
    client.post(
        "/recipes",
        json={
            "title": "salad",
            "description": "Green salad",
            "ingredients": ["Lettuce"],
            "steps": ["Chop", "Serve"],
            "prep_minutes": 5,
        },
    )

    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Salad"


def test_get_recipe_by_id(client):
    create_response = client.post(
        "/recipes",
        json={
            "title": "soup",
            "description": "Tomato soup",
            "ingredients": ["Tomatoes"],
            "steps": ["Boil"],
            "prep_minutes": 30,
        },
    )
    recipe_id = create_response.json()["id"]

    response = client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["id"] == recipe_id


def test_get_missing_recipe_returns_404(client):
    response = client.get("/recipes/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_delete_recipe(client):
    create_response = client.post(
        "/recipes",
        json={
            "title": "cake",
            "description": "Chocolate cake",
            "ingredients": ["Flour", "Cocoa"],
            "steps": ["Mix", "Bake"],
            "prep_minutes": 45,
        },
    )
    recipe_id = create_response.json()["id"]

    response = client.delete(f"/recipes/{recipe_id}")
    assert response.status_code == 204

    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 404


def test_prep_minutes_too_small_is_rejected(client):
    response = client.post(
        "/recipes",
        json={
            "title": "instant",
            "description": "Too fast",
            "ingredients": ["Magic"],
            "steps": ["Snap"],
            "prep_minutes": 0,
        },
    )
    assert response.status_code == 422
