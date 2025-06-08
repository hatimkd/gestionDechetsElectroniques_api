from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    DemandeCollecteViewSet,
    ChargementViewSet,
    ChargementCreateView,
    DechetViewSet,
    RapportViewSet,
    DemandesAChargerView,
    
    
    
    
    # ClientDashboardView 
)

router = DefaultRouter()
router.register(r"demandes", DemandeCollecteViewSet, basename="demandecollecte")
router.register(r"chargements", ChargementViewSet, basename="chargement")
router.register(r"dechets", DechetViewSet, basename="dechet")
router.register(r"rapports", RapportViewSet, basename="rapport")

# router.register(r'rapports', RapportViewSet, basename='rapport')

# router.register(r'dechets', DechetViewSet)
from django.conf.urls.static import static


from django.conf import settings

urlpatterns = [
    path("", include(router.urls)),
    path(
        "demandes-a-charger/", DemandesAChargerView.as_view(), name="demandes-a-charger"
    ),
    path("chargement/", ChargementCreateView.as_view(), name="chargement-create"),
    # path("dashboard/count/", DashboardCountView.as_view(), name="dashboard-count"),

    
        # path('client/dashboard/', ClientDashboardView.as_view(), name='client-dashboard'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
