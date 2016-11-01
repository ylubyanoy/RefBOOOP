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
                            " областного объединения организаций профсоюзов ")
        self.username = None
        self.password = None

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
        # if fm_add_user.username is not None and fm_add_user.password is not None:
        #     new_index = self.stm.rowCount()
        #     self.stm.insertRow(new_index)
        #     self.stm.setData(self.stm.index(new_index, 1), fm_add_user.username)
        #     self.stm.setData(self.stm.index(new_index, 2), fm_add_user.password)
        #     self.stm.setData(self.stm.index(new_index, 3), 1 if fm_add_user.is_admin else 0)
        #
        #     self.stm.setData(self.stm.index(new_index, 5), 1 if fm_add_user.is_booop else 0)
        #     self.stm.submit()
        #     self.stm.select()

    def on_delete_record(self):
        pass
        # button = QtWidgets.QMessageBox.question(None, "Удаление пользователя", "Удалить пользователя '{}'?"
        #                                         .format(self.stm.index(self.tvUsers.currentIndex().row(), 1).data().strip()))
        # if button == QtWidgets.QMessageBox.Yes:
        #     self.delete_user(self.stm.index(self.tvUsers.currentIndex().row(), 0).data())

    def delete_record(self, user_id):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM usersdb WHERE id_user=:sel_user")
        query.bindValue(':sel_user', user_id)
        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", query.lastError().text())
        else:
            self.stm.submit()
            self.stm.select()

    def on_clicked_cancel(self):
        self.close()

    def on_edit_record(self):
        fm_add_data = df.DoDataForm(self, do_type=2)
        fm_add_data.exec()
        # fm_edit_user = uf.UserForm(self, do_type=2)
        # fm_edit_user.set_username(self.stm.index(self.tvUsers.currentIndex().row(), 1).data().strip())
        # fm_edit_user.set_pass(self.stm.index(self.tvUsers.currentIndex().row(), 2).data().strip())
        # fm_edit_user.set_admin_flag(self.stm.index(self.tvUsers.currentIndex().row(), 3).data())
        #
        # fm_edit_user.set_booop_flag(self.stm.index(self.tvUsers.currentIndex().row(), 5).data())
        # fm_edit_user.exec()
        # if fm_edit_user.username is not None and fm_edit_user.password is not None:
        #     edit_index = self.tvUsers.currentIndex().row()
        #     rec = self.stm.record(edit_index)
        #     rec.setValue(1, fm_edit_user.username)
        #     rec.setValue(2, fm_edit_user.password)
        #     rec.setValue(3, True if fm_edit_user.is_admin else False)
        #
        #     rec.setValue(5, True if fm_edit_user.is_booop else False)
        #     self.stm.setRecord(edit_index, rec)
        #     self.stm.submit()

