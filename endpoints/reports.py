import calendar
from constants import MONTHS
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


def build_monthly_report(available_maintenances: list[Maintenance], start_year: int, end_year: int):

    date_counts = build_year_month_obj(available_maintenances, start_year, end_year)
    returned_obj = []
    for year in range(start_year, end_year + 1, 1):
        for month in range(1, 13, 1):
            returned_obj.append(
                {
                    "yearMonth": {
                        "year": year,
                        "month": MONTHS[month],
                        "leapYear": calendar.isleap(year),
                        "monthValue": month,
                    },
                    "requests": date_counts[year][month],
                }
            )

    return returned_obj


def build_year_month_obj(available_maintenances: list[Maintenance], start_year: int, end_year: int):
    """Builds a 2 level dict with `year`:`month` -> `count` structure"""
    date_count = {}
    for year in range(start_year, end_year + 1, 1):
        date_count[year] = {}
        for month in range(1, 13, 1):
            date_count[year][month] = 0

    for maintenance in available_maintenances:
        year = maintenance.scheduledDate.year
        month = maintenance.scheduledDate.month

        date_count[year][month] += 1

    return date_count
