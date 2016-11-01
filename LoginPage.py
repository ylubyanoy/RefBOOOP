from settings import *
import sys
from PyQt5 import QtWidgets, uic, QtSql
import UsersForm
import MainForm


class MyLoginWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        global db
        self.DBPass = None
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/LoginMainForm.ui", self)
        # Настройка окна авторизации
        self.setWindowTitle("Авторизация")
        self.setFixedSize(584, 156)
        self.status_init()
        # self.pushButton.setStyleSheet(S_PUSH_BUTTON_OK)
        # self.btnCancel.setStyleSheet(S_PUSH_BUTTON_CANCEL)
        self.pushButton.setEnabled(False)
        # Подключение обработчиков для кнопок
        self.pushButton.clicked.connect(self.on_clicked_ok_login)
        self.btnCancel.clicked.connect(self.on_clicked_cancel_login)
        self.btnSelectUser.clicked.connect(self.on_clicked_select_login)
        self.PassEdit.textEdited[str].connect(self.on_pass_edit_changed)

    def status_init(self):
        if db.open():
            self.statusBar().setStyleSheet(
                "QStatusBar{padding-left:8px;background:rgba(47,117,46,1);color:black;font-weight:bold;}")
            self.statusBar().showMessage('Подключено')
        else:
            self.status.setStyleSheet(
                "QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:black;font-weight:bold;}")
            self.statusBar().showMessage('Нет подключения')

    def on_pass_edit_changed(self, text):
        if text == self.DBPass:
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def on_clicked_select_login(self):
        uw = UsersForm.MyUsersWindow(self, db=db)
        uw.exec()
        if uw.username is not None:
            self.UserEdit.setText(uw.username.strip())
            self.DBPass = uw.password.strip()
            self.PassEdit.setFocus()

    def on_clicked_cancel_login(self):
        if db.isOpen():
            db.close()
        db.removeDatabase(db.databaseName())
        QtWidgets.qApp.quit()

    def on_clicked_ok_login(self):
        mf = MainForm.MyMainWindow(self, db=db)
        mf.exec()


def connect_to_db():
    db_oops = QtSql.QSqlDatabase.addDatabase('QPSQL')
    db_oops.setHostName(DB_HOST)
    db_oops.setPort(DB_PORT)
    db_oops.setDatabaseName(DB_NAME)
    db_oops.setUserName(DB_USER)
    db_oops.setPassword(DB_PASS)
    if not db_oops.open():
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Ошибка подключения к БД: {0}".format(db_oops.lastError().text()))
    return db_oops

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    db = connect_to_db()
    w = MyLoginWindow()
    w.show()
    sys.exit(app.exec_())
