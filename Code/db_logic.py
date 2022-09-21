import psycopg2

from Code import login_logic
from Code.db_config import db_name, host, user, password, db_name
from Message import status_print


# подключение к БД
def conn():
    global connection_to_db, host, user, password, database
    connection_to_db = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection_to_db.autocommit = True


# проверка подключения к бд
def test_db():
    global connection_to_db
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            'SELECT version();'
        )
        print('Версия для проверки конекта -> ', cursor.fetchone())
        status_print('Это база')


# создание таблиц
def create_tables():
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS public.victims_passport
            (
                pasp_number character varying(15) NOT NULL PRIMARY KEY,
                date_of_issue date NOT NULL,
                who_issued character varying(40) NOT NULL,
                division_code character varying(10) NOT NULL,
                surname character varying(40) NOT NULL,
                first_name character varying(40) NOT NULL,
                dads_name character varying(40),
                place_of_residence character varying(90) NOT NULL,
                born_year date NOT NULL,
                place_of_born character varying(40) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS public.pts
            (
                vin_number character varying(17) NOT NULL PRIMARY KEY,
                marka character varying(17) NOT NULL,
                model character varying(17) NOT NULL,
                car_type character varying(10) NOT NULL,
                category character varying(1) NOT NULL,
                year_of_isse integer NOT NULL,
                engine_number character varying(17) NOT NULL,
                shassi_number character varying(17) NOT NULL,
                color character varying(20) NOT NULL,
                power_horse integer NOT NULL,
                poewer_kwt integer NOT NULL,
                engine_size integer NOT NULL,
                zavod character varying(40) NOT NULL,
                approval_number character varying(30) NOT NULL,
                country_of_import character varying(15) NOT NULL,
                gtd character varying(30) NOT NULL,
                restrictions character varying(30) NOT NULL,
                first_owner character varying(40) NOT NULL,
                adsress_of_first_owner character varying(70) NOT NULL,
                issued_by character varying(30) NOT NULL,
                adress_of_issued_by character varying(70) NOT NULL,
                date_of_isse date NOT NULL,
                engine_name character varying(10) NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS public.stol
            (
                gos_num character varying(12) NOT NULL PRIMARY KEY,
                city_of_drivig_away character varying(40) NOT NULL,
                placr_of_drivig_away character varying(40) NOT NULL,
                date_of_drivig_away date NOT NULL
            );
            
            
            CREATE TABLE IF NOT EXISTS public.victim
            (
                phone_number character varying(14) NOT NULL,
                email character varying(60) NOT NULL,
                passport character varying(15) NOT NULL  REFERENCES victims_passport(pasp_number),
                residential_address character varying(90) NOT NULL,
                id_statement character varying(11) NOT NULL PRIMARY KEY,
                car_gos_num character varying(12) NOT NULL REFERENCES stol(gos_num),
                vin character varying(17) NOT NULL REFERENCES pts(vin_number)
            );
            
            CREATE TABLE IF NOT EXISTS public.details
            (
                id_statement character varying(11) NOT NULL REFERENCES victim(id_statement),
                comments character varying(120),
                sings_of_car character varying(120),
                sings_of_intruder character varying(120)
            );
            
            
            CREATE TABLE IF NOT EXISTS public.users
            (
                login character varying(20),
                password character varying(20),
                status integer
            )
        
                '''
        )
        status_print('База создана')


def fill_users_table(login_val, password_val, status_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO users (login, password, status) VALUES
        ('%s', '%s', '%i');''' % (login_val, password_val, status_val)
        )


# получить значение из тпблицы пользователей
def find_users():
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT login FROM users where status = 0;"""
        )
        return(str(cursor.fetchone()))


def get_pas_value(lo,i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT password, status FROM users WHERE login  = '%s';"""%(lo)
        )
        return(str(cursor.fetchone()[i]))


