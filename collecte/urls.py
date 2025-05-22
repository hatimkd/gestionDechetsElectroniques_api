from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    DemandeCollecteViewSet,
    ChargementViewSet,
    ChargementCreateView,
    DechetViewSet,
    RapportViewSet,
    DemandesAChargerView,
)

router = DefaultRouter()
router.register(r"demandes", DemandeCollecteViewSet, basename="demandecollecte")
router.register(r"chargements", ChargementViewSet, basename="chargement")
router.register(r"dechets", DechetViewSet, basename="dechet")
router.register(r"rapports", RapportViewSet, basename="rapport")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "demandes-a-charger/", DemandesAChargerView.as_view(), name="demandes-a-charger"
    ),
    
    path("chargement/", ChargementCreateView.as_view(), name="chargement-create"),
]
