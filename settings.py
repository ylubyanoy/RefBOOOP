# Database parameters
DB_USER = "postgres"
DB_PASS = "12345"
DB_NAME = "BookOOPS"
DB_HOST = "localhost"
DB_PORT = 5432

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
