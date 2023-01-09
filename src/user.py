import datetime

DEFAULT_DATETIME = datetime.datetime(1, 1, 1)


class User():
    def __init__(self, id: int, name: str, username: str, email: str,
                 company_name: str):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.company_name = company_name
        self.current_tasks = dict()
        self.completed_tasks = dict()
        self.last_datetime_save_doc = DEFAULT_DATETIME

    def add_or_update_task(self, task_id: int, title: str, completed: bool):
        title = format(title)

        default = False
        if completed:
            have = self.current_tasks.get(task_id, default)

            if have != default:
                self.current_tasks.pop(task_id)

            self.completed_tasks[task_id] = title
        else:
            have = self.completed_tasks.get(task_id, default)

            if have != default:
                self.completed_tasks.pop(task_id)

            self.current_tasks[task_id] = title

    def get_total_tasks(self):
        return len(self.current_tasks) + len(self.completed_tasks)


def delete_last_spaces(title):
    i = len(title)
    while i != 0:
        if title[i - 1] == ' ':
            i -= 1
        else:
            break

    return title[:i - 1]


def format(title):
    title = delete_last_spaces(title)

    limit_len_title = 46
    if len(title) > limit_len_title:
        title = title[:limit_len_title]
        title += '...'

    return title
