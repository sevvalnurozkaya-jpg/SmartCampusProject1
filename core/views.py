from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import (
    Event, Application, Announcement, Feedback, Club,
    ClubMember, AcademicCalendar, SportsField, FieldReservation,
    StaffApplication
)

from .forms import EventForm

User = get_user_model()


def is_admin(user):
    return user.is_authenticated and (
        getattr(user, 'role', None) == 'admin' or user.is_superuser
    )


def is_staff_member(user):
    staff_roles = ['staff', 'Kulüp / Akademisyen']
    return user.is_authenticated and (
        getattr(user, 'role', None) in staff_roles or user.is_staff
    )


def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    return redirect('login')


@login_required
def dashboard_redirect(request):
    if getattr(request.user, 'role', None) == 'staff' or getattr(request.user, 'role', None) == 'Kulüp / Akademisyen':
        return redirect('staff_dashboard')
    elif request.user.is_superuser or getattr(request.user, 'role', None) == 'admin':
        return redirect('admin_dashboard')
    else:
        return redirect('student_dashboard')


@login_required
def student_dashboard(request):
    if is_staff_member(request.user):
        return redirect('staff_dashboard')

    applied_events_ids = Application.objects.filter(student=request.user).values_list('event_id', flat=True)

    events = Event.objects.filter(status__iexact='approved').exclude(
        id__in=applied_events_ids
    ).order_by('-date')

    my_apps_count = Application.objects.filter(student=request.user).count()
    calendar_items = AcademicCalendar.objects.all().order_by('start_date')[:10]

    return render(request, 'core/student_dashboard.html', {
        'events': events,
        'my_apps_count': my_apps_count,
        'calendar_items': calendar_items
    })


@login_required
def booking_center(request):
    return render(request, 'core/booking_center.html')


@login_required
def make_reservations(request):
    return render(request, 'core/make_reservations.html')


@login_required
def my_reservations(request):
    reservations = FieldReservation.objects.filter(student=request.user).order_by('-date')
    return render(request, 'core/my_reservations.html', {
        'reservations': reservations
    })


@login_required
def book_study_room(request):
    if request.method == 'POST':
        reservation_type = request.POST.get('reservation_type')
        date = request.POST.get('res_date')
        time_slot = request.POST.get('time_slot')

        if not date or not time_slot:
            messages.error(request, "Please select date and time slot.")
            return redirect('field_list')

        if reservation_type == 'study':
            room_id = request.POST.get('room_id')

            if not room_id:
                messages.error(request, "Please select a study room.")
                return redirect('field_list')

            field_name = f"Study Room {room_id}"

            field, created = SportsField.objects.get_or_create(
                name=field_name,
                defaults={
                    'location': 'Study Area',
                    'description': 'Study room reservation'
                }
            )

        elif reservation_type == 'sports':
            field_id = request.POST.get('field_id')

            field_names = {
                'football_field': 'Football Field',
                'basketball_court': 'Basketball Court',
                'volleyball_court': 'Volleyball Court',
                'tennis_court': 'Tennis Court',
                'fitness_room': 'Fitness Room',
            }

            field_name = field_names.get(field_id)

            if not field_name:
                messages.error(request, "Invalid sports facility selected.")
                return redirect('field_list')

            field, created = SportsField.objects.get_or_create(
                name=field_name,
                defaults={
                    'location': 'Sports Area',
                    'description': 'Sports facility reservation'
                }
            )

        elif reservation_type == 'equipment':
            equipment_id = request.POST.get('equipment_id')

            equipment_names = {
                'football_ball': 'Football Ball',
                'basketball_ball': 'Basketball Ball',
                'volleyball_ball': 'Volleyball Ball',
                'tennis_racket': 'Tennis Racket',
                'badminton_racket': 'Badminton Racket',
                'training_cones': 'Training Cones',
                'jump_rope': 'Jump Rope',
            }

            field_name = equipment_names.get(equipment_id)

            if not field_name:
                messages.error(request, "Invalid equipment selected.")
                return redirect('field_list')

            field, created = SportsField.objects.get_or_create(
                name=field_name,
                defaults={
                    'location': 'Equipment Office',
                    'description': 'Sport equipment rental'
                }
            )

        else:
            messages.error(request, "Invalid reservation type.")
            return redirect('field_list')

        if FieldReservation.objects.filter(field=field, date=date, time_slot=time_slot).exists():
            messages.error(request, f"{field.name} is already reserved for this time.")
            return redirect('field_list')

        FieldReservation.objects.create(
            field=field,
            student=request.user,
            date=date,
            time_slot=time_slot
        )

        messages.success(request, f"Reservation for {field.name} confirmed!")
        return redirect('reservation_history')

    return render(request, 'core/field_list.html')


@login_required
def book_sports_facility(request):
    return redirect('field_list')


@login_required
def my_applications(request):
    apps = Application.objects.filter(student=request.user).select_related('event').order_by('-applied_at')
    return render(request, 'core/my_applications.html', {
        'apps': apps
    })


@login_required
def my_profile(request):
    return render(request, 'core/my_profile.html')


@login_required
@user_passes_test(is_staff_member)
def staff_dashboard(request):
    context = {
        'username': request.user.username,
        'total_events': Event.objects.count(),
        'pending_res': FieldReservation.objects.count(),
        'pending_apps': Event.objects.filter(status__iexact='pending').count(),
        'events': Event.objects.all().order_by('-date'),
    }

    return render(request, 'core/staff_dashboard.html', context)


