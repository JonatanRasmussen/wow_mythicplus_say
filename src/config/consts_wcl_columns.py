class WclColumnConsts:
    # Wcl searchpage column names
    SEARCHPAGE_GUID = "GUID"
    SEARCHPAGE_DESCRIPTION = "Description"  # DO NOT CHANGE, Wcl website const
    SEARCHPAGE_GUILD = "Guild"              # DO NOT CHANGE, Wcl website const
    SEARCHPAGE_OWNER = "Owner"              # DO NOT CHANGE, Wcl website const
    SEARCHPAGE_VISIBILITY = "Visibility"    # DO NOT CHANGE, Wcl website const
    SEARCHPAGE_UPLOADED = "Uploaded"        # DO NOT CHANGE, Wcl website const
    SEARCHPAGE_DURATION = "Duration"        # DO NOT CHANGE, Wcl website const
    UPLOADED_AS_EPOCH = "UploadedAsEpoch"
    UPLOADED_AS_DATETIME = "UploadedAsDateTime"
    DURATION_AS_EPOCH = "DurationAsEpoch"
    DURATION_AS_TIME = "DurationAsTime"

    # WclFight dataclass column names
    FIGHT_LOG_GUID = "log_guid"
    FIGHT_ID = "fight_id"
    FIGHT_OUTCOME = "outcome"
    FIGHT_DURATION = "duration"
    FIGHT_DURATION_IN_SEC = "duration_in_sec"
    FIGHT_WCL_BOSS_ID = "wcl_boss_id"
    FIGHT_BOSS_TEXT = "boss_text"
    FIGHT_ZONE_NAME = "zone_name"
    FIGHT_BOSS_LEVEL = "boss_level"
    FIGHT_AFFIX_ICON = "affix_icon"
    FIGHT_TIME = "fight_time"

    # WclFight dataclass column values
    FIGHT_OUTCOME_KILL = "kill"
    FIGHT_OUTCOME_WIPE = "wipe"
