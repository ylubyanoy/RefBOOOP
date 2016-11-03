from PyQt5 import QtCore, QtWidgets, uic, QtSql


EMPTY_TEXT = "<Пустое значение>"
EMPTY_DATA = 0

class UserForm(QtWidgets.QDialog):
    def __init__(self, parent=None, do_type=1, id_user=0):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/DoUserForm.ui", self)
        # Настройка окна Добавления/редактирования пользователя
        self.setFixedSize(613, 234)
        self.setWindowTitle("Новый пользователь") if do_type == 1 else self.setWindowTitle(
            "Редактирование пользователя")
        # Подключение обработчиков для кнопок
        self.btnSave.clicked.connect(self.on_clicked_save)
        self.btnCancel.clicked.connect(self.on_clicked_cancel)
        # Инициализация формы
        self.do_type = do_type
        self.id_user = id_user
        self.dict_data_form = {}

        self.users_init(self.do_type)

    def users_init(self, do_type):
        # Подготовить данные
        if do_type == 2:
            self.dict_data_form = self.select_usersdb(self.id_user)

            self.leUserName.setText(self.dict_data_form['leUserName'])
            self.lePassword.setText(self.dict_data_form['lePassword'])
            self.cbIsAdmin.setCheckState(self.dict_data_form['cbIsAdmin'])
            self.cbIsBOOOP.setCheckState(self.dict_data_form['cbIsBOOOP'])

        # Подготовить Отрасли
        self.cboOtrasl.clear()
        query = QtSql.QSqlQuery()
        query.exec("SELECT id_otrasl, otname FROM otrasli")
        if query.isActive():
            query.first()
            while query.isValid():
                self.cboOtrasl.addItem(query.value('otname'), int(query.value('id_otrasl')))
                query.next()
        if do_type == 1:
            self.cboOtrasl.addItem(EMPTY_TEXT, EMPTY_DATA)
        self.cboOtrasl.setCurrentIndex(self.cboOtrasl.findData(self.dict_data_form.get('id_otrasl', EMPTY_DATA)))

    # def set_username(self, username):
    #     self.leUserName.setText(username)
    #
    # def set_pass(self, password):
    #     self.lePassword.setText(password)
    #
    # def set_admin_flag(self, state_flag):
    #     if state_flag:
    #         self.cbIsAdmin.setCheckState(QtCore.Qt.Checked)
    #     else:
    #         self.cbIsAdmin.setCheckState(QtCore.Qt.Unchecked)
    #
    # def set_booop_flag(self, state_flag):
    #     if state_flag:
    #         self.cbIsBOOOP.setCheckState(QtCore.Qt.Checked)
    #     else:
    #         self.cbIsBOOOP.setCheckState(QtCore.Qt.Unchecked)

    def on_clicked_cancel(self):
        self.close()

    def on_clicked_save(self):
        self.dict_data_form['leUserName'] = self.leUserName.text()
        self.dict_data_form['lePassword'] = self.lePassword.text()
        self.dict_data_form['id_otrasl'] = self.cboOtrasl.itemData(self.cboOtrasl.currentIndex())
        self.dict_data_form['cbIsAdmin'] = self.cbIsAdmin.checkState()
        self.dict_data_form['cbIsBOOOP'] = self.cbIsBOOOP.checkState()

        # Запись новых данных
        if self.do_type == 1:
            self.dict_data_form['id_user'] = self.insert_usersdb(self.dict_data_form)
            if self.dict_data_form['id_user']:
                self.close()

        # Запись отредактированных данных
        elif self.do_type == 2 and self.update_usersdb(self.dict_data_form):
            self.close()

    def update_usersdb(self, dict_data_upd):
        """Редактирование и запись данных в таблицу usersdb"""
        # Проверка заполнения данных
        if not self.dict_data_form['leUserName'] or not self.dict_data_form['lePassword']:
            QtWidgets.QMessageBox.warning(None, "Редактирование", "Ошибка при записи! Не все обязательные поля заполнены")
            return False

        query = QtSql.QSqlQuery()
        query.prepare("UPDATE usersdb SET username=:username, userpass=:userpass, isadmin=:isadmin, otraslid=:otraslid, "
                      "isbooop=:isbooop "
                      "WHERE id_user=:id_user")

        query.bindValue(':username', dict_data_upd['leUserName'])
        query.bindValue(':userpass', dict_data_upd['lePassword'])
        query.bindValue(':otraslid', dict_data_upd['id_otrasl'])
        query.bindValue(':isadmin', dict_data_upd['cbIsAdmin'])
        query.bindValue(':isbooop', dict_data_upd['cbIsBOOOP'])

        query.bindValue(':id_user', dict_data_upd['id_user'])

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Редактирование", "Ошибка при записи: {0}".format(query.lastError().text()))
            return False
        else:
            return True

    def insert_usersdb(self, dict_data_ins):
        """Запись новых данных в таблицу usersdb"""
        # Проверка заполнения данных
        if not self.dict_data_form['leUserName'] or not self.dict_data_form['lePassword']:
            QtWidgets.QMessageBox.warning(None, "Новая запись", "Ошибка при записи! Не все обязательные поля заполнены")
            return 0

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO usersdb (username, userpass, isadmin, otraslid, isbooop) "
                      "VALUES (:username, :userpass, :isadmin, :otraslid, :isbooop)")

        query.bindValue(':username', dict_data_ins['leUserName'])
        query.bindValue(':userpass', dict_data_ins['lePassword'])
        query.bindValue(':otraslid', dict_data_ins['id_otrasl'])
        query.bindValue(':isadmin', dict_data_ins['cbIsAdmin'])
        query.bindValue(':isbooop', dict_data_ins['cbIsBOOOP'])

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Новая запись", "Ошибка при записи: {0}".format(query.lastError().text()))
            return 0
        else:
            return query.lastInsertId()

    def select_usersdb(self, id_user):
        """Получение данных из таблицы usersdb"""

        dict_data = {}

        query = QtSql.QSqlQuery()
        query.prepare("SELECT id_user, username, userpass, isadmin, otraslid, isbooop FROM usersdb "
                      "WHERE id_user=:id_user")

        query.bindValue(':id_user', id_user)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Выборка данных", "Ошибка: {0}".format(query.lastError().text()))
            return None
        else:
            # Заполнение словаря с данными
            query.first()

            dict_data['leUserName'] = query.value('username')
            dict_data['lePassword'] = query.value('userpass')
            dict_data['id_otrasl'] = query.value('otraslid')
            dict_data['cbIsAdmin'] = query.value('isadmin')
            dict_data['cbIsBOOOP'] = query.value('isbooop')

            dict_data['id_user'] = query.value('id_user')

            return dict_data


