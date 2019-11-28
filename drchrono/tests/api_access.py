import json
import sqlite3


def get_extra_data ():
    conn = sqlite3.connect('/srv/raiddisk/dev/pydev/drc2/drchrono.sqlite3')
    cursor = conn.cursor()

    cursor.execute("select extra_data from social_auth_usersocialauth where provider='drchrono'")
    row = cursor.fetchone()
    if row:
        conn.close()
        return row[0]
    else:
        conn.close()
        return None



def get_access_tok ():
    x = get_extra_data()
    d = json.loads(x)
    return d['access_token']


def main ():
    try:
        print (get_access_tok())
    except Exception as e:
        print("Crashed",e)

if __name__ == '__main__':
    main()