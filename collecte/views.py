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


from .permissions import (
    IsClient,
    IsManager,
    IsLogisticien,
    IsTechnicienManager,
    IsTechnicien,
    IsLogisticienOrManager,
)


from .models import Client
from account.serializers import TechnicienSerializer


class DemandeCollecteViewSet(viewsets.ModelViewSet):
    queryset = DemandeCollecte.objects.all()
    serializer_class = DemandeCollecteSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]
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
        # request.user.groups.filter(name="Technicien").exists()
        return [
            IsTechnicienManager()
            # permissions.IsAuthenticated(),
            # IsTechnicien(),IsManager()
        ]
        # or selrequest.user.groups.filter(name="Technicien").exists()

    def perform_create(self, serializer):
        serializer.save()
    
    
    
    
    def get_queryset(self):
        queryset = Dechet.objects.all()
        chargement_id = self.request.query_params.get("chargement_id")

        if chargement_id:
            queryset = queryset.filter(chargement__id=chargement_id)

        return queryset


# class RapportViewSet(viewsets.ModelViewSet):
#     queryset = Rapport.objects.all()
#     serializer_class = RapportSerializer

#     def get_permissions(self):
#         if self.action == "create":
#             return [permissions.IsAuthenticated(), IsTechnicien()]
#         return [permissions.IsAuthenticated()]
from reportlab.pdfgen import canvas
from django.conf import settings
import os
from datetime import datetime


# def generer_pdf_rapport(rapport):
#     # Crée un nom de fichier unique
#     nom_fichier = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     # chemin_relatif = os.path.join("rapports", nom_fichier)
#     chemin_relatif = os.path.join("rapports", nom_fichier).replace("\\", "/")

#     chemin_absolu = os.path.join(settings.MEDIA_ROOT, chemin_relatif)

#     # Crée le dossier s'il n'existe pas
#     os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)

#     # Création du PDF
#     c = canvas.Canvas(chemin_absolu)
#     c.drawString(100, 800, f"Rapport du {rapport.date}")
#     c.drawString(100, 780, f"Poids mesuré : {rapport.poids_mesure} kg")
#     c.drawString(100, 760, f"Trié par : {rapport.trie_par.user.username}")

#     y = 740
#     for dechet in rapport.dechets:
#         c.drawString(
#             100,
#             y,
#             f"- {dechet['type_dechet']} x{dechet['quantite']} ({dechet['poids']}kg)",
#         )
#         y -= 20

#     c.save()
#     return chemin_relatif  # À stocker dans `chemin_pdf`

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from django.conf import settings
import os
from datetime import datetime


def generer_pdf_rapport(rapport):
    nom_fichier = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    chemin_relatif = os.path.join("rapports", nom_fichier)
    chemin_absolu = os.path.join(settings.MEDIA_ROOT, chemin_relatif)
    os.makedirs(os.path.dirname(chemin_absolu), exist_ok=True)

    c = canvas.Canvas(chemin_absolu, pagesize=A4)
    largeur, hauteur = A4
    y = hauteur - 2 * cm

    def add_line(text, size=12, bold=False):
        nonlocal y
        if y < 2 * cm:
            c.showPage()
            y = hauteur - 2 * cm
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(2 * cm, y, text)
        y -= 1 * cm

    add_line("📄 Rapport de tri", size=16, bold=True)
    add_line(f"Date du rapport : {rapport.date}")
    add_line(f"Poids mesuré : {rapport.poids_mesure} kg")
    add_line(
        f"Rapport est Validé par manager : {'Oui' if rapport.valide_par_manager else 'Non'}"
    )
    add_line("")

    # 🔹 Technicien
    technicien = rapport.trie_par
    add_line("👨‍🔧 Technicien", bold=True)
    add_line(f"Nom : {technicien.user.username}")
    add_line(f"Email : {technicien.user.email}")
    add_line(f"Spécialité : {technicien.specialite}")
    add_line("")

    # 🔹 Chargement
    chargement = rapport.chargement
    add_line("🚛 Chargement", bold=True)
    add_line(f"Date : {chargement.date}")
    add_line(f"Logisticien nom: {chargement.logisticien.user.username}")
    add_line(f"Logisticien telephone: {chargement.logisticien.telephone}")
    add_line(f"Poids estimé : {chargement.poids_estime} kg")
    add_line("Contenu réel :")
    for k, v in chargement.contenu_reel.items():
        add_line(f"  - {k} : {v}")

    # 🔹 Demande collecte
    # demande = chargement.demande_collecte_detail
    demande = chargement.demande_collecte

    add_line("")
    add_line("📦 Demande de collecte", bold=True)
    add_line(f"Date souhaitée : {demande.date_souhaitee_client}")
    add_line(f"Statut : {demande.statut}")
    add_line(f"Client ID : {demande.client}")
    add_line("Contenu déclaré :")
    for k, v in demande.contenu_declare.items():
        add_line(f"  - {k} : {v}")

    # # 🔹 Manager
    # manager = demande.manager
    # add_line("")
    # add_line("🧑‍💼 Manager", bold=True)
    # add_line(f"Nom : {manager['user']['username']}")
    # add_line(f"Email : {manager['user']['email']}")

    # 🔹 Déchets
    add_line("")
    add_line("♻️ Déchets triés", bold=True)
    # for dechet in rapport.dechets:
    #     add_line(
    #         f"- {dechet['type_dechet']} x{dechet['quantite']} ({dechet['poids']} kg)"
    #     )
    # Déchets
    dechets = rapport.dechets

    total_global = 0.0

    for dechet in dechets:
        type_dechet = dechet.get('type_dechet', 'Inconnu')
        mode_valo = dechet.get('mode_valorisation', 'par_piece')
        prix_unitaire = float(dechet.get('prix_unitaire', 0))
        quantite = int(dechet.get('quantite', 0))
        poids = float(dechet.get('poids', 0))

        if mode_valo == 'par_kg':
            valeur_totale = prix_unitaire * poids
            unit = f"{poids} kg"
        else:  # par_piece par défaut
            valeur_totale = prix_unitaire * quantite
            unit = f"{quantite} pièces"

        total_global += valeur_totale

        add_line(
            f"- {type_dechet} | {unit} | "
            f"Mode: {mode_valo.replace('_', ' ')} | "
            f"Prix unitaire: {prix_unitaire:.2f} € | "
            f"Total: {valeur_totale:.2f} €"
        )

        add_line("")
        add_line(f"💰 Valeur totale des déchets : {total_global:.2f} €", bold=True)
    c.save()
    return chemin_relatif


