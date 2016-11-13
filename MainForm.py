from PyQt5 import QtCore, QtWidgets, uic, QtSql, QtGui
import DoDataForm


class NewQSqlRelationalTableModel(QtSql.QSqlRelationalTableModel):

    def data(self, index, role=None):
        value = QtSql.QSqlRelationalTableModel.data(self, index, role)

        if role == QtCore.Qt.FontRole:
            column15_data = index.sibling(index.row(), 15).data()  # deleteddata
            column16_data = index.sibling(index.row(), 16).data()  # markeddata
            if column15_data == 1:
                font = QtGui.QFont('Arial', 10)
                font.setStrikeOut(True)
                return QtCore.QVariant(font)
            if column16_data == 1:
                font = QtGui.QFont('Arial', 8)
                font.setBold(True)
                return QtCore.QVariant(font)

        if role == QtCore.Qt.TextColorRole:
            column15_data = index.sibling(index.row(), 15).data()  # deleteddata
            column16_data = index.sibling(index.row(), 16).data()  # markeddata
            if column15_data == 1:
                return QtCore.QVariant(QtGui.QColor(QtCore.Qt.darkRed))
            if column16_data == 1:
                return QtCore.QVariant(QtGui.QColor(QtCore.Qt.darkGreen))

        return value


class NewQSortFilterProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(NewQSortFilterProxyModel, self).__init__(parent)
        self.all_key_cols = {}

    def set_filter_key_columns(self, key_cols):
        self.all_key_cols.clear()
        self.all_key_cols = self.all_key_cols.fromkeys(key_cols, "")

    def add_filter_fixed_string(self, col_num, col_str):
        if col_num not in self.all_key_cols:
            return

        self.all_key_cols[col_num] = col_str
        self.invalidateFilter()

    def filterAcceptsRow(self, row, parent):
        """Reimplemented from base class."""
        if not self.all_key_cols:
            return True
        # res = [True if self.sourceModel().index(row, k).data() == v else False for k, v in self.all_key_cols]
        res = []
        for k, v in self.all_key_cols.items():
            try:
                if self.sourceModel().index(row, k).data() == v or v in "":
                    res += [True]
                else:
                    res += [False]
            except TypeError:
                res += [False]

        if not self.all_key_cols:
            res += [True]

        return all(res)


class MyMainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, dict_user=None):
        super(MyMainWindow, self).__init__(parent)

        uic.loadUi("Forms/MainForm.ui", self)

        self.btnCloseMainForm.clicked.connect(self.on_clicked_cancel)
        self.btnAddRecord.clicked.connect(self.on_add_record)
        self.btnDelRecord.clicked.connect(self.on_delete_record)
        self.btnEditRecord.clicked.connect(self.on_edit_record)

        self.tvMain.doubleClicked.connect(self.on_edit_record)

        self.cmbRayons.currentIndexChanged[str].connect(self.rayons_filter_on)
        self.cmbOtrasli.currentIndexChanged[str].connect(self.otrasli_filter_on)

        self.setWindowTitle("Справочник первичных профсоюзных организаций Белгородского"
                            " областного объединения организаций профсоюзов")

        self.dict_user = {} if dict_user is None else dict_user

        self.stm = NewQSqlRelationalTableModel()
        self.stm.setTable("preds")
        self.stm.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.stm.setRelation(11, QtSql.QSqlRelation('otrasli', 'id_otrasl', 'otname'))
        self.stm.setRelation(12, QtSql.QSqlRelation('rayons', 'id_rayon', 'rayonname'))

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
        self.stm.select()

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

        self.tvMain.setAlternatingRowColors(True)
        self.tvMain.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Инициализация фильтров на форме
        self.proxy = NewQSortFilterProxyModel(self)   # QtCore.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.stm)
        self.proxy.setDynamicSortFilter(True)
        # Установка колонок для фильтрации
        if self.dict_user and (not self.dict_user['ADMIN'] and not self.dict_user['BOOOP']):
            self.laOtrasl.setVisible(False)
            self.cmbOtrasli.setVisible(False)
        else:
            self.laOtrasl.setVisible(True)
            self.cmbOtrasli.setVisible(True)

            # Установка модели фильтру по отраслям
            self.cmbOtrasli.blockSignals(True)
            self.otrasli_model = QtSql.QSqlTableModel()
            self.otrasli_model.setTable('otrasli')
            self.otrasli_model.select()

            self.cmbOtrasli.setModel(self.otrasli_model)
            self.cmbOtrasli.setModelColumn(1)
            self.cmbOtrasli.setCurrentIndex(-1)
            self.cmbOtrasli.blockSignals(False)

        filter_key_columns = (11, 12, 15)
        self.proxy.set_filter_key_columns(filter_key_columns)

        if self.dict_user and not self.dict_user['ADMIN']:
            self.proxy.add_filter_fixed_string(15, 0)
        if self.dict_user and (not self.dict_user['ADMIN'] and not self.dict_user['BOOOP']):
            self.proxy.add_filter_fixed_string(11, self.dict_user['otname'])

        # Установка прокси модели таблице
        self.tvMain.setModel(self.proxy)

        # Установка модели фильтру по районам
        self.cmbRayons.blockSignals(True)
        self.rayons_model = QtSql.QSqlTableModel()
        self.rayons_model.setTable('rayons')
        self.rayons_model.select()

        self.cmbRayons.setModel(self.rayons_model)
        self.cmbRayons.setModelColumn(1)
        self.cmbRayons.setCurrentIndex(-1)
        self.cmbRayons.blockSignals(False)

    def rayons_filter_on(self, text):
        self.proxy.add_filter_fixed_string(12, text)

    def otrasli_filter_on(self, text):
        self.proxy.add_filter_fixed_string(11, text)

    def on_add_record(self):
        fm_add_data = DoDataForm.DoDataForm(self, do_type=1)
        fm_add_data.dict_user = self.dict_user
        fm_add_data.exec()
        self.stm.select()

    def on_delete_record(self):
        button = QtWidgets.QMessageBox.question(None, "Удаление данных", "Удалить запись '{}'?"
                                                .format(self.tvMain.model().index(self.tvMain.currentIndex().row(), 1).data()))
        if button == QtWidgets.QMessageBox.Yes:
            self.delete_pred(self.tvMain.model().index(self.tvMain.currentIndex().row(), 0).data())

    def delete_pred(self, pred_id):
        query = QtSql.QSqlQuery()
        query.prepare("UPDATE preds SET deleteddata=1 WHERE id_pred=:pred_id")
        query.bindValue(':pred_id', pred_id)
        if not query.exec_():
            QtWidgets.QMessageBox.warning(None, "Ошибка", query.lastError().text())
        else:
            self.stm.select()

    def on_clicked_cancel(self):
        self.close()
        self.destroy()

    def on_edit_record(self):
        if self.tvMain.model().index(self.tvMain.currentIndex().row(), 0).data():
            fm_edit_data = DoDataForm.DoDataForm(self, do_type=2,
                                                 pred_id=self.tvMain.model().index(self.tvMain.currentIndex().row(), 0).data())
            fm_edit_data.dict_user = self.dict_user
            fm_edit_data.exec()
            self.stm.selectRow(self.tvMain.currentIndex().row())
