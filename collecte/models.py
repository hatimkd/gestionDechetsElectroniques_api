
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

# À adapter selon ta structure
from account.models import Client, Manager , Logisticien, Technicien

class DemandeCollecte(models.Model):
    """Représente une demande de collecte effectuée par un client et validée par un manager."""

    class Statut(models.TextChoices):
        EN_ATTENTE = 'en_attente', _('En attente')
        VALIDEE = 'validee', _('Validée')
        REFUSEE = 'refusee', _('Refusée')

    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_souhaitee_client = models.DateField(verbose_name="Date souhaitée par le client")
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='demandes_collecte'
    )
    contenu_declare = models.JSONField(
        verbose_name="Contenu déclaré", help_text="Exemple : {'papier': 10, 'plastique': 5}"
    )
    poids_estime = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Poids estimé (kg)"
    )
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE
    )
    validee_par = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='demandes_validees'
    )

    class Meta:
        verbose_name = "Demande de collecte"
        verbose_name_plural = "Demandes de collecte"
        ordering = ['-date_souhaitee_client']

    def __str__(self):
        return f"Demande #{self.uuid} - {self.get_statut_display()}"

    def is_validee(self):
        return self.statut == self.Statut.VALIDEE
    
    
import uuid
from django.core.exceptions import ValidationError
class Chargement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    contenu_reel = models.JSONField()
    demande_collecte = models.ForeignKey(DemandeCollecte, on_delete=models.CASCADE, related_name='chargements')
    logisticien = models.ForeignKey(Logisticien, on_delete=models.CASCADE, related_name='chargements')
    poids_estime = models.FloatField()

    def __str__(self):
        return f"Chargement {self.id} du {self.date}"
    def clean(self):
        if self.poids_estime < 0:
            raise ValidationError("Le poids estimé ne peut pas être négatif.")
    def save(self, *args, **kwargs):
        # Vous pouvez ajouter une logique pour assigner automatiquement un logisticien, par exemple
        if not self.logisticien:
            # Assigner un logisticien par défaut ou basé sur la logique métier
            self.logisticien = get_default_logisticien()  # Assurez-vous que cette fonction existe
        super().save(*args, **kwargs)


from django.db import models
from django.utils.translation import gettext_lazy as _




class Dechet(models.Model):
    """Représente un déchet géré par un technicien."""

    class Etat(models.TextChoices):
        FONCTIONNEL = 'fonctionnel', _('Fonctionnel')
        HS = 'hors_service', _('Hors service')
        A_REPARER = 'a_reparer', _('À réparer')
        A_DEMANTELER = 'a_demanteler', _('À démanteler')

    class ModeValorisation(models.TextChoices):
        PAR_PIECE = 'par_piece', _('Par pièce')
        PAR_KG = 'par_kg', _('Par kg')
        AUTRE = 'autre', _('Autre')

    id = models.AutoField(
        primary_key=True,
        verbose_name="Identifiant"
    )
    type_dechet = models.CharField(
        max_length=100,
        verbose_name="Type de déchet",
        help_text='Ex. "serveur", "écran", etc.'
    )
    etat = models.CharField(
        max_length=20,
        choices=Etat.choices,
        default=Etat.FONCTIONNEL,
        verbose_name="État",
        help_text='Ex. "fonctionnel", "hors_service"'
    )
    quantite = models.PositiveIntegerField(
        verbose_name="Quantité",
        help_text="Nombre d’unités"
    )
    poids = models.FloatField(
        verbose_name="Poids total (kg)",
        help_text="Poids cumulé de toutes les unités"
    )
    mode_valorisation = models.CharField(
        max_length=20,
        choices=ModeValorisation.choices,
        default=ModeValorisation.PAR_PIECE,
        verbose_name="Mode de valorisation",
        help_text='Ex. "par_piece", "par_kg"'
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix unitaire (€)",
        help_text="Prix par unité ou par kg"
    )
    declare_par = models.ForeignKey(
          Technicien,
        on_delete=models.CASCADE,
        related_name='dechets_declares',
        verbose_name="Déclaré par"
    )

    class Meta:
        verbose_name = "Déchet"
        verbose_name_plural = "Déchets"
        ordering = ['type_dechet', 'etat']

    def __str__(self):
        return f"{self.type_dechet} ({self.quantite}×) – {self.get_etat_display()}"

    def valeur_totale(self) -> float:
        """
        Retourne la valeur totale : quantite * prix_unitaire.
        Ex. 3 × 25.0 = 75.0
        """
        return float(self.quantite) * float(self.prix_unitaire)
    
    

class Rapport(models.Model):
    # Date du rapport
    date = models.DateField(verbose_name="Date du rapport")
    
    # Poids mesuré (en kilogrammes, par exemple)
    poids_mesure = models.FloatField(verbose_name="Poids mesuré (kg)")

    # Chemin vers le fichier PDF généré
    chemin_pdf = models.CharField(max_length=255, verbose_name="Chemin du PDF")

    # Indique si le rapport a été validé par le manager
    valide_par_manager = models.BooleanField(default=False, verbose_name="Validé par le manager")

    # Lien vers le chargement associé à ce rapport
    chargement = models.ForeignKey(
        'Chargement', 
        on_delete=models.CASCADE, 
        related_name='rapports', 
        verbose_name="Chargement associé"
    )

    # Lien vers le technicien ayant trié les déchets
    trie_par = models.ForeignKey(
             Technicien, 
        on_delete=models.CASCADE, 
        related_name='rapports', 
        verbose_name="Technicien ayant trié"
    )

    # Lien vers le déchet associé au rapport
    dechets = models.JSONField(verbose_name="Détails des déchets triés")


    def __str__(self):
        """Retourne une représentation lisible de l'objet"""
        return f"Rapport du {self.date} - Poids: {self.poids_mesure} kg"

    class Meta:
        """Méthodes de configuration supplémentaires pour l'admin et la base de données"""
        verbose_name = "Rapport"
        verbose_name_plural = "Rapports"
        ordering = ['-date']  # Triez les rapports par date décroissante



