from django.urls import path
from .views import (
    ClientRegisterView,
    CustomTokenObtainPairView,
    AdminValidateClientView,
    UserMeView,
    VehiculeViewSet,
)
from rest_framework.routers import DefaultRouter

from .views import (
    AdminCreateClientView,
    AdminCreateTechnicienView,
    AdminCreateLogisticienView,
    AdminCreateManagerView,
    
    
    InactiveEntreprisesView,
    UserViewSet
)
router = DefaultRouter()
router.register('vehicules', VehiculeViewSet , basename='vehicule')
router.register(r'users', UserViewSet, basename='user')
urlpatterns = [
    path("register/", ClientRegisterView.as_view(), name="client_register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    
    
    path("create-client/", AdminCreateClientView.as_view()),
    path("admin/create-technicien/", AdminCreateTechnicienView.as_view()),
    path("admin/create-logisticien/", AdminCreateLogisticienView.as_view()),
    path("admin/create-manager/", AdminCreateManagerView.as_view()),
    path(
        "admin/validate-client/<int:pk>/",
        AdminValidateClientView.as_view(),
        name="validate-client",
    ),
    path("me/", UserMeView.as_view(), name="user_me"),
        path('admin/entreprises/inactives/', InactiveEntreprisesView.as_view(), name='inactive-entreprises'),


]+ router.urls
