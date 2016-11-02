from PyQt5 import QtCore, QtWidgets, uic, QtSql
import DoDataForm as df


class MyMainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, db=None):
        self.db = db
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/MainForm.ui", self)
        self.btnCloseMainForm.clicked.connect(self.on_clicked_cancel)
        self.btnAddRecord.clicked.connect(self.on_add_record)
        self.btnDelRecord.clicked.connect(self.on_delete_record)
        self.btnEditRecord.clicked.connect(self.on_edit_record)
        self.setWindowTitle("Справочник первичных профсоюзных организаций Белгородского"
                            " областного объединения организаций профсоюзов")
        self.username = None
        self.password = None
        # Словарь с данными для редактирования и сохранения в БД
        self.dict_data = {}

        if self.db.isOpen():
            self.stm = QtSql.QSqlRelationalTableModel()
            self.stm.setTable("preds")
            self.stm.setRelation(11, QtSql.QSqlRelation('otrasli', 'id_otrasl', 'otname'))
            self.stm.setRelation(12, QtSql.QSqlRelation('rayons', 'id_rayon', 'rayonname'))
            self.stm.select()
            self.stm.setHeaderData(0, QtCore.Qt.Horizontal, "id")
            self.stm.setHeaderData(1, QtCore.Qt.Horizontal, "Наименование организации")
            self.stm.setHeaderData(2, QtCore.Qt.Horizontal, "Должность\nруководителя")
            self.stm.setHeaderData(3, QtCore.Qt.Horizontal, "Руководитель\nорганизации")
            self.stm.setHeaderData(4, QtCore.Qt.Horizontal, "Телефон\nруководитель")
            self.stm.setHeaderData(5, QtCore.Qt.Horizontal, "Должность\nпредседателя")
            self.stm.setHeaderData(6, QtCore.Qt.Horizontal, "Председатель\nпервичной\nпрофсоюзной\nорганизации")
            self.stm.setHeaderData(7, QtCore.Qt.Horizontal, "Телефон\nпрофсоюз")
            self.stm.setHeaderData(8, QtCore.Qt.Horizontal, "Численность\nработников")
            self.stm.setHeaderData(9, QtCore.Qt.Horizontal, "Численность\nчленов\nпрофсоюза")
            self.stm.setHeaderData(11, QtCore.Qt.Horizontal, "Отрасль")
            self.stm.setHeaderData(12, QtCore.Qt.Horizontal, "Район")

            self.tvMain.setModel(self.stm)

            self.tvMain.setColumnWidth(1, 300)
            self.tvMain.setColumnWidth(2, 150)
            self.tvMain.setColumnWidth(3, 150)
            self.tvMain.setColumnWidth(4, 100)
            self.tvMain.setColumnWidth(5, 150)
            self.tvMain.setColumnWidth(6, 150)
            self.tvMain.setColumnWidth(7, 100)
            self.tvMain.setColumnWidth(8, 100)
            self.tvMain.setColumnWidth(9, 100)
            self.tvMain.setColumnWidth(11, 150)
            self.tvMain.setColumnWidth(12, 150)

            self.tvMain.hideColumn(0)
            self.tvMain.hideColumn(10)
            self.tvMain.hideColumn(13)
            self.tvMain.hideColumn(14)
            self.tvMain.hideColumn(15)
            self.tvMain.hideColumn(16)

            self.tvMain.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def on_add_record(self):
        fm_add_data = df.DoDataForm(self, do_type=1)
        fm_add_data.exec()
        self.stm.select()

    def on_delete_record(self):
        button = QtWidgets.QMessageBox.question(None, "Удаление данных", "Удалить запись '{}'?"
                                                .format(self.stm.index(self.tvMain.currentIndex().row(), 1).data()))
        if button == QtWidgets.QMessageBox.Yes:
            self.delete_pred(self.stm.index(self.tvMain.currentIndex().row(), 0).data())

    def delete_pred(self, pred_id):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM preds WHERE id_pred=:pred_id")
        query.bindValue(':pred_id', pred_id)
        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", query.lastError().text())
        else:
            self.stm.submit()
            self.stm.select()

    def on_clicked_cancel(self):
        self.close()

    def on_edit_record(self):
        self.dict_data = {'EditPredName': self.stm.index(self.tvMain.currentIndex().row(), 1).data(),
                          'sbWorkers': self.stm.index(self.tvMain.currentIndex().row(), 8).data(),
                          'sbProfs': self.stm.index(self.tvMain.currentIndex().row(), 9).data(),
                          'EditWPosition': self.stm.index(self.tvMain.currentIndex().row(), 2).data(),
                          'EditWFIO': self.stm.index(self.tvMain.currentIndex().row(), 3).data(),
                          'EditWTel': self.stm.index(self.tvMain.currentIndex().row(), 4).data(),
                          'EditPPosition': self.stm.index(self.tvMain.currentIndex().row(), 5).data(),
                          'EditPFIO': self.stm.index(self.tvMain.currentIndex().row(), 6).data(),
                          'EditPTel': self.stm.index(self.tvMain.currentIndex().row(), 7).data(),
                          'EditAdress': self.stm.index(self.tvMain.currentIndex().row(), 10).data(),
                          'otrasl_name': self.stm.index(self.tvMain.currentIndex().row(), 11).data(),
                          'rayon_name': self.stm.index(self.tvMain.currentIndex().row(), 12).data(),
                          'id_pred': self.stm.index(self.tvMain.currentIndex().row(), 0).data()
                          }

        fm_edit_data = df.DoDataForm(self, do_type=2, dict_data=self.dict_data)
        fm_edit_data.exec()
        self.stm.selectRow(self.tvMain.currentIndex().row())
