import datetime
import pickle
import tempfile

import numpy as np
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
# import os
#
# os.add_dll_directory("C:\\Program Files\GTK3-Runtime Win64")
#
# from weasyprint import HTML
from xhtml2pdf import pisa

from parkinsons_prediction import settings
from .models import *

from io import BytesIO
# Create your views here.

def index(request):
    return render(request, "index.html")


def doctor_login(request):
    return render(request, "doctor_login.html")


def doctor_register(request):
    return render(request, "doctor_register.html")


def save_register(request):
    if request.method == "POST":
        doctor_name = request.POST.get("doctor_name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        job_level = request.POST.get("job_level")
        username = request.POST.get("username")
        password = request.POST.get("password")
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        obj = Register_details()
        obj.doctor_name = doctor_name
        obj.mobile = mobile
        obj.email = email
        obj.job_level = job_level
        obj.username = username
        obj.password = password
        obj.image = uploaded_file_url
        obj.save()
        obj1 = Login_details()
        obj1.username = username
        obj1.password = password
        obj1.save()
        message = 'Username:%s \n Password:%s' % (obj.username, obj.password)
        send_mail('Login Details for doctors',
                  message,
                  settings.EMAIL_HOST_USER,
                  [obj.email])

        return redirect("/view_all_doctors/")


def doctor_login_check(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if (Login_details.objects.filter(username=username, password=password).exists()):
            login_obj = Login_details.objects.get(username=username, password=password)
            request.session['d_id'] = login_obj.id
            return redirect('/doctor_dashboard/')
        else:
            message = "Invalid Username or Password"
            return render(request, "doctor_login.html", {"message": message})


def doctor_dashboard(request):
    return render(request, "doctor_dashboard.html")


def add_patient(request):
    return render(request, "add_patient.html")


def save_patient(request):
    if request.method == "POST":
        patient_name = request.POST['patient_name']
        address = request.POST['address']
        email = request.POST['email']
        mobile = request.POST['mobile']
        age = request.POST['age']
        username = request.POST['username']
        password = request.POST['password']
        data = Patient_details_new()
        data.patient_name = patient_name
        d_id = request.session['d_id']
        d = Register_details.objects.get(id=d_id)
        data.doctor_name_id = d.id
        data.address = address
        data.age = age
        data.mobile = mobile
        data.username = username
        data.password = password
        data.email = email
        data.save()
        message = 'Username:%s \n Password:%s' % (data.username, data.password)
        send_mail('Login Details',
                  message,
                  settings.EMAIL_HOST_USER,
                  [data.email])

        return redirect('/doctor_dashboard/')


def view_patient(request):
    d_id = request.session['d_id']
    doc = Register_details.objects.get(id=d_id)
    data = Patient_details_new.objects.filter(doctor_name=doc)
    return render(request, "view_patient.html", {"data": data})


def edit_patient(request, id):
    data = Patient_details_new.objects.get(id=id)
    return render(request, "edit_patient.html", {"data": data})


def update_patient(request, id):
    data = Patient_details_new.objects.get(id=id)
    if request.method == "POST":
        data.patient_name = request.POST['patient_name']
        data.address = request.POST['address']
        data.age = request.POST['age']
        data.email = request.POST['email']
        data.password = request.POST['password']
        data.username = request.POST['username']
        data.mobile = request.POST['mobile']
        data.save()
        return redirect('/view_patient/')


def delete_patient(request, id):
    data = Patient_details_new.objects.get(id=id)
    data.delete()
    return redirect("/view_patient/")


#######################################################################################################


def prediction(request, id):
    data = Patient_details_new.objects.get(id=id)
    return render(request, "prediction.html", {"data": data})


def save_prediction(request, id):
    print(type(id),"firsttype")
    model = pickle.load(open('park.pkl', 'rb'))
    if request.method == "POST":
        Fo = request.POST.get("MDVP:Fo(Hz)")
        Flo = request.POST.get("MDVP:Flo(Hz)")
        Abs = request.POST.get("MDVP:Jitter(Abs)")
        shimmer = request.POST.get("MDVP:Shimmer")
        dB = request.POST.get("MDVP:Shimmer(dB)")
        APO = request.POST.get("MDVP:APQ")
        DDA = request.POST.get("Shimmer:DDA")
        HNR = request.POST.get("HNR")
        RPDE = request.POST.get("RPDE")
        DFA = request.POST.get("DFA")
        Spread1 = request.POST.get("Spread1")
        Spread2 = request.POST.get("Spread2")
        D2 = request.POST.get("D2")
        PPE = request.POST.get("PPE")
        arr = np.array([[Fo, Flo, Abs, shimmer, dB, APO, DDA, HNR, RPDE, DFA, Spread1, Spread2, D2, PPE]],dtype=object)
        pred = model.predict(arr)
        print(pred, "predictionnn")

        ps = Prediction_details_new1()
        d_id = request.session['d_id']
        d = Register_details.objects.get(id=d_id)
        p=Patient_details_new.objects.get(id=id)
        ps.doctor_name_id = d.id
        ps.patient_name_id = id
        ps.Fo = Fo
        ps.Flo = Flo
        ps.Abs = Abs
        ps.shimmer = shimmer
        ps.dB = dB
        ps.APO = APO
        ps.DDA = DDA
        ps.HNR = HNR
        ps.RPDE = RPDE
        ps.DFA = DFA
        ps.Spread1 = Spread1
        ps.Spread2 = Spread2
        ps.D2 = D2
        ps.PPE = PPE
        ps.save()
        print("pred,",pred)
        doctor = d.id
        patient = id
        Fo = ps.Fo
        Flo = ps.Flo
        Abs = ps.Abs
        shimmer = ps.shimmer
        dB = ps.dB
        APO = ps.APO
        DDA = ps.DDA
        HNR = ps.HNR
        RPDE = ps.RPDE
        DFA = ps.DFA
        Spread1 = ps.Spread1
        Spread2 = ps.Spread2
        D2 = ps.D2
        PPE = ps.PPE
        email=p.email

        html_template = 'download_pdf.html'
        html_message = download_to_pdf(request,email, doctor,patient, Fo, Flo, Abs, shimmer, dB, APO, DDA, HNR,
                                       RPDE,DFA,Spread1,Spread2,D2,PPE)
        if pred == [1]:
            ps.result="Positive"
            ps.save()
            status=1
            return render(request, "result.html", {"status": status})
        else:
            ps.result="Negative"
            ps.save()
            status=0
            return render(request, "result.html", {"status": status})



def download_to_pdf(request,email, doctor, patient, Fo, Flo, Abs, shimmer, dB, APO, DDA, HNR,RPDE,DFA,Spread1,Spread2,D2,PPE):

    template = get_template('download_pdf.html')
    context = {'doctor': doctor, 'patient': patient, 'Fo': Fo, 'Flo': Flo, 'Abs': Abs, 'shimmer': shimmer, 'dB': dB,
               'APO': APO, 'DDA': DDA, 'HNR': HNR,"RPDE":RPDE,"DFA":DFA,"Spread1":Spread1,"Spread2":Spread2,
               "D2":D2,"PPE":PPE}
    html = template.render(context)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = 'result.pdf'

    to_emails = [email]
    subject = "Result"
    email = EmailMessage(subject, "Result", from_email=settings.EMAIL_HOST_USER, to=to_emails)
    email.attach(filename, pdf, "application/pdf")
    email.send(fail_silently=False)


def result(request):
    return render(request, "result.html")


def user_login(request):
    return render(request, "user_login.html")


def check_user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if (Patient_details_new.objects.filter(username=username, password=password).exists()):
            login_obj = Patient_details_new.objects.get(username=username, password=password)
            request.session['u_id'] = login_obj.id
            return redirect("/user_dashboard/")
        else:
            return HttpResponse("Invalid Credentials")


def user_dashboard(request):
    return render(request, "user_dashboard.html")


def my_profile(request):
    u_id = request.session['u_id']
    data = Patient_details_new.objects.get(id=u_id)
    return render(request, "myprofile.html", {"data": data})


def my_result(request):
    u_id = request.session['u_id']
    data = Prediction_details_new1.objects.filter(patient_name=u_id)

    return render(request, "my_result.html",{"data":data})


def admin_login(request):
    return render(request, "admin_login.html")


def check_admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # request.session['uid']=un
        message = "invalid"
        if user is not None:
            login(request, user)
            return redirect('/admin_dashboard/')
        else:
            return render(request, 'admin_login.html', {'message': message})


def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


def view_all_doctors(request):
    data=Register_details.objects.all()
    return render(request, "view_all_doctors.html",{"data":data})


def admin_view_predictions(request):
    data=Prediction_details_new1.objects.all()
    return render(request, "admin_view_predictions.html",{"data":data})


def view_all_patients(request):
    data=Patient_details_new.objects.all()
    return render(request,"view_all_patient.html",{"data":data})


def edit_doctor(request,id):
    data = Register_details.objects.get(id=id)
    return render(request, "edit_doctor.html", {"data": data})


def update_doctor(request, id):
    data = Register_details.objects.get(id=id)


    if request.method == "POST":
        data.doctor_name = request.POST.get("doctor_name")

        data.job_level = request.POST.get("job_level")
        data.email = request.POST.get("email")
        data.password = request.POST.get("password")
        data.username = request.POST.get("username")
        data.mobile = request.POST.get("mobile")
        data.save()

        return redirect('/view_all_doctors/')


def delete_doctor(request,id):
    data = Register_details.objects.get(id=id)
    data.delete()
    return redirect("/view_all_doctors/")


def view_predictions(request):
    d_id=request.session['d_id']
    data=Prediction_details_new1.objects.filter(doctor_name=d_id)
    return render(request,"view_predictions.html",{"data":data})


def doctor_view_messages(request):
    d_id = request.session['d_id']
    data=message_details.objects.filter(doctor_name=d_id)

    return render(request,"doctor_view_messages.html",{"data":data})



def msg_to_doctor(request):
    u_id = request.session['u_id']
    data = Patient_details_new.objects.get(id=u_id)

    return render(request,"msg_to_doctor.html",{"data":data})





def save_msg_to_doctor(request):
    if request.method=="POST":
        u_id=request.session['u_id']
        doctor_name = request.POST.get("doctor_name")
        d = Register_details.objects.get(doctor_name=doctor_name)


        message=request.POST.get("message")
        obj=message_details()
        obj.doctor_name_id = d.id
        obj.patient_name_id=u_id
        obj.message=message
        obj.save()
        msg="success"
        return redirect("/view_user_message/")


def view_user_message(request):
    u_id=request.session['u_id']

    data=message_details.objects.filter(patient_name=u_id)
    return render(request,"view_user_message.html",{"data":data})


def reply_to_patient(request,id):
    data=message_details.objects.get(id=id)

    return render(request,"reply_to_patient.html",{"data":data})


def update_message(request,id):
    data = message_details.objects.get(id=id)
    if request.method=="POST":

        data.reply=request.POST.get("reply")
        data.save()
        return redirect("/doctor_view_messages/")


def view_reply_from_doctor(request,id):
    data=message_details.objects.get(id=id)
    return render(request,"view_reply_from_doctor.html",{"data":data})

def pdf(request):
    return render(request,"download_pdf.html")