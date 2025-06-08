
# signals.py
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from account.models import (
    Client, Manager, Technicien, Logisticien, Entreprise, Vehicule
)


from .models import   DemandeCollecte, Chargement, Dechet, Rapport
def create_group_with_permissions(group_name, permissions_list):
    """
    Fonction utilitaire pour créer un groupe avec ses permissions
    """
    group, created = Group.objects.get_or_create(name=group_name)
    
    for codename, name, model in permissions_list:
        content_type = ContentType.objects.get_for_model(model)
        permission, perm_created = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type,
        )
        group.permissions.add(permission)
    
    return group


@receiver(post_migrate)
def setup_groups_and_permissions(sender, **kwargs):
    """
    Signal exécuté après les migrations pour créer les groupes et permissions
    """
    
    # Permissions pour chaque groupe
    client_permissions = [
        # ('view_demandecollecte', 'Can view DemandeCollecte', DemandeCollecte),
        # ('add_demandecollecte', 'Can add DemandeCollecte', DemandeCollecte),
        # ('change_demandecollecte', 'Can change own DemandeCollecte', DemandeCollecte),
        # ('view_entreprise', 'Can view own Entreprise', Entreprise),
    ]
    
    manager_permissions = [
    #     ('view_demandecollecte', 'Can view DemandeCollecte', DemandeCollecte),
    #     ('change_demandecollecte', 'Can change DemandeCollecte', DemandeCollecte),
    #     ('delete_demandecollecte', 'Can delete DemandeCollecte', DemandeCollecte),
    #     ('view_chargement', 'Can view Chargement', Chargement),
    #     ('add_chargement', 'Can add Chargement', Chargement),
    #     ('change_chargement', 'Can change Chargement', Chargement),
    #     ('view_rapport', 'Can view Rapport', Rapport),
    #     ('add_rapport', 'Can add Rapport', Rapport),
    #     ('view_client', 'Can view Client', Client),
    #     ('view_entreprise', 'Can view Entreprise', Entreprise),
    #     ('view_vehicule', 'Can view Vehicule', Vehicule),
    ]
    
    technicien_permissions = [
        # ('view_demandecollecte', 'Can view DemandeCollecte', DemandeCollecte),
        # ('view_chargement', 'Can view Chargement', Chargement),
        # ('view_dechet', 'Can view Dechet', Dechet),
        # ('add_dechet', 'Can add Dechet', Dechet),
        # ('change_dechet', 'Can change Dechet', Dechet),
        # ('view_rapport', 'Can view Rapport', Rapport),
        # ('add_rapport', 'Can add Rapport', Rapport),
    ]
    
    logisticien_permissions = [
        # ('view_demandecollecte', 'Can view DemandeCollecte for chargement', DemandeCollecte),
        # ('view_chargement', 'Can view Chargement', Chargement),
        # ('add_chargement', 'Can add Chargement', Chargement),
        # ('change_chargement', 'Can change Chargement', Chargement),
        # ('delete_chargement', 'Can delete Chargement', Chargement),
        # ('view_vehicule', 'Can view Vehicule', Vehicule),
    ]
    
    admin_permissions = [
        # Toutes les permissions pour tous les modèles
        # ('view_demandecollecte', 'Can view DemandeCollecte', DemandeCollecte),
        # ('add_demandecollecte', 'Can add DemandeCollecte', DemandeCollecte),
        # ('change_demandecollecte', 'Can change DemandeCollecte', DemandeCollecte),
        # ('delete_demandecollecte', 'Can delete DemandeCollecte', DemandeCollecte),
        # ('view_chargement', 'Can view Chargement', Chargement),
        # ('add_chargement', 'Can add Chargement', Chargement),
        # ('change_chargement', 'Can change Chargement', Chargement),
        # ('delete_chargement', 'Can delete Chargement', Chargement),
        # ('view_dechet', 'Can view Dechet', Dechet),
        # ('add_dechet', 'Can add Dechet', Dechet),
        # ('change_dechet', 'Can change Dechet', Dechet),
        # ('delete_dechet', 'Can delete Dechet', Dechet),
        # ('view_rapport', 'Can view Rapport', Rapport),
        # ('add_rapport', 'Can add Rapport', Rapport),
        # ('change_rapport', 'Can change Rapport', Rapport),
        # ('delete_rapport', 'Can delete Rapport', Rapport),
        # ('view_client', 'Can view Client', Client),
        # ('add_client', 'Can add Client', Client),
        # ('change_client', 'Can change Client', Client),
        # ('delete_client', 'Can delete Client', Client),
        # ('view_manager', 'Can view Manager', Manager),
        # ('add_manager', 'Can add Manager', Manager),
        # ('change_manager', 'Can change Manager', Manager),
        # ('delete_manager', 'Can delete Manager', Manager),
        # ('view_technicien', 'Can view Technicien', Technicien),
        # ('add_technicien', 'Can add Technicien', Technicien),
        # ('change_technicien', 'Can change Technicien', Technicien),
        # ('delete_technicien', 'Can delete Technicien', Technicien),
        # ('view_logisticien', 'Can view Logisticien', Logisticien),
        # ('add_logisticien', 'Can add Logisticien', Logisticien),
        # ('change_logisticien', 'Can change Logisticien', Logisticien),
        # ('delete_logisticien', 'Can delete Logisticien', Logisticien),
        # ('view_entreprise', 'Can view Entreprise', Entreprise),
        # ('add_entreprise', 'Can add Entreprise', Entreprise),
        # ('change_entreprise', 'Can change Entreprise', Entreprise),
        # ('delete_entreprise', 'Can delete Entreprise', Entreprise),
        # ('view_vehicule', 'Can view Vehicule', Vehicule),
        # ('add_vehicule', 'Can add Vehicule', Vehicule),
        # ('change_vehicule', 'Can change Vehicule', Vehicule),
        # ('delete_vehicule', 'Can delete Vehicule', Vehicule),
    ]
    
    # # Création des groupes avec leurs permissions
    # create_group_with_permissions('Client', client_permissions)
    # create_group_with_permissions('Manager', manager_permissions)
    # create_group_with_permissions('Technicien', technicien_permissions)
    # create_group_with_permissions('Logisticien', logisticien_permissions)
    # create_group_with_permissions('Admin', admin_permissions)


