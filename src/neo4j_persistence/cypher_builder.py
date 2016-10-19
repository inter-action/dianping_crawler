
def build_placeholders(dict, prefix=""):
    rs = []
    for key in list(dict.keys()):
        if isinstance(key, str) is False:
            raise RuntimeError("invalid dict")
        other = prefix + key
        rs.append(key + ": {" + other + "}")

    return ", ".join(rs)


def prefix_dict(dict, prefix=""):
    if prefix == "":
        return dict
    else:
        result = {}
        for key in list(dict.keys()):
            if isinstance(key, str) is False:
                raise RuntimeError("invalid dict")
            result[prefix+key] = dict[key]
        return result
