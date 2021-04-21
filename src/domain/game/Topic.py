from enum import Enum


class Topic(Enum):
    BOOT = "boot"
    START_CYCLE = "start cycle"
    CYCLE_COMPLETED = "cycle completed"
    START_STAGE = "start stage"
    STAGE_COMPLETED = "stage completed"
    MOVEMENTS = "movements"
    ROTATION = "rotation"
    GRAB_PUCK = "grab puck"
    DROP_PUCK = "drop puck"
    READ_RESISTANCE = "read resistance"
    ANALYZE_COMMAND_PANEL = "analyze command panel"
    TURN_LED_ON = "turn led on"
    ERROR = "error"
