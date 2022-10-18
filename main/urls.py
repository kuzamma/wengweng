"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import admin_views, staff_views, views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", admin_views.admin_home, name='admin_home'),
    path("staff/add", admin_views.add_staff, name='add_staff'),

    path("admin_view_profile", admin_views.admin_view_profile,
         name='admin_view_profile'),

    path("check_email_availability", admin_views.check_email_availability,
         name="check_email_availability"),
    path("staff/view/feedback/", admin_views.staff_feedback_message,
         name="staff_feedback_message", ),
    path("staff/view/leave/", admin_views.view_staff_leave, name="view_staff_leave", ),

path("staff/view/view_staff_competency_journal/", admin_views.view_staff_competency_journal, name="view_staff_competency_journal"),

    path("staff/manage/", admin_views.manage_staff, name='manage_staff'),

    path("formal/manage/", admin_views.manage_formal, name='manage_formal'),


    path("staff/edit/<int:staff_id>", admin_views.edit_staff, name='edit_staff'),
    path("staff/delete/<int:staff_id>",


         admin_views.delete_staff, name='delete_staff'),



    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),

    path("staff/add/competency/", staff_views.competency_journal,
         name='competency_journal'),
    path("staff/delete_competency/", staff_views.delete_competency,
         name='delete_competency'),
path("staff/edit_competency/", staff_views.edit_competency,
         name='edit_competency'),

    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),

    path("staff/add/", staff_views.add_formal, name='add_formal'),
    path("staff/profile/", staff_views.staff_profile, name='staff_profile'),

]