def get_status_value(lo):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT status FROM users WHERE login = '%s';"""%(lo)
        )
        return(str(cursor.fetchone())[1:-2])


# заполнение таблицы паспорта потерпевшего
def fill_victims_passport_table(pasp_number_val, date_of_issue_val, who_issued_val, division_code_val, surname_val,
                                first_name_val, dads_name_val, place_of_residence_val, born_year_val, place_of_born_val):
    surname_val = login_logic.rus_encode(surname_val)
    first_name_val = login_logic.rus_encode(first_name_val)
    dads_name_val = login_logic.rus_encode(dads_name_val)

    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO victims_passport (pasp_number, date_of_issue, who_issued, division_code, surname, 
            first_name, dads_name, place_of_residence, born_year, place_of_born) VALUES
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (pasp_number_val, date_of_issue_val,
                                                                        who_issued_val, division_code_val, surname_val,
                                                                        first_name_val, dads_name_val,
                                                                        place_of_residence_val, born_year_val,
                                                                                    place_of_born_val)
        )


def fill_victim_table(phone_number_val, email_val, passport_val, residential_address_val, id_statement_val,
                     car_gos_num_val, vin_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO victim (phone_number, email, passport, residential_address, id_statement, 
                                    car_gos_num, vin) VALUES
                ('%s', '%s', '%s','%s','%s','%s','%s');''' % (
                    phone_number_val, email_val, passport_val, residential_address_val, id_statement_val,
                    car_gos_num_val, vin_val))


def fill_pts_table(vin_number_val, marka_val, model_val, car_type_val, category_val, year_of_isse_val,
                     engine_number_val, shassi_number_val, color_val, power_horse_val, poewer_kwt_val,
                     engine_size_val, zavod_val, approval_number_val, country_of_import_val, gtd_val,
                     restrictions_val, first_owner_val, adsress_of_first_owner_val, issued_by_val,
                     adress_of_issued_by_val, date_of_isse_val, engine_name_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO pts (vin_number, marka, model, car_type, category, year_of_isse,
                                 engine_number, shassi_number, color, power_horse, poewer_kwt,
                                 engine_size, zavod, approval_number, country_of_import, gtd,
                                 restrictions, first_owner, adsress_of_first_owner, issued_by,
                                 adress_of_issued_by, date_of_isse, engine_name) VALUES
            ('%s', '%s', '%s', '%s', '%s', '%i', '%s', '%s', '%s', '%i', '%i', '%i', '%s', '%s', '%s', '%s', 
            '%s', '%s', '%s', '%s', '%s', '%s', '%s');''' % (
                vin_number_val, marka_val, model_val, car_type_val, category_val, year_of_isse_val,
                engine_number_val, shassi_number_val, color_val, power_horse_val, poewer_kwt_val,
                engine_size_val, zavod_val, approval_number_val, country_of_import_val, gtd_val,
                restrictions_val, first_owner_val, adsress_of_first_owner_val, issued_by_val,
                adress_of_issued_by_val, date_of_isse_val, engine_name_val))


def fill_stol_table(gos_num_val, city_of_drivig_away_val, placr_of_drivig_away_val, date_of_drivig_away_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO stol (gos_num, city_of_drivig_away, placr_of_drivig_away, date_of_drivig_away) VALUES
                ('%s', '%s', '%s', '%s');''' % (gos_num_val, city_of_drivig_away_val, placr_of_drivig_away_val,
                                  date_of_drivig_away_val))


def fill_details_table(id_statement_val, comments_val, sings_of_car_val, sings_of_intruder_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO details (id_statement, comments, sings_of_car, sings_of_intruder) VALUES
                ('%s', '%s', '%s', '%s');''' % (id_statement_val, comments_val, sings_of_car_val,
                                                sings_of_intruder_val))


def fill_victim_table(phone_number_val, email_val, passport_val, residential_address_val, id_statement_val, car_gos_num_val, vin_val):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''INSERT INTO victim (phone_number, email, passport, residential_address, id_statement, car_gos_num, vin) VALUES
                ('%s', '%s', '%s', '%s','%s','%s','%s');''' % (phone_number_val, email_val, passport_val,
                                                residential_address_val, id_statement_val, car_gos_num_val, vin_val))


# вывод из таблиц для gui
def get_value_from_victims_passport(n_pas, i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM victims_passport WHERE pasp_number  = '%s';"""%(n_pas))
        return(str(cursor.fetchone()[i]))


def get_value_from_pts(n_vin, i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM pts WHERE vin_number  = '%s';"""%(n_vin))
        return(str(cursor.fetchone()[i]))


def get_value_from_stol(n_gos, i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM stol WHERE gos_num  = '%s';"""%(n_gos))
        return(str(cursor.fetchone()[i]))


