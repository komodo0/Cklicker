# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from datetime import date, datetime
from drive.models import DriveList, Area, FullAddress, OperatorToDepartnemt, Department

# Create your views here.
def DriveView(request):

    if request.POST:
        #Оператор, делающий заказ
        operator = auth.get_user(request)
        department = Department.objects.get(id=request.POST.get('department', ''))
        operator_to_department = OperatorToDepartnemt(operator=operator, department=department)
        operator_to_department.save()
        return redirect("/drive/signup/")

    args = {}

    args['username'] = auth.get_user(request).username

    if datetime.now().hour < 3:
        args['date'] = date.today().replace(day=date.today().day-1)
    else:
        args['date'] = date.today()

    args['registered_notes'] = DriveList.objects.filter(drive_date=args['date'])
    if not args['username']:
        args['user_department'] = None
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator = auth.get_user(request))

        if not args['user_department']:
            args['user_department'] = None

    args['user_department_list'] = OperatorToDepartnemt.objects.all()

    #Добавляем поле департамент в набор записей, чтобы нагляднее было и трахаться меньше надо было
    for note in args['registered_notes']:
        try:
            note.department = OperatorToDepartnemt.objects.get(operator = note.address.operator).department
        except:
            args={}
            args['username'] = auth.get_user(request).username
            args['error_description'] = "Каким-то образом в сегодняшней развозке оказался человек,в профиле которого не указан отдел, поправьте это делов базе, а то не заработает! (Если ты просто пиздюк работник - иди к старшему, он знает, что делать."
            return render_to_response('drive_error.html', args)


    args['departments'] = Department.objects.all()

    response = render_to_response('drive_list.html', args)
    return response

def SignUpDriveView(request):
    if request.POST:
        #Оператор, делающий заказ
        operator = auth.get_user(request)

        #Адрес, id которого указан в запросе
        address = FullAddress.objects.get(id=request.POST.get('address', ''))

        #Если чувак подделал запрос и записывается на чужой адрес
        if (address.operator != operator):
            args={}
            args['username'] = auth.get_user(request).username
            args['error_description'] = "Что-то ты не так отправляешь мне на сервер... Наебать вздумал? Или просто ошибка? Если ошибка - обратись к старшему, если наебываешь - пиздуй нахуй, пидор, говно, ебаное. Забаню в следующий раз!"
            return render_to_response('drive_error.html', args)

        #все заявки за сегодня, надо вытащить за текущего юзера
        drive_list_today = DriveList.objects.filter(drive_date=date.today())

        #Заявка за текущего юзера
        current_note = None
        for note in drive_list_today:
            if note.address.operator == operator:
                current_note = note

        if current_note is None:
            current_note = DriveList(address=address)
        else:
            current_note.address = address
        current_note.save()

        return redirect("/drive/signup/")

    args = {}
    args['username'] = auth.get_user(request).username


    if not args['username']:
        return redirect("/drive/")

    args['date'] = date.today()

    drive_list_today = DriveList.objects.filter(drive_date=date.today())
    current_note = None
    for note in drive_list_today:
            if note.address.operator == auth.get_user(request):
                current_note = note

    args['current_address'] = current_note
    args['addresses'] = FullAddress.objects.filter(operator=auth.get_user(request), was_deleted=False)
    args['registered_notes'] = DriveList.objects.filter(drive_date=date.today())

    if not args['username']:
        return redirect("/drive/")
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator = auth.get_user(request))
        if not args['user_department']:
            return redirect("/drive/")

    args['department'] = OperatorToDepartnemt.objects.get(operator=auth.get_user(request)).department.name


    args['current_time'] = datetime.now()
    if args['current_time'] > datetime.now().replace(hour=2, minute=0, second=0) or args['current_time'] < datetime.now().replace(hour=9, minute=0, second=0) or args['current_time'] > datetime.now().replace(hour=21, minute=0, second=0):
        args['wrong_time'] = True
    else:
        args['wrong_time'] = False

    response = render_to_response('signup.html', args)
    return response

def AdressesDriveView(request):
    args = {}
    user = auth.get_user(request)
    args['username'] = auth.get_user(request).username
    if not args['username']:
        return redirect("/drive/")
    args['addresses'] = FullAddress.objects.filter(operator = user, was_deleted=False)
    args['areas'] = Area.objects.all()
    if not args['username']:
        return redirect("/drive/")
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator = auth.get_user(request))
        if not args['user_department']:
            return redirect("/drive/")
    response = render_to_response('my_address_list.html', args)
    return response

def AddAddress(request):
    if request.POST:
        operator = auth.get_user(request)
        address = request.POST.get('address', '')
        area = Area.objects.get(id=request.POST.get('area_id', ''))
        address_note = FullAddress(address=address, area = area, operator=operator)
        address_note.save()
    return redirect("/drive/addresses/")

def DeleteAddress(request):
    if request.POST:
        operator = auth.get_user(request)
        address_note = FullAddress.objects.get(id=request.POST.get('address_note_id', ''))
        if address_note.operator == operator:
            address_note.was_deleted = True
            address_note.save()

    return redirect("/drive/addresses/")