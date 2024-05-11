from django import forms
from django.http import HttpResponse
from django.db.models import Q 
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Student_detail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AddressDetailForm, BranchDetailForm, DocumentDetailForm, GraduationDetailForm, StudentDetailForm, ContactDetailForm, QualificationDetailForm

# Alert: For testing purposes only.
from django.views.decorators.csrf import csrf_exempt

from ams_main import settings
from .tokens import generate_token
from django.conf import settings
import os
from django.db.models import Q




############# HOME VIEW   ########################

def home(request):
    return render(request, "authentication/index.html")


############# ABOUT VIEW   ########################
def about(request):
    return HttpResponse("About Page is under construction")


############# USER DASHBOARD VIEW   ########################
@login_required(login_url='/signin')
def dashboard(request):
    user_id = request.session.get('user_id')
    user_data = Student_detail.objects.filter(user_id=user_id).first()
    fname = request.session.get('fname', user_data.first_name if user_data else '')
    lname = request.session.get('lname', user_data.last_name if user_data else '')
    context = {
        'fname': fname,
        'lname': lname,
        'student_detail': user_data,
        'personal_details_completed': user_data.personal_details_completed if user_data else False,
        'contact_details_completed': user_data.contact_details_completed if user_data else False,
        'address_details_completed': user_data.address_details_completed if user_data else False,
        'qualification_details_completed': user_data.qualification_details_completed if user_data else False,
        'graduation_details_completed': user_data.graduation_details_completed if user_data else False,
        'document_details_completed': user_data.document_details_completed if user_data else False,
    }
    return render(request, "user_pages/dashboard.html", context)


############# ADMIN DASHBOARD VIEW   ########################
@login_required(login_url='/signin')
def a_dashboard(request):
    data=Student_detail.objects.filter(is_submitted=True)
    return render(request, "admin_pages/admin_dashboard.html", {'data':data})


############ DETAIL VIEW ###############
@login_required(login_url='/signin')
def detail_view(request, user_id):
    student_detail = get_object_or_404(Student_detail, user_id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        remark = request.POST.get('remark', '')

        if action == 'reject':
            student_detail.is_submitted = False
            print(student_detail.is_submitted)
            student_detail.save()
            
        if action in ['accept', 'reject']:
            student_detail.is_accepted = action
            student_detail.remark = remark
            
            student_detail.save()


            request.session['is_accepted'] = action
            request.session['remark'] = remark

    return render(request, 'admin_pages/detail_view.html', {'user_data': student_detail})


############# USER APPLICATION VIEW   ########################
@login_required(login_url='/signin')
def application(request):  
    user_id = request.session.get('user_id')
    all_user_data = Student_detail.objects.filter(user_id=user_id)
    
    if Student_detail.objects.filter(user_id=user_id, app_is_clicked=True).exists():
        return redirect("program_choices")
    
    if request.method == "POST":
        Student_detail.objects.filter(user_id=user_id).update(app_is_clicked=True)
        return redirect("program_choices")

    return render(request, "user_pages/application.html", {'all_user_data': all_user_data})




############# SIGNUP VIEW   ########################

@csrf_exempt
def signup(request):
    if request.method != "POST":
        return render(request, "authentication/signup.html")

    email = request.POST.get('email')
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    pass1 = request.POST.get('password')
    pass2 = request.POST.get('confirm_password')

    if User.objects.filter(username=email):
        messages.error(request, "Email already exist! Login instead.")
        return redirect('signin')


    applicant = User.objects.create_user(username=email, password=pass1)
    applicant.email = email
    applicant.first_name = fname
    applicant.last_name = lname
    applicant.is_active = False
    applicant.save()

    messages.success(request, "Your Account has been successfully created!")

    current_site = get_current_site(request)
    email_subject = f"Welcome to {settings.INSTITUTE}!"
    message1 = render_to_string('email_confirmation.html', {
        'name': applicant.first_name,
        'institute': settings.INSTITUTE,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(applicant.pk)),
        'token': generate_token.make_token(applicant),
    })

    email = EmailMessage (
        email_subject, 
        message1,
        settings.EMAIL_HOST_USER,
        [applicant.username],
    )
    email.fail_silently = True
    email.send()

    return redirect('signin')


