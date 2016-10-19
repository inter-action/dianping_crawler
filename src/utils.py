

class StringUtils:
    @staticmethod
    def format(tpl, *values):
        result = tpl
        for value in values:
            result = result.replace("%s", str(value), 1)
        return result