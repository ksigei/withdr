from allauth.account.adapter import DefaultAccountAdapter


class NoUsernameAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        # Prevent allauth from trying to set a username
        user.username = None
