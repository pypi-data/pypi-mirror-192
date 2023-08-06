from pathlib import Path
import pickle
import pandas as pd
from typing import Union

from gitlab.v4.objects import Project
from gitlab import Gitlab

class Core():
    """
    Initializes core object with general information.
    Decide wheather to initialize with a project object or with the project namespace and name.
    Extractions can only be done with a project object or after connecting to a server with the project namespace and name.

    Parameters
    ----------
    data_root_dir : str
        A existing top level directory for data extraction.
    project : Project, default=None
        Project object from gitlab.
    project_namespace : str, default=None
        Namespace of the project.
    project_name : str, default=None
        Name of the project.

    """
    
    class Features():
        # Name <= 31 chars
        USERS = "Users"
        BRANCHES = "Branches"
        RELEASES = "Releases"
        PIPELINES = "Pipelines"
        PIPELINES_REPORT = "PipelinesReport"
        PIPELINES_BRIDGES = "PipelinesBridges"
        JOBS = "Jobs"
        ISSUES = "Issues"
        ISSUES_NOTES = "IssuesNotes"
        ISSUES_AWARD_EMOJIS = "IssuesAwardEmojis"
        ISSUES_NOTES_AWARD_EMOJIS = "IssuesNotesAwardEmojis"
        ISSUES_RESOURCESTATEEVENTS = "IssuesResourcestateevents"
        ISSUES_RESOURCELABELEVENTS = "IssuesResourcelabelevents"
        ISSUES_RESOURCEMILESTONESEVENTS = "IssuesResourcemilestonesevents"
        ISSUES_CLOSED_BY_MR = "IssuesClosedByMR"
        ISSUES_RELATED_MR = "IssuesRelatedMR"
        ISSUES_LINKS = "IssuesLinks"
        MERGE_REQUESTS = "MergeRequests"
        MERGE_REQUESTS_NOTES = "MRsNotes"
        MERGE_REQUESTS_COMMITS = "MRsCommits"
        MERGE_REQUESTS_AWARD_EMOJIS = "MRsAwardEmojis"
        MERGE_REQUESTS_NOTES_AWARD_EMOJIS = "MRsNotesAwardEmojis"
        MERGE_REQUESTS_RESOURCESTATEEVENTS = "MRsResourcestateevents"
        MERGE_REQUESTS_RESOURCELABELEVENTS = "MRsResourcelabelevents"
        MERGE_REQUESTS_CHANGES = "MRsChanges"
        MERGE_REQUESTS_DIFFS = "MRsDiffs"
        MERGE_REQUESTS_RESOURCEMILESTONESEVENTS = "MRsResourcemilestonesevents"
        COMMITS = "Commits"
        COMMITS_COMMENTS = "CommitsComments"
        COMMITS_REFS = "CommitsRefs"
        COMMITS_DIFFS = "CommitsDiffs"
        COMMITS_STATUSES = "CommitStatuses"
        PROJECTS = "Projects"
        EVENTS = "Events"
        ISSUE_BOARDS = "IssueBoards"
        ISSUE_BOARDS_LISTS = "IssueBoardsLists"
        LABELS = "Labels"
        TRIGGERS = "Triggers"
        PIPELINE_SCHEDULES = "PipelineSchedules"
        RUNNERS = "Runners"
        RUNNERS_JOBS = "RunnersJobs"
        SNIPPETS = "Snippets"
        WIKIS = "Wikis"
        MILESTONES = "Milestones"

        @classmethod
        def to_list(cls) -> list:
            """
            Returns a list of strings with all Features.
            
            Returns
            -------
            list
                A list of strings with all Features.

            """
            features = []
            for var, value in vars(cls).items():
                if isinstance(value,str):
                    if not var.startswith("__"):
                        features.append(value)
            return features

    class FileTypes():
        PANDAS = ".p"
        JSON = ".json"

    def __init__(self, data_root_dir:str, project:Project = None, project_namespace:str = None, project_name:str = None) -> None:
        """
        Initializes core object with general information.
        Decide wheather to initialize with a project object or with the project namespace and name.
        Extractions can only be done with a project object.
        ToDo: log_level=logging.INFO

        Parameters
        ----------
        data_root_dir : str
            A existing top level directory for data extraction.
        project : Project, default=None
            Project object from gitlab.
        project_namespace : str, default=None
           Namespace of the project.
        project_name : str, default=None
            Name of the project.
    
        """
        self.data_root_dir = data_root_dir
        self.project = project
        self.project_namespace = project_namespace
        self.project_name = project_name
        if project is None and (project_namespace is None or project_name is None):
            raise Exception("Need a project or its namespace and name")
        if project is None:
            self.project_data_dir = Path(self.data_root_dir,project_namespace,project_name)
            self.project_data_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.project_namespace = project.attributes["namespace"]["path"]
            self.project_name = project.attributes["path"]
            self.project_data_dir = Path(self.data_root_dir,project.attributes["path_with_namespace"])
            self.project_data_dir.mkdir(parents=True, exist_ok=True)
        self.input_file_type = self.FileTypes.PANDAS
        self.output_file_type = self.FileTypes.PANDAS

    def connect(self, server_url:str, private_token:str=None, oauth_token:str=None, job_token:str=None) -> None:
        """
        Get the project object from GitLab and using the project namespace and name. Only public projects can be accessed (read-only) without a token.
        Extraction can be done after a connection.

        Parameters
        ----------
        server_url: str
            Url to the GitLab server.
        private_token : str, default=None
            Private token or personal token for authentication.
        project_name : str, default=None
            Oauth token for authentication
        project_name : str, default=None
            Job token for authentication (to be used in CI).
            
        """
        gitlab_object = None
        if private_token:
            gitlab_object = Gitlab(server_url, private_token=private_token, per_page=100)
        elif oauth_token:
            gitlab_object = Gitlab(server_url, oauth_token=oauth_token, per_page=100)
        elif job_token:
            gitlab_object = Gitlab(server_url, job_token=job_token, per_page=100)
        else:
            # anonymous gitlab instance, read-only for public resources
            gitlab_object = Gitlab(server_url)
        self.project = gitlab_object.projects.get(f"{self.project_namespace}/{self.project_name}", per_page=100)

    def save_as_pandas(self, filename:str, data:pd.DataFrame) -> None:
        """    
        Saves a pandas DataFrame to the project directory.
        The project metadata will be saved in the top level directory with a filename as pandas file.

        Parameters
        ----------
        filename : str
            Name for the file.
        data : pd.DataFrame
            DataFrame to be saved.
    
        """
        if filename == Core.Features.PROJECTS:
            pd_file = Path(self.data_root_dir, filename + self.output_file_type)
        else:
            pd_file = Path(self.project_data_dir, filename + self.output_file_type)
        if self.output_file_type == self.FileTypes.PANDAS:
            with open(pd_file, "wb") as f:
                pickle.dump(data, f)
        elif self.output_file_type == self.FileTypes.JSON:
            data.to_json(pd_file, indent=2)
    
    def get_pandas_data_frame(self, filename:str) -> Union[pd.DataFrame,None]:
        """    
        Get a pandas DataFrame from the project directory.
        The project metadata will be excessed from the top level directory.

        Parameters
        ----------
        filename : str
            Name of the file to import.
    
    
        Returns
        -------
        DataFrame
            Return a DataFrame of the existing file.
        None
            Return None because the file does not exists.

        """
        if filename == Core.Features.PROJECTS:
            pd_file = Path(self.data_root_dir, filename + self.input_file_type)
        else:
            pd_file = Path(self.project_data_dir, filename + self.input_file_type)
        if pd_file.is_file():
            if self.input_file_type == self.FileTypes.PANDAS:
                return pd.read_pickle(pd_file)
            elif self.input_file_type == self.FileTypes.JSON:
                return pd.read_json(pd_file)
        else:
            return None
              
    def get_pandas_data_frame_path(self, filename:str) -> Union[Path,None]:
        """    
        Get a pandas DataFrame path from the project directory.
        The project metadata will be excessed from the top level directory.

        Parameters
        ----------
        filename : str
            Name of the feature to get the file path.
    
    
        Returns
        -------
        Path
            Return a str path of the feature.
        None
            Return None because the file does not exists.

        """
        if filename == Core.Features.PROJECTS:
            pd_file = Path(self.data_root_dir, filename + self.input_file_type)
        else:
            pd_file = Path(self.project_data_dir, filename + self.input_file_type)
        if pd_file.is_file():
            return pd_file
        else:
            return None

    def set_input_type(self, input_file_type:str) -> bool:
        """    
        Set the input type file and check if the file type is supported by gitlab2pandas.
        Input file type is needed for the update feature.

        Parameters
        ----------
        input_file_type : str
            File ending of the desired input type.
    
        Returns
        -------
        bool
            Return if the input file type was changed.
        """
        if input_file_type == ".p" or input_file_type == ".json":
            self.input_file_type = input_file_type
            return True
        else:
            return False
    
    def set_output_type(self, output_file_type:str) -> bool:
        """    
        Set the output type file and check if the file type is supported by gitlab2pandas.
        Output file type is needed for the automatically dataframe storage of the extrations.

        Parameters
        ----------
        output_file_type : str
            File ending of the desired input type.
    
        Returns
        -------
        bool
            Return if the input file type was changed.
        """
        if output_file_type == ".p" or output_file_type == ".json":
            self.output_file_type = output_file_type
            return True
        else:
            return False

    def convert_to_excel(self, excel_filename, features:list = None) -> None:
        """    
        Converts features to an excel file. If no features are passed, then all features will be converted.

        Parameters
        ----------
        excel_filename : str
            Name for the file.
        features : list, default=None
            Features to convert. If no features are passed, then all features will be converted.
            
        """
        writer = pd.ExcelWriter(Path(self.project_data_dir, f'{excel_filename}.xlsx'), engine='xlsxwriter')
        if features is None:
            features = Core.Features.to_list()
        for feature in features:
            df = self.get_pandas_data_frame(feature)
            if df is not None:
                col_times = [col for col in df.columns if any([isinstance(x, pd.Timestamp) for x in df[col]])]
                for col in col_times:
                    df[col] = pd.to_datetime(
                        df[col], infer_datetime_format=True) 
                    df[col] = df[col].dt.tz_localize(None) 
                df.to_excel(writer, sheet_name=feature)
        writer.close()