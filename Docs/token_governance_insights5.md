1. Predictions Table:

| Month | Ideal Votable Supply |
|-------|---------------------|
| Dec-2024 | 105066220.77 |
| Jan-2025 | 107587100.33 |
| Feb-2025 | 110107979.89 |
| Mar-2025 | 112628859.45 |
| Apr-2025 | 115149739.01 |
| May-2025 | 117670618.57 |
| Jun-2025 | 120191498.13 |
| Jul-2025 | 122712377.69 |
| Aug-2025 | 125233257.25 |
| Sep-2025 | 127754136.81 |
| Oct-2025 | 130275016.37 |
| Nov-2025 | 132795895.93 |
| Dec-2025 | 135316775.49 | 

2. Methodology Documentation:

    a. Key Considerations:

        - Relationship between VS (Votable Supply) and Attack Cost: The cost of an attack is directly proportional to the votable supply. The larger the votable supply, the more costly an attack will be, which strengthens the security of the system.
        
        - PR (Participation Ratio) Impact: A higher PR means there are more active participants in the governance process and hence, more tokens are being actively used for voting. A higher PR could potentially lead to a higher VS, therefore, making any attacks more costly.
        
        - Total Supply Influence: The size of the total supply restricts the size of the votable supply and thus can also influence the cost of an attack vector.

    b. Calculation Method: 

       The prediction method is based on a linear regression model that captures the relationship between the months and the Votable Supply. The first step involves defining a correlation function between PR and VS based on historical data and cost of attack vector. The attack cost model shows an attack resistance score of 0.992, which suggests a strong correlation between the votable supply (VS) and the resistance to attacks.

        - Prediction equation: Based on this correlation, the prediction equation is simply the votable supply for the previous month + ((average growth rate) * (previous month's votable supply)). The reason for choosing this metric is because of the high correlation score between the two variables PR and VS. The growth rate between months is determined by calculating the mean of differences in votable supply month over month.

    With these calculations, we can predict the cost of an attack for the coming 12 months while honoring the observed patterns in the dataset and considering the upward trend of votable supply.