import pandas as pd

# one = [1, 2, 3, 4, 5]
# due = [['unu', 'unu', 'unu', 'unu', 'unu'],
#        ['doi', 'doi', 'doi', 'doi', 'doi'],
#        ['trei', 'trei', 'trei', 'trei', 'trei'],
#        ['patru', 'patru', 'patru', 'patru', 'patru'],
#        ['cinci', 'cinci', 'cinci', 'cinci', 'cinci']]
# df = pd.DataFrame(due)
# df = df.transpose()
# df.loc[df.shape[0]] = one
# print(df)
# rs = df.to_json('rez.json')
# df = df.to_csv('rez.csv')



# df = pd.read_csv('datadog.csv')
# print(df)
# for data in df.itertuples():
#        print(data.Breed)

df = pd.read_excel('LISTA-AGENTIILOR-DE-TURISM-LICENTIATE-actualizare-13.10.2022.xlsx')
print(df)
