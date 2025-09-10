from bokeh.plotting import figure, output_file, show
output_file('Hello.html')

x1 = [5, 6, 9, 10, 100, 120, 142, 160]
x2 = [8, 10, 18, 20, 30, 101, 111, 152]


p = figure()
p.line(x1, x2, color = 'blue', legend_label = 'line')
p.legend.click_policy = 'hide'

show(p)