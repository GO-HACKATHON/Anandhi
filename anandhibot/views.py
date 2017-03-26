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
from anandhibot.answerfinder import AnswerFinder
from anandhibot.models import User

from app_properties import channel_secret, channel_access_token
from django.views.generic import TemplateView
from anandhibot.forms import InputForm
import os
import indicoio
from operator import itemgetter
import schedule
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from indicoio.custom import Collection

indicoio.config.api_key = '897b8fc085058e1a5ee77bc7f2cc24de'


# Create your views here
# class HomePageView(TemplateView):
#      def get(self, request, **kwargs):
#           return render(request, 'index.html', context=None)


# sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds=10)
# def timed_job():
#     print('This job is run every three minutes.')
#     teknikInformatika = User.objects.filter(major="teknik informatika")
#     for ti in teknikInformatika:
#         print(ti.uid)
#         pushToUser(ti.uid, "Hi Anandhi bawa informasi menarik nih buat kamu! Ini dia 4 situs belajar pemrograman yang bisa kamu coba. \nhttps://id.techinasia.com/dev-series-4-website-gratis-belajar-coding")
#         print("Text sent")

# # @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# # def scheduled_job():
# #     print('This job is run every weekday at 5pm.')

# sched.start()

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
    # if aXLineSignature != signature:
    #     return Response("X-Line-Signature is not valid")
    
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

    # d = User.objects.get(uid=mTargetId)
    # d.delete()

    # for pub in User.objects.all():
    #     pub.delete()
    list_of_id = []

    for user in User.objects.all():
        print(user.uid)
        print(user.major)
        list_of_id.append(user.uid)

    print("Before:")
    print(list_of_id)

    if mTargetId not in list_of_id:
        newuser = User(uid=mTargetId, name="", city="", uclass="", prompt="0", major="")
        newuser.save()
        list_of_id.append(newuser.uid)

    print("After:")
    print(list_of_id)

    # obj, created = User.objects.get_or_create(uid=mTargetId, name="", city="", uclass="", prompt="0")
    # print(created)
    # if created == False:
    #     obj.save()

    # if 'minta rekomendasi' in mText:
    #     replyToUser(mReplyToken, "Emang apa aja mata pelajaran yang kamu suka di sekolah? ^^")
    #     getRecommendation(mText, mReplyToken, mTargetId)
    # elif 'tanya dong,' in mText:
    #     getInfo(mText, mReplyToken, mTargetId)
    # else:
    #     getRecommendation(mText, mReplyToken, mTargetId)
    sendMessage(aPayload)
    
    return Response ("anandhibot")


