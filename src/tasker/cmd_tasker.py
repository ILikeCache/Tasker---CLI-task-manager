import cmd
from output import R,G,B,Y,RE,WARNING,INFO,NEGATIVE,POSITIVE
from storage import save_tasks, load_tasks
from manager import Manager

# Current version v1.0

"""
XXX: Return codes
return 1: Success
return 0: no arguments provided
return -1: 2 arguments required but only 1 provided
return -2: not found
return -3: already present
return -4: list already empty
""" 

# TODO: i need to change the code to use manager commands
class Tasker(cmd.Cmd):
    intro = r"""
        ,----,                    
      ,/   .`|                    
    ,`   .'  :                    
  ;    ;     /                    
.'___,/    ,'                     
|    :     |            .--.--.   
;    |.';  ; ,--.--.   /  /    '  
`----'  |  |/       \ |  :  /`./  
    '   :  .--.  .-. ||  :  ;_    
    |   |  '\__\/: . . \  \    `. 
    '   :  |," .--.; |  `----.   \
    ;   |.'/  /  ,.  | /  /`--'  /
    '-,-. ;  :   .'   '--'.     / 
  ,--/ /| |  ,     .-./ `--'---'  
,--. :/ |  `--`---' __  ,-.       
:  : ' /          ,' ,'/ /|       
|  '  /     ,---. '  | |' |       
'  |  :    /     \|  |   ,'       
|  |   \  /    /  '  :  /         
'  : |. \.    ' / |  | '          
|  | ' \ '   ;   /;  : |          
'  : |--''   |  / |  , ;          
;  |,'   |   :    |---'           
'--'      \   \  /                
           `----'                 
"""
    def emptyline(self):
        pass
        
    def __init__(self):
        super().__init__()
        
        self.manager = Manager(load_tasks())
        self.update_prompt()
        
    def list_items(self,list_name):
        
        if not self.manager.data[list_name]:
            print(f"{INFO}List empty.")
            return
        print(f"{INFO}List '{list_name}' contains: ")    
        for i,key in enumerate(self.manager.data[list_name], start=1):
            print(i,". ",key,end="")
            if self.manager.data[list_name][key]:
                print(f"{G} [✓]{RE}")
            if not self.manager.data[list_name][key]:
                print(f"{R} [X]{RE}")
    def update_prompt(self):
        self.prompt = f" Manage [{self.manager.current_list_name}]> "
        
    @property
    def current_list(self):
        return self.manager.current_list
    def do_create(self, arg):
        response: int = self.manager.create(arg)
        
        if response == 0:
            print(f"{NEGATIVE}No arguments provided.")
            return
        if response == -3: #already present
            print(f"{NEGATIVE}List '{arg.strip()}' already present.")
            return
        save_tasks(self.manager.data)    
        print(f"{POSITIVE}List '{arg.strip()}' successfully created.")    
    def do_open(self, arg): # Open command to open a list
        response: int = self.manager.open_list(arg)
        if response == 0:
            print(f"{WARNING}No arguments provided.")
            return
            
        if response == -2:
            print(f"{NEGATIVE}List '{arg}' not found.")
            return
            
        self.update_prompt()
            
    def do_add(self, arg):
        response: int = self.manager.add(arg)
        
        if response == 0:
            print(f"{NEGATIVE}No arguments provided.")
            return
        if response == -3: # already present
            print(f"{WARNING}Item '{arg.strip()}' already present.")
            return
            
        save_tasks(self.manager.data)    
        print(f"{POSITIVE}Item '{arg.strip()}' Appended to list.")
        
    def do_list(self, arg):
        if arg == 'root':
            for index, list in enumerate(self.manager.data.keys(), start=1):
                print(index,'. ',B,list,RE, end="\n", sep="")
            return
            
        if arg.strip():
            if not arg.strip() in self.manager.data.keys():
                print(f"{NEGATIVE}List '{arg}' not found.")
                return
                
            self.list_items(arg.strip())
            return 
            
        if len(self.current_list) < 1:
            print(f"{INFO}List empty.")
            return
        self.list_items(self.manager.current_list_name)
        
    def do_quit(self, _):
        print(f"{POSITIVE}Quitting peacefully.")
        return True
        
    def do_check(self, arg):
        response: int = self.manager.check(arg)
        if response == -4:
            print(f"{NEGATIVE}List empty.")
            return
        if response == 0:
            print(f"{NEGATIVE}No arguments provided.")
            return
        if response == -2: # not found
            print(f"{NEGATIVE}Item '{arg}' not found.")
            return
        print(f"{POSITIVE}Item '{arg}' successfully checked.")
        save_tasks(self.manager.data)
        
    def do_remove(self, arg):
        response: int = self.manager.remove(arg)
        if response == -4:
            print(f"{NEGATIVE}List empty.")
            return
        if response == 0:
            print(f"{NEGATIVE}No arguments provided.")
            return
        if response == -2:
            print(f"{NEGATIVE}Item '{arg}' not found.")
            return
        save_tasks(self.manager.data)    
        print(f"{POSITIVE}Item '{arg}' removed successfully.")
    def do_rename(self, arg):
        args = arg.split(maxsplit=1)
        if len(args) < 1:
            response = 0
            
        elif len(args) < 2:
            response = -1
            
        elif len(args) == 2:
            response: int = self.manager.rename(args[0],args[1])
        if response == 0:
            print(f"{NEGATIVE}No arguments provided.")
            return
        if response == -4:
            print(f"{NEGATIVE}List empty.")
            return
        if response == -2:
            print(f"{NEGATIVE}Item '{args[0].strip()}' not found.")
            return
        if response == -1:
            print(f"{NEGATIVE}2 arguments required but only 1 provided.")
            return
        if response == -3:
            print(f"{NEGATIVE}Name '{args[1].strip()}' already present.")
            return
        save_tasks(self.manager.data)    
        print(f"{POSITIVE}Item '{args[0]}' renamed to '{args[1]}' successfully.")
    
    def help_open(self):
        print(f"open <list> - opens the list of the specified name.")
    def help_add(self):
        print(f"add <task> - add a new task.")
    def help_list(self):
        print(f"list (list-name) - lists all tasks inside the specified list or the current list by default..")
    def help_quit(self):
        print(f"quit - close the command line interface.")
    def help_check(self):
        print(f"check <task> - toggles a task's completion status.")
    def help_remove(self):
        print(f"remove <task> - removes a task by name.")
    def help_rename(self):
        print(f"rename <task> <new-task-name>- renames an item from the list")
if __name__ == "__main__":
    try:
        Tasker().cmdloop()
    except KeyboardInterrupt:
        print(f"\n{NEGATIVE}Program Interrupted. GoodBye..\n")

