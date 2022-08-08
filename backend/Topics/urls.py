from django.contrib import admin
from django.urls import path, include

from catalogue.views import sign_up


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("catalogue.urls")),
    path('accounts/sign-up', sign_up, name="sign-up"),
    path('accounts/', include('django.contrib.auth.urls')), 
]
