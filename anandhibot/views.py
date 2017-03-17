from django.shortcuts import render
from django.views.generic import TemplateView
from anandhibot.forms import InputForm


# Create your views here
# class HomePageView(TemplateView):
#      def get(self, request, **kwargs):
#           return render(request, 'index.html', context=None)
def input(request):
	subject = " "
	   
	if request.method == "POST":
	   #Get the posted form
	   MyInputForm = InputForm(request.POST)
	      
	   if MyInputForm.is_valid():
	       subject = MyInputForm.cleaned_data['subject']
	else:
	   MyInputForm = Inputform()
			
	return render(request, 'output.html', {"subject" : subject})
