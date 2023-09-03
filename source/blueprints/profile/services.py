from typing import Union
from uuid import uuid4

from source.dtos.profile import CreateProfileDTO
from source.dtos.report import CreateReportDTO
from source.models.profile.profile import Profile
from source.models.report.report import Report


def get_profile_by_nickname(nickname: str) -> Union[Profile, None]:
    """Get profile from database filtered by nickname.

    Parameters
    ----------
    nickname: str

    Returns
    -------
    (Profile | None)
    """
    return Profile.query.filter_by(nickname=nickname).one_or_none()


def create_new_profile(session, profile_data: CreateProfileDTO) -> Union[Profile, None]:
    """Create new profile.

    Parameters
    ----------
    profile_data: CreateProfileDTO

    Returns
    -------
    (Profile | None)

    Raises
    ------
    Value error: Profile with this nickname already exists
    """

    if get_profile_by_nickname(profile_data["nickname"]):
        raise ValueError("Profile with this nickname already exists")

    profile = Profile(**profile_data, id=uuid4())

    session.add(profile)
    session.flush()

    return profile


def creat_new_report(session, report_data: CreateReportDTO):
    """Create new report."""
    report = Report(**report_data, id=uuid4())

    session.add(report)
    session.flush()

    return report
