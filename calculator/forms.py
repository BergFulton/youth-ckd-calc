from django import forms
from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from calculator.models import InputModel
from django.utils.safestring import mark_safe


class InputBasicInfoForm(ModelForm):
	class Meta:
		model = InputModel
		fields = ['male_y1n0','age','ckddiag_g1ng0']
		widgets = {
			'male_y1n0': forms.RadioSelect(attrs={'class': 'star'}),
			'ckddiag_g1ng0': forms.RadioSelect(attrs={'class': 'star'}),
		}
		help_texts = {
			'ckddiag_g1ng0': mark_safe("""
				<p>Examples of non-glomerular diagnosis: aplastic/hypoplastic/dysplastic kidney, obstructive uropathy, reflux nephropathy</p><p>Examples of glomerular diagnosis: focal segmental glomerulosclerosis [FSGS], systemic immunologic disease, hemolytic uremic syndrome [HUS]</p>
				click <a href="#" onClick="MyWindow=window.open('/static/calculator/images/ckd_diagnosis.png','MyWindow',width=400,height=200); return false;">here</a> for detailed descriptions.
				""")
		}
		labels  = {
			"male_y1n0": _("Enter patient's sex:"),
			"age": _("Enter patient's age (in years, between 2 and 18 years):"),
			"ckddiag_g1ng0": _("Enter CKD diagnosis:"),
		}


class InputClinicInfoCurrentForm(ModelForm):
	class Meta:
		model = InputModel
		fields = ['gfr_l1m2h3','proteinuria_cur_y1n0','htn_y1n0','hypoalb_y1n0','hightrig_y1n0','lowhdl_y1n0','highnonhdl_y1n0','anemia_cur_y1n0','aceiarb_cur_y1n0']
		labels = {
			'gfr_l1m2h3': _("What is patient's GFR?"),
			'proteinuria_cur_y1n0': _("Does patient have nephrotic range proteinuria (Urine P/Cr > 2 mg/mg)?"),
			'htn_y1n0': _("Is patient's BP classified elevated BP, Stage 1 or Stage 2 hypertension?"),
			'hypoalb_y1n0': _("Serum albumin < 3.8 g/dL?"),
			'hightrig_y1n0': _("Triglyceride level > 130 mg/dL?"),
			'lowhdl_y1n0': _("HDL cholesterol level < 40 mg/dL?"),
			'highnonhdl_y1n0': _("non-HDL cholesterol level > 160 mg/dL?"),
			'anemia_cur_y1n0': _("Is anemia present?"),
			'aceiarb_cur_y1n0': _("Currently using an ACEi/ARB medication?")
		}
		widgets = {
			'gfr_l1m2h3': forms.RadioSelect(attrs={'class': 'star'}), 
			'proteinuria_cur_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'htn_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'hypoalb_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'hightrig_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'lowhdl_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'highnonhdl_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'anemia_cur_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'aceiarb_cur_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
		}
		help_texts = {
			'htn_y1n0': mark_safe("""
				Elevated BP, Stage 1 or Stage 2 hypertension is defined as BP &ge; 90th percentile for age, sex and height (
					<a href="#" onClick="MyWindow=window.open('/static/calculator/images/ref-bpcat.png','MyWindow',width=400,height=200); return false;">Table of definitions of BP categories and Stages</a>)
					"""),
			'gfr_l1m2h3': mark_safe("""GFR calculated as 41.3 x height in meters/SCr in mg/dL"""),
			'highnonhdl_y1n0': "Non-HDL cholesterol is calculated as total cholesterol - HDL cholesterol",
			'anemia_cur_y1n0': mark_safe("""Hemoglobin < 5th percentile for age and sex (<a href="#" onClick="MyWindow=window.open('/static/calculator/images/ref-hb.png','MyWindow',width=600,height=300); return false;">Table of definitions of anemia</a>), regardless of therapy use, such as erythropoietin stimulating agents""")
		}

	def __init__(self, *args, **kwargs):
		self.is_g = kwargs.pop('is_g')
		super(InputClinicInfoCurrentForm, self).__init__(*args, **kwargs)
		if self.is_g:
			fields_to_delete = ('hightrig_y1n0', 'lowhdl_y1n0', 'highnonhdl_y1n0', 'aceiarb_cur_y1n0')
			for field in fields_to_delete:
				del self.fields[field]

class InputClinicInfoPastForm(ModelForm):
	class Meta:
		model = InputModel
		fields = ['proteinuria_past_y1n0','anemia_past_y1n0','aceiarb_past_y1n0']
		labels = {
			"proteinuria_past_y1n0":_("One year ago, did patient have nephrotic range proteinuria (Urine P/Cr > 2 mg/mg)?"),
			"anemia_past_y1n0":_("One year ago, was anemia present?"),
			"aceiarb_past_y1n0":_("One year ago, was patient using an ACEi/ARB medication?"),
		}
		widgets = {
			'proteinuria_past_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'anemia_past_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
			'aceiarb_past_y1n0': forms.RadioSelect(attrs={'class': 'star'}), 
		}

	def __init__(self, *args, **kwargs):
		self.is_g = kwargs.pop('is_g')
		super(InputClinicInfoPastForm, self).__init__(*args, **kwargs)
		if self.is_g:
			del self.fields['aceiarb_past_y1n0']