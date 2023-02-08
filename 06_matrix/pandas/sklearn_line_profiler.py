import numpy as np
import pandas as pd
from line_profiler import LineProfiler
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import _base as base
from utility import ols_sklearn

# We learn that
# LinearRegression.fit is expensive because
# of calls to _validate_data, _preprocess_data and linalg.lstsq
# _preprocess_data
# has 3 expensive lines - check_array, np.asarray, np.average

df = pd.read_pickle("generated_ols_data.pickle")
print(f"Loaded {df.shape} rows")

est = LinearRegression()
row = df.iloc[0]
X = np.arange(row.shape[0]).reshape(-1, 1).astype(np.float_)

lp = LineProfiler(est.fit)
print("Run on a single row")
lp.run("est.fit(X, row.values)")
lp.print_stats()

print("Run on 5000 rows")
lp.run("df[:5000].apply(ols_sklearn, axis=1)")
lp.print_stats()

lp = LineProfiler(base._preprocess_data)
lp.run("base._preprocess_data(X, row, fit_intercept=True)")
lp.print_stats()
