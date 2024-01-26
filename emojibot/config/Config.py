from .Visibility import *
from .UseCw import *
from .Messages import *

class Config:
   
    NO_HOST = "host-is-not-defined"
    NO_TOKEN = "token-is-not-defined"
    IS_DRY_RUN = False
    MODERATION_LOGS_LIMIT = 5
    RUNNING_INTERVAL_SECONDS = 60
    LOCAL_ONLY = True
    REACTION_ACCEPTANCE = None

    def __init__(self, dict):
        self.host = dict["host"] if "host" in dict else self.NO_HOST
        self.token = dict["token"] if "token" in dict else self.NO_TOKEN
        self.is_dry_run = dict["is_dry_run"] if "is_dry_run" in dict else self.IS_DRY_RUN
        self.moderation_logs_limit = dict["moderation_logs_limit"] if "moderation_logs_limit" in dict else self.MODERATION_LOGS_LIMIT
        self.running_interval_seconds = dict["running_interval_seconds"] if "running_interval_seconds" in dict else self.RUNNING_INTERVAL_SECONDS
        self.visibility = Visibility(dict["visibility"]) if "visibility" in dict else Visibility({})
        self.use_cw = UseCw(dict["use_cw"]) if "use_cw" in dict else UseCw({})
        self.local_only = dict["local_only"] if "local_only" in dict else self.LOCAL_ONLY
        self.reaction_acceptance = dict["reaction_acceptance"] if "reaction_acceptance" in dict else self.REACTION_ACCEPTANCE
        self.messages = Messages(dict["messages"]) if "messages" in dict else Messages({})
      
