from social_core.backends.google import GoogleOAuth2
from social_core.utils import handle_http_errors
from six.moves.urllib_parse import urlencode, unquote
import time


class CustomGoogle(GoogleOAuth2):
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token'),
        ('expires_in', 'expires'),
        ('access_type', 'access_type'),
        ('token_type', 'token_type')
    ]

    def get_scope(self):
        scope = super(CustomGoogle, self).get_scope()
        scope = scope + ['https://www.googleapis.com/auth/bigquery']
        return scope

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        """Return default extra data to store in extra_data field"""
        # import pdb; pdb.set_trace()
        data = {
            # store the last time authentication toke place
            'auth_time': int(time.time())
        }
        extra_data_entries = []
        if self.GET_ALL_EXTRA_DATA or self.setting('GET_ALL_EXTRA_DATA', False):
            extra_data_entries = response.keys()
        else:
            extra_data_entries = (self.EXTRA_DATA or []) + self.setting('EXTRA_DATA', [])
        for entry in extra_data_entries:
            if not isinstance(entry, (list, tuple)):
                entry = (entry,)
            size = len(entry)
            if size >= 1 and size <= 3:
                if size == 3:
                    name, alias, discard = entry
                elif size == 2:
                    (name, alias), discard = entry, False
                elif size == 1:
                    name = alias = entry[0]
                    discard = False
                value = response.get(name) or details.get(name)
                if discard and not value:
                    continue
                data[alias] = value
        # import pdb; pdb.set_trace()
        return data

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        # import pdb; pdb.set_trace()
        self.process_error(self.data)
        state = self.validate_state()

        response = self.request_access_token(
            self.access_token_url(),
            data=self.auth_complete_params(state),
            headers=self.auth_headers(),
            auth=self.auth_complete_credentials(),
            method=self.ACCESS_TOKEN_METHOD
        )
        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def auth_params(self, state=None):
        # import pdb; pdb.set_trace()
        client_id, client_secret = self.get_key_and_secret()
        params = {
            'client_id': client_id,
            'redirect_uri': self.get_redirect_uri(state)
        }
        if self.STATE_PARAMETER and state:
            params['state'] = state
        if self.RESPONSE_TYPE:
            params['response_type'] = self.RESPONSE_TYPE
        return params

    def auth_url(self):
        """Return redirect url"""
        state = self.get_or_create_state()
        params = self.auth_params(state)
        params.update(self.get_scope_argument())
        params.update(self.auth_extra_arguments())
        params = urlencode(params)
        if not self.REDIRECT_STATE:
            # redirect_uri matching is strictly enforced, so match the
            # providers value exactly.
            params = unquote(params)
        # import pdb; pdb.set_trace()
        return '{0}?{1}'.format(self.authorization_url(), params)

    def refresh_token_params(self, token, *args, **kwargs):
        client_id, client_secret = self.get_key_and_secret()
        return {
            'refresh_token': token,
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret
        }

    def process_refresh_token_response(self, response, *args, **kwargs):
        return response.json()

    def refresh_token(self, token, *args, **kwargs):
        # import pdb; pdb.set_trace()
        params = self.refresh_token_params(token, *args, **kwargs)
        url = self.refresh_token_url()
        method = self.REFRESH_TOKEN_METHOD
        key = 'params' if method == 'GET' else 'data'
        request_args = {'headers': self.auth_headers(),
                        'method': method,
                        key: params}
        request = self.request(url, **request_args)
        return self.process_refresh_token_response(request, *args, **kwargs)

    def refresh_token_url(self):
        return self.REFRESH_TOKEN_URL or self.access_token_url()