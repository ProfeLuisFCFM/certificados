# ui/dialogs.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QHBoxLayout, QCheckBox

class CrearCursoDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Crear Curso")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Nombre del curso:"))
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Selecciona instructores:"))
        self.instructores_list = QListWidget()
        self.instructores_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.instructores_list)

        # Cargar instructores
        instructores = self.db.obtener_instructores()
        for inst in instructores:
            # Aseguramos que inst sea diccionario con clave 'nombre'
            nombre = inst["nombre"] if "nombre" in inst.keys() else str(inst[1])
            self.instructores_list.addItem(nombre)

        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        btn_layout.addWidget(self.btn_guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def guardar(self):
        nombre_curso = self.nombre_input.text().strip()
        if not nombre_curso:
            QMessageBox.warning(self, "Error", "El nombre del curso no puede estar vacío.")
            return

        seleccionados = self.instructores_list.selectedItems()
        if not seleccionados:
            QMessageBox.warning(self, "Error", "Debes seleccionar al menos un instructor.")
            return

        # Obtener ids de instructores seleccionados (buscando en la BD)
        instructores = self.db.obtener_instructores()
        nombres_seleccionados = [item.text() for item in seleccionados]
        ids_seleccionados = []
        for inst in instructores:
            nombre = inst["nombre"] if "nombre" in inst.keys() else str(inst[1])
            if nombre in nombres_seleccionados:
                ids_seleccionados.append(inst["id"] if "id" in inst.keys() else inst[0])

        # Insertar curso y relaciones
        try:
            curso_id = self.db.crear_curso(nombre_curso, ids_seleccionados)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el curso:\n{e}")
            return

        self.accept()


class CrearInstructorDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Crear Instructor")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre del instructor:"))
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input)

        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        btn_layout.addWidget(self.btn_guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def guardar(self):
        nombre = self.nombre_input.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre del instructor no puede estar vacío.")
            return
        try:
            self.db.crear_instructor(nombre)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el instructor:\n{e}")
            return
        self.accept()


class CrearEstudianteDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Crear Estudiante")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nombre completo del estudiante:"))
        self.nombre_input = QLineEdit()
        layout.addWidget(self.nombre_input)

        layout.addWidget(QLabel("Selecciona cursos:"))
        self.cursos_list = QListWidget()
        self.cursos_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        layout.addWidget(self.cursos_list)

        cursos = self.db.obtener_cursos()
        for curso in cursos:
            nombre = curso["nombre"] if "nombre" in curso.keys() else str(curso[1])
            self.cursos_list.addItem(nombre)

        btn_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar)
        btn_layout.addWidget(self.btn_guardar)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_cancelar)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def guardar(self):
        nombre_estudiante = self.nombre_input.text().strip()
        if not nombre_estudiante:
            QMessageBox.warning(self, "Error", "El nombre del estudiante no puede estar vacío.")
            return

        seleccionados = self.cursos_list.selectedItems()
        if not seleccionados:
            QMessageBox.warning(self, "Error", "Debes seleccionar al menos un curso.")
            return

        cursos = self.db.obtener_cursos()
        nombres_seleccionados = [item.text() for item in seleccionados]
        ids_seleccionados = []
        for curso in cursos:
            nombre = curso["nombre"] if "nombre" in curso.keys() else str(curso[1])
            if nombre in nombres_seleccionados:
                ids_seleccionados.append(curso["id"] if "id" in curso.keys() else curso[0])

        try:
            estudiante_id = self.db.crear_estudiante(nombre_estudiante, ids_seleccionados)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear el estudiante:\n{e}")
            return

        self.accept()
