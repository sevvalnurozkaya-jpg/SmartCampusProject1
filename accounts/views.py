from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    if request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    elif request.user.role == 'STAFF':
        return redirect('staff_dashboard')
    else:
        return redirect('student_dashboard')