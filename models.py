from database import get_db


def get_all_recipes(search=None, category=None):
    db = get_db()
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY created_at DESC"
    recipes = db.execute(query, params).fetchall()
    return recipes


def get_recipe_by_id(recipe_id):
    db = get_db()
    recipe = db.execute(
        "SELECT * FROM recipes WHERE id = ?", (recipe_id,)
    ).fetchone()
    return recipe


def add_recipe(title, ingredients, instructions, category, cook_time):
    db = get_db()
    db.execute(
        """INSERT INTO recipes (title, ingredients, instructions, category, cook_time)
           VALUES (?, ?, ?, ?, ?)""",
        (title, ingredients, instructions, category, cook_time),
    )
    db.commit()


def update_recipe(recipe_id, title, ingredients, instructions, category, cook_time):
    db = get_db()
    db.execute(
        """UPDATE recipes
           SET title=?, ingredients=?, instructions=?, category=?, cook_time=?
           WHERE id=?""",
        (title, ingredients, instructions, category, cook_time, recipe_id),
    )
    db.commit()


def delete_recipe(recipe_id):
    db = get_db()
    db.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    db.commit()


def validate_recipe(title, ingredients, instructions):
    if not title or not title.strip():
        return "Название не может быть пустым"
    if not ingredients or not ingredients.strip():
        return "Ингредиенты не могут быть пустыми"
    if not instructions or not instructions.strip():
        return "Инструкция не может быть пустой"
    return None