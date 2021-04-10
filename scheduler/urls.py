from django.contrib import admin
from django.urls import include, path
from schedulerZstatic.views import home

urlpatterns = [
    path('about/', home, name='home'),
    path('blog/', include('schedulerZ.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('schedulerZ.urls', namespace='api')),
    path('api-auth/', include('rest_framework.urls')),
]
