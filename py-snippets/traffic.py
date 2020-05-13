import matplotlib as mpl
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

# From: https://gist.github.com/jgrahamc/38950ddaa928b2d89c3776b1c8ce73a4

# grey is the colour of the horizontal grid lines, blue the chart line
# Since matplotlib uses dpi and inches (!) need to have the DPI value
# and pixels and then convert to inches (see below)
grey = '#D7D7D7'
blue = '#00A1FF'
dpi = 144
w=1280
h=1024

countries = pd.read_csv('./countries.csv', encoding='utf8')
traffic = pd.read_csv('./all.csv', parse_dates=['Date'])

for c in traffic.Country.unique():

    # subplots_adjust done to leave room at bottom for vertical dates
    # on the X-axis
    fig, ax = plt.subplots(figsize=(w/dpi, h/dpi), dpi=dpi)
    fig.subplots_adjust(bottom=0.2)

    # Filter the traffic by the Country column and retrieve the
    # country's name. Note for some countries we need to add 'the ' to
    # make a readable title for the chart.
    country = traffic[traffic.Country == c]
    country_name = countries[countries['Code'] == c].iloc[0]['Name']
    prefix = ('', 'the ')[country_name.startswith(('United', 'Nether', 'US'))]
    ax.set_title("Change in Internet traffic in %s%s seen by Cloudflare" % (prefix, country_name),
                 pad=20)

    # Remove border from the top, LHS and RHS of the chart (i.e. just
    # leave the X-axis). And use grid/tick_params to make horizontal
    # lines that align with the Y-axis ticks
    for s in ['top', 'left', 'right']:
        ax.spines[s].set_visible(False)
    ax.grid(axis='y', color=grey)
    ax.tick_params(axis='y', color=grey)

    # Average the data over a seven day sliding window and normalize
    # the data to 1 on the first average.
    window = 7
    roll = country.Count.rolling(window).mean()
    roll = roll.divide(roll.iloc[window]).iloc[window:]

    # Try to find out a "nice" interval for the ticks on the X-axis,
    # try weekly, every 5 days, every 11 days, ... retry 7 at the end
    # so that we default to weekly if all else fails. Not that count
    # is decreased by one because want to try to get the first date
    # and last date appearing as ticks
    x = country.Date.iloc[window:]
    count, = x.shape
    count = count - 1
    for d in [7, 5, 11, 3, 7]:
        if count % d == 0:
            break
    plt.xticks(x.iloc[::d], rotation='vertical')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    # Scale the Y-axis into no more than 10 ticks that are 0.1, 0.2, 0.3 etc. apart
    yfloor = np.floor(roll.min()*10)
    yceil = np.ceil(roll.max()*10)
    ytick_range = yceil - yfloor
    ytick_spacing = np.floor(ytick_range/10)+1
    ytick_count = np.ceil(ytick_range/ytick_spacing)
    print(country_name, yfloor, yceil, ytick_range, ytick_spacing, ytick_count)
    ticks = [(yfloor+x)/10 for x in np.arange(0, ytick_spacing*(ytick_count+1), ytick_spacing)]
    plt.yticks(ticks)
    ax.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: '%1.1fx' % x))
    ax.set_ylim(ticks[0], ticks[-1])

    # Draw and save the chart. The chart name is the country name .png
    ax.plot(x, roll, linewidth=3, linestyle='solid', color=blue, marker='None')
    plt.savefig('country-list/%s.png' % country_name, dpi=dpi)
    plt.close()