@login_required
@user_passes_test(is_staff_member)
def staff_reports(request):
    popular_events = Event.objects.annotate(
        application_count=Count('application')
    ).order_by('-application_count')[:5]

    active_students = Application.objects.values(
        'student__username'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]

    most_used_reservations = SportsField.objects.annotate(
        reservation_count=Count('reservations')
    ).order_by('-reservation_count')[:5]

    context = {
        'total_events': Event.objects.count(),
        'total_applications': Application.objects.count(),
        'pending_requests': Event.objects.filter(status__iexact='pending').count(),
        'total_reservations': FieldReservation.objects.count(),
        'popular_events': popular_events,
        'active_students': active_students,
        'most_used_reservations': most_used_reservations,
    }

    return render(request, 'core/staff_reports.html', context)

@login_required
@user_passes_test(is_staff_member)
def manage_applications(request):
    apps = Application.objects.all().order_by('-applied_at')
    return render(request, 'core/manage_applications.html', {
        'apps': apps
    })


@login_required
@user_passes_test(is_staff_member)
def update_application_status(request, app_id, status):
    app = get_object_or_404(Application, id=app_id)
    app.status = status
    app.save()
    messages.info(request, f"Application status updated to {status}.")
    return redirect('manage_applications')


@login_required
@user_passes_test(is_staff_member)
def manage_reservations(request):
    reservations = FieldReservation.objects.all().order_by('-date')
    return render(request, 'core/manage_reservations.html', {
        'reservations': reservations
    })


@login_required
@user_passes_test(is_staff_member)
def manage_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'core/manage_announcements.html', {
        'announcements': announcements
    })


@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': User.objects.count(),
        'total_events': Event.objects.count(),
        'pending_events': Event.objects.filter(status__iexact='pending').count(),
        'staff_requests': StaffApplication.objects.count(),
        'recent_events': Event.objects.all().order_by('-date')[:6],
    }

    return render(request, 'core/admin_dashboard.html', context)

@user_passes_test(is_admin)
def manage_staff_applications(request):
    apps = StaffApplication.objects.all()
    return render(request, 'core/manage_staff_apps.html', {
        'apps': apps
    })


@user_passes_test(is_admin)
def evaluate_staff_application(request, app_id, action):
    app = get_object_or_404(StaffApplication, id=app_id)

    if action == 'approve':
        app.student.role = 'staff'
        app.student.is_staff = True
        app.student.save()
        app.delete()
        messages.success(request, f"{app.student.username} promoted to staff.")
    else:
        app.delete()
        messages.warning(request, "Application rejected.")

    return redirect('manage_staff_applications')

@user_passes_test(is_admin)
def admin_user_management(request):
    users = User.objects.all()

    stats = {
        'total_users': User.objects.count(),
        'student_count': User.objects.filter(role='student').count(),
        'staff_count': User.objects.filter(role='staff').count(),
    }

    return render(request, 'core/admin_users.html', {
        'users': users,
        'stats': stats
    })

@user_passes_test(is_admin)
def admin_event_approval(request):
    events = Event.objects.filter(status__iexact='pending')
    return render(request, 'core/admin_event_approval.html', {
        'pending_events': events
    })


@user_passes_test(is_admin)
def update_event_status(request, event_id, status):
    event = get_object_or_404(Event, id=event_id)
    event.status = status
    event.save()
    return redirect('admin_event_approval')


@login_required
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('-created_at')

    if request.user.role == 'admin':
        return render(request, 'core/admin_announcements.html', {
            'announcements': announcements
        })

    return render(request, 'core/announcements.html', {
        'announcements': announcements
    })

@login_required
def send_feedback(request):
    if request.method == 'POST':
        messages.success(request, "Feedback sent!")
        return redirect('student_dashboard')

    return render(request, 'core/feedback.html')


@login_required
def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'core/clubs.html', {
        'clubs': clubs
    })


@login_required
def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    ClubMember.objects.get_or_create(club=club, student=request.user)
    messages.success(request, f"You have joined {club.name}!")
    return redirect('club_list')


@login_required
def event_list(request):
    events = Event.objects.filter(status__iexact='approved')
    return render(request, 'core/events.html', {
        'events': events
    })


@login_required
def apply_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Application.objects.get_or_create(event=event, student=request.user)
    messages.success(request, "Application submitted for the event!")
    return redirect('event_list')


@login_required
@user_passes_test(is_staff_member)
def staff_event_management(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'core/staff_event_management.html', {
        'events': events
    })


@login_required
@user_passes_test(is_staff_member)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            event = form.save(commit=False)
            event.status = 'pending'
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('staff_dashboard')
    else:
        form = EventForm()

    return render(request, 'core/create_event.html', {
        'form': form
    })


@login_required
@user_passes_test(is_staff_member)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.warning(request, "Event deleted.")
    return redirect('staff_event_management')


@login_required
@user_passes_test(is_staff_member)
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Application.objects.filter(event=event).order_by('-applied_at')
    return render(request, 'core/event_participants.html', {
        'event': event,
        'participants': participants
    })


@login_required
def apply_for_staff(request):
    if request.method == 'POST':
        StaffApplication.objects.get_or_create(student=request.user)
        messages.success(request, "Staff application submitted!")
        return redirect('student_dashboard')

    return render(request, 'core/apply_staff.html')


@login_required
def equipment_list(request):
    return render(request, 'core/equipment_list.html')

@user_passes_test(is_admin)
def change_user_role(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_role = request.POST.get('role')

        if new_role in ['student', 'staff', 'admin']:
            user.role = new_role

            if new_role == 'staff':
                user.is_staff = True
                user.is_superuser = False
            elif new_role == 'admin':
                user.is_staff = True
                user.is_superuser = True
            else:
                user.is_staff = False
                user.is_superuser = False

            user.save()
            messages.success(request, f"{user.username}'s role updated to {new_role}.")

    return redirect('admin_user_management')

@user_passes_test(is_admin)
def admin_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'core/admin_announcements.html', {
        'announcements': announcements
    })