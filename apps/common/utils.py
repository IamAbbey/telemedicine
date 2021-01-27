from apps.authentication.models import DAYS_OF_WEEK

def get_day_of_week(weekday):
    return DAYS_OF_WEEK[weekday][0]
    