import sqlite3
import os


class SQLite3:

    """
    Parameters:
        dbfilename: str (Creates the database with the name passed if it does not exist)
        path_start: str (Scans any directory or root by defaults)
    """

    def __init__(self, dbfilename: str, path_start='/'):
        global scandb
        scandb = sqlite3.connect(dbfilename)
        self.scan_directory(path_start)

    def progress(self):
        # TODO: Write a method to display scan progress to the console
        pass

    def scan_directory(self, path):
        try:
            scanner =  os.scandir(path=path)
            for file in scanner:
                if file.is_dir():
                        self.scan_directory(os.path.realpath(file))
                elif file.is_file():
                    self.check(file)
        except FileNotFoundError as e:
            pass
        except PermissionError as e:
            pass

    def check(self, file):
        try:
            fd = open(file, 'rb')
            header = fd.read(100)
            if 'SQLite' in str(header) and os.path.realpath(file) is not os.path.realpath(os.curdir):
                self.connect(file)
        except PermissionError as e:
            pass
        except OSError as e:
            pass

    def connect(self, file):
        tables_list = []
        try:
            db = sqlite3.connect(file)
            cur = db.cursor()
            tables = cur.execute('SELECT tbl_name FROM sqlite_master')
            for table in tables:
                for name in table:
                    tables_list.append(name)
        except sqlite3.OperationalError as oe:
            pass
            # print("\t\t " + str(oe))
        except sqlite3.DatabaseError as de:
            pass
            # print("\t\t " + str(de))
        finally:
            self.save(file, os.path.realpath(file), tables_list)

    @staticmethod
    def save(file, location, tables, test="pass"):
        scandb.execute('CREATE TABLE IF NOT EXISTS results(file, location, tables, test)')
        sql = 'INSERT INTO results VALUES ("{}", "{}", "{}" ,"{}")'.format(file, location, tables, test)
        scandb.execute(sql)
        scandb.commit()

    @staticmethod
    def destroy():
        try:
            for db in scandb.execute('SELECT location FROM results'):
                destroy = sqlite3.connect(db[0])
                cursor = destroy.cursor()
                for tables in cursor.execute("SELECT name FROM sqlite_master WHERE type IS 'table'"):
                    if "sqlite_sequence" in tables[0]:
                        continue
                    else:
                        cursor.execute("DROP TABLE IF EXISTS " + tables[0])
        except Exception as e:
            print(e)


class MySQL:
    # TODO: Build a class for MySQL
    def __init__(self):
        pass

SQLite3("gcloud")
