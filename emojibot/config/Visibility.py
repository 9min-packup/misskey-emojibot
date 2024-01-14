class Visibility:

    VISIBILITY_ADD = "public"
    VISIBILITY_UPDATE = "home"
    VISIBILITY_DELETE = "home"

    def __init__(self, dict):
        self.add = dict["add"] if "add" in dict else self.VISIBILITY_ADD
        self.update = dict["update"] if "update" in dict else self.VISIBILITY_UPDATE
        self.delete = dict["delete"] if "delete" in dict else self.VISIBILITY_DELETE