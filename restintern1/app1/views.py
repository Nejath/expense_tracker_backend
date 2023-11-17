

#CLASS BASED VIEWS WITH MIXINS

from app1.models import CustomUser
from app1.serializers import Userserializers,ChangePasswordSerializer
from rest_framework import generics,mixins
from rest_framework.permissions import IsAuthenticated
#from django.contrib.auth.models import User

class Userregistration(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=CustomUser.objects.all()
    serializer_class=Userserializers

    def get(self,request):
        return self.list(request)

    def post(self,request,*args,**kwargs):
        return self.create(request)


from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import update_session_auth_hash
from .serializers import ChangePasswordSerializer
from rest_framework.views import APIView

class change_password(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.method == 'POST':
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_password(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request, user)  # To update session after password change
                    return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
                return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

