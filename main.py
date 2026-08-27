import json
import cmd
R = "\033[91m" # [-]
G = "\033[32m" # [+]
B = "\033[36m" # [*]
Y = "\033[33m" # [!]
RE = "\033[0m"  # Normal Color
NEGATIVE = R+" [-] "+RE
POSITIVE = G+" [+] "+RE
INFO = B+" [*] "+RE
WARNING = Y+" [!] "+RE
class tasker(cmd.Cmd):
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



    prompt = " Manage > "
    def __init__(self):
        super().__init__()
        self.tasks = {}
    def do_add(self, arg):
        if arg.strip():
            self.tasks[arg] = False
            print(f"{POSITIVE}Item '{arg}' Appended to list.\n")
        else:
            print(f"{NEGATIVE}Item name must be 1 or more letters")
    def do_list(self, arg):
        if len(self.tasks) >= 1:
            print(f"{INFO}Main list: ")
            for i,key in enumerate(self.tasks, start=1):
                print(i,". ",key,end="")
                if self.tasks[key]:
                    print(f"{G} [✓]{RE}")
                if not self.tasks[key]:
                    print(f"{R} [X]{RE}")
        else:
            print(f"{INFO}List empty.")
    def do_quit(self, _):
        print(f"{POSITIVE}Quitting peacefully.\n")
        return True
    def do_check(self, arg):
        item = arg.strip()
        if len(self.tasks) == 0:
            print(f"{WARNING}The list is empty.")
        if item:
            if item in self.tasks:
                print(f"{POSITIVE}Item '{arg}' successfully checked.")
                self.tasks[arg] = not self.tasks[arg]
            elif item not in self.tasks:
                print(f"{NEGATIVE}Item '{arg}' not found")
        else:
            print(f"{NEGATIVE}Please enter something.")
    def do_remove(self, arg):
        if len(self.tasks) == 0:
            print(f"{WARNING}The list is empty.")
        item_in = False
        if arg.strip():
            for item in self.tasks:
                if item == arg:
                    item_in = True
                    print(f"{POSITIVE}Task '{arg}' successfully removed.")
            if item_in:
                self.tasks.pop(arg)
            elif not item_in:
                print(f"{NEGATIVE}Item '{arg}' not in list.")
        if not arg.strip():
            print(f"{NEGATIVE}Please enter something.")
    def do_save(self, _):
        with open("save.json","w") as jsonsave:
            json.dump(self.tasks,jsonsave)
        print(f"{POSITIVE}Saved successfully.")
    def do_load(self,_):
        with open("save.json","r") as jsonsave:
            self.tasks = json.load(jsonsave)
        print(f"{POSITIVE}Loaded successfully.")
    def help_add(self):
        print(f"add <task> - add a new task.")
    def help_list(self):
        print(f"list - lists all tasks.")
    def help_quit(self):
        print(f"quit - close the command line interface.")
    def help_check(self):
        print(f"check <task> - toggles a task's completion status.")
    def help_remove(self):
        print(f"remove <task> - removes a task by name.")
    def help_save(self):
        print(f"save - writes the list to save.json")
    def help_load(self):
        print(f"load - loads the list back from save.json")
if __name__ == "__main__":
    try:
        tasker().cmdloop()
    except KeyboardInterrupt:
        print(f"{WARNING}Program Interrupted. GoodBye..")
