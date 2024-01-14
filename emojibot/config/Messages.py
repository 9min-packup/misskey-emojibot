class Messages:

    EMOJI_ADD = "新しい絵文字が追加されました。"
    EMOJI_ADD_USER = "追加したユーザー"
    EMOJI_UPDATE = "絵文字が更新されました。"
    EMOJI_UPDATE_USER = "更新したユーザー"
    EMOJI_DELETE = "絵文字が削除されました。"
    EMOJI_DELETE_USER = "削除したユーザー"
    DECORATION_ADD = "新しいアバターデコレーションが追加されました。"
    DECORATION_ADD_USER = "追加したユーザー"
    DECORATION_UPDATE = "アバターデコレーションが更新されました。"
    DECORATION_UPDATE_USER = "更新したユーザー"
    DECORATION_DELETE = "アバターデコレーションが削除されました。"
    DECORATION_DELETE_USER = "削除したユーザー"

    def __init__(self, dict):
        self.emoji_add = dict["emoji_add"] if "emoji_add" in dict else self.EMOJI_ADD
        self.emoji_add_user = dict["emoji_add_user"] if "emoji_add_user" in dict else self.EMOJI_ADD_USER
        self.emoji_update = dict["emoji_update"] if "emoji_update" in dict else self.EMOJI_UPDATE
        self.emoji_update_user = dict["emoji_update_user"] if "emoji_update_user" in dict else self.EMOJI_UPDATE_USER
        self.emoji_delete = dict["emoji_delete"] if "emoji_delete" in dict else self.EMOJI_DELETE
        self.emoji_delete_user = dict["emoji_delete_user"] if "emoji_delete_user" in dict else self.EMOJI_DELETE_USER
        self.decoration_add = dict["decoration_add"] if "decoration_add" in dict else self.DECORATION_ADD
        self.decoration_add_user = dict["decoration_add_user"] if "decoration_add_user" in dict else self.DECORATION_ADD_USER
        self.decoration_update = dict["decoration_update"] if "decoration_update" in dict else self.DECORATION_UPDATE
        self.decoration_update_user = dict["decoration_update_user"] if "decoration_update_user" in dict else self.DECORATION_DELETE_USER
        self.decoration_delete = dict["decoration_delete"] if "decoration_delete" in dict else self.DECORATION_DELETE
        self.decoration_delete_user = dict["decoration_delete_user"] if "decoration_delete_user" in dict else self.DECORATION_DELETE_USER