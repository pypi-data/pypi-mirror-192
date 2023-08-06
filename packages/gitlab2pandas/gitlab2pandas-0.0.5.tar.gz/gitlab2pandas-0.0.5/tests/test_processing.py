import unittest
from . import utility
from gitlab2pandas.processing import Processing

class TestBasics(unittest.TestCase):

    def test_replace_user_id(self):
        processing = Processing(utility.DATA_ROOT_DIR, project_namespace=utility.project_namespace(), project_name=utility.project_name())
        processing.replace_user_id()
        processing.convert_to_excel("Processed")
        pass
    
if __name__ == "__main__":
    unittest.main()