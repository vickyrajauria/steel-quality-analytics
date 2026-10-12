"""Exercise rendering, filter recalculation, and an empty selection."""
from pathlib import Path
import unittest
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parents[1]

class DashboardTests(unittest.TestCase):
    def test_full_filtered_and_empty_views(self):
        app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value,'1,941')
        app.sidebar.multiselect[0].set_value(['A300']).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value,'777')
        self.assertEqual(app.metric[1].value,'Bumps')
        app.sidebar.multiselect[1].set_value(['<=50']).run()
        self.assertFalse(app.exception)
        from src.pipeline import load_raw,transform
        df=transform(load_raw())
        n=len(df[(df.steel_type=='A300')&(df.thickness_band=='<=50')])
        self.assertEqual(app.metric[0].value,f'{n:,}')
        app.sidebar.multiselect[0].set_value([]).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('No observations' in w.value for w in app.warning))

if __name__=='__main__':unittest.main()
