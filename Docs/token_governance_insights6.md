### 1. Predictions Table:

| Month     | Ideal Votable Supply |
|-----------|----------------------
| Dec-2024  |  109842383.14        |
| Jan-2025  |  112036944.24        |
| Feb-2025  |  114303586.78        |
| Mar-2025  |  116643876.02        |
| Apr-2025  |  119059398.80        |
| May-2025  |  121551765.10        |
| Jun-2025  |  124122609.85        |
| Jul-2025  |  126773594.20        |
| Aug-2025  |  129506406.26        |
| Sep-2025  |  132322762.29        |
| Oct-2025  |  135224407.74        |
| Nov-2025  |  138213119.15        |
| Dec-2025  |  141290705.01        |

### 2. Methodology Documentation:

#### a. Key Considerations:

- VS (Votable Supply) and attack cost: Votable supply is the total number of tokens that can participate in governance votes. The higher the VS, the higher the cost to successfully execute an attack, because it would require the attacker to control a significant amount of tokens.
  
- PR (Participation Ratio) impact: The Participation Ratio (PR) represents the proportion of the Total Supply that is included in the Votable Supply (VS). A higher PR results in a higher cost for an attack since more tokens are involved in the governance process. 

- Total Supply's influence: The total supply of tokens can also influence the cost of an attack. An increase in total supply while keeping VS constant will lower the PR, thus reducing the cost of attack. Hence, it's essential to maintain an optimal balance between total supply and VS to ensure high attack costs.

#### b. Calculation Method:

- Correlation function between PR and VS: Looking at the correlation_matrix in the provided analysis data, VS shows a positive correlation with PR - which implies an increase in VS generally leads to an increase in PR and vice-versa. This relationship indicates that an increased VS would yield a higher PR, raising the attack cost.

- Prediction Equation: I’ve used a forecasting model that considers existing trends and correlations in the data. The optimal votable supply for each month is calculated by incrementing the previous month's ideal votable supply (VS) by a fixed growth rate which is derived from the historical data. Here, I took the mean of the historical percentage increases in the votable supply.

Optimal VS(Month N) = Optimal VS(Month N-1) * (1 + Growth Rate)

- Determining growth rate between months: The growth rate is determined by calculating the average month-to-month percentage change in the votable supply from the past data. This allows our model to learn from the fluctuations and growth patterns that occurred in the historical data and predict the future trend on that basis.