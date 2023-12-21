import os
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from courses.horario_courses import get_schedule_course, generar_excel_course

from ingreso.login import loguear
from instructors.horario import get_sum_horas, get_cant_fichas, get_fichas_titular, cant_no_aprobados, not_approved_students, get_horario_i, generar_excel

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

user, ficha = None, None
trimestre_academico = '1-2024'
@app.route("/", methods=["GET", "POST"])
def login():
    global user, hours
    error = None
    if request.method == "POST":
        username = request.form["username"]        
        user = loguear(username)

        if user:
            session["username"] = username
            session["user"] = user
            return redirect(url_for("dashboard"))             
        else:
            error = 'Usuario no registrado'
            return render_template("instructors/index.html", error=error)              
    return render_template("instructors/index.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user", None)
    return redirect(url_for("login"))

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
        user = session["user"]
        schedule = get_horario_i(user['name'])    
        print(schedule)
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        hours = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
        hours_f = ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']
        hours_combined = zip(hours, hours_f)
        return render_template("instructors/schedule.html", user=user, schedule=schedule, days=days, hours_combined=hours_combined, trimestre= trimestre_academico)
    else:
        return redirect(url_for("login"))

@app.route("/schedule_down")
def schedule_down():
    if "username" in session:
        user = session["user"]
        generar_excel(get_horario_i(user['name']), f"Horario {trimestre_academico} - {user['name']}.xlsx")

        file_path = f"static/schedule-instructores/Horario {trimestre_academico} - {user['name']}.xlsx"        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return redirect(url_for("schedule"))
        

@app.route("/course_schedule", methods=["GET", "POST"])
def course_schedule():
    if "username" in session:
        error = None
        user = session["user"]
        if request.method == "POST":
            global ficha
            ficha = request.form["ficha"]
            if ficha:
                schedule_course = get_schedule_course(ficha)
                print(schedule_course)
                days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
                hours = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
                hours_f = ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']
                hours_combined = zip(hours, hours_f)   
                return render_template('courses/schedule.html', user=user, schedule_course=schedule_course, days=days, hours_combined=hours_combined, code_course= ficha, trimestre=trimestre_academico)     
            else:
                error = 'Ficha no encontrada'
                return render_template('courses/schedule.html', error=error)
        return render_template('courses/schedule.html', user=user)
    else:
        return redirect(url_for("login"))
    
@app.route("/schedule_course_down")
def schedule_course_down():
    if "username" in session:        
        generar_excel_course(get_schedule_course(ficha), f"Horario {trimestre_academico} - {ficha}.xlsx")

        file_path = f"static/schedule-courses/Horario {trimestre_academico} - {ficha}.xlsx"        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return redirect(url_for("course_schedule"))
        
@app.route("/complaints")
def complaints():
    return render_template("instructors/complaints.html")

@app.route("/instructors")
def instructors():
    return render_template("instructors/instructors.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
    