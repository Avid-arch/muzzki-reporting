# tests/test_clean.py
import pandas as pd
from src.clean import normalize

def test_normalize_basic():
    df = pd.DataFrame({
        'date':['2025-07-01','07/02/2025','bad'],
        'post_id':['a','b','c'],
        'impressions':['100','200','300'],
        'engagement':['10','20','']
    })
    out = normalize(df)
    # should drop the bad date row
    assert out['date'].isnull().sum() == 0
    # impressions should exist and be integer
    assert 'impressions' in out.columns
    assert out['impressions'].dtype == int
    # duplicates removal shouldn't throw here
    assert len(out) == 2