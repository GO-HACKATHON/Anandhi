from django.shortcuts import render
from django.views.generic import TemplateView
from anandhibot.forms import InputForm
import os
import indicoio
from operator import itemgetter

from indicoio.custom import Collection

indicoio.config.api_key = '897b8fc085058e1a5ee77bc7f2cc24de'


# Create your views here
# class HomePageView(TemplateView):
#      def get(self, request, **kwargs):
#           return render(request, 'index.html', context=None)
def input(request):
	subject = " "
	recom_list = []
	if request.method == "POST":
	   #Get the posted form
	   MyInputForm = InputForm(request.POST)
	      
	   if MyInputForm.is_valid():
	       allsubject = MyInputForm.cleaned_data['subject']
           subject = allsubject.split(" ")
           for sub in subject:
               recommendation = generateRecommendation(sub)
               recom_list.append(recommendation)
	else:
	   MyInputForm = Inputform()
	
	return render(request, 'input.html', {
        "subject" : subject,
        "recommendation" : recom_list,
        })


def generate_training_data(fname):
    """
    Read in text file and generate training data.
    Each line looks like the following:

    1050: [1, 2, 3, 4, 5]
    1349: [1, 2, 3, 4, 5]
    4160: [1, 2, 3]
    ...

    First we split on the colon of each row, where the first
    half is the image filename and the second half is its
    associated labels.
    """
    with open(fname, "rb") as f:
        for line in f:
            subject, targets = line.split(":")
            # shirt_path = "training_shirts/{image}.jpg".format(
            #     image=shirt.strip()
            # )
            # shirt_path = os.path.abspath(shirt_path)

            # parse out the list of targets
            target_list = targets.strip()[1:-1].split(",")
            labels = map(lambda target: target.strip(), target_list)
            yield [ (subject, label) for label in labels]
    raise StopIteration


def generateRecommendation(subject):
    collection = Collection("subject_collection_1")

    # # Clear any previous changes
    # try:
    #     collection.clear()
    # except:
    #     pass

    # train = generate_training_data("anandhibot/subject_match_labeled_data_1.txt")

    # total = 0
    # for samples in train:
    #     print "Adding {num} samples to collection".format(num=len(samples))
    #     collection.add_data(samples)
    #     total += len(samples)
    #     print "Added {total} samples to collection thus far".format(total=total)

    # collection.train()
    # collection.wait()
    sort_key = itemgetter(1)
    return max(collection.predict(subject).items(), key=sort_key)[0]
