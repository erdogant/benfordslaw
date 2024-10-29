"""Examples for benfords law."""

# import benfordslaw
# print(benfordslaw.__version__)

# %% Issue #13
# https://github.com/erdogant/benfordslaw/issues/13
from benfordslaw import benfordslaw
import pandas as pd
# import datzets as dz
# df = dz.get(data='elections')

bl = benfordslaw()
df = bl.import_example(data='elections_usa')
df = bl.import_example(data='elections_rus')


# %% Issue #10
import pandas as pd
from benfordslaw import benfordslaw

bl = benfordslaw(pos=-2)
# USA example
df = bl.import_example(data='elections_usa')
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values

results = bl.fit(X)
# Plot
bl.plot(title='Donald Trump', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)

# %% Issue #9
import pandas as pd
from benfordslaw import benfordslaw

# Initialize
bl = benfordslaw(pos=2)

# Load elections example
df = bl.import_example(data='elections_usa')

# Extract election information.
X = df['votes'].loc[df['candidate']=='Donald Trump'].values

X = pd.DataFrame(X)

# Make fit
results = bl.fit(X)


# %% Issue #8
import pandas as pd
from benfordslaw import benfordslaw

bl = benfordslaw(alpha=0.05)

data = pd.DataFrame({'value': [1,2,3,4,5]})
bl.fit(data['value'].astype(int)) # this works fine 
bl.fit(data['value'].astype(pd.Int64Dtype())) #this throws an error

# %%
import numpy as np
from benfordslaw import benfordslaw

# Create uniform random data
X = np.random.randint(0, high=100, size=1000)
bl = benfordslaw(alpha=0.05, method='chi2')
# Fit
results = bl.fit(X)
# Plot
bl.plot(title='Random data')

# %% Analyze Second digit
from benfordslaw import benfordslaw

bl = benfordslaw(pos=2)
# USA example
df = bl.import_example(data='elections_usa')
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values
results = bl.fit(X)
# Plot
bl.plot(title='Donald Trump', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)

# %%
import numpy as np
from benfordslaw import benfordslaw
bl = benfordslaw(alpha=0.05, method='chi2')
x = np.linspace(0,1000,1001)
x = np.append(x,[1,1,1,1,1,1,])
isben2 = bl.fit(x)

print(f"isben2 {isben2}")
print(f"P_significant: {isben2['P_significant']}")
if not isben2['P_significant']:
    print("sorry, nope.")

# %% USA example
from benfordslaw import benfordslaw

bl = benfordslaw(pos=1)

# USA example
df = bl.import_example(data='elections_usa')

# Get data for candidate
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values

# Fit
results = bl.fit(X)
# Plot
bl.plot(title='Donald Trump', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)


# %% Analyze last digit

bl = benfordslaw(pos=-1)
# USA example
df = bl.import_example(data='elections_usa')
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values

results = bl.fit(X)
# Plot
bl.plot(title='Donald Trump', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)

# %% second last digit

bl = benfordslaw(pos=-2)
# USA example
df = bl.import_example(data='elections_usa')
Iloc = df['candidate']=='Donald Trump'
X = df['votes'].loc[Iloc].values

results = bl.fit(X)
# Plot
bl.plot(title='Donald Trump', barcolor=[0.5, 0.5, 0.5], fontsize=12, barwidth=0.4)

# %% RUS
df = bl.import_example('RUS')
candidates=['Putin Vladimir Vladimirovich', 'Baburin Sergei Nikolaevich', 'Titov Boris Yurievich', 'Yavlinskiy Gregory Alekseivich']

for candidate in candidates:
    bl = benfordslaw(method='ks')
    bl.fit(df[candidate].values)
    bl.plot(title=candidate)

# %% USA
df = bl.import_example('elections_usa')
for candidate in df['candidate'].unique():
    Iloc = df['candidate']==candidate
    X = df['votes'].loc[Iloc].values
    bl.fit(X)
    bl.plot(title=candidate)

# %%