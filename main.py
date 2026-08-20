import json
import os
import hashlib
import secrets
from datetime import datetime
from getpass import getpass

class PersonalDiarey:
   def __intit__(self): 
      self.data_file = "personal_diary_data.json"
      self.backup_folder = "diary_backups"
      self.data = {
         "users": {},
         "entries": []
      }
      self.current_user = None
      self.load_data()



      
