# # # from django.db.models.signals import post_save
# # # from django.dispatch import receiver
# # # from django.contrib.auth.models import Group
# # # from django.contrib.auth.models import User
# # # from .models import Client, Manager, Technicien, Logisticien
# # # from .models import DemandeCollecte, Chargement, Dechet, Rapport

# # # from django.contrib.auth.models import Group, Permission, User
# # # from django.contrib.contenttypes.models import ContentType

# # # # @receiver(post_save, sender=Client)
# # # # def assign_client_group(sender, instance, created, **kwargs):
# # # #     if created:
# # # #         group, _ = Group.objects.get_or_create(name="Client")
# # # #         instance.user.groups.add(group)

# # # # @receiver(post_save, sender=Manager)
# # # # def assign_manager_group(sender, instance, created, **kwargs):
# # # #     if created:
# # # #         group, _ = Group.objects.get_or_create(name="Manager")
# # # #         instance.user.groups.add(group)

# # # # @receiver(post_save, sender=Technicien)
# # # # def assign_technicien_group(sender, instance, created, **kwargs):
# # # #     if created:
# # # #         group, _ = Group.objects.get_or_create(name="Technicien")
# # # #         instance.user.groups.add(group)

# # # # @receiver(post_save, sender=Logisticien)
# # # # def assign_logisticien_group(sender, instance, created, **kwargs):
# # # #     if created:
# # # #         group, _ = Group.objects.get_or_create(name="Logisticien")
# # # #         instance.user.groups.add(group)
# # # # @receiver(post_save, sender=User)
# # # # def assign_group_based_on_profile(sender, instance, created, **kwargs):
# # # #     if created:
# # # #         if hasattr(instance, 'client'):
# # # #             group, _ = Group.objects.get_or_create(name="Client")
# # # #             instance.groups.add(group)
# # # #         elif hasattr(instance, 'manager'):
# # # #             group, _ = Group.objects.get_or_create(name="Manager")
# # # #             instance.groups.add(group)
# # # #         elif hasattr(instance, 'technicien'):
# # # #             group, _ = Group.objects.get_or_create(name="Technicien")
# # # #             instance.groups.add(group)
# # # #         elif hasattr(instance, 'logisticien'):
# # # #             group, _ = Group.objects.get_or_create(name="Logisticien")
# # # #             instance.groups.add(group)
# # # def add_permission_to_group(group_name, permission_codename, model):
# # #     group, _ = Group.objects.get_or_create(name=group_name)
# # #     content_type = ContentType.objects.get_for_model(model)
# # #     permission = Permission.objects.get(codename=permission_codename, content_type=content_type)
# # #     group.permissions.add(permission)

# # # @receiver(post_save, sender=Client)
# # # def assign_client_group(sender, instance, created, **kwargs):
# # #     if created:
# # #         group, _ = Group.objects.get_or_create(name="Client")
# # #         instance.user.groups.add(group)
# # #         add_permission_to_group("Client", "view_demandecollecte", DemandeCollecte)

# # # @receiver(post_save, sender=Manager)
# # # def assign_manager_group(sender, instance, created, **kwargs):
# # #     if created:
# # #         group, _ = Group.objects.get_or_create(name="Manager")
# # #         instance.user.groups.add(group)
# # #         add_permission_to_group("Manager", "view_demandecollecte", DemandeCollecte)

# # # @receiver(post_save, sender=Manager)
# # # def assign_logisticien_group(sender, instance, created, **kwargs):
# # #     if created:
# # #         group, _ = Group.objects.get_or_create(name="Logisticien")
# # #         instance.user.groups.add(group)
# # #         add_permission_to_group("Logisticien", "view_demandecollecte", DemandeCollecte)


# # from django.db.models.signals import post_migrate
# # from django.dispatch import receiver
# # from django.contrib.auth.models import Group, Permission
# # from django.contrib.contenttypes.models import ContentType
# # from .models import DemandeCollecte  # Remplacez par votre modèle réel

# # # Signal exécuté après les migrations
# # @receiver(post_migrate)
# # def create_logisticien_group(sender, **kwargs):
# #     # Créer ou récupérer le groupe 'Logisticien'
# #     group, created = Group.objects.get_or_create(name='Logisticien')

# #     # Créer le ContentType pour DemandeCollecte
# #     content_type = ContentType.objects.get_for_model(DemandeCollecte)

# #     # Créer ou récupérer la permission 'can_viewcollecte'
# #     permission, created = Permission.objects.get_or_create(
# #         codename='view_demandecollecte',
# #         name='View DemandeCollecte for chargement',
# #         content_type=content_type,
# #     )

# #     # Ajouter la permission au groupe
# #     group.permissions.add(permission)

# #     # Ajouter un utilisateur par défaut (si nécessaire) ou gérer autrement
# #     # user = User.objects.get(username='nom_utilisateur')  # Ajoutez ici la logique si vous voulez ajouter un utilisateur spécifique
# #     # user.groups.add(group)



# from django.db.models.signals import post_migrate
# from django.dispatch import receiver
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType
# from .models import DemandeCollecte  # Remplacez par votre modèle réel

# # Signal exécuté après les migrations
# @receiver(post_migrate)
# def create_logisticien_group(sender, **kwargs):
#     # Créer ou récupérer le groupe 'Logisticien'
#     group, created = Group.objects.get_or_create(name='Logisticien')

#     # Créer le ContentType pour DemandeCollecte
#     content_type = ContentType.objects.get_for_model(DemandeCollecte)

#     # Supprimer l'ancienne permission 'can_viewcollecte' si elle existe
#     try:
#         old_permission = Permission.objects.get(codename='can_viewcollecte', content_type=content_type)
#         old_permission.delete()
#     except Permission.DoesNotExist:
#         pass  # La permission n'existait pas, on continue

#     # Vérifier si la permission 'view_demandecollecte' existe déjà
#     permission = Permission.objects.filter(
#         codename='view_demandecollecte',
#         content_type=content_type
#     ).first()

#     if not permission:
#         # Si la permission n'existe pas, la créer
#         permission = Permission.objects.create(
#             codename='view_demandecollecte',
#             name='Can view DemandeCollecte for chargement',
#             content_type=content_type,
#         )

#     # Ajouter la permission au groupe
#     group.permissions.add(permission)



from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType
from .models import DemandeCollecte  # Remplacez 'yourapp' par le nom réel de votre application

# Signal exécuté après les migrations
@receiver(post_migrate)
def create_logisticien_and_manager_groups(sender, **kwargs):
    # Créer ou récupérer les groupes 'Logisticien' et 'Manager'
    logisticien_group, created = Group.objects.get_or_create(name='Logisticien')
    manager_group, created = Group.objects.get_or_create(name='Manager')

    # Créer le ContentType pour le modèle DemandeCollecte
    content_type = ContentType.objects.get_for_model(DemandeCollecte)

    # Créer ou récupérer la permission 'view_demandecollecteacharger'
    permission, created = Permission.objects.get_or_create(
        codename='view_demandecollecteacharger',
        name='Can view DemandeCollecte for chargement',
        content_type=content_type,
    )

    # Ajouter la permission aux groupes 'Logisticien' et 'Manager'
    logisticien_group.permissions.add(permission)
    manager_group.permissions.add(permission)

    
