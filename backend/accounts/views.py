import os
from clerk import Clerk
from decouple import config
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile

# Initialize Clerk client only if the API key is available
clerk_secret_key = config("CLERK_SECRET_KEY", default=None)
clerk_client = Clerk(api_key=clerk_secret_key) if clerk_secret_key else None

@api_view(["GET"])
def protected_view(request):
    if not clerk_client:
        return Response(
            {"error": "Clerk client not configured"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return Response(
            {"error": "Authorization header missing"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = auth_header.replace("Bearer ", "")

    try:
        session = clerk_client.sessions.verify_session(token)
        clerk_user_id = session["user_id"]

        user = clerk_client.users.get_user(clerk_user_id)

        profile, created = UserProfile.objects.get_or_create(
            clerk_user_id=clerk_user_id,
            defaults={
                "email": user.email_addresses[0].email_address,
                "name": user.first_name or "",
            },
        )

        return Response(
            {
                "message": "Access granted",
                "user": {
                    "clerk_user_id": profile.clerk_user_id,
                    "email": profile.email,
                    "name": profile.name,
                },
            },
            status=status.HTTP_200_OK,
        )

    except Exception:
        return Response(
            {"error": "Invalid or expired token"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
