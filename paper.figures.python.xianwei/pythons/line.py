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
side_margin = config.getfloat(cfg_section, 'side_margin') #gap to outsider border
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
tick_high=config.getfloat(cfg_section, 'tick_high') #max tick value of y axis
num_ticks=config.getint(cfg_section, 'num_ticks') #number of ticks on y axis
ynote = config.get(cfg_section, 'ynote') #label of y axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** bar *****************************
line_data=config.get(cfg_section, 'line_data')
line_data_list = line_data.split(',')
colors=config.get(cfg_section, 'line_colors') #color set for the bars
color_list = colors.split(',')
patterns = config.get(cfg_section, 'line_patterns') #pattern set for the bars
pattern_list = patterns.split(',')
marker_patterns = config.get(cfg_section, 'marker_patterns') #pattern set for the bars
marker_pattern_list = marker_patterns.split(',')
marker_sizes = config.get(cfg_section, 'marker_size') #pattern set for the bars
marker_size_list = marker_sizes.split(',')
rotation_angle = config.get(cfg_section, 'rotation') #ratation of x tick labels

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

#-- csvrec: load data from comma/space/tab delimited file in 'fname' into a numpy record and return the record array
#data = csv2rec(datafile, delimiter=' ')

#-- set figure size: e.g., 14in wide, 6in high, 80 dots per inch
pl.figure(figsize=(figure_w,figure_h), dpi=80)
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)

with open(datafile) as f:
	data = f.read().splitlines()
num_rows = len(data)

#-- get the least number of points
NUM_X_POINTS = 1000
graph_rows = []
for ind in range(num_rows):
	row = data[ind].split(" ")
	line_label = row[0]
	if find(line_label, line_data_list) or len(line_label.strip())==0:
		row_data = row[1:]
		num_data = len(row_data)
		if(num_data < NUM_X_POINTS):
			NUM_X_POINTS = num_data
		graph_rows.append(row)

for ind in range(len(graph_rows)):
	row = graph_rows[ind]
	line_label = row[0]
	x = range(1, NUM_X_POINTS)
	y = row[1:NUM_X_POINTS]
#pl.plot(x, y, pattern_list[ind], color=color_list[ind], linewidth=2, label=line_label)
	pl.plot(x, y, pattern_list[ind], color=color_list[ind], marker=marker_pattern_list[ind], markersize=int(marker_size_list[ind]), linewidth=2, label=line_label)

pl.xlim(1,NUM_X_POINTS+1)
num_x_ticks = int(NUM_X_POINTS/10)
print NUM_X_POINTS, num_x_ticks
real_ticks = np.linspace(0,num_x_ticks*10,num_x_ticks/2+1,endpoint=True)
#pl.xticks(np.linspace(0,90,10,endpoint=True))
fake_ticks = real_ticks*10
pl.xticks(real_ticks, fake_ticks)
#--adding a legend
pl.legend(loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})
#--labeling the axes
#pl.ylabel(ynote, fontsize=24)
pl.ylabel(ynote)
#--setting y-axis range
pl.ylim(ylow, yhigh)
pl.yticks(np.linspace(ylow,tick_high,num_ticks,endpoint=True))
#-- setting x-axis
if len(xnote.strip()) != 0:
	pl.xlabel(xnote)
	pl.axes().xaxis.set_label_coords(0.98, -0.065)

#--adding minor ticks, one tick every 0.02 unit
ml = MultipleLocator(1)
pl.axes().xaxis.set_minor_locator(ml)
#--drawing lines for major and minor ticks
#pl.grid(True)
pl.axes().yaxis.grid(b=True, which='major', color='k', linestyle='--')
#pl.axes().yaxis.grid(b=True, which='minor', color=(0.5,0.5,0.5), linestyle=':')
#--setting the tick marks
pl.tick_params(top="on")
pl.tick_params(bottom="on")

#pl.show()
#pl.savefig(datafile + ".eps", format='eps', dpi=1000, bbox_inches='tight')
pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
