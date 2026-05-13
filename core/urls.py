from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # --- LOGIN ---
    path('', views.home_redirect, name='home'),

    path(
        'login/',
        auth_views.LoginView.as_view(template_name='core/login.html'),
        name='login'
    ),

    path(
        'logout/',
         auth_views.LogoutView.as_view(next_page='/'),
        name='logout'
    ),

    # --- DASHBOARD ---
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    path(
        'dashboard/student/',
        views.student_dashboard,
        name='student_dashboard'
    ),

    path(
        'dashboard/staff/',
        views.staff_dashboard,
        name='staff_dashboard_alt'
    ),

    # --- PROFILE ---
    path(
        'my-profile/',
        views.my_profile,
        name='my_profile'
    ),

    # --- STAFF / ADMIN ---
    path('staff-portal/', views.staff_dashboard, name='staff_dashboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),

    path(
        'admin-panel/users/change-role/<int:user_id>/',
        views.change_user_role,
        name='change_user_role'
    ),


    path(
    'admin-panel/users/',
    views.admin_user_management,
    name='admin_user_management'
    ),

    path(
        'admin-panel/events/approval/',
        views.admin_event_approval,
        name='admin_event_approval'
    ),

    path(
        'admin-panel/events/status/<int:event_id>/<str:status>/',
        views.update_event_status,
        name='update_event_status'
    ),

    path(
        'admin-panel/staff-applications/',
        views.manage_staff_applications,
        name='manage_staff_applications'
    ),

    path(
        'admin-panel/staff-applications/evaluate/<int:app_id>/<str:action>/',
        views.evaluate_staff_application,
        name='evaluate_staff_application'
    ),

    # --- STAFF MANAGEMENT ---
    path(
        'staff/events/',
        views.staff_event_management,
        name='staff_event_management'
    ),

    path(
        'staff/events/create/',
        views.create_event,
        name='create_event'
    ),

    path(
        'staff/applications/',
        views.manage_applications,
        name='manage_applications'
    ),


    path(
        'staff/applications/update/<int:app_id>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),

    path(
        'staff/reservations/',
        views.manage_reservations,
        name='manage_reservations'
    ),

    path(
        'staff/announcements/',
        views.manage_announcements,
        name='manage_announcements'
    ),


    path(
        'staff/reports/',
        views.staff_reports,
        name='staff_reports'
    ),

    # --- RESERVATION SYSTEM ---
    path(
        'my-reservations/',
        views.make_reservations,
        name='my_reservations'
    ),

    path(
        'reservation-history/',
        views.my_reservations,
        name='reservation_history'
    ),

    path(
        'fields/',
        views.book_study_room,
        name='field_list'
    ),

    path(
        'sports-booking/',
        views.book_sports_facility,
        name='sports_booking'
    ),

    path(
        'equipments/',
        views.equipment_list,
        name='equipment_list'
    ),

    path(
        'events/<int:event_id>/participants/',
        views.event_participants,
        name='event_participants'
    ),

    # --- OTHER ---
    path('clubs/', views.club_list, name='club_list'),

    path(
        'clubs/join/<int:club_id>/',
        views.join_club,
        name='join_club'
    ),

    path('events/', views.event_list, name='event_list'),

    path(
        'events/apply/<int:event_id>/',
        views.apply_event,
        name='apply_event'
    ),

    path(
        'my-applications/',
        views.my_applications,
        name='my_applications'
    ),

    path(
        'announcements/',
        views.announcements_list,
        name='announcements_list'
    ),

    path(
        'feedback/',
        views.send_feedback,
        name='send_feedback'
    ),

    path(
        'apply-for-staff/',
        views.apply_for_staff,
        name='apply_for_staff'
    ),

    path('staff/reports/', views.staff_reports, name='staff_reports'),


    path(
        'admin-panel/announcements/',
        views.admin_announcements,
        name='admin_announcements'
    ),
]