class RapportViewSet(viewsets.ModelViewSet):
    queryset = Rapport.objects.all()
    serializer_class = RapportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Vérifie si l'utilisateur appartient au groupe 'Client'
        if user.groups.filter(name='Client').exists():
            if hasattr(user, 'client_profile') and user.client_profile is not None:
                # Filtrer les rapports pour ce client uniquement
                return Rapport.objects.filter(
                    chargement__demande_collecte__client=user.client_profile
                )
            else:
                raise PermissionDenied("Client non trouvé pour cet utilisateur.")
        
        # Pour les autres groupes (Manager, Technicien, etc), renvoyer tous les rapports
        return Rapport.objects.all()

    def perform_create(self, serializer):
        user = self.request.user

        if not hasattr(user, "technicien_profile"):
            raise PermissionDenied("Seul un technicien peut créer un rapport.")

        # Créer d'abord le rapport avec le technicien lié
        rapport = serializer.save(trie_par=user.technicien_profile)

        # Générer le PDF
        chemin_pdf = generer_pdf_rapport(rapport)

        # Mettre à jour le champ chemin_pdf
        rapport.chemin_pdf = chemin_pdf
        rapport.save()

    def update(self, request, *args, **kwargs):
        # Récupérer le rapport à modifier
        rapport = self.get_object()
        user = request.user

        # Vérifier que seul un manager peut valider
        # Ici on suppose is_staff comme manager, adapte selon ton modèle de rôle
        if "valide_par_manager" in request.data or "valide_par" in request.data:
            if not user.groups.filter(name="Manager").exists():
                raise PermissionDenied("Seul un manager peut valider un rapport.")

            # Si tu as un champ ForeignKey valide_par
            if "valide_par" in request.data:
                rapport.valide_par = user

            # Marquer la validation
            rapport.valide_par_manager = True

            # Enregistrer date validation si tu as ce champ
            if hasattr(rapport, "validated_at"):
                rapport.validated_at = timezone.now()

            rapport.save()

            serializer = self.get_serializer(rapport)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Sinon comportement update normal (par exemple modification autre que validation)
        return super().update(request, *args, **kwargs)


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
    permission_classes = [IsAuthenticated, IsLogisticienOrManager]

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
from  account.models  import Client,Vehicule, Entreprise,Logisticien,Manager , Technicien
from rest_framework.views import APIView 
class DashboardCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Cas ADMIN (superuser ou groupe Admin)
        if user.is_superuser or user.groups.filter(name="Admin").exists():
            return Response({
                "total_demandes": DemandeCollecte.objects.count(),
                "total_chargements": Chargement.objects.count(),
                "total_rapports": Rapport.objects.count(),
            })

        # Cas MANAGER
        elif user.groups.filter(name="Manager").exists():
            try:
                manager = user.manager_profile
            except Manager.DoesNotExist:
                raise PermissionDenied("Profil manager introuvable.")

            return Response({
                "total_demandes": DemandeCollecte.objects.filter(validee_par=manager).count(),
                "total_chargements": Chargement.objects.filter(demande_collecte__validee_par=manager).count(),
                "total_rapports": Rapport.objects.filter(chargement__demande_collecte__validee_par=manager).count(),
            })

        # Cas LOGISTICIEN
        elif user.groups.filter(name="Logisticien").exists():
            try:
                logisticien = user.logisticien_profile
            except Logisticien.DoesNotExist:
                raise PermissionDenied("Profil logisticien introuvable.")

            return Response({
                "total_demandes": DemandeCollecte.objects.filter(chargement__logisticien=logisticien).distinct().count(),
                "total_chargements": Chargement.objects.filter(logisticien=logisticien).count(),
                "total_rapports": Rapport.objects.filter(chargement__logisticien=logisticien).count(),
            })

        # Cas TECHNICIEN
        elif user.groups.filter(name="Technicien").exists():
            try:
                technicien = user.technicien_profile
            except Technicien.DoesNotExist:
                raise PermissionDenied("Profil technicien introuvable.")

            return Response({
                "total_demandes": 0,
                "total_chargements": 0,
                "total_rapports": Rapport.objects.filter(trie_par=technicien).count(),
            })

        # Autres rôles : interdit
        raise PermissionDenied("Rôle non autorisé.")
    
