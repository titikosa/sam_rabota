from flask import Flask, render_template, request, redirect, url_for, abort
from database import init_app, init_db
import models

app = Flask(__name__)
app.config["DATABASE"] = "recipes.db"
app.config["SECRET_KEY"] = "dev-secret-key"

init_app(app)

CATEGORIES = ["супы", "салаты", "десерты", "завтраки", "основные блюда", "напитки", "другое"]


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    recipes = models.get_all_recipes(search=search or None, category=category or None)
    return render_template("index.html", recipes=recipes, search=search,
                           category=category, categories=CATEGORIES)


@app.route("/recipe/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = models.get_recipe_by_id(recipe_id)
    if recipe is None:
        abort(404)
    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/add", methods=["GET", "POST"])
def add_recipe():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "")
        ingredients = request.form.get("ingredients", "")
        instructions = request.form.get("instructions", "")
        category = request.form.get("category", "другое")
        cook_time = request.form.get("cook_time", "")

        error = models.validate_recipe(title, ingredients, instructions)
        if error is None:
            models.add_recipe(title, ingredients, instructions, category, cook_time)
            return redirect(url_for("index"))

    return render_template("add_recipe.html", error=error, categories=CATEGORIES)


@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = models.get_recipe_by_id(recipe_id)
    if recipe is None:
        abort(404)

    error = None
    if request.method == "POST":
        title = request.form.get("title", "")
        ingredients = request.form.get("ingredients", "")
        instructions = request.form.get("instructions", "")
        category = request.form.get("category", "другое")
        cook_time = request.form.get("cook_time", "")

        error = models.validate_recipe(title, ingredients, instructions)
        if error is None:
            models.update_recipe(recipe_id, title, ingredients, instructions, category, cook_time)
            return redirect(url_for("recipe_detail", recipe_id=recipe_id))

    return render_template("edit_recipe.html", recipe=recipe, error=error, categories=CATEGORIES)


@app.route("/delete/<int:recipe_id>", methods=["POST"])
def delete_recipe(recipe_id):
    recipe = models.get_recipe_by_id(recipe_id)
    if recipe is None:
        abort(404)
    models.delete_recipe(recipe_id)
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


with app.app_context():
    init_db()


if __name__ == "__main__":
    app.run(debug=True)