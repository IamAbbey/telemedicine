"""telemedicine URL Configuration

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
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("apps.authentication.urls")),
    path("api/", include("apps.consultation.urls")),
]

handler500 = "rest_framework.exceptions.server_error"
handler400 = "rest_framework.exceptions.bad_request"

from rest_framework.exceptions import NotFound


def error404(request, exception):
    raise NotFound(detail="Error 404, page not found", code=404)


handler404 = error404

admin.site.site_header = "Telemedicine Adminstration"
admin.site.index_title = "Telemedicine Admin Panel"
admin.site.site_title = "Telemedicine Admin"