# Running in python 3.5.2

import os
import subprocess
from datetime import datetime
from sqlconnection import sqlconnection

class KodiSQL:
  def __init__(self):
    self.home_location = os.path.expanduser("~")
    self.id_location   = os.path.join(".kodi", "addons", "script.kodi.controller", "tmp", "id.txt")
    self.mysql = sqlconnection("10.0.0.221", "4624", "kodi_controller", "tempP@$$", "KODI")
    # Set initial values
    self.rank = self.mysql.execute_script("SELECT COUNT(*) FROM SYNC")
    self.rank = self.rank[0][0]
    self.mysql.insert_script("INSERT INTO SYNC(RANK, TIME, POSITION)VALUES(%s, 0, 0)" % (str(self.rank)))
    self.unique_id = self.get_unique_id()

  def set_sync(self, input_time, input_position):
    # command = ("UPDATE SYNC SET TIME = %s, POSITION = %s WHERE RANK = %s" % (str(input_time), str(input_position), str(self.rank)))
    # print(command)
    self.mysql.insert_script("UPDATE SYNC SET TIME = %s, POSITION = %.6f WHERE RANK = %s" % (str(input_time), float(input_position), str(self.rank)))

  def get_sync(self, sync_time):
    result = self.mysql.execute_script("SELECT TIME, POSITION FROM SYNC WHERE RANK = 0")
    time = result[0][0]
    position = result[0][1]
    time_difference= float(sync_time) - float(time)
    # print("Time: %s\nPosition: %s\nDifrance: %s" % (str(time), str(position), str(time_difference)))
    return_value = 0
    if time_difference > 0:
      return_value = float(position) + float(time_difference)
    return return_value

  def get_difference(self):
    return_value = 0
    if self.rank is not 0:
      result1 = self.mysql.execute_script("SELECT TIME, POSITION FROM SYNC WHERE RANK = %s" % (self.rank))
      result2 = self.mysql.execute_script("SELECT TIME, POSITION FROM SYNC WHERE RANK = 0")
      return_value = float(result2[0][1]) - float(result1[0][1])
      return_value = return_value + (float(datetime.now().strftime("%S")) - float(result2[0][0]))
      subprocess.call("echo \"Result1: %s\nResult2: %s\nReturn Value: %s\" >> $HOME/.kodi/temp/my_log2.txt" % (result1, result2, return_value), shell=True)
    return return_value

  def get_rank(self):
    return self.rank

  def get_position(self):
    result = self.mysql.execute_script("SELECT POSITION FROM SYNC WHERE RANK = %s" % (self.rank))
    return result[0][0]

  def get_lead_position(self):
    result = self.mysql.execute_script("SELECT POSITION FROM SYNC WHERE RANK = 0")
    print(result)
    return result[0][0]

  def get_unique_id(self):
    subprocess.call("ifconfig | grep eth1 | awk '{print $NF}' | sed 's/://g' > %s" % (os.path.join(self.home_location, self.id_location)), shell=True)
    id_file = open(os.path.join(self.home_location, self.id_location), 'r')
    self.unique_id = id_file.read().replace(" ", "")
    self.unique_id = self.unique_id[:len(self.unique_id) - 1]
    id_file.close()
    return self.unique_id
    
  def set_device_id(self):
    if self.unique_id is None:
      self.get_unique_id()
    self.mysql.insert_script("INSERT INTO DEVICES (UNIQUE_ID)VALUE('%s')" % self.unique_id)

  def get_device_id(self):
    return_value = None
    result = self.mysql.execute_script("SELECT DEVICE_ID FROM DEVICES WHERE UNIQUE_ID LIKE('%s')" % (self.unique_id))

    if result is None or len(result) is int(0):
      self.set_device_id()
      return_value = self.get_device_id()
    else:
      return_value = result[0][0]
    return return_value



# Connections to handle songs

# Get current song ID

# Get Song Location

# Skip Song