############# SIGNIN VIEW   ########################

@csrf_exempt
def signin(request):
    if request.method != "POST":
        return render(request, "authentication/signin.html")

    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(username=email, password=password)
    if user is not None:

        request.session.clear()

        login(request, user)
        if user.is_staff:
            return redirect('a_dashboard')
        request.session['fname'] = user.first_name
        request.session['lname'] = user.last_name
        request.session['user_email'] = email
        request.session['user_id'] = user.id
        fname = user.first_name
        return redirect('dashboard')
        
    else:
        messages.error(request, "Bad credentials!")
    return redirect('signin')

############# SIGNOUT VIEW   ########################

def signout(request):
    logout(request)
    messages.success(request, "Logged out!")
    return redirect('signin')

############# ACTIVATE VIEW   ########################

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        applicant = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        applicant = None

    if applicant is not None and generate_token.check_token(applicant, token):
        applicant.is_active = True
        applicant.save()
        return redirect('signin')
    return render(request, 'activation_failed.html')


############# USER PROFILE VIEW   ########################

@login_required(login_url='/signin')
def user_profile(request):
    user_id = request.session.get('user_id')
    all_user_data = Student_detail.objects.filter(user_id=user_id)
    return render(request, "user_pages/user_profile.html", {'all_user_data': all_user_data})


############### PROGRAM CHOICES VIEW #########################

@login_required(login_url='/signin')
def program_choices(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)

    branch_details_data = request.session.get('program_choices', {})
    form = BranchDetailForm(request.POST or None, instance=student_detail, initial=branch_details_data)
    if student_detail.is_submitted:
        for field_name, field in form.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True

    if request.method == 'POST':
        form = BranchDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            branch_details_data = form.cleaned_data
            request.session['program_choices'] = branch_details_data
            request.session['user_id'] = user.id
            form.save()
            return redirect('personal_details')
            
    return render(request, 'user_pages/application_pages/program_choices.html', {'form': form, 'is_submitted': student_detail.is_submitted})


############# PERSONAL DETAILS VIEW   ########################


@login_required(login_url='/signin')
def personal_details(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)

    personal_details_data = request.session.get('personal_details', {})
    form = StudentDetailForm(request.POST or None, instance=student_detail, initial=personal_details_data)
    if student_detail.is_submitted:
        for field_name, field in form.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True
    
    if request.method == 'POST':
        form = StudentDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            personal_details_data = form.cleaned_data
            personal_details_data['date_of_birth'] = str(personal_details_data['date_of_birth'])
            request.session['personal_details'] = personal_details_data
            request.session['user_id'] = user.id
            student_detail.personal_details_completed = True
            form.save()
            return redirect('contact_details')
   
    return render(request, 'user_pages/application_pages/personal details.html', {'form': form, 'is_submitted': student_detail.is_submitted})


############# CONTACT DETAILS VIEW   ########################

@login_required(login_url='/signin')
def contact_details(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)
    contact_details_data = request.session.get('contact_details', {})
    form = ContactDetailForm(request.POST or None, instance=student_detail, initial=contact_details_data)
    if student_detail.is_submitted:
        for field_name, field in form.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True

    if request.method == 'POST':
        form = ContactDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            contact_details_data = form.cleaned_data
            request.session['contact_details'] = contact_details_data
            student_detail.contact_details_completed = True
            form.save()
            return redirect('address') 

    return render(request, 'user_pages/application_pages/contact details.html', {'form': form, 'is_submitted': student_detail.is_submitted})



############# ADDRESS VIEW   ########################3


@login_required(login_url='/signin')
def address(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)
    address_details_data = request.session.get('address', {})
    form = AddressDetailForm(request.POST or None, instance=student_detail, initial=address_details_data)
    if student_detail.is_submitted:
        for field_name, field in form.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True
    
    if request.method == 'POST':
        form = AddressDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            address_details_data = form.cleaned_data
            request.session['address'] = address_details_data
            student_detail.address_details_completed = True
            form.save()
            return redirect('qualification')

    return render(request, 'user_pages/application_pages/address.html', {'form': form, 'is_submitted': student_detail.is_submitted})



