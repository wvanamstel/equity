import statsmodels.tsa.stattools as st


def dickey_fuller(time_series, window):
    # returns rolling p-value from augmented dickey fuller test
    adf = time_series.rolling(window).apply(lambda x: st.adfuller(x, 1)[1])
    return adf
