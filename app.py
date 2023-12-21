from flask import Flask, render_template, request, redirect, url_for, session

from ingreso.login import loguear
from instructors.horario import get_sum_horas, get_cant_fichas, get_fichas_titular, cant_no_aprobados, not_approved_students

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

user = None
@app.route("/", methods=["GET", "POST"])
def login():
    global user, hours
    error = None
    if request.method == "POST":
        username = request.form["username"]        
        user = loguear(username)
        
        """ count_not_approved = len( cant_no_aprobados(user['document']) )
        
        quantity_groups = get_cant_fichas(user['name'])
        not_approved = not_approved_students(cant_no_aprobados(user['name'])) """

        if user:
            session["username"] = username
            session["user"] = user
            return redirect(url_for("dashboard"))             
        else:
            error = 'Usuario no registrado'
            return render_template("instructors/index.html", error=error)              
    return render_template("instructors/index.html")


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        user = session["user"]
        titular = get_fichas_titular(user['name'])            
        hours = get_sum_horas(user['name'])
        quantity_groups = get_cant_fichas(user['name'])
        return render_template("instructors/dashboard.html", user=user, hours=hours, quantity_groups=quantity_groups, titular=titular)
    else:
        return redirect(url_for("login"))

@app.route("/schedule")
def schedule():
    if "username" in session:
        return render_template("instructors/schedule.html")
    else:
        return redirect(url_for("login"))

@app.route("/course_schedule")
def course_schedule():
    if "username" in session:
        return render_template("instructors/course_schedule.html")
    else:
        return redirect(url_for("login"))

@app.route("/complaints")
def complaints():
    return render_template("instructors/complaints.html")

@app.route("/instructors")
def instructors():
    return render_template("instructors/instructors.html")

if __name__ == '__main__':
    app.run(debug=True)
    