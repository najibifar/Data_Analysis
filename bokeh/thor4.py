import pandas as pd
from bokeh.plotting import figure, output_file, show 
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
output_file('thor4-resample.html')

data = pd.read_csv('thor_wwii.csv')
data['MSNDATE'] = pd.to_datetime(data['MSNDATE'], format='%m/%d/%Y')
dataGrouped = data.groupby('MSNDATE')[['TOTAL_TONS', 'TONS_FRAG','TONS_IC','TONS_HE']].sum()
dataSource = ColumnDataSource(dataGrouped)
p = figure(x_axis_type='datetime')
p.line(x='MSNDATE', y='TOTAL_TONS', source=dataSource, legend_label='complet_explotion', line_width=2, color='blue')
p.line(x='MSNDATE', y='TONS_IC', source=dataSource, legend_label='complet_explotion', line_width=2, color='green')
p.line(x='MSNDATE', y='TONS_HE', source=dataSource, legend_label='complet_explotion', line_width=2, color='red')

show(p)