import unittest
from . import utility
from gitlab2pandas.gitlab2pandas import GitLab2Pandas

class TestUtitlity(unittest.TestCase):

    def test_extract_all_to_json(self):
        gitlab2pandas = GitLab2Pandas(utility.DATA_ROOT_DIR, 
                                        project_namespace = utility.project_namespace(), 
                                        project_name = utility.project_name())
        utility.connect(gitlab2pandas)
        gitlab2pandas.set_input_type(gitlab2pandas.FileTypes.JSON)
        gitlab2pandas.set_output_type(gitlab2pandas.FileTypes.JSON)
        gitlab2pandas.extract_data(True,update=True)
        gitlab2pandas.convert_to_excel("Extraction_data_json")

if __name__ == "__main__":
    unittest.main()