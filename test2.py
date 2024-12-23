import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List
import openai
from pathlib import Path

class TokenMetricsIntegrator:
    """
    Integrates predicted metrics from separate CSV files and uses LLM to predict ideal votable supply
    """
    
    def __init__(self, file_paths: Dict[str, str], csv_path: str):
        """
        Initialize with paths to prediction CSV files
        
        Args:
            file_paths: Dictionary mapping metric names to file paths
            Example: {
                'PR': 'PR-forecast-data.csv',
                'PSI': 'PSI-forecast-data.csv',
                'VPI': 'VPI-forecast-data.csv',
                'LAR': 'LAR-forecast-data.csv',
                'Actual_VPI': 'Actual-VPI-forecast-data.csv'
            }
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


        self.file_paths = file_paths
        self.required_metrics = ['PR', 'PSI', 'VPI', 'LAR', 'Actual_VPI']
        self.integrated_data = None
        
    def validate_files(self) -> None:
        """Validate that all required files exist and have correct format"""
        for metric in self.required_metrics:
            if metric not in self.file_paths:
                raise ValueError(f"Missing file path for required metric: {metric}")
            
            if not Path(self.file_paths[metric]).exists():
                raise FileNotFoundError(f"File not found: {self.file_paths[metric]}")

    def read_and_integrate_data(self) -> pd.DataFrame:
        """Read all CSV files and integrate them into a single DataFrame"""
        try:
            # Initialize with first file
            first_metric = self.required_metrics[0]
            df = pd.read_csv(self.file_paths[first_metric])
            df.columns = ['Date', first_metric]
            
            # Add other metrics
            for metric in self.required_metrics[1:]:
                temp_df = pd.read_csv(self.file_paths[metric])
                df[metric] = temp_df['Forecasted Value']
            
            # Convert Date to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            self.integrated_data = df
            return df
            
        except Exception as e:
            raise Exception(f"Error integrating data: {str(e)}")

    def calculate_monthly_statistics(self) -> Dict[str, Dict]:
        """Calculate monthly statistics for each metric"""
        if self.integrated_data is None:
            raise ValueError("No data loaded. Call read_and_integrate_data first.")
        
        monthly_stats = {}
        
        # Add month-year column for grouping
        self.integrated_data['Month-Year'] = self.integrated_data['Date'].dt.strftime('%Y-%m')
        
        for metric in self.required_metrics:
            monthly_grouped = self.integrated_data.groupby('Month-Year')[metric]
            
            metric_stats = {
                'monthly_data': {
                    month: {
                        'min': float(group.min()),
                        'max': float(group.max()),
                        'avg': float(group.mean()),
                        'median': float(group.median()),
                        'std': float(group.std())
                    }
                    for month, group in monthly_grouped
                },
                'overall_stats': {
                    'min': float(self.integrated_data[metric].min()),
                    'max': float(self.integrated_data[metric].max()),
                    'avg': float(self.integrated_data[metric].mean()),
                    'median': float(self.integrated_data[metric].median()),
                    'std': float(self.integrated_data[metric].std())
                }
            }
            monthly_stats[metric] = metric_stats
        
        return monthly_stats
    
    def monthly_statistics_vs(self) -> dict:
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
        
        return monthly_stats['VS']

    def create_llm_prompt(self, monthly_stats: Dict, monthly_stats_vs: Dict) -> str:
        """Create detailed prompt for LLM"""
        return f"""
        Task: As a financial analyst specializing in token governance and economic modeling, predict the ideal monthly Votable Supply (VS) from Dec 2024 to Dec 2025 that maximizes attack cost based on the provided metrics.

        Parameter Definitions:
        - PR (Participation Ratio): Ratio of tokens participating in governance
        - PSI (Protocol Staking Index): Measure of tokens staked in protocol
        - VPI (Voting Power Index): Measure of voting power distribution
        - LAR (Liquidity Availability Ratio): Measure of token liquidity
        - Actual VPI: Realized voting power index
        - VS (Votable Supply): Amount of tokens eligible for voting

        Your predictions should:
        - The predictions should maximize the cost of potential attacks on the system
        - Votable Supply (VS) should be optimized based on relationship with other metrics and to maximize the cost of attack as a major consideration
        - Consider monthly patterns and trends in the Historical data of VS
        - Ensure predictions maintain realistic growth patterns of Historical data of VS
        
        Monthly Statistics for Key Metrics:
        {json.dumps(monthly_stats, indent=2)}

        Monthly Statistics for Historical data of VS:
        {json.dumps(monthly_stats_vs, indent=2)}

        Required Output Format:
            1. Month-by-Month VS Predictions Table:
            | Month | Predicted VS |
            * VS: whole numbers
            - Show monthly progression with consistent growth rates
            - Ensure December 2024 values logically follow from November 2024
            - Include all months from Dec 2024 to Dec 2025

            2. Methodology Documentation:
            - Explain how the predicted VS values maximize attack cost
            - Document relationships between metrics that influenced predictions
            - Detail any patterns or trends considered

            3. Security Analysis:
            - Explain how these VS predictions enhance system security
            - Analyze potential attack vectors and their costs
            - Quantify the improvement in security metrics
        """

    def get_llm_predictions(self, monthly_stats: Dict, api_key: str) -> str:
        """Get predictions from LLM"""
        openai.api_key = api_key

        monthly_stats_vs = self.monthly_statistics_vs()
        
        try:
            prompt = self.create_llm_prompt(monthly_stats, monthly_stats_vs)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a financial analyst specializing in token governance and economic modeling, with expertise in security and attack vector analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"LLM prediction failed: {str(e)}")

def main():
    # File paths configuration
    file_paths = {
        'PR': 'Votable-supply-data-forecasting/PR/PR-forecast-data.csv',
        'PSI': 'Votable-supply-data-forecasting/PSI/PSI-forecast-data.csv',
        'VPI': 'Votable-supply-data-forecasting/VPI/VPI-forecast-data.csv',
        'LAR': 'Votable-supply-data-forecasting/LAR/LAR-forecast-data.csv',
        'Actual_VPI': 'Votable-supply-data-forecasting/Actual-VPI/Actual-VPI-forecast-data.csv'
    }

    csv_path = "merged_data.csv"
    
    # OpenAI API key
    api_key = 'OpenAI_Api_Key'
    
    try:
        # Initialize integrator
        integrator = TokenMetricsIntegrator(file_paths, csv_path)
        
        # Validate files
        integrator.validate_files()
        print("Validation Completed")
        
        # Read and integrate data
        integrator.read_and_integrate_data()
        print("Intigration Completed")
        
        # Calculate monthly statistics
        monthly_stats = integrator.calculate_monthly_statistics()
        # print(monthly_stats)
        
        # Get LLM predictions
        predictions = integrator.get_llm_predictions(monthly_stats, api_key)
        
        # Save results
        results = {
            'monthly_statistics': monthly_stats,
            'llm_predictions': predictions
        }
        
        with open('token_metrics_analysis.json', 'w') as f:
            json.dump(results, f, indent=2)

        with open(f'token_metrics_analysis.md', 'w') as f:
            f.write(results['llm_predictions'])
            
        print("Analysis complete. Results saved to token_metrics_analysis.json")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()