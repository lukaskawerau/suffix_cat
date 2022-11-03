import pandas as pd

output_file = 'data/manual/parsed_suffixes_manual.csv'
input_lists = [
    'data/manual/legacy_public_suffixes.csv',
    'data/manual/manual_additions_not_public_suffix.csv',
    'data/processed/parsed_suffixes.csv'
]

columns = ['tld', 'suffix', 'category', 'reference']
df = pd.DataFrame()

for l in input_lists:
    d = pd.read_csv(l, names=columns, keep_default_na=False)
    df = df.append(d)

def uniq_join_strip(l):
    l = set(l)
    return ' '.join(l).strip()

# deduplicate suffixes and merge category and reference
df = df.groupby(['tld', 'suffix'], as_index = False).agg({'category': uniq_join_strip, 'reference': uniq_join_strip})
df.sort_values(['tld', 'suffix'], inplace=True)

df.to_csv(output_file, index=False)
