"""Examples for benfords law."""

import benfordslaw as bl

# %%
# Load example
df = bl.import_example(data='USA')

# %% Donald Trump
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values
out = bl.fit(X)
bl.plot(out, title='Donald Trump')

# %% RUS
df = bl.import_example('RUS')
candidates=['Putin Vladimir Vladimirovich', 'Baburin Sergei Nikolaevich', 'Titov Boris Yurievich', 'Yavlinskiy Gregory Alekseivich']

for candidate in candidates:
    out = bl.fit(df[candidate].values, method='ks')
    bl.plot(out, title=candidate)

# %% USA
df = bl.import_example('USA')
for candidate in df['candidate'].unique():
    Iloc = df['candidate']==candidate
    X = df['votes'].loc[Iloc].values
    out = bl.fit(X)
    bl.plot(out, title=candidate)