def replyToUser(reply_token, text_message):
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.reply_message(reply_token, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print('Exception is raised')

def pushToUser(target_id, text_message):
    line_bot_api = LineBotApi(channel_access_token)
    try:
        line_bot_api.push_message(target_id, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print('Exception is raised')    


def sendMessage(event):
    mText = event['events'][0]['message']['text'].lower()
    mReplyToken = event['events'][0]['replyToken']
    mTargetId = event['events'][0]['source']['userId']

    user = User.objects.get(uid=mTargetId)
    print(user.prompt)
    print(mText)
    print(mReplyToken)

    # if user.name == "":
    #     pushToUser(mTargetId, "Kenalan dulu yuk, nama kamu siapa?")
    #     user.name = mText
    #     pushToUser(mTargetId, "Berarti seterusnya aku boleh ya manggil kamu"+user.name+"?")
    #     if "iya" or "iya" in mText:
    #         pushToUser(mTargetId, "Makasih ya "+user.name+". Seneng bisa kenalan sama kamu :D")
    #         if user.city == "":
    #             pushToUser(mTargetId, "Kalo boleh tahu, kamu tinggal di kota mana?")
    #             user.city = mText
    #             pushToUser(mTargetId, "Ooh ternyata kamu tinggal di "+user.city)
    #             if "iya" or "ya" in mText:
    #                 pushToUser(mTargetId, "Sip deh :D")
    #                 if user.uclass=="":
    #                     pushToUser(mTargetId, "Sekarang kamu kelas berapa?")
    #                     if '12' or 'dua belas' in mText:
    #                         pushToUser(mTargetId, "Wah tepar banget! Aku bisa bantu kamu lho untuk ngasih rekomendasi jurusan kuliah. Jangan malu untuk nanya aku ya")
    #                         user.uclass = "12"
    #                     else:
    #                         pushToUser(mTargetId, "Hebat! Dari sekarang udah tertarik untuk cari tau informasi tentang jurusan kuliah. Anandhi seneng banget bisa bantu kamu.")
    #                 else:
    #                     pushToUser(mTargetId, "Kamu udah tau nanti kuliah mau di jurusan apa?")
    #             else:
    #                 pushToUser(mTargetId, "Yah, jadi dimana dong?")
    #                 user.city==""
    #     else:
    #         pushToUser(mTargetId, "Jadi nama kamu siapa? :(")
    #         user.name=""

    # user baru mau bertanya
    if user.prompt == "0":
        print("masuk")
        if 'rekomendasi' or 'saran' in mText:
            print("Iya?")
            pushToUser(mTargetId, "Emang apa aja mata pelajaran yang kamu suka di sekolah? ^^")
            user.prompt = "1"
            user.save()
        elif 'tanya' or 'nanya' in mText:
            print("apa?")
            pushToUser(mTargetId, "Kamu mau tau tentang jurusan apa?")
            user.prompt = "2"
            user.save()
        elif 'apa' or 'coba' or 'tebak' in mText:
            if user.major == "":
                pushToUser(mTargetId, "Kamu kan belum kasih tau aku -__-")
            else:
                pushToUser(mTargetId, "Aku tau, " + user.major + " kan? :3")
                print(user.major)
        elif 'pilih' or 'tau' or 'tahu' or 'mau' in mText:
            pushToUser(mTargetId, "Wah, " + mText.split('pilih ', 1)[1] + " itu pilihan yang tepat banget buat kamu! Anandhi janji bakal  ngasih tau kamu informasi menarik tentang jurusan"+ mText.split('pilih ', 1)[1] +".")
            user.major = mText.split('pilih ', 1)[1]
            print(user.major)
            user.save()
            if user.major == "teknik informatika":
                time.sleep(5)
                pushToUser(mTargetId, "Hi Anandhi bawa informasi menarik nih buat kamu! Ini dia 4 situs belajar pemrograman yang bisa kamu coba. \nhttps://id.techinasia.com/dev-series-4-website-gratis-belajar-coding")
        else:
            replyToUser(mReplyToken, "Kalau kamu ada pertanyaan soal jurusan kuliah, atau mau tau jurusan favoritmu ada di kampus mana, kamu bisa bilang ke aku "/"Anandhi, tanya dong"/" (james wink)\nKalo kamu butuh saran jurusan kuliah yang kira-kira cocok untuk kamu, kamu bisa panggil aku dengan "/"Anandhi, minta saran dong"/" (moon wink)")
            # schedule.every(10).seconds.do(spam)

            # while True:
            #     schedule.run_pending()
            #     time.sleep(1)
    elif user.prompt == "1":
        # user sudah meminta rekomendasi
        print("oke")
        getRecommendation(mText, mTargetId)
        # pushToUser(mTargetId, "Dari semua jurusan yang udah aku sebutin, kasih tau dong 1 jurusan yang buat kamu tertarik. Nanti aku kasih tau deh informasi mengenai jurusan pilihan kamu.")
        # if 'belum' or 'nggak' or 'enggak' or 'tidak' in mText:
        #     pushToUser(mTargetId, "Ya udah deh. Mungkin kamu ada yang bingung ya sama jurusan di atas?")
        #     if 'iya' in mText:
        #         pushToUser(mTargetId, "Kamu bingung sama jurusan apa?")
        #         user.prompt = "2"
        user.save()
    elif user.prompt == "2":
        print("siap")
        getInfo(mText, mTargetId)
        user.prompt = "0"
        user.save()


def getInfo(pertanyaan, target_id):
    msgToUser = ' '
    hasilQuestionAnalyzer = []
    hasilDocumentRetriever = []
    hasilAnswerFinder = []

    try:
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

        # answer finder
        answerFinder = AnswerFinder(questionAnalyzer.questionEAT, questionAnalyzer.query, questionAnalyzer.keywords, hasilDocumentRetriever)

        for doc in hasilDocumentRetriever:
            print("ketemu:")
            print(doc.url)

        # simpan answer finder
        hasilAnswerFinder = answerFinder.getAnswers()

        msgToUser = hasilAnswerFinder[0]

        print("Message to user: " + hasilAnswerFinder[0])

        if len(msgToUser) <= 11 :
            pushToUser(target_id, "Request Timeout")
        else:
            pushToUser(target_id, msgToUser)
    except (IndexError, ValueError):
        pushToUser(target_id, "Maaf, sayangnya aku belum bisa bantu jawab soal itu :(")
        print("Maaf")


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


def getRecommendation(subject, target_id):
    collection = Collection("subject_collection_1")

    msgToUser = ' '
    pelajaran = subject.split(",")
    recom_list = []
    sentrec = []
    # # Clear any previous changes
    # try:
    #     collection.clear()
    # except:
    #     pass

    # train = generate_training_data("anandhibot/subject_match_labeled_data_1.txt")

    # total = 0
    # for samples in train:
    #     pushToUser(target_id, "training......")
    #     print("training.....")
    #     collection.add_data(samples)
    #     total += len(samples)
    #     pushToUser(target_id, "still training....")
    #     print("still training.....")

    # collection.train()
    # pushToUser(target_id, "selesai training")
    # print("selesai training")
    # collection.wait()

    sort_key = itemgetter(1)
    for sub in pelajaran:
        recommendation = sorted(collection.predict(sub).items(), key=sort_key)
        recom_list = recom_list + recommendation[-2:]
    
    for rec in recom_list:
        if rec[0] not in sentrec:
            sentrec.append(rec[0])

    msgToUser = "Berikut jurusan yang cocok buat kamu berdasarkan minat mata pelajaran:" + ', '.join(sentrec)

    print("Message to user: " + ', '.join(sentrec))

    if len(msgToUser) <= 11 :
        pushToUser(target_id, "Request Timeout")
    else:
        pushToUser(target_id, msgToUser)
    
    # return max(collection.predict(subject).items(), key=sort_key)[0]

# def spam():
#     teknikInformatika = User.objects.filter(major="teknik informatika")
#     for ti in teknikInformatika:
#         print(ti.uid)
#         pushToUser(ti.uid, "Hi Anandhi bawa informasi menarik nih buat kamu! Ini dia 4 situs belajar pemrograman yang bisa kamu coba. \nhttps://id.techinasia.com/dev-series-4-website-gratis-belajar-coding")
#         print("Text sent")
