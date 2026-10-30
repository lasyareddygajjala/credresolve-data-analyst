import pandas as pd
from src.pipeline import profile,golden_payments,monthly_metrics

def test_duplicate_profile():
    q=profile({"x":pd.DataFrame({"id":[1,1,2]})})
    assert q.iloc[0].exact_duplicate_rows==1

def test_payment_dedupe():
    p=pd.DataFrame({"payment_id":["p1","p2"],"account_id":["a","a"],"payment_reference":["r","r"],
      "event_at":["2026-01-01","2026-01-02"],"amount":[50,50],"payment_status":["SUCCESS","SUCCESS"]})
    g=golden_payments({"payments":p,"accounts":pd.DataFrame()})
    assert len(g)==1
    assert monthly_metrics(g).iloc[0].successful_payment_amount==50
