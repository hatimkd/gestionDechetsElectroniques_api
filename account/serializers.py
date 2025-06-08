from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Manager, Client, Technicien, Logisticien, Vehicule, Entreprise


from collecte.models import DemandeCollecte, Chargement, Dechet, Rapport


class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def create_user(self, validated_data):
        return User.objects.create_user(
            username=validated_data.pop("username"),
            password=validated_data.pop("password"),
            email=validated_data.pop("email"),
        )


class AdminClientCreateSerializer(BaseUserSerializer):
    adresse = serializers.CharField()
    telephone = serializers.CharField()
    entreprise = serializers.PrimaryKeyRelatedField(queryset=Entreprise.objects.all())

    def create(self, validated_data):
        user = self.create_user(validated_data)
        return Client.objects.create(user=user, **validated_data)


class AdminTechnicienCreateSerializer(BaseUserSerializer):
    specialite = serializers.CharField()

    def create(self, validated_data):
        user = self.create_user(validated_data)
        return Technicien.objects.create(user=user, **validated_data)


class AdminLogisticienCreateSerializer(BaseUserSerializer):
    telephone = serializers.CharField()
    vehicule = serializers.PrimaryKeyRelatedField(queryset=Vehicule.objects.all())

    def create(self, validated_data):
        user = self.create_user(validated_data)
        return Logisticien.objects.create(user=user, **validated_data)


class AdminManagerCreateSerializer(BaseUserSerializer):
    def create(self, validated_data):
        user = self.create_user(validated_data)
        return Manager.objects.create(user=user)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Vérifier si l'utilisateur est actif
        if not user.is_active:
            raise serializers.ValidationError("Compte désactivé.")

        # Rôle et validation d'entreprise
        role = None
        if hasattr(user, "manager_profile"):
            role = "manager"
        elif hasattr(user, "client_profile"):
            if not user.client_profile.entreprise.is_active:
                raise serializers.ValidationError("Entreprise désactivée.")
            role = "client"
        elif hasattr(user, "technicien_profile"):
            role = "technicien"
        elif hasattr(user, "logisticien_profile"):
            role = "logisticien"
        elif user.is_superuser:
            role = "admin"
        else:
            raise serializers.ValidationError("Rôle utilisateur inconnu.")

        data["user"] = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": role,
        }

        return data


class ClientRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    entreprise_nom = serializers.CharField()
    entreprise_adresse = serializers.CharField()
    entreprise_ice = serializers.CharField()
    entreprise_telephone = serializers.CharField()

    def create(self, validated_data):
        entreprise = Entreprise.objects.create(
            nom=validated_data["entreprise_nom"],
            adresse=validated_data["entreprise_adresse"],
            ice=validated_data["entreprise_ice"],
            telephone=validated_data["entreprise_telephone"],
            is_active=False,  # En attente de validation
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False,  # En attente de validation
        )

        Client.objects.create(
            user=user,
            entreprise=entreprise,
            adresse=entreprise.adresse,
            telephone=entreprise.telephone,
            is_active=False,
        )

        return user


class AdminValidateSerializer(serializers.Serializer):
    is_active = serializers.BooleanField()


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ManagerSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)

    class Meta:
        model = Manager
        fields = ["user"]  # ou les champs que tu souhaites exposer


class VehiculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicule
        fields = "__all__"


# class ClientSerializer(serializers.ModelSerializer):
#     user = User(read_only=True)
#     entreprise = Entreprise(read_only=True)

#     class Meta:
#         model = Client
#         fields = [
#             'id',
#             'user',
#             'entreprise',
#             'adresse',
#             'telephone',
#             'is_active',
#             'affiliation',
#             'informations'
#         ]


class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = "__all__"


class ClientListSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)
    entreprise = (
        serializers.StringRelatedField()
    )  # ou un serializer complet si tu veux plus de détails

    class Meta:
        model = Client
        fields = ["id", "user", "entreprise", "adresse", "telephone", "is_active"]

class LogisticienSerializers(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)

    class Meta:
        model = Logisticien
        fields = '__all__'  # Inclut automatiquement user + tous les champs du modèle



class TechnicienSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(
        read_only=True
    )  # Sérialisation imbriquée de l'utilisateur lié

    class Meta:
        model = Technicien
        fields = "__all__"  # chaîne de caractères, pas liste !
        fields_only = ["user"]
