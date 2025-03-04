#  glossary/management/commands/populate_glossary.py
import csv
import os
from django.core.management.base import BaseCommand
from glossary.models import GlossaryTerm


class Command(BaseCommand):
    """
    Management command to populate the glossary with initial financial terms.

    Usage:
        python manage.py populate_glossary

    The command will add a set of common financial terms to the glossary database.
    Each term includes a definition and category.
    """
    help = 'Populates the glossary with initial financial terms'

    def handle(self, *args, **kwargs):
        # List of initial financial terms with their definitions and categories
        terms = [
            {
                'term': 'Alpha',
                'definition': 'A measure of the active return on an investment compared to a market index. It represents the excess return of an investment relative to the return of a benchmark index.\n\n'
                              'Alpha is often used in the context of active portfolio management to evaluate a manager\'s performance. A positive alpha indicates that the investment has outperformed its benchmark.'
                              '\n\n### Mathematical Representation\n\n'
                              'Alpha is represented by the Greek letter α in the following equation:\n\n'
                              '$$R_i = \\alpha + \\beta R_m + \\epsilon$$\n\n'
                              'Where:\n'
                              '- $R_i$ is the return of the investment\n'
                              '- $R_m$ is the return of the benchmark\n'
                              '- $\\beta$ is the beta of the investment\n'
                              '- $\\alpha$ is the excess return\n'
                              '- $\\epsilon$ is the error term',
                'category': 'Performance Metrics'
            },
            {
                'term': 'Beta',
                'definition': 'A measure of the volatility or systematic risk of a security or portfolio compared to the market as a whole. Beta measures the tendency of a security\'s returns to respond to market swings.\n\n'
                              'A beta of 1 indicates that the security\'s price moves with the market. A beta less than 1 means the security is less volatile than the market, while a beta greater than 1 indicates more volatility than the market.'
                              '\n\n### Mathematical Calculation\n\n'
                              'Beta is calculated as the covariance of the security\'s returns and the benchmark\'s returns, divided by the variance of the benchmark\'s returns:\n\n'
                              '$$\\beta = \\frac{Cov(r_i, r_m)}{Var(r_m)}$$\n\n'
                              'Where:\n'
                              '- $r_i$ represents the returns of the security\n'
                              '- $r_m$ represents the returns of the market',
                'category': 'Risk Measures'
            },
            {
                'term': 'Dividend Yield',
                'definition': 'A financial ratio that shows how much a company pays out in dividends each year relative to its stock price. Dividend yield is calculated as annual dividends per share divided by price per share.\n\n'
                              '### Formula\n\n'
                              '$$\\text{Dividend Yield} = \\frac{\\text{Annual Dividends per Share}}{\\text{Price per Share}} \\times 100\\%$$\n\n'
                              '### Example\n\n'
                              'If a company pays annual dividends of $2 per share and its current stock price is $50 per share, the dividend yield would be:\n\n'
                              '$$\\text{Dividend Yield} = \\frac{\\$2}{\\$50} \\times 100\\% = 4\\%$$\n\n'
                              'Investors focused on income often look for stocks with high dividend yields.',
                'category': 'Fundamental Analysis'
            },
            {
                'term': 'Efficient Market Hypothesis (EMH)',
                'definition': 'A theory in financial economics stating that asset prices reflect all available information. The EMH exists in three forms:\n\n'
                              '1. **Weak Form**: Current prices reflect all historical price information\n'
                              '2. **Semi-Strong Form**: Prices reflect all publicly available information\n'
                              '3. **Strong Form**: Prices reflect all information, both public and private\n\n'
                              'The EMH implies that it is impossible to consistently "beat the market" through stock selection or market timing, as markets are efficient and prices adjust rapidly to new information.'
                              '\n\n### Implications\n\n'
                              'If markets are efficient:\n'
                              '- Active investment strategies should not consistently outperform passive strategies\n'
                              '- Technical analysis should not be consistently profitable\n'
                              '- Even insider information may not provide an advantage (in the strong form)',
                'category': 'Market Theory'
            },
            {
                'term': 'EBITDA',
                'definition': 'Earnings Before Interest, Taxes, Depreciation, and Amortization. A measure of a company\'s overall financial performance and is used as an alternative to net income in some circumstances.\n\n'
                              '### Calculation\n\n'
                              'EBITDA can be calculated in two ways:\n\n'
                              '1. Starting with net income and adding back interest, taxes, depreciation, and amortization:\n\n'
                              '   $$\\text{EBITDA} = \\text{Net Income} + \\text{Interest} + \\text{Taxes} + \\text{Depreciation} + \\text{Amortization}$$\n\n'
                              '2. Starting with operating profit and adding back depreciation and amortization:\n\n'
                              '   $$\\text{EBITDA} = \\text{Operating Profit} + \\text{Depreciation} + \\text{Amortization}$$\n\n'
                              '### Python Example\n\n'
                              '```python\n'
                              'def calculate_ebitda(net_income, interest, taxes, depreciation, amortization):\n'
                              '    return net_income + interest + taxes + depreciation + amortization\n'
                              '\n'
                              '# Example usage\n'
                              'company_ebitda = calculate_ebitda(1000000, 50000, 300000, 200000, 150000)\n'
                              'print(f"Company EBITDA: ${company_ebitda:,}")\n'
                              '```\n\n'
                              'EBITDA is often used to evaluate a company\'s performance without the effects of financing and accounting decisions.',
                'category': 'Financial Metrics'
            },
            {
                'term': 'Sharpe Ratio',
                'definition': 'A measure that indicates the average return earned in excess of the risk-free rate per unit of volatility or total risk. The Sharpe ratio characterizes how well the return of an asset compensates the investor for the risk taken.\n\n'
                              '### Formula\n\n'
                              '$$\\text{Sharpe Ratio} = \\frac{R_p - R_f}{\\sigma_p}$$\n\n'
                              'Where:\n'
                              '- $R_p$ is the return of the portfolio\n'
                              '- $R_f$ is the risk-free rate\n'
                              '- $\\sigma_p$ is the standard deviation of the portfolio\'s excess return\n\n'
                              'A higher Sharpe ratio indicates better risk-adjusted performance. A negative Sharpe ratio indicates that the risk-free rate is greater than the portfolio\'s return, or that the portfolio\'s return is expected to be negative.\n\n'
                              '### Python Implementation\n\n'
                              '```python\n'
                              'import numpy as np\n'
                              '\n'
                              'def sharpe_ratio(returns, risk_free_rate):\n'
                              '    """Calculate the Sharpe ratio of a set of returns.\n'
                              '    \n'
                              '    Args:\n'
                              '        returns (array-like): A series of returns\n'
                              '        risk_free_rate (float): The risk-free rate of return\n'
                              '        \n'
                              '    Returns:\n'
                              '        float: The Sharpe ratio\n'
                              '    """\n'
                              '    excess_returns = np.array(returns) - risk_free_rate\n'
                              '    return excess_returns.mean() / excess_returns.std()\n'
                              '```',
                'category': 'Performance Metrics'
            },
            {
                'term': 'Monte Carlo Simulation',
                'definition': 'A computational technique used to model the probability of different outcomes in a process that cannot easily be predicted due to the intervention of random variables. It is commonly used in finance for risk assessment and in the valuation of derivatives.\n\n'
                              '### Applications in Finance\n\n'
                              '- **Portfolio Management**: Estimating the probability of different returns\n'
                              '- **Option Pricing**: Simulating various price paths for the underlying asset\n'
                              '- **Risk Management**: Calculating Value at Risk (VaR)\n'
                              '- **Retirement Planning**: Projecting potential outcomes for retirement portfolios\n\n'
                              '### Basic Python Implementation\n\n'
                              '```python\n'
                              'import numpy as np\n'
                              'import matplotlib.pyplot as plt\n'
                              '\n'
                              'def monte_carlo_stock_sim(S0, mu, sigma, dt, T, num_simulations):\n'
                              '    """Monte Carlo simulation for stock price paths.\n'
                              '    \n'
                              '    Args:\n'
                              '        S0 (float): Initial stock price\n'
                              '        mu (float): Expected return (annualized)\n'
                              '        sigma (float): Volatility (annualized)\n'
                              '        dt (float): Time step\n'
                              '        T (float): Time period in years\n'
                              '        num_simulations (int): Number of simulation paths\n'
                              '        \n'
                              '    Returns:\n'
                              '        numpy.ndarray: Matrix of simulated stock price paths\n'
                              '    """\n'
                              '    num_steps = int(T / dt)\n'
                              '    paths = np.zeros((num_steps + 1, num_simulations))\n'
                              '    paths[0] = S0\n'
                              '    \n'
                              '    for t in range(1, num_steps + 1):\n'
                              '        z = np.random.standard_normal(num_simulations)\n'
                              '        paths[t] = paths[t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * z)\n'
                              '        \n'
                              '    return paths\n'
                              '```',
                'category': 'Quantitative Methods'
            },
            {
                'term': 'Black-Scholes Model',
                'definition': 'A mathematical model for pricing European-style options. The model assumes that the price of heavily traded assets follows a geometric Brownian motion with constant drift and volatility.\n\n'
                              '### Key Assumptions\n\n'
                              '- The stock price follows a log-normal distribution\n'
                              '- No transaction costs or taxes\n'
                              '- No dividends during the option\'s life\n'
                              '- Markets are efficient (no arbitrage)\n'
                              '- Risk-free interest rate is constant\n'
                              '- Volatility of the underlying asset is constant\n\n'
                              '### Formulas\n\n'
                              'For a call option:\n\n'
                              '$$C = S_0 N(d_1) - Ke^{-rT} N(d_2)$$\n\n'
                              'For a put option:\n\n'
                              '$$P = Ke^{-rT} N(-d_2) - S_0 N(-d_1)$$\n\n'
                              'Where:\n\n'
                              '$$d_1 = \\frac{\\ln(\\frac{S_0}{K}) + (r + \\frac{\\sigma^2}{2})T}{\\sigma\\sqrt{T}}$$\n\n'
                              '$$d_2 = d_1 - \\sigma\\sqrt{T}$$\n\n'
                              '- $S_0$ is the current stock price\n'
                              '- $K$ is the strike price\n'
                              '- $r$ is the risk-free interest rate\n'
                              '- $T$ is the time to maturity\n'
                              '- $\\sigma$ is the volatility of the stock price\n'
                              '- $N(\\cdot)$ is the cumulative distribution function of the standard normal distribution',
                'category': 'Derivatives Pricing'
            },
            {
                'term': 'Value at Risk (VaR)',
                'definition': 'A statistical technique used to measure and quantify the level of financial risk within a firm or investment portfolio over a specific time frame. VaR is defined as the maximum potential loss in value of a portfolio due to adverse market movements, for a given confidence level, over a defined period.\n\n'
                              '### Types of VaR Calculation Methods\n\n'
                              '1. **Historical Method**: Uses past data to project future outcomes\n'
                              '2. **Variance-Covariance Method**: Assumes returns follow a normal distribution\n'
                              '3. **Monte Carlo Simulation**: Generates numerous random scenarios\n\n'
                              '### Mathematical Expression\n\n'
                              'For a portfolio, VaR can be expressed as:\n\n'
                              '$$P(\\Delta P \\leq -\\text{VaR}) = 1 - c$$\n\n'
                              'Where:\n'
                              '- $\\Delta P$ is the change in portfolio value\n'
                              '- $c$ is the confidence level (typically 95% or 99%)\n'
                              '- $\\text{VaR}$ is the Value at Risk\n\n'
                              'This means that with confidence $c$, the loss will not exceed VaR over the specified time period.',
                'category': 'Risk Management'
            },
            {
                'term': 'Yield Curve',
                'definition': 'A line that plots yields (interest rates) of bonds having equal credit quality but differing maturity dates. The slope of the yield curve gives an idea of future interest rate changes and economic activity.\n\n'
                              '### Types of Yield Curves\n\n'
                              '1. **Normal Yield Curve**: Upward sloping, indicating higher yields for longer maturities\n'
                              '2. **Inverted Yield Curve**: Downward sloping, indicating lower yields for longer maturities (often seen as a recession indicator)\n'
                              '3. **Flat Yield Curve**: Similar yields regardless of maturity\n'
                              '4. **Humped Yield Curve**: Yields rise for medium-term maturities and fall for long-term maturities\n\n'
                              '### Visualization in Python\n\n'
                              '```python\n'
                              'import numpy as np\n'
                              'import matplotlib.pyplot as plt\n'
                              '\n'
                              '# Sample data for different yield curves\n'
                              'maturities = [1, 2, 3, 5, 7, 10, 20, 30]  # years\n'
                              '\n'
                              '# Different types of yield curves\n'
                              'normal_curve = [1.5, 1.8, 2.1, 2.5, 2.8, 3.0, 3.3, 3.4]  # Normal\n'
                              'inverted_curve = [3.2, 3.0, 2.8, 2.5, 2.2, 2.0, 1.8, 1.7]  # Inverted\n'
                              'flat_curve = [2.5, 2.5, 2.5, 2.6, 2.5, 2.5, 2.5, 2.5]  # Flat\n'
                              '\n'
                              'plt.figure(figsize=(10, 6))\n'
                              'plt.plot(maturities, normal_curve, \'b-\', label=\'Normal Yield Curve\')\n'
                              'plt.plot(maturities, inverted_curve, \'r-\', label=\'Inverted Yield Curve\')\n'
                              'plt.plot(maturities, flat_curve, \'g-\', label=\'Flat Yield Curve\')\n'
                              'plt.xlabel(\'Maturity (years)\')\n'
                              'plt.ylabel(\'Yield (%)\')\n'
                              'plt.title(\'Types of Yield Curves\')\n'
                              'plt.legend()\n'
                              'plt.grid(True)\n'
                              'plt.show()\n'
                              '```',
                'category': 'Fixed Income'
            }
        ]

        # Add terms to the database
        terms_added = 0
        for term_data in terms:
            # Skip if the term already exists
            if GlossaryTerm.objects.filter(term=term_data['term']).exists():
                self.stdout.write(self.style.WARNING(f"Term '{term_data['term']}' already exists. Skipping."))
                continue

            # Create and save the term
            term = GlossaryTerm(
                term=term_data['term'],
                definition=term_data['definition'],
                category=term_data['category']
            )
            term.save()
            terms_added += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully added {terms_added} glossary terms'))
