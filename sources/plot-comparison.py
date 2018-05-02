import pandas as pd
import seaborn as sns

ngl = pd.read_table('../data/precomputed/ngless_benchmarks.tsv')
ngl.groupby([ngl.columns[0], ngl.columns[2]]).max()

mocat = pd.read_csv('../data/precomputed/mocat_benchmark.csv')
mocat.rename(columns={'Elapsed time': 'wallclock'}, inplace=True)
command = {
 'gut.ngl' : ('gut', 'Full', ''),
 'gut0-rtf.ngl': ('gut', 'ReadTrimFilter', ''),
 'gut1-s.hg19.ngl': ('gut', 'Screen', 'hg19'),
 'gut2-f.hg19.ngl': ('gut', 'Filter', 'hg19'),
 'gut3-motus.ngl': ('gut', 'motus', ''),
 'gut4-s.igc.ngl': ('gut', 'Screen', 'IGC'),
 'gut5-f.igc.ngl': ('gut', 'Filter', 'IGC'),
 'gut6-p.igc.ngl': ('gut', 'Profile', 'IGC'),
 'ocean.ngl' : ('tara', 'Full', ''),
 'ocean0-rtf.ngl' : ('tara', 'ReadTrimFilter', ''),
 'ocean1-s-om-rgc.ngl' : ('tara', 'Screen', 'OM-RGC.1'),
 'ocean2-f-om-rgc.ngl' : ('tara', 'Filter', 'OM-RGC.1'),
 'ocean3-p-functional-om-rgc.ngl' : ('tara', 'Profile', 'OM-RGC.1'),
 'ocean4-p-seqname-om-rgc.ngl' : ('tara', 'Profile', 'OM-RGC.1'),
 }

ngl['dataset'] = ngl.command.map(lambda c: command[c.split()[2]][0])
ngl['action'] = ngl.command.map(lambda c: command[c.split()[2]][1])
ngl['target'] = ngl.command.map(lambda c: command[c.split()[2]][2])

ngl['tool'] = 'ngless'
mocat['tool'] = 'mocat'

COLS = ['dataset', 'action', 'target', 'tool', 'wallclock']

data = pd.concat((ngl[COLS], mocat[COLS]))
data.fillna('-', inplace=True)


g = sns.factorplot(x="action", y="wallclock", hue="tool", hue_order=['ngless', 'mocat'], kind="box", col='dataset', data=data, aspect=1.7)
g.fig.get_axes()[0].set_yscale('log')
g.fig.get_axes()[1].set_yscale('log')

g.fig.tight_layout()
g.savefig('ngless-mocat-compare.pdf')

