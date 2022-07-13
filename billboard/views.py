from datetime import date
import uuid
from numpy import true_divide
import razorpay
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout

from billboard.models import Billboard, Slot, SlotTimings
from django.contrib.auth.models import User
from .forms import RegistrationForm, AccountAuthenticationForm
from azure.storage.blob import BlockBlobService

# Create your views here.
client = razorpay.Client(auth=("rzp_test_TLUvg2DT1iU8Tr", "LUJK44G90eKAgsH3sKV3Z037"))
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
                return redirect("dashboard", status = 0)
    context['login_form'] = form
    print(form.errors)
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard(request, status):
    amount_paid = False
    if(status==1):
        amount_paid = True
    slots = SlotTimings.objects.all()
    billboards = Billboard.objects.all()
    if request.method=="POST":
        file = request.FILES['myfile']
        blob_service_client = BlockBlobService(account_name = 'advertisementfyp', account_key='eA5hDrk+XmnDPYJirFVPIMdaqT9dNaBTxNq4u6SaBaMVTo24Nd0tXauLkknF8l3QVrj41Mds3k6H+ASt2SYBew==')
        blob_service_client.create_blob_from_bytes( container_name = 'videos', blob_name = file, blob = file.read())
        Slot.objects.create(company=User.objects.get(pk=request.user.pk), slot_date=date.today(), slot_timing=SlotTimings.objects.get(slot_timing_id=request.POST['slots']), 
        billboard=Billboard.objects.get(billboard_id=request.POST['billboards']),
        video_url = "https://advertisementfyp.blob.core.windows.net/videos/"+file.name)
        #return JsonResponse( { "status": "success", "uploaded_file_name": file_upload_name}, status=201)
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, "dashboard.html", {'slots': slots, 'billboards': billboards, 'amount_paid': amount_paid})

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

def razorpay(request):
    context = {}
    DATA = {
    "amount": 100,
    "currency": "INR",
    "receipt": "receipt#1",
    "notes": {
        "key1": "value3",
        "key2": "value2"
    }
    }
    print(client.order.create(data=DATA))
    context['details'] = client.order.create(data=DATA)
    return render(request, 'payment.html', context)
