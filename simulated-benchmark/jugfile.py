import pandas as pd
from scipy import stats, spatial
from jug import Task, TaskGenerator, barrier

BASEDIR_GUT = '../data/simulated_gut/'
BASEDIR_MARINE = '../data/simulated_tara/'

def run_ngless(sc, idir, odir):
    from jug.utils import jug_execute
    from os import makedirs
    makedirs(odir, exist_ok=True)
    jug_execute.f(['ngless', '--trace', '-j', 'auto', sc, idir, odir])

@TaskGenerator
def run_gut(s):
    run_ngless('human-gut-profiler.ngl', BASEDIR_GUT + s, 'RESULTS/' + s)
@TaskGenerator
def run_marine(s):
    run_ngless('marine-profiler.ngl', BASEDIR_MARINE + s, 'RESULTS/' + s)

for s in open(BASEDIR_GUT + 'simulated_gut'):
    run_gut(s.strip())

for s in open(BASEDIR_MARINE + 'simulated_tara'):
    run_marine(s.strip())



barrier()


def load_data(sample, catalog):
    underlying = pd.read_table('data/all_samples.cog-distribution', index_col=0)
    truth = underlying[sample]
    if catalog == 'gut':
        fname = f'./RESULTS/{sample}/eggNOG.traditional.counts.txt'
        ngless = pd.read_table(fname, index_col=0, comment='#', squeeze=True)
        ngless = ngless[ngless.index.map(lambda c: c.endswith('@NOG'))]
        ngless.index = ngless.index.map(lambda c: c.replace('@NOG', ''))
    elif catalog == 'tara':
        fname = f'./RESULTS/{sample}/om-rgc.functional.profiles.txt'
        ngless = pd.read_table(fname, index_col=0, comment='#', squeeze=True)
        ngless = ngless[ngless.index.map(lambda ix: ix.startswith('eggNOG_OG:'))]
        ngless.index = ngless.index.map(lambda c: c[len('eggNOG_OG:'):]).map(lambda c : (c[len('ENOG41'):] if c.startswith('ENOG41') else c))
    else:
        raise ValueError(f"Catalog = '{catalog}'")
    mocat_catalog = ('IGC.1-2' if catalog =='gut' else 'OM-RGC.1-9')
    headers = pd.read_table(f'./MOCAT/{sample}.functional.profile.screened.reads.processed.on.{mocat_catalog}.solexaqa.allbest.l45.p95.eggNOG_OG.rownames', squeeze=True)
    mocat = pd.read_table(f'./MOCAT/{sample}.functional.profile.screened.reads.processed.on.{mocat_catalog}.solexaqa.allbest.l45.p95.base.mm.dist.among.unique.scaled.eggNOG_OG', squeeze=True)
    mocat = pd.DataFrame({'h': headers, 'mocat': mocat}).set_index('h').mocat
    mocat.index = mocat.index.map(lambda ix: (ix[len('ENOG41'):] if ix.startswith('ENOG41') else ix))
    mocat.drop(['unassigned', 'mapped',], inplace=True)
    htseq = pd.read_table(f'htseq-outputs/{sample}.txt', index_col=0, header=(None if catalog =='gut' else 0), squeeze=True)
    htseq.drop([c for c in htseq.index if c.startswith('__')], inplace=True)
    htindex = set(htseq.index)
    for c in htseq.index:
        if ',' in c:
            for b in c.split(','):
                if b in htindex:
                    htseq[b] += htseq[c]
                else:
                    htseq[b] = htseq[c]
        if '|' in c:
            for b in c.split('|'):
                if b in htindex:
                    htseq[b] += htseq[c]
                else:
                    htseq[b] = htseq[c]
    htseq.index = htseq.index.map(lambda c : (c[len('ENOG41'):] if c.startswith('ENOG41') else c))
    htseq.drop([c for c in htseq.index if ',' in c], inplace=True)
    htseq.drop([c for c in htseq.index if '|' in c], inplace=True)
    return pd.DataFrame({'truth': truth, 'ngless': ngless, 'mocat': mocat, 'htseq': htseq}).fillna(0)


def compare(a, b):
    data = pd.DataFrame({'o' : a, 't': b})
    sp = stats.spearmanr(data.o, data.t)
    p = stats.pearsonr(data.o, data.t)
    j = spatial.distance.jaccard(data.o > 0, data.t > 0)
    return (sp[0], p[0], 1.0 - j)

@TaskGenerator
def build_table(catalog):
    sample_list = {
            'gut' : BASEDIR_GUT + 'simulated_gut',
            'tara' : BASEDIR_MARINE + 'simulated_tara',
            }[catalog]

    table = []


    for s in open(sample_list):
        s = s.strip()
        data = load_data(s, catalog)
        row = [s]

        row.extend(compare(data.truth, data.ngless))
        row.extend(compare(data.truth, data.mocat))
        row.extend(compare(data.truth, data.htseq))
        table.append(row)
    return pd.DataFrame(table, columns=['index',
        'ngless_spearman', 'ngless_pearson', 'ngless_jaccard',
        'mocat_spearman', 'mocat_pearson', 'mocat_jaccard',
        'htseq_spearman', 'htseq_pearson', 'htseq_jaccard',
        ]).set_index('index')


@TaskGenerator
def summarize(table_gut, table_tara):
    final = {}
    final['tara', 'spearman (mean)'] = table_tara[[c for c in table_tara.columns if 'spear' in c]].mean()
    final['tara', 'spearman (std)'] = table_tara[[c for c in table_tara.columns if 'spear' in c]].std()
    final['gut', 'spearman (std)'] = table_gut[[c for c in table_tara.columns if 'spear' in c]].std()
    final['gut', 'spearman (mean)'] = table_gut[[c for c in table_tara.columns if 'spear' in c]].mean()


    final = pd.DataFrame(final).rename(index=lambda n: n.split('_')[0])*100
    final.to_excel('final.xlsx')

    full = pd.concat([table_tara, table_gut])
    full = full.T[full.columns.map(lambda c: 'spear' in c)].T
    full['environment'] = full.index.map(lambda c: ('marine' if  c in table_tara.index else 'human gut'))
    full.to_excel('full.xlsx')


@Task
def save_precomputed():
    full_data = {}
    for catalog in ['gut', 'tara']:

        sample_list = {
                'gut' : BASEDIR_GUT + 'simulated_gut',
                'tara' : BASEDIR_MARINE + 'simulated_tara',
                }[catalog]

        for s in open(sample_list):
            s = s.strip()
            full_data[s] = load_data(s, catalog)
    f = pd.concat({k:v.T for k,v in full_data.items()}, keys=full_data.keys())
    f = f.fillna(0)
    f = f.T[f.any()]
    f.to_csv('simulation-abundances.tsv', sep='\t')




table_gut = build_table('gut')
table_tara = build_table('tara')

summarize(table_gut, table_tara)
