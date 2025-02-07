from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from filebrowser.sites import site
from django.views.i18n import set_language

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('dashboard/',include('dashboard.urls',namespace='dash')),
    path('tinymce/', include('tinymce.urls')),
    # Language Changer
    path('set-language/', set_language, name='set_language'),
    # frontend
    path('', include('frontend.urls',namespace='frontend')),
    # Auth
    path('',include('user_auth.urls',namespace='user_auth')),
    # Patient 
    path('patient/',include('patient.urls',namespace='patient')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
