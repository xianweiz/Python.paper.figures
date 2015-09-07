###############################################
#               by Xianwei Zhang(xianwei@outlook.com)
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
start_col=config.getint(cfg_section, 'start_col') #col index in the data file for the 1st bar
NUM_BARS=config.getint(cfg_section, 'num_bars') #number of cluster bars in the figure
bar_gap=config.getfloat(cfg_section, 'bar_gap') #gap between bars in a cluster
cluster_gap=config.get(cfg_section, 'cluster_gap') #gap between clusters
colors=config.get(cfg_section, 'bar_colors') #color set for the bars
color_list = colors.split(',')
patterns = config.get(cfg_section, 'bar_patterns') #pattern set for the bars
pattern_list = patterns.split(',')
cfg_labels=config.get(cfg_section, 'bar_labels') #color set for the bars
rotation_angle = config.get(cfg_section, 'rotation') #ratation of x tick labels

#-- font setting
font = {'family' : font_family,
        'weight' : font_weight,
        'size'   : font_size}
pl.rc('font', **font)

#-- csvrec: load data from comma/space/tab delimited file in 'fname' into a numpy record and return the record array
data = csv2rec(datafile, delimiter=' ')
#-- first line as headers
headers = data.dtype.names #-- workload, scheme_1, scheme_2, scheme_3, ...
p_headers = headers[start_col:start_col+NUM_BARS] #-- discard some cols
labels = np.asarray(p_headers)

#-- if empty (no setting in cfg), then extract from data file
if len(cfg_labels.strip()) == 0:
	legend_labels = []
	for s in p_headers:
		capt_wd = s.title() #-- first letter capital
		legend_labels.append(capt_wd)
#-- if NOT empty (has been set in cfg), then use the provided one
else:
	legend_labels = cfg_labels.split(',')
#print (legend_labels)

#-- set figure size: e.g., 14in wide, 6in high, 80 dots per inch
pl.figure(figsize=(figure_w,figure_h), dpi=80)
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)

#-- draw the bars
if len(cluster_gap.strip()) == 0:
    bar_width = 1.0/(NUM_BARS+1) #-- cluster gap equals to bar_width
else:
    bar_width = (1.0-float(cluster_gap))/(NUM_BARS)#the remaining space is evenly divided among bars

for i in range(NUM_BARS): #-- draw each bar
	loc = bar_width*i
	pl.bar((np.arange(len(data))+loc), data[labels[i]], width=bar_width-bar_gap, color=color_list[i], label=legend_labels[i], hatch=pattern_list[i], align='center')

#--adding a legend
pl.legend(loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})
#--labeling the axes
#pl.ylabel(ynote, fontsize=24)
pl.ylabel(ynote)
#--setting y-axis range
pl.ylim(ylow, yhigh)
pl.yticks(np.linspace(ylow,tick_high,num_ticks,endpoint=True))
margin=bar_width+(1-len(labels)*bar_width)
#-- setting x-axis
pl.xlim(side_margin-margin,len(data)-side_margin)
if len(xnote.strip()) != 0:
    pl.xlabel(xnote)

#--adding minor ticks, one tick every 0.02 unit
#ml = MultipleLocator(10)
#pl.axes().yaxis.set_minor_locator(ml)
#--drawing lines for major and minor ticks
#pl.grid(True)
pl.axes().yaxis.grid(b=True, which='major', color='k', linestyle='--')
#pl.axes().yaxis.grid(b=True, which='minor', color=(0.5,0.5,0.5), linestyle=':')
#--setting the tick marks
pl.xticks(np.arange(len(data))+bar_width*0.5*(NUM_BARS-1), data[headers[0]], rotation=rotation_angle)
pl.tick_params(top="off")
pl.tick_params(bottom="off")

#pl.show()
#pl.savefig(datafile + ".eps", format='eps', dpi=1000, bbox_inches='tight')
pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
