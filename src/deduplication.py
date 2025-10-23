import pandas as pd
import numpy as np
import mermaid as md
from mermaid.graph import Graph

def deduplicate(df, cols):
    input_file_name = 'data/' + input('Enter file name: ') + '.csv'
    df = pd.read_csv(input_file_name) # A (records)
    cols_input = input('Enter the columns for which to deduplicate based on: ')
    cols = [c.strip() for c in cols_input.split(',')]
    output_file_name = 'data/' + '_'.join(cols) + '_deduplicated.csv'
    prisma_file_name = output_file_name.replace('.csv', '.mmd')

    nulls_mask = df[cols].isnull().any(axis=1)
    df_nulls = df[nulls_mask] # B
    df_non_nulls = df[~nulls_mask] # C
    
    duplicates_mask = df_non_nulls.duplicated(subset = cols, keep = False)
    df_non_duplicates = df_non_nulls[~duplicates_mask] # D
    df_duplicates = df_non_nulls[duplicates_mask] # E
    df_kept = df_duplicates.drop_duplicates(subset = cols, keep = 'first')
    df_removed = df_duplicates[~df_duplicates.index.isin(df_kept.index)]
    df_unique = df_non_nulls.drop_duplicates(subset = cols, keep = 'first') # df of unique
    df_deduplicated = pd.concat([df_unique, df_nulls], ignore_index=True) # df of unique + df of nulls

    results = {
        "records": len(df),
        "nulls": len(df_nulls),
        "non_nulls": len(df_non_nulls),
        "non_duplicates": len(df_non_duplicates),
        "duplicates": len(df_duplicates),
        "removed": len(df_removed),
        "kept": len(df_kept),
        "unique": len(df_unique),
        "deduplicated": len(df_deduplicated)
    }
    
    df_deduplicated.to_csv(output_file_name, index = False)
    df_removed.to_csv(output_file_name.replace('.csv', '_removed.csv'), index = False)


    return results, df_deduplicated, df_kept, df_removed, output_file_name, prisma_file_name

if __name__ == "__main__":
    results, df_deduplicated, df_kept, df_removed, output_file_name, prisma_file_name = deduplicate(df=None, cols=None)
    
    graph_text = f"""---
config:
  theme: neutral
  curve: stepBefore
---
graph TD;
A["**records** (*n* = {results['records']})"];
B["null (*n* = {results['nulls']})"];
C["non-null (*n* = {results['non_nulls']})"];
D["non-duplicates (*n* = {results['non_duplicates']})"];
E["duplicates (*n* = {results['duplicates']})"];
F["duplicates kept (*n* = {results['kept']})"];
G["duplicates removed (*n* = {results['removed']})"];
H["unique (*n* = {results['unique']})"];
I["deduplicated (*n* = {results['deduplicated']})"];

A --> B & C;
C --> D & E;
E --> F & G;
D & F --> H;
B & H --> I"""
    

    with open(prisma_file_name, "w") as f:
        f.write(graph_text)
