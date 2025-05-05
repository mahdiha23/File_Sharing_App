"""
URL configuration for DjangoShareFast project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from core.views import home , download , login_view , logout_view

from core.apis import HandleFileUpload

urlpatterns = [
    path('' , home ,name="home"),
    path('download/<uid>/' ,download ,name="download"),
    path('handle/', HandleFileUpload.as_view() ,name="handle"),
    path('login/', login_view ,name="login"),
    path("logout/", logout_view, name="logout"),
    path('admin/', admin.site.urls),
]



if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()