# ========================================
# SIGNAUX POUR ASSIGNMENT AUTOMATIQUE
# ========================================

@receiver(post_save, sender=Client)
def assign_client_to_group(sender, instance, created, **kwargs):
    """
    Assigne automatiquement un client au groupe 'Client' lors de sa création
    """
    if created:
        try:
            group = Group.objects.get(name='Client')
            instance.user.groups.clear()  # Supprimer autres groupes
            instance.user.groups.add(group)
            print(f"✅ Utilisateur {instance.user.username} assigné au groupe Client")
        except Group.DoesNotExist:
            print("❌ Groupe 'Client' n'existe pas")


@receiver(post_save, sender=Manager)
def assign_manager_to_group(sender, instance, created, **kwargs):
    """
    Assigne automatiquement un manager au groupe 'Manager' lors de sa création
    """
    if created:
        try:
            group = Group.objects.get(name='Manager')
            instance.user.groups.clear()
            instance.user.groups.add(group)
            print(f"✅ Utilisateur {instance.user.username} assigné au groupe Manager")
        except Group.DoesNotExist:
            print("❌ Groupe 'Manager' n'existe pas")


@receiver(post_save, sender=Technicien)
def assign_technicien_to_group(sender, instance, created, **kwargs):
    """
    Assigne automatiquement un technicien au groupe 'Technicien' lors de sa création
    """
    if created:
        try:
            group = Group.objects.get(name='Technicien')
            instance.user.groups.clear()
            instance.user.groups.add(group)
            print(f"✅ Utilisateur {instance.user.username} assigné au groupe Technicien")
        except Group.DoesNotExist:
            print("❌ Groupe 'Technicien' n'existe pas")


