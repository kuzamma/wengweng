import json

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *


def staff_home(request):
    staff = get_object_or_404(Staff, admin=request.user)
    total_leave = LeaveReportStaff.objects.filter(staff=staff).count()
    total_Competency = CompetencyJournal.objects.filter(staff=staff).count()

    context = {
        'page_title': 'My dashboard' ,
        'total_leave': total_leave,
        'total_Competency':total_Competency,
    }
    return render(request, 'staff_template/home_content.html', context)


def staff_apply_leave(request):
    form = LeaveReportStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(staff=staff),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('staff_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_apply_leave.html", context)



def competency_journal(request):
    form = CompetencyJournalStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'competencyjournal': CompetencyJournal.objects.filter(staff=staff),
        'page_title': 'Journal Competency'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(
                    request, "Add Successdully")
                return redirect(reverse('competency_journal'))
            except Exception:
                messages.error(request, "Could not add!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/add_competency.html", context)

def edit_competency(request):
    competency = CompetencyJournal.objects.get()

    context = {
        'competency': competency,
    }
    return render(request, 'edit_competency.html', context)


def delete_competency(request):
    competency = CompetencyJournal.objects.get()
    competency.delete()
    messages.info(request, 'Deleted Successfully!')

    return redirect(competency_journal)


def staff_feedback(request):
    form = FeedbackStaffForm(request.POST or None)
    staff = get_object_or_404(Staff, admin_id=request.user.id)
    context = {
        'form': form,
        'feedbacks': FeedbackStaff.objects.filter(staff=staff),
        'page_title': 'Add Feedback'
    }

    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.staff = staff
                obj.save()
                messages.success(request, "Feedback submitted for review")
                return redirect(reverse('staff_feedback'))
            except Exception:
                messages.error(request, "Could not Submit!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, "staff_template/staff_feedback.html", context)




def staff_view_profile(request):
    staff = get_object_or_404(Staff, admin=request.user)
    form = StaffEditForm(request.POST or None, request.FILES or None,instance=staff)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = staff.admin

                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                staff.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('staff_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/staff_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "staff_template/staff_view_profile.html", context)

    return render(request, "staff_template/staff_view_profile.html", context)

@csrf_exempt
def staff_fcmtoken(request):
    token = request.POST.get('token')
    try:
        staff_user = get_object_or_404(CustomUser, id=request.user.id)
        staff_user.fcm_token = token
        staff_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


def add_formal(request):
            staff = get_object_or_404(Staff, admin_id=request.user.id)
            form = StaffAddFormalForm(request.POST or None, request.FILES or None,instance=staff)

            context = {'form': form, 'page_title': 'Add Formal'}

            if request.method == 'POST':
                if form.is_valid():
                    title = form.cleaned_data.get('title')
                    address = form.cleaned_data.get('address')
                    conducted = form.cleaned_data.get('conducted')
                    date_ended = form.cleaned_data.get('date_ended')
                    time_duration = form.cleaned_data.get('time_duration')
                    date_started = form.cleaned_data.get('date_started')
                    try:
                        formal = Formal()
                        formal.title = title
                        formal.address = address
                        formal.conducted = conducted
                        formal.date_ended = date_ended
                        formal.time_duration = time_duration
                        formal.date_started = date_started

                        formal.save()
                        messages.success(request, "Successfully Added")
                        return redirect(reverse('add_formal'))

                    except Exception as e:
                        messages.error(request, "Could Not Add " + str(e))
                else:
                     messages.error(request, "Fill Form Properly")
            return render(request, 'staff_template/add_formal.html', context)


def manage_formal(request):
    formals = Formal.objects.all()
    context = {
        'formals': formals,
        'page_title': 'Manage Formal'
    }
    return render(request, "staff_template/manage_formal.html", context)

def staff_profile(request):

    return render(request, 'staff_template/profile.html')



