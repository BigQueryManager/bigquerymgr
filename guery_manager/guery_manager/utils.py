from social_core.backends.google import GoogleOAuth2


class CustomGoogle(GoogleOAuth2):
    def get_scope(self):
        scope = super(CustomGoogle, self).get_scope()
        scope = scope + ['https://www.googleapis.com/auth/bigquery']
        return scope