############# QUALIFICATION VIEW   ########################

@login_required(login_url='/signin')
def qualification(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)
    qualification_data = request.session.get('qualification', {})
    form = QualificationDetailForm(request.POST or None, instance=student_detail, initial=qualification_data)
    if student_detail.is_submitted:
        for field in form.fields.values():
            field.widget.attrs['readonly'] = True

    if request.method == 'POST':
        form = QualificationDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            qualification_data = form.cleaned_data
            request.session['qualification'] = qualification_data
            student_detail.qualification_details_completed = True
            form.save()
            return redirect('graduation')

    return render(request,"user_pages/application_pages/qualification.html",{'form':form, 'is_submitted': student_detail.is_submitted})
    

############# GRADUATION VIEW   ########################

@login_required(login_url='/signin')
def graduation(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)
    graduation_data = request.session.get('graduation', {})
    form = GraduationDetailForm(request.POST or None, instance=student_detail, initial=graduation_data)
    if student_detail.is_submitted:
        for field_name, field in form.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['disabled'] = True
            else:
                field.widget.attrs['readonly'] = True

    if request.method == 'POST':
        form = GraduationDetailForm(request.POST, instance=student_detail)
        if form.is_valid():
            graduation_data = form.cleaned_data
            request.session['graduation'] = graduation_data
            student_detail.graduation_details_completed = True
            form.save()
            return redirect('document')

    return render(request, "user_pages/application_pages/graduation.html", {'form': form, 'is_submitted': student_detail.is_submitted})


############# DOCUMENT VIEW   ########################

@login_required(login_url='/signin')
def document(request):
    user = request.user
    user_id = request.session.get('user_id', user.id)
    student_detail, created = Student_detail.objects.get_or_create(user_id=user_id)
    document_data = request.session.get('document', {})

    form = DocumentDetailForm(request.POST or None, request.FILES or None, instance=student_detail, initial=document_data)
    if student_detail.is_submitted:
        for field in form.fields.values():
            field.widget.attrs['readonly'] = True

    if request.method == 'POST':
        form = DocumentDetailForm(request.POST, request.FILES or None, instance=student_detail)
        if form.is_valid():
            if 'file_tenth' in request.FILES:
                save_file(request.FILES['file_tenth'], settings.MEDIA_ROOT)
            if 'file_twelfth' in request.FILES:
                save_file(request.FILES['file_twelfth'], settings.MEDIA_ROOT)
            if 'leaving_certificate' in request.FILES:
                save_file(request.FILES['leaving_certificate'], settings.MEDIA_ROOT)
            if 'graduation_marksheet' in request.FILES:
                save_file(request.FILES['graduation_marksheet'], settings.MEDIA_ROOT)
            if 'mah_cet_scorecard' in request.FILES:
                save_file(request.FILES['mah_cet_scorecard'], settings.MEDIA_ROOT)

            student_detail.document_details_completed = True
            form.save()

            return redirect('preview')

    return render(request, "user_pages/application_pages/document.html", {'form': form, 'is_submitted': student_detail.is_submitted})


############# LOGIC FOR SAVING FILES ########################
def save_file(file, destination):
    file_path = os.path.join(destination, file.name)
    return file_path


############# PREVIEW VIEW   ########################
@login_required(login_url='/signin')
def preview(request):
    user_id = request.session.get('user_id')
    student_detail = Student_detail.objects.filter(user_id=user_id).first()

    if request.method == 'POST':
        student_detail.is_submitted = True
        student_detail.is_accepted = False
        student_detail.remark = ""
        student_detail.save()

    # Extracting only filenames from the full paths
    file_tenth = os.path.basename(student_detail.file_tenth.path) if student_detail.file_tenth else None
    file_twelfth = os.path.basename(student_detail.file_twelfth.path) if student_detail.file_twelfth else None
    leaving_certificate = os.path.basename(student_detail.leaving_certificate.path) if student_detail.leaving_certificate else None
    graduation_marksheet = os.path.basename(student_detail.graduation_marksheet.path) if student_detail.graduation_marksheet else None
    mca_cet_scorecard = os.path.basename(student_detail.mah_cet_scorecard.path) if student_detail.mah_cet_scorecard else None

    return render(request, "user_pages/application_pages/review.html", {
        'all_user_data': student_detail,
        'is_submitted': student_detail.is_submitted,
        'file_tenth': file_tenth,
        'file_twelfth': file_twelfth,
        'leaving_certificate': leaving_certificate,
        'graduation_marksheet': graduation_marksheet,
        'mca_cet_scorecard': mca_cet_scorecard,
    })


