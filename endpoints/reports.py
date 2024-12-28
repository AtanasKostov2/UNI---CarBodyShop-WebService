from models import Maintenance


def build_daily_report(available_maintenances: list[Maintenance], capacity: int) -> list[dict]:
    """Build the daily report for the Garage availability"""

    date_count = {}
    for maintenance in available_maintenances:
        if maintenance.scheduledDate not in date_count:
            date_count[maintenance.scheduledDate] = 1
        else:
            date_count[maintenance.scheduledDate] += 1

    response = []
    for maintenance_date in date_count:
        date_report = {}
        date_report["date"] = str(maintenance_date)
        date_report["requests"] = date_count[maintenance_date]
        date_report["availableCapacity"] = capacity - date_report["requests"]

        response.append(date_report)

    return response
