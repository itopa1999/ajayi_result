from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group= None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                messages.error(request, "You don't have access to view this page")
                return redirect('lecturerdashboard')
        return wrapper_func
    return decorator


def allowed_users1(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group= None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                messages.error(request, "You don't have access to view this page")
                return redirect('admindashboard')
        return wrapper_func
    return decorator

            
            