import os
from pathlib import Path
import datetime
import itertools

from user import User


def make_doc(user: User, path_dir_to_save: Path):
    filename = f'{user.username}.txt'
    path_file = path_dir_to_save / filename

    if path_file.exists():
        path_newfile = path_dir_to_save / f'actual_{filename}'
    else:
        path_newfile = Path(path_file)

    with open(path_newfile, 'w', encoding="utf-8") as file:
        try:
            datetime_filling_in = fill_doc(file, user)
            file.close()
            save_doc(path_newfile, path_file, path_dir_to_save, user)
            user.last_datetime_save_doc = datetime_filling_in
        except Exception as e:
            print(e)
            file.close()
            os.remove(str(path_newfile))


def fill_doc(file, user: User):
    file.write(f'# Отчёт для {user.company_name}\n')

    datetime_now = datetime.datetime.now()
    strfdatetime = datetime_now.strftime("%Y-%m-%d %H:%M:%S")
    file.write(f'{user.name} <{user.email}> {strfdatetime}\n')

    file.write(f'Всего задач: {user.get_total_tasks()}\n')

    file.write('\n')

    file.write(f'## Актуальные задачи ({len(user.current_tasks)}):\n')
    for task in user.current_tasks.values():
        file.write(f'-{task}\n')

    file.write('\n')

    file.write(f'## Завершённые задачи ({len(user.completed_tasks)}):')
    for task in user.completed_tasks.values():
        file.write(f'\n-{task}')

    return datetime_now


def save_doc(path_newfile: Path, path_file: Path,
             path_dir_to_save: Path, user: User):
    if path_newfile.name != path_file.name:
        strflast_datetime_save_doc = user.last_datetime_save_doc.strftime('%Y-%m-%d %H_%M')
        last_datetime_save_doc = strflast_datetime_save_doc.replace(' ', 'T', 1)
        newname_oldfile = f'old_{user.username}_{last_datetime_save_doc}.txt'

        newpath_to_oldfile = path_dir_to_save / newname_oldfile
        newpath_to_oldfile = get_newpath_file(newpath_to_oldfile)

        os.rename(str(path_file), str(newpath_to_oldfile))
        os.rename(str(path_newfile), str(path_file))


def get_newpath_file(path_file: Path) -> Path:
    if not path_file.exists():
        return path_file

    for i in itertools.count(1):
        newpath = path_file.parent / f'{path_file.stem}({i}){path_file.suffix}'
        if not newpath.exists():
            return newpath
