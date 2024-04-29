from datetime import datetime
from django.utils import timezone
import pytz
from prempredict.models import PremSeasonInfo, PremGameweeks

def getGameweekDeadline():
    currentMatchday = PremSeasonInfo.objects.filter(active=True).get().currentMatchday
    deadline_datetime = datetime.strptime(str(PremGameweeks.objects.filter(number=currentMatchday).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))
    current_datetime = timezone.now().astimezone(pytz.timezone('Europe/London'))

    while current_datetime >= deadline_datetime:
        currentMatchday += 1
        deadline_datetime = datetime.strptime(str(PremGameweeks.objects.filter(number=currentMatchday).get().deadline), '%Y-%m-%d %H:%M:%S%z').astimezone(pytz.timezone('Europe/London'))

    total_seconds = (deadline_datetime - current_datetime).total_seconds()
    days = total_seconds // 86400
    total_seconds %= 86400
    hours = total_seconds // 3600
    total_seconds %= 3600
    
    # Temp to load previous predictions
    #currentMatchday-=1

    return {
            'matchday': currentMatchday,
            'deadline': deadline_datetime,
            'timetodeadline': f"{int(days)}:{int(hours)}:{int(total_seconds // 60)} dd:hh:mm",
            'current': current_datetime,
    }