from PyQt5 import QtCore, QtWidgets, uic, QtSql

EMPTY_DATA = "<Пустое значение>"

class DoDataForm(QtWidgets.QDialog):
    def __init__(self, parent=None, do_type=1, dict_data=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/DoDataForm.ui", self)
        # Настройка окна Добавления/редактирования данных
        self.setWindowTitle("Добавить информацию") if do_type == 1 else self.setWindowTitle("Редактировать информацию")
        # Подключение обработчиков для кнопок
        self.btnSave.clicked.connect(self.on_clicked_save)
        self.btnCancel.clicked.connect(self.on_clicked_cancel)
        # Инициализация формы
        self.do_type = do_type
        if dict_data is None:
            self.dict_data_form = {}
        else:
            self.dict_data_form = dict_data

        self.data_init(self.do_type)

    def data_init(self, do_type):
        # Подготовить данные
        if do_type == 2 and self.dict_data_form:
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
            self.cmbOtrasl.addItem(EMPTY_DATA, 0)
        self.cmbOtrasl.setCurrentIndex(self.cmbOtrasl.findText(self.dict_data_form.get('otrasl_name', EMPTY_DATA)))

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
            self.cmbRayon.addItem(EMPTY_DATA, 0)
        self.cmbRayon.setCurrentIndex(self.cmbRayon.findText(self.dict_data_form.get('rayon_name', EMPTY_DATA)))

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

        self.dict_data_form['id_otrasl'] = self.cmbOtrasl.itemData(self.cmbOtrasl.currentIndex())
        self.dict_data_form['id_rayon'] = self.cmbRayon.itemData(self.cmbRayon.currentIndex())

        if self.do_type == 1:
            self.dict_data_form['id_pred'] = self.insert_preds(self.dict_data_form)
            self.close()
        elif self.do_type == 2 and self.update_preds(self.dict_data_form):
            self.close()

    def update_preds(self, dict_data_upd):
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE preds SET prname=:prname, rukdolgnost=:rukdolgnost, rukfio=:rukfio, ruktel=:ruktel, "
                      "profdolgnost=:profdolgnost, proffio=:proffio, proftel=:proftel, rabcount=:rabcount, "
                      "profcount=:profcount, adress=:adress, otraslid=:otraslid, rayonid=:rayonid "
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

        query.bindValue(':id_pred', dict_data_upd['id_pred'])

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Ошибка при записи: {0}".format(query.lastError().text()))
        else:
            return True

    def insert_preds(self, dict_data_ins):
        query = QtSql.QSqlQuery()
        query.prepare("INSERT INTO preds (prname, rukdolgnost, rukfio, ruktel, profdolgnost, proffio, proftel, rabcount, "
                      "profcount, adress, otraslid, rayonid) "
                      "VALUES (:prname, :rukdolgnost, :rukfio, :ruktel, :profdolgnost, :proffio, :proftel, :rabcount, "
                      ":profcount, :adress, :otraslid, :rayonid)")

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

        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Ошибка при записи: {0}".format(query.lastError().text()))
        else:
            return query.lastInsertId()
