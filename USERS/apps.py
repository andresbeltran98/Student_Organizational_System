from django.apps import AppConfig


# Set up the signaling of the Users class
class UsersConfig(AppConfig):
    name = 'USERS'

    def ready(self):
        import USERS.signals