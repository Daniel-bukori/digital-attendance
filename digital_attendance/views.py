from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import Attendance, Announcement, Material, AttendanceSession
import datetime

# Fomu ya Signup
class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Jina la Kwanza")
    last_name = forms.CharField(max_length=30, required=True, label="Jina la Mwisho")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Registration Number"

# View ya Signup
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data.get('username').upper()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            login(request, user)
            messages.success(request, "Akaunti imetengenezwa kikamilifu!")
            return redirect('dashboard')
    else:
        form = CustomSignupForm()
    return render(request, 'digital_attendance/signup.html', {'form': form})

# View ya Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'digital_attendance/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    user = request.user
    announcements = Announcement.objects.all().order_by('-created_at')
    materials = Material.objects.all().order_by('-uploaded_at')
    all_attendance = Attendance.objects.all().order_by('-id')
    active_session = AttendanceSession.objects.last()
    already_submitted = False
    if active_session:
        already_submitted = Attendance.objects.filter(student=request.user, session=active_session).exists()

    is_cr = user.groups.filter(name='CR').exists() or user.is_staff
   
    context = {
        'announcements': announcements,
        'materials': materials,
        'all_attendance': all_attendance,
        'is_cr': is_cr,
        'active_session': active_session,       
        'already_submitted': already_submitted,
    }
    return render(request, 'digital_attendance/dashboard.html', context)


@login_required
def submit_attendance(request):
    if request.method == 'POST':
        today = datetime.date.today()
        if Attendance.objects.filter(student=request.user, date=today).exists():
            messages.error(request, "Tayari umeshasubmit mahudhurio ya leo!")
            return redirect('dashboard')
        status = request.POST.get('status')
        reason = request.POST.get('reason', '')
        medical_doc = request.FILES.get('medical_document', None)
        Attendance.objects.create(student=request.user, status=status, reason=reason, medical_document=medical_doc)
        messages.success(request, "Mahudhurio yako yamerekodiwa!")
    return redirect('dashboard')

@login_required
def post_announcement(request):
    if request.method == 'POST' and (request.user.groups.filter(name='CR').exists() or request.user.is_staff):
        title = request.POST.get('title')
        content = request.POST.get('content')
        Announcement.objects.create(title=title, content=content, created_by=request.user)
        messages.success(request, "Tangazo limerushwa!")
    return redirect('dashboard')

@login_required
def upload_material(request):
    if request.method == 'POST' and (request.user.groups.filter(name='CR').exists() or request.user.is_staff):
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        if file:
            Material.objects.create(title=title, description=description, file=file)
            messages.success(request, "Nyaraka imepakiwa!")
    return redirect('dashboard')

def view_document(request, file_type, file_id):
    if not request.user.is_authenticated:
        return redirect('login')
        
    file_url = ""
    file_name = ""
    
    if file_type == 'medical' and (request.user.groups.filter(name='CR').exists() or request.user.is_staff):
        att = Attendance.objects.get(id=file_id)
        if att.medical_document:
            file_url = att.medical_document.url
            file_name = f"Cheti cha {att.student.first_name}"
    elif file_type == 'material':
        mat = Material.objects.get(id=file_id)
        if mat.file:
            file_url = mat.file.url
            file_name = mat.title

    if not file_url:
        messages.error(request, "Faili halipatikani au huna mamlaka nalo!")
        return redirect('dashboard')

    return render(request, 'digital_attendance/view_document.html', {
        'file_url': file_url,
        'file_name': file_name
    })


from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponse
from django.template.loader import render_to_string

CHUO_LATITUDE = -3.4133   # GPS ya chuo chenu
CHUO_LONGITUDE = 36.7073
MAX_ALLOWED_DISTANCE = 500 # Mita 300 kutoka katikati ya chuo

def get_distance(lat1, lon1, lat2, lon2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 6371000

@login_required
def cr_start_session(request):
    """ CR anafungua kipindi kipya kwa kuweka Module Name na Code """
    if request.method == 'POST' and (request.user.groups.filter(name='CR').exists() or request.user.is_staff):
        m_name = request.POST.get('module_name')
        m_code = request.POST.get('module_code')
        AttendanceSession.objects.create(module_name=m_name, module_code=m_code, created_by=request.user)
        messages.success(request, f"🎉 Kipindi cha {m_code} - {m_name} kimefunguliwa kwa masaa 2!")
    return redirect('dashboard')

@login_required
def submit_attendance_smart(request):
    """ Mwanafunzi anasubmit: Kama ni mzima GPS inakaguliwa, kama anaumwa inapita na maelezo pamoja na cheti """
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        status = request.POST.get('status')
        session = AttendanceSession.objects.get(id=session_id)
        
        if not session.is_active():
            messages.error(request, "❌ Muda wa masaa 2 wa kipindi hiki umeshamalizika!")
            return redirect('dashboard')

        # HAPA NDIO TUMEREKEBISHA ILI KUNASA DATA ZOTE ZA UGONJWA KUTOKA KWENYE FOMU
        reason = request.POST.get('reason', '')
        medical_doc = request.FILES.get('medical_document', None)

        # USALAMA WA GPS: Unakagua tu kama mtumiaji amechagua 'Present'
        if status == 'Present':
            student_lat = request.POST.get('latitude')
            student_lon = request.POST.get('longitude')
            
            if not student_lat or not student_lon:
                messages.error(request, "❌ Imeshindwa kusoma GPS! Ruhusu Location kusign kama upo darasani.")
                return redirect('dashboard')
                
            distance = get_distance(float(student_lat), float(student_lon), CHUO_LATITUDE, CHUO_LONGITUDE)
            if distance > MAX_ALLOWED_DISTANCE:
                messages.error(request, f"❌ Huwezi kusign Present ukiwa nyumbani! (Uko mbali na chuo kwa mita {round(distance)})")
                return redirect('dashboard')
        
        # Sasa hapa reason na medical_document zinasave-iwa vizuri mwanafunzi anapojaza
        Attendance.objects.create(
            student=request.user, 
            session=session, 
            status=status,
            reason=reason,
            medical_document=medical_doc
        )
        messages.success(request, f"✅ Mahudhurio ya {session.module_code} yamesajiliwa!")
        
    return redirect('dashboard')

@login_required
def download_attendance_pdf(request, session_id):
    """ Inatengeneza ripoti safi kabisa ya PDF/Print kwa ajili ya Walimu """
    if request.user.is_staff or request.user.groups.filter(name='Lecturer').exists() or request.user.groups.filter(name='CR').exists():
        session = AttendanceSession.objects.get(id=session_id)
        records = Attendance.objects.filter(session=session)
        
        context = {'session': session, 'records': records}
        html_string = render_to_string('digital_attendance/attendance_pdf_template.html', context)
        
        response = HttpResponse(html_string, content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="Mahudhurio_{session.module_code}.html"'
        return response
    return HttpResponse("Huna mamlaka ya kuona ripoti hii.", status=403)