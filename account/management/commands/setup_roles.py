from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from account.models import Client, Manager, Technicien, Logisticien  # adapte selon ton app


# ========================================
# SETUP ROLE UTILITAIRE
# ========================================


from django.core.management.base import BaseCommand











class Command(BaseCommand):
    help = "Assigne tous les utilisateurs à leur groupe selon leur profil"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        count = 0
        for user in users:
            if assign_user_to_correct_group(user):
                count += 1
        self.stdout.write(self.style.SUCCESS(f"{count}/{users.count()} utilisateurs assignés avec succès."))
def setup_role(instance, role_name):
    """
    Assigne l'utilisateur lié à une instance à un groupe donné
    """
    try:
        group = Group.objects.get(name=role_name)
        instance.user.groups.clear()
        instance.user.groups.add(group)
        print(f"✅ Utilisateur {instance.user.username} assigné au groupe {role_name}")
    except Group.DoesNotExist:
        print(f"❌ Groupe '{role_name}' n'existe pas")


@receiver(post_save, sender=Client)
def assign_client(sender, instance, created, **kwargs):
    if created:
        setup_role(instance, 'Client')


@receiver(post_save, sender=Manager)
def assign_manager(sender, instance, created, **kwargs):
    if created:
        setup_role(instance, 'Manager')


@receiver(post_save, sender=Technicien)
def assign_technicien(sender, instance, created, **kwargs):
    if created:
        setup_role(instance, 'Technicien')


@receiver(post_save, sender=Logisticien)
def assign_logisticien(sender, instance, created, **kwargs):
    if created:
        setup_role(instance, 'Logisticien')


# ========================================
# FONCTIONS UTILITAIRES
# ========================================

def get_user_role(user):
    """
    Détermine le rôle d'un utilisateur basé sur ses profils
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
    Assigne un utilisateur à son groupe selon son profil
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
    Réassigne tous les utilisateurs existants à leurs groupes respectifs
    """
    users = User.objects.all()
    success = 0
    for user in users:
        if assign_user_to_correct_group(user):
            success += 1
    print(f"✅ {success}/{users.count()} utilisateurs assignés avec succès")


def create_admin_user(username, email, password):
    """
    Crée un superutilisateur et l'ajoute au groupe 'Admin' si existant
    """
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        is_staff=True,
        is_superuser=True
    )
    try:
        group = Group.objects.get(name='Admin')
        user.groups.add(group)
        print(f"✅ Admin {username} créé et assigné au groupe Admin")
    except Group.DoesNotExist:
        print("❌ Groupe 'Admin' n'existe pas")
    return user
