import json

import bokeh.io
import bokeh.models
import bokeh.plotting
import bokeh.palettes
import bokeh.core.properties


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

    box = bokeh.models.BoxAnnotation(bottom=14, top=17,
                                     fill_alpha=0.5, fill_color='green')
    plot.add_layout(box)

    plot.xgrid.grid_line_color = None
    plot.xaxis.axis_label_text_font_size = '12pt'
    plot.xaxis.major_label_text_font_size = '12pt'
    plot.yaxis.axis_label_text_font_size = '12pt'
    plot.yaxis.major_label_text_font_size = '12pt'

    bokeh.io.save(plot)

    plot.output_backend = 'svg'
    bokeh.io.export_svgs(plot, filename='weekly.svg')


def render_topic(weekly_topic):
    bokeh.io.output_file('topic.html')
    weeks = [str(wk) for wk in range(1, 15)]
    topics = ['Documentation', 'Implementation', 'Contributions', 'Meetings',
              'Other']

    data = {'weeks': weeks}
    data.update(weekly_topic)

    source = bokeh.models.ColumnDataSource(data=data)

    plot = bokeh.plotting.figure(x_range=weeks, x_axis_label='Semester week',
                                 y_axis_label='Time (h)', plot_width=1200)

    colors = bokeh.palettes.Category10[len(topics)]

    for i, topic in enumerate(topics):
        x = bokeh.transform.dodge('weeks', -0.2 + i*0.1, range=plot.x_range)
        legend = bokeh.core.properties.value(topic)
        plot.vbar(x=x, top=topic, width=0.1, source=source, color=colors[i],
                  legend=legend)

    plot.legend.location = (300, 350)
    plot.xgrid.grid_line_color = None
    plot.xaxis.axis_label_text_font_size = '12pt'
    plot.xaxis.major_label_text_font_size = '12pt'
    plot.yaxis.axis_label_text_font_size = '12pt'
    plot.yaxis.major_label_text_font_size = '12pt'
    plot.legend.label_text_font_size = '12pt'

    phases = [
        (0, 'Inception'),
        (1, 'Preparation'),
        (6, 'Elaboration'),
        (9, 'Construction'),
        (13, 'Transition'),
    ]

    for week, _name in phases:
        if week == 0:
            continue
        line = bokeh.models.Span(location=week, dimension='height',
                                 line_color='grey', line_width=2)
        plot.add_layout(line)

    for week, text in phases:
        label = bokeh.models.Label(x=week + 0.1, y=25, text=text)
        plot.add_layout(label)

    bokeh.io.save(plot)

    plot.output_backend = 'svg'
    bokeh.io.export_svgs(plot, filename='topic.svg')


def main():
    with open('weekly.json', 'r') as f:
        weekly_hours = json.load(f)

    with open('weekly_topic.json', 'r') as f:
        weekly_topic = json.load(f)

    render_weekly(weekly_hours)
    render_topic(weekly_topic)


if __name__ == '__main__':
    main()
