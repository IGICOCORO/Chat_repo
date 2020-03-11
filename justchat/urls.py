from django.contrib import admin
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas.coreapi import AutoSchema
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

schema_view = get_swagger_view(title='Chat API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/doc/', schema_view),
    path('api-auth/', include('rest_framework.urls')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('rest-auth/', include('rest_auth.urls')),
      path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
