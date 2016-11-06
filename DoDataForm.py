from PyQt5 import QtCore, QtWidgets, uic, QtSql

EMPTY_TEXT = "<Пустое значение>"
EMPTY_DATA = 0


class DoDataForm(QtWidgets.QDialog):
    def __init__(self, parent=None, do_type=1, pred_id=0):
        super(QtWidgets.QDialog, self).__init__(parent)
        uic.loadUi("Forms/DoDataForm.ui", self)
        # Настройка окна Добавления/редактирования данных
        self.setWindowTitle("Добавить информацию") if do_type == 1 else self.setWindowTitle("Редактировать информацию")
        # Подключение обработчиков для кнопок
        self.btnSave.clicked.connect(self.on_clicked_save)
        self.btnCancel.clicked.connect(self.on_clicked_cancel)
        # Инициализация формы
        self.do_type = do_type
        self.pred_id = pred_id
        self.dict_data_form = {}
        self.dict_user = {}

        self.data_init(self.do_type)

    def data_init(self, do_type):
        # Подготовить данные
        if do_type == 2:
            self.dict_data_form = self.select_preds(self.pred_id)

            self.EditPredName.setText(self.dict_data_form['EditPredName'])
            self.sbWorkers.setValue(self.dict_data_form['sbWorkers'])
            self.sbProfs.setValue(self.dict_data_form['sbProfs'])
            self.EditWPosition.setText(self.dict_data_form['EditWPosition'])
            self.EditWFIO.setText(self.dict_data_form['EditWFIO'])
            self.EditWTel.setText(self.dict_data_form['EditWTel'])
            self.EditPPosition.setText(self.dict_data_form['EditPPosition'])
            self.EditPFIO.setText(self.dict_data_form['EditPFIO'])
            self.EditPTel.setText(self.dict_data_form['EditPTel'])
            self.EditAdress.setText(self.dict_data_form['EditAdress'])

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
            self.cmbOtrasl.addItem(EMPTY_TEXT, EMPTY_DATA)
        self.cmbOtrasl.setCurrentIndex(self.cmbOtrasl.findData(self.dict_data_form.get('id_otrasl', EMPTY_DATA)))

        # Подготовить Районы
        self.cmbRayon.clear()
        query = QtSql.QSqlQuery()
        query.exec("SELECT id_rayon, rayonname FROM rayons")
        if query.isActive():
            query.first()
            while query.isValid():
                self.cmbRayon.addItem(query.value('rayonname'), int(query.value('id_rayon')))
                query.next()
        if do_type == 1:
            self.cmbRayon.addItem(EMPTY_TEXT, EMPTY_DATA)
        self.cmbRayon.setCurrentIndex(self.cmbRayon.findData(self.dict_data_form.get('id_rayon', EMPTY_DATA)))

    def on_clicked_cancel(self):
        self.close()

    def on_clicked_save(self):
        self.dict_data_form['EditPredName'] = self.EditPredName.text()
        self.dict_data_form['sbWorkers'] = self.sbWorkers.value()
        self.dict_data_form['sbProfs'] = self.sbProfs.value()
        self.dict_data_form['EditWPosition'] = self.EditWPosition.text()
        self.dict_data_form['EditWFIO'] = self.EditWFIO.text()
        self.dict_data_form['EditWTel'] = self.EditWTel.text()
        self.dict_data_form['EditPPosition'] = self.EditPPosition.text()
        self.dict_data_form['EditPFIO'] = self.EditPFIO.text()
        self.dict_data_form['EditPTel'] = self.EditPTel.text()
        self.dict_data_form['EditAdress'] = self.EditAdress.text()

        self.dict_data_form['id_user'] = self.dict_user['id_user']
        self.dict_data_form['id_otrasl'] = self.cmbOtrasl.itemData(self.cmbOtrasl.currentIndex())
        self.dict_data_form['id_rayon'] = self.cmbRayon.itemData(self.cmbRayon.currentIndex())

        # Запись новых данных
        if self.do_type == 1:
            self.dict_data_form['id_pred'] = self.insert_preds(self.dict_data_form)
            if self.dict_data_form['id_pred']:
                self.close()

        # Запись отредактированных данных
        elif self.do_type == 2 and self.update_preds(self.dict_data_form):
            self.close()

    def update_preds(self, dict_data_upd):
        """Редактирование и запись данных в таблицу Preds"""
        # Проверка заполнения данных
        if not self.dict_data_form['EditPredName'] \
                or not self.dict_data_form['id_otrasl'] \
                or not self.dict_data_form['id_rayon']:

            QtWidgets.QMessageBox.warning(None, "Редактирование",
                                          "Ошибка при записи! Не все обязательные поля заполнены")
            return False

        query = QtSql.QSqlQuery()
        query.prepare("UPDATE preds SET prname=:prname, rukdolgnost=:rukdolgnost, rukfio=:rukfio, ruktel=:ruktel, "
                      "profdolgnost=:profdolgnost, proffio=:proffio, proftel=:proftel, rabcount=:rabcount, "
                      "profcount=:profcount, adress=:adress, otraslid=:otraslid, rayonid=:rayonid "  # , userid=:id_user
                      "WHERE id_pred=:id_pred")

        query.bindValue(':prname', dict_data_upd['EditPredName'])
        query.bindValue(':rukdolgnost', dict_data_upd['EditWPosition'])
        query.bindValue(':rukfio', dict_data_upd['EditWFIO'])
        query.bindValue(':ruktel', dict_data_upd['EditWTel'])
        query.bindValue(':profdolgnost', dict_data_upd['EditPPosition'])
        query.bindValue(':proffio', dict_data_upd['EditPFIO'])
        query.bindValue(':proftel', dict_data_upd['EditPTel'])
        query.bindValue(':rabcount', dict_data_upd['sbWorkers'])
        query.bindValue(':profcount', dict_data_upd['sbProfs'])
        query.bindValue(':adress', dict_data_upd['EditAdress'])
        query.bindValue(':otraslid', dict_data_upd['id_otrasl'])
        query.bindValue(':rayonid', dict_data_upd['id_rayon'])

        # query.bindValue(':id_user', dict_data_upd['id_user'])
        query.bindValue(':id_pred', dict_data_upd['id_pred'])

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Редактирование", "Ошибка при записи: {0}".format(query.lastError().text()))
            return False
        else:
            return True

    def insert_preds(self, dict_data_ins):
        """Запись новых данных в таблицу Preds"""
        # Проверка заполнения данных
        if not self.dict_data_form['EditPredName'] \
                or not self.dict_data_form['id_otrasl'] \
                or not self.dict_data_form['id_rayon']:

            QtWidgets.QMessageBox.warning(None, "Новая запись", "Ошибка при записи! Не все обязательные поля заполнены")
            return 0

        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO preds (prname, rukdolgnost, rukfio, ruktel, profdolgnost, proffio, proftel, rabcount, "
                      "profcount, adress, otraslid, rayonid, userid) "
                      "VALUES (:prname, :rukdolgnost, :rukfio, :ruktel, :profdolgnost, :proffio, :proftel, :rabcount, "
                      ":profcount, :adress, :otraslid, :rayonid, :id_user)")

        query.bindValue(':prname', dict_data_ins['EditPredName'])
        query.bindValue(':rukdolgnost', dict_data_ins['EditWPosition'])
        query.bindValue(':rukfio', dict_data_ins['EditWFIO'])
        query.bindValue(':ruktel', dict_data_ins['EditWTel'])
        query.bindValue(':profdolgnost', dict_data_ins['EditPPosition'])
        query.bindValue(':proffio', dict_data_ins['EditPFIO'])
        query.bindValue(':proftel', dict_data_ins['EditPTel'])
        query.bindValue(':rabcount', dict_data_ins['sbWorkers'])
        query.bindValue(':profcount', dict_data_ins['sbProfs'])
        query.bindValue(':adress', dict_data_ins['EditAdress'])
        query.bindValue(':otraslid', dict_data_ins['id_otrasl'])
        query.bindValue(':rayonid', dict_data_ins['id_rayon'])

        query.bindValue(':id_user', dict_data_ins['id_user'])

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Новая запись",
                                          "Ошибка при записи: {0}".format(query.lastError().text()))
            return 0
        else:
            return query.lastInsertId()

    def select_preds(self, pred_id):
        """Получение данных из таблицы Preds"""

        dict_data = {}

        query = QtSql.QSqlQuery()
        query.prepare("SELECT id_pred, prname, rukdolgnost, rukfio, ruktel, profdolgnost, proffio, proftel, rabcount, "
                      "profcount, adress, otraslid, rayonid FROM preds "
                      "WHERE id_pred=:id_pred")

        query.bindValue(':id_pred', pred_id)

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Выборка данных", "Ошибка: {0}".format(query.lastError().text()))
            return None
        else:
            # Заполнение словаря с данными
            query.first()

            dict_data['EditPredName'] = query.value('prname')
            dict_data['EditWPosition'] = query.value('rukdolgnost')
            dict_data['EditWFIO'] = query.value('rukfio')
            dict_data['EditWTel'] = query.value('ruktel')
            dict_data['EditPPosition'] = query.value('profdolgnost')
            dict_data['EditPFIO'] = query.value('proffio')
            dict_data['EditPTel'] = query.value('proftel')
            dict_data['sbWorkers'] = query.value('rabcount')
            dict_data['sbProfs'] = query.value('profcount')
            dict_data['EditAdress'] = query.value('adress')
            dict_data['id_otrasl'] = query.value('otraslid')
            dict_data['id_rayon'] = query.value('rayonid')

            dict_data['id_pred'] = query.value('id_pred')

            return dict_data
