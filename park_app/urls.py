from django.urls import path
from park_app import views
urlpatterns=[
    path('', views.index),
    path('index/',views.index),
    path('doctor_login/',views.doctor_login),
    path('doctor_register/',views.doctor_register),
    path('save_register/',views.save_register),
    path('doctor_login_check/',views.doctor_login_check),
    path('doctor_dashboard/',views.doctor_dashboard),
    path('add_patient/',views.add_patient),
    path('save_patient/',views.save_patient),
    path('view_patient/',views.view_patient),
    path('edit_patient/<id>',views.edit_patient),
    path('update_patient/<id>',views.update_patient),
    path("delete_patient/<id>",views.delete_patient),
    path('prediction/<id>',views.prediction),
    path('save_prediction/<id>',views.save_prediction),
    path('result/',views.result),

    path('user_login/',views.user_login),
    path('check_user_login/',views.check_user_login),
    path('user_dashboard/',views.user_dashboard),
    path('my_profile/',views.my_profile),
    path('my_result/',views.my_result),



    path('admin_login/',views.admin_login),
    path('check_admin_login/',views.check_admin_login),
    path('admin_dashboard/', views.admin_dashboard),
    path('admin_view_predictions/',views.admin_view_predictions),
    path('view_all_doctors/',views.view_all_doctors),
    path('view_all_patients/',views.view_all_patients),
    path('edit_doctor/<id>',views.edit_doctor),
    path('update_doctor/<id>',views.update_doctor),
    path('view_predictions/',views.view_predictions),

    path('delete_doctor/<id>',views.delete_doctor),
    path('doctor_view_messages/',views.doctor_view_messages),
    path("msg_to_doctor/",views.msg_to_doctor),
    path("download_to_pdf/",views.download_to_pdf),
    path("save_msg_to_doctor/",views.save_msg_to_doctor),
    path("view_user_message/",views.view_user_message),
    path("reply_to_patient/<id>",views.reply_to_patient),
    path("update_message/<id>",views.update_message),
    path("view_reply_from_doctor/<id>",views.view_reply_from_doctor),
    path("pdf/",views.pdf)
]