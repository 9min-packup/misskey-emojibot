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
                    emoji,
                    ml,
                    self.config.messages.emoji_add,
                    self.config.messages.emoji_add_user,
                    self.config.visibility.add,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.add
                )
            elif ml.type == 'updateCustomEmoji':
                emoji = CustomEmoji(ml.info["after"])
                self.create_emoji_note(
                    emoji,
                    ml,
                    self.config.messages.emoji_update,
                    self.config.messages.emoji_update_user,
                    self.config.visibility.update,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.update
                )
            elif ml.type == 'deleteCustomEmoji':
                emoji = CustomEmoji(ml.info["emoji"])
                self.create_emoji_note(
                    emoji,
                    ml,
                    self.config.messages.emoji_delete,
                    self.config.messages.emoji_delete_user,
                    self.config.visibility.delete,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.delete,
                    True
                )
            elif ml.type == 'createAvatarDecoration':
                decoration = AvatorDecoration(ml.info["avatarDecoration"])
                self.create_decoration_note(
                    decoration,
                    ml,
                    self.config.messages.decoration_add,
                    self.config.messages.decoration_add_user,
                    self.config.visibility.add,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.add
                )
            elif ml.type == 'updateAvatarDecoration':
                decoration = AvatorDecoration(ml.info["after"])
                self.create_decoration_note(
                    decoration,
                    ml,
                    self.config.messages.decoration_update,
                    self.config.messages.decoration_update_user,
                    self.config.visibility.update,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.update
                )
            elif ml.type == 'deleteAvatarDecoration':
                decoration = AvatorDecoration(ml.info["avatarDecoration"])
                self.create_decoration_note(
                    decoration,
                    ml,
                    self.config.messages.decoration_delete,
                    self.config.messages.decoration_delete_user,
                    self.config.visibility.delete,
                    self.config.local_only,
                    self.config.reaction_acceptance,
                    self.config.use_cw.delete,
                    True
                )


    def create_emoji_note(self, emoji, moderation_log, message_header, message_user, visibility, local_only, reaction_acceptance, use_cw, is_delete=False):
        if not is_delete:
            if use_cw:
                cw = f"{message_header} :{emoji.name}:"
                header = ""
            else:
                cw = None
                header = f"{message_header} :{emoji.name}:\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `:{emoji.name}:`\n" \
                    f"category    : `{emoji.category}`\n" \
                    f"tags        : `{emoji.aliases}`\n" \
                    f"license     : `{emoji.license}`\n" \
                    f"isSensitive : `{emoji.isSensitive}`\n" \
                    f"localOnly   : `{emoji.localOnly}`\n\n" \
                    f"{message_user}:@{moderation_log.user.username}" \
                    "</small>"
        else :
            if use_cw:
                cw = f"{message_header}"
                header = ""
            else:
                cw = None
                header = f"{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `:{emoji.name}:`\n" \
                    f"{message_user}:@{moderation_log.user.username}" \
                    "</small>"
        if self.config.is_dry_run:
            # dry_run のときは投稿しない
            self.logger.log("not posting due to dry run")
            self.logger.log(text, color = Color.CYAN)
        else:
            try:
                self.api.create_note(text, cw = cw, visibility = visibility, localOnly = local_only, reactionAcceptance = reaction_acceptance)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, create_note failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, create_note success", color = Color.GREEN)

    def create_decoration_note(self, decoration, moderation_log, message_header, message_user, visibility, local_only, reaction_acceptance, use_cw, is_delete=False):
        if not is_delete:
            if use_cw:
                cw = f"{message_header} : `{decoration.name}`"
                header = ""
            else:
                cw = None
                header = f"{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `{decoration.name}`\n" \
                    f"url         : `{decoration.url}`\n" \
                    f"description : `{decoration.description}`\n" \
                    f"{message_user}:@{moderation_log.user.username}" \
                    "</small>"
        else :
            if use_cw:
                cw = f"{message_header}"
                header = ""
            else:
                cw = None
                header = f"{message_header}\n\n"
            text =  header + \
                    "<small>" \
                    f"name        : `{decoration.name}`\n" \
                    f"{message_user}:@{moderation_log.user.username}" \
                    "</small>"
        if self.config.is_dry_run:
            # dry_run のときは投稿しない
            self.logger.log("not posting due to dry run")
            self.logger.log(text, color = Color.CYAN)
        else:
            try:
                self.api.create_note(text, cw = cw, visibility = visibility, localOnly = local_only, reactionAcceptance = reaction_acceptance)
            except BadApiRequestException as e:
                self.logger.log(f"{datetime.datetime.today()}, create_note failure", color = Color.RED)
                print(e)
                return None
            self.logger.log(f"{datetime.datetime.today()}, create_note success", color = Color.GREEN)

