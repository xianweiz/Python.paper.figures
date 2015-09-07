###############################################
#               by Xianwei Zhang
###############################################

import sys
import numpy as np
import pylab as pl
from matplotlib.mlab import csv2rec
from collections import OrderedDict
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
cfg_legends = config.get(cfg_section, 'legend_labels') #symbols #legend names, e.g., 1.0x/0.84x/0.3x
legends_list = cfg_legends.split(',')
##-- ******************** axis ****************************
ylow=config.getfloat(cfg_section, 'ylow') #min value of y axis
yhigh=config.getfloat(cfg_section, 'yhigh') #max value of y axis
tick_high=config.getfloat(cfg_section, 'tick_high') #max tick value of y axis
num_ticks=config.getint(cfg_section, 'num_ticks') #number of ticks on y axis
ynote = config.get(cfg_section, 'ynote') #label of y axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** bar *****************************
bar_width = config.getfloat(cfg_section, 'bar_width') #bar width
bar_gap=config.getfloat(cfg_section, 'bar_gap') #gap between bars in a cluster
colors=config.get(cfg_section, 'bar_colors') #color set for the bars
color_list = colors.split(',')
patterns = config.get(cfg_section, 'bar_patterns') #pattern set for the bars
pattern_list = patterns.split(',')
schemes = config.get(cfg_section, 'schemes') #schemes, e.g, ['default', 'base_preset', 'code_preset']
schemes_list = schemes.split(',')
cfg_symbols = config.get(cfg_section, 'symbols') #alias of scheme names, e.g. a/b/c
symbols_list = cfg_symbols.split(',')
cfg_headers = config.get(cfg_section, 'headers') #headers (i.e., workloads), e.g., ['wkld', 'zeu', 'Gem', ...]
cfg_cases = config.get(cfg_section, 'cases') #cases of each scheme, e.g., _norm/_fast/_very
cases_list = cfg_cases.split(',')
delim = config.get(cfg_section, 'delim_symbol_wkld').replace('\"', '') #bar width
rotation_angle = config.get(cfg_section, 'rotation') #ratation of x tick labels

#-- font setting
font = {'family' : font_family,
    'weight' : font_weight,
        'size'   : font_size}
pl.rc('font', **font)

#schemes = ['default', 'base_preset', 'code_preset']
NUM_SCHEMES = len(schemes_list) #how many schemes
NUM_SYMBOLS = len(symbols_list) #how many alias (=#schemes)
NUM_CASES = len(cases_list) #how many cases per scheme
NUM_LEGENDS = len(legends_list)
if NUM_SCHEMES != NUM_SYMBOLS:
	print "Ooops! #schemes must be equal to #symbols"
	sys.exit(1)
if NUM_CASES != NUM_LEGENDS:
	print "Ooops! #cases must be equal to #legends"
	sys.exit(1)
#-- label location for the cluster (better to be in middle)
cluster_label_location = (NUM_SYMBOLS-1)//2

num_workloads = 0

top_list = [] #-- list to save the whole data file (including the headers)

#-- read the data file, and re-organize the data from following plot
def readFile(filename) :
	global top_list
	global num_workloads
	data = csv2rec(filename, delimiter=' ')
	headers = data.dtype.names
    #print headers
    
    #-- num of workloads (cols)
	num_workloads = len(headers)-1
    
    #-- prepare the headers
	#-- header_list: {"a", "b\nast", "c", "a", ...}
	if len(cfg_headers.strip()) == 0:
	#-- if 'headers' is empty in the cfg file, then read from data file 
		header_list = []
		for i in xrange(1,num_workloads+1,1):
		#header_list.extend(["a","b\n"+headers[i],"c"])
			for ind in range(NUM_SYMBOLS):
				if(ind!=cluster_label_location): header_list.extend([symbols_list[ind]])
				else: header_list.extend([symbols_list[ind]+"\n"+delim+headers[i]])
	else: 
	#-- if 'headers' is provided in the cfg file, then use them
		cfg_headers_list = cfg_headers.split(',')
		header_list = []
		for i in xrange(1,num_workloads+1,1):
			for ind in range(NUM_SYMBOLS):
				if(ind!=cluster_label_location): header_list.extend([symbols_list[ind]])
				else: header_list.extend([symbols_list[ind]+"\n"+delim+cfg_headers_list[i]])
	top_list.append(header_list)

	#-- prepare the row data
	#-- pad '0's, according to the scheme
	for row in data: #-- row[0]: scheme_case
		row_list = []
		for i in xrange(1,num_workloads+1,1):
			for ind in range(NUM_SCHEMES): #-- add '0's to non_scheme locations
				if schemes_list[ind] in row[0]:
					if(ind>0):
						for bf in range(ind): row_list.extend([0])
					row_list.extend([row[i]])
					if(ind+1==NUM_SCHEMES):break
					for bf in range(ind+1,NUM_SCHEMES): row_list.extend([0])
		top_list.append(row_list)
