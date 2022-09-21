import sys
from PyQt5 import QtWidgets

from Code.defense import attack_protection
from GUI_CODE.gui_main_menu import Ui_MainWindow
from GUI_CODE.gui_menu import Ui_MenuWindow
from GUI_CODE.gui_add import Ui_AddWindow
from GUI_CODE.gui_AdminWindow import Ui_AdminWindow
from GUI_CODE.gui_whatch import Ui_WhatchWindow
from Code import login_logic, db_logic


def out_login():
    app = QtWidgets.QApplication([])
    global application_login_menu
    application_login_menu = login_window()
    application_login_menu.show()
    sys.exit(app.exec())

def open_adm_admin_window():
    global application_admin_adm
    application_admin_adm = adm_admin_window()
    application_login_menu.close()
    application_admin_adm.show()

def back_to_menu_admin_adm():
    global application_login_menu
    application_login_menu = login_window()
    application_admin_adm.close()
    application_login_menu.show()


def open_menu_window():
    global application_adm
    application_adm = admin_menu_window()
    application_login_menu.close()
    application_adm.show()

def back_to_login_adm():
    global application_login_menu
    application_login_menu = login_window()
    application_adm.close()
    application_login_menu.show()

def open_add_window():
    global application_add
    application_add = adm_add_window()
    application_adm.close()
    application_add.show()

def back_to_menu_add_adm():
    global application_adm
    application_adm = admin_menu_window()
    application_add.close()
    application_adm.show()


def open_adm_whatch_window():
    global application_wh
    application_wh = adm_whatch_window()
    application_adm.close()
    application_wh.show()

def back_to_menu_wh_adm():
    global application_adm
    application_adm = admin_menu_window()
    application_wh.close()
    application_adm.show()


class login_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(login_window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.login_res)

    def login_res(self):
        try:
            db_logic.conn()
            log = str(self.ui.login_line.text())
            log = attack_protection(log)
            pas = str(self.ui.password_line.text())
            pas = attack_protection(pas)
            if login_logic.admin_login(log, pas):
                self.ui.login_status.setText('Усаешная авторизация')
                status = db_logic.get_pas_value(login_logic.encode(log), 1)
                if int(status) == 1:
                    open_adm_admin_window()
                else:
                    open_menu_window()
            else:
                self.ui.login_status.setText('Не верный логин или пароль')
        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.login_status.setText(str(ex))
        finally:
            db_logic.end_of_work()


class admin_menu_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(admin_menu_window, self).__init__()
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.ui.exit_button.clicked.connect(back_to_login_adm)
        self.ui.add_button.clicked.connect(open_add_window)
        self.ui.watch_button.clicked.connect(open_adm_whatch_window)


class adm_admin_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(adm_admin_window, self).__init__()
        self.ui = Ui_AdminWindow()
        self.ui.setupUi(self)
        self.ui.back_button.clicked.connect(back_to_menu_admin_adm)

        self.ui.add_user_button.clicked.connect(self.add_user)
        self.ui.del_user_button.clicked.connect(self.del_user)
        self.ui.del_statement.clicked.connect(self.del_statement)

    def add_user(self):
        try:
            db_logic.conn()
            log = login_logic.encode(str(self.ui.new_login_line.text()))
            log = attack_protection(log)
            pas = login_logic.encode(str(self.ui.new_password_line.text()))
            pas = attack_protection(pas)
            print(db_logic.find_users())
            if log not in db_logic.find_users():
                db_logic.fill_users_table(log, pas, 0)
                self.ui.admin_status.setText('новый пользователь добавлен')
            if log == '':
                self.ui.admin_status.setText('заполните поле')

        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.admin_status.setText(str(ex))
        finally:
            db_logic.end_of_work()

    def del_user(self):
        try:
            db_logic.conn()
            login = login_logic.encode(self.ui.del_login_line.text())
            login = attack_protection(login)
            db_logic.del_user(login)
            if login != '':
                self.ui.admin_status.setText('пользователь удалён')
            else:
                self.ui.admin_status.setText('заполните поле')
        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.admin_status.setText(str(ex))
        finally:
            db_logic.end_of_work()

    def del_statement(self):
        try:
            db_logic.conn()
            id = self.ui.del_login_line_2.text()
            id = attack_protection(id)
            pasp = db_logic.get_value_from_victim(id, 2)
            vin_n = db_logic.get_value_from_victim(id, 6)
            gos_n = db_logic.get_value_from_victim(id, 5)
            db_logic.del_statement(str(pasp), str(vin_n), str(gos_n), int(id))
            self.ui.admin_status.setText('объявление удалено')
        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.admin_status.setText(str(ex))
        finally:
            db_logic.end_of_work()


