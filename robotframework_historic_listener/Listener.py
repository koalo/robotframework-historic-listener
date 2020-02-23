import datetime
import mysql.connector
from robot.libraries.BuiltIn import BuiltIn

class Listener:

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.PRE_RUNNER = 0
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.start_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_suite(self, name, attrs):        
        self.test_count = len(attrs['tests'])
        self.suite_name =  name

        # set-up database
        if self.PRE_RUNNER == 0:
            self.HOST = BuiltIn().get_variable_value("${SQL_HOST}",'localhost')
            self.USER_NAME = BuiltIn().get_variable_value("${SQL_USER_NAME}",'superuser')
            self.PASSWORD = BuiltIn().get_variable_value("${SQL_PASSWORD}",'passw0rd')
            self.DATABASE_NAME = BuiltIn().get_variable_value("${RFH_PROJECT_NAME}")
            self.EXECUTION_NAME = BuiltIn().get_variable_value("${RFH_EXECUTION_NAME}")
            self.PRE_RUNNER = 1

            # Connect to db
            self.con = connect_to_mysql_db(self.HOST, self.USER_NAME, self.PASSWORD, self.DATABASE_NAME)
            # insert values into execution table
            self.id = insert_into_results_mysql_table(self.con, str(self.date_now), self.EXECUTION_NAME)

    def start_test(self, name, attrs):
        if self.test_count != 0:
            self.t_start_time = datetime.datetime.now().time().strftime('%H:%M:%S')

    def end_test(self, name, attrs):
        if self.test_count != 0:
            self.total_tests += 1

            if attrs['status'] == 'PASS':
                self.passed_tests += 1
            else:
                self.failed_tests += 1

            self.t_end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.t_total_time=(datetime.datetime.strptime(self.t_end_time,'%H:%M:%S') - datetime.datetime.strptime(self.t_start_time,'%H:%M:%S'))
            self.test_exe_time = get_min(str(self.t_total_time))
            # insert values into test table
            insert_into_test_results_mysql_table(self.con, self.id, str(self.suite_name) + " - " + str(name), str(attrs['status']), str(self.test_exe_time), str(attrs['message']))

    def close(self):
        self.end_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.total_time=(datetime.datetime.strptime(self.end_time,'%H:%M:%S') - datetime.datetime.strptime(self.start_time,'%H:%M:%S'))
        self.exe_time = get_min(str(self.total_time))
        # insert values into results table
        update_results_mysql_table(self.con, self.id, str(self.total_tests), str(self.passed_tests), str(self.failed_tests), str(self.exe_time))

'''

# * # * # * # * Re-usable methods out of class * # * # * # * #

''' 

def get_current_date_time(format,trim):
    t = datetime.datetime.now()
    if t.microsecond % 1000 >= 500:  # check if there will be rounding up
        t = t + datetime.timedelta(milliseconds=1)  # manually round up
    if trim:
        return t.strftime(format)[:-3]
    else:
        return t.strftime(format)

def get_min(time_str):
    h, m, s = time_str.split(':')
    ctime = int(h) * 3600 + int(m) * 60 + int(s)
    crtime = "%.2f" % (ctime/60)
    return crtime

def connect_to_mysql_db(host, user, pwd, db):
    try: 
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            passwd=pwd,
            database=db
        )
        return mydb
    except Exception:
        print(Exception)

def insert_into_results_mysql_table(con, date, name):
    cursorObj = con.cursor()
    sql = "INSERT INTO results (ID, DATE, NAME, TOTAL, PASSED, FAILED, TIME) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (0, date, name, "0", "0", "0", "0")
    cursorObj.execute(sql, val)
    con.commit()
    cursorObj.execute("select count(*) from results")
    rows = cursorObj.fetchone()
    return str(rows[0])

def update_results_mysql_table(con, eid, total, passed, failed, duration):
    cursorObj = con.cursor()
    sql = "UPDATE results SET TOTAL=%s, PASSED=%s, FAILED=%s, TIME='%s' WHERE ID=%s;" % (str(total), str(passed), str(failed), str(duration), int(eid))
    cursorObj.execute(sql)
    con.commit()

def insert_into_test_results_mysql_table(con, eid, test, status, duration, msg):
    cursorObj = con.cursor()
    sql = "INSERT INTO test_results (ID, UID, TESTCASE, STATUS, TIME, MESSAGE) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (eid, 0, test, status, duration, msg)
    cursorObj.execute(sql, val)
    # Skip commit to avoid load on db (commit once execution is done as part of close)
    # con.commit()