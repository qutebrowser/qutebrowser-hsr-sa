import json

import bokeh.io
import bokeh.models
import bokeh.plotting
import bokeh.palettes
import bokeh.core.properties


def render_weekly(hours):
    bokeh.io.output_file('weekly.html')
    weeks = ['SW {}'.format(wk) for wk in range(1, 15)]

    source = bokeh.models.ColumnDataSource(data={
        'weeks': weeks,
        'hours': hours,
    })

    plot = bokeh.plotting.figure(x_range=weeks, x_axis_label='Semester week',
                                 y_axis_label='Time (h)')
    plot.vbar(x='weeks', top='hours', source=source, width=0.9)

    line1 = bokeh.models.Span(location=17, dimension='width',
                              line_color='orange', line_width=2)
    line2 = bokeh.models.Span(location=14, dimension='width',
                              line_color='orange', line_width=2)
    plot.add_layout(line1)
    plot.add_layout(line2)

    bokeh.io.save(plot)


def render_topic(weekly_topic):
    bokeh.io.output_file('topic.html')
    weeks = ['SW {}'.format(wk) for wk in range(1, 15)]
    topics = ['meetings', 'other', 'docs', 'contributions', 'implementation']

    data = {'weeks': weeks}
    data.update(weekly_topic)

    source = bokeh.models.ColumnDataSource(data=data)

    plot = bokeh.plotting.figure(x_range=weeks, x_axis_label='Semester week',
                                 y_axis_label='Time (h)')

    colors = bokeh.palettes.Category10[len(topics)]

    for i, topic in enumerate(topics):
        x = bokeh.transform.dodge('weeks', -0.2 + i*0.1, range=plot.x_range)
        legend = bokeh.core.properties.value(topic)
        plot.vbar(x=x, top=topic, width=0.1, source=source, color=colors[i],
                  legend=legend)

    plot.legend.location = "top_center"

    bokeh.io.save(plot)


def main():
    with open('weekly.json', 'r') as f:
        weekly_hours = json.load(f)

    with open('weekly_topic.json', 'r') as f:
        weekly_topic = json.load(f)

    render_weekly(weekly_hours)
    render_topic(weekly_topic)


if __name__ == '__main__':
    main()
