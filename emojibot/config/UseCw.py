class UseCw:

    USE_CW_ADD = True
    USE_CW_UPDATE = True
    USE_CW_DELETE = True

    def __init__(self, dict):
        self.add = dict["add"] if "add" in dict else self.USE_CW_ADD
        self.update = dict["update"] if "update" in dict else self.USE_CW_UPDATE
        self.delete = dict["delete"] if "delete" in dict else self.USE_CW_DELETE   