import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the working directory to where your data is located
os.chdir("C:\\Users\\User\\Documents\\Local Send")
os.makedirs("Plot", exist_ok=True)

data_path = 'data.csv'
df_full = pd.read_csv(data_path)

# Filter the dataset to include G1, G2, G3, and G4
df_full = df_full[df_full['Group'].isin(['G1', 'G2', 'G3', 'G4'])]

# Mapping for nicer titles
title_mapping = {
    'Recovery_time': 'Recovery Time',
    'Reaction_time': 'Reaction Time',
    'Response_time': 'Response Time',
    'Accuracy': 'Accuracy',
    'Alarms_silenced': 'Alarms Silenced',
    'Alarms_ack': 'Alarms Acknowledged',
    'Mimics_opened': 'Mimics Opened',
    'No_of_procedures': 'Number of Procedures',
    'No_of_alarms': 'Number of Alarms',
    'Consequence': 'Consequence',
    'Overall_performance': 'Overall Performance'
}

def plot_box(df, column, title):
    # Create a new figure for each plot to avoid overlap with increased figure size
    plt.figure(figsize=(20, 10))  # Adjust the figure size as needed
    
    # Using seaborn for more complex plotting
    sns.boxplot(x='Scenario', y=column, hue='Group', data=df, palette="Set3", hue_order=['G1', 'G2', 'G3', 'G4'])
    
    # Set plot title and labels
    plt.title(title, fontsize=24)
    plt.xlabel('Scenario', fontsize=20)
    plt.ylabel(title_mapping.get(column, column), fontsize=20)
    
    # Show the plot
    plt.legend(title='Group', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=16, title_fontsize=20)
    plt.tight_layout()  # Adjust layout to not cut off legend    
    plt.savefig(f"Plot/{title}.png")
    #plt.show()

def plot_count(df, column, title):
    # Create a new figure for each plot to avoid overlap with increased figure size
    scenarios = df['Scenario'].unique()
    n_scenarios = len(scenarios)
    fig, axes = plt.subplots(1, n_scenarios, figsize=(20, 10), sharey=True)
    fig.suptitle(title, fontsize=24)
    
    # Using seaborn for more complex plotting
    for i, scenario in enumerate(scenarios):
        sns.countplot(ax=axes[i], x='Group', hue=column, data=df[df['Scenario'] == scenario], palette="Set3", hue_order=df[column].unique(), order=['G1', 'G2', 'G3', 'G4'])
        axes[i].set_title(f'Scenario {scenario}', fontsize=20)
        axes[i].set_xlabel('Group', fontsize=16)
        if i == 0:
            axes[i].set_ylabel('Count', fontsize=16)
        else:
            axes[i].set_ylabel('')
        axes[i].tick_params(axis='both', which='major', labelsize=14)
    
    # Show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust layout to not cut off legend    
    plt.savefig(f"Plot/{title}.png")
    #plt.show()

# List of continuous variables for which we need to create box plots
continuous_variables = ['Recovery_time', 'Reaction_time', 'Response_time', 'Accuracy', 'Alarms_silenced', 'Alarms_ack', 'Mimics_opened', 'No_of_procedures', 'No_of_alarms']

# Creating a box plot for each continuous variable with nicer titles
for variable in continuous_variables:
    nice_title = title_mapping.get(variable, variable)
    plot_box(df_full, variable, nice_title)

# List of categorical variables for which we need to create count plots
categorical_variables = ['Consequence', 'Overall_performance', 'Recovery_status']

# Creating a count plot for each categorical variable with nicer titles
for variable in categorical_variables:
    nice_title = title_mapping.get(variable, variable)
    plot_count(df_full, variable, f'Distribution of {nice_title} by Group and Scenario')

data_path = 'Simulator_error.csv'
df_errors = pd.read_csv(data_path)

# Filter the dataset to include G1, G2, G3, and G4
df_errors = df_errors[df_errors['Group'].isin(['G1', 'G2', 'G3', 'G4'])]

# Mapping for nicer titles
title_mapping = {
    'Error': 'Error'
}

# Creating a count plot for the 'Error' variable with a nicer title
plot_count(df_errors, 'Error', f'Distribution of Errors by Group and Scenario')


print("\n" + "="*60)
print("SUCCESS! All plots have been generated.")
print("The plots can be found in the 'Plot' folder.")
print("="*60)