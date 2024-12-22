import time
import db
from sqlalchemy import text
import datetime


def update(mysql, postgres, email: str):
    cabinet_id = postgres.execute(
        text(f"select cabinet_id from main where employee_id = (select id from employees where email = '{email}')")).fetchone()[0]
    cabinet = postgres.execute(text(f"select number from cabinet where id = {cabinet_id}")).fetchone()[0]
    with mysql.begin():
        mysql.execute(text(f"""
            UPDATE glpi_locations
            SET name = {cabinet}
            WHERE id = (
                SELECT gu.locations_id
                FROM glpi_users gu
                LEFT JOIN glpi_useremails gm ON gm.users_id = gu.id
                WHERE gm.email = '{email}'
            )
        """))


def main():
    mysql_engine = db.mysql_connect()
    postgres_engine = db.postgresql_connect()
    session = datetime.datetime.strptime(datetime.datetime.today().strftime('%H:%M'), '%H:%M')
    print('Session start: ', datetime.datetime.today())

    while True:
        time_delta = datetime.datetime.strptime(datetime.datetime.today().strftime('%H:%M'), '%H:%M') - session
        time_delta = time_delta.total_seconds()
        if time_delta >= 3600:
            main()
            break
        try:
            print("\nВведите данные для обновления или 'exit' для выхода.")
            email = input("Введите email пользователя: ")
            if email.lower() == "exit":
                print("Завершение программы.")
                break

            if not email.strip():
                print("Поле должно быть заполнено")
                continue

            update(mysql_engine.connect(), postgres_engine.connect(), email)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Данные обновлены успешно: email={email}")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Ошибка при обновлении: {e}")


if __name__ == "__main__":
    main()
