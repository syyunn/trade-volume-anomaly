import pandas as pd
import datetime
import matplotlib.pyplot as plt

df = pd.read_csv('./test.csv', header=None)
df = df.sort_values(0)

keys = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
vals = [i for i in range(1, 13)]

months = dict(zip(keys, vals))
years = [i for i in range(2010, 2021)]
years = [i for i in range(2010, 2020)]


periods = []

for year in years:
    for val in vals:
        periods.append(datetime.date(year=year, month=val, day=15))

gdp = pd.read_csv(
    "./API_NY.GDP.MKTP.CD_DS2_en_csv_v2_1345540.csv"
)

year_codes = [str(year) for year in years]
idx = gdp.index[gdp["Country Code"] == 'PER'].tolist()
gdps = dict(zip(year_codes, gdp.loc[idx[0]][year_codes].to_list()))


tvs = []
for year in years:
    for key in keys:
        rdxs = df.index[df[0] == int(str(year) + key)].tolist()
        if len(rdxs) > 0:
            tvs.append((df.iloc[rdxs[0], 4] * 100) / gdps[str(year)])
        else:
            try:
                tvs.append(tvs[-1])
            except IndexError:
                tvs.append(0)

linestyle = 'solid'
fig = plt.gcf()
fig.set_size_inches(100, 10.5)
plt.plot(
    periods,
    tvs,
    label=f"",
    linestyle=linestyle
)
plt.show()
if __name__ == "__main__":
    pass
