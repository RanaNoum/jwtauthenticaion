from django import forms
from tinymce.widgets import TinyMCE
from .models import BlogPost,Case
# from .models import PricingEstimate

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = BlogPost
        fields = ['title', 'description','content', 'category', 'published_date', 'author', 'image']
        # Make sure to include all other fields you want to be part of the form

class CaseForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Case
        fields = '__all__'
        
        # Make sure to include all other fields you want to be part of the form


from .models import PrivacyPolicy, TermsAndConditions

class PrivacyPolicyForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = PrivacyPolicy
        fields = '__all__'
        

class TermsAndConditionsForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = TermsAndConditions
        fields = '__all__'
        




# class PricingEstimateForm(forms.ModelForm):
#     class Meta:
#         model = PricingEstimate
#         fields = ['service_type', 'feature_set', 'complexity', 'estimated_hours', 'hourly_rate', 'additional_costs', 'discounts', 'contact_information', 'file']




# class PricingEstimateForm(forms.ModelForm):
#     class Meta:
#         model = PricingEstimate
#         fields = '__all__'