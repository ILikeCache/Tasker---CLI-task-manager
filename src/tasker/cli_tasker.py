import argparse
import json
from output import *
from storage import save_tasks, load_tasks
from manager import Manager

"""
XXX: Return codes
return 1: Success
return 0: no arguments provided
return -1: 2 arguments required but only 1 provided
return -2: not found
return -3: already present
return -4: list already empty
"""

manager = Manager(load_tasks())

parser = argparse.ArgumentParser(prog="tasker", description="cli task manager for python.")
commands = parser.add_subparsers(
    dest="command",
    required=True,
)
# Add parser
add_parser = commands.add_parser("add", help="Add an item.")
list_parser = commands.add_parser("list",help="List items")
remove_parser = commands.add_parser("remove",help="Remove an item.")
check_parser = commands.add_parser("check",help="Toggle the state of an item.")
rename_parser = commands.add_parser("rename",help="Rename an item.")

add_parser.add_argument("item_name", help="Name of the item.")
remove_parser.add_argument("item_name",help="Name of the item.")
check_parser.add_argument("item_name",help="Name of the item.")
rename_parser.add_argument("item_name",help="Name of the item you want to change.")
rename_parser.add_argument("new_item_name",help="Name of the new item name.")
list_parser.add_argument("list_name",nargs='?',default=manager.current_list_name,help="Name of the list")

args = parser.parse_args()

def do_list(list_name: str):
    if list_name not in manager.data:
        print(f"{NEGATIVE}List '{list_name}' not found.")
        return
            
    if len(manager.data[list_name]) < 1:
        print(f"{INFO}List '{list_name}' empty.")
        return
        
    print(f"{INFO}List '{list_name}' contains: ")        
    for index, key in enumerate(manager.data[list_name], start=1):
        
        print(index,". ",key,end="")
        if manager.data[list_name][key]:
            print(f"{G} [✓]{RE}")
        if not manager.data[list_name][key]:
            print(f"{R} [X]{RE}")
        
            
def do_add(arg):
    response: int = manager.add(arg)
    
    if response == 0:
        print(f"{NEGATIVE}Item name must be 1 or more letters.")
        return
    if response == -3:
        print(f"{WARNING}Item '{arg.strip()}' already present.")
        print("manager.add() returned 3 / already present")
        return
        
    if response == 1:
        print(f"{POSITIVE}Item '{arg}' Appended to list.\n")
        return
        
def do_remove(arg):
    response: int = manager.remove(arg)
    if response == -4:
        print(f"{WARNING}The list is empty.")
        return
        
    if response == 0:
        print(f"{NEGATIVE}Please enter something.")
        return
    if response == -2:
        print(f"{NEGATIVE}Item '{arg.strip()}' not found.")
        return
    if response == 1:
        print(f"{POSITIVE}Item '{arg.strip()}' successfully removed.")
        return
        
def do_check(arg):
    response: int = manager.check(arg)
    
    if response == -4:
        print(f"{WARNING}The list is empty.")
        return
    if response == -2:
        print(f"{NEGATIVE}Item '{arg}' not found")
        return
    if response == 1:
        print(f"{POSITIVE}Item '{arg}' successfully checked.")
        return
        
def do_rename(old_name: str, new_name: str):
    response: int = manager.rename(old_name, new_name)
    
    if response == -4:
        print(f"{INFO}List empty.")
        return
    if response == -2:
        print(f"{NEGATIVE}Item '{old_name}' not found.")
        return
    if response == -3:
        print(f"{WARNING}Item '{new_name}' already present.")
        return
    if response == 1:
        print(f"{POSITIVE}Item '{old_name}' renamed to '{new_name}' successfully.")
        return
        
if args.command == "list":
    do_list(args.list_name)
    
if args.command == "add":
    do_add(args.item_name)
    
if args.command == "remove":
    do_remove(args.item_name)
    
if args.command == "check":
    do_check(args.item_name)
    
if args.command == "rename":
    do_rename(args.item_name, args.new_item_name)
    