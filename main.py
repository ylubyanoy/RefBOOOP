import sys
from PyQt5 import QtWidgets, QtSql
import LoginPage
from settings import db_conn


def connect_to_db():
    db_oops = QtSql.QSqlDatabase.addDatabase('QPSQL')
    db_oops.setHostName(db_conn['db_host'])
    db_oops.setPort(db_conn['db_port'])
    db_oops.setDatabaseName(db_conn['db_name'])
    db_oops.setUserName(db_conn['db_user'])
    db_oops.setPassword(db_conn['db_pass'])
    if not db_oops.open():
        QtWidgets.QMessageBox.warning(None, "Ошибка", "Ошибка подключения к БД: {0}".format(db_oops.lastError().text()))
    return db_oops

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    db = connect_to_db()
    w = LoginPage.MyLoginPage(db=db)
    w.show()
    sys.exit(app.exec_())
