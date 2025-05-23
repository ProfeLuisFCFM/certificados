import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="constancias.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        # Tabla instructores
        c.execute("""
            CREATE TABLE IF NOT EXISTS instructores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        # Tabla cursos
        c.execute("""
            CREATE TABLE IF NOT EXISTS cursos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        """)
        # Relacion curso-instructor (muchos a muchos)
        c.execute("""
            CREATE TABLE IF NOT EXISTS cursos_instructores (
                curso_id INTEGER NOT NULL,
                instructor_id INTEGER NOT NULL,
                PRIMARY KEY (curso_id, instructor_id),
                FOREIGN KEY (curso_id) REFERENCES cursos(id),
                FOREIGN KEY (instructor_id) REFERENCES instructores(id)
            )
        """)
        # Tabla estudiantes
        c.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_completo TEXT UNIQUE NOT NULL
            )
        """)
        # Relacion estudiante-curso (muchos a muchos)
        c.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes_cursos (
                estudiante_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                PRIMARY KEY (estudiante_id, curso_id),
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (curso_id) REFERENCES cursos(id)
            )
        """)
        # Tabla constancias (sin cambios, para referencia)
        c.execute("""
            CREATE TABLE IF NOT EXISTS constancias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_unico TEXT UNIQUE NOT NULL,
                estudiante_id INTEGER NOT NULL,
                curso_id INTEGER NOT NULL,
                fecha_generacion TEXT NOT NULL,
                activo INTEGER DEFAULT 1,
                FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                FOREIGN KEY (curso_id) REFERENCES cursos(id)
            )
        """)
        self.conn.commit()

    ## Instructores ##
    def obtener_instructores(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM instructores ORDER BY nombre")
        return c.fetchall()

    def crear_instructor(self, nombre):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO instructores (nombre) VALUES (?)", (nombre,))
            self.conn.commit()
            return c.lastrowid
        except sqlite3.IntegrityError as e:
            raise ValueError("El instructor ya existe") from e

    def eliminar_instructor(self, instructor_id):
        c = self.conn.cursor()
        # Eliminación lógica o física, aquí física por ejemplo
        c.execute("DELETE FROM instructores WHERE id = ?", (instructor_id,))
        self.conn.commit()

    def actualizar_instructor(self, instructor_id, nuevo_nombre):
        c = self.conn.cursor()
        c.execute("UPDATE instructores SET nombre = ? WHERE id = ?", (nuevo_nombre, instructor_id))
        self.conn.commit()

    ## Cursos ##
    def obtener_cursos(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM cursos ORDER BY nombre")
        return c.fetchall()

    def crear_curso(self, nombre, instructor_ids):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO cursos (nombre) VALUES (?)", (nombre,))
            curso_id = c.lastrowid
            for instructor_id in instructor_ids:
                c.execute("INSERT INTO cursos_instructores (curso_id, instructor_id) VALUES (?, ?)",
                          (curso_id, instructor_id))
            self.conn.commit()
            return curso_id
        except sqlite3.IntegrityError as e:
            raise ValueError("El curso ya existe o instructor inválido") from e

    def eliminar_curso(self, curso_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM cursos_instructores WHERE curso_id = ?", (curso_id,))
        c.execute("DELETE FROM cursos WHERE id = ?", (curso_id,))
        self.conn.commit()

    def actualizar_curso(self, curso_id, nuevo_nombre, instructor_ids):
        c = self.conn.cursor()
        c.execute("UPDATE cursos SET nombre = ? WHERE id = ?", (nuevo_nombre, curso_id))
        c.execute("DELETE FROM cursos_instructores WHERE curso_id = ?", (curso_id,))
        for instructor_id in instructor_ids:
            c.execute("INSERT INTO cursos_instructores (curso_id, instructor_id) VALUES (?, ?)",
                      (curso_id, instructor_id))
        self.conn.commit()

    def obtener_instructores_por_curso(self, curso_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT i.* FROM instructores i
            JOIN cursos_instructores ci ON i.id = ci.instructor_id
            WHERE ci.curso_id = ?
        """, (curso_id,))
        return c.fetchall()

    ## Estudiantes ##
    def obtener_estudiantes(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM estudiantes ORDER BY nombre_completo")
        return c.fetchall()

    def crear_estudiante(self, nombre_completo, curso_ids):
        c = self.conn.cursor()
        try:
            c.execute("INSERT INTO estudiantes (nombre_completo) VALUES (?)", (nombre_completo,))
            estudiante_id = c.lastrowid
            for curso_id in curso_ids:
                c.execute("INSERT INTO estudiantes_cursos (estudiante_id, curso_id) VALUES (?, ?)",
                          (estudiante_id, curso_id))
            self.conn.commit()
            return estudiante_id
        except sqlite3.IntegrityError as e:
            raise ValueError("El estudiante ya existe o curso inválido") from e

    def eliminar_estudiante(self, estudiante_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM estudiantes_cursos WHERE estudiante_id = ?", (estudiante_id,))
        c.execute("DELETE FROM estudiantes WHERE id = ?", (estudiante_id,))
        self.conn.commit()

    def actualizar_estudiante(self, estudiante_id, nuevo_nombre, curso_ids):
        c = self.conn.cursor()
        c.execute("UPDATE estudiantes SET nombre_completo = ? WHERE id = ?", (nuevo_nombre, estudiante_id))
        c.execute("DELETE FROM estudiantes_cursos WHERE estudiante_id = ?", (estudiante_id,))
        for curso_id in curso_ids:
            c.execute("INSERT INTO estudiantes_cursos (estudiante_id, curso_id) VALUES (?, ?)",
                      (estudiante_id, curso_id))
        self.conn.commit()

    def obtener_cursos_por_estudiante(self, estudiante_id):
        c = self.conn.cursor()
        c.execute("""
            SELECT c.* FROM cursos c
            JOIN estudiantes_cursos ec ON c.id = ec.curso_id
            WHERE ec.estudiante_id = ?
        """, (estudiante_id,))
        return c.fetchall()

    ## Constancias ##
    def obtener_constancias(self):
        c = self.conn.cursor()
        c.execute("""
            SELECT constancias.id, constancias.codigo_unico, estudiantes.nombre_completo,
                   cursos.nombre AS curso, constancias.fecha_generacion
            FROM constancias
            JOIN estudiantes ON constancias.estudiante_id = estudiantes.id
            JOIN cursos ON constancias.curso_id = cursos.id
            WHERE constancias.activo = 1
            ORDER BY constancias.fecha_generacion DESC
        """)
        return c.fetchall()

    def crear_constancia(self, codigo_unico, estudiante_id, curso_id):
        c = self.conn.cursor()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
            INSERT INTO constancias (codigo_unico, estudiante_id, curso_id, fecha_generacion, activo)
            VALUES (?, ?, ?, ?, 1)
        """, (codigo_unico, estudiante_id, curso_id, fecha))
        self.conn.commit()
        return c.lastrowid

    def eliminar_constancia(self, constancia_id):
        c = self.conn.cursor()
        c.execute("UPDATE constancias SET activo = 0 WHERE id = ?", (constancia_id,))
        self.conn.commit()

    def actualizar_constancia(self, constancia_id, nuevo_codigo_unico):
        c = self.conn.cursor()
        c.execute("UPDATE constancias SET codigo_unico = ? WHERE id = ?", (nuevo_codigo_unico, constancia_id))
        self.conn.commit()
