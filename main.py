import sqlite3
import credentials
from model import absatzmarkt, aktie, analyse, besitzer, bilanz, geschaeftsfeld, guv, sparte

cur = None


def query_db(query):
    cur.execute(query)
    return cur.fetchall()


def deserialize_analysis(data):
    analysis = analyse.Analyse
    analysis.aktie = aktie.Aktie(data)
    analysis.guv = []
    rows = query_db(credentials.get_guv(analysis.aktie.name))
    for row in rows:
        analysis.guv.append(guv.GuV(row))

    rows = query_db(credentials.get_bilanz(analysis.aktie.name))[0]
    bilanz_id = rows[0]
    analysis.bilanz = bilanz.Bilanz(rows)

    rows = query_db(credentials.get_aktiva(bilanz_id))
    for row in rows:
        analysis.bilanz.add_aktiva(row[2], row[3])

    rows = query_db(credentials.get_passiva(bilanz_id))
    for row in rows:
        analysis.bilanz.add_passiva(row[2], row[3])

    i = 0
    return analysis


def extract_db_data():
    try:
        db_conn = sqlite3.connect(credentials.get_db_path())
        global cur
        cur = db_conn.cursor()
        rows = query_db(credentials.get_aktie())

        for row in rows:
            # for each stock
            a = deserialize_analysis(row)



            i = 0
    except sqlite3.DatabaseError or sqlite3.IntegrityError as e:
        print(e)
    return None


if __name__ == '__main__':
    extract_db_data()



