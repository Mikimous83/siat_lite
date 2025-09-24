from ttkbootstrap.dialogs import Messagebox


class AccidenteFormActions:
    def __init__(self, view):
        """
        Recibe la vista AccidenteFormView para poder manipular
        sus widgets (treeviews, entries, etc.)
        """
        self.view = view

    # ======= VEHÍCULOS =======
    def agregar_vehiculo(self):
        Messagebox.show_info("Agregar vehículo", "Aquí irá el formulario para registrar un vehículo.")

        # Ejemplo de inserción temporal en el Treeview:
        self.view.tree_vehiculos.insert(
            "", "end",
            values=("Automóvil", "Toyota", "Corolla", "ABC-123", "Azul")
        )

    def editar_vehiculo(self):
        seleccionado = self.view.tree_vehiculos.selection()
        if not seleccionado:
            Messagebox.show_warning("Atención", "Selecciona un vehículo para editar")
            return
        Messagebox.show_info("Editar vehículo", f"Editar vehículo ID: {seleccionado}")

    def eliminar_vehiculo(self):
        seleccionado = self.view.tree_vehiculos.selection()
        if not seleccionado:
            Messagebox.show_warning("Atención", "Selecciona un vehículo para eliminar")
            return
        self.view.tree_vehiculos.delete(seleccionado)
        Messagebox.show_info("Eliminado", "Vehículo eliminado de la lista")

    # ======= PERSONAS =======
    def agregar_persona(self):
        Messagebox.show_info("Agregar persona", "Aquí irá el formulario para registrar una persona.")

        # Ejemplo de inserción temporal en el Treeview:
        self.view.tree_personas.insert(
            "", "end",
            values=("Conductor", "Juan", "Pérez", "87654321")
        )

    def editar_persona(self):
        seleccionado = self.view.tree_personas.selection()
        if not seleccionado:
            Messagebox.show_warning("Atención", "Selecciona una persona para editar")
            return
        Messagebox.show_info("Editar persona", f"Editar persona ID: {seleccionado}")

    def eliminar_persona(self):
        seleccionado = self.view.tree_personas.selection()
        if not seleccionado:
            Messagebox.show_warning("Atención", "Selecciona una persona para eliminar")
            return
        self.view.tree_personas.delete(seleccionado)
        Messagebox.show_info("Eliminado", "Persona eliminada de la lista")
