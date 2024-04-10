from .config import Config
from .misskey_api import *
from .logger import *
import datetime
import time
import sys

class EmojiBot:

    # 初期化処理
    def __init__(self, config_dict):
        self.config = Config(config_dict)
        self.api = MisskeyApi(self.config.host, self.config.token)
        self.logger = Logger()
        self.logger.log("emojibot initializing...")
        # ユーザー情報を取得
        try:
            self.user = self.api.show_user()
        except BadApiRequestException as e:
            self.logger.log(f"{datetime.datetime.today()}, show_user failure", color = Color.RED)
            print(e)
            self.logger.log("initialize failure", color = Color.RED)
            sys.exit(1)
        self.logger.log(f"{datetime.datetime.today()}, show_user success", color = Color.GREEN)
        # visible_user_ids を取得
        self.visible_user_ids = []
        for username in self.config.visible_usernames:
            try:
                user = self.api.search_user_by_username(username)
            except BadApiRequestException as e:
                print(e)
                self.logger.log("initialize failure", color = Color.RED)
                sys.exit(1)
            self.visible_user_ids.append(user.id)
        # 最新のモデレーションログの id を取得
        try:
            moderation_logs = self.api.show_moderation_logs(limit = 1)
        except BadApiRequestException as e:
            print(e)
            self.logger.log("initialize failure", color = Color.RED)
            sys.exit(1)
        self.logger.log(f"{datetime.datetime.today()}, show_moderation_logs success", color = Color.GREEN)
        self.sinceId = moderation_logs[0].id if len(moderation_logs) >= 1 else None
        self.logger.log("initialize success")

    def run(self):
        self.logger.log("emojibot start")
        while True:
            self._run()
            time.sleep(self.config.running_interval_seconds)

    def _run(self): 
        if self.sinceId is None:
            try:
                moderation_logs = self.api.show_moderation_logs(limit=self.config.moderation_logs_limit)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, show_moderation_logs failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, show_moderation_logs success", color = Color.GREEN)
            if len(moderation_logs) == 0:
                self.logger.log("no moderationlog.")
                return None
            # sinceId を指定しなかった場合はログが新しい順になっているので古い順に変える
            moderation_logs.reverse()
        else:
            try:
                moderation_logs = self.api.show_moderation_logs(limit=self.config.moderation_logs_limit, sinceId=self.sinceId)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, show_moderation_logs failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, show_moderation_logs success", color = Color.GREEN)
            if len(moderation_logs) == 0:
                self.logger.log("no moderationlog.")
                return None

        # since_id を更新する
        self.sinceId = moderation_logs[-1].id

        # 最新のモデレーションログが見つかった場合は古い順で通知する
        for ml in moderation_logs:
            if ml.type == 'addCustomEmoji':
                emoji = CustomEmoji(ml.info["emoji"])
                self.create_emoji_note(
                    emoji = emoji,
                    moderation_log = ml,
                    message_header = self.config.messages.emoji_add,
                    message_user = self.config.messages.emoji_add_user,
                    visibility = self.config.visibility.add,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.add,
                    use_mention = self.config.use_mention,
                    is_delete = False
                )
            elif ml.type == 'updateCustomEmoji':
                emoji = CustomEmoji(ml.info["after"])
                self.create_emoji_note(
                    emoji = emoji,
                    moderation_log = ml,
                    message_header = self.config.messages.emoji_update,
                    message_user = self.config.messages.emoji_update_user,
                    visibility = self.config.visibility.update,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.update,
                    use_mention = self.config.use_mention,
                    is_delete = False
                )
            elif ml.type == 'deleteCustomEmoji':
                emoji = CustomEmoji(ml.info["emoji"])
                self.create_emoji_note(
                    emoji = emoji,
                    moderation_log = ml,
                    message_header = self.config.messages.emoji_delete,
                    message_user = self.config.messages.emoji_delete_user,
                    visibility = self.config.visibility.delete,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.delete,
                    use_mention = self.config.use_mention,
                    is_delete = True
                )
            elif ml.type == 'createAvatarDecoration':
                decoration = AvatorDecoration(ml.info["avatarDecoration"])
                self.create_decoration_note(
                    decoration = decoration,
                    moderation_log = ml,
                    message_header = self.config.messages.decoration_add,
                    message_user = self.config.messages.decoration_add_user,
                    visibility = self.config.visibility.add,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.add,
                    use_mention = self.config.use_mention,
                    is_delete = False
                )
            elif ml.type == 'updateAvatarDecoration':
                decoration = AvatorDecoration(ml.info["after"])
                self.create_decoration_note(
                    decoration = decoration,
                    moderation_log = ml,
                    message_header = self.config.messages.decoration_update,
                    message_user = self.config.messages.decoration_update_user,
                    visibility = self.config.visibility.update,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.update,
                    use_mention = self.config.use_mention,
                    is_delete = False
                )
            elif ml.type == 'deleteAvatarDecoration':
                decoration = AvatorDecoration(ml.info["avatarDecoration"])
                self.create_decoration_note(
                    decoration = decoration,
                    moderation_log = ml,
                    message_header = self.config.messages.decoration_delete,
                    message_user = self.config.messages.decoration_delete_user,
                    visibility = self.config.visibility.delete,
                    visible_usernames = self.config.visible_usernames,
                    visible_user_ids = self.visible_user_ids,
                    local_only = self.config.local_only,
                    reaction_acceptance = self.config.reaction_acceptance,
                    use_cw = self.config.use_cw.delete,
                    use_mention = self.config.use_mention,
                    is_delete = True
                )


    def create_emoji_note(self, emoji, moderation_log, message_header, message_user, visibility, visible_usernames, visible_user_ids, local_only, reaction_acceptance, use_cw, use_mention, is_delete = False):
        header_mention = ""
        if visibility == "specified":
            for username in visible_usernames:
                header_mention = header_mention + "@" + username + " "
        footer_mention = ""
        if use_mention and moderation_log.user.username not in visible_usernames:
            footer_mention = f"{message_user}:@{moderation_log.user.username}"
        else:
            footer_mention = f"{message_user}:`@{moderation_log.user.username}`"
        if not is_delete:
            if use_cw:
                cw = f"{message_header} :{emoji.name}:"
                header = f"{header_mention}"
            else:
                cw = None
                header = f"{header_mention}\n{message_header} :{emoji.name}:\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `:{emoji.name}:`\n" \
                    f"category    : `{emoji.category}`\n" \
                    f"tags        : `{emoji.aliases}`\n" \
                    f"license     : `{emoji.license}`\n" \
                    f"isSensitive : `{emoji.isSensitive}`\n" \
                    f"localOnly   : `{emoji.localOnly}`\n\n" \
                    f"{footer_mention}" \
                    "</small>"
        else :
            if use_cw:
                cw = f"{message_header}"
                header = f"{header_mention}"
            else:
                cw = None
                header = f"{header_mention}\n{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `:{emoji.name}:`\n" \
                    f"{footer_mention}" \
                    "</small>"
        if self.config.is_dry_run:
            # dry_run のときは投稿しない
            self.logger.log("not posting due to dry run")
            self.logger.log(text, color = Color.CYAN)
        else:
            try:
                self.api.create_note(text, cw = cw, visibility = visibility, visibleUserIds = visible_user_ids, localOnly = local_only, reactionAcceptance = reaction_acceptance)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, create_note failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, create_note success", color = Color.GREEN)

    def create_decoration_note(self, decoration, moderation_log, message_header, message_user, visibility, visible_usernames, visible_user_ids, local_only, reaction_acceptance, use_cw, use_mention, is_delete = False):
        header_mention = ""
        if visibility == "specified":
            for username in visible_usernames:
                header_mention = header_mention + "@" + username + " "
        footer_mention = ""
        if use_mention and moderation_log.user.username not in visible_usernames:
            footer_mention = f"{message_user}:@{moderation_log.user.username}"
        else:
            footer_mention = f"{message_user}:`@{moderation_log.user.username}`"
        if not is_delete:
            if use_cw:
                cw = f"{message_header} : `{decoration.name}`"
                header = f"{header_mention}"
            else:
                cw = None
                header = f"{header_mention}\n{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `{decoration.name}`\n" \
                    f"url         : {decoration.url}\n" \
                    f"description : `{decoration.description}`\n" \
                    f"{footer_mention}" \
                    "</small>"
        else :
            if use_cw:
                cw = f"{message_header}"
                header = f"{header_mention}"
            else:
                cw = None
                header = f"{header_mention}\n{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `{decoration.name}`\n" \
                    f"{footer_mention}" \
                    "</small>"
        if self.config.is_dry_run:
            # dry_run のときは投稿しない
            self.logger.log("not posting due to dry run")
            self.logger.log(text, color = Color.CYAN)
        else:
            try:
                self.api.create_note(text, cw = cw, visibility = visibility, visibleUserIds = visible_user_ids, localOnly = local_only, reactionAcceptance = reaction_acceptance)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, create_note failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, create_note success", color = Color.GREEN)

