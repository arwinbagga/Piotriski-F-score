# 📊 Piotroski F-Score Stock Screener

## 📘 Overview
This project implements the **Piotroski F-Score** model in Python to evaluate and rank publicly listed companies based on their financial strength.  
The Piotroski F-Score is a 9-point scoring system that assesses a firm’s **profitability, leverage, liquidity, and operating efficiency** using accounting data.

The goal of this project is to build a **fundamental stock screener** that can systematically identify financially strong companies.

---

## ⚙️ Methodology
For each company, the script:
- Extracts **Balance Sheet**, **Income Statement**, and **Cash Flow Statement** data using Yahoo Finance (`yfinance`)
- Computes all **9 Piotroski signals**, grouped into:
  - **Profitability**
  - **Leverage, Liquidity, and Funding**
  - **Operating Efficiency**
- Aggregates individual scores into a **total F-Score**
- Ranks companies based on their F-Score using `pandas`

Each company is processed independently to avoid data leakage or reuse of incorrect financial information.

---

## 🧮 Piotroski F-Score Breakdown

### Profitability (4 checks)
- Positive Return on Assets (ROA)
- Positive Operating Cash Flow
- Improvement in ROA year-over-year
- Operating Cash Flow greater than Net Income

### Leverage, Liquidity & Funding (3 checks)
- Reduction in long-term debt
- Improvement in current ratio
- No equity dilution (no increase in shares outstanding)

### Operating Efficiency (2 checks)
- Improvement in gross margin
- Improvement in asset turnover ratio

---

## 📊 Output
The script produces a ranked DataFrame with the following columns:
- Ticker
- Profitability Score
- Leverage Score
- Operating Efficiency Score
- Total F-Score
- Rank (higher rank = stronger fundamentals)

Example structure:

| Ticker | Profitability | Leverage | Efficiency | F Score | Rank |
|------|--------------|----------|------------|---------|------|
| AAPL | 3 | 2 | 2 | 7 | 1 |

---

## 🧠 Key Learnings
- Translating financial theory into executable Python logic
- Working with financial statements programmatically
- Importance of correct loop placement when processing multiple companies
- Avoiding silent data reuse bugs by computing and storing results per company
- Writing clear, modular, and interview-friendly analytical code

---

## 🧰 Technologies Used
- Python
- pandas
- yfinance
