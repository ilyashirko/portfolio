from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.main_page, name='main_page'),
    path('resume/', main_views.resume, name='resume'),
    path('biography/', main_views.biography, name='biography'),
    path('contacts/', main_views.contacts, name='contacts'),
    path('portfolio/', main_views.portfolio, name='portfolio'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
