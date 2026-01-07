import pandas as pd
import yfinance as yf

def get_financial_data(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    bal_sheet = ticker.balance_sheet
    inc_stat = ticker.financials
    cfs = ticker.cash_flow
    return bal_sheet, inc_stat, cfs



# ----Profitability Score----

def profitability_score(bal_sheet, inc_stat, cfs):
    score1 = 0

    net_income = inc_stat.loc['Net Income'].iloc[0]
    net_income_py = inc_stat.loc['Net Income'].iloc[1]
    cy_assets = bal_sheet.loc['Total Assets'].iloc[0]
    py_assets = bal_sheet.loc['Total Assets'].iloc[1]
    py2_assets = bal_sheet.loc['Total Assets'].iloc[2]
    avg_assets = (cy_assets + py_assets)/ 2
    avg_assets_py = (py_assets + py2_assets)/ 2
    return_on_assets = net_income/avg_assets
    return_on_assets_py = net_income_py/avg_assets_py

# check 1 -- positive return on assets
    
    if return_on_assets > 0:
        score1 += 1

# check 2 -- positive operating cashflow
    op_cfs = cfs.loc['Operating Cash Flow'].iloc[0]
    if op_cfs > 0:
        score1 += 1
   
# check 3 -- change in return on assets
    
    if return_on_assets > return_on_assets_py:
        score1 += 1
    
# check 4 -- operating cashflow vs return on assets
    if (op_cfs/avg_assets) > return_on_assets:
        score1 += 1

    return score1
    
# ----Leverage, Liquidity and Funds Score----

def Leverage_Score(bal_sheet, inc_stat, cfs):
    score2 = 0

# check 1 -- change in leverage
    long_t_debt = bal_sheet.loc["Long Term Debt"].iloc[0]
    long_t_debt_py = bal_sheet.loc["Long Term Debt"].iloc[1]
    if long_t_debt < long_t_debt_py:
        score2 += 1

# check 2 -- change in current ratio
    ca = bal_sheet.loc["Current Assets"].iloc[0]
    ca_py = bal_sheet.loc["Current Assets"].iloc[1]
    cl = bal_sheet.loc["Current Liabilities"].iloc[0]
    cl_py = bal_sheet.loc["Current Liabilities"].iloc[1]
    curr_rat = ca/cl
    curr_rat_py = ca_py/cl_py
    if curr_rat > curr_rat_py:
        score2 += 1

# check 3 -- change in no. of shares
    no_shares = bal_sheet.loc["Ordinary Shares Number"].iloc[0]
    no_shares_py = bal_sheet.loc["Ordinary Shares Number"].iloc[1]
    if no_shares <= no_shares_py:
        score2 += 1

    return score2

# ----Operating Efficiency Score----

def operating_efficiency_score(bal_sheet, inc_stat, cfs):
    score3 = 0

# check 1 -- change in gross margin

    gp = inc_stat.loc["Gross Profit"].iloc[0]
    gp_py = inc_stat.loc["Gross Profit"].iloc[1]
    rev = inc_stat.loc["Total Revenue"].iloc[0]
    rev_py = inc_stat.loc["Total Revenue"].iloc[1]
    gp_margin = gp/rev
    gp_margin_py = gp_py/rev_py
    if gp_margin > gp_margin_py:
        score3 += 1

# check 2 -- change in asset turnover ratio

    cy_assets = bal_sheet.loc['Total Assets'].iloc[0]
    py_assets = bal_sheet.loc['Total Assets'].iloc[1]
    py2_assets = bal_sheet.loc['Total Assets'].iloc[2]
    avg_assets = (cy_assets + py_assets)/ 2
    avg_assets_py = (py_assets + py2_assets)/ 2
    asset_turnover = rev / avg_assets
    asset_turnover_py = rev_py / avg_assets_py
    if asset_turnover > asset_turnover_py:
        score3 += 1
    
    return score3

tickers = ["AAPL", "MSFT", "MMM", "AOS", "ABT", "ADBE", "AMD"]
ranking = []

for tkr in tickers:
    bal_sheet, inc_stat, cfs = get_financial_data(tkr)
    pft_score = profitability_score(bal_sheet, inc_stat, cfs)
    lev_score = Leverage_Score(bal_sheet, inc_stat, cfs)
    op_score = operating_efficiency_score(bal_sheet, inc_stat, cfs)
    f_score = pft_score + lev_score + op_score
    ranking.append({
        "Ticker" : tkr,
        "Profitability Score" : pft_score,
        "Leverage Score" : lev_score,
        "Operating Efficiency Score" : op_score,
        "F score" : f_score,
    })

df_rank = pd.DataFrame(ranking)
df_rank = df_rank.sort_values(by = "F score", ascending = False)
df_rank = df_rank.reset_index(drop = True)
df_rank["Ranking"] = df_rank.index + 1
print(df_rank)