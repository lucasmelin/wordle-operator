from datetime import datetime, timedelta
from wordlist import words


def start_date():
    return datetime(2021, 5, 19, 0, 0, 0, 0)


def calculate_offset(e: datetime, a: datetime):
    millis_in_day = 24 * 60 * 60 * 1000
    s = e.replace(hour=0, minute=0, second=0, microsecond=0)
    t = a.replace(hour=0, minute=0, second=0, microsecond=0) - s
    t_millis = t.total_seconds() * 1000.0
    return round(t_millis / millis_in_day)


def days_since_start(e):
    return calculate_offset(start_date(), e)


def choose_word(e):
    s = days_since_start(e)
    a = s % len(words)
    return words[a]


def todays_word(date: datetime = None):
    if not date:
        date = datetime.now()
    d = date - timedelta(days=31)
    d.replace(hour=0, minute=0, second=0, microsecond=0)
    return choose_word(d)


if __name__ == "__main__":
    print(todays_word())
