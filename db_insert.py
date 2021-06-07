from Db_Helper import DB_Helper

def db_record_insert(query):
    db= DB_Helper()
    db.execute_query(query)
