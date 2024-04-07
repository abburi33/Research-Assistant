FILEPATH = "todos.txt"

def get_todos(filepath=FILEPATH):
    """
    Read a text file and return the list of to-do items.

    Args:
        filepath (str): The path to the text file containing to-do items.
                        Default is FILEPATH.

    Returns:
        list: A list of to-do items read from the text file.
    """
    with open(filepath, "r") as todoFile:
        todos_local = todoFile.readlines()
    return todos_local

def write_todos(new_todos, filepath=FILEPATH):
    """
    Write the list of to-do items to the text file.

    Args:
        new_todos (list): The list of to-do items to be written to the file.
        filepath (str): The path to the text file to write the to-do items.
                        Default is FILEPATH.

    Returns:
        None
    """
    with open(filepath, "w") as todoFile:
        todoFile.writelines(new_todos)

if __name__ == "__main__":
    print(get_todos())
