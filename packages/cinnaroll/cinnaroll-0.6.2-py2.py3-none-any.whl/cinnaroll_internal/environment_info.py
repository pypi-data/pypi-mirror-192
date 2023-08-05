import sys
from typing import Tuple, List, Optional, Set

from cinnaroll_internal import constants, jupyter_notebook
from cinnaroll_internal.working_environment import WorkingEnvironment


class UnknownEnvironmentError(Exception):
    ...


class UnhandledEnvironmentError(Exception):
    ...


class UnknownFrameworkError(Exception):
    ...


class FrameworkPackageNotFoundError(Exception):
    ...


class EnvironmentInfo:
    def __init__(self, framework: str, required_packages: Set[str]):
        self.framework = framework
        self.python_version = _get_python_version()
        self.requirements = _get_requirements(framework, required_packages)
        self.framework_version = _get_framework_version(framework, self.requirements)


KNOWN_SUPPORTED_ENVIRONMENTS = (
    WorkingEnvironment.GOOGLE_COLAB,
    WorkingEnvironment.NOTEBOOK,
    WorkingEnvironment.SCRIPT,
)


# todo: check if environment is supported on cinnaroll module import
def get_working_environment_and_notebook_if_appropriate() -> Tuple[
    WorkingEnvironment, Optional[jupyter_notebook.Notebook]
]:
    working_environment = _get_working_environment()
    if working_environment is WorkingEnvironment.SCRIPT:
        current_notebook = None
    elif working_environment in (WorkingEnvironment.GOOGLE_COLAB, WorkingEnvironment.NOTEBOOK):
        current_notebook = jupyter_notebook.Notebook(working_environment)
    elif working_environment is WorkingEnvironment.IPYTHON_TERMINAL:
        raise UnhandledEnvironmentError("IPython terminal is not supported.")
    else:
        raise UnknownEnvironmentError(
            f"Using unknown environment. "
            f"Currently supported environments are {KNOWN_SUPPORTED_ENVIRONMENTS})."
        )

    return working_environment, current_notebook


# https://stackoverflow.com/questions/15411967/how-can-i-check-if-code-is-executed-in-the-ipython-notebook
def _get_working_environment() -> WorkingEnvironment:
    try:
        ipython_class = get_ipython().__class__  # type: ignore[name-defined]
        module = ipython_class.__module__
        if module == "google.colab._shell":
            return WorkingEnvironment.GOOGLE_COLAB
        shell = ipython_class.__name__
        if shell == 'ZMQInteractiveShell':
            return WorkingEnvironment.NOTEBOOK   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return WorkingEnvironment.IPYTHON_TERMINAL  # Terminal running IPython
        else:
            return WorkingEnvironment.UNKNOWN  # Other type (?)
    except NameError:
        return WorkingEnvironment.SCRIPT      # Probably standard Python interpreter


def _get_python_version() -> Tuple[int, int, int, str, int]:
    return sys.version_info


def _get_requirements(framework: str, infer_func_package_dependencies: Set[str]) -> List[str]:
    try:
        from pip._internal.operations import freeze
    except ImportError:
        raise ImportError("Import error occurred while importing pip. Upgrade pip!")
    all_requirements = list(freeze.freeze())
    possible_ml_framework_package_names = _infer_possible_package_names(framework)
    required_packages = possible_ml_framework_package_names + list(infer_func_package_dependencies)
    trimmed_requirements: List[str] = []
    for requirement in all_requirements:
        if any(requirement.split("==")[0] == package_name for package_name in required_packages):
            trimmed_requirements.append(requirement)
    return trimmed_requirements


def _infer_possible_package_names(framework: str) -> List[str]:
    if framework == constants.PYTORCH:
        return [constants.PYTORCH_PACKAGE_NAME]
    elif framework in (constants.KERAS, constants.TENSORFLOW):
        return [
            constants.TENSORFLOW_PACKAGE_NAME,
            f"{constants.TENSORFLOW_PACKAGE_NAME}-macos",
            f"{constants.TENSORFLOW_PACKAGE_NAME}-cpu"
        ]
    raise UnknownFrameworkError


def _get_framework_version(framework: str, requirements: List[str]) -> str:
    possible_package_names = _infer_possible_package_names(framework)
    possible_framework_version_prefixes = list(
        map(lambda x: f"{x}==", possible_package_names)
    )

    for req in requirements:
        if any(req.startswith(prefix) for prefix in possible_framework_version_prefixes):
            return req.split("==")[1]
    raise FrameworkPackageNotFoundError(
        f"Couldn't find one of {possible_package_names} "
        f"in packages installed in currently used environment. "
        f"Run pip freeze in your terminal to inspect installed packages."
    )
