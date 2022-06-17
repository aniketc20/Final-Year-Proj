from datetime import date
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from billboard.models import Billboard, Slot, SlotTimings
from django.contrib.auth.models import User
from .forms import RegistrationForm, AccountAuthenticationForm
from azure.storage.blob import BlockBlobService

# Create your views here.

def login_view(request):
    context = {}
    form = AccountAuthenticationForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("dashboard")
    context['login_form'] = form
    print(form.errors)
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    slots = SlotTimings.objects.all()
    billboards = Billboard.objects.all()
    if request.method=="POST":
        file = request.FILES['myfile']
        file_upload_name = str(uuid.uuid4()) + file.name
        blob_service_client = BlockBlobService(account_name = 'advertisementfyp', account_key='eA5hDrk+XmnDPYJirFVPIMdaqT9dNaBTxNq4u6SaBaMVTo24Nd0tXauLkknF8l3QVrj41Mds3k6H+ASt2SYBew==')
        blob_service_client.create_blob_from_bytes( container_name = 'videos', blob_name = file, blob = file.read())
        Slot.objects.create(company=User.objects.get(pk=request.user.pk), slot_date=date.today(), slot_timing=SlotTimings.objects.get(slot_timing_id=request.POST['slots']), 
        billboard=Billboard.objects.get(billboard_id=request.POST['billboards']),
        video_url = "https://advertisementfyp.blob.core.windows.net/videos/"+file.name)
        #return JsonResponse( { "status": "success", "uploaded_file_name": file_upload_name}, status=201)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "dashboard.html", {'slots': slots, 'billboards': billboards})

def registration_view(request):
    context = {}
    form = RegistrationForm(request.POST or None)
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return render(request, 'login.html')
        else:
            return render(request, 'register.html')
    context['registration_form'] = form
    return render(request, 'register.html', context)