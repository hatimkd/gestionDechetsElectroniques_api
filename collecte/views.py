from rest_framework import viewsets, permissions
from .models import DemandeCollecte, Chargement, Dechet, Rapport
from .serializers import (
    DemandeCollecteSerializer,
    ChargementSerializer,
    DechetSerializer,
    RapportSerializer,
)
from rest_framework.response import Response


from rest_framework import status

from rest_framework.decorators import action


from .permissions import IsClient, IsManager, IsLogisticien, IsTechnicien


from .models import Client


class DemandeCollecteViewSet(viewsets.ModelViewSet):
    queryset = DemandeCollecte.objects.all()
    serializer_class = DemandeCollecteSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated(), IsClient()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        client = Client.objects.get(
            user=self.request.user
        )  # Assure-toi que l'utilisateur a un client associé
        # Créer la demande avec le client
        serializer.save(client=client)

    def get_queryset(self):
        """
        Cette méthode filtre les demandes pour que l'utilisateur ne voie que ses propres demandes.
        Si l'utilisateur est un admin, il peut voir toutes les demandes.
        """
        user = self.request.user

        # Si l'utilisateur est admin, il peut voir toutes les demandes
        if (
            user.is_staff or user.groups.filter(name="Manager").exists()
        ):  # Cela vérifie si l'utilisateur est un administrateur
            return DemandeCollecte.objects.all()

        # Si l'utilisateur est un client, on filtre les demandes par client
        if user.is_authenticated:
            return DemandeCollecte.objects.filter(client__user=user)

        # Si l'utilisateur n'est pas authentifié, aucune demande n'est retournée
        return DemandeCollecte.objects.none()

    @action(detail=True, methods=["patch"], url_path="valider")
    def valider(self, request, pk=None):
        """
        Action réservée aux administrateurs (is_staff) ou aux managers
        pour valider la demande de collecte.
        """
        demande = self.get_object()

        if demande.statut == DemandeCollecte.Statut.VALIDEE:
            return Response(
                {"detail": "Cette demande est déjà validée."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Mettre à jour le statut
        demande.statut = DemandeCollecte.Statut.VALIDEE

        # Si c'est un admin, on peut le laisser vide ou stocker un manager générique
        if request.user.is_staff:
            # Ne change pas demande.validee_par ou le laisser à None
            pass
        else:
            # Récupère le profil Manager lié à request.user
            try:
                manager = request.user.manager_profile
            except Manager.DoesNotExist:
                return Response(
                    {"detail": "Profil manager introuvable."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            demande.validee_par = manager

        # Sauvegarde
        demande.save(update_fields=["statut", "validee_par"])

        serializer = self.get_serializer(demande)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChargementViewSet(viewsets.ModelViewSet):
    queryset = Chargement.objects.all()
    serializer_class = ChargementSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsLogisticien()]
        return [permissions.IsAuthenticated()]


class DechetViewSet(viewsets.ModelViewSet):
    queryset = Dechet.objects.all()
    serializer_class = DechetSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTechnicien()]
        return [permissions.IsAuthenticated()]


class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsTechnicien()]
        return [permissions.IsAuthenticated()]


from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied


class CanViewCollectePermission(BasePermission):
    """
    Permission pour vérifier si l'utilisateur peut voir les demandes de collecte.
    """

    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et a la permission can_viewcollecte
        if request.user.has_perm(
            "collecte.view_demandecollecteacharger"
        ):  # Remplacez 'yourapp' par le nom de votre application
            return True
        raise PermissionDenied("Vous n'avez pas la permission de voir cette ressource.")


from django.db.models import Exists, OuterRef
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class DemandesAChargerView(generics.ListAPIView):
    serializer_class = DemandeCollecteSerializer
    permission_classes = [IsAuthenticated, CanViewCollectePermission]

    def get_queryset(self):
        # Exclure les demandes déjà associées à un chargement
        return (
            DemandeCollecte.objects.filter(statut=DemandeCollecte.Statut.VALIDEE)
            .annotate(
                has_chargement=Exists(
                    DemandeCollecte.chargements.rel.related_model.objects.filter(
                        demande_collecte=OuterRef("pk")
                    )
                )
            )
            .filter(has_chargement=False)
        )


class CanAddChargementPermission(BasePermission):
    """
    Permission personnalisée pour vérifier si l'utilisateur peut ajouter un chargement.
    """

    def has_permission(self, request, view):
        return request.user.has_perm(
            "collecte.add_chargement"
        )  # Remplacez 'yourapp' par le nom de votre app

from rest_framework import serializers

# Appliquez cette permission dans la vue
class ChargementCreateView(generics.CreateAPIView):
    queryset = Chargement.objects.all()
    serializer_class = ChargementSerializer
    permission_classes = [
        IsAuthenticated,
        CanAddChargementPermission,
    ]  # Utilisation de la permission personnalisée

    def perform_create(self, serializer):

        demande_collecte_id = self.request.data.get("demande_collecte")

        try:
            demande_collecte = DemandeCollecte.objects.get(id=demande_collecte_id)
        except DemandeCollecte.DoesNotExist:
            raise serializers.ValidationError(
                "DemandeCollecte avec cet ID n'existe pas."
            )

        # 🔴 Vérifie si la demande est validée
        if not demande_collecte.validee_par:
            raise serializers.ValidationError(
                "Cette demande de collecte n'a pas encore été validée par un manager."
            )
        # L'utilisateur connecté est automatiquement assigné comme logisticien
        serializer.save(logisticien=self.request.user)
