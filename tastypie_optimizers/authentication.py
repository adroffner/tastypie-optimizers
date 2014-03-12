from tastypie.authentication import ApiKeyAuthentication
from tastypie.models import ApiKey
from tastypie.compat import User, username_field
from tastypie.http import HttpUnauthorized
from django.core.cache import get_cache

import logging

class CachedApiKeyAuthentication(ApiKeyAuthentication):
    """
    Handles API key auth, in which a user provides a username & API key.

    Caches the ApiKey & goes back to the database to refresh.
    Uses the ``ApiKey`` model that ships with tastypie in the DB.

    Overrides the ``get_key`` method to perform the key check
    to ask cache first.
    """

    def __init__(self, cache_name='default', ttl_seconds=60):
        super(CachedApiKeyAuthentication, self).__init__()
        try:
            self._cache = get_cache(cache_name)
            self._ttl_seconds = ttl_seconds
        except InvalidCacheBackendError:
            raise # TODO: handle this better.

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """

        try:
            username, api_key = self.extract_credentials(request)
        except ValueError:
            return self._unauthorized()

        if not username or not api_key:
            return self._unauthorized()

        # cache key=api_key, value=User-object
        user = self._cache.get(api_key)
        logging.error("cached ApiKey: %r value: %r==%r" % (api_key, user and user.username, user))
        if not user:
            try:
                lookup_kwargs = {username_field: username}
                user = User.objects.get(**lookup_kwargs)
                ApiKey.objects.get(user=user, key=api_key)
                self._cache.set(api_key, user, self._ttl_seconds)
            except (User.DoesNotExist, User.MultipleObjectsReturned,
                    ApiKey.DoesNotExist, ApiKey.MultipleObjectsReturned):
                return self._unauthorized()

        if user.username != username:
            return self._unauthorized()

        if not self.check_active(user):
            return False

        key_auth_check = self.get_key(user, api_key)
        if key_auth_check and not isinstance(key_auth_check, HttpUnauthorized):
            request.user = user

        return key_auth_check

    def get_key(self, user, api_key):
        """
        no-op; everything happens in is_authenticated.
        """
        return True

