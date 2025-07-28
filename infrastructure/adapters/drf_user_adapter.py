class DRFUserAdapter:
    def __init__(self, user_entity):
        self._user = user_entity

    @property
    def id(self):
        return self._user.id

    @property
    def username(self):
        return self._user.username

    @property
    def email(self):
        return self._user.email.value if hasattr(self._user.email, 'value') else self._user.email

    @property
    def role_id(self):
        return self._user.role_id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.username