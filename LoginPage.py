from PyQt5 import QtWidgets, uic, QtSql
import UsersForm
import MainForm
import SettingsForm


class MyLoginPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None, db_is_open=False):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        uic.loadUi("Forms/LoginMainForm.ui", self)
        # Настройка окна авторизации
        self.setWindowTitle("Авторизация")
        self.setFixedSize(584, 156)
        # Инициализация статусной строки
        self.status_init(db_is_open)

        # self.pushButton.setStyleSheet(S_PUSH_BUTTON_OK)
        # self.btnCancel.setStyleSheet(S_PUSH_BUTTON_CANCEL)
        self.dict_user = {}
        self.pushButton.setEnabled(False)
        # Подключение обработчиков для кнопок
        self.pushButton.clicked.connect(self.on_clicked_ok_login)
        self.btnCancel.clicked.connect(self.on_clicked_cancel_login)
        self.btnSelectUser.clicked.connect(self.on_clicked_select_login)
        self.PassEdit.textEdited[str].connect(self.on_pass_edit_changed)
        self.btnConfig.clicked.connect(self.on_click_settings)

    def status_init(self, db_is_open):
        if db_is_open:
            self.statusBar().setStyleSheet(
                "QStatusBar{padding-left:8px;background:rgba(47,117,46,1);color:black;font-weight:bold;}")
            self.statusBar().showMessage('Подключено')
        else:
            self.statusBar().setStyleSheet(
                "QStatusBar{padding-left:8px;background:rgba(255,0,0,255);color:black;font-weight:bold;}")
            self.statusBar().showMessage('Нет подключения')

    def on_click_settings(self):
        sf = SettingsForm.MySettingsWindow(self)
        sf.exec()

    def on_pass_edit_changed(self, text):
        if text == self.dict_user['password']:
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
        if text == 'Admin123':
            self.btnConfig.setEnabled(True)
        else:
            self.btnConfig.setEnabled(False)

    def on_clicked_select_login(self):
        uw = UsersForm.MyUsersWindow(self)
        uw.exec()
        self.dict_user = uw.dict_user
        if self.dict_user['username']:
            self.UserEdit.setText(self.dict_user['username'])
            self.PassEdit.setFocus()

    def on_clicked_cancel_login(self):
        self.close()

    def on_clicked_ok_login(self):
        mf = MainForm.MyMainWindow(self)
        mf.dict_user = self.dict_user
        mf.exec()



