import pandas as pd
from bokeh.plotting import figure, output_file, show 
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
output_file('thor2.html')

data = pd.read_csv('thor_wwii.csv')
dataGrouped = data.groupby('COUNTRY_FLYING_MISSION')[['TOTAL_TONS', 'TONS_FRAG','TONS_IC','TONS_HE']].sum()
print(dataGrouped)