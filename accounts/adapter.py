from allauth.account.adapter import DefaultAccountAdapter


class NoUsernameAccountAdapter(DefaultAccountAdapter):
    def populate_username(self, request, user):
        """
        Override allauth's default behavior of requiring a username.
        Since our CustomUser has no username field, we just skip this.
        """
        user.username = None