def get_value_from_victim(n_id, i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM victim WHERE id_statement  = '%s';"""%(n_id))
        return(str(cursor.fetchone()[i]))


def get_value_from_details(n_id, i):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """SELECT * FROM details WHERE id_statement  = '%i';"""%(n_id))
        return(str(cursor.fetchone()[i]))


# функции админа
def del_statement(pasp, vin_n, gos_n, id_st):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """ BEGIN;
                DELETE FROM details WHERE id_statement  = '%i';
                DELETE FROM victim WHERE id_statement  = '%i';
                DELETE FROM victims_passport WHERE pasp_number  = '%s';
                DELETE FROM pts WHERE vin_number  = '%s';
                DELETE FROM stol WHERE gos_num  = '%s';
                
                COMMIT;"""%(int(id_st), int(id_st), pasp, vin_n, gos_n))
        status_print('заявление удалено')


# добавление заявления через gui
def add_big_statement(pasp_number, date_of_issue, who_issued, division_code, surname, first_name, dads_name,
                      place_of_residence, born_year, place_of_born, vin_number, marka, model, car_type, category,
                      year_of_isse, engine_number, shassi_number, color, power_horse, poewer_kwt, engine_size, zavod,
                      approval_number, country_of_import,gtd, restrictions, first_owner, adsress_of_first_owner,
                      issued_by, adress_of_issued_by, date_of_isse, engine_name, gos_num, city_of_drivig_away,
                      place_of_drivig_away, date_of_drivig_away,phone_number, email, passport,
                      residential_address, id_statement,car_gos_num,vin_vi,id_statement_de, comments, sings_of_car,
                      sings_of_intruder):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''BEGIN;
                INSERT INTO victims_passport (pasp_number, date_of_issue, who_issued, division_code, surname, 
                first_name, dads_name, place_of_residence, born_year, place_of_born) VALUES
                ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                
                INSERT INTO pts (vin_number, marka, model, car_type, category, year_of_isse,
                                 engine_number, shassi_number, color, power_horse, poewer_kwt,
                                 engine_size, zavod, approval_number, country_of_import, gtd,
                                 restrictions, first_owner, adsress_of_first_owner, issued_by,
                                 adress_of_issued_by, date_of_isse, engine_name) VALUES
                ('%s', '%s', '%s', '%s', '%s', '%i', '%s', '%s', '%s', '%i', '%i', '%i', '%s', '%s', '%s', '%s', 
                '%s', '%s', '%s', '%s', '%s', '%s', '%s');
                
                INSERT INTO stol (gos_num, city_of_drivig_away, placr_of_drivig_away, date_of_drivig_away) 
                VALUES('%s', '%s', '%s', '%s');
                
                INSERT INTO victim (phone_number, email, passport, residential_address, id_statement, car_gos_num, vin) 
                VALUES('%s', '%s', '%s','%s','%s','%s','%s');
                
                INSERT INTO details (id_statement, comments, sings_of_car, sings_of_intruder) VALUES
                ('%s', '%s', '%s', '%s');
        
                COMMIT;'''
                    % (pasp_number, date_of_issue, who_issued, division_code, surname, first_name, dads_name,
                      place_of_residence, born_year, place_of_born, vin_number, marka, model, car_type, category,
                      year_of_isse, engine_number, shassi_number, color, power_horse, poewer_kwt, engine_size, zavod,
                      approval_number, country_of_import,gtd, restrictions, first_owner, adsress_of_first_owner,
                      issued_by, adress_of_issued_by, date_of_isse, engine_name, gos_num, city_of_drivig_away,
                      place_of_drivig_away, date_of_drivig_away,phone_number, email, passport,
                      residential_address, id_statement,car_gos_num,vin_vi,id_statement_de, comments, sings_of_car,
                      sings_of_intruder))


def del_user(u_name):
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            """DELETE FROM users WHERE login  = '%s';"""%(u_name))


def end_of_work():
    if connection_to_db:
        connection_to_db.close()
        status_print('Хорошо поработали, отрубаю базу')


# дропнуть таблицы
def del_tables():
    with connection_to_db.cursor() as cursor:
        cursor.execute(
            '''DROP TABLE victim, victims_passport, PTS, stol, details;''')
        status_print('Хана базе')
