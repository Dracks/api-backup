
parsers = {}

def register_parser(c):
    if isinstance(c, str):
        def l(cls):
            parsers[c] = cls
            return cls
        return l
    else :
        name = c.__name__.replace('Parser', '').lower()
        parsers[name] = c
        return c