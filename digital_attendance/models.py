from django.db import models
from django.contrib.auth.models import User

# 1. Meza ya UserProfile (Inayotunza Reg Number kama mwanafunzi)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    reg_number = models.CharField(max_length=50, unique=True, verbose_name="Registration Number")

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.reg_number})"

# 2. Meza ya Mahudhurio (Attendance)
class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey('AttendanceSession', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True) # Inasave tarehe tu kwa urahisi wa mfumo
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Sick', 'Sick')])
    reason = models.TextField(blank=True, null=True)
    medical_document = models.FileField(upload_to='medical_docs/', blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.date} ({self.status})"

# 3. Meza ya Matangazo (Announcement)
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# 4. Meza ya Nyaraka za Masomo (Material)
class Material(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='class_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# CHINI KABISA YA MODELS.PY:

class AttendanceSession(models.Model):
    module_name = models.CharField(max_length=100, verbose_name="Jina la Somo")
    module_code = models.CharField(max_length=20, verbose_name="Code ya Somo")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def is_active(self):
        # Kipindi kinadumu masaa 2 (sekunde 7200) tangu CR akifungue
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() < 7200

    def __str__(self):
        return f"{self.module_code} - {self.module_name}"