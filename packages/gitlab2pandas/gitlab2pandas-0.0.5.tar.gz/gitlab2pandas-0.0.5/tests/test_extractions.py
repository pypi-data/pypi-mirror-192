import unittest
from . import utility
from gitlab2pandas.extractions import Extractions

class TestBasics(unittest.TestCase):

    def test_extract_branches(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_branches()
        pass

    def test_extract_releases(self):
        extractions = Extractions(utility.DATA_ROOT_DIR,
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_releases()
        pass

    def test_extract_pipelines(self):
        extractions = Extractions(utility.DATA_ROOT_DIR,
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_pipelines()
        pass
    
    def test_extract_jobs(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_jobs()
        pass

    def test_issues(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_issues()
        pass

    def test_merge_requests(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_merge_requests()
        pass

    def test_commits(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_commits()
        pass

    def test_project(self):
        extractions = Extractions(utility.DATA_ROOT_DIR, 
                                    project_namespace = utility.project_namespace(), 
                                    project_name = utility.project_name())
        utility.connect(extractions)
        extractions.extract_project()
        pass
    
if __name__ == "__main__":
    unittest.main()