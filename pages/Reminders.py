import streamlit as st
import functions

def add_todo():
    if 'new_todo' in st.session_state:
        todo = st.session_state.new_todo + '\n'
        todos.append(todo)
        functions.write_todos(todos)
        st.session_state.new_todo = ''  # Reset the input field after adding

def main():
    global todos
    todos = functions.get_todos()
    
    st.title("Your Current Reminders")

    for index, todo in enumerate(todos):
        check_box = st.checkbox(todo.strip(), key=todo.strip())
        if check_box:
            todos.pop(index)
            functions.write_todos(todos)
            st.experimental_rerun()  # Rerun the app to reflect the changes

    new_todo = st.text_input(label='', placeholder="Add new todo...", key='new_todo', on_change=add_todo)
    if new_todo:
        st.session_state.new_todo = new_todo

if __name__ == "__main__":
    main()