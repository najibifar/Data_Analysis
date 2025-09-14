import numpy as np
import pandas as pd
from bokeh.palettes import Category20_16
from bokeh.models import CheckboxGroup, Slider, RangeSlider, ColumnDataSource, Panel
from bokeh.plotting import figure
from bokeh.layouts import column, row



def hist_tab(data):

    def md(s_data, rs=60, re=120, bin=10):
        d = pd.DataFrame(columns=['proportion', 'left', 'right', 'f_proportion', 'f_interval', 'name', 'color'])
        r = re - rs
        for i, r_data in enumerate(s_data):
            subset = data[data['name'] == r_data]
            arr_hist, edge = np.histogram(subset['arr_delay'], bins=int(r/bin), range=(rs, re))
            arr_df = pd.DataFrame({
                'proportion': arr_hist / np.sum(arr_hist),
                'left': edge[:-1],
                'right': edge[1:]
            })
            arr_df['f_proportion'] = ['%0.5f' % p for p in arr_df['proportion']]
            arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
            arr_df['name'] = r_data
            arr_df['color'] = Category20_16[i % len(Category20_16)]
            d = pd.concat([d, arr_df], ignore_index=True)

        d = d.sort_values(['name', 'left'])
        return ColumnDataSource(d)

    def mp(s_data):
        p = figure(plot_width=700, plot_height=700, title='Flight Delay')
        p.quad(source=s_data, bottom=0, top='proportion', left='left', right='right',
               color='color', fill_alpha=0.7, legend_field='name')
        return p

    def update(attr, old, new):
        air_line_checked = [chbox.labels[i] for i in chbox.active]
        ds = md(air_line_checked)
        src.data = ds.data

    # لیست خطوط هوایی
    air_lines = sorted(list(set(data['name'])))
    colors = Category20_16

    # ویجت‌ها
    chbox = CheckboxGroup(labels=air_lines, active=[0, 1])
    chbox.on_change('active', update)

    slider = Slider(start=1, end=30, step=1, value=5, title='bin size')
    slider.on_change('value', update)

    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title='delay range')
    range_slider.on_change('value', update)

    # داده‌ی اولیه
    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data)
    p = mp(src)

    # لایه‌بندی
    w = column(chbox, slider, range_slider)
    l = row(w, p)
    tab = Panel(child=l, title='panel')
    return tab