#print row

readFile(datafile)

#print top_list
#sys.exit(1)

pl.figure(figsize=(figure_w,figure_h), dpi=800)

IDs = top_list[0] #1st row stores the headers

N = len(IDs) #-- N= NUM_SCHEMES*num_workloads

#-- [0, N-1]
#-- default_: 1,4,7,10,13
#-- basepreset_: 2,5,8,11,14
#-- codepreset_: 3,6,9,12,15
ind = np.arange(1,N+1)

bar_start_x = 1
bar_end_x = (N-NUM_SCHEMES+1)+bar_width*NUM_SCHEMES
#side_margin = bar_width/2
#print bar_end_x
#pl.xlim(0.6,N+0.6)
pl.xlim(bar_start_x-side_margin,bar_end_x+side_margin)
pl.ylim(ylow, yhigh)
pl.yticks(np.linspace(ylow,tick_high,num_ticks,endpoint=True))

#bar_width = 0.66 #-- width of each bar
step = 1.0 - bar_width #-- gap between groups is also 0.75

#-- record the bar locaions for later xticks
tick_locs = []

list_len = len(top_list) #-- how many rows, #rows=NUM_SCHEMES(default/base/code)*num_scheme_case(norm/fast/very)
#-- workload            zeu les ...
#-- default_norm        x   y   ...
#-- default_fast        x   y   ...
#-- default_very        x   y   ...
#-- base_preset_norm    x   y   ...
#-- base_preset_fast    x   y   ...
#-- base_preset_very    x   y   ...

for i in range(list_len):
    if i==0: continue #-- skip the first header row
    #-- _norm: 0, _fast: 0.25, _very: 0.5
    scheme_ind = (i-1)/NUM_CASES #
    loc = step*int(scheme_ind)
    
    case_ind = (i-1)%NUM_CASES #case (e.g., norm/fast/very) index within a scheme (default/base_preset/code_preset)
    #-- get the tick locations
    if case_ind == 0:
        tmp = ind-loc
        for dd in range(num_workloads):
            tick_locs.append(tmp[NUM_SCHEMES*dd+scheme_ind])

    #-- get the height of previous scheme bars
    bf_values_sum = 0
    for bf_case_ind in range(case_ind):
        bf_values_sum += np.asarray(top_list[i-bf_case_ind-1])

    #### plot steps:
    ####    (1) draw all '_norm' bars (decide the bar locactions)
    ####    (2) stack '_fast' and '_very' atop of '_norm' (same bar locations as '_norm')
#print ind-loc
    pl.bar(ind-loc, np.asarray(top_list[i]), width=bar_width-bar_gap, bottom=bf_values_sum, color=color_list[case_ind], hatch=pattern_list[case_ind], label=legends_list[case_ind])

#tick_locs = []
#for i in range(N): tick_locs.append(i/3*3+1+bar_width*int(i%3))
#-- sort the ticks
tick_locs.sort()
#print tick_locs
tick_locs = np.asarray(tick_locs)
#-- place labels in the center
pl.xticks(tick_locs+bar_width/2., IDs,  rotation=rotation_angle)
pl.tick_params(top="off")
pl.tick_params(bottom="off")
if len(xnote.strip()) != 0:
    pl.xlabel(xnote)

#pl.ylabel(ynote, fontsize=24)
pl.ylabel(ynote)

#-- draw the legend, remove the duplicate labels
#-- legend takes as arguments a list of axis handles and labels
handles, labels = pl.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
pl.legend(by_label.values(), by_label.keys(), loc=legend_loc, ncol=legend_cols, prop={'size':font_size-legend_size_diff})
pl.axes().yaxis.grid(b=True, which='major', color='k', linestyle='--')

#pl.title('(a)WP   (b)WP+P_SET   (c)WP+T_SET', fontsize=24)
pl.title(figure_title, fontsize=font_size)

#pl.show()
#pl.savefig(datafile + ".eps", format='eps', bbox_inches='tight')
pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
