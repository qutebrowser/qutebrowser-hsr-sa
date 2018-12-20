import datetime
import csv
import json


def parse_time(date, time):
    return datetime.datetime.strptime('{} {}'.format(date, time),
                                      '%Y-%m-%d %H:%M')


def get_semweek(start, end):
    _year, start_week, _wkday = start.isocalendar()
    _year, end_week, _wkday = end.isocalendar()
    assert start_week == end_week
    return start_week - 37


def analyze(f):
    r = csv.DictReader(f)

    weekly_hours = [0.0] * 14

    for entry in r:
        desc = entry['Description']
        if not desc:
            continue

        start_date = entry['Start date']
        start_time = entry['Start time']
        end_date = entry['End date']
        end_time = entry['End time']

        start_dt = parse_time(start_date, start_time)
        end_dt = parse_time(end_date, end_time)

        hours = (end_dt - start_dt).total_seconds() / 3600
        assert hours == float(entry['Duration (decimal)'])

        semweek = get_semweek(start_dt, end_dt)

        weekly_hours[semweek - 1] += hours

    return weekly_hours


def main():
    with open('time.csv', 'r', encoding='utf-8') as f:
        weekly_hours = analyze(f)

    with open('weekly.json', 'w') as f:
        json.dump(weekly_hours, f)


if __name__ == '__main__':
    main()