###################### MERIT LIST VIEW ####################3
@login_required(login_url='/signin')
def merit_list(request):
    try:
        user_id = request.session.get('user_id')
        all_user_data = Student_detail.objects.filter(user_id=user_id)
        all_students_seat_is_accepted = Student_detail.objects.filter(seat_is_accepted=True)
        if all_user_data.exists():
            user_data = all_user_data.first()
            if user_data.publish_selected_branch == user_data.branch:
                if all_user_data.first().admin_selected_round == '1':
                    context = generate_merit_list(user_data.publish_selected_branch)
                else:
                    context = generate_merit_list2(user_data.publish_selected_branch)
                is_on_merit_list = check_if_user_on_merit_list(user_data) 
                seat_is_accepted = all_user_data.first().seat_is_accepted
                return render(request, 'user_pages/merit_list.html', {'context': context, 'is_on_merit_list': is_on_merit_list, 'seat_is_accepted': seat_is_accepted, 'user_id': user_id, 'all_students_seat_is_accepted': all_students_seat_is_accepted, 'all_user_data': all_user_data}) 
            else:
                return HttpResponse("Merit List has not yet declared")
        else:
            return HttpResponse("Fill the form first!")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Fill the form first!")



def check_if_user_on_merit_list(user_data):
    branch = user_data.publish_selected_branch
    user_name = f"{user_data.first_name} {user_data.last_name}"
    if user_data.admin_selected_round == '1':
        merit_list_students = generate_merit_list(branch)
    else:
        merit_list_students = generate_merit_list2(branch)

    for student in merit_list_students:
        if f"{student.first_name} {student.last_name}" == user_name:
            return True

    return False


