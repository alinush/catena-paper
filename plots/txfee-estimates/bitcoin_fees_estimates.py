#import pylab as P
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.dates import MonthLocator, DateFormatter, DayLocator,\
    epoch2num, num2date

import data_bitcoin_fees_estimates as estimate

x = estimate.date
y1 = estimate.one_block_fee
y0 = estimate.mempool_size
y2 = estimate.two_block_fee
y3 = estimate.three_block_fee
y4 = estimate.six_block_fee

# convert from unix epoch to matplotlib's own custom date format
for i in range(len(x)):
    x[i] = x[i]/1000    # we have milliseconds in our file
    x[i] = epoch2num(x[i])

assert len(x) == len(y0)
assert len(y0) == len(y1)
assert len(y1) == len(y2)
assert len(y2) == len(y3)
assert len(y3) == len(y4)

# adjust the size of the plot here: (20, 10) is bigger than (10, 5) in the
# sense that fonts will look smaller on (20, 10)
fig, ax1 = plt.subplots(figsize=(13, 5))

plt0, = ax1.plot(x, y0, color='gray', fillstyle='full')
plt.fill_between(x, y0, 0, color='0.8')


ax2 = ax1.twinx()
ax2.xaxis.set_major_locator(MonthLocator())
#ax2.xaxis.set_minor_locator(DayLocator())
ax2.xaxis.set_major_formatter(DateFormatter('%b \'%y'))
ax2.autoscale_view()
#ax2.set_xlim(x[0], x[len(x)-1])
print "min:", num2date(x[0]), "max", num2date(x[len(x)-1])

# NOTE: This doesn't seem to display the price when we hover over.
#def price(y):
#    return y + " satoshi/kB"
#
#ax2.fmt_ydata = price
#ax2.fmt_xdata = DateFormatter('%Y-%m-%d')
ax2.grid(True)


def satoshi_fmt(y, pos):
    return str(int(y/1000)) + ",000"


def mb_fmt(y, pos):
    return "%2.2f" % (y/1000000) + " MB"

ax1.set_ylabel("Mempool size (in MB)")
ax1.yaxis.set_major_formatter(FuncFormatter(mb_fmt))
ax2.set_ylabel('Min. fee per kB (satoshi/kB)')
ax2.yaxis.set_major_formatter(FuncFormatter(satoshi_fmt))

plt1, = ax2.plot_date(x, y1, '-', color='blue')
plt2, = ax2.plot_date(x, y2, '-', color='orange')
plt3, = ax2.plot_date(x, y3, '-', color='green')
plt4, = ax2.plot_date(x, y4, '-', color='red')

plt.legend([plt0, plt1, plt2, plt3, plt4],
           ['mempool', 'within 1 block', 'within 2 blocks', 'within 3 blocks', 'within 6 blocks'],
           fontsize='small', loc='best')

fig.autofmt_xdate()
plt.title('Min TX fee to confirm within K blocks (with 90% probability)')  # , fontsize=16)
#plt.xlabel('Date')
plt.show()

#plt.xticks(fontsize=16)
#plt.yticks(fontsize=16)
