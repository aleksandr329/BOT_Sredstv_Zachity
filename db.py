import datetime
import sqlite3

a_time1 = datetime.datetime.now()
a_time2 = str(a_time1).split('.')[0]
a_time = a_time2.split(' ')[0]# для получения даты в формате 2024-01-07



conn = sqlite3.connect('data_base.db', check_same_thread=False)
cursor = conn.cursor()


def db_table_val(us: int, name: str, fam: str, nik: str):# функция для записи пользователя
	cursor.execute(f"SELECT user_id FROM user WHERE user_id = {us}")
	result = cursor.fetchone()
	if result is None:
		cursor.execute("INSERT INTO user (user_id, name_user, famyly_user, nikname_user, time_in) VALUES (?, ?, ?, ?, ?)", (us, name, fam, nik, a_time))
		conn.commit()


def db_table_zap(zag, text, foto, chislo, id, name, nik):# функция для записи задания
	cursor.execute("INSERT INTO table1 (zagolovok, text, foto, data_do_kakogo, data_sozdania, id_user, name_user, nik_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(zag, text, foto, chislo, a_time, id, name, nik))
	conn.commit()


def db_table_all():# функция для получения всех данных
	cursor.execute("SELECT * FROM table1")
	result = cursor.fetchall()
	return result


def db_table_get(zag):# функция для одного запроса
	cursor.execute(f"SELECT * FROM table1 WHERE zagolovok = '{zag}'")
	result = cursor.fetchone()
	return result


def db_table_delete(zag):# функция для удаления задания из таблицы
	cursor.execute(f"DELETE FROM table1 WHERE zagolovok = '{zag}'")
	conn.commit()

def db_table_zap2(zag, text, avtor, name_avtor, nik, foto, data_sozdania, chislo_do_kotorogo_vipolnit):# функция для записи данных в архив
	cursor.execute("INSERT INTO arhiv (zagolovok, text, avtor, name_avtor, nik_name, foto, data_sozdania, data_vipolnenia, chislo_do_kotorogo_vipolnit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(zag, text, avtor, name_avtor, nik, foto, data_sozdania, a_time, chislo_do_kotorogo_vipolnit))
	conn.commit()
