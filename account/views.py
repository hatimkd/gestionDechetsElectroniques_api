

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ClientRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, VehiculeSerializer




from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser




from .models  import Client,Vehicule

from rest_framework import status

from .serializers import (
    AdminClientCreateSerializer,
    AdminTechnicienCreateSerializer,
    AdminLogisticienCreateSerializer,
    AdminManagerCreateSerializer,
    
    AdminValidateSerializer
)


from django.shortcuts import get_object_or_404

class AdminCreateClientView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminClientCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Client créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateTechnicienView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminTechnicienCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Technicien créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateLogisticienView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminLogisticienCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Logisticien créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateManagerView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = AdminManagerCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Manager créé avec succès"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ClientRegisterView(APIView):
    def post(self, request):
        serializer = ClientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Désactiver le compte en attendant la validation admin
            user.is_active = False
            user.save()

            return Response(
                {"message": "Inscription réussie. En attente de validation par un administrateur."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    



class AdminValidateClientView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        """
        Active simultanément :
        - le client (Client.is_active)
        - l'utilisateur lié (User.is_active)
        - l'entreprise liée (Entreprise.is_active)
        """
        client = get_object_or_404(Client, pk=pk)

        # On attend dans le body { "is_active": true } ou false
        serializer = AdminValidateSerializer(client, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Activation du client
        client.is_active = serializer.validated_data['is_active']
        client.save()

        # Activation de l'utilisateur Django
        user = client.user
        user.is_active = client.is_active
        user.save()

        # Activation de l'entreprise
        entreprise = client.entreprise
        entreprise.is_active = client.is_active
        entreprise.save()

        return Response(
            {"message": f"Client, utilisateur et entreprise {'activés' if client.is_active else 'désactivés'}."},
            status=status.HTTP_200_OK
        )
        
    
from rest_framework.permissions import IsAuthenticated






class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        role = None

        if hasattr(user, 'client_profile'):
            role = 'client'
        elif hasattr(user, 'manager_profile'):
            role = 'manager'
        elif hasattr(user, 'technicien_profile'):
            role = 'technicien'
        elif hasattr(user, 'logisticien_profile'):
            role = 'logisticien'
        else:
            role = 'admin' if user.is_staff else 'user'

        return Response({
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "role": role,
            "permissions": list(user.get_all_permissions()),
        })



class VehiculeViewSet(viewsets.ModelViewSet):
    serializer_class = VehiculeSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Vehicule.objects.none()

        if user.is_staff or getattr(user, 'role', None) == 'admin':
            return Vehicule.objects.all()

        # Sinon, accès refusé
        return Vehicule.objects.none()