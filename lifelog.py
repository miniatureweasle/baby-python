"""
Log your life? No, just the little important things we tend to forget...
"""
import sqlite3
import sys
import time


def save(entry):
    """Persist a log entry"""
    conn = db_conn()
    sql = "insert into log (datetime, entry) values(strftime('%s','now'), '{}')"
    conn.execute(sql.format(entry))
    conn.commit()


def db_conn():
    """Connect to a database and setup table if required"""
    conn = sqlite3.connect('lldb')
    conn.cursor().execute((
        'create table if not exists log'
        '(id integer primary key autoincrement, '
        'datetime integer, '
        'entry text)'
    ))
    return conn


def lifelog(conn):
    """Extract our lifelog from the db into memory"""
    lifelog = {}
    cur = conn.execute('select * from log')
    for _, datetime, entry in cur.fetchall():
        lifelog[time.gmtime(datetime)] = entry
    return lifelog


if __name__ == '__main__':
    if len(sys.argv) == 1:
        save(input())
    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        lifelog = lifelog(db_conn())
        for datetime in sorted(lifelog.keys(), reverse=True):
            print(datetime.tm_year, datetime.tm_mon, datetime.tm_mday, end=': ')
            print(lifelog[datetime][:55], '...', sep='')