from django.contrib import admin

from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas.coreapi import AutoSchema
from rest_framework_simplejwt import views as jwt_views

schema_view = get_swagger_view(title='Chat API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc/', schema_view),
    path('api-auth/', include('rest_framework.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('rest-auth/', include('rest_auth.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
] \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
