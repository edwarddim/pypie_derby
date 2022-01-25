from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.pie import Pie


@app.route('/dashboard')
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    all_pies = Pie.get_all_from_user({'creator_id' : session['user_id']})


    return render_template('dashboard.html', pies = all_pies)


@app.route('/pies')
def pies():

    # pies = Pie.get_all()
    pies = Pie.get_pies_with_votes()


    return render_template("pies.html", pies = pies)


# CREATE PIE
@app.route("/pies/new", methods=["POST"])
def create_pie():
    if not Pie.validate(request.form):
        return redirect("/dashboard")
    data = {
        **request.form,
        'creator_id' : session['user_id']
    }
    Pie.save(data)
    return redirect("/dashboard")


# EDIT PIE
@app.route("/pies/<int:pie_id>/edit")
def edit_pie(pie_id):
    pie = Pie.get_one({"pie_id" : pie_id})
    return render_template("edit.html", pie = pie)

@app.route("/pies/<int:pie_id>/update", methods=["POST"])
def update_pie(pie_id):
    if not Pie.validate(request.form):
        return redirect(f"/pies/{pie_id}/edit")
    data = {
        **request.form,
        'pie_id' : pie_id
    }
    Pie.update(data)
    return redirect("/dashboard")

# DELETE PIE
@app.route('/pies/<int:pie_id>/delete')
def delete_pie(pie_id):
    Pie.delete({'pie_id' : pie_id})
    return redirect("/dashboard")


# DISPLAY SINGLE PIE
@app.route("/pies/<int:pie_id>")
def one_pie(pie_id):
    pie = Pie.get_one({"pie_id" : pie_id})
    data = {
        'user_id' : session['user_id'],
        'pie_id' : pie_id
    }
    voted = Pie.check_vote(data)

    return render_template("show_pie.html", pie = pie, voted = voted)

# LIKE / DISLIKE
@app.route('/pies/<int:pie_id>/like', methods=['POST'])
def like_pie(pie_id):
    data = {
        'user_id' : session['user_id'],
        'pie_id' : pie_id
    }
    Pie.like(data)
    return redirect('/pies')

@app.route('/pies/<int:pie_id>/dislike', methods=['POST'])
def dislike_pie(pie_id):
    data = {
        'user_id' : session['user_id'],
        'pie_id' : pie_id
    }
    Pie.dislike(data)
    return redirect('/pies')