from django.db import models
from django.conf import settings
from accounts.models import User

# ÖNEMLİ: Custom User modelini buradan sildik. 
# Onu accounts/models.py içinde tanımlamalısın.
# Eğer accounts içinde zaten varsa, Django çakışma hatası verir.

# 1. CLUB MODEL
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    logo_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 2. EVENT MODEL
class Event(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    capacity = models.PositiveIntegerField(default=50)
    is_free = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 3. EVENT APPLICATION MODEL
class Application(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"

# 4. CLUB MEMBER MODEL
class ClubMember(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='members')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'student')

# 5. ANNOUNCEMENT MODEL
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

# 6. FEEDBACK MODEL
class Feedback(models.Model):
    SUBJECT_CHOICES = [('suggestion', 'Suggestion'), ('complaint', 'Complaint'), ('request', 'Request'), ('other', 'Other')]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# 7. ACADEMIC CALENDAR MODEL
class AcademicCalendar(models.Model):
    event_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_holiday = models.BooleanField(default=False)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.event_name

# 8. SPORTS FIELD MODEL
class SportsField(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='fields/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 9. FIELD RESERVATION MODEL
class FieldReservation(models.Model):
    TIME_SLOTS = [
        ('09:00-10:00', '09:00-10:00'),
        ('10:00-11:00', '10:00-11:00'),
        ('11:00-12:00', '11:00-12:00'),
        ('13:00-14:00', '13:00-14:00'),
        ('14:00-15:00', '14:00-15:00'),
        ('15:00-16:00', '15:00-16:00'),
        ('16:00-17:00', '16:00-17:00'),
        ('17:00-18:00', '17:00-18:00'),
    ]

    field = models.ForeignKey(SportsField, on_delete=models.CASCADE, related_name='reservations')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('field', 'date', 'time_slot')
        ordering = ['date', 'time_slot']

    def __str__(self):
        return f"{self.student.username} - {self.field.name} ({self.date} {self.time_slot})"

# core/models.py en alta ekle

class StaffApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('approved', 'Onaylandı'),
        ('rejected', 'Reddedildi'),
    ]
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField(verbose_name="Neden Staff olmak istiyorsun?")
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.student.username} - Staff Başvurusu"

class StaffApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    motivation = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.status}"