1. Predictions Table:

| Month (MMM-YYYY) | Ideal Votable Supply |
| --- | --- |
| Dec-2024 | 107560000 |
| Jan-2025 | 109050000 |
| Feb-2025 | 110550000 |
| Mar-2025 | 112060000 |
| Apr-2025 | 113580000 |
| May-2025 | 115110000 |
| Jun-2025 | 116650000 |
| Jul-2025 | 118190000 |
| Aug-2025 | 119740000 |
| Sep-2025 | 121300000 |
| Oct-2025 | 122870000 |
| Nov-2025 | 124450000 |
| Dec-2025 | 126040000 |

2. Methodology Documentation:

a. Key Considerations:

- Relationship between VS (Votable Supply) and attack cost: A larger votable supply means a higher number of tokens that an attacker would need to influence the network, and thus the cost of the attack would be more expensive. This suggests that maximizing the Votable Supply would require an increase in the cost of the attack.

- PR (Participation Ratio) impact: The higher the PR, the more decentralized the network, which usually leads to higher security. However, a large PR also implies a potential decrease in VS as more tokens are staked in the network rather than staying liquid. Therefore, a balance between a healthy PR and a sufficient VS needs to be maintained to ensure both network stability and resistance to attack.

- Total Supply's influence: Any calculation related to the VS must take the total supply into consideration, as the VS cannot exceed the total supply. Additionally, the PR is a factor of both VS and total supply.

b. Calculation Method:

- Correlation function: From the correlation matrix provided, it's seen that there's a strong positive correlation (0.87) between 'VS' and 'CS' (Circulating Supply). For PR there's a smaller negative correlation (-0.165) with VS. Given these correlations, while a high PR is ideal, an increase in VS is likely even more effective in increasing the cost of attack.

- Prediction equation: Based on overall trends, there appears to be a linear relationship in the growth of the 'VS' from the 'monthly_stats' data over the past 12 months. We can therefore predict the future VS by applying a linear growth pattern observed from the past data.

- Growth rate determination: The growth rate was determined by calculating the average month over month percent change in 'VS' for the last 12 months from the 'monthly_stats'. A 1.4% monthly growth rate was observed and has been applied for future predictions. 

This prediction strategy ensures a steady growth of the VS which should increase the cost of attack and thus maintain security of the network. Further, taking into account the correlations with circulating supply and PR allows for a more well-rounded strategy. This prediction model however is quite simple and assumes that current trends will continue into the future. Therefore, these predictions should be updated and validated as new data becomes available.