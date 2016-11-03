import sys
from PyQt5 import QtWidgets, QtSql
import LoginPage
from settings import db_conn_default, settings_load


def connect_to_db(db_conn=None):
    if not db_conn:
        db_conn = db_conn_default

    db_oops = QtSql.QSqlDatabase.addDatabase('QPSQL')
    db_oops.setHostName(db_conn['db_host'])
    db_oops.setPort(int(db_conn['db_port']))
    db_oops.setDatabaseName(db_conn['db_name'])
    db_oops.setUserName(db_conn['db_user'])
    db_oops.setPassword(db_conn['db_pass'])
    try:
        db_oops.open()
    except Exception:
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Ошибка подключения к БД: {0}".format(db_oops.lastError().text()))

    return db_oops

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    try:
        db = connect_to_db(settings_load())
        w = LoginPage.MyLoginPage(db_is_open=db.isOpen())
        if db.isOpen():
            db.close()
            db.removeDatabase(db.databaseName())
    except Exception as err:
        w = LoginPage.MyLoginPage(db_is_open=False)

    w.show()
    sys.exit(app.exec_())
