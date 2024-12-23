import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import json

# Optional: For LLM integration (if using OpenAI)
import openai

class TokenGovernanceAnalyzer:
    def __init__(self, csv_path: str):
        """
        Initialize the analyzer with CSV data
        
        Args:
            csv_path (str): Path to the CSV file containing token governance metrics
        """
        # Read CSV file
        self.df = pd.read_csv(csv_path)
        
        # Validate required columns
        required_columns = ['Date', 'PR', 'PSI', 'VPI', 'LAR', 'Actual VPI', 'VS', 'CS']
        for col in required_columns:
            if col not in self.df.columns:
                raise ValueError(f"Missing required column: {col}")
        
        # Convert Date column to datetime
        self.df['Date'] = pd.to_datetime(self.df['Date'], dayfirst=True)

    
    def descriptive_statistics(self) -> Dict[str, Any]:
        """
        Generate descriptive statistics for key metrics
        
        Returns:
            Dict containing detailed statistical summary
        """
        metrics = ['CS', 'VS', 'PR', 'PSI', 'LAR', 'VPI', 'Actual VPI']
        stats_summary = {}
        
        for metric in metrics:
            stats_summary[metric] = {
                'min': self.df[metric].min(),
                'max': self.df[metric].max(),
                'mean': self.df[metric].mean(),
                'median': self.df[metric].median(),
                'std': self.df[metric].std(),
                'skew': self.df[metric].skew()
            }
        
        return stats_summary
    
    def correlation_analysis(self) -> np.ndarray:
        """
        Perform correlation analysis between metrics
        
        Returns:
            Correlation matrix as numpy array
        """
        metrics = ['CS', 'VS', 'PR', 'PSI', 'LAR', 'VPI', 'Actual VPI']
        correlation_matrix = self.df[metrics].corr()
        return correlation_matrix
    
    def optimal_vs_analysis(self) -> Dict[str, Any]:
        """
        Analyze optimal Votable Supply (VS) range
        
        Returns:
            Dictionary with optimal VS insights
        """
        # Sort by Participation Ratio
        sorted_df = self.df.sort_values('PR')
        
        # Select middle 50% of data
        start_idx = len(sorted_df) // 4
        end_idx = len(sorted_df) * 3 // 4
        optimal_range = sorted_df.iloc[start_idx:end_idx]
        
        return {
            'optimal_vs_mean': optimal_range['VS'].mean(),
            'optimal_vs_median': optimal_range['VS'].median(),
            'optimal_vs_std': optimal_range['VS'].std(),
            'participation_range': (optimal_range['PR'].min(), optimal_range['PR'].max())
        }
    
    def attack_cost_model(self) -> Dict[str, float]:
        """
        Estimate attack cost based on token metrics
        
        Returns:
            Dictionary with attack cost model parameters
        """
        # Simplified attack cost estimation
        return {
            'total_supply': self.df['CS'].mean(),
            'votable_supply': self.df['VS'].mean(),
            'participation_ratio': self.df['PR'].mean(),
            'attack_resistance_score': 1 - (self.df['VS'].mean() / self.df['CS'].mean())**2
        }
    
    def visualize_metrics(self, output_path: str = 'token_metrics_viz.png'):
        """
        Create visualizations of key metrics
        
        Args:
            output_path (str): Path to save visualization
        """
        plt.figure(figsize=(15, 10))
        
        # Metrics to visualize
        metrics = ['VS', 'PR', 'VPI']
        
        for i, metric in enumerate(metrics, 1):
            plt.subplot(2, 2, i)
            sns.lineplot(x=self.df['Date'], y=self.df[metric])
            plt.title(f'{metric} Over Time')
            plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def monthly_statistics(self) -> dict:
        """
        Calculate monthly statistics for all metrics
        
        Returns:
            Dictionary containing monthly stats for each metric
        """
        metrics = ['PR', 'PSI', 'VPI', 'LAR', 'Actual VPI', 'VS', 'CS']
        # First ensure the Date column is in datetime format
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%m-%Y')
        
        # Extract month and year
        self.df['Month-Year'] = self.df['Date'].dt.strftime('%Y-%m')
        
        monthly_stats = {}
        
        # Group by month and calculate statistics for each metric
        monthly_grouped = self.df.groupby('Month-Year')
        
        for metric in metrics:
            metric_stats = {
                'monthly_data': {
                    month: {
                        'avg': float(group[metric].mean()),
                        'max': float(group[metric].max())
                    }
                    for month, group in monthly_grouped
                },
                'overall_stats': {
                    'mean': float(self.df[metric].mean()),
                    'max': float(self.df[metric].max())
                }
            }
            monthly_stats[metric] = metric_stats
        
        return monthly_stats
    
    def generate_llm_insights(self, api_key: str = None) -> str:
        """
        Generate insights using an LLM (OpenAI GPT by default)
        
        Args:
            api_key (str, optional): OpenAI API key
        
        Returns:
            Generated insights as a string
        """
        # Prepare analysis data
        analysis_data = {
            'monthly_stats': self.monthly_statistics(),
            'descriptive_stats': self.descriptive_statistics(),
            'correlation_matrix': self.correlation_analysis().to_dict(),
            'optimal_vs': self.optimal_vs_analysis(),
            'attack_cost_model': self.attack_cost_model()
        }
        # print(json.dumps(analysis_data, indent=2, default=convert_numpy_types))
        # If OpenAI key is provided, use GPT for insights
        if api_key:
            openai.api_key = api_key
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a financial analyst specializing in token governance and economic modeling. Your expertise is in analyzing and predicting token supply metrics with a focus on security and attack vector costs."},
                        {"role": "user", "content": f"""
                        Task: Analyze the historical data and predict parameters for Dec 2024 - Dec 2025 that would maximize the cost of attack vector while maintaining trend continuity from Nov 2024. Calculate each parameter in relation to others to determine the optimal Votable Supply.

                        Historical Data Context:
                        {json.dumps(analysis_data, indent=2, default=convert_numpy_types)}

                        Your predictions should:
                        - First predict PR, PSI, VPI, LAR, and Actual VPI based on historical trends
                        - Ensure December 2024 predictions follow November 2024's trend
                        - Each parameter should be calculated considering its impact on attack cost
                        - Parameters should show logical month-over-month progression
                        - Calculate ideal Votable Supply as a function of other predicted parameters
                        - VS should maximize cost of attack while maintaining realistic growth
                        - Show how VS relates to other parameters in the attack cost equation
                        - Identify growth patterns in historical data
                        - Use these patterns to inform forward predictions
                        - Ensure all predictions follow logical progression from November 2024
                        - Consider seasonal patterns if present in historical data


                        Required Output Format:
                        1. Predictions Table:
                        Generate a detailed markdown table with the following specifications:
                        - Time period: Dec 2024 - Dec 2025 (13 months)
                        - Columns: Month (MMM-YYYY) | PR | PSI | VPI | LAR | Actual VPI | VS
                        - Format numbers consistently:
                        * PR, PSI, VPI, LAR, Actual VPI: 4 decimal places
                        * VS: whole numbers
                        - Show monthly progression with consistent growth rates
                        - Ensure December 2024 values logically follow from November 2024

                        2. Calculation Methodology:
                        a. Parameter Relationships:
                            - Explain how each parameter affects others
                            - Show formulas used for parameter calculations
                            - Demonstrate how parameters combine to maximize attack cost
                        
                        b. Trend Continuity:
                            - Document how predictions maintain trend from November 2024
                            - Explain growth rates used for each parameter
                            - Show how predictions avoid unrealistic jumps or drops

                        3. Attack Cost Analysis:
                        - Show how predicted parameters maximize attack cost
                        - Demonstrate relationship between parameters and attack resistance
                        - Quantify improvement in security from current state
                        """}
                    ]


                    # messages=[
                    #     {"role": "system", "content": "CopyYou are a financial analyst specializing in token governance and economic modeling. Your expertise is in analyzing and predicting token supply metrics with a focus on security and attack vector costs."},
                    #     {"role": "user", "content": f"""
                    #     Task: Based on the provided analysis_data for the past 12 months, analyze and predict the ideal Votable Supply (VS) that would maximize the cost of attack for the next 12 months (Dec 2024 - Dec 2025).

                    #     Analysis Data:
                    #     {json.dumps(analysis_data, indent=2, default=convert_numpy_types)}


                    #     Your predictions should:
                    #         - Show logical continuity from the historical data of VS in the monthly_stats of analysis_data
                    #         - Demonstrate how they maximize the cost of attack vector
                    #         - Include clear monthly progression
                    #         - Be based on observable patterns in the provided data
                    #         - Follow VS trend of last month to next months while predicting

                    #         Base all calculations and predictions solely on the patterns and relationships found in the provided analysis_data.

                    #     Required Output Format:

                    #         1. Predictions Table:
                    #         Present a markdown table showing month-wise predictions with exactly two columns:
                    #         - Column 1: Month (Format: MMM-YYYY)
                    #         - Column 2: Ideal Votable Supply (numeric values)

                    #         2. Methodology Documentation:
                    #         Document your prediction methodology using these sections:
                    #         a. Key Considerations:
                    #             - Explain the relationship between VS (Votable Supply) and attack cost
                    #             - Describe the PR (Participation Ratio) impact
                    #             - Detail the Total Supply's influence
                            
                    #         b. Calculation Method:
                    #             - Define your correlation function between PR and VS based on historical data and cost of attack vector.
                    #             - Present your prediction equation and explain why you chose it
                    #             - Detail how you determined the growth rate between months
                    #     """}
                    # ]


                    # messages=[
                    #     {"role": "system", "content": "You are a financial analyst specializing in token governance and economic modeling. Your expertise is in analyzing and predicting token supply metrics with a focus on security and attack vector costs."},
                    #     {"role": "user", "content": f"""
                    #     Task: Based on the provided analysis_data for the past 12 months, analyze all the available independent variable and predict the ideal Votable Supply (VS) and all other features that would maximize the cost of attack for the next 12 months (Dec 2024 - Dec 2025).

                    #     Analysis Data:
                    #     {json.dumps(analysis_data, indent=2, default=convert_numpy_types)}


                    #     Your predictions should:
                    #         - Use all Features to define and predict with respect to cost of attack vector.
                    #         - Show logical continuity from the historical data of all parameters['PR', 'PSI', 'VPI', 'LAR', 'Actual VPI', 'VS'] in the monthly_stats of analysis_data
                    #         - Demonstrate how they maximize the cost of attack vector
                    #         - Include clear monthly progression
                    #         - Be based on observable patterns in the provided data
                    #         - Follow trend of last month(Historical) to next months(Forecasting) while predicting for all parameters['PR', 'PSI', 'VPI', 'LAR', 'Actual VPI', 'VS']
                    #         - Follow trend of last month to next month while prediction VS.

                    #         Base all calculations and predictions solely on the patterns and relationships found in the provided analysis_data.

                    #     Required Output Format:

                    #         1. Predictions Table:
                    #         Present a markdown table showing month-wise predictions with exactly two columns:
                    #         - Column 1: Month (Format: MMM-YYYY)
                    #         - Column 2: Participation Ratio[PR]
                    #         - Column 3: PSI
                    #         - Column 4: VPI
                    #         - Column 5: LAR
                    #         - Column 6: Actual VPI
                    #         - Column 7: Ideal Votable Supply (numeric values)

                    #         2. Methodology Documentation:
                    #         Document your prediction methodology using these sections:
                    #         a. Key Considerations:
                    #             - Explain the relationship between VS (Votable Supply) and attack cost
                    #             - Describe the PR (Participation Ratio) impact
                    #             - Detail the Total Supply's influence
                    #             - Describe all other parameters and cos of attack vector.
                            
                    #         b. Calculation Method:
                    #             - Define your correlation function between all parameters based on historical data and cost of attack vector.
                    #             - Present your prediction. detailed note how you have calculated.
                    #     """}
                    # ]



                    # messages=[
                    #     {"role": "system", "content": "You are a financial analyst specializing in token governance and economic modeling. You need to provide predictions based on cost of attack vector over the system."},
                    #     {"role": "user", "content": f"""
                    #     Understand the cost of attack vector for the system.
                    #     Your task is to calculate and predict the outcome of Ideal Votable Supply with maximizing the cost of attack vector month-wise for(Dec/24 - Dec/25) next 12 months, not to provide steps to predict.
                    #     Anaysis of data for last 12 months (Jan/24 to Nov/24) monthwise from [monthly_stats].
                    #     For predicting ideal votable supply consider maximizing cost of attack vector as a major parameter. but follow the continuous trend also(from last 12 months to next 12 month)

                    #     Analysis Data:
                    #     {json.dumps(analysis_data, indent=2, default=convert_numpy_types)}

                    #     Determine the ideal VS (Votable Supply) that maximizes the cost of attack. Calculate and predict the below requirements:
                    #         1. (In Table Format)The predicted value of the ideal Votable Supply month-wise for(Dec/24 - Dec/25) next 12 months.
                    #         2. Document the detailed logic used for predicting the ideal VS for month-wise for next 12 months.
                    #     """}
                    # ]
                )
                respon = response.choices[0].message.content
                # print(respon)
                return respon
            
            except Exception as e:
                print(f"LLM insight generation failed: {e}")
        
        # Fallback text-based insights generation
        return self._generate_text_insights(analysis_data)
    
    def _generate_text_insights(self, analysis_data: Dict) -> str:
        """
        Generate text-based insights when LLM is not available
        
        Args:
            analysis_data (Dict): Prepared analysis data
        
        Returns:
            Generated insights as a string
        """
        insights = "# Token Governance Analysis Insights\n\n"
        
        # Descriptive Statistics
        insights += "## Descriptive Statistics\n"
        for metric, stats in analysis_data['descriptive_stats'].items():
            insights += f"### {metric} Metrics\n"
            insights += f"- Mean: {stats['mean']:.4f}\n"
            insights += f"- Median: {stats['median']:.4f}\n"
            insights += f"- Min: {stats['min']:.4f}\n"
            insights += f"- Max: {stats['max']:.4f}\n"
        
        # Optimal VS Analysis
        optimal_vs = analysis_data['optimal_vs']
        insights += "\n## Optimal Votable Supply (VS) Analysis\n"
        insights += f"- Optimal VS Mean: {optimal_vs['optimal_vs_mean']:.4f}\n"
        insights += f"- Optimal VS Median: {optimal_vs['optimal_vs_median']:.4f}\n"
        insights += f"- Participation Range: {optimal_vs['participation_range']}\n"
        
        # Attack Cost Model
        attack_model = analysis_data['attack_cost_model']
        insights += "\n## Attack Cost Model\n"
        insights += f"- Total Supply: {attack_model['total_supply']:.4f}\n"
        insights += f"- Votable Supply: {attack_model['votable_supply']:.4f}\n"
        insights += f"- Attack Resistance Score: {attack_model['attack_resistance_score']:.4f}\n"
        
        return insights
    
    def run_full_analysis(self, output_dir: str = '.', llm_api_key: str = None):
        """
        Perform comprehensive token governance analysis
        
        Args:
            output_dir (str): Directory to save output files
            llm_api_key (str, optional): API key for LLM insights
        """
        # Descriptive Statistics
        stats = self.descriptive_statistics()
        with open('descriptive_stats.json', 'w') as f:
            json.dump(stats, f, indent=2, default=convert_numpy_types)
        # Correlation Analysis
        corr_matrix = self.correlation_analysis()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Matrix of Token Metrics')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/correlation_heatmap.png')
        plt.close()
        
        # Visualize Metrics
        self.visualize_metrics(f'{output_dir}/token_metrics_viz.png')
        
        # Generate Insights
        insights = self.generate_llm_insights(llm_api_key)
        with open(f'{output_dir}/token_governance_insights.md', 'w') as f:
            f.write(insights)

def convert_numpy_types(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


# Example Usage
def main():
    # Replace with your actual CSV path
    csv_path = 'merged_data.csv'
    
    # Initialize Analyzer
    analyzer = TokenGovernanceAnalyzer(csv_path)
    
    # Optional: Add your OpenAI API key for LLM insights
    llm_api_key = "OpenAI_Api_Key"
    # llm_api_key = None
    
    # Run Full Analysis
    analyzer.monthly_statistics()
    analyzer.run_full_analysis(llm_api_key=llm_api_key)
    
    # Print some immediate insights
    print("Descriptive Statistics:")
    print(json.dumps(analyzer.descriptive_statistics(), 
                 indent=2, 
                 default=convert_numpy_types))
    
    print("\nOptimal VS Analysis:")
    print(json.dumps(analyzer.optimal_vs_analysis(), indent=2, default=convert_numpy_types))

if __name__ == '__main__':
    main()