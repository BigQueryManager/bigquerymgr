from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class QueryProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    def __repr__(self):
        """."""
        return """
        user: {}
    """.format(self.user)
