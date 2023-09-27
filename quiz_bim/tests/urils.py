from functools import wraps

from django.contrib.auth import get_user_model


def login_superuser_test(test_func):
    @wraps(test_func)
    def wrapper(self, *args, **kwargs):
        # Log the client in
        self.client.force_login(self.superuser)

        try:
            # Execute the test function
            test_func(self, *args, **kwargs)
        finally:
            # Log the client out
            self.client.logout()

    return wrapper
