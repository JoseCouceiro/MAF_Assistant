import streamlit as st

def main():
    st.title("Generador de Botones con opción de eliminación")

    # Número de botones que deseas generar
    num_botones = st.slider("Selecciona el número de botones:", min_value=1, max_value=10)

    # Lista para almacenar el estado de las checkboxes
    checkboxes = [False] * num_botones

    # Generar botones y checkboxes en un bucle for
    for i in range(num_botones):
        # Checkbox correspondiente a cada botón
        checkboxes[i] = st.checkbox(f'Eliminar botón {i+1}', key=f'checkbox_{i}')

    # Mostrar solo los botones que no han sido eliminados
    for i, checkbox in enumerate(checkboxes):
        if not checkbox:
            st.button(f"Botón {i+1}")

if __name__ == "__main__":
    main()

def delete_checkboxes(key):
    while st.checkbox('Delete', key = key):
        st.write(st.session_state[key])
        return True

def history_buttons():
    filenames = dict()
    delete_buttons = dict()
    for __file in __searches_path.iterdir():
        __n += 1
        filenames[__n] = __file.name.split('.')[0]
        variables[__n] = st.button(f"{filenames[__n].replace('_', '/')}")
        delete_buttons[__n] = st.checkbox('Delete', key = key)
        
        if variables[__n]:
            return True, filenames[__n]
        if delete_buttons[__n]:
            os.remove(os.path.join(__searches_path, filenames[__n]+'.json'))