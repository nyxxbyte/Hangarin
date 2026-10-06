from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('pwa.urls')), 
    path('', include('tracker.urls')),
    path('serviceworker.js', TemplateView.as_view(template_name="serviceworker.js", content_type='application/javascript'), name='serviceworker'),
]