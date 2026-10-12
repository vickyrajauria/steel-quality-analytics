"""Validate source records, build a tidy table, run SQL, and export evidence."""
from pathlib import Path
import hashlib
import json
import sqlite3
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
LABELS = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
DISPLAY = {'K_Scatch': 'K Scratch', 'Z_Scratch': 'Z Scratch', 'Other_Faults': 'Other Faults'}

def load_raw():
    columns = (ROOT / 'data/raw/Faults27x7_var').read_text().split()
    return pd.read_csv(ROOT / 'data/raw/Faults.NNA', sep=r'\s+', names=columns)

def validate(df):
    """Fail loudly rather than silently repairing invalid analytical records."""
    errors = []
    if df.empty: errors.append('Dataset is empty')
    if df.isna().any().any(): errors.append('Missing values')
    if not all(pd.api.types.is_numeric_dtype(df[c]) for c in df): errors.append('Non-numeric source values')
    elif not np.isfinite(df.to_numpy()).all(): errors.append('Non-finite source values')
    if not df[LABELS].isin([0, 1]).all().all() or not df[LABELS].sum(axis=1).eq(1).all():
        errors.append('Each record must have exactly one binary fault label')
    steel = df[['TypeOfSteel_A300', 'TypeOfSteel_A400']]
    if not steel.isin([0, 1]).all().all() or not steel.sum(axis=1).eq(1).all():
        errors.append('Each record must have exactly one binary steel type')
    if not df.Pixels_Areas.gt(0).all(): errors.append('Non-positive pixel area')
    if not df.Steel_Plate_Thickness.gt(0).all(): errors.append('Non-positive thickness')
    if not ((df.X_Maximum >= df.X_Minimum) & (df.Y_Maximum >= df.Y_Minimum)).all():
        errors.append('Reversed coordinate bounds')
    if errors: raise ValueError('; '.join(errors))
    return {'rows': len(df), 'columns': len(df.columns), 'missing_cells': int(df.isna().sum().sum()),
            'exact_duplicate_rows': int(df.duplicated().sum()), 'validation': 'passed',
            'duplicate_policy': 'Flag, do not drop: identical measurements may be distinct observations.'}

def transform(df):
    validate(df)
    out = df.copy()
    out.insert(0, 'record_id', np.arange(1, len(df)+1))
    out['fault_type'] = df[LABELS].idxmax(axis=1).map(lambda x: DISPLAY.get(x, x))
    out['steel_type'] = np.where(df.TypeOfSteel_A300.eq(1), 'A300', 'A400')
    out['thickness_band'] = pd.cut(df.Steel_Plate_Thickness, [0, 50, 100, float('inf')],
                                 labels=['<=50', '51-100', '>100']).astype(str)
    # Thickness units are not documented; preserve source units without conversion.
    out['log10_pixel_area'] = np.log10(out.Pixels_Areas)
    out.columns = [c.lower() for c in out.columns]
    return out.drop(columns=[x.lower() for x in LABELS] + ['typeofsteel_a300', 'typeofsteel_a400'])

def queries():
    text = (ROOT / 'sql/analysis.sql').read_text()
    for block in text.split('-- query: ')[1:]:
        name, sql = block.split('\n', 1)
        yield name.strip(), sql.strip()

def fault_summary(df):
    """Shares always use the supplied selection as denominator."""
    x = df.groupby('fault_type').agg(records=('record_id', 'size'),
        total_pixels=('pixels_areas', 'sum'), median_pixels=('pixels_areas', 'median')).reset_index()
    x = x.sort_values(['records', 'fault_type'], ascending=[False, True])
    x['record_share_pct'] = 100*x.records/x.records.sum()
    x['cumulative_share_pct'] = x.record_share_pct.cumsum()
    x['pixel_share_pct'] = 100*x.total_pixels/x.total_pixels.sum()
    return x

