import pandas as pd
import seaborn as sns

ngl = pd.read_table('../data/precomputed/ngless_benchmark.tsv')
mocat = pd.read_csv('../data/precomputed/mocat_benchmark.csv', index_col=0)
hts = pd.read_table('../data/precomputed/htseq-count_benchmark.tsv')
hts.rename(columns={
    hts.columns[0]: 'dataset',
    hts.columns[1]: 'action',
    hts.columns[2]: 'sample-id',
    hts.columns[3]: 'rep-nr',
    }, inplace=True)

hts = hts.groupby(['dataset', 'action', 'rep-nr']).sum().reset_index()
hts['action'] = hts.action.map({'map':'Screen', 'htseq-count':'Profile'})
hts['target'] = hts.dataset.map({'gut': 'IGC', 'tara' : 'OM-RGC'})
htsfull = hts.groupby(['dataset', 'rep-nr']).sum().reset_index()
htsfull['action'] = 'Full'
htsfull['target'] = '-'
hts = pd.concat((hts, htsfull))
hts['tool'] = 'bwa/htseq-count'

mocat.rename(columns={
    'Elapsed time': 'wallclock',
    'Maximum resident set size (kbytes)': 'max_rss',
    }, inplace=True)

mocat = mocat[~ (mocat.target == 'RefMG.v1.padded')]
mocat = mocat[~ (mocat.target == 'mOTU.v1.padded')]
mocat = mocat[~ (mocat.target == 'hg19')]


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

ngl = ngl.groupby([ngl.columns[0], ngl.columns[1]]).sum()
ngl['tool'] = 'ngless'
mocat['tool'] = 'mocat'
ngl['dataset'] = ngl.index.get_level_values(0).map(lambda c: command[c][0])
ngl['action'] = ngl.index.get_level_values(0).map(lambda c: command[c][1])
ngl['target'] = ngl.index.get_level_values(0).map(lambda c: command[c][2])

ngl = ngl.drop([
        'ocean4-p-seqname-om-rgc.ngl',
        'gut3-motus.ngl',
        'gut1-s.hg19.ngl',
        'gut2-f.hg19.ngl',
        ])

COLS = ['dataset', 'action', 'target', 'tool', 'wallclock']

mocat = mocat[COLS]
tara_full = mocat[mocat.dataset == 'tara'].reset_index()
tara_full = pd.DataFrame([('tara', 'Full', '-', 'mocat', wc) for wc in tara_full.groupby(lambda i : i // 4).sum()['wallclock'].values], columns=COLS)
gut_full = mocat[mocat.dataset == 'gut'].reset_index()
gut_full = pd.DataFrame([('gut', 'Full', '-', 'mocat', wc) for wc in gut_full.groupby(lambda i : i // 5).sum()['wallclock'].values], columns=COLS)

data = pd.concat((ngl[COLS], mocat[COLS], hts[COLS], gut_full, tara_full))

data.reset_index(inplace=True)
data.fillna('-', inplace=True)

g = sns.factorplot(x="action", y="wallclock", hue="tool", hue_order=['ngless', 'mocat', 'bwa/htseq-count'], kind="swarm", col='dataset', sharey=True, data=data, aspect=1.7)
g.fig.get_axes()[0].set_yscale('log')
g.fig.get_axes()[1].set_yscale('log')

g.fig.tight_layout()
g.savefig('ngless-mocat-htseq-count-compare.png', dpi=150)
g.savefig('ngless-mocat-htseq-count-compare.svg')
g.savefig('ngless-mocat-htseq-count-compare.pdf')

