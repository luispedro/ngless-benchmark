import re
from jug import TaskGenerator
import numpy as np
from os import makedirs

@TaskGenerator
def run_hg19(sample):
    makedirs('mapped', exist_ok=True)
    from ngless import NGLess
    ofile = 'mapped/' + sample + '.sam'
    sc = NGLess.NGLess('0.8')
    sc.import_('mocat', '0.0')
    e = sc.env
    e.data = sc.load_mocat_sample_('data/' + sample)
    @sc.preprocess_(e.data, using='r')
    def proc(bk):
        bk.r = sc.substrim_(bk.r, min_quality=25)
        sc.if_(sc.len_(bk.r) < 45, sc.discard_)
    e.mapped = sc.map_(e.data, reference='hg19')
    e.mapped = sc.select_(e.mapped, keep_if=['{mapped}'])
    sc.write_(e.mapped, ofile=ofile)
    sc.run(auto_install=False)
    return ofile

def pcigar(cigar):
    r = []
    while cigar:
        m = re.search('[IDMHS]',cigar)
        code = m.group()
        n = cigar[:m.start()]
        cigar = cigar[m.end():]
        r.append((int(n), code))
    return r

@TaskGenerator
def parse_sam(fname):
    lens = []
    for line in open(fname):
        if line[0] == '@':
            continue
        tokens = line.split('\t')
        if tokens[5] != '*':
            parsed = pcigar(tokens[5])
            lens.append(sum(c for c,code in parsed if code =='M'))
            
    lens = np.array(lens)
    lens.sort()
    return lens

@TaskGenerator
def threshold_curve(lens):
    lens = np.concatenate(lens)
    vs = [np.mean(lens  > i) for i in range(1, 102)]
    return 1- np.array(vs)

@TaskGenerator
def plot_result(H):
    import seaborn as sns
    from matplotlib import pyplot as plt
    from matplotlib import style
    style.use('seaborn-white')
             
    MIN_X = 20

             
    fig,ax = plt.subplots()
    H = H[MIN_X:]
             
    ax.plot(np.arange(MIN_X, len(H) + MIN_X), 100 - H*100)
    ax.set_xlabel('Threshold for detection (basepairs)')
    ax.set_ylabel('Spurious hits kept (%)')
    sns.despine(fig, trim=True, offset=4)
    fig.savefig('HumanFilteringThresholds.pdf')

samples = [line.strip() for line in open('data/simulations')]
samples.sort()

sams = [run_hg19(s) for s in samples]

lens = []
for s in sams:
    lens.append(parse_sam(s))
curve = threshold_curve(lens)
plot_result(curve)
