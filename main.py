import os
from pathlib import Path
import json  

import requests

from user import User
from fileService import makeDocument

with open('config.json', 'r') as configFile:
    configData = json.load(configFile)

URL_TO_TASKS = configData["urlToTasks"] 
tasks = requests.get(URL_TO_TASKS)
if tasks.status_code // 100 == 2:
    tasks = tasks.json()
else:
    print(f'Erorr conectiong to {URL_TO_TASKS}:', tasks.status_code)
    exit()

URL_TO_USERS = configData["urlToUsers"] 
usersData = requests.get(URL_TO_USERS)
if usersData.status_code // 100 == 2:
    usersData = usersData.json()
else:
    print(f'Erorr conectiong to {URL_TO_USERS}:', usersData.status_code)
    exit()

pathToDirToSave = Path(configData["nameDirToSave"])
#Create folder "tasks"
if not pathToDirToSave.exists():
    pathToDirToSave.mkdir()

users = dict()
for userData in usersData:
    newUser = User(userData['id'], userData['name'], userData['username'], 
                   userData['email'], userData['company']['name'])
    users[userData['id']] = newUser

for task in tasks:
    default = False

    userId = task.get('userId', default)
    taskId = task.get('id', default)
    title = task.get('title', default)
    completed = task.get('completed', default)

    if default in (userId, taskId, title, completed):
        continue

    user = users.get(userId, default)
    if user != default:
        users[userId].addOrUpdateTask(taskId, title, completed)
        makeDocument(users[userId], pathToDirToSave)