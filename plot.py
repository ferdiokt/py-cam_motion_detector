from bokeh.models.sources import ColumnDataSource
from bokeh.models.tools import HoverTool
from main import time_df
from bokeh.plotting import figure, output_file, show

time_df["Start_string"]= time_df["Motion Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
time_df["End_string"]= time_df["Motion End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(time_df)

time_figure= figure(width= 500, height= 100, x_axis_type= "datetime",
                    sizing_mode= "scale_width", title= "Motion Graph")

hover= HoverTool(tooltips= [("Start", "@Start_string"), ("End", "@End_string")])
time_figure.add_tools(hover)

time_plot= time_figure.quad(left= "Motion Start",
                            right= "Motion End",
                            bottom= 0, top= 1, source= cds)

output_file("motion_detected_plot.html")
show(time_figure)