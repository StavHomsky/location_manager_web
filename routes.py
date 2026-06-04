import json
from flask import Blueprint, render_template, request, redirect
from storage import load_locations, save_locations, get_next_id

main_bp = Blueprint("main", __name__)
@main_bp.route("/")
def index():
 locations = load_locations()
 
 filter_by = request.args.get("filter_by", "")
 filter_value = request.args.get("filter_value", "")

 all_types = sorted(
    list(set(location["type"] for location in locations))
 )

 all_countries = sorted(
    list(set(location["country"] for location in locations))
)

 filtered_locations = locations

 if filter_by == "type" and filter_value:
    filtered_locations = [
        location
        for location in locations
        if location["type"] == filter_value
    ]

 elif filter_by == "country" and filter_value:
    filtered_locations = [
        location
        for location in locations
        if location["country"] == filter_value
    ]

 total_locations = len(locations)
 visited_count = sum(1 for location in locations if location["visited"])
 wishlist_count = total_locations - visited_count

 return render_template(
    "index.html",
    locations=filtered_locations,
    total_locations=total_locations,
    visited_count=visited_count,
    wishlist_count=wishlist_count,
    all_types=all_types,
    all_countries=all_countries,
    filter_by=filter_by,
    filter_value=filter_value
)

@main_bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        locations = load_locations()

        new_location = {
            "id": get_next_id(locations),
            "name": request.form["name"],
            "country": request.form["country"],
            "type": request.form["type"],
            "visited": "visited" in request.form
        }

        locations.append(new_location)
        save_locations(locations)

        return redirect("/")

    return render_template("add.html")


@main_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    locations = load_locations()
    location = next((l for l in locations if l["id"] == id), None)

    if request.method == "POST":
        location["name"] = request.form["name"]
        location["country"] = request.form["country"]
        location["type"] = request.form["type"]
        location["visited"] = "visited" in request.form

        save_locations(locations)
        return redirect("/")

    return render_template("edit.html", location=location)


@main_bp.route("/delete/<int:id>")
def delete(id):
    locations = load_locations()
    locations = [l for l in locations if l["id"] != id]
    save_locations(locations)
    return redirect("/")

@main_bp.route("/import", methods=["GET", "POST"])
def import_locations():
    if request.method == "POST":
        file = request.files.get("json_file")
        action = request.form.get("action")

        if not file or file.filename == "":
            return redirect("/import")

        imported_locations = json.load(file)

        if not isinstance(imported_locations, list):
            return redirect("/import")

        cleaned_locations = []

        next_id = 1 if action == "replace" else get_next_id(load_locations())

        for location in imported_locations:
            cleaned_location = {
                "id": next_id,
                "name": location.get("name", ""),
                "country": location.get("country", ""),
                "type": location.get("type", ""),
                "visited": location.get("visited", False)
            }

            cleaned_locations.append(cleaned_location)
            next_id += 1

        if action == "replace":
            save_locations(cleaned_locations)

        elif action == "append":
            current_locations = load_locations()
            current_locations.extend(cleaned_locations)
            save_locations(current_locations)

        return redirect("/")

    return render_template("import.html")