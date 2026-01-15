import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import os

# Set the working directory to where your data is located
os.chdir("C:\\Users\\User\\Documents\\Local Send")

# Load the data

data = pd.read_csv('data.csv')

# Define numeric and categorical variables of interest
numeric_variables = [
    "Recovery_time", "Reaction_time", "Response_time", "Accuracy", 
    "Alarms_silenced", "Alarms_ack", "Mimics_opened", "No_of_alarms"
]
special_variable = "No_of_procedures"
categorical_variables = ["Recovery_status", "Consequence", "Overall_performance"]
scenarios = ['S1', 'S2', 'S3']

# Initialize a list to hold all results for statistical tests
all_results = []

# Group comparisons
group_pairs = [('G1', 'G2'), ('G2', 'G3'), ('G3', 'G4')]

# Loop through each scenario
for scenario in scenarios:
    scenario_data = data[data['Scenario'] == scenario]
    
    # Numeric variable analysis    # Numeric variable analysis
    for variable in numeric_variables + [special_variable]:
        # Special handling for "No_of_procedures"
        if variable == special_variable and ('G3', 'G4') in group_pairs:
            continue


        # Statistical tests for numeric variables
        for group_pair in group_pairs:
            g1_data = scenario_data[scenario_data['Group'] == group_pair[0]][variable].dropna()
            g2_data = scenario_data[scenario_data['Group'] == group_pair[1]][variable].dropna()

            # Shapiro-Wilk test for normality
            sw_g1 = stats.shapiro(g1_data).pvalue
            sw_g2 = stats.shapiro(g2_data).pvalue

            # Levene's test for equality of variances
            levene_stat, levene_p = stats.levene(g1_data, g2_data)

            # Choose test based on normality and variance equality
            if sw_g1 > 0.05 and sw_g2 > 0.05:
                # Both distributions are normal and variances are equal
                t_stat, t_p = stats.ttest_ind(g1_data, g2_data,equal_var=levene_p > 0.05)
                test_used = 't-test'
            else:
                # Use non-parametric test
                wilcoxon_stat, wilcoxon_p = stats.mannwhitneyu(g1_data, g2_data, alternative='two-sided')
                test_used = 'Wilcoxon Rank-Sum Test'

            # Save the results for numeric variables
            all_results.append({
                'Variable': variable,
                'Scenario': scenario,
                'Group Comparison': f'{group_pair[0]} vs {group_pair[1]}',
                'Test Used': test_used,
                'Shapiro-Wilk G1': sw_g1,
                'Shapiro-Wilk G2': sw_g2,
                'Levene Test': levene_p,
                'Test Statistic': wilcoxon_stat if test_used == 'Wilcoxon Rank-Sum Test' else t_stat,
                'p-value': wilcoxon_p if test_used == 'Wilcoxon Rank-Sum Test' else t_p
            })

    # Categorical variable analysis with Chi-Squared test
    for variable in categorical_variables:
        for group_pair in group_pairs:
            # Prepare the contingency table
            contingency_table = pd.crosstab(scenario_data[scenario_data['Group'].isin(group_pair)][variable], 
                                             scenario_data[scenario_data['Group'].isin(group_pair)]['Group'])
            
            # Chi-Squared test
            chi2_stat, chi2_p, dof, _ = stats.chi2_contingency(contingency_table)
            
            # Save the results for categorical variables
            all_results.append({
                'Variable': variable,
                'Scenario': scenario,
                'Group Comparison': f'{group_pair[0]} vs {group_pair[1]}',
                'Test Used': 'Chi-Squared Test',
                'Chi2 Statistic': chi2_stat,
                'p-value': chi2_p,
                'Degrees of Freedom': dof
            })

# Convert all results to a DataFrame
results_df =np.round( pd.DataFrame(all_results),3)

# Print and save the results

results_df.to_csv('combined_statistical_tests_results.csv', index=False)



print("\n" + "="*60)
print("SUCCESS! All Statistical Test have been generated.")
print("The result can be found in the combined_statistical_tests_results.csv file")
print("="*60)
