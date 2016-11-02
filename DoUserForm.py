from PyQt5 import QtCore, QtWidgets, uic, QtSql


class UserForm(QtWidgets.QDialog):
    def __init__(self, parent=None, do_type=1, otrasl_name="<Пустое значение>"):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/DoUserForm.ui", self)
        # Настройка окна Добавления/редактирования пользователя
        self.setFixedSize(613, 234)
        self.setWindowTitle("Новый пользователь") if do_type == 1 else self.setWindowTitle(
            "Редактирование пользователя")
        # Подключение обработчиков для кнопок
        self.btnSave.clicked.connect(self.on_clicked_save)
        self.btnCancel.clicked.connect(self.on_clicked_cancel)
        # Переменные для новых значений
        self.username = None
        self.password = None
        self.is_admin = False
        self.otrasl_id = 0
        self.otrasl_name = otrasl_name
        self.is_booop = False
        # Инициализация формы
        self.otrasli_init(do_type)

    def otrasli_init(self, do_type):
        self.cboOtrasl.clear()
        query = QtSql.QSqlQuery()
        query.exec("SELECT id_otrasl, otname FROM otrasli")
        if query.isActive():
            query.first()
            while query.isValid():
                self.cboOtrasl.addItem(query.value('otname'), int(query.value('id_otrasl')))
                query.next()
        if do_type == 1:
            self.cboOtrasl.addItem("<Пустое значение>", 0)
        self.cboOtrasl.setCurrentIndex(self.cboOtrasl.findText(self.otrasl_name))

    def set_username(self, username):
        self.leUserName.setText(username)

    def set_pass(self, password):
        self.lePassword.setText(password)

    def set_admin_flag(self, state_flag):
        if state_flag:
            self.cbIsAdmin.setCheckState(QtCore.Qt.Checked)
        else:
            self.cbIsAdmin.setCheckState(QtCore.Qt.Unchecked)

    def set_booop_flag(self, state_flag):
        if state_flag:
            self.cbIsBOOOP.setCheckState(QtCore.Qt.Checked)
        else:
            self.cbIsBOOOP.setCheckState(QtCore.Qt.Unchecked)

    def on_clicked_cancel(self):
        self.close()

    def on_clicked_save(self):
        if not self.leUserName.text() and not self.leUserName.text().isalnum():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите имя пользователя")
            return
        if not self.lePassword.text() and not self.lePassword.text().isalnum():
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Введите имя пользователя")
            return
        self.username = self.leUserName.text()
        self.password = self.lePassword.text()
        self.is_admin = self.cbIsAdmin.checkState()
        self.otrasl_id = self.cboOtrasl.itemData(self.cboOtrasl.currentIndex())
        self.otrasl_name = self.cboOtrasl.itemText(self.cboOtrasl.currentIndex())
        self.is_booop = self.cbIsBOOOP.checkState()
        self.close()


