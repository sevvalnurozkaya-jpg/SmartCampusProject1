from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Yeni eklenen SportsField ve FieldReservation modellerini import listesine ekledik
from .models import Club, Event, Application, ClubMember, Announcement, Feedback, AcademicCalendar, SportsField, FieldReservation

# 1. USER MODEL KAYDI
User = get_user_model()

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Senin özel User modelindeki 'role' alanını buraya ekliyoruz
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

# 2. SPOR TESİSLERİ VE REZERVASYONLAR (YENİ)
@admin.register(SportsField)
class SportsFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(FieldReservation)
class FieldReservationAdmin(admin.ModelAdmin):
    # Kim, nereyi, ne zaman rezerve etmiş admin panelinde görebileceksin
    list_display = ('field', 'student', 'date', 'time_slot', 'created_at')
    list_filter = ('field', 'date', 'time_slot')
    search_fields = ('student__username', 'field__name')

# 3. DİĞER MODELLER
@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date', 'status', 'capacity')
    list_filter = ('status', 'organizer')
    search_fields = ('title', 'location')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'event', 'applied_at', 'status')
    list_filter = ('event', 'status')

@admin.register(ClubMember)
class ClubMemberAdmin(admin.ModelAdmin):
    list_display = ('student', 'club', 'status', 'joined_at')
    list_filter = ('status', 'club')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_active')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject_type', 'title', 'created_at')
    list_filter = ('subject_type',)

@admin.register(AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'start_date', 'end_date', 'is_holiday')
    list_filter = ('is_holiday',)
    search_fields = ('event_name',)
