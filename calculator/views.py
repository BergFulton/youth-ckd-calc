from django.shortcuts import render, get_object_or_404, HttpResponseRedirect

# Create your views here.
from calculator.models import InputModel
from calculator.forms import InputBasicInfoForm, InputClinicInfoCurrentForm, InputClinicInfoPastForm
from django.urls import reverse
from formtools.wizard.views import SessionWizardView
from crispy_forms.helper import FormHelper
from django.utils.safestring import mark_safe
import math




#########################################
# Helper functions                      #
#########################################
def intuitive_year_month(time):
    if time >= 10:
        time_display = "greater than 10 years"
    elif time >= 5:
        time_display = "%d years" % round(time)
    else:
        time_year = math.floor(time)
        time_month = round((time - time_year)*12)
        if time_year == 1:
            display_year = "1 year"
        elif time_year == 0:
            display_year = ""
        else:
            display_year = "%d years" % time_year
        if time_month == 1:
            display_month = "%d month" % time_month
        else:
            display_month = "%d months" % time_month
        time_display = "%s %s" % (display_year, display_month)
    return time_display.strip()
#########################################
# Main pages                            #
#########################################


def home(request):
    return render(request, 'home.html')
def reference(request):
    return render(request, 'reference.html')
def faq(request):
    return render(request, 'faq.html')


FORMS = [
    ("form1", InputBasicInfoForm),
    ("form2", InputClinicInfoCurrentForm),
    ("form3", InputClinicInfoPastForm),
]
TEMPLATES = {
    "form1": "formtools/wizard/form.html",
    "form2": "formtools/wizard/form.html",
    "form3": "formtools/wizard/form.html",
}

def display_result(request):
    data = request.session.get('data')
    age = data['age']
    male_y1n0 = data['male_y1n0']
    gfr_l1m2h3 = data['gfr_l1m2h3']
    gfr_l = int((gfr_l1m2h3 == 1)) # GFR < 30
    gfr_m = int((gfr_l1m2h3 == 2)) # GFR between 30 and 45
    gfr_l45 = int((gfr_l1m2h3 == 1) | (gfr_l1m2h3 == 2)) # gfr < 45 (including gfr_l & gfr_m)
    hypoalb_y1n0 = data['hypoalb_y1n0'] # hypoalbuminemia
    htn_y1n0 = data['htn_y1n0'] # hypertension
    hightrig_y1n0 = data.get('hightrig_y1n0', 0) # high triglycerides
    lowhdl_y1n0 = data.get('lowhdl_y1n0', 0) # low HDL
    highnonhdl_y1n0 = data.get('highnonhdl_y1n0', 0) # High non-HDL
    # Define dyslipidemia
    if (hightrig_y1n0 == 0) & (lowhdl_y1n0 == 0) & (highnonhdl_y1n0 == 0):
        dyslip_y1n0 = 0
    else:
        dyslip_y1n0 = 1

    # Define change of proteinuria
    proteinuria_cur_y1n0 = data['proteinuria_cur_y1n0']
    proteinuria_past_y1n0 = data['proteinuria_past_y1n0']
    onset_proteinuria = 0
    persistent_proteinuria = 0
    resolved_proteinuria = 0
    if (proteinuria_past_y1n0 == 0) & (proteinuria_cur_y1n0 == 1):
        onset_proteinuria = 1
    if (proteinuria_past_y1n0 == 1) & (proteinuria_cur_y1n0 == 1):
        persistent_proteinuria = 1
    if (proteinuria_past_y1n0 == 1) & (proteinuria_cur_y1n0 == 0):
        resolved_proteinuria = 1

    # Define change of anemia
    anemia_past_y1n0 = data['anemia_past_y1n0']
    anemia_cur_y1n0 = data['anemia_cur_y1n0']
    onset_anemia = 0
    persistent_anemia = 0
    resolved_anemia = 0
    if (anemia_past_y1n0 == 0) & (anemia_cur_y1n0 == 1):
        onset_anemia = 1
    if (anemia_past_y1n0 == 1) & (anemia_cur_y1n0 == 1):
        persistent_anemia = 1
    if (anemia_past_y1n0 == 1) & (anemia_cur_y1n0 == 0):
        resolved_anemia = 1

    # Define change of ACEi/ARB medication
    aceiarb_past_y1n0 = data.get('aceiarb_past_y1n0',0)
    aceiarb_cur_y1n0 = data.get('aceiarb_cur_y1n0',0)
    onset_aceiarb = 0
    persistent_aceiarb = 0
    resolved_aceiarb = 0
    if (aceiarb_past_y1n0 == 0) & (aceiarb_cur_y1n0 == 1):
        onset_aceiarb = 1
    if (aceiarb_past_y1n0 == 1) & (aceiarb_cur_y1n0 == 1):
        persistent_aceiarb = 1
    if (aceiarb_past_y1n0 == 1) & (aceiarb_cur_y1n0 == 0):
        resolved_aceiarb = 1

    # Calculate the log(time) using the formula
    ckddiag_g1ng0 = data['ckddiag_g1ng0']
    if (ckddiag_g1ng0 == 0):
        m = 3.58-(0.03*age)-0.2*male_y1n0-0.27*gfr_m-0.83*gfr_l-0.67*hypoalb_y1n0-0.32*htn_y1n0-0.15*dyslip_y1n0-0.77*resolved_proteinuria-1.07*onset_proteinuria-1.19*persistent_proteinuria-0.3*resolved_anemia-0.40*onset_anemia-0.56*persistent_anemia-0.05*resolved_aceiarb-0.51*onset_aceiarb-0.31*persistent_aceiarb
        if gfr_l1m2h3 == 1:
            sd = 1.21
        elif gfr_l1m2h3 == 2:
            sd = 0.98
        else:
            sd = 0.81
    if (ckddiag_g1ng0 == 1):
        m = 3.97-2.01*gfr_l45-0.38*hypoalb_y1n0-0.60*htn_y1n0-2.37*resolved_proteinuria-1.17*onset_proteinuria-1.35*persistent_proteinuria-0.18*resolved_anemia-0.37*onset_anemia-1.16*persistent_anemia
        sd = 1.62
    estimate50 = math.exp(m)
    estimate25 = math.exp(m - sd*0.67449)
    estimate10 = math.exp(m - sd*1.28155)


    # Prepare the report, transform the raw data to readable descriptions
    male_y1n0_t     = "Male"       if male_y1n0     == 1 else "Female"
    ckddiag_g1ng0_t = "Glomerular" if ckddiag_g1ng0 == 1 else "Non-glomerular"
    htn_y1n0_t      = "Yes"        if htn_y1n0      == 1 else "No"
    hypoalb_y1n0_t  = "Yes"        if hypoalb_y1n0  == 1 else "No"
    dyslip_y1n0_t   = "Yes"        if dyslip_y1n0   == 1 else "No"

    if onset_proteinuria == 1:
        proteinuria_t = "Onset of nephrotic proteinuria"
    elif persistent_proteinuria == 1:
        proteinuria_t = "Persistent nephrotic proteinuria"
    elif resolved_proteinuria == 1:
        proteinuria_t = "Resolved nephrotic proteinuria"
    else:
        proteinuria_t = "No nephrotic proteinuria"

    if onset_anemia == 1:
        anemia_t = "Onset of anemia"
    elif persistent_anemia == 1:
        anemia_t = "Persistent anemia"
    elif resolved_anemia == 1:
        anemia_t = "Resolved anemia"
    else:
        anemia_t = "No anemia"

    if onset_aceiarb == 1:
        aceiarb_t = "Initiation of ACEi/ARB therapy"
    elif persistent_aceiarb == 1:
        aceiarb_t = "Persistent use of ACEi/ARB therapy"
    elif resolved_aceiarb == 1:
        aceiarb_t = "Discontinued ACEi/ARB therapy"
    else:
        aceiarb_t = "Never ACEi/ARB therapy"

    if gfr_l1m2h3 == 1:
        gfr_l1m2h3_t = mark_safe("< 30 ml/min|1.73m<sup>2</sup>")
    elif gfr_l1m2h3 == 2:
        gfr_l1m2h3_t = mark_safe("30 ~ 45 ml/min|1.73m<sup>2</sup>")
    else:
        gfr_l1m2h3_t = mark_safe("&ge; 45 ml/min|1.73m<sup>2</sup>")

    context = {
        'age':age,
        'male_y1n0_t': male_y1n0_t,
        'ckddiag_g1ng0_t': ckddiag_g1ng0_t,
        'htn_y1n0_t': htn_y1n0_t,
        'hypoalb_y1n0_t': hypoalb_y1n0_t,
        'dyslip_y1n0_t': dyslip_y1n0_t,
        'proteinuria_t': proteinuria_t,
        'anemia_t': anemia_t,
        'aceiarb_t': aceiarb_t,
        'gfr_l1m2h3_t': gfr_l1m2h3_t,
        'estimate50': intuitive_year_month(estimate50),
        'estimate25': intuitive_year_month(estimate25),
        'estimate10': intuitive_year_month(estimate10),
    }
    return render(request, 'calculator/pg4_results.html', context)  

