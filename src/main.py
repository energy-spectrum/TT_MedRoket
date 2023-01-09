from pathlib import Path
import json

import requests

from user import User
from file_service import make_doc

with open('src/config.json', 'r') as config_file:
    config_data = json.load(config_file)

URL_TO_TASKS = config_data["urlToTasks"]
tasks = requests.get(URL_TO_TASKS)
if tasks.status_code // 100 == 2:
    tasks = tasks.json()
else:
    print(f'Erorr conectiong to {URL_TO_TASKS}:', tasks.status_code)
    exit()

URL_TO_USERS = config_data["urlToUsers"]
users_data = requests.get(URL_TO_USERS)
if users_data.status_code // 100 == 2:
    users_data = users_data.json()
else:
    print(f'Erorr conectiong to {URL_TO_USERS}:', users_data.status_code)
    exit()

path_dir_to_save = Path(config_data["nameDirToSave"])
# Create folder "tasks"
if not path_dir_to_save.exists():
    path_dir_to_save.mkdir()

users = dict()
for user_data in users_data:
    new_user = User(user_data['id'], user_data['name'], user_data['username'],
                    user_data['email'], user_data['company']['name'])
    users[user_data['id']] = new_user

for task in tasks:
    default = -1

    user_id = task.get('userId', default)
    task_id = task.get('id', default)
    title = task.get('title', default)
    completed = task.get('completed', default)

    if default in (user_id, task_id, title, completed):
        continue

    user = users.get(user_id, default)
    if user != default:
        users[user_id].add_or_update_task(task_id, title, completed)
        make_doc(users[user_id], path_dir_to_save)
