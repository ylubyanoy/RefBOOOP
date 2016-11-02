from PyQt5 import QtWidgets, uic, QtSql
import UsersForm
import MainForm


class MyLoginPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None, db=None):
        self.db = db
        self.DBPass = None
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi("Forms/LoginMainForm.ui", self)
        # Настройка окна авторизации
        self.setWindowTitle("Авторизация")
        self.setFixedSize(584, 156)
        # Инициализация статусной строки
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
        if self.db.open():
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
        uw = UsersForm.MyUsersWindow(self, db=self.db)
        uw.exec()
        if uw.username is not None:
            self.UserEdit.setText(uw.username.strip())
            self.DBPass = uw.password.strip()
            self.PassEdit.setFocus()

    def on_clicked_cancel_login(self):
        if self.db.isOpen():
            self.db.close()
            self.db.removeDatabase(self.db.databaseName())
        QtWidgets.qApp.quit()

    def on_clicked_ok_login(self):
        mf = MainForm.MyMainWindow(self, db=self.db)
        mf.exec()



