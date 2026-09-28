from storage import save_tasks, load_tasks
"""
XXX: Return codes
return 1: Success
return 0: no arguments provided
return -1: 2 arguments required but only 1 provided
return -2: not found
return -3: already present
return -4: list already empty
""" 

class Manager:
    def __init__(self, data):
        self.data: dict = data
        self.current_list_name: str = "main"
        if self.current_list_name not in self.data:
            self.data[self.current_list_name] = {}
    @property
    def current_list(self):
        return self.data[self.current_list_name]
        
    def open_list(self, list_name: str) -> int:
        list_name: str = list_name.strip()
        if not list_name:
            return 0
        if list_name not in self.data:
            return -2
        self.current_list_name = list_name
        
        return 1
    def create(self, list_name: str) -> int:
        if not list_name.strip():
            return 0
        if list_name.strip() in self.data:
            return -3
        self.data[list_name] = {}
        return 1
    def add(self, task_name: str) -> int:
        task_name: str = task_name.strip()

        if not task_name:
            return 0 # no args provided
        if task_name in self.data[self.current_list_name]:
            return -3 # item already present
        self.current_list[task_name] = False
        save_tasks(self.data)
        return 1

    def remove(self, task_name: str) -> int:
        task_name: str = task_name.strip()
        if not task_name:
            return 0 # no args provided
        if len(self.data[self.current_list_name]) < 1:
            return -4
        if task_name not in self.data[self.current_list_name]:
            return -2 # item not found
         
        del self.current_list[task_name]
        save_tasks(self.data)
        return 1

    def check(self, task_name: str) -> int:
        task_name: str = task_name.strip()
        if not task_name:
            return 0 # no args provided
        if task_name not in self.data[self.current_list_name]:
            return -2 # item not found
            
        self.data[self.current_list_name][task_name] = not self.data[self.current_list_name][task_name]
        save_tasks(self.data)
        return 1

    def rename(self, old_name: str, new_name: str) -> int: # BUG
        old_name: str = old_name.strip()
        new_name: str = new_name.strip()
        if len(self.data[self.current_list_name]) < 1:
            return -4 # list empty
        if not old_name:
            return 0 # no args provided
        if old_name and not new_name:
            return -1 # 1 arg provided only
                
        if old_name not in self.data[self.current_list_name]:
            return -2 # item not found

        if new_name in self.current_list:
            return -3 # already present
          
        self.data[self.current_list_name][new_name] = self.current_list.pop(old_name)
        save_tasks(self.data)
        return 1
        