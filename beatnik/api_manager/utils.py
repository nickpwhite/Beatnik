class Utils:
    @classmethod
    def dict_find(cls, d, key):
        if key in d:
            return d[key]
        for k, v in d.items():
            if isinstance(v, dict):
                item = cls.dict_find(v, key)
                if item is not None:
                    return item

        return None
