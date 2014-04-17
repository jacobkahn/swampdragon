def login_required(func):
    def not_logged_in(self, **kwargs):
        self.send_login_required({'signin_required': 'you need to sign in'})
        return

    def check_user(self, **kwargs):
        user = self.connection.get_user()
        if user.is_anonymous():
            return not_logged_in(self, **kwargs)
        return func(self, **kwargs)
    return check_user


class RoutePermission(object):
    def test_permission(self, handler, verb, **kwargs):
        raise NotImplemented("You need to implement test_permission")

    def permission_failed(self, handler):
        raise NotImplemented("You need to implement permission_failed")


class LoginRequired(RoutePermission):
    def __init__(self, verbs=None):
        self.test_against_verbs = verbs

    def test_permission(self, handler, verb, **kwargs):
        if self.test_against_verbs:
            if verb not in self.test_against_verbs:
                return True
        user = handler.connection.get_user()
        return not user.is_anonymous()

    def permission_failed(self, handler):
        handler.send_login_required()
