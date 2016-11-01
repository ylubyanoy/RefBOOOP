from PyQt5 import QtCore, QtWidgets, uic, QtSql
import DoUserForm as uf


class MyUsersWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, db=None):
        self.db = db
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/UsersForm.ui", self)
        self.btnCancel.clicked.connect(self.on_clicked_cancel_user)
        self.btnSelectUser.clicked.connect(self.on_clicked_select_user)
        self.btnAddRecord.clicked.connect(self.on_add_user)
        self.btnDelRecord.clicked.connect(self.on_delete_user)
        self.btnEditRecord.clicked.connect(self.on_edit_user)
        self.setWindowTitle("Выберите пользователя")
        self.username = None
        self.password = None

        if self.db.isOpen():
            self.stm = QtSql.QSqlRelationalTableModel()
            self.stm.setJoinMode(QtSql.QSqlRelationalTableModel.LeftJoin)
            self.stm.setTable("usersdb")
            self.stm.setRelation(4, QtSql.QSqlRelation('otrasli', 'id_otrasl', 'otname'))
            self.stm.select()
            self.stm.setHeaderData(0, QtCore.Qt.Horizontal, "id")
            self.stm.setHeaderData(1, QtCore.Qt.Horizontal, "Имя пользователя")
            self.stm.setHeaderData(2, QtCore.Qt.Horizontal, "Пароль")
            self.stm.setHeaderData(3, QtCore.Qt.Horizontal, "ADMIN")
            self.stm.setHeaderData(4, QtCore.Qt.Horizontal, "Отрасль")
            self.stm.setHeaderData(5, QtCore.Qt.Horizontal, "BOOOP")
            self.tvUsers.setModel(self.stm)
            self.tvUsers.hideColumn(0)
            self.tvUsers.setColumnWidth(1, 150)
            self.tvUsers.setColumnWidth(2, 150)
            self.tvUsers.setColumnWidth(3, 80)
            self.tvUsers.setColumnWidth(4, 300)
            self.tvUsers.setColumnWidth(5, 80)
            self.tvUsers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def on_add_user(self):
        fm_add_user = uf.UserForm(self, do_type=1)
        fm_add_user.exec()
        if fm_add_user.username is not None and fm_add_user.password is not None:
            new_index = self.stm.rowCount()
            self.stm.insertRow(new_index)
            self.stm.setData(self.stm.index(new_index, 1), fm_add_user.username)
            self.stm.setData(self.stm.index(new_index, 2), fm_add_user.password)
            self.stm.setData(self.stm.index(new_index, 3), 1 if fm_add_user.is_admin else 0)
            self.stm.setData(self.stm.index(new_index, 4), fm_add_user.otrasl_id)
            self.stm.setData(self.stm.index(new_index, 5), 1 if fm_add_user.is_booop else 0)
            self.stm.submit()
            self.stm.select()

    def on_delete_user(self):
        button = QtWidgets.QMessageBox.question(None, "Удаление пользователя", "Удалить пользователя '{}'?"
                                                .format(self.stm.index(self.tvUsers.currentIndex().row(), 1).data().strip()))
        if button == QtWidgets.QMessageBox.Yes:
            self.delete_user(self.stm.index(self.tvUsers.currentIndex().row(), 0).data())

    def delete_user(self, user_id):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE FROM usersdb WHERE id_user=:sel_user")
        query.bindValue(':sel_user', user_id)
        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", query.lastError().text())
        else:
            self.stm.submit()
            self.stm.select()

    def on_clicked_select_user(self):
        self.username = self.stm.index(self.tvUsers.currentIndex().row(), 1).data()
        self.password = self.stm.index(self.tvUsers.currentIndex().row(), 2).data()
        self.close()

    def on_clicked_cancel_user(self):
        self.close()

    def on_edit_user(self):
        otrasl_name = self.stm.index(self.tvUsers.currentIndex().row(), 4).data()
        fm_edit_user = uf.UserForm(self, do_type=2, otrasl_name=otrasl_name)
        fm_edit_user.set_username(self.stm.index(self.tvUsers.currentIndex().row(), 1).data().strip())
        fm_edit_user.set_pass(self.stm.index(self.tvUsers.currentIndex().row(), 2).data().strip())
        fm_edit_user.set_admin_flag(self.stm.index(self.tvUsers.currentIndex().row(), 3).data())
        fm_edit_user.set_booop_flag(self.stm.index(self.tvUsers.currentIndex().row(), 5).data())
        fm_edit_user.exec()
        if fm_edit_user.username is not None and fm_edit_user.password is not None:
            edit_index = self.tvUsers.currentIndex().row()
            rec = self.stm.record(edit_index)
            rec.setValue(1, fm_edit_user.username)
            rec.setValue(2, fm_edit_user.password)
            rec.setValue(3, True if fm_edit_user.is_admin else False)
            rec.setValue(4, fm_edit_user.otrasl_id)
            rec.setValue(5, True if fm_edit_user.is_booop else False)
            self.stm.setRecord(edit_index, rec)
            self.stm.submit()
            self.stm.selectRow(edit_index)


