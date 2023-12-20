import os
from django.http import Http404, HttpResponse
from django.shortcuts import render
import pandas as pd

from courses import horario
from .complaint import complaints_students
from  .uploads import upl_students, upl_competences
from . models import Course, CourseStudent, CourseCompetence

code_course = ''
trimestre_academico = '4-2023'
def index_courses(request):    
    return render(request, 'courses/index.html')      

def schedule(request):    
    if request.method == 'POST':
        global code_course
        code_course = request.POST.get('ficha')        
        course = Course.objects.filter(code=code_course).first() 
        if course:
            schedule = horario.get_schedule_course(code_course)
            days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
            hours = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
            hours_f = ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']
            hours_combined = zip(hours, hours_f)   
            return render(request, 'courses/schedule.html', {'schedule': schedule, 'days': days, 'hours_combined': hours_combined, 'code_course': code_course, 'trimestre': trimestre_academico})     
        else:
            message = 'Ficha no encontrada'
            return render(request, 'courses/schedule.html', {'message': message})   
    return render(request, 'courses/schedule.html')      


def schedule_down(request):    
    course = Course.objects.filter(code=code_course).first()
    horario.generar_excel(horario.get_schedule_course(course.code), f'Horario {trimestre_academico} - {course.code}.xlsx')
    
    file_path = f'static/schedule-courses/Horario {trimestre_academico} - {course.code}.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def uploadStudents(request):
    if request.method == 'POST':
        code_course = request.POST.get('code_course')
        file = request.FILES['file']
        file.name = code_course + '.xlsx'
        file_path = f'static/course-students/{file.name}'
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        students = upl_students(code_course)
               
        for student_data in students:
            # Obtén el curso correspondiente al código del curso
            course = Course.objects.get(code=student_data['course'])

            # Elimina la clave 'course' de student_data
            del student_data['course']

            # Crea una nueva instancia de CourseStudent
            student = CourseStudent(course=course, **student_data)

            # Guarda la nueva instancia de CourseStudent en la base de datos
            student.save()                       

        return render(request, 'courses/uploadStudents.html', {'message': 'Archivo subido correctamente'})
    return render(request, 'courses/uploadStudents.html')

def uploadCompetences(request):
    if request.method == 'POST':
        code_course = request.POST.get('code_course')
        file = request.FILES['file']
        file.name = code_course + '.xlsx'
        file_path = f'static/course-competences/{file.name}'
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        competences = upl_competences(code_course)
        for competence_data in competences:
            # Obtén el curso correspondiente al código del curso
            course = Course.objects.get(code=competence_data['course'])

            # Elimina la clave 'course' de competence_data
            del competence_data['course']

            # Crea una nueva instancia de CourseCompetence
            competence = CourseCompetence(course=course, **competence_data)

            # Guarda la nueva instancia de CourseCompetence en la base de datos
            competence.save()
        return render(request, 'courses/uploadCompetences.html', {'message': 'Archivo subido correctamente'})
    return render(request, 'courses/uploadCompetences.html')

def complaints(request):
    comp_students = complaints_students()      
    
    return render(request, 'courses/complaints.html', {'comp_students': comp_students}) 


        
        
    