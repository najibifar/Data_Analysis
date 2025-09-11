import pandas as pd
from bokeh.plotting import figure, output_file, show 
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool

output_file('thor1.html')

data = pd.read_csv('thor_wwii.csv')
dataSource = ColumnDataSource(data)


p = figure()
p.circle(source=dataSource, size=15, x='AC_ATTACKING', y='TOTAL_TONS', color='green')
p.title.text = 'عملیات هوایی جنگ جهانی دوم'
p.xaxis.axis_label = 'تعداد نیروهای هوایی'
p.yaxis.axis_label = ' حجم انفجار'

h = HoverTool()
h.tooltips = [
    ('تاریخ حمله', '@MSNDATE')

]

p.add_tools(h)
show(p)