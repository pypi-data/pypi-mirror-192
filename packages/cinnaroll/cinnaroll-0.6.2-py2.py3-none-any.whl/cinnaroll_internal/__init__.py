import os

from cinnaroll_internal import constants

if "CINNAROLL_BACKEND_URL" in os.environ:
    constants.BACKEND_BASE_URL = os.environ["CINNAROLL_BACKEND_URL"]
