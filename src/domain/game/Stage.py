from enum import Enum


class Stage(Enum):
    BOOT = "boot"
    START_CYCLE = "start_cycle"
    GO_TO_OHMMETER = "go_to_ohmmeter"
    FIND_COMMAND_PANEL = "find_command_panel"
    TRANSPORT_PUCK = "transport_puck"
    GO_PARK = "go_park"
    STOP = "stop"
    CYCLE_STARTED = "cycle_started"
    STAGE_COMPLETED = "stage_completed"
