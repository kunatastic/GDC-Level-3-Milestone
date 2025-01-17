from http.server import BaseHTTPRequestHandler, HTTPServer


class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def runserver(self):
        address = "127.0.0.1"
        port = 8000
        server_address = (address, port)
        httpd = HTTPServer(server_address, TasksServer)
        print(f"Started HTTP Server on http://{address}:{port}")
        httpd.serve_forever()

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            self.add(args)
        elif command == "done":
            self.done(args)
        elif command == "delete":
            self.delete(args)
        elif command == "ls":
            self.ls()
        elif command == "report":
            self.report()
        elif command == "runserver":
            self.runserver()
        elif command == "help":
            self.help()

    def help(self):
        print(
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics
$ python tasks.py runserver # Starts the tasks management server"""
        )

    def add(self, args):
        if (len(args)==0):
            print("Error: Missing priority string. Nothing added!")
        elif (len(args)==1):
            print("Error: Missing task string. Nothing added!")
        try:
            current = int(args[0])
            task = " ".join(args[1:])
            while current in list(self.current_items.keys()):
                temp_task = self.current_items[current]
                self.current_items[current] = task
                task = temp_task
                current+=1
            self.current_items[current] = task
            self.write_current()
            print('Added task: "' + " ".join(args[1:]) + '" with priority ' + (args[0]))
        except Exception:
            print("Error: Invalid priority number. Nothing added!")
            pass



    def done(self, args):
        try:
            if (int(args[0]) in list(self.current_items.keys())):
                self.completed_items.append(self.current_items[int(args[0])])
                self.write_completed()
                del self.current_items[int(args[0])]
                self.write_current()
                print("Marked item as done.")
            else:
                print(f"Error: no incomplete item with priority {args[0]} exists.")
                
        except Exception:
            print("Error: Invalid priority number. Nothing deleted!")
            pass
        


    def delete(self, args):
        try:
            if (int(args[0]) in list(self.current_items.keys())):
                del self.current_items[int(args[0])]
                self.write_current()
                print(f"Deleted item with priority {args[0]}")
            else:
                print(f"Error: item with priority {args[0]} does not exist. Nothing deleted.")
        except Exception:
            print("Error: Invalid priority number. Nothing deleted!")
            pass

    def ls(self):
        count = 1
        for i in (list(self.current_items.keys())):
            print(f"{count}. {self.current_items[i]} [{i}]")
            count+=1
        

    def report(self):
        print("Pending : " + str(len(self.current_items)))
        count = 1
        for i in (list(self.current_items.keys())):
            print(f"{count}. {self.current_items[i]} [{i}]")
            count+=1
        
        count = 1
        print("\nCompleted : "+ str(len(self.completed_items)))
        for i in (list(self.completed_items)):
            print(f"{count}. {i}")
            count+=1



    def render_pending_tasks(self):
        # Complete this method to return all incomplete tasks as HTML
        content = "<h1> List of Pending Tasks are Here </h1>"
        count = 1
        self.read_current()
        for i in (list(self.current_items.keys())):
            content += f"<h2>{count}. {self.current_items[i]} [{i}]</h2>"
            count+=1
        return content

    def render_completed_tasks(self):
        # Complete this method to return all completed tasks as HTML
        content = "<h1> List of Completed Tasks are Here </h1>"
        count = 1
        self.read_completed()
        for i in (list(self.completed_items)):
            content += f"<h2>{count}. {i}</h2>"
            count+=1
        return content

class TasksServer(TasksCommand, BaseHTTPRequestHandler):
    def do_GET(self):
        task_command_object = TasksCommand()
        if self.path == "/tasks":
            content = task_command_object.render_pending_tasks()
        elif self.path == "/completed":
            content = task_command_object.render_completed_tasks()
        else:
            self.send_response(404)
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())



# UNCOMMENT
# address = "127.0.0.1"
# port = 8000
# server_address = (address, port)
# httpd = HTTPServer(server_address, TasksServer)
# print(f"Started HTTP Server on http://{address}:{port}")
# httpd.serve_forever()