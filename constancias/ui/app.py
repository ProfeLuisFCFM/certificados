# ui/app.py
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget, QMenuBar, QMenu
)
from PyQt6.QtGui import QAction
from db.models import Database
from ui.dialogs import CrearEstudianteDialog, CrearCursoDialog, CrearInstructorDialog

class ConstanciasApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Constancias")
        self.db = Database()
        self.init_ui()

    def init_ui(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.menu_estudiantes = QMenu("Estudiantes", self)
        self.menu_cursos = QMenu("Cursos", self)
        self.menu_instructores = QMenu("Instructores", self)

        self.menu_bar.addMenu(self.menu_estudiantes)
        self.menu_bar.addMenu(self.menu_cursos)
        self.menu_bar.addMenu(self.menu_instructores)

        self.action_ver_constancias = QAction("Ver constancias", self)
        self.action_ver_constancias.triggered.connect(self.mostrar_constancias)
        self.menu_bar.addAction(self.action_ver_constancias)

        # Acciones del menú
        self.action_crear_estudiante = QAction("Agregar Estudiante", self)
        self.action_crear_estudiante.triggered.connect(self.crear_estudiante)
        self.menu_estudiantes.addAction(self.action_crear_estudiante)

        self.action_crear_curso = QAction("Agregar Curso", self)
        self.action_crear_curso.triggered.connect(self.crear_curso)
        self.menu_cursos.addAction(self.action_crear_curso)

        self.action_crear_instructor = QAction("Agregar Instructor", self)
        self.action_crear_instructor.triggered.connect(self.crear_instructor)
        self.menu_instructores.addAction(self.action_crear_instructor)

        self.table = QTableWidget()
        self.setCentralWidget(self.table)

        self.mostrar_constancias()

    def mostrar_constancias(self):
        constancias = self.db.obtener_constancias()
        self.table.setRowCount(len(constancias))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Estudiante", "Curso", "Fecha"])

        for row_idx, row in enumerate(constancias):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(row_idx, 1, QTableWidgetItem(row["codigo_unico"]))
            self.table.setItem(row_idx, 2, QTableWidgetItem(row["nombre_completo"]))
            self.table.setItem(row_idx, 3, QTableWidgetItem(row["curso"]))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row["fecha_generacion"])))

    def crear_estudiante(self):
        dialog = CrearEstudianteDialog(self.db)
        dialog.exec()
        self.mostrar_constancias()

    def crear_curso(self):
        dialog = CrearCursoDialog(self.db)
        dialog.exec()

    def crear_instructor(self):
        dialog = CrearInstructorDialog(self.db)
        dialog.exec()


def launch_app():
    import sys
    app = QApplication(sys.argv)
    window = ConstanciasApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ConstanciasApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
