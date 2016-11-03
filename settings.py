import shelve


# Database parameters
db_conn_default = {'db_user': "postgres",
                   'db_pass': "12345",
                   'db_name': "BookOOPS",
                   'db_host': "localhost",
                   'db_port': 5432}

# Имя файла настроек
SETTINGS_NAME = 'settings'


def settings_load():
    dict_settings = {}
    settings_file = shelve.open(SETTINGS_NAME)
    if settings_file:
        dict_settings['db_user'] = settings_file[SETTINGS_NAME][0]
        dict_settings['db_pass'] = settings_file[SETTINGS_NAME][1]
        dict_settings['db_name'] = settings_file[SETTINGS_NAME][2]
        dict_settings['db_host'] = settings_file[SETTINGS_NAME][3]
        dict_settings['db_port'] = settings_file[SETTINGS_NAME][4]

        settings_file.close()

        return dict_settings
    else:
        return None


def settings_save(settings_values):
    settings_file = shelve.open(SETTINGS_NAME)
    if settings_file:
        # settings_values = [dict_values['leUserName'], dict_values['lePassword'], dict_values['leDBName'],
        #                    dict_values['leDBHost'], dict_values['leDBPort']]
        # settings_values = [settings_values[0], settings_values[1], settings_values[2],
        #                    settings_values[3], settings_values[4]]
        settings_file['settings'] = settings_values
        settings_file.close()

        return True
    else:
        return False

# Styles for interfaces
S_PUSH_BUTTON_OK = """
                QPushButton {
                    background-color: #054a2e;
                    border-style: outset;
                    border-width: 2px;
                    border-radius: 10px;
                    border-color: beige;
                    font: bold 12px;
                    min-width: 8em;
                    padding: 6px;
                    }
                QPushButton:pressed{
                    background-color: #4CAF50;
                    color: white;
                    border-color: black;
                    border-style: inset;
                    }
                QPushButton:hover{
                            background-color: #11cf1d;
                            color: white;
                            border-color: black;
                            border-style: inset;
                            }
                """
S_PUSH_BUTTON_CANCEL = """
                        QPushButton {
                            background-color: #054a2e;
                            border-style: outset;
                            border-width: 2px;
                            border-radius: 10px;
                            border-color: beige;
                            font: bold 12px;
                            min-width: 8em;
                            padding: 6px;
                            }
                        QPushButton:pressed{
                            background-color: #4CAF50;
                            color: white;
                            border-color: black;
                            border-style: inset;
                            }
                        QPushButton:hover{
                            background-color: #a61111;
                            color: white;
                            border-color: black;
                            border-style: inset;
                            }
                        """
