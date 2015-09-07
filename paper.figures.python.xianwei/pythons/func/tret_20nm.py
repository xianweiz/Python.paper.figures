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
from scipy import integrate
from scipy.stats import lognorm
import math

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
##-- ******************** y axis ****************************
ylow=config.getfloat(cfg_section, 'ylow') #min value of y axis
yhigh=config.getfloat(cfg_section, 'yhigh') #max value of y axis
y_tick_high=config.getfloat(cfg_section, 'y_tick_high') #max tick value of y axis
y_num_ticks=config.getint(cfg_section, 'y_num_ticks') #number of ticks on y axis
ynote = config.get(cfg_section, 'ynote') #label of y axis
##-- ******************** x axis ****************************
xlow=config.getfloat(cfg_section, 'xlow') #min value of x axis
xhigh=config.getfloat(cfg_section, 'xhigh') #max value of x axis:min/max/number
x_tick_high=config.getfloat(cfg_section, 'x_tick_high') #max tick value of x axis
x_ticks=config.get(cfg_section, 'x_ticks') #ticks on x axis
x_tick_list = x_ticks.split(',')
x_num_ticks=len(x_tick_list)
x_minor_tick=config.get(cfg_section, 'x_minor_tick_interval') #minor tick on x axis
xnote = config.get(cfg_section, 'xnote') #label of x axis
##-- ******************** bar *****************************
line_data=config.get(cfg_section, 'line_data') #which line to draw: if empty, then draw all rows in the file
line_data_list = line_data.split(',')
line_width=config.getint(cfg_section, 'line_width') #line width
colors=config.get(cfg_section, 'line_colors') #color set for the lines
color_list = colors.strip().split(',')
patterns = config.get(cfg_section, 'line_patterns') #pattern set for the lines
pattern_list = patterns.split(',')
marker_patterns = config.get(cfg_section, 'marker_patterns') #pattern set for the markers
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
pl.figure(figsize=(figure_w,figure_h), dpi=80)
#--setting the title
if len(figure_title.strip()) != 0:
    pl.title(figure_title)

def graph(formula, x_range, my_color):  
	x = np.array(x_range)  
	y = eval(formula)
	pl.plot(x, y, color=my_color, linewidth=1.5)  
	#pl.show()

def lognorm_cdf(x,mu=0,sigma=1):
	a = (math.log(x) - mu)/math.sqrt(2*sigma**2)
	p = 0.5 + 0.5*math.erf(a)
	return p
#60nm, mu=5.6, sigma=1.2
#mu, sigma = 5.6, 1.2 # mean and standard deviation
#graph('(np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))',
#	   	pl.linspace(1e-2, 1e3, 10000), 'green')

#20nm
mu_bulk, sigma_bulk = 3.55, 1.05
mu_tail, sigma_tail = -0.88, 0.665
#pdf = (np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) / (x * sigma * np.sqrt(2 * np.pi)))
graph('(np.exp(-(np.log(x) - mu_bulk)**2 / (2 * sigma_bulk**2)) / (x * sigma_bulk * np.sqrt(2 * np.pi)))',
	   	pl.linspace(0.23, 1e3, 10000), 'black')
graph('(np.exp(-(np.log(x) - mu_tail)**2 / (2 * sigma_tail**2)) / (x * sigma_tail * np.sqrt(2 * np.pi)))/1e5',
	   	pl.linspace(1e-2, 0.23, 1000), 'black')

cdf_tx = [0.032, 0.064, 0.128]
#print cdf_tx
cdf_ty = [lognorm_cdf(xx, mu_tail, sigma_tail)/1e5 for xx in cdf_tx]
#print cdf_ty
pl.plot(cdf_tx,cdf_ty, color='black', linestyle='--', marker='x', markersize=10)

pl.plot([0.128,0.256], [lognorm_cdf(0.128, mu_tail, sigma_tail)/1e5, lognorm_cdf(0.256, mu_bulk, sigma_bulk)+1.88e-6], color='black', linestyle='--', marker='x', markersize=10)

cdf_bx = [0.256, 0.512, 1.024, 2.048, 4.096, 16.384, 64, 100, 500, 1000]
#print cdf_bx
cdf_by = [lognorm_cdf(xx, mu_bulk, sigma_bulk)+1.88e-6 for xx in cdf_bx]
#cdf_by[0] = 1.88e-6
#print cdf_by

print '20nm:'
for ii in range(len(cdf_tx)+len(cdf_bx)):
	if ii < len(cdf_tx):
		print '%6s: %.4e' % (cdf_tx[ii], cdf_ty[ii])
	else:
		ind = ii - len(cdf_tx)
		print '%6s: %.4e' % (cdf_bx[ind], cdf_by[ind])

pl.plot(cdf_bx,cdf_by, color='black', linestyle='--', marker='x', markersize=10)
#ax=pl.gca()

pl.text(0.1e2,1e-3, 'pdf', fontsize=40)
pl.text(0.3e1,1e-1, 'cdf', fontsize=40)

#mu, sigma = 4.46, 1.2 # mean and standard deviation
#cdf_x = [0.032, 0.064, 0.128, 0.256, 0.512, 1.024, 2.048, 4.096, 16.384, 64, 100, 500, 1000]
#cdf_y = [lognorm_cdf(xx, mu, sigma) for xx in cdf_x]

#print '\n\n60nm:'
#for ii in range(len(cdf_x)):
#	print '%6s: %.4e' % (cdf_x[ii], cdf_y[ii])
#pl.plot(cdf_x,cdf_y, color='red', linestyle='--', marker='x', markersize=10)

#pl.xlim(x_low_1,x_high_1)
pl.xlim(1e-2,1e3)
#real_ticks = np.linspace(3,x_tick_high,x_num_ticks,endpoint=True)
#Vdd = 1.5
#percs = [0.59, 0.7, 0.8, 0.9, 1.0]
#real_ticks = [pp*Vdd for pp in percs]
#fake_ticks = real_ticks*10
#pl.xticks(real_ticks, x_tick_list)
#pl.xticks(real_ticks, fake_ticks, rotation='vertical')
#--adding a legend
#pl.legend(loc=legend_loc, ncol=legend_cols, prop={'size':font_size+legend_size_diff})
#--labeling the axes
pl.ylabel(ynote)
#--setting y-axis range
#pl.ylim(ylow, yhigh)
pl.ylim(1e-9,1e0)
#pl.yticks(np.linspace(1e-9,1e0,6,endpoint=True))
#-- setting x-axis
if len(xnote.strip()) != 0:
	pl.xlabel(xnote)
	#pl.axes().xaxis.set_label_coords(0.98, -0.065)

pl.xscale('log',basex=10, subsx=[2,3,4,5,6,7,8,9])
pl.yscale('log',basey=10, subsy=[2,3,4,5,6,7,8,9])

#--adding minor ticks, one tick every X unit
if len(x_minor_tick.strip()) != 0:
	ml = MultipleLocator(float(x_minor_tick))
	pl.axes().xaxis.set_minor_locator(ml)
#--drawing lines for major and minor ticks
pl.grid(True)
#pl.axes().yaxis.grid(b=True, which='major', color='k', linestyle='--')
#pl.axes().yaxis.grid(b=True, which='minor', color=(0.5,0.5,0.5), linestyle=':')
#--setting the tick marks
pl.tick_params(top="on")
pl.tick_params(bottom="on")

pl.savefig(datafile + "." + figure_f, format=figure_f, dpi=1000, bbox_inches='tight')
pl.close()
