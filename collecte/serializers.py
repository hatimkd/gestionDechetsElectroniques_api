from rest_framework import serializers
from .models import DemandeCollecte, Chargement, Dechet, Rapport
from account.serializers import ManagerSerializer 




from account.models import Logisticien  
class DemandeCollecteSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer(source='validee_par', read_only=True)
    
    class Meta:
        model = DemandeCollecte
        fields = [
            'id','uuid', 'date_souhaitee_client',
            'contenu_declare', 'poids_estime',
            'statut', 'client', 'validee_par',
            'manager'  # nouveau champ pour l'output
        ]
        read_only_fields = ['uuid', 'statut', 'validee_par']
        extra_kwargs = {
            'client': {'required': False}
        }

    def to_representation(self, instance):
        """
        Override pour ne jamais renvoyer 'validee_par' brut,
        et n'ajouter 'manager' que si validee_par n'est pas null.
        """
        data = super().to_representation(instance)
        # Supprime toujours le champ brut
        data.pop('validee_par', None)

        # Si pas validée, on n’ajoute pas 'manager'
        if instance.validee_par is None:
            data.pop('manager', None)
        return data
        
        
        # def perform_create(self, serializer):
        #     serializer.save(client=self.request.user)








class ChargementSerializer(serializers.ModelSerializer):
    # demande_collecte= DemandeCollecteSerializer()
    
    
    
    # demande_collecte = serializers.PrimaryKeyRelatedField(queryset=DemandeCollecte.objects.all())
    demande_collecte_detail = DemandeCollecteSerializer(source='demande_collecte', read_only=True)




    
    demande_collecte = serializers.PrimaryKeyRelatedField(
        queryset=DemandeCollecte.objects.filter(validee_par__isnull=False)
    )


    class Meta:
        model = Chargement
        fields = ['id','date','contenu_reel','poids_estime','demande_collecte', 'demande_collecte_detail']
        read_only_fields = ['id']

   
     
     
     
     
    def create(self, validated_data):
        # Récupérer l'utilisateur connecté via 'request' dans le contexte
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            
            # Vérifier si l'utilisateur connecté a un Logisticien
            try:
                logisticien = Logisticien.objects.get(user=user)
                validated_data['logisticien'] = logisticien
            except Logisticien.DoesNotExist:
                raise serializers.ValidationError("L'utilisateur connecté n'est pas un Logisticien.")
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
            raise serializers.ValidationError("Il existe déjà un chargement pour cette demande de collecte.")
        return value



class DechetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dechet
        fields = '__all__'


class RapportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rapport
        fields = '__all__'

