"""Protect denominators, SQL reconciliation, and validation failure paths."""
import sqlite3
import unittest
import pandas as pd
from src.pipeline import load_raw, validate, transform, queries, fault_summary

class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.raw=load_raw();cls.df=transform(cls.raw)
    def test_source_contract(self):
        self.assertEqual(self.raw.shape,(1941,34));self.assertEqual(validate(self.raw)['missing_cells'],0)
    def test_multiple_labels_rejected(self):
        bad=self.raw.copy();bad.loc[0,['Pastry','Stains']]=1
        with self.assertRaises(ValueError):validate(bad)
    def test_missing_value_rejected(self):
        bad=self.raw.copy();bad.loc[0,'Pixels_Areas']=float('nan')
        with self.assertRaises(ValueError):validate(bad)
    def test_bad_area_rejected(self):
        bad=self.raw.copy();bad.loc[0,'Pixels_Areas']=0
        with self.assertRaises(ValueError):validate(bad)
    def test_unique_lineage_and_preserved_rows(self):
        self.assertTrue(self.df.record_id.is_unique);self.assertEqual(len(self.df),len(self.raw))
        self.assertEqual(self.df.pixels_areas.sum(),self.raw.Pixels_Areas.sum())
    def test_sql_matches_pandas(self):
        with sqlite3.connect(':memory:') as con:
            self.df.to_sql('faults',con,index=False)
            outputs={name:pd.read_sql_query(sql,con) for name,sql in queries()}
        expected=fault_summary(self.df)
        actual=outputs['fault_pareto']
        self.assertEqual(actual.records.tolist(),expected.records.tolist())
        self.assertEqual(actual.fault_type.tolist(),expected.fault_type.tolist())
        self.assertAlmostEqual(actual.cumulative_share_pct.iloc[-1],100)
        for _, g in outputs['steel_fault_mix'].groupby('steel_type'):
            self.assertAlmostEqual(g.within_steel_share_pct.sum(),100,delta=.05)
        self.assertEqual(outputs['area_priority'].total_pixels.sum(),self.df.pixels_areas.sum())
    def test_filtered_denominator(self):
        sample=self.df[self.df.steel_type.eq('A300')];s=fault_summary(sample)
        self.assertEqual(s.records.sum(),len(sample));self.assertAlmostEqual(s.record_share_pct.sum(),100)

if __name__=='__main__':unittest.main()
