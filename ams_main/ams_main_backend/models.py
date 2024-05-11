# models.py

from django.db import models
from django.contrib.auth.models import User

class Student_detail(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ####################### PROGRAM CHOICES ###################################
    COURSE_CHOICES = [
        ('MCA_60', 'Master of Computer Applications - 60 seats'),
        ('MTECH_2', 'Master of Technology - 2 seats'),
        # Add more choices as needed
    ]
    branch = models.CharField(max_length=15, choices=COURSE_CHOICES)
    
    ######################## PERSONAL DETAILS MODEL ###############################
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True)
    nationality = models.CharField(max_length=100)
    annual_income = models.CharField(max_length=100, blank=True)

    
    ######################## CONTACT DETAILS MODEL ###############################
    contact_number = models.CharField(max_length=20,null=True)
    alternate_contact_number = models.CharField(max_length=20, blank=True,null=True)
    email = models.EmailField(blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_contact = models.CharField(max_length=20, blank=True, null=True)

    ######################## ADDRESS DETAILS MODEL ###############################
    address_line1 = models.CharField(max_length=30)
    address_line2 = models.CharField(max_length=30)
    landmark = models.CharField(max_length=30)
    town_city = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    district = models.CharField(max_length=20)
    state = models.CharField(max_length=30)
    permanent_address = models.BooleanField(default=False)


    ######################## QUALIFICATION DETAILS MODEL ###############################
    bachelor_choices = [
        ('Bsc IT', 'Bsc IT'),
        ('BCA', 'BCA'),
        ('OTHER', 'Other'),
    ]
    bachelor = models.CharField(max_length=10, choices=bachelor_choices, default="") 

    uni = models.CharField(max_length=30)
    placeChoice = [
        ('India', 'India'),
        ('Abroad', 'Abroad'),
    ]
    place= models.CharField(max_length=30,choices=placeChoice,default="") 
    gtypeChoice = [
        ('Full time', 'Full time'),
        ('part time', 'part time'),
    ]
    gtype=  models.CharField(max_length=30,choices=gtypeChoice,default="") 
    p_yearChoice =[
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
    ]
    p_year = models.CharField(max_length=30,choices=p_yearChoice,default="") 
    gstatusChoice = [
        ('PASSED', 'PASSED'),
        ('FAILED', 'FAILED'),
    ]
    gstatus= models.CharField(max_length=30,choices=gstatusChoice,default="") 
    gradMarks_choice = [
        ('CGPA', 'CGPA'),
        ('PERCENT', 'PERCENT'),
    ]
    g_marks= models.CharField(max_length=30,choices=gradMarks_choice,default="") 
    cgpa_marks= models.CharField(max_length=30,default="")
    cgpa_outof= models.CharField(max_length=30, blank=True,default="")
    cgpa_percent= models.CharField(max_length=30,default="")


    ######################## GRADUATION DETAILS MODEL ###############################
    ssc_marks = models.CharField(max_length=30)
    ssc_outof = models.CharField(max_length=30, blank=True)
    ssc_percent = models.CharField(max_length=30, blank=True)

    hsc_marks = models.CharField(max_length=30)
    hsc_outof = models.CharField(max_length=30, blank=True)
    hsc_percent = models.CharField(max_length=30, blank=True)

    maths_marks = models.CharField(max_length=30)
    maths_outof = models.CharField(max_length=30, blank=True)
    maths_percent = models.CharField(max_length=30, blank=True)

    science_marks = models.CharField(max_length=30)
    science_outof = models.CharField(max_length=30, blank=True)
    science_percent = models.CharField(max_length=30, blank=True)

    english_marks = models.CharField(max_length=30)
    english_outof = models.CharField(max_length=30, blank=True)
    english_percent = models.CharField(max_length=30, blank=True)
    mahcet_score = models.CharField(max_length=20, blank=True)

    
    ######################## DOCUMENT DETAILS MODEL ###############################
    file_tenth = models.FileField(upload_to='documents/tenth/', max_length=250, null=True, default=None)
    file_twelfth = models.FileField(upload_to='documents/twelfth/', max_length=250, null=True, default=None)
    leaving_certificate = models.FileField(upload_to='documents/leaving/', max_length=250, null=True, default=None)
    graduation_marksheet = models.FileField(upload_to='documents/graduation/',  max_length=250, null=True, default=None)
    mah_cet_scorecard = models.FileField(upload_to='documents/mca_cet/', max_length=250, null=True, default=None)

    
    
    
    ####################### CHECKING IF RESPECTIVE PAGE IS COMPLETED OR NOT MODEL ##########################
    personal_details_completed = models.BooleanField(default=False)
    contact_details_completed = models.BooleanField(default=False)
    address_details_completed = models.BooleanField(default=False)
    qualification_details_completed = models.BooleanField(default=False)
    graduation_details_completed = models.BooleanField(default=False)
    document_details_completed = models.BooleanField(default=False)
    is_submitted = models.BooleanField(default=False)
    
    
    #########################CHECK IF APPLICATION(TERMS AND CONDITION PAGE WAS CLICKED) #########################
    app_is_clicked = models.BooleanField(default=False)
    
    
    ######################## CHECK IF APPLICATION WAS ACCEPTED, REJECTED, REMARKED #################
    is_accepted = models.CharField(max_length=10, default='Pending')
    remark = models.CharField(max_length=100, blank=True)
    
    
    ######################## CHECK WHICH BRANCH IS SELECTED ##########################
    publish_selected_branch = models.CharField(max_length=50, default='', null=True)
    
    
    
    ######################## SEAT ACCEPTED OR REJECTED ########################
    is_declined = models.BooleanField(default=False)
    
    
    ######################## CHECK IF SEAT IS ACCEPTED OR NOT ########################
    seat_is_accepted = models.BooleanField(default=False)
    
    
    ######################## CHECK WHICH ROUND IS SELECTED BY ADMIN ########################
    admin_selected_round = models.CharField(max_length=1, default='')
    
    def __str__(self):
        return self.first_name