class adm_whatch_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(adm_whatch_window, self).__init__()
        self.ui = Ui_WhatchWindow()
        self.ui.setupUi(self)
        self.ui.exit_button.clicked.connect(back_to_menu_wh_adm)
        self.ui.serch_button.clicked.connect(self.output_statemant_to_screen)

    def output_statemant_to_screen(self):
        try:
            db_logic.conn()
            id = self.ui.serch_line.text()
            id = attack_protection(id)
            id = int(id)
            self.ui.id_statement_line_vi.setText(db_logic.get_value_from_victim(id, 4))
            self.ui.car_gos_num_line.setText(db_logic.get_value_from_victim(id, 5))
            self.ui.vin_line_vi.setText(db_logic.get_value_from_victim(id, 6))
            self.ui.phone_number_line.setText(db_logic.get_value_from_victim(id, 0))
            self.ui.email_line.setText(db_logic.get_value_from_victim(id, 1))
            self.ui.passport_line_vi.setText(db_logic.get_value_from_victim(id, 2))
            self.ui.residential_address_line.setText(db_logic.get_value_from_victim(id, 3))

            pasp = db_logic.get_value_from_victim(id, 2)
            pasp = attack_protection(pasp)
            self.ui.pasp_number_line.setText(db_logic.get_value_from_victims_passport(pasp, 0))
            self.ui.date_of_issue_line.setText(db_logic.get_value_from_victims_passport(pasp, 1))
            self.ui.who_issued_line.setText(db_logic.get_value_from_victims_passport(pasp, 2))
            self.ui.division_code_line.setText(db_logic.get_value_from_victims_passport(pasp, 3))
            self.ui.surname_line.setText(login_logic.rus_decode(db_logic.get_value_from_victims_passport(pasp, 4)))
            self.ui.first_name_line.setText(login_logic.rus_decode(db_logic.get_value_from_victims_passport(pasp, 5)))
            self.ui.dads_name_line.setText(login_logic.rus_decode(db_logic.get_value_from_victims_passport(pasp, 6)))
            self.ui.place_of_residence_line.setText(db_logic.get_value_from_victims_passport(pasp, 7))
            self.ui.born_year_line.setText(db_logic.get_value_from_victims_passport(pasp, 8))
            self.ui.place_of_born_line.setText(db_logic.get_value_from_victims_passport(pasp, 9))

            vin_n = db_logic.get_value_from_victim(id, 6)
            self.ui.vin_number_line.setText(db_logic.get_value_from_pts(vin_n, 0))
            self.ui.marka_line.setText(db_logic.get_value_from_pts(vin_n, 1))
            self.ui.model_line.setText(db_logic.get_value_from_pts(vin_n, 2))
            self.ui.car_type_line.setText(db_logic.get_value_from_pts(vin_n, 3))
            self.ui.category_line.setText(db_logic.get_value_from_pts(vin_n, 4))
            self.ui.year_of_isse_line.setText(db_logic.get_value_from_pts(vin_n, 5))
            self.ui.engine_number_line.setText(db_logic.get_value_from_pts(vin_n, 6))
            self.ui.shassi_number_line.setText(db_logic.get_value_from_pts(vin_n, 7))
            self.ui.color_line.setText(db_logic.get_value_from_pts(vin_n, 8))
            self.ui.power_horse_line.setText(db_logic.get_value_from_pts(vin_n, 9))
            self.ui.poewer_kwt_line.setText(db_logic.get_value_from_pts(vin_n, 10))
            self.ui.engine_size_line.setText(db_logic.get_value_from_pts(vin_n, 11))
            self.ui.zavod_line.setText(db_logic.get_value_from_pts(vin_n, 12))
            self.ui.approval_number_line.setText(db_logic.get_value_from_pts(vin_n, 13))
            self.ui.country_of_import_line.setText(db_logic.get_value_from_pts(vin_n, 14))
            self.ui.gtd_line.setText(db_logic.get_value_from_pts(vin_n, 15))
            self.ui.restrictions_line.setText(db_logic.get_value_from_pts(vin_n, 16))
            self.ui.first_owner_line.setText(db_logic.get_value_from_pts(vin_n, 17))
            self.ui.adsress_of_first_owner_line.setText(db_logic.get_value_from_pts(vin_n, 18))
            self.ui.issued_by_line.setText(db_logic.get_value_from_pts(vin_n, 19))
            self.ui.adress_of_issued_by_line.setText(db_logic.get_value_from_pts(vin_n, 20))
            self.ui.date_of_isse_line.setText(db_logic.get_value_from_pts(vin_n, 21))
            self.ui.engine_name_line.setText(db_logic.get_value_from_pts(vin_n, 22))

            gos_n = db_logic.get_value_from_victim(id, 5)
            self.ui.gos_num_line.setText(db_logic.get_value_from_stol(gos_n, 0))
            self.ui.city_of_drivig_away_line.setText(db_logic.get_value_from_stol(gos_n, 1))
            self.ui.place_of_drivig_away_line.setText(db_logic.get_value_from_stol(gos_n, 2))
            self.ui.date_of_drivig_away_line.setText(db_logic.get_value_from_stol(gos_n, 3))

            id_s = self.ui.serch_line.text()
            id_s = attack_protection(id_s)
            id_s = int(id_s)
            self.ui.id_statement_line_de.setText(db_logic.get_value_from_details(id_s, 0))
            self.ui.comments_line.setText(db_logic.get_value_from_details(id_s, 1))
            self.ui.sings_of_car_line.setText(db_logic.get_value_from_details(id_s, 2))
            self.ui.sings_of_intruder_line.setText(db_logic.get_value_from_details(id_s, 3))
        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.login_status.setText(str(ex))

            self.ui.id_statement_line_vi.setText('')
            self.ui.car_gos_num_line.setText('')
            self.ui.vin_line_vi.setText('')
            self.ui.phone_number_line.setText('')
            self.ui.email_line.setText('')
            self.ui.passport_line_vi.setText('')
            self.ui.residential_address_line.setText('')

            self.ui.pasp_number_line.setText('')
            self.ui.date_of_issue_line.setText('')
            self.ui.who_issued_line.setText('')
            self.ui.division_code_line.setText('')
            self.ui.surname_line.setText('')
            self.ui.first_name_line.setText('')
            self.ui.dads_name_line.setText('')
            self.ui.place_of_residence_line.setText('')
            self.ui.born_year_line.setText('')
            self.ui.place_of_born_line.setText('')

            self.ui.vin_number_line.setText('')
            self.ui.marka_line.setText('')
            self.ui.model_line.setText('')
            self.ui.car_type_line.setText('')
            self.ui.category_line.setText('')
            self.ui.year_of_isse_line.setText('')
            self.ui.engine_number_line.setText('')
            self.ui.shassi_number_line.setText('')
            self.ui.color_line.setText('')
            self.ui.power_horse_line.setText('')
            self.ui.poewer_kwt_line.setText('')
            self.ui.engine_size_line.setText('')
            self.ui.zavod_line.setText('')
            self.ui.approval_number_line.setText('')
            self.ui.country_of_import_line.setText('')
            self.ui.gtd_line.setText('')
            self.ui.restrictions_line.setText('')
            self.ui.first_owner_line.setText('')
            self.ui.adsress_of_first_owner_line.setText('')
            self.ui.issued_by_line.setText('')
            self.ui.adress_of_issued_by_line.setText('')
            self.ui.date_of_isse_line.setText('')
            self.ui.engine_name_line.setText('')

            self.ui.gos_num_line.setText('')
            self.ui.city_of_drivig_away_line.setText('')
            self.ui.place_of_drivig_away_line.setText('')
            self.ui.date_of_drivig_away_line.setText('')

            self.ui.id_statement_line_de.setText('')
            self.ui.comments_line.setText('')
            self.ui.sings_of_car_line.setText('')
            self.ui.sings_of_intruder_line.setText('')

        finally:
            db_logic.end_of_work()


