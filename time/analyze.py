import datetime
import csv
import json
import collections
import enum
import pprint


def parse_time(date, time):
    return datetime.datetime.strptime('{} {}'.format(date, time),
                                      '%Y-%m-%d %H:%M')


def get_semweek(start, end):
    _year, start_week, _wkday = start.isocalendar()
    _year, end_week, _wkday = end.isocalendar()
    assert start_week == end_week
    return start_week - 37


class Topic(enum.Enum):

    meetings = 1
    other = 2
    # upstream = 3
    docs = 4
    contributions = 5
    # bugfixes = 6
    implementation = 7


def analyze(f):
    r = csv.DictReader(f)

    weekly_hours = [0.0] * 14
    per_topic = collections.defaultdict(float)
    per_desc = collections.defaultdict(float)
    weekly_topic = [collections.defaultdict(float) for _ in range(14)]

    topic_map = {
        'Sitzung': Topic.meetings,
        'Sitzung (Nachbereitung)': Topic.meetings,
        'Video call mit fiete': Topic.meetings,
        'Videocall fiete': Topic.meetings,
        'Sitzung (Vorbereitung)': Topic.meetings,
        'Sitzung Sprachberatung': Topic.meetings,
        'Sitzung (API review)': Topic.meetings,
        'Sprachreview': Topic.meetings,

        'Einführung': Topic.other,
        'Community': Topic.other,
        'Release': Topic.other,
        'Tracking': Topic.other,
        'Buch lesen': Topic.other,
        'Organisatorisches': Topic.other,

        'Upstream': Topic.other,
        'pytest upgrade': Topic.other,
        'Qt 5.12': Topic.other,

        'Dokumentation': Topic.docs,
        'Doku': Topic.docs,
        'Dokumentation (Projektplan)': Topic.docs,
        'Sphinx': Topic.docs,

        'Implementation': Topic.implementation,
        'API review implementation': Topic.implementation,
        'Implementation (dynamic loading)': Topic.implementation,
        'mypy': Topic.implementation,
        'Bugfixes': Topic.implementation,
        'Bugfixing': Topic.implementation,

        'PRs': Topic.contributions,
    }

    for entry in r:
        print(entry)
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
        topic = topic_map[desc].name

        weekly_hours[semweek - 1] += hours
        per_topic[topic] += hours
        per_desc[(topic, desc)] += hours
        weekly_topic[semweek - 1][topic] += hours

    return weekly_hours, per_topic, per_desc, weekly_topic


def main():
    with open('time.csv', 'r', encoding='utf-8') as f:
        weekly_hours, per_topic, per_desc, weekly_topic = analyze(f)

    print('\n===== weekly =====')
    pprint.pprint(weekly_hours)

    print('\n===== per topic =====')
    pprint.pprint(dict(per_topic))

    print('\n===== per desc =====')
    pprint.pprint(dict(per_desc))

    print('\n===== weekly per topic =====')
    pprint.pprint(weekly_topic)

    with open('weekly.json', 'w') as f:
        json.dump(weekly_hours, f)

    with open('per_topic.json', 'w') as f:
        json.dump(per_topic, f)

    with open('weekly_topic.json', 'w') as f:
        json.dump(weekly_topic, f)


if __name__ == '__main__':
    main()