def make_figures(df, dest):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.spines.top': False,
        'axes.spines.right': False, 'axes.titleweight': 'bold', 'figure.facecolor': '#f7f9fc',
        'axes.facecolor': '#f7f9fc', 'text.color': '#172b4d', 'axes.labelcolor': '#172b4d'})
    s = fault_summary(df)
    fig, ax = plt.subplots(figsize=(11, 5.6), layout='constrained')
    bars = ax.bar(s.fault_type, s.records, color=['#0f766e']*3+['#94a3b8']*4, width=.65)
    ax.bar_label(bars, padding=4); ax.set_ylim(0, 780); ax.set_ylabel('Fault records')
    ax.set_title('Three categories account for most recorded faults', loc='left', pad=20)
    ax.tick_params(axis='x', rotation=15)
    right = ax.twinx();right.plot(s.fault_type, s.cumulative_share_pct, color='#d97706', marker='o')
    right.set_ylim(0, 110);right.set_ylabel('Cumulative share of fault records (%)')
    right.axhline(80, color='#d97706', linestyle=':', alpha=.5)
    fig.savefig(dest/'fault_pareto.png', dpi=170);plt.close(fig)
    comp = pd.crosstab(df.steel_type, df.fault_type, normalize='index')*100
    fig, ax = plt.subplots(figsize=(11, 5.6), layout='constrained')
    comp.plot.barh(stacked=True, ax=ax, color=['#0f766e','#d97706','#334155','#60a5fa','#a78bfa','#f472b6','#84cc16'])
    ax.set_xlabel('Share of recorded faults within steel type (%)');ax.set_ylabel('Steel type')
    ax.set_title('Steel types have different recorded fault mixes',loc='left',pad=20)
    ax.legend(bbox_to_anchor=(.5,-.17), loc='upper center', ncol=4, frameon=False)
    fig.savefig(dest/'steel_mix.png',dpi=170);plt.close(fig)
    fig, ax=plt.subplots(figsize=(11,5.6),layout='constrained')
    ax.barh(s.fault_type, s.pixel_share_pct, color='#0f766e');ax.invert_yaxis()
    ax.set_xlabel('Share of summed defect pixel areas (%)')
    ax.set_title('Pixel-area concentration differs from record frequency',loc='left',pad=20)
    ax.set_xlim(0,100)
    for i, v in enumerate(s.pixel_share_pct): ax.text(v+1,i,f'{v:.1f}%',va='center')
    fig.savefig(dest/'pixel_area_share.png',dpi=170);plt.close(fig)

def main():
    processed=ROOT/'data/processed'; reports=ROOT/'reports';figures=reports/'figures'
    for d in [processed,reports,figures]:d.mkdir(parents=True,exist_ok=True)
    raw=load_raw();audit=validate(raw);df=transform(raw)
    audit['raw_sha256']=hashlib.sha256((ROOT/'data/raw/Faults.NNA').read_bytes()).hexdigest()
    (reports/'quality_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    df.to_csv(processed/'faults_clean.csv',index=False)
    with sqlite3.connect(processed/'quality.db') as con:
        df.to_sql('faults',con,if_exists='replace',index=False)
        con.execute('CREATE UNIQUE INDEX record_id_idx ON faults(record_id)')
        for name, sql in queries():pd.read_sql_query(sql,con).to_csv(reports/f'{name}.csv',index=False)
    make_figures(df,figures)
    s=fault_summary(df);top=s.head(3);k=s[s.fault_type.eq('K Scratch')].iloc[0]
    result={'records':len(df),'top_three_record_share_pct':float(top.record_share_pct.sum()),
            'top_three_categories':top.fault_type.tolist(),'k_scratch_pixel_share_pct':float(k.pixel_share_pct),
            'k_scratch_record_share_pct':float(k.record_share_pct)}
    (reports/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));print('Pipeline complete. Outputs: data/processed and reports.')

if __name__ == '__main__': main()
