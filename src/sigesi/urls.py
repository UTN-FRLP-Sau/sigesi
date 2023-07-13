"""
URL configuration for sigesi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static
#from django.contrib.auth.views import logout, login


from apps.core.views import landing_page, Error_404, Error_500

handler404 = Error_404
handler500 = Error_500

urlpatterns = [
    #path('logout/', logout, {'template_name': 'sesion/logout.html'}, name='logout'), #Sesion_logout
    #path('login/', login, {'template_name': 'sesion/login.html'}, name='login'), #Sesion_login
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),  # admin site
    path('', landing_page, name='home'),
    path('inscripcion/', include('apps.inscripcion.urls')),
    path('cuentas/', include('django.contrib.auth.urls'))
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
