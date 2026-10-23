import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class VentanaInventario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard de Inventario - Empresa de Jabones Aromáticos")
        self.setGeometry(100, 100, 1100, 700)

        # Cargar datos
        self.df = pd.read_csv("inventario_jabones.csv")
        self.df["valor_total"] = self.df["stock"] * self.df["precio_unitario"]

        # Widget central y Layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Título principal
        titulo = QLabel("Sistema de Análisis y Evaluación de Inventario")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        self.main_layout.addWidget(titulo)

        # Layout horizontal para dividir Gráficos y Tabla
        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)

        # 1. Configuración de Matplotlib
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.content_layout.addWidget(self.canvas, stretch=2)

        # 2. Configuración de la Tabla de Datos
        self.tabla = QTableWidget()
        self.content_layout.addWidget(self.tabla, stretch=1)

        # Renderizar componentes
        self.cargar_tabla()
        self.generar_graficos()

    def cargar_tabla(self):
        self.tabla.setRowCount(len(self.df))
        self.tabla.setColumnCount(len(self.df.columns))
        self.tabla.setHorizontalHeaderLabels(self.df.columns)

        for row_idx, row_data in self.df.iterrows():
            for col_idx, value in enumerate(row_data):
                self.tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def generar_graficos(self):
        self.figure.clear()

        # Gráfico 1: Stock Total por Sucursal
        ax1 = self.figure.add_subplot(121)
        stock_por_sucursal = self.df.groupby("sucursal")["stock"].sum()
        stock_por_sucursal.plot(kind="bar", ax=ax1, color="#4CAF50")
        ax1.set_title("Stock Total por Sucursal")
        ax1.set_ylabel("Unidades en Stock")
        ax1.set_xlabel("Sucursal")
        ax1.tick_params(axis='x', rotation=45)

        # Gráfico 2: Valor Total del Inventario por Categoría
        ax2 = self.figure.add_subplot(122)
        valor_por_cat = self.df.groupby("categoria")["valor_total"].sum()
        valor_por_cat.plot(kind="pie", ax=ax2, autopct='%1.1f%%', colors=['#FF9999','#66B2FF','#99FF99','#FFCC99','#D1C4E9'])
        ax2.set_title("Distribución de Valor por Categoría")
        ax2.set_ylabel("")

        self.figure.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInventario()
    ventana.show()
    sys.exit(app.exec_())