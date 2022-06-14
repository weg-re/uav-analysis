import os
import __main__ as main
import argparse
import pandas as pd
from pylab import plt

from read_uav_data import read_xq2_data

intaractive = not hasattr(main, '__file__')

remove_first_n_entries = 32

parser = argparse.ArgumentParser()
parser.add_argument('ifile', type=str, help='filename of xq2 log (csv file)')

if intaractive:
    ifile = 'xq2/20220525-142415-00058755.csv'
else:
    args = parser.parse_args()
    ifile = args.ifile

plotdir = f'plots/{os.path.splitext(ifile)[0]}'
os.makedirs(plotdir, exist_ok=True)

df = read_xq2_data(ifile)

df = df.iloc[remove_first_n_entries:]

df['alt'] = df['Altitude']
df.drop(columns=['Altitude'])

n_vars = df.shape[1]

plt.figure(figsize=(10, 20))
for i in range(n_vars):
    plt.subplot(n_vars, 1, i + 1)
    plt.plot(df[df.keys()[i]])
    plt.ylabel(df.keys()[i])
plt.savefig(f'{plotdir}/time_vs_vars.svg')
plt.savefig(f'{plotdir}/time_vs_vars.png')

plt.figure(figsize=(30, 10))
for i in range(n_vars):
    plt.subplot(1, n_vars, i + 1)
    plt.plot(df[df.keys()[i]].values, df['alt'], marker='x')
    plt.xlabel(df.keys()[i])
    plt.ylabel('alt')
plt.savefig(f'{plotdir}/alt_vs_vars.svg')
plt.savefig(f'{plotdir}/alt_vs_vars.png')
