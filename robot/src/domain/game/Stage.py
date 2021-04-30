from enum import Enum


class Stage(Enum):
    START_CYCLE = "start_cycle"
    GO_TO_OHMMETER = "go_to_ohmmeter"
    READ_COMMAND_PANEL = "read_command_panel"
    TRANSPORT_PUCK = "transport_puck"
    GO_PARK = "go_park"
    STOP = "stop"
    CYCLE_STARTED = "cycle_started"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
