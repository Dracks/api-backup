

class RestCookie:
    def __init__(self, models, config):
        self.model = models.get(config.get('model'))
        self.data = {
            'login': config.get('user'),
            'password': config.get('password')
        }
        self.authenticated = False

    def authenticate(self):
        data = self.model.create(self.data)
        if not data.get('is_authenticated'):
            raise Exception("Bad credentials")
        self.authenticated = True
