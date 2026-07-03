import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()


def get_db_connection()
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    
    
def send_email(manager_email, employee_email, office_days):
    print(
        f"ALERT -> Manager: {manager_email}, "
        f"Employee: {employee_email}, "
        f"Office Days: {office_days}"
    )
   
def main():
    conn = None
    cur = None

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                manager_email,
                employee_email,
                COUNT(*) AS office_days
            FROM staff_management
            WHERE location = 'Office'
              AND record_date BETWEEN '2026-04-01' AND '2026-04-30'
            GROUP BY manager_email, employee_email
            HAVING COUNT(*) < 12;
        """)

        results = cur.fetchall()

        for manager_email, employee_email, office_days in results:
            send_email(
                manager_email,
                employee_email,
                office_days
            )

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
