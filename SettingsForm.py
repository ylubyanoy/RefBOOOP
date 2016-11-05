from PyQt5 import QtWidgets, uic
import settings


class MySettingsWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(QtWidgets.QDialog, self).__init__(parent)
        uic.loadUi("Forms/SettingsForm.ui", self)
        self.btnCancel.clicked.connect(self.on_cancel_settings)
        self.btnSave.clicked.connect(self.on_save_settings)
        self.setWindowTitle("Настройки подлючения к БД")
        self.leUserName.setFocus()
        # Чтение настроек из файла 'settings'
        self.settings_init()

    def settings_init(self):
        dict_settings = settings.settings_load()
        if dict_settings:
            self.leUserName.setText(dict_settings['db_user'])
            self.lePassword.setText(dict_settings['db_pass'])
            self.leDBName.setText(dict_settings['db_name'])
            self.leDBHost.setText(dict_settings['db_host'])
            self.leDBPort.setText(dict_settings['db_port'])

    def on_save_settings(self):
        settings_values = [self.leUserName.text(), self.lePassword.text(), self.leDBName.text(),
                           self.leDBHost.text(), self.leDBPort.text()]

        settings.settings_save(settings_values)

        self.close()

    def on_cancel_settings(self):
        self.close()