class InputFormWizard(SessionWizardView):
    save_values_all = {}
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):
        kwargs = {}
        if step != 'form1':
            cleaned_data = self.get_cleaned_data_for_step('form1')
            kwargs.update({'is_g': cleaned_data['ckddiag_g1ng0'] == 1})
        return kwargs

    # def process_step(self, form):
    #     self.save_values_all[self.steps.current] = dict(self.get_form_step_data(form))
    #     print(list(self.save_values_all[self.steps.current].keys())[1])
    #     return self.get_form_step_data(form)

    # def get_form(self, step=None, data=None, files=None):
    #     form = super(InputFormWizard, self).get_form(step, data, files)
    #     print(self.get_form_step_data(form))
    #     return form

    # def get_next_step(self, step=None):
        # return self.request.POST.get('wizard_next_step',super().get_next_step(step))

    def post(self, *args, **kwargs):
        go_to_step = self.request.POST.get('wizard_goto_step', None)  # get the step name        
        form = self.get_form(data=self.request.POST, files=self.request.FILES)
        current_index = self.get_step_index(self.steps.current)
        goto_index = self.get_step_index(go_to_step)
        print("go_to_step is %s" % (go_to_step))
        print("Current index is %s; goto_index is %s" % (current_index, goto_index))
        if current_index > goto_index:
            if form.is_valid():
                self.storage.set_step_data(self.steps.current,self.process_step(form))
                self.storage.set_step_files(self.steps.current,self.process_step_files(form))
        return super(InputFormWizard, self).post(*args, **kwargs)

    def done(self, form_list, **kwargs):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        self.request.session['data'] = data
        return HttpResponseRedirect(reverse('result'))

input_form_wizard_view = InputFormWizard.as_view(FORMS)
