"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.urls import path, include
from expapp.views import EmployeeViewSet, EmployeeGenericListView, LoginView, SignUpView, HelloView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views


router = DefaultRouter()
router.register("", EmployeeViewSet, basename="employee-detail")
urlpatterns = [
    path("api/hello", HelloView.as_view(), name="helloview"),
    path('api/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("employee/auth/login/", LoginView.as_view(), name="login"),
    path("employee/auth/signup/", SignUpView.as_view(), name="signup"),
    path("api/", include(router.urls)),
    path("employeegeneric/", EmployeeGenericListView.as_view(), name="generic"),
    path("employeegeneric/<int:id>/", EmployeeGenericListView.as_view(), name="generic"),



]
