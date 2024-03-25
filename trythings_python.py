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

    # Eliminar botones y checkboxes seleccionados
    indices_a_eliminar = [i for i, checkbox in enumerate(checkboxes) if checkbox]
    for index in reversed(indices_a_eliminar):
        del checkboxes[index]

if __name__ == "__main__":
    main()

