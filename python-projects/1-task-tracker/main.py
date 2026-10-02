import sys
import json
from datetime import datetime

file_name = "tasks.json"


def main():
    if len(sys.argv) > 2:
        match sys.argv[1]:
            case "add":
                add_task(sys.argv[2])
            case "update":
                update_task(sys.argv[2], sys.argv[3])
            case "delete":
                delete_task(sys.argv[2])
            case "list":
                show_task(sys.argv[2])


def add_task(task_des):
    with open(file_name, "r") as file:
        content = json.load(file)
    if content:
        last_id = content[-1]["id"]
    else:
        last_id = 0

    task = {
        "id": last_id + 1,
        "description": f"{task_des}",
        "status": "todo",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    content.append(task)

    with open(file_name, "w") as file:
        json.dump(content, file, indent=2)

    print(f"{task_des} was added succesfully, id is {task['id']}")


def update_task(task_id, task):
    pass


def delete_task(task_id):
    pass


def show_task(tasks="done"):
    pass


if __name__ == "__main__":
    try:
        with open(file_name, "x") as file:
            json.dump([], file)
    except Exception as e:
        pass

    main()
