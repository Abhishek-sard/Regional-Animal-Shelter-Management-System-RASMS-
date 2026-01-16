from flask import Flask, render_template, request, redirect, url_for, flash
import rasms

app = Flask(__name__)
app.secret_key = "super_secret_key_rasms"

# Load data on startup
shelters = rasms.load_data()

@app.route("/")
def index():
    total_revenue = sum(s.revenue for s in shelters)
    total_adopted = sum(s.adopted_count for s in shelters)
    return render_template("index.html", shelters=shelters, total_revenue=total_revenue, total_adopted=total_adopted)

@app.route("/revenue")
def revenue():
    total_revenue = sum(s.revenue for s in shelters)
    total_adopted = sum(s.adopted_count for s in shelters)
    return render_template("revenue_report.html", shelters=shelters, total_revenue=total_revenue, total_adopted=total_adopted)


@app.route("/inventory")
def inventory():
    return render_template("inventory.html", shelters=shelters)

@app.route("/move", methods=["GET", "POST"])
def move():
    if request.method == "POST":
        animal_id = request.form.get("animal_id")
        try:
            target_shelter_index = int(request.form.get("target_shelter"))
        except (ValueError, TypeError):
             flash("Invalid shelter selection", "danger")
             return redirect(url_for("move"))

        success, result = rasms.move_animal_core(shelters, animal_id, target_shelter_index)
        if success:
            rasms.save_data(shelters)
            flash(f"Moved {result['animal_name']} from {result['from_shelter']} to {result['to_shelter']}", "success")
        else:
            flash(result, "danger")
        return redirect(url_for("move"))
    
    all_animals = []
    for s in shelters:
        for a in s.animals:
            all_animals.append({"obj": a, "shelter": s.name})
            
    return render_template("move.html", shelters=shelters, animals=all_animals)

@app.route("/adopt", methods=["GET", "POST"])
def adopt():
    if request.method == "POST":
        animal_id = request.form.get("animal_id")
        success, result = rasms.adopt_animal_core(shelters, animal_id)
        if success:
            rasms.save_data(shelters)
            flash(f"Adopted! Fee: ${result}", "success")
        else:
            flash(result, "danger")
        return redirect(url_for("adopt"))

    all_animals = []
    for s in shelters:
        for a in s.animals:
            if a.status != "Adopted":
                all_animals.append(a)
    return render_template("adopt.html", animals=all_animals)

@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        animal_id = request.form.get("animal_id")
        action = request.form.get("action")
        value = request.form.get("value")
        
        success = False
        msg = ""

        if action == "health":
            success, msg = rasms.update_health_core(shelters, animal_id, value)
        elif action == "status":
            success, msg = rasms.update_status_core(shelters, animal_id, value)
        else:
            msg = "Invalid action"
            
        if success:
            rasms.save_data(shelters)
            flash(msg, "success")
        else:
            flash(msg, "danger")
        return redirect(url_for("update"))
        
    all_animals = []
    for s in shelters:
        for a in s.animals:
            all_animals.append(a)
    return render_template("update.html", animals=all_animals)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
