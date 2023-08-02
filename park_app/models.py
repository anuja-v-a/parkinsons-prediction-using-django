from django.db import models

# Create your models here.

class Login_details(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    dt=models.DateField(auto_now_add=True)
    tm=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=200)


class Register_details(models.Model):
    doctor_name=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    job_level=models.CharField(max_length=200,default="Junior")
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    image=models.FileField(upload_to="")
    dt=models.DateField(auto_now_add=True)
    tm=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=200)

class Patient_details_new(models.Model):
    doctor_name = models.ForeignKey(Register_details, on_delete=models.CASCADE, related_name="patient_register_doctor")

    patient_name=models.CharField(max_length=200)
    address=models.TextField(max_length=500)
    email=models.EmailField(max_length=200)
    age=models.CharField(max_length=200)
    mobile=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    dt=models.DateField(auto_now_add=True)
    tm=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=200)


class Prediction_details_new1(models.Model):
    doctor_name=models.ForeignKey(Register_details,on_delete=models.CASCADE,related_name="register_doctor")
    patient_name=models.ForeignKey(Patient_details_new,on_delete=models.CASCADE,related_name="prediction_patient")
    Fo=models.CharField(max_length=200)
    Flo=models.CharField(max_length=200)
    Abs=models.CharField(max_length=200)
    shimmer=models.CharField(max_length=200)
    dB=models.CharField(max_length=200)
    APO=models.CharField(max_length=200)
    DDA=models.CharField(max_length=200)
    HNR=models.CharField(max_length=200)
    RPDE=models.CharField(max_length=200)
    DFA=models.CharField(max_length=200)
    Spread2=models.CharField(max_length=200)
    Spread1=models.CharField(max_length=200)
    D2=models.CharField(max_length=200)
    PPE=models.CharField(max_length=200)
    result=models.CharField(max_length=200)
    dt=models.DateField(auto_now_add=True)
    tm=models.TimeField(auto_now_add=True)
    status=models.CharField(max_length=200)


class message_details(models.Model):
    doctor_name=models.ForeignKey(Register_details,on_delete=models.CASCADE,related_name="msg_doctor")
    patient_name=models.ForeignKey(Patient_details_new,on_delete=models.CASCADE,related_name="msg_patient")
    message=models.TextField(max_length=1000)
    reply=models.TextField(max_length=1000,blank=True)
    dt = models.DateField(auto_now_add=True)
    tm = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=200)

