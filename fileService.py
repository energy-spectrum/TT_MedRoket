import os
from pathlib import Path
import datetime
import itertools

from user import User

def fillDocument(file, user: User):
    file.write(f'# Отчёт для {user.companyName}\n')

    dateTimeNow = datetime.datetime.now()
    file.write(f'{user.name} <{user.email}> {dateTimeNow.strftime("%Y-%m-%d %H:%M:%S")}\n')
    file.write(f'Всего задач: {user.getTotalTasks()}\n')

    file.write('\n')

    file.write(f'## Актуальные задачи ({len(user.currentTasks)}):\n')
    for currentTask in user.currentTasks.values():
        file.write(f'-{currentTask}\n')
    
    file.write('\n')

    file.write(f'## Завершённые задачи ({len(user.completedTasks)}):')
    for currentTask in user.completedTasks.values():
        file.write(f'\n-{currentTask}')

    return dateTimeNow

def newPathToFile(pathToFile: Path) -> Path:
    if not pathToFile.exists():
        return pathToFile

    for i in itertools.count(1):
        newPath = pathToFile.parent / f'{pathToFile.stem}({i}){pathToFile.suffix}'
        if not os.path.isfile(newPath):
            return newPath  

def saveDocument(pathToNewFile: Path, pathToFile: Path, pathToDirToSave: Path, user: User):
    if pathToNewFile.name != pathToFile.name:
        lastDateTimeSaveDocument = user.lastDateTimeSaveDocument.strftime('%Y-%m-%d %H_%M').replace(' ', 'T', 1)
        oldFileName = f'old_{user.username}_{lastDateTimeSaveDocument}.txt'

        oldPathToFile = pathToDirToSave / oldFileName
        oldPathToFile = newPathToFile(oldPathToFile)

        os.rename(str(pathToFile), str(oldPathToFile))
        os.rename(str(pathToNewFile), str(pathToFile))

def makeDocument(user: User, pathToDirToSave: Path):
    fileName = f'{user.username}.txt'
    pathToFile = pathToDirToSave / fileName

    if pathToFile.exists():
        pathToNewFile = pathToDirToSave / f'actual_{fileName}'
    else:
        pathToNewFile = Path(pathToFile)

    with open(pathToNewFile, 'w', encoding="utf-8") as file:
        try:
            dateTimeFillingIn = fillDocument(file, user)
            file.close()
            saveDocument(pathToNewFile, pathToFile, pathToDirToSave, user)
            user.lastDateTimeSaveDocument = dateTimeFillingIn
        except Exception as e:
            file.close()
            os.remove(str(pathToNewFile))