import os


def get_project_id() -> str:
    if 'PROJECT_ID' in os.environ:
        project_id = os.environ['PROJECT_ID']
    else:
        project_id = "fb897d8f-59ae-41fe-9258-45fccd45fd67"
    return project_id
