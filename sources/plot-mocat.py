# coding: utf-8
import pandas as pd
import seaborn as sns

d = pd.read_csv('../data/precomputed/mocat_benchmark.csv')

g = sns.factorplot(x="action", y="Elapsed time", hue="dataset", kind="bar", capsize=.05, data=d, aspect=1.7)
g.fig.get_axes()[0].set_yscale('log')
g.set_ylabels("Elapsed time - seconds")
g.savefig("mocat_benchmark_dataset.png")

g = sns.factorplot(x="action", y="Elapsed time", hue="target", kind="bar", capsize=.05, data=d, aspect=1.7)
g.fig.get_axes()[0].set_yscale('log')
g.set_ylabels("Elapsed time - seconds")
g.savefig("mocat_benchmark_database.png")
