from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, RecordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Record
import logging
from django.db.models import Q


@login_required(login_url='login')
def index(request):
    return render(request, 'Record/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  
    else:
        form = CreateUserForm()
    
    context = {
        'form':form
    }

    return render(request, 'Record/register.html', context)

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login is succssfully.')
                return redirect('dashboard')  # Redirect to a success page
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    context = {"form": form}
    return render(request, 'Record/login.html', context)


def log_out(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    records = Record.objects.all()

    context = {
        'records':records
    }
    return render(request, 'Record/dashboard.html', context)

@login_required(login_url='login')
def create_record(request):
    form = RecordForm()

    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record is created.')
            return redirect('dashboard')
    else:
        form = RecordForm()
    context = {'form':form}
    return render(request, 'Record/create_record.html', context)

@login_required(login_url='login')
def record_detail(request, record_id):
    record = get_object_or_404(Record, id=record_id)

    context = {'record':record}
    return render(request, 'Record/record_detail.html', context)

@login_required(login_url='login')
def update_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    form = RecordForm(instance=record)

    if request.method == 'POST':
        form = RecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record is updated.')
            return redirect('record_detail', record_id=record.id)

    context = {'form':form}
    return render(request, 'Record/update_record.html', context)

@login_required(login_url='login')
def delete_record(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    record.delete()
    messages.success(request, 'Record is deleted.')
    return redirect('dashboard')

logger = logging.getLogger(__name__)
@login_required(login_url='login')
def search(request):
    query = request.GET.get('query')
    results = []

    try:
        if query:
            results = Record.objects.filter(Q(first_name__icontains=query) | Q(id__icontains=query))
    except Exception as e:
        logger.error("Error during search: %s", e)

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'Record/search.html', context)
    