from flask import Flask, render_template, request, redirect
from database import get_connection, init_db

app = Flask(__name__)

init_db()

@app.route("/")
def index():
    search = request.args.get("search", "")

    conn = get_connection()

    if search:
        recipes = conn.execute(
            "SELECT * FROM recipes WHERE title LIKE ?",
            (f"%{search}%",)
        ).fetchall()
    else:
        recipes = conn.execute(
            "SELECT * FROM recipes"
        ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        recipes=recipes
    )

@app.route("/add", methods=["GET", "POST"])
def add_recipe():

    if request.method == "POST":

        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        category = request.form["category"]

        conn = get_connection()

        conn.execute("""
        INSERT INTO recipes
        (title, ingredients, instructions, category)
        VALUES (?, ?, ?, ?)
        """,
        (title, ingredients, instructions, category))

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_recipe.html")

@app.route("/recipe/<int:id>")
def recipe_detail(id):

    conn = get_connection()

    recipe = conn.execute(
        "SELECT * FROM recipes WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if recipe is None:
        return "Recipe not found", 404

    return render_template(
        "recipe_detail.html",
        recipe=recipe
    )

@app.route("/delete/<int:id>")
def delete_recipe(id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM recipes WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)