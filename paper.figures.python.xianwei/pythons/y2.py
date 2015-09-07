###############################################
#               by Xianwei Zhang
###############################################

import numpy as np
import pylab as pl
import sys
import csv
import ConfigParser

datafile = sys.argv[1] #figure data file
cfgfile = sys.argv[2] #all figures config file
cfg_section = sys.argv[3] #section for a figure

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
y1_low=config.getfloat(cfg_section, 'y1_low') #min value of y1 axis
y1_high=config.getfloat(cfg_section, 'y1_high') #max value of y1 axis
y1_tick_high=config.getfloat(cfg_section, 'y1_tick_high') #max tick value of y1 axis
y1_note = config.get(cfg_section, 'y1_note') #label of y1 axis

y2_low=config.getfloat(cfg_section, 'y2_low') #min value of y2 axis
y2_high=config.getfloat(cfg_section, 'y2_high') #max value of y2 axis
y2_tick_high=config.getfloat(cfg_section, 'y2_tick_high') #max tick value of y2 axis
y2_note = config.get(cfg_section, 'y2_note') #label of y2 axis

num_ticks=config.getint(cfg_section, 'num_ticks') #number of ticks on y axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** bar/line *************************
bar_width = config.getfloat(cfg_section, 'bar_width') #bar width
cfg_metrics=config.get(cfg_section, 'metric_names') #metric names
metrics_list = cfg_metrics.split(',')
y1_metric=config.get(cfg_section, 'y1_metric') #metric on y1 axis
colors=config.get(cfg_section, 'bar_colors') #color set for the bars
color_list = colors.split(',')
patterns = config.get(cfg_section, 'bar_patterns') #pattern set for the bars
pattern_list = patterns.split(',')
rotation_angle = config.get(cfg_section, 'rotation') #ratation of x tick labels

#-- read the data file and transpose row/column
#
# FROM:
# scheme    metric_1     metric_2
# lane4     x           y
# lane8     a           b
#
# TO:
# scheme    lane4       lane8
# metric_1   x           a
# metric_2 	 y           b
#
with open(datafile, 'rb') as csvfile:
	reader = [x.split() for x in csvfile] #csv.reader(csvfile)
	col_id = 0
	for column in zip(*reader):
		if col_id == 0: labels_list = column[1:]
		if col_id == 1: metric_1_list = column[1:]
		if col_id == 2: metric_2_list = column[1:]
		col_id += 1
#-- fake ticks, i.e. x labels
fake_ticks = np.asarray(labels_list)
#-- get real_ticks, some consecutive values
num_schemes = len(fake_ticks)
real_ticks = np.arange(1,num_schemes+1) #/2.0
#print real_ticks

#-- 'metric_1' data
metric_1_vals = map(float,np.asarray(metric_1_list))
#-- 'metric_2' data
metric_2_vals = map(float,np.asarray(metric_2_list))
#sys.exit(1)

#--set figure size: 14in wide, 6in high, 80 dots per inch
fig, ax1 = pl.subplots(figsize=(figure_w,figure_h))
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)

#font = { 'size'  : '24' }
#pl.rc('font', **font)

font = {'family' : font_family,
    'weight' : font_weight,
        'size'   : font_size}

pl.rc('font', **font)

ax2 = ax1.twinx()

if y1_metric == metrics_list[0]: #-- metric_1_vals is on y1 axis
	#-- draw the 'metric_1' bar
	ax1.bar(real_ticks, metric_1_vals, width=bar_width, color=color_list[0], label=metrics_list[0], hatch=pattern_list[0], align='center')
	#-- draw the 'metric_2' line
	ax2.plot(real_ticks, metric_2_vals, '-',c='grey', marker='^', markersize=20, markerfacecolor='k', linewidth=4, label=metrics_list[1])
else: #-- metric_2_vals is on y1 axis
	#-- draw the 'metric_2' bar
	ax1.bar(real_ticks, metric_2_vals, width=bar_width, color=color_list[0], label=metrics_list[1], hatch=pattern_list[0], align='center')
	#-- draw the 'metric_1' line
	ax2.plot(real_ticks, metric_1_vals, '-',c='grey', marker='^', markersize=20, markerfacecolor='k', linewidth=4, label=metrics_list[0])

#-- show legend, loc: http://matplotlib.org/api/legend_api.html
h1,l1=ax1.get_legend_handles_labels()
h2,l2=ax2.get_legend_handles_labels()
ax1.legend(h1+h2,l1+l2,loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})

#ax1.set_xlabel('Lanes of Request Link')
if len(xnote.strip()) != 0:
    ax1.set_xlabel(xnote)
#ax1.set_xlabel(fig_note)
pl.xticks(real_ticks, fake_ticks)
ax1.tick_params(top="off")
ax1.tick_params(bottom="off")
ax1.set_xticklabels(fake_ticks, rotation=rotation_angle)
#side_margin = 0.5
pl.xlim(1-side_margin,num_schemes+side_margin)

ax1.set_ylabel(y1_note, color='k',fontsize=font_size-2)
ax2.set_ylabel(y2_note, color='k',fontsize=font_size+1)
#ax2.set_ylabel(y2_note, color='k')

ax1.set_ylim(y1_low,y1_high)
ax1.set_yticks(np.linspace(y1_low,y1_tick_high,num_ticks,endpoint=True))
ax2.set_ylim(y2_low,y2_high)
ax2.set_yticks(np.linspace(y2_low,y2_tick_high,num_ticks,endpoint=True))
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='--')

#pl.show()
#pl.savefig(datafile + ".eps", format='eps', dpi=1000, bbox_inches='tight')
pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
