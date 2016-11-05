from PyQt5 import QtCore, QtWidgets, uic, QtSql
import DoUserForm


class MyUsersWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QtWidgets.QDialog, self).__init__(parent)
        uic.loadUi("Forms/UsersForm.ui", self)
        self.btnCancel.clicked.connect(self.on_clicked_cancel_user)
        self.btnSelectUser.clicked.connect(self.on_clicked_select_user)
        self.btnAddRecord.clicked.connect(self.on_add_user)
        self.btnDelRecord.clicked.connect(self.on_delete_user)
        self.btnEditRecord.clicked.connect(self.on_edit_user)
        self.setWindowTitle("Выберите пользователя")
        self.username = None
        self.password = None

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
        fm_add_user = DoUserForm.UserForm(self, do_type=1)
        fm_add_user.exec()
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
            self.stm.select()

    def on_clicked_select_user(self):
        self.username = self.stm.index(self.tvUsers.currentIndex().row(), 1).data()
        self.password = self.stm.index(self.tvUsers.currentIndex().row(), 2).data()
        self.close()

    def on_clicked_cancel_user(self):
        self.close()

    def on_edit_user(self):
        fm_edit_user = DoUserForm.UserForm(self, do_type=2,
                                           id_user=self.stm.index(self.tvUsers.currentIndex().row(), 0).data())
        fm_edit_user.exec()
        self.stm.selectRow(self.tvUsers.currentIndex().row())


