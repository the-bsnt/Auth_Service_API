from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


# customizing refresh token to add extra claims in token
class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        if not user.is_active:
            raise AuthenticationFailed("User is not active")
        token = super().for_user(user)
        token["email"] = user.email
        token["role"] = user.role
        return token
