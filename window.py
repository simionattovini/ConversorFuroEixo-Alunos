from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout, QMessageBox
from PyQt6 import QtGui
from PyQt6.QtCore import Qt

import backend_tools as bt

import matplotlib.pyplot as plt


class CFEWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__initialize()

    def __initialize(self):
        self.setWindowTitle('Conversor Furo-Eixo ABNT/NBR 6158')
        self.setWindowIcon(QtGui.QIcon('Resources/zw.ico'))
        self.setMinimumWidth(600)
        self.widget = QWidget()
        self.label1 = QLabel("Digite o ajuste furo-eixo desejado")
        self.label2 = QLabel()
        self.label2.setFixedHeight(5)
        self.label2.setStyleSheet("background-color: black")
        self.button1 = QPushButton("Converter!")
        self.button1.setFixedHeight(40)
        self.button1.clicked.connect(self.__button_clicked_action_performed)
        self.textedit1 = QTextEdit()
        self.textedit1.setFixedHeight(50)
        self.textedit1.setFontPointSize(18)
        self.textedit1.setPlaceholderText("ex: 40H7/g6")
        self.textedit1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textedit2 = QTextEdit()
        self.textedit2.setReadOnly(True)
        self.textedit2.zoomIn(10)
        self.textedit2.setFixedHeight(400)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.textedit1)
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.textedit2)

        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def __button_clicked_action_performed(self):
        try:
            instr = self.textedit1.toPlainText()
            indata = bt.input_parser(instr)
            bt.input_validator(indata)
            axledata = bt.calculate_asymmetric_tol_dimension_axle(indata)
            holedata = bt.calculate_asymmetric_tol_dimension_hole(indata)
            self.__fill_text_data(holedata, axledata)
            self.__plot_field_data(holedata, axledata)
        except ValueError as ve:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Erro!")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText(str(ve))
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.exec()
        except Exception as ee:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Erro!")
            dlg.setIcon(QMessageBox.Icon.Critical)
            dlg.setText(str(ee))
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.exec()

    def __fill_text_data(self, holedata: bt.AsymmetricToleranceDimension, axledata: bt.AsymmetricToleranceDimension):
        straux = ''
        straux += '<div style="text-align:center">'
        straux += '<table><tr>'
        straux += '<td><h1>Furo: </h1>'
        straux += holedata.get_html_string()
        straux += '</td><td><span> &nbsp; &nbsp; &nbsp; </span></td>'
        straux += '<td><h1>Eixo: </h1>'
        straux += axledata.get_html_string()
        straux += '</td></tr></table></div><br>\n\n'
        straux += 'Tipo de Ajuste: <b>'
        fit_type = bt.AsymmetricToleranceDimension.calc_fit_type(holedata, axledata)
        straux += fit_type
        straux += '</b><br><br>'
        if fit_type == bt.AsymmetricToleranceDimension.fit_type_gap:
            gaps = bt.AsymmetricToleranceDimension.calc_clearance_limits(holedata, axledata)
            straux += f'Folga mínima = {min(gaps) / 1000:.3f} mm <br>'
            straux += f'Folga máxima = {max(gaps) / 1000:.3f} mm <br>'
            straux += f'Folga média = {sum(gaps) / 2000:.4f} mm <br>'
        if fit_type == bt.AsymmetricToleranceDimension.fit_type_interf:
            interfs = bt.AsymmetricToleranceDimension.calc_interference_limits(holedata, axledata)
            straux += f'Interferência mínima = {min(interfs) / 1000:.3f} mm <br>'
            straux += f'Interferência máxima = {max(interfs) / 1000:.3f} mm <br>'
            straux += f'Interferência média = {sum(interfs) / 2000:.4f} mm <br>'
        self.textedit2.setText(straux)

    def __plot_field_data(self, holedata: bt.AsymmetricToleranceDimension, axledata: bt.AsymmetricToleranceDimension):
        fit_type = bt.AsymmetricToleranceDimension.calc_fit_type(holedata, axledata)

        plt.close(plt.gcf())

        fig = plt.figure()
        plt.plot([0, 10], [holedata.dim, holedata.dim], 'k-', linewidth=3, label="Linha Zero")
        plt.fill_between([0.5, 4.5],
                         [holedata.dim + holedata.lower_tol / 1e3, holedata.dim + holedata.lower_tol / 1e3],
                         [holedata.dim + holedata.upper_tol / 1e3, holedata.dim + holedata.upper_tol / 1e3],
                         color=[0.5, 0.1, 0.1], label="Campo: Furo")
        plt.fill_between([5.5, 9.5],
                         [axledata.dim + axledata.lower_tol / 1e3, axledata.dim + axledata.lower_tol / 1e3],
                         [axledata.dim + axledata.upper_tol / 1e3, axledata.dim + axledata.upper_tol / 1e3],
                         color=[0.1, 0.1, 0.5], label="Campo: Eixo")
        plt.legend()
        plt.grid(True)
        plt.gca().set_axisbelow(True)
        plt.ylabel("Medida [mm]")
        plt.title("Tipo de ajuste: " + fit_type)
        plt.get_current_fig_manager().window.setGeometry(self.x() + self.width() + 5, self.y() + 30, 720, 500)
        ticks = sorted([axledata.mindim, axledata.maxdim, holedata.mindim, holedata.maxdim])
        plt.gca().set_yticks(ticks)
        plt.show()
