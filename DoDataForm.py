from PyQt5 import QtCore, QtWidgets, uic, QtSql


class DoDataForm(QtWidgets.QDialog):
    def __init__(self, parent=None, do_type=1):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/DoDataForm.ui", self)
        # Настройка окна Добавления/редактирования данных
        self.setWindowTitle("Добавить информацию") if do_type == 1 else self.setWindowTitle("Редактировать информацию")
        # Подключение обработчиков для кнопок
        self.btnSave.clicked.connect(self.on_clicked_save)
        self.btnCancel.clicked.connect(self.on_clicked_cancel)
        self.data_init(do_type)

    def data_init(self, do_type):
        # Подготовить Отрасли
        self.cmbOtrasl.clear()
        query = QtSql.QSqlQuery()
        query.exec("SELECT id_otrasl, otname FROM otrasli")
        if query.isActive():
            query.first()
            while query.isValid():
                self.cmbOtrasl.addItem(query.value('otname'), int(query.value('id_otrasl')))
                query.next()
        if do_type == 1:
            self.cmbOtrasl.setCurrentIndex(self.cmbOtrasl.findText("<Пустое значение>"))

        # Подготовить Отрасли
        self.cmbRayon.clear()
        # self.cboOtrasl.addItem("<Пустое значение>", 0)
        query = QtSql.QSqlQuery()
        query.exec("SELECT id_rayon, rayonname FROM rayons")
        if query.isActive():
            query.first()
            while query.isValid():
                self.cmbRayon.addItem(query.value('rayonname'), int(query.value('id_rayon')))
                query.next()
        if do_type == 1:
            self.cmbRayon.addItem("<Пустое значение>", 0)
            self.cmbRayon.setCurrentIndex(self.cmbRayon.findText("<Пустое значение>"))

    def on_clicked_cancel(self):
        self.close()

    def on_clicked_save(self):
        pass

