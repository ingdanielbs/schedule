import os
from flask import Flask, flash, render_template, request, redirect, url_for, session, send_file, jsonify
from coordination.classroom_schedule import get_horario_ambiente
from coordination.dashboard import count_courses, count_instructors, count_not_approved_rap
from courses.competences import join_files
from courses.complaint import committe_history, complaints_students
from courses.horario_courses import get_schedule_course, generar_excel_course
from decorators.decorators import login_required
from ingreso.login import change_status, delete_user, get_users, instructor_list, loguear, register_user, update_user
from instructors.horario import apprentices_to_report, get_sum_horas, get_cant_fichas, get_fichas_titular, cant_no_aprobados, not_approved_students, get_horario_i, generar_excel

import pandas as pd

from datetime import timedelta


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=15)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
hours = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
hours_f = ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']

user = None
trimestre_academico = '1-2024'
@app.route("/", methods=["GET", "POST"])
def login():
    global user
    error = None
    if "username" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        remember = 'remember' in request.form        
        username = request.form["username"]        
        user = loguear(username)               
        if user and user["status"]:
            session["username"] = username
            session["user"] = user
            if remember:
                session.permanent = True
            else:
                session.permanent = False           
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
@login_required
def dashboard():    
    user = session["user"]              
    titular = get_fichas_titular(user['name'], trimestre_academico)            
    hours_trimestre = get_sum_horas(user['name'], trimestre_academico)
    quantity_groups = get_cant_fichas(user['name'], trimestre_academico)
    quantity_no_approved = len(cant_no_aprobados(str(user['document']))) 
    students_not_approved = not_approved_students(cant_no_aprobados(str(user['document'])))        
    apprentices_report = apprentices_to_report(students_not_approved, int(user['document'])) 
    quantity_instructors = count_instructors() 
    quantity_no_approved_rap = len(count_not_approved_rap())
    quantity_courses = count_courses()            
    return render_template("instructors/dashboard.html", user=user, hours_trimestre=hours_trimestre, quantity_groups=quantity_groups, titular=titular, quantity_no_approved=quantity_no_approved, trimestre=trimestre_academico, students_not_approved=students_not_approved, apprentices_report=apprentices_report, quantity_instructors=quantity_instructors, quantity_no_approved_rap=quantity_no_approved_rap, quantity_courses=quantity_courses)

@app.route("/schedule", methods=["GET", "POST"])
@login_required
def schedule():     
    user = session["user"]    
    hours_combined = zip(hours, hours_f)
    schedule = get_horario_i(user['name'], trimestre_academico)       
    return render_template("instructors/schedule.html", user=user, schedule=schedule, days=days, hours_combined=hours_combined, trimestre= trimestre_academico)

@app.route("/schedule_down")
@login_required
def schedule_down():    
    user = session["user"]
    generar_excel(get_horario_i(user['name'], trimestre_academico), f"Horario {trimestre_academico} - {user['name']}.xlsx")
    file_path = f"static/schedule-instructores/Horario {trimestre_academico} - {user['name']}.xlsx"        
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return redirect(url_for("schedule"))

@app.route("/course_schedule", methods=["GET", "POST"])
@login_required
def course_schedule():    
    error = None
    user = session["user"]
    global ficha
    if request.method == "POST":        
        hours_combined = zip(hours, hours_f)
        ficha = request.form["ficha"].strip()
        session['ficha_down'] = ficha
        if ficha:
            schedule_course = get_schedule_course(ficha, trimestre_academico)              
            return render_template('courses/schedule.html', user=user, schedule_course=schedule_course, days=days, hours_combined=hours_combined, code_course= ficha, trimestre=trimestre_academico)     
        else:
            error = 'Ficha no encontrada'
            return render_template('courses/schedule.html', error=error, user=user, trimestre=trimestre_academico)
    return render_template("courses/schedule.html", user=user, trimestre=trimestre_academico)        
    
@app.route("/schedule_course_down")
@login_required
def schedule_course_down():    
    ficha = session['ficha_down']
    generar_excel_course(get_schedule_course(ficha, trimestre_academico), f"Horario {trimestre_academico} - {ficha}.xlsx")
    file_path = f"static/schedule-courses/Horario {trimestre_academico} - {ficha}.xlsx"        
    if os.path.exists(file_path):                 
        return send_file(file_path, as_attachment=True)
    else:
        return redirect(url_for("course_schedule"))
        
@app.route("/complaints")
@login_required
def complaints():    
    user = session["user"]
    comp_students= complaints_students()
    return render_template("courses/complaints.html", user=user, comp_students=comp_students, trimestre=trimestre_academico)

