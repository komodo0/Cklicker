# coding: utf-8
from types import NoneType
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from datetime import date, datetime, timedelta
from drive.models import DriveList, Area, FullAddress, OperatorToDepartnemt, Department, DriveTime
import calendar


def DriveView(request):
    if request.POST:
        # Оператор, делающий заказ
        operator = auth.get_user(request)
        department = Department.objects.get(id=request.POST.get('department', ''))
        operator_to_department = OperatorToDepartnemt(operator=operator, department=department)
        operator_to_department.save()
        return redirect("/drive/signup/")

    args = {}

    args['username'] = auth.get_user(request).username

    if not args['username']:
        args['user_is_staff'] = False
    else:
        args['user_is_staff'] = auth.get_user(request).is_staff

    if datetime.now().hour < 3:
        args['date'] = date.today() - timedelta(1)
    else:
        args['date'] = date.today()

    args['registered_notes'] = DriveList.objects.filter(drive_date=args['date'])

    # Если у пользователя еще не выбрано подразделение (только зарегался), то его заставят выбрать подразделение
    if not args['username']:
        args['user_department'] = None
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator=auth.get_user(request))

        if not args['user_department']:
            args['user_department'] = None

    args['user_department_list'] = OperatorToDepartnemt.objects.all()

    drive_time_variants = set()

    # Добавляем поле департамент в набор записей, чтобы нагляднее было и трахаться меньше надо было
    for note in args['registered_notes']:
        try:
            note.department = OperatorToDepartnemt.objects.get(operator=note.address.operator).department
            drive_time_variants.add(note.drive_time)
        except:
            args = {}
            args['username'] = auth.get_user(request).username
            args[
                'error_description'] = "Каким-то образом в сегодняшней развозке оказался человек,в профиле которого не указан отдел, поправьте это делов базе, а то не заработает! (Если ты просто пиздюк работник - иди к старшему, он знает, что делать."
            return render_to_response('drive_error.html', args)

    args['departments'] = Department.objects.all()

    args['drive_time_variants'] = drive_time_variants  # DriveTime.objects.filter(is_available = True)

    response = render_to_response('drive_list.html', args)
    return response


def SignUpDriveView(request):
    if request.POST:
        # Оператор, делающий заказ
        operator = auth.get_user(request)

        # Время выезда
        time = DriveTime.objects.get(id=request.POST.get('time', ''))

        # Адрес, id которого указан в запросе
        address = FullAddress.objects.get(id=request.POST.get('address', ''))

        # Если чувак подделал запрос и записывается на чужой адрес
        if (address.operator != operator):
            args = {}
            args['username'] = auth.get_user(request).username
            args[
                'error_description'] = "Что-то ты не так отправляешь мне на сервер... Наебать вздумал? Или просто ошибка? Если ошибка - обратись к старшему, если наебываешь - пиздуй нахуй, пидор, говно, ебаное. Забаню в следующий раз!"
            return render_to_response('drive_error.html', args)

        # все заявки за сегодня, надо вытащить за текущего юзера
        drive_list_today = DriveList.objects.filter(drive_date=date.today())

        # Заявка за текущего юзера
        current_note = None
        for note in drive_list_today:
            if note.address.operator == operator:
                current_note = note

        if current_note is None:
            current_note = DriveList(address=address, drive_date=date.today(), drive_time=time)
        else:
            current_note.address = address
            current_note.drive_time = time
        current_note.save()

        return redirect("/drive/signup/")

    args = {}
    args['username'] = auth.get_user(request).username

    if not args['username']:
        return redirect("/drive/")

    args['user_is_staff'] = auth.get_user(request).is_staff

    args['date'] = date.today()

    drive_list_today = DriveList.objects.filter(drive_date=date.today())
    current_note = None
    for note in drive_list_today:
        if note.address.operator == auth.get_user(request):
            current_note = note

    args['current_address'] = current_note
    args['addresses'] = FullAddress.objects.filter(operator=auth.get_user(request), was_deleted=False)
    args['drive_time_variants'] = DriveTime.objects.filter(is_available=True)

    if not args['username']:
        return redirect("/drive/")
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator=auth.get_user(request))
        if not args['user_department']:
            return redirect("/drive/")

    args['department'] = OperatorToDepartnemt.objects.get(operator=auth.get_user(request)).department.name

    args['current_time'] = datetime.now()
    if args['current_time'] < datetime.now().replace(hour=9, minute=0, second=0) or args[
        'current_time'] > datetime.now().replace(hour=19, minute=10, second=0):
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
    args['user_is_staff'] = auth.get_user(request).is_staff
    args['addresses'] = FullAddress.objects.filter(operator=user, was_deleted=False)
    args['areas'] = Area.objects.all()
    if not args['username']:
        return redirect("/drive/")
    else:
        args['user_department'] = OperatorToDepartnemt.objects.filter(operator=auth.get_user(request))
        if not args['user_department']:
            return redirect("/drive/")
    response = render_to_response('my_address_list.html', args)
    return response


def AddAddress(request):
    if request.POST:
        operator = auth.get_user(request)
        address = request.POST.get('address', '')
        area = Area.objects.get(id=request.POST.get('area_id', ''))
        address_note = FullAddress(address=address, area=area, operator=operator)
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


def DriveHistory(request):
    args = {}
    args['username'] = auth.get_user(request).username
    if not args['username']:
        return redirect("/drive/")
    args['user_is_staff'] = auth.get_user(request).is_staff
    if not args['user_is_staff']:
        return redirect("/drive/")

    try:
        args['search_date'] = request.GET.get('search_date', '')
        print(args['search_date'])
        args['search_date'] = datetime.strptime(args['search_date'], "%d.%m.%Y").date()
        print(args['search_date'])
    except:
        args['search_date'] = None

    args['registered_notes'] = DriveList.objects.filter(drive_date=args['search_date'])

    drive_time_variants = set()
    # Добавляем поле департамент в набор записей, чтобы нагляднее было и трахаться меньше надо было
    for note in args['registered_notes']:
        try:
            note.department = OperatorToDepartnemt.objects.get(operator=note.address.operator).department
            drive_time_variants.add(note.drive_time)
        except:
            args = {}
            args['username'] = auth.get_user(request).username
            args[
                'error_description'] = "Каким-то образом в сегодняшней развозке оказался человек,в профиле которого не указан отдел, поправьте это делов базе, а то не заработает! (Если ты просто пиздюк работник - иди к старшему, он знает, что делать."
            return render_to_response('drive_error.html', args)

        args['drive_time_variants'] = drive_time_variants

    return render_to_response('history.html', args)
