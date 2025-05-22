from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from collecte.models import DemandeCollecte, Chargement, Dechet, Rapport


class Command(BaseCommand):
    help = "Crée les rôles et permissions personnalisées pour l'application de collecte."

    def handle(self, *args, **kwargs):
        # Définir les permissions personnalisées à associer à chaque rôle
        roles_permissions = {
            "Client": [
                "add_demandecollecte", "view_demandecollecte",
            ],
            "Manager": [
                "change_demandecollecte", "view_demandecollecte",
                "can_validate_demande", "can_view_all_demandes",
                "can_validate_rapport"
            ],
            "Logisticien": [
                "add_chargement", "view_chargement",
                "can_assign_logisticien"
            ],
            "Technicien": [
                "add_dechet", "view_dechet", 
                "can_declare_dechets", "can_validate_dechets",
                "add_rapport", "view_rapport", 
                "can_generate_pdf"
            ]
        }

        # Création ou mise à jour des groupes
        for role_name, perm_codenames in roles_permissions.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Groupe '{role_name}' créé."))
            else:
                self.stdout.write(f"ℹ️ Groupe '{role_name}' déjà existant.")

            # Ajout des permissions
            for codename in perm_codenames:
                try:
                    permission = Permission.objects.get(codename=codename)
                    group.permissions.add(permission)
                    self.stdout.write(f"  ➕ Permission '{codename}' ajoutée au groupe '{role_name}'.")
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"  ⚠️ Permission '{codename}' introuvable. Assure-toi qu'elle est bien définie dans les modèles ou via une migration."))

        self.stdout.write(self.style.SUCCESS("🎉 Tous les groupes et permissions ont été configurés avec succès."))
