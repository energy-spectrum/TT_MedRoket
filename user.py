import datetime

DEFAULT_DATE_TIME = datetime.datetime(1, 1, 1)

class User():
    def __init__(self, id: int, name: str, username: str, email: str, companyName: str):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.companyName = companyName
        self.currentTasks = dict()
        self.completedTasks = dict()
        self.lastDateTimeSaveDocument = DEFAULT_DATE_TIME

    def addOrUpdateTask(self, taskId: int, title: str, completed: bool):
        print(title + '|stop')

        title = deleteLastSpaces(title)
        limitLenTitle = 46
        if len(title) > limitLenTitle:
            title = title[:limitLenTitle] + '...'

        default = False
        if completed:
            have = self.currentTasks.get(taskId, default)

            if have != default:
                self.currentTasks.pop(taskId)

            self.completedTasks[taskId] = title
        else:
            have = self.completedTasks.get(taskId, default)

            if have != default:
                self.completedTasks.pop(taskId)

            self.currentTasks[taskId] = title  

    def getTotalTasks(self):
        return len(self.currentTasks) + len(self.completedTasks)

def deleteLastSpaces(title):
    i = len(title)
    while i != 0:
        if title[i - 1] == ' ':
            i -= 1
        else:
            break

    return title[:i - 1]