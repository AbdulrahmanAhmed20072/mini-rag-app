from helpers.config import get_settings
import os
import string
import random

class BaseController:
    
    def __init__(self):

        self.app_settings = get_settings()
        
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.files_dir = os.path.join(self.base_dir, "assets/files")

    def generate_random_string(self, length: int = 12):

        # generating random strings
        return ''.join(random.choices(string.ascii_letters, k = length))