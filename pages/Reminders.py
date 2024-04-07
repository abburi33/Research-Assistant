import streamlit as st
import functions

def add_todo():
    """
    Function to add a new todo item.
    """
    if 'new_todo' in st.session_state:
        todo = st.session_state.new_todo + '\n'
        todos.append(todo)
        functions.write_todos(todos)
        st.session_state.new_todo = ''  # Reset the input field after adding

def main():
    """
    Main function to run the app for managing reminders.
    """
    global todos
    todos = functions.get_todos()
    
    st.title("Your Current Reminders")

    # Display existing todos
    for index, todo in enumerate(todos):
        check_box = st.checkbox(todo.strip(), key=todo.strip())
        if check_box:
            todos.pop(index)
            functions.write_todos(todos)
            st.experimental_rerun()  # Rerun the app to reflect the changes

    # Input field to add new todo
    new_todo = st.text_input(label='', placeholder="Add new todo...", key='new_todo', on_change=add_todo)
    if new_todo:
        st.session_state.new_todo = new_todo

if __name__ == "__main__":
    main()
