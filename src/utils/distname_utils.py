def distName_to_dict(distName):
    """
    Convert a distName string to a dictionary.
    Example: "PLMN-PLMN1/ENodeB-1234/LTECell-5678" -> {"PLMN": "PLMN1", "ENodeB": "1234", "LTECell": "5678"}
    """
    result = {}
    parts = distName.split("/")
    for part in parts:
        if "-" in part:
            key, value = part.split("-", 1)
            result[key] = value
    return result