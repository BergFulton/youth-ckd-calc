from django.urls import path
from calculator import views

urlpatterns = [
	path('', views.home, name='home'),
	path('wizard/', views.input_form_wizard_view, name="wizard"),
	path('result/', views.display_result, name='result'),
	path('reference/', views.reference, name='reference'),
	path('faq/', views.faq, name='faq'),
]