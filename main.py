from datetime import datetime, timedelta
import uuid
import sys


FILEPATH = "db.txt"
SEPARATOR = "<>"
STATUS_ACTIVE = "active"
STATUS_DONE = "done"
STATUS_OVERDUE = "overdue"


def read_database(filepath):
    raw_lines = []
    with open(filepath, "r", encoding="utf8") as file:
        for line in file.read().splitlines():
            raw_lines.append(line)
    return raw_lines



def parse_tasks(lines):
    tasks = []
    for line in lines:
        if line == "\n": continue
        tasks.append(line.split(SEPARATOR)[1:])
    return tasks


def print_readable(tasks):
    print("Актуальные задачи:")
    for index, task in enumerate(tasks, 1):
        print(f"{index}. {'✕' if task[-1] == STATUS_ACTIVE else '✓' if task[-1] == STATUS_DONE else '⌛'} {' '.join(task[:-1])}")


def make_new_task():
    task_name = ""
    date_complete = ""

    while True:
        task_name = input("Введите имя задачи: ").strip()
        if not task_name:
            print("Введите валидное имя задачи.")
            continue
        break
    
    while True:
        date_complete = input("Введите дату выполнения в формате ДД.ММ.ГГГГ или enter: ")
        if not date_complete:
            break
        try:
            datetime.strptime(date_complete, "%d.%m.%Y")
        except ValueError:
            print("Введите дату в правильном формате.")
            continue
        break
    
    print("Вы собираетесь создать задание с параметрами:")
    print(f" - Имя задачи: {task_name}")
    print(f" - Дата выполнения: [{date_complete if date_complete else 'не задана'}]")

    write_database(FILEPATH, task_name, date_complete, datetime.now())
    main_menu()

def complete_task():
    pass

def change_task_parameters():
    pass


def write_database(filepath, task_name, date_complete, timestamp):
    with open(filepath, "a", encoding="utf8") as file:
        task_string = f"{uuid.uuid4()}{SEPARATOR}{task_name}{SEPARATOR}[{date_complete}]{SEPARATOR}{timestamp}{SEPARATOR}"
        if not date_complete or datetime.strptime(date_complete, "%d.%m.%Y") > timestamp:
            task_string += f"{STATUS_ACTIVE}"
        else:
            task_string == f"{STATUS_OVERDUE}"
        file.write(task_string)


def main_menu():
    while True:
        tasks_list = parse_tasks(read_database(FILEPATH))
        print_readable(tasks_list)
        print("#------------------------#")
        print("Выберите действие")
        print("1 - Создать новую задачу")
        print("2 - Завершить задачу")
        print("3 - Изменить параметры задачи")
        print("0 - Выйти из программы")
        choice = input()
        if not choice.isdigit() or not (0 <= int(choice) <= 3):
            print("Введите действие в правильном формате")
            continue
        choice = int(choice)
        match choice:
            case 1:
                make_new_task()
            case 2:
                complete_task()
            case 3:
                change_task_parameters()
            case _:
                sys.exit()


if __name__ == "__main__":
    main_menu()