class adm_add_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(adm_add_window, self).__init__()
        self.ui = Ui_AddWindow()
        self.ui.setupUi(self)
        self.ui.exit_button.clicked.connect(back_to_menu_add_adm)
        self.ui.add_button.clicked.connect(self.add_statement)

    def add_statement(self):
        try:
            db_logic.conn()
            id_statement = self.ui.id_statement_line_vi.text()
            car_gos_num = self.ui.car_gos_num_line.text()
            vin_vi = self.ui.vin_line_vi.text()
            phone_number = self.ui.phone_number_line.text()
            email = self.ui.email_line.text()
            passport = self.ui.passport_line_vi.text()
            residential_address = self.ui.residential_address_line.text()

            id_statement = attack_protection(id_statement)
            car_gos_num = attack_protection(car_gos_num)
            vin_vi = attack_protection(vin_vi)
            phone_number = attack_protection(phone_number)
            email = attack_protection(email)
            passport = attack_protection(passport)
            residential_address = attack_protection(residential_address)

            pasp_number = self.ui.pasp_number_line.text()
            date_of_issue = self.ui.date_of_issue_line.text()
            who_issued = self.ui.who_issued_line.text()
            division_code = self.ui.division_code_line.text()
            surname = self.ui.surname_line.text()
            first_name = self.ui.first_name_line.text()
            dads_name = self.ui.dads_name_line.text()
            place_of_residence = self.ui.place_of_residence_line.text()
            born_year = self.ui.born_year_line.text()
            place_of_born = self.ui.place_of_born_line.text()

            pasp_number = attack_protection(pasp_number)
            date_of_issue = attack_protection(date_of_issue)
            who_issued = attack_protection(who_issued)
            division_code = attack_protection(division_code)
            surname = attack_protection(surname)
            first_name = attack_protection(first_name)
            dads_name = attack_protection(dads_name)
            place_of_residence = attack_protection(place_of_residence)
            born_year = attack_protection(born_year)
            place_of_born = attack_protection(place_of_born)

            # шифрование имён
            first_name = login_logic.rus_encode(first_name)
            dads_name = login_logic.rus_encode(dads_name)
            surname = login_logic.rus_encode(surname)


            vin_number = self.ui.vin_number_line.text()
            marka = self.ui.marka_line.text()
            model = self.ui.model_line.text()
            car_type = self.ui.car_type_line.text()
            category = self.ui.category_line.text()
            year_of_isse = self.ui.year_of_isse_line.text()
            engine_number = self.ui.engine_number_line.text()
            shassi_number = self.ui.shassi_number_line.text()
            color = self.ui.color_line.text()
            power_horse = self.ui.power_horse_line.text()
            poewer_kwt = self.ui.poewer_kwt_line.text()
            engine_size = self.ui.engine_size_line.text()
            zavod = self.ui.zavod_line.text()
            approval_number = self.ui.approval_number_line.text()
            country_of_import = self.ui.country_of_import_line.text()
            gtd = self.ui.gtd_line.text()
            restrictions = self.ui.restrictions_line.text()
            first_owner = self.ui.first_owner_line.text()
            adsress_of_first_owner = self.ui.adsress_of_first_owner_line.text()
            issued_by = self.ui.issued_by_line.text()
            adress_of_issued_by = self.ui.adress_of_issued_by_line.text()
            date_of_isse = self.ui.date_of_isse_line.text()
            engine_name = self.ui.engine_name_line.text()

            vin_number = attack_protection(vin_number)
            marka = attack_protection(marka)
            model = attack_protection(model)
            car_type = attack_protection(car_type)
            category = attack_protection(category)
            year_of_isse = attack_protection(year_of_isse)
            engine_number = attack_protection(engine_number)
            shassi_number = attack_protection(shassi_number)
            color = attack_protection(color)
            power_horse = attack_protection(power_horse)
            poewer_kwt = attack_protection(poewer_kwt)
            engine_size = attack_protection(engine_size)
            zavod = attack_protection(zavod)
            approval_number = attack_protection(approval_number)
            country_of_import = attack_protection(country_of_import)
            gtd = attack_protection(gtd)
            restrictions = attack_protection(restrictions)
            first_owner = attack_protection(first_owner)
            adsress_of_first_owner = attack_protection(adsress_of_first_owner)
            issued_by = attack_protection(issued_by)
            adress_of_issued_by = attack_protection(adress_of_issued_by)
            date_of_isse = attack_protection(date_of_isse)
            engine_name = attack_protection(engine_name)

            gos_num = self.ui.gos_num_line.text()
            place_of_drivig_away = self.ui.city_of_drivig_away_line.text()
            city_of_drivig_away = self.ui.place_of_drivig_away_line.text()
            date_of_drivig_away = self.ui.date_of_drivig_away_line.text()

            gos_num = attack_protection(gos_num)
            place_of_drivig_away = attack_protection(place_of_drivig_away)
            city_of_drivig_away = attack_protection(city_of_drivig_away)
            date_of_drivig_away = attack_protection(date_of_drivig_away)

            id_statement_de = self.ui.id_statement_line_de.text()
            comments = self.ui.comments_line.text()
            sings_of_car = self.ui.sings_of_car_line.text()
            sings_of_intruder = self.ui.sings_of_intruder_line.text()

            id_statement_de = attack_protection(id_statement_de)
            comments = attack_protection(comments)
            sings_of_car = attack_protection(sings_of_car)
            sings_of_intruder = attack_protection(sings_of_intruder)

            db_logic.add_big_statement(pasp_number, date_of_issue, who_issued, division_code, surname, first_name, dads_name,
                      place_of_residence, born_year, place_of_born, vin_number, marka, model, car_type, category,
                      int(year_of_isse), engine_number, shassi_number, color, int(power_horse), int(poewer_kwt), int(engine_size), zavod,
                      approval_number, country_of_import,gtd, restrictions, first_owner, adsress_of_first_owner,
                      issued_by, adress_of_issued_by, date_of_isse, engine_name, gos_num, city_of_drivig_away,
                      place_of_drivig_away, date_of_drivig_away,phone_number, email, passport,
                      residential_address, id_statement, car_gos_num, vin_vi, id_statement_de, comments, sings_of_car,
                      sings_of_intruder)

            self.ui.login_status.setText('заявление добавлено')

        except Exception as ex:
            print('Ошибочка, сэр -> ' + str(ex))
            self.ui.login_status.setText(str(ex))

        finally:
            db_logic.end_of_work()
