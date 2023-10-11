import plotext
import numpy as np

def chart_settings(width, height):
    plotext.xaxes(True, False)
    plotext.yaxes(True, False)
    plotext.plot_size(width, height)
    plotext.axes_color("black")
    plotext.canvas_color("black")
    plotext.ticks_color("white")

def build_chart(values, values_index, aofive, trend_builder):
    plotext.clear_data()
    if aofive:
        plotext.hline(aofive)
    plotext.plot(
        values_index,
        trend_builder(values_index),
        marker="braille")
    plotext.plot(
        values_index,
        values,
        marker="fhd")
    return plotext.build()


def get_chart(values, height, width):
    if len(values) < 2: return "Not enough solves yet"
    values_index = [index for index, _ in enumerate(values)]
    aofive = None if len(values) < 5 else int(1000 * sum(values[-5:]) / 5) / 1000
    trend_builder = np.poly1d(np.polyfit(np.array(values_index), np.array(values), 1))

    chart_settings(width, height)

    return build_chart(values, values_index, aofive, trend_builder)