@app.route("/upload_competences", methods=["GET", "POST"])
@login_required
def upload_competences():    
    user = session["user"]
    join_files()
    if request.method == "POST":
        code_course = request.form["code_course"]
        file = request.files["file"]           
        file.save(os.path.join("static/course-competences", code_course + ".xls"))
        return redirect(url_for("upload_competences"))            
    return render_template("courses/uploadCompetences.html", user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/history_complaints", methods=["GET", "POST"])
@login_required
def history_complaints():    
    user = session["user"]
    if request.method == "POST":              
        documento_aprendiz = request.form["documentoaprendiz"]
        try:
            data = committe_history(int(documento_aprendiz))
        except ValueError:
            return render_template("courses/historyComplaints.html", user=user, error='El valor ingresado debe ser un numero')
        if data:
            return render_template("courses/historyComplaints.html", data=data, user=user)
        else:
            return render_template("courses/historyComplaints.html", user=user, error='No se encontraron resultados')            
    
    return render_template("courses/historyComplaints.html", user=user, trimestre_academico=trimestre_academico)
    
@app.route("/schedule_instructors", methods=["GET", "POST"])
@login_required
def schedule_instructors():    
    user = session["user"]
    df = pd.read_excel('static/datalog/datos.xls')    
    """ instructors = list(df[(df['role'] == 'INSTRUCTOR') | (df['role'] == 'INSTRUCTOR_APOYO')]['name'].sort_values()) """
    instructors = instructor_list()      
      
    if request.method == "POST":        
        hours_combined = zip(hours, hours_f)
        name_i = request.form["instructor_name"]       
        schedule = get_horario_i(name_i, trimestre_academico)        
        return render_template("instructors/schedule_instructors.html", user=user, schedule=schedule, days=days, hours_combined=hours_combined, trimestre= trimestre_academico, instructors=instructors)    
    return render_template("instructors/schedule_instructors.html", user=user, instructors=instructors, trimestre= trimestre_academico)

@app.route("/schedule_classroom", methods=["GET", "POST"])
@login_required
def schedule_classroom():    
    user = session["user"]
    classroom_list = ['506','503','504','502','505','303','TEC303','2','703','806','705','801','802','701','706','702','704','805','803','501','203','605','205','411','0','1004','1003','1005','1007','1001','804','403','410']                    
    classroom_list.sort()
    if request.method == "POST":        
        hours_combined = zip(hours, hours_f)
        number_classroom = request.form["classroom_number".strip()]        
        if number_classroom != 'TEC303':
            number = int(number_classroom)
        else:
            number = number_classroom
        schedule = get_horario_ambiente(number)       
        return render_template("coordination/schedule_classroom.html", user=user, schedule=schedule, days=days, hours_combined=hours_combined, trimestre= trimestre_academico, number=number, classroom_list=classroom_list)
    return render_template("coordination/schedule_classroom.html", user=user, classroom_list=classroom_list, trimestre= trimestre_academico)
    
@app.route("/users", methods=["GET", "POST"])
@login_required
def users():    
    user = session["user"]        
    list_users = get_users()
    return render_template("users/index.html", user=user, list_users=list_users)    

@app.route("/users_state_change", methods=["GET", "POST"])
@login_required
def users_state_change():           
    if request.method == "POST":
        document = request.form["document"]            
        if change_status(document):
            flash('Estado cambiado correctamente', 'success')
            return redirect(url_for("users")) 
        else:
            flash('Error al cambiar el estado', 'error')
            return redirect(url_for("users")) 

@app.route("/users_register", methods=["GET", "POST"])
@login_required
def users_register():           
    if request.method == "POST":
        name = request.form["name"]
        document = request.form["document"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        contract_type = request.form["contract_type"]
        role = request.form["role"]
        registro = register_user(name, document, email, phone, gender, contract_type, role)
        if registro:
            flash('Usuario registrado correctamente', 'success')
            return redirect(url_for("users"))         
        else:
            flash('El usuario ya se encuentra registrado', 'error')
            return redirect(url_for("users"))

@app.route("/users_update/<id>", methods=["GET", "POST"])
@login_required
def users_update(id):               
    if request.method == "POST":
        name = request.form["name"]
        document = request.form["document"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        contract_type = request.form["contract_type"]
        role = request.form["role"]        
        update = update_user(id, name, document, email, phone, gender, contract_type, role)
        if update:
            flash('Usuario actualizado correctamente', 'success')
            return redirect(url_for("users"))         
        else:
            flash('Error al actualizar el usuario', 'error')
            return redirect(url_for("users"))
  
@app.route("/users_delete/<id>", methods=["GET", "POST"])
@login_required
def users_delete(id):  
    delete = delete_user(id)
    if delete:
        flash('Usuario eliminado correctamente', 'success')
        return redirect(url_for("users"))         
    else:
        flash('Error al eliminar el usuario', 'error')        
        return redirect(url_for("users"))    
   

if __name__ == '__main__':
    app.run(debug=True)
    