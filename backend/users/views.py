from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User


@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at.isoformat() if user.created_at else None,
        }
        for user in users
    ]
    return Response(data)
