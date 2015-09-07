###############################################
#               by Xianwei Zhang
###############################################

#-- the module does most array and mathematical manipulation
import numpy as np
#-- the module for plotting
import pylab as pl
#-- matplotlib: the whole package, a library for plotting
#-- matplotlib.pyplot: a module in matplotlib, a wrapper module to provide a Matlab-style interface to matplotlib.
#-- pylab: a module that gets installed alongside matplotlib, a mode in which pyplot and numpy are imported in a single namespace.
from matplotlib.mlab import csv2rec 
from matplotlib.ticker import MultipleLocator
import sys
import ConfigParser

datafile = sys.argv[1] #figure data file
cfgfile = sys.argv[2] #figure config file
cfg_section = sys.argv[3] #figure cfg section

#-- parse the config file to get each parameter value
config = ConfigParser.ConfigParser()
config.read(cfgfile)

##-- ******************** figure **************************
figure_w = config.getint(cfg_section, 'figure_width') #figure width
figure_h = config.getint(cfg_section, 'figure_height') #figure height
figure_f = config.get(cfg_section, 'figure_format') #figure format
figure_title = config.get(cfg_section, 'figure_title') #figure title
##-- ******************** font ****************************
font_family = config.get(cfg_section, 'font_family')
font_weight = config.get(cfg_section, 'font_weight')
font_size = config.getint(cfg_section, 'font_size')
##-- ******************** legend **************************
legend_size_diff = config.getint(cfg_section, 'legend_font_size') #font size difference between legend and others
legend_loc = config.get(cfg_section, 'legend_loc') #legend location
legend_cols = config.getint(cfg_section, 'legend_cols') #number of legend cols
##-- ******************** axis ****************************
ylow=config.getfloat(cfg_section, 'ylow') #min value of y axis
yhigh=config.getfloat(cfg_section, 'yhigh') #max value of y axis
y_tick_low=config.getfloat(cfg_section, 'y_tick_low') #min tick value of y axis
y_tick_high=config.getfloat(cfg_section, 'y_tick_high') #max tick value of y axis
y_num_ticks=config.getint(cfg_section, 'y_num_ticks') #number of ticks on y axis
ynote = config.get(cfg_section, 'ynote') #label of y axis
xlow=config.getfloat(cfg_section, 'xlow') #min value of x axis
xhigh_str=config.get(cfg_section, 'xhigh') #max value of x axis
x_tick_low=config.getfloat(cfg_section, 'x_tick_low') #min tick value of x axis
x_tick_high=config.getfloat(cfg_section, 'x_tick_high') #max tick value of x axis
x_num_ticks=config.getint(cfg_section, 'x_num_ticks') #number of ticks on x axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** sub *****************************
lines_per_sub = config.getint(cfg_section, 'lines_per_sub') #number of file lines in each sub
rows_in_graph = config.getint(cfg_section, 'rows_in_graph') #rows in the whole graph
line_data=config.get(cfg_section, 'line_data')
line_data_list = line_data.split(',')
line_colors=config.get(cfg_section, 'line_colors') #color set for the lines
line_color_list = line_colors.split(',')
patterns = config.get(cfg_section, 'line_patterns') #pattern set for the lines
pattern_list = patterns.split(',')
marker_colors=config.get(cfg_section, 'marker_colors') #color set for the markers
marker_color_list = marker_colors.split(',')
marker_patterns = config.get(cfg_section, 'marker_patterns') #pattern set for the markerss
marker_pattern_list = marker_patterns.split(',')
marker_sizes = config.get(cfg_section, 'marker_size') #size set for the markers
marker_size_list = marker_sizes.split(',')

def find(ss, list_seq):
	"""Return first item in sequence where f(item) == True."""
	for item in list_seq:
		if item in ss:
			return True
	return False

#-- font setting
font = {'family' : font_family,
        'weight' : font_weight,
        'size'   : font_size}
pl.rc('font', **font)

