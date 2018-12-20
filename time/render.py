import json

import bokeh.io
import bokeh.models
import bokeh.plotting


def render_weekly(hours):
    bokeh.io.output_file('weekly.html')
    weeks = [str(wk) for wk in range(1, 15)]

    source = bokeh.models.ColumnDataSource(data={
        'weeks': weeks,
        'hours': hours,
    })

    plot = bokeh.plotting.figure(x_range=weeks, x_axis_label='Semester week',
                                 y_axis_label='Time (h)')
    plot.vbar(x='weeks', top='hours', source=source, width=0.9)

    bokeh.io.save(plot)


def main():
    with open('weekly.json', 'r') as f:
        weekly_hours = json.load(f)

    with open('per_topic.json', 'r') as f:
        per_topic = json.load(f)

    render_weekly(weekly_hours)


if __name__ == '__main__':
    main()
