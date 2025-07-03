from rest_framework import serializers
from .models import DemandeCollecte, Chargement, Dechet, Rapport
from account.serializers import ManagerSerializer, TechnicienSerializer,LogisticienSerializers


from account.models import Logisticien


class DemandeCollecteSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(source="validee_par", read_only=True)

    class Meta:
        model = DemandeCollecte
        fields = [
            "id",
            "uuid",
            "date_souhaitee_client",
            "contenu_declare",
            "poids_estime",
            "statut",
            "client",
            "validee_par",
            "manager",  # nouveau champ pour l'output
        ]
        read_only_fields = ["uuid", "statut", "validee_par"]
        extra_kwargs = {"client": {"required": False}}

    def to_representation(self, instance):
        """
        Override pour ne jamais renvoyer 'validee_par' brut,
        et n'ajouter 'manager' que si validee_par n'est pas null.
        """
        data = super().to_representation(instance)
        # Supprime toujours le champ brut
        data.pop("validee_par", None)

        # Si pas validée, on n’ajoute pas 'manager'
        if instance.validee_par is None:
            data.pop("manager", None)
        return data

        # def perform_create(self, serializer):
        #     serializer.save(client=self.request.user)


class ChargementSerializer(serializers.ModelSerializer):
    # demande_collecte= DemandeCollecteSerializer()

    # demande_collecte = serializers.PrimaryKeyRelatedField(queryset=DemandeCollecte.objects.all())
    demande_collecte_detail = DemandeCollecteSerializer(
        source="demande_collecte", read_only=True
    )

    demande_collecte = serializers.PrimaryKeyRelatedField(
        queryset=DemandeCollecte.objects.filter(validee_par__isnull=False)
    )

    # logisticien = LogisticienSerializers
    
    
    logisticien = LogisticienSerializers(read_only=True)  # serializer nested en lecture seule

    class Meta:
        model = Chargement
        fields = [
            "id",
            "date",
            "contenu_reel",
            "poids_estime",
            "demande_collecte",
            "demande_collecte_detail",
            "logisticien"
        ]
        read_only_fields = ["id","logisticien"]

    def create(self, validated_data):
        # Récupérer l'utilisateur connecté via 'request' dans le contexte
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

            # Vérifier si l'utilisateur connecté a un Logisticien
            try:
                logisticien = Logisticien.objects.get(user=user)
                validated_data["logisticien"] = logisticien
            except Logisticien.DoesNotExist:
                raise serializers.ValidationError(
                    "L'utilisateur connecté n'est pas un Logisticien."
                )
        else:
            raise serializers.ValidationError("L'utilisateur connecté est requis.")

            # Assurer que demande_collecte est un UUID valide
            # demande_collecte_id = validated_data.get('demande_collecte')
            # if isinstance(demande_collecte_id, str):  # Vérifie si c'est une chaîne
            #     try:
            #         demande_collecte = DemandeCollecte.objects.get(id=demande_collecte_id)
            #         validated_data['demande_collecte'] = demande_collecte
            #     except DemandeCollecte.DoesNotExist:
            #         raise serializers.ValidationError("DemandeCollecte avec cet ID n'existe pas.")

        return super().create(validated_data)

    def validate_demande_collecte(self, value):
        # Check if a Chargement already exists for the given DemandeCollecte
        if Chargement.objects.filter(demande_collecte=value).exists():
            raise serializers.ValidationError(
                "Il existe déjà un chargement pour cette demande de collecte."
            )
        return value


class DechetSerializer(serializers.ModelSerializer):
    declare_par = TechnicienSerializer(read_only=True)

     
     
     
     
    chargement = ChargementSerializer(read_only=True)
    chargement_id = serializers.PrimaryKeyRelatedField(
        queryset=Chargement.objects.all(),
        source='chargement',  # fait le lien avec le champ chargement du modèle
        write_only=True
    )

    class Meta:
        model = Dechet
        fields = "__all__"

        read_only_fields = [
            "declare_par"
        ]  # Important : empêche le front de devoir l'envoyer

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        if not hasattr(user, "technicien_profile"):
            raise serializers.ValidationError(
                "Cet utilisateur n'est pas un technicien."
            )

        validated_data["declare_par"] = user.technicien_profile
        return super().create(validated_data)


# class RapportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Rapport
#         fields = "__all__"



# from django.conf.urls.static import static


from django.conf import settings



class RapportSerializer(serializers.ModelSerializer):
    trie_par = TechnicienSerializer(read_only=True)
    chargement = ChargementSerializer(read_only=True)
    chargement_id = serializers.PrimaryKeyRelatedField(
        queryset=Chargement.objects.all(), write_only=True, source='chargement'
    )
    
    
    
    
    pdf_url = serializers.SerializerMethodField()


    class Meta:
        model = Rapport
        fields = [
            "id",
            "date",
            
                        'pdf_url',  # 🔹 lien absolu ici

            "poids_mesure",
            "chemin_pdf",
            "valide_par_manager",
            "chargement",       # lecture seule détaillée
            "chargement_id",    # pour l'envoi (écriture)
            "trie_par",
            "dechets",
        ]
        read_only_fields = ["trie_par","chemin_pdf"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        if not hasattr(user, "technicien_profile"):
            raise serializers.ValidationError("Seul un technicien peut créer un rapport.")

        validated_data["trie_par"] = user.technicien_profile
        return super().create(validated_data)

    
    
    
    def get_pdf_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(settings.MEDIA_URL + obj.chemin_pdf)
        return settings.MEDIA_URL + obj.chemin_pdf