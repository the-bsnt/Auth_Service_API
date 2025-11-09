from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()


# custom backend logic to authenticate user via both email and username
class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # fetching user by user name or email. Here, i used user term "username" as user_identifier (it can take both email or username)
        try:
            lookup = Q(username__iexact=username) | Q(email__iexact=username)
            user = User.objects.get(lookup)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None
