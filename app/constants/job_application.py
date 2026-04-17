from typing import Literal, get_args

JobApplicationStatus = Literal[
    "applied",
    "interview_scheduled",
    "interviewing",
    "selected",
    "rejected",
    "offer_received",
    "withdrawn",
]
JOBAPPLICATION_STATUS_LIST = get_args(JobApplicationStatus)
