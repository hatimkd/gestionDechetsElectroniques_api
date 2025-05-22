from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User








# ===============================
# Utilisateur personnalisé
# ===============================


# ===============================
# Entreprise
# ===============================

class Entreprise(models.Model):
    """
    Modèle représentant une entreprise cliente.
    """
    nom = models.CharField(max_length=100, verbose_name="Nom de l'entreprise")
    adresse = models.CharField(max_length=255, verbose_name="Adresse du siège")
    
    ice = models.CharField(max_length=15, unique=True, verbose_name="ICE", help_text="Identifiant Commun de l'Entreprise (15 chiffres)")
    
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


# ===============================
# Véhicule
# ===============================

class Vehicule(models.Model):
    """
    Modèle représentant un véhicule utilisé pour les livraisons.
    """
    nom = models.CharField(max_length=100, verbose_name="Nom du véhicule")
    marque = models.CharField(max_length=100)
    poids = models.FloatField(help_text="Poids en kilogrammes")
    disponibilite = models.BooleanField(default=True, verbose_name="Disponible")

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
        ordering = ["marque", "nom"]

    def __str__(self):
        return f"{self.marque} - {self.nom}"


# ===============================
# Rôles liés aux utilisateurs
# ===============================

class Manager(models.Model):
    """
    Responsable ou administrateur de l'application.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manager_profile")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Manager"
        verbose_name_plural = "Managers"

    def __str__(self):
        return f"Manager: {self.user.username}"


class Client(models.Model):
    """
    Client associé à une entreprise.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name="clients")
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"Client: {self.user.username}"


class Technicien(models.Model):
    """
    
    Technicien chargé des interventions techniques.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="technicien_profile")
    specialite = models.CharField(max_length=100, verbose_name="Spécialité")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Technicien"
        verbose_name_plural = "Techniciens"

    def __str__(self):
        return f"Technicien: {self.user.username}"


class Logisticien(models.Model):
    """
    Logisticien assigné à un véhicule.
    """
    
    
    telephone = models.CharField(max_length=20)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="logisticien_profile")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name="logisticiens")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Logisticien"
        verbose_name_plural = "Logisticiens"
        

    def __str__(self):
        return f"Logisticien: {self.user.username}"
