from flask import Flask, request, jsonify
from flask.views import MethodView
import json

app = Flask(__name__)

JSON_FILE = "tasks.json"

def read_tasks():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_tasks(tasks):
    with open(JSON_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

@app.route("/")
def root():
    return "<h1>Welcome to the Tasks CRUD</h1>"

class TaskAPI(MethodView):
    def get(self):
        tasks_list = read_tasks()
        status_filter = request.args.get("status")
        if status_filter:
            tasks_list = [task for task in tasks_list if task["status"] == status_filter]
        return jsonify({"data": tasks_list})

    def post(self):
        tasks_list = read_tasks()
        new_task = request.json

        if not all(key in new_task for key in ["identifier", "title", "description", "status"]):
            return jsonify({"error": "Mandatory Fields are missing."}), 400
        
        if any(task["identifier"] == new_task["identifier"] for task in tasks_list):
            return jsonify({"error": "The identifier already exists."}), 400
        
        if new_task["status"] not in ["Pending", "In Progress", "Completed"]:
            return jsonify({"error": "The status is invalid."}), 400
        
        tasks_list.append(new_task)
        write_tasks(tasks_list)
        return jsonify({"message": "Task created successfully.", "task": new_task}), 201

class TaskDetailAPI(MethodView):

    def put(self, identifier):
        tasks_list = read_tasks()
        updated_data = request.json

        for task in tasks_list:
            if task["identifier"] == identifier:
                task.update(updated_data)
                write_tasks(tasks_list)
                return jsonify({"message": "Task updated successfully.", "task": task}), 200

        return jsonify({"error": "Task not found."}), 404

    def delete(self, identifier):
        tasks_list = read_tasks()

        for task in tasks_list:
            if task["identifier"] == identifier:
                tasks_list.remove(task)
                write_tasks(tasks_list)
                return jsonify({"message": "Task deleted successfully."}), 200

        return jsonify({"error": "Task not found."}), 404
    
app.add_url_rule("/tasks", view_func=TaskAPI.as_view("tasks"))
app.add_url_rule("/tasks/<int:identifier>", view_func=TaskDetailAPI.as_view("task_detail"))

if __name__ == "__methodv__":
    app.run(host="localhost", debug=True)