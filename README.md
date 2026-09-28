# Features

* Create lists using the 'create' command followed by the name of the list.
* Open a list using the 'open' command followed by the list name to open it.
* Add tasks using the 'add' command followed by the task name.
* List the items inside any available list using the 'list' command optionally followed by the list name or 'root' to see all lists available,
  it defaults to your current opened list.
* Remove tasks using the 'remove' command followed by the task name.
* Check a task using the 'check' command followed by the task name, this command toggles the state of the task.
* Rename tasks using the 'rename' command followed by the task name then the new task name.

You can run cli_tasker.py with arguments (made with argparse) or cmd_tasker.py to open a console
similar to metasploit or recon-ng.

# Commands

1. create (list_name)*
2. open (list_name)*
3. add (item_name)*
4. list (list_name)
5. remove (item_name)*
6. check (item_name)*
7. remame (old_name)* (new_name)*

# Requirements

Python 3.10 or higher.

Made by @ILikeCache on github.com