@receiver(post_save, sender=Logisticien)
def assign_logisticien_to_group(sender, instance, created, **kwargs):
    """
    Assigne automatiquement un logisticien au groupe 'Logisticien' lors de sa création
    """
    if created:
        try:
            group = Group.objects.get(name='Logisticien')
            instance.user.groups.clear()
            instance.user.groups.add(group)
            print(f"✅ Utilisateur {instance.user.username} assigné au groupe Logisticien")
        except Group.DoesNotExist:
            print("❌ Groupe 'Logisticien' n'existe pas")


# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def get_user_role(user):
    """
    Détermine le rôle d'un utilisateur basé sur ses profils
    
    Returns:
        str: Le nom du rôle ('Client', 'Manager', 'Technicien', 'Logisticien', 'Admin', 'Unknown')
    """
    if hasattr(user, 'client_profile'):
        return 'Client'
    elif hasattr(user, 'manager_profile'):
        return 'Manager'
    elif hasattr(user, 'technicien_profile'):
        return 'Technicien'
    elif hasattr(user, 'logisticien_profile'):
        return 'Logisticien'
    elif user.is_superuser:
        return 'Admin'
    else:
        return 'Unknown'


def assign_user_to_correct_group(user):
    """
    Assigne un utilisateur au bon groupe basé sur son profil
    Utile pour corriger des assignations ou pour des utilisateurs existants
    """
    role = get_user_role(user)
    
    if role != 'Unknown':
        try:
            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)
            print(f"✅ Utilisateur {user.username} assigné au groupe {role}")
            return True
        except Group.DoesNotExist:
            print(f"❌ Groupe '{role}' n'existe pas")
            return False
    else:
        print(f"❌ Impossible de déterminer le rôle de {user.username}")
        return False


def bulk_assign_all_users():
    """
    Assigne tous les utilisateurs existants à leurs groupes corrects
    Utile lors de la première configuration ou pour corriger les assignations
    """
    users = User.objects.all()
    success_count = 0
    
    for user in users:
        if assign_user_to_correct_group(user):
            success_count += 1
    
    print(f"✅ {success_count}/{users.count()} utilisateurs assignés avec succès")


def create_admin_user(username, email, password):
    """
    Crée un utilisateur admin avec tous les privilèges
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    
    try:
        admin_group = Group.objects.get(name='Admin')
        user.groups.add(admin_group)
        print(f"✅ Admin {username} créé avec succès")
        return user
    except Group.DoesNotExist:
        print("❌ Groupe 'Admin' n'existe pas")
        return user


# ========================================
# EXEMPLE D'UTILISATION DANS VOS VUES
# ========================================

def check_user_permissions_in_view(request):
    """
    Exemple de vérification des permissions dans une vue
    """
    user = request.user
    role = get_user_role(user)
    
    if role == 'Client':
        # Logique pour les clients
        pass
    elif role == 'Manager':
        # Logique pour les managers
        pass
    elif role == 'Technicien':
        # Logique pour les techniciens
        pass
    elif role == 'Logisticien':
        # Logique pour les logisticiens
        pass
    elif role == 'Admin':
        # Accès complet
        pass
    else:
        # Accès refusé
        pass


# ========================================
# COMMANDES DJANGO MANAGEMENT
# ========================================

"""
# Créer un fichier management/commands/setup_groups.py

from django.core.management.base import BaseCommand
from myapp.signals import bulk_assign_all_users

class Command(BaseCommand):
    help = 'Assigne tous les utilisateurs à leurs groupes corrects'
    
    def handle(self, *args, **options):
        bulk_assign_all_users()
        self.stdout.write(
            self.style.SUCCESS('Assignation des groupes terminée avec succès')
        )
"""