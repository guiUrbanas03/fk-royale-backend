from uuid import uuid4

from source.dtos.report import CreateReportDTO
from source.models.report.report import Report


def creat_new_report(session, report_data: CreateReportDTO):
    """Create new report."""
    report = Report(**report_data, id=uuid4())

    session.add(report)
    session.flush()

    return report
