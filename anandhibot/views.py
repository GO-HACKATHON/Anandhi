import hmac
import hashlib
import base64
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from linebot import LineBotApi
from linebot.models import (TextSendMessage, ImageSendMessage, CarouselTemplate, CarouselColumn, TemplateSendMessage, MessageTemplateAction)
from linebot.exceptions import LineBotApiError

from anandhibot.questionanalyzer import QuestionAnalyzer
from anandhibot.documentretriever import DocumentRetriever

from app_properties import channel_secret, channel_access_token
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

@api_view(['POST'])
def callback(request):
    # Get request header and request body
    aXLineSignature = request.META.get('HTTP_X_LINE_SIGNATURE')
    print('Signature: ' + str(aXLineSignature))
    body = request.body
    print('Payload: ' + body)
    
    # Validate signature
    hash = hmac.new(channel_secret.encode('utf-8'),body.encode('utf-8'), hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    
    # Exit when signature not valid
    if aXLineSignature != signature:
        return Response("X-Line-Signature is not valid")
    
    aPayload = json.loads(body)
    mEventType = aPayload['events'][0]['type']
    print('Event type: ' + mEventType)
    mSource = aPayload['events'][0]['source']['type']
    mReplyToken = aPayload['events'][0]['replyToken']

    # if mEventType == 'join':
    #     if mSource == 'user':
    #         replyToUser(mReplyToken, 'Hello User')
    #     elif mSource == 'group':
    #         replyToUser(mReplyToken, 'Hello User')
    #     elif mSource == 'room':
    #         replyToUser(mReplyToken, 'Hello User')
    #     return Response("Event is join")

    if mEventType == 'message':
        if mSource == 'user':
            mTargetId = aPayload['events'][0]['source']['userId']
        else:
            replyToUser(mReplyToken, 'Maaf, aku belum tersedia untuk grup')
    else:
        replyToUser(mReplyToken, 'Wah, aku belum bisa bantu jawab untuk itu')
        # elif mSource == 'group':
        #     mTargetId = aPayload['events'][0]['source']['groupId']
        # elif mSource == 'room':
        #     mTargetId = aPayload['events'][0]['source']['roomId']

    mType = aPayload['events'][0]['message']['type']

    if mType != 'text':
        replyToUser(mReplyToken, 'Wah, aku belum bisa bantu jawab untuk itu')
        return Response("Message Type is not text")

    mText = aPayload['events'][0]['message']['text'].lower()

    if 'minta rekomendasi' in mText:
        getRecommendation(mText, mReplyToken, mTargetId)
    elif 'tanya dong,' in mText:
        getInfo(mText, mReplyToken, mTargetId)
    else:
        getRecommendation(mText, mReplyToken, mTargetId)
    
    return Response ("anandhibot")


def replyToUser(reply_token, text_message):
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.reply_message(reply_token, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print('Exception is raised')


def getInfo(pertanyaan, reply_token, target_id):
    msgToUser = ' '
    hasilQuestionAnalyzer = []
    hasilDocumentRetriever = []

    questionAnalyzer = QuestionAnalyzer(pertanyaan)
    hasilQuestionAnalyzer = []
    hasilQuestionAnalyzer.append("Pertanyaan: %s" % questionAnalyzer.query)
    print("Query: ")
    print(questionAnalyzer.query)
    hasilQuestionAnalyzer.append("Tipe: %s" % questionAnalyzer.questionEAT)
    print("EAT: ")
    print(questionAnalyzer.questionEAT)
    hasilQuestionAnalyzer.append("Kata Kunci: %s" % ", ".join(questionAnalyzer.keywords))
    print("Keywords: ")
    print(questionAnalyzer.keywords)

    documentRetriever = DocumentRetriever()

    hasilDocumentRetriever = documentRetriever.retrieve(questionAnalyzer.keywords)

    msgToUser = ', '.join(hasilQuestionAnalyzer) + '\n\n' + "Dokumen ditemukan: \n"+'\n '.join(hasilDocumentRetriever)

    print("Message to user: " + '\n '.join(hasilQuestionAnalyzer) + '\n' + '\n '.join(hasilDocumentRetriever))

    if len(msgToUser) <= 11 :
        replyToUser(reply_token, "Request Timeout")
    else:
        replyToUser(reply_token, msgToUser)



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

    msgToUser = ' '
    recom_list = []
    # Clear any previous changes
    try:
        collection.clear()
    except:
        pass

    train = generate_training_data("anandhibot/subject_match_labeled_data_1.txt")

    total = 0
    for samples in train:
        print "Adding {num} samples to collection".format(num=len(samples))
        collection.add_data(samples)
        total += len(samples)
        print "Added {total} samples to collection thus far".format(total=total)

    collection.train()
    collection.wait()

    sort_key = itemgetter(1)
    
    return max(collection.predict(subject).items(), key=sort_key)[0]


def getRecommendation(subject, reply_token, target_id):
    collection = Collection("subject_collection_1")

    msgToUser = ' '
    pelajaran = subject.split(" ")
    recom_list = []
    # # Clear any previous changes
    # try:
    #     collection.clear()
    # except:
    #     pass

    # train = generate_training_data("anandhibot/subject_match_labeled_data_1.txt")

    # total = 0
    # for samples in train:
    #     replyToUser(reply_token, "training......")
    #     collection.add_data(samples)
    #     total += len(samples)
    #     replyToUser(reply_token, "still training....")

    # collection.train()
    # replyToUser(reply_token, "selesai training")
    # collection.wait()

    sort_key = itemgetter(1)
    for sub in pelajaran:
        recommendation = max(collection.predict(sub).items(), key=sort_key)[0]
        recom_list.append(recommendation)

    msgToUser = "Rekomendasi dariku: " + ', '.join(recom_list)

    print("Message to user: " + ', '.join(recom_list))

    if len(msgToUser) <= 11 :
        replyToUser(reply_token, "Request Timeout")
    else:
        replyToUser(reply_token, msgToUser)
    
    # return max(collection.predict(subject).items(), key=sort_key)[0]
