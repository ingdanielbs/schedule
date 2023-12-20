import os
from django.http import Http404, HttpResponse
from django.shortcuts import render


from . import horario
from . models import Instructor
from courses import complaint
document = ''
trimestre_academico = '1-2024'
def index_instructors(request):
    if request.method == 'POST':
        global document
        document = request.POST['username']
        instructor = Instructor.objects.filter(document=document).first()        
        hours = horario.get_sum_horas(instructor.name)
        count_not_approved = len( horario.cant_no_aprobados(document) )
        
        quantity_groups = horario.get_cant_fichas(instructor.name)
        titular = horario.get_fichas_titular(instructor.name)            
        not_approved = horario.not_approved_students(horario.cant_no_aprobados(document))
        print(not_approved)
        if instructor:
            return render(request, 'instructors/dashboard.html', {'instructor': instructor, 'hours': hours, 'quantity_groups': quantity_groups, 'titular': titular, 'count_not_approved': count_not_approved, 'not_approved': not_approved})
        else:
            message = 'Instructor no encontrado'
            return render(request, 'instructors/index.html', {'message': message})              
    return render(request, 'instructors/index.html')      

def dashboard(request):
    global document
    instructor = Instructor.objects.filter(document=document).first()
    hours = horario.get_sum_horas(instructor.name)
    quantity_groups = horario.get_cant_fichas(instructor.name)
    count_not_approved = len( horario.cant_no_aprobados(document) )
    titular = horario.get_fichas_titular(instructor.name)            
    not_approved = horario.not_approved_students(horario.cant_no_aprobados(document))
    return render(request, 'instructors/dashboard.html', {'instructor': instructor, 'hours': hours, 'quantity_groups': quantity_groups, 'titular': titular, 'not_approved': not_approved, 'trimestre': trimestre_academico, 'count_not_approved': count_not_approved})

def schedule(request):    
    instructor = Instructor.objects.filter(document=document).first()    
    schedule = horario.get_horario_i(instructor.name)    
    print(schedule)
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
    hours = ['h6_7', 'h7_8', 'h8_9', 'h9_10', 'h10_11', 'h11_12', 'h12_13', 'h13_14', 'h14_15', 'h15_16', 'h16_17', 'h17_18', 'h18_19', 'h19_20', 'h20_21', 'h21_22']
    hours_f = ['6:00 - 7:00', '7:00 - 8:00', '8:00 - 9:00', '9:00 - 10:00', '10:00 - 11:00', '11:00 - 12:00', '12:00 - 13:00', '13:00 - 14:00', '14:00 - 15:00', '15:00 - 16:00', '16:00 - 17:00', '17:00 - 18:00', '18:00 - 19:00', '19:00 - 20:00', '20:00 - 21:00', '21:00 - 22:00']
    hours_combined = zip(hours, hours_f)
    return render(request, 'instructors/schedule.html', {'schedule': schedule, 'days': days, 'hours_combined': hours_combined, 'trimestre': trimestre_academico})      


def schedule_down(request):    
    instructor = Instructor.objects.filter(document=document).first()
    horario.generar_excel(horario.get_horario_i(instructor.name), f'Horario {trimestre_academico} - {instructor.name}.xlsx')
    
    file_path = f'static/schedule-instructores/horario {trimestre_academico} - {instructor.name}.xlsx'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404




    