#-- set figure size: e.g., 14in wide, 6in high, 80 dots per inch
#pl.figure(figsize=(figure_w,figure_h), dpi=80)
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)

#-- read data file
with open(datafile) as f:
	data = f.read().splitlines()
num_rows = len(data)

#-- get the least number of points
shortest_row = 1000
longest_row = 0
graph_rows = []
for ind in range(num_rows):
	row = data[ind].split(" ")
	line_label = row[0]
	if len(line_data.strip()) == 0 or find(line_label, line_data_list):
		row_data = row[1:]
		r_len = len(row_data)
		if r_len > longest_row:
			longest_row = r_len
		if r_len < shortest_row:
			shortest_row = r_len
		graph_rows.append(row)

print 'shortest_row=',shortest_row,'\tlongest_row=',longest_row

#-- if 'MAX', then longest
if xhigh_str == 'max':
	xhigh = longest_row
#-- if 'MIN', then shortest
elif xhigh_str == 'min':
	xhigh = shortest_row
#-- ow, setting value
else:
	xhigh = float(xhigh_str)

#-- num of lines to be drawn in a graph
#-- how many sub-graphs to draw
graphs_to_plot = int(len(graph_rows)/lines_per_sub)
#-- how may rows in the graph
#-- how may sub-graphs per row
graphs_per_row = int(graphs_to_plot/rows_in_graph)

#f = pl.figure(1)
#pl.subplots(rows_in_graph,graphs_per_row,sharex='col', sharey='row')
pl.subplots(rows_in_graph,graphs_per_row,figsize=(figure_w, figure_h))
pl.subplots_adjust(hspace = 0.3)
#-- 1st sub-graph
ax1 = pl.subplot(rows_in_graph,graphs_per_row,1)

#-- 0	1	2	3
#-- 4	5	6	7
#-- 8	9	10	11
for ind in range(graphs_to_plot):
	ax = pl.subplot(rows_in_graph,graphs_per_row,ind+1) #, sharex=ax1,sharey=ax1)
	#-- non-bottom subgraphs, no x tick labels
	if ind+1<=graphs_per_row*(rows_in_graph-1): 
		pl.setp(ax.get_xticklabels(), visible=False)
	else:#-- bottom one, show x tick labels
		if len(xnote.strip()) != 0:
			ax.set_xlabel(xnote)

	#-- non-leftmost subgraphs, no y tick labels
	if ind%graphs_per_row != 0: 
		pl.setp(ax.get_yticklabels(), visible=False)
	else:#-- leftmost ones, show y tick labels
		pl.ylabel(ynote)

	#-- draw each line of the subgraph
	for line_inner_ind in range(lines_per_sub):
		#-- calcualte the row ID in the file of this subgraph line
		line_ind = lines_per_sub*(ind) + line_inner_ind
		#-- fetch the file data row
		row = graph_rows[line_ind]
		#-- scheme name
		line_label = row[0].split("_")[1]
		#-- workload name
		x_label = row[0].split("_")[0]
		x = range(1,len(row))
		y = row[1:]
		pl.plot(x, y, pattern_list[line_inner_ind], color=line_color_list[line_inner_ind], marker=marker_pattern_list[line_inner_ind], markeredgecolor=marker_color_list[line_inner_ind],markerfacecolor=marker_color_list[line_inner_ind], markersize=int(marker_size_list[line_inner_ind]), linewidth=1, label=line_label)
		if line_inner_ind == 1:
			pl.xlim(xlow,xhigh)
			pl.xticks(np.linspace(x_tick_low,x_tick_high,x_num_ticks,endpoint=True))
			pl.ylim(ylow, yhigh)
			pl.yticks(np.linspace(y_tick_low,y_tick_high,y_num_ticks,endpoint=True))
			pl.title(x_label)
	if ind == 0:
		pl.legend(loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})

#pl.legend(loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff},bbox_to_anchor=(0.3, 1.26), borderaxespad=0.)
pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
