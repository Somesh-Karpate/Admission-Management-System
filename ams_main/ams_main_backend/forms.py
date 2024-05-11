# forms.py

from django import forms
from .models import Student_detail


class StudentDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields = ['first_name', 'last_name', 'gender', 'date_of_birth','nationality', 'annual_income']
        widgets={
            'date_of_birth':forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'gender':forms.Select(attrs={'class': 'form-control'}),
            }


class ContactDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields = ['contact_number', 'alternate_contact_number', 'email', 'guardian_name', 'guardian_contact']


class AddressDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields = ['address_line1', 'address_line2', 'landmark', 'town_city', 'pincode', 'district', 'state', 'permanent_address']

class QualificationDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields=['ssc_marks','ssc_outof','ssc_percent','hsc_marks','hsc_outof','hsc_percent','maths_marks','maths_outof','maths_percent','science_marks','science_outof','science_percent','english_marks','english_outof','english_percent', 'mahcet_score']

class DocumentDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields = ['file_tenth', 'file_twelfth', 'leaving_certificate', 'graduation_marksheet', 'mah_cet_scorecard']
class GraduationDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields=['bachelor','uni','place','gtype','p_year','gstatus','g_marks','cgpa_marks','cgpa_outof','cgpa_percent',]
        widgets={
            'bachelor':forms.Select(attrs={'class': 'form-control'}),}

class BranchDetailForm(forms.ModelForm):
    class Meta:
        model = Student_detail
        fields = ['branch']

        
        

