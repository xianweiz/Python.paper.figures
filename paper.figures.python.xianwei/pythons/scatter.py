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
##-- ******************** y-axis ****************************
ylow=config.getfloat(cfg_section, 'ylow') #min value of y axis
yhigh=config.getfloat(cfg_section, 'yhigh') #max value of y axis
y_tick_high=config.getfloat(cfg_section, 'y_tick_high') #max tick value of y axis
y_num_ticks=config.getint(cfg_section, 'y_num_ticks') #number of ticks on y axis
ynote = config.get(cfg_section, 'ynote') #label of y axis
##-- ******************** x-axis ****************************
xlow=config.getfloat(cfg_section, 'xlow') #min value of y axis
xhigh=config.getfloat(cfg_section, 'xhigh') #max value of y axis
x_tick_high=config.getfloat(cfg_section, 'x_tick_high') #max tick value of y axis
x_num_ticks=config.getint(cfg_section, 'x_num_ticks') #number of ticks on y axis
x_minor_tick=config.get(cfg_section, 'x_minor_tick_interval') #minor tick on x axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** bar *****************************
colors=config.get(cfg_section, 'colors') #color set for the bars
color_list = colors.split(',')
marker_patterns = config.get(cfg_section, 'marker_patterns') #pattern set for the bars
marker_pattern_list = marker_patterns.split(',')
marker_sizes = config.get(cfg_section, 'marker_size') #pattern set for the bars
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
pl.figure(figsize=(figure_w,figure_h), dpi=80)
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)


#--read the whole file and break it into rows 
with open(datafile) as f:
	data = f.read().splitlines()
num_rows = len(data)

#-- randomly generate colors
if len(color_list)<num_rows:
	color_list = []
	prev_marker_pattern = 'not_a_pattern'
	for ind in range(len(marker_pattern_list)):
		marker_pattern = marker_pattern_list[ind]
		#-- if a new pattern, then create a new color
		if marker_pattern != prev_marker_pattern:
			new_color = np.random.rand(3,1)
		color_list.append(new_color)
		prev_marker_pattern = marker_pattern

#-- draw for each row in the graph
for ind in range(num_rows):
	row = data[ind].split("\t")
	type_label = row[0]
	y_data = row[1]
	x_data = row[2]

	#-- if type is "-", no label 
	if type_label == "-":
		pl.scatter(x_data,y_data,c=color_list[ind],marker=marker_pattern_list[ind],s=int(marker_size_list[ind]))
	else:
		pl.scatter(x_data,y_data,c=color_list[ind],marker=marker_pattern_list[ind],s=int(marker_size_list[ind]),label=type_label)
		#-- control the label position
		x_shift = 0; y_shift = 0
		if type_label == "DDR3":
			x_shift = -12.5; y_shift = 0.5
		elif type_label == "DDR4":
			x_shift = 7; y_shift = 0
		elif type_label == "GDDR5":
			x_shift = 0; y_shift = -2
		elif type_label == "WideIO":
			x_shift = -10; y_shift = -1
		elif type_label == "WideIO2":
			x_shift = 0; y_shift = 1
		elif type_label == "HBM":
			x_shift = 3; y_shift = 0
		elif type_label == "HMC":
			x_shift = 0; y_shift = 0.5
		pl.annotate(type_label, (float(x_data)+x_shift, float(y_data)+y_shift),fontsize=font_size)

#-- scatterpoints=1, show only one point in 'scatter' plot, for normal plot, use 'numpoints=1'
#-- http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
pl.legend(scatterpoints=1,loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})
pl.xlim(xlow, xhigh)
pl.xticks(np.linspace(xlow,x_tick_high,x_num_ticks,endpoint=True))
pl.ylabel(ynote)
#--setting y-axis range
pl.ylim(ylow-1, yhigh)
pl.yticks(np.linspace(ylow,y_tick_high,y_num_ticks,endpoint=True))
#-- setting x-axis
if len(xnote.strip()) != 0:
	pl.xlabel(xnote)

#--adding minor ticks, one tick every X unit
if len(x_minor_tick.strip()) != 0:
	ml = MultipleLocator(float(x_minor_tick))
	pl.axes().xaxis.set_minor_locator(ml)
#--drawing lines for major and minor ticks
#pl.grid(True)
pl.axes().yaxis.grid(b=True, which='major', color='k', linestyle='--')
#pl.axes().yaxis.grid(b=True, which='minor', color=(0.5,0.5,0.5), linestyle=':')
#--setting the tick marks
pl.tick_params(top="off")
pl.tick_params(bottom="on")

pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
