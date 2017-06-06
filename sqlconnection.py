# Running on python 3.5.2


import MySQLdb

class sqlconnection:
  def __init__(self, host_input=None, port_input=None, user_input=None, passwd_input=None, db_input=None):
    self.host    = host_input
    self.port    = int(port_input)
    self.user    = user_input
    self.passwd  = passwd_input
    self.db_name = db_input
  def connect(self):
    try:
      self.db = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db_name)
      self.cursor = self.db.cursor()
    except:
      print("ERROR Invalid Connection Info")

  # Execute a command and expect a result
  def execute_script(self, command):
    return_items = None
    try:
      self.connect()
      self.cursor.execute(command)
      return_items = self.cursor.fetchall()
      self.db.close()
    except:
      print("ERROR invalid command")
    return return_items

  # Execute a command to insert data into database
  def insert_script(self, command):
    return_items = None
    try:
      self.connect()
      self.cursor.execute(command)
      self.db.commit()
      self.db.close()
    except:
      print("ERROR Inserting Command")