####################### APPROVAL PENDING VIEW ######################
@login_required(login_url='/signin')
def approval(request):
    try:
        user_id = request.session.get('user_id')
        all_user_data = Student_detail.objects.filter(user_id=user_id)
        
        if all_user_data.exists() and all_user_data.first().personal_details_completed \
            and all_user_data.first().contact_details_completed \
            and all_user_data.first().address_details_completed \
            and all_user_data.first().qualification_details_completed \
            and all_user_data.first().graduation_details_completed \
            and all_user_data.first().document_details_completed:
            return render(request, 'user_pages/approval.html', {'all_user_data': all_user_data})
        else:
            return HttpResponse("Fill the form first")
    except (AttributeError, TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("An error occurred while processing your request")



###################### LOGIC OF GENERATING MERIT LIST ##################3

def generate_merit_list(branch):
    student_details = Student_detail.objects.filter(is_accepted='accept')

    def sorting_key(student_details):
        try:
            mahcet_score = float(student_details.mahcet_score)
            hsc_percent = float(student_details.hsc_percent)
        except (ValueError, TypeError):
            mahcet_score = 0
            hsc_percent = 0

        return (-mahcet_score, -hsc_percent)
    
    sorted_students = sorted(student_details, key=sorting_key)   

    if branch == 'all':
        return sorted_students

    filtered_students = [student for student in sorted_students if student.branch == branch]
    
    declined_students = Student_detail.objects.filter(is_declined=True, branch=branch)
    total_declined = declined_students.count()
    
    intake_capacity = int(branch.split('_')[-1])
    filtered_students = []

    for student in sorted_students:
        if student.branch == branch and not student.is_declined:
            filtered_students.append(student)
    
    top_students = filtered_students[:intake_capacity - total_declined]

    return top_students


def generate_merit_list2(branch):
    student_details = Student_detail.objects.filter(is_accepted='accept')
    accpeted_students = Student_detail.objects.filter(seat_is_accepted=True, branch=branch)
    total_accepted = accpeted_students.count()
    
    def sorting_key(student_details):
        try:
            mahcet_score = float(student_details.mahcet_score)
            hsc_percent = float(student_details.hsc_percent)
        except (ValueError, TypeError):
            mahcet_score = 0
            hsc_percent = 0

        return (-mahcet_score, -hsc_percent)
    sorted_students = sorted(student_details, key=sorting_key)   

    if branch == 'all':
        return sorted_students

    intake_capacity = int(branch.split('_')[-1])
    remaining_seats = intake_capacity - total_accepted
    
    filtered_students = [student for student in sorted_students if student.branch == branch]
    
    filtered_students = [student for student in filtered_students if not student.is_declined and student.seat_is_accepted==False]
    
    top_students = filtered_students[:remaining_seats]

    return top_students


#################### ADMIN MERIT LIST WHERE ADMIN CAN WE THE LIST OF ELIGIBLE STUDENTS ############
@login_required(login_url='/signin')
def admin_merit_list(request):
    selected_branch = 'all' 

    if request.method == 'POST':
        selected_branch = request.POST.get('branch', 'all')
        round_num = request.POST.get('round', '1')  # Get the round value from the form
        Student_detail.objects.filter(branch=selected_branch).update(publish_selected_branch=selected_branch, admin_selected_round=round_num)
    else:
        round_num = request.POST.get('round', '1')

    if round_num == '1': 
        top_students = generate_merit_list(branch=selected_branch)
    else:
        top_students = generate_merit_list2(branch=selected_branch)
        
    return render(request, 'admin_pages/admin_merit_list.html', {
        'student_details': top_students,
        'selected_branch': selected_branch,
        'round_num': round_num 
    })



########## ACCEPT OR DECLINE SEAT ###################
@csrf_exempt
@login_required(login_url='/signin')
def accept_decline_seat(request):
    user_id = request.session.get('user_id')
    student_detail = get_object_or_404(Student_detail, user_id=user_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'accept':
            student_detail.seat_is_accepted = True
            student_detail.save()
            return HttpResponse('Seat Accepted. Redirecting to payment website')
        else:
            student_detail.is_declined = True
            student_detail.save()
            return HttpResponse('Seat Declined.')
    
    
    return render(request, 'user_pages/merit_list.html')



############# SEARCHING THE USER IN THE ADMIN PAGE ####################

@login_required(login_url='/signin')
def search_user(request):
    all_user_data = search(request)
    return render(request, 'admin_pages/search_user.html', {'data': all_user_data})

############# SEARCHING THE USER IN THE MERIT LIST PAGE ####################
@login_required(login_url='/signin')
def search_student(request):
    user_id = request.session.get('user_id')
    student_detail = Student_detail.objects.filter(user_id=user_id).first()
    top_students = generate_merit_list(student_detail.branch)
    top_student_names = {student.first_name for student in top_students}
    searched_user = search(request)
    
    if searched_user.first().first_name not in top_student_names:
        return HttpResponse("User not found in merit list")
    
    context = {'context': searched_user}
    return render(request, 'user_pages/search_student.html', context)

################## SEARCH FUNCTION ######################
@login_required(login_url='/signin')
def search(request):
    query = request.GET.get('query')
    filter_condition = Q(first_name__icontains=query) | Q(last_name__icontains=query)
    
    if query.isdigit():
        filter_condition = Q(user=query)
    
    searched_user = Student_detail.objects.filter(filter_condition)
    
    return searched_user


############ COURSE DATA VIEW ######################
@login_required(login_url='/signin')
def course_data(request):
    selected_branch = 'all' 
    if request.method == 'POST':
        selected_branch = request.POST.get('branch', 'all')
            
    if selected_branch == 'all':
        filtered_students = Student_detail.objects.filter(is_declined=False)
    else:
        filtered_students = Student_detail.objects.filter(is_declined=False, branch=selected_branch)
        
    return render(request, 'admin_pages/course_data.html', {
        'data': filtered_students,
        'selected_branch': selected_branch
    })
