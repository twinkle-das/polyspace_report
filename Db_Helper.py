import psycopg2

class DB_Helper(object):
    '''DB Helper class responsible to interact with postgress using psycopg2'''
    
    conn=cursor=_obj=None
    user = 'postgres'
    password = 'tdpostgres19'
    host = '127.0.0.1'
    port = '5432'
    database = 'postgres'
    jobtable = 'POLYSPACE'
    istbl_job_created = 1
 

    def __init__(self):
        self.conn=self._obj.conn
        self.cursor=self._obj.cursor
            
    @classmethod
    def __new__(cls, *args, **kwargs):
        if(cls._obj is None):
            cls._obj=object.__new__(cls)
            try:
                conn = cls._obj.conn = psycopg2.connect(
                    user = cls._obj.user, 
                    password = cls._obj.password,
                    host = cls._obj.host,
                    port = cls._obj.port,
                    database = cls._obj.database)
                cls.cursor=conn.cursor()
            except Exception as ex:
                cls._obj=None
                print(ex)
        return cls._obj

    def execute_query(self, query, args = None):
        '''Method to execute query in postgres'''
        try:
            result = self.cursor.execute(query, args)
            self.conn.commit()
#             print("Successfuly executed : " + query)
        except Exception as error:
            print(f"error execting query '{query}', error: {error}")
            return None
        else:
            return result

   
    def __del__(self):
        self.conn.close()
        self.cursor.close()
        print("Connection closed")
