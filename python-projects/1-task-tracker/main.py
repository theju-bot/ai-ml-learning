import sys
import json
from datetime import datetime

file_name = "tasks.json"


def main():
    if len(sys.argv) <= 1:
        print("""
            Usage:
            
            python main.py add "<description>"
            python main.py update <id> "<new description>"
            python main.py delete <id>
             
            python main.py list
            python main.py list todo
            python main.py list in-progress
            python main.py list done
             
            python main.py mark-in-progress <id>
            python main.py mark-done <id>
            """)
        return

    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "add":
                add_task(sys.argv[2])
            case "update":
                update_task(int(sys.argv[2]), sys.argv[3])
            case "delete":
                delete_task(int(sys.argv[2]))
            case "list":
                if len(sys.argv) > 2:
                    show_task(sys.argv[2])
                else:
                    show_task()
            case "mark-in-progress" | "mark-done":
                task_status_update(sys.argv[1], int(sys.argv[2]))
            case _:
                print("""
                Usage:
                
                python main.py add "<description>"
                python main.py update <id> "<new description>"
                python main.py delete <id>
                 
                python main.py list
                python main.py list todo
                python main.py list in-progress
                python main.py list done
                 
                python main.py mark-in-progress <id>
                python main.py mark-done <id>
                """)


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


def update_task(task_id, updated_task):
    with open(file_name, "r") as file:
        content = json.load(file)

    task = next((task for task in content if task_id == task["id"]), None)

    if task:
        task["description"] = updated_task
        task["updatedAt"] = datetime.now().isoformat()
        with open(file_name, "w") as file:
            json.dump(content, file, indent=2)
        print(f"{task['description']} was updated succesfully, id is {task['id']}")
    else:
        print(f"There is no such task with id {task_id}")


def delete_task(task_id):
    with open(file_name, "r") as file:
        content = json.load(file)
    task = next((task for task in content if task_id == task["id"]), None)

    if task:
        content.remove(task)
        with open(file_name, "w") as file:
            json.dump(content, file, indent=2)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"There is no task with id {task_id}")


def show_task(tasks_status="all"):
    with open(file_name, "r") as file:
        content = json.load(file)
    if tasks_status == "all":
        tasks = content
    else:
        tasks = [task for task in content if task["status"] == tasks_status]

    if tasks:
        for task in tasks:
            print(f"{task['id']} - {task['description']} - {task['status']}")
    else:
        print("No tasks found")


def task_status_update(task_status, task_id):
    with open(file_name, "r") as file:
        content = json.load(file)
    task = next((task for task in content if task_id == task["id"]), None)

    if task:
        task["status"] = task_status
        with open(file_name, "w") as file:
            json.dump(content, file, indent=2)
        print(f"Task {task_id} status change to {task_status} successfully")
    else:
        print(f"There is no task with id {task_id}")


if __name__ == "__main__":
    try:
        with open(file_name, "x") as file:
            json.dump([], file)
    except Exception as e:
        pass

    try:
        with open(file_name, "r") as file:
            json.load(file)
    except json.JSONDecodeError:
        with open(file_name, "w") as file:
            json.dump([], file)

    main()
