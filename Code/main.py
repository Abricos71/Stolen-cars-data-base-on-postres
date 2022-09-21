import db_logic
from Code import login_logic
from Code.test_add import test_fill1, test_fill2, test_fill3, test_fill4
from GUI_CODE import gui_logic

if __name__ == '__main__':

    try:
        db_logic.conn()
        db_logic.test_db()
        db_logic.create_tables()

        #test_fill1()
        #test_fill2()
        #test_fill3()
        #test_fill4()

        gui_logic.out_login()

    except Exception as ex:
        print('Ошибочка, сэр -> ' + str(ex))
    finally:
        db_logic.end_of_work()
