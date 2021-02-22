class Message:
    def __init__(self, task: str, is_completed: bool):
        self.task = task
        self.is_task_completed = is_completed

    def get_task(self) -> str:
        return self.task

    def is_completed(self) -> bool:
        return self.is_task_completed
