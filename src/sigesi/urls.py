# future

# Librerias Standars

# Librerias de Terceros

# Django
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Django Locales
from apps.core.views import landing_page, Error_404, Error_500

handler404 = Error_404
handler500 = Error_500

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),  # admin site
    path('', landing_page, name='home'),
    path('inscripcion/', include('apps.inscripcion.urls')),
    # Vistas para el manejo de cuentas, inscriptor_home reemplaza las de
    # path('cuentas/', include('django.contrib.auth.urls'))
    path("cuentas/login/", auth_views.LoginView.as_view(template_name="cuentas/login.html"), name='login'),
    path("cuentas/logout/", auth_views.LogoutView.as_view(template_name="cuentas/logout.html"), name='logout'),
    #path("cuentas/password_change/", auth_views.PasswordChangeView.as_view(template_name="cuentas/password_change.html"), name='password_change'),
    #path("cuentas/password_change/done/", auth_views.PasswordChangeDoneView.as_view(template_name="cuentas/password_change_done.html"), name='password_change_done'),
    path("cuentas/password_reset/", auth_views.PasswordResetView.as_view(template_name="cuentas/password_reset_form.html"), name='password_reset'),
    path("cuentas/password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="cuentas/password_reset_done.html"), name='password_reset_done'),
    path("cuentas/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="cuentas/password_reset_confirm.html"), name='password_reset_confirm'),
    path("cuentas/reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/password_reset_complete.html"), name='password_reset_complete'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
