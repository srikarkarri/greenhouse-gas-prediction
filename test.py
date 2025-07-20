import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data = {'Models': ['LSTM', 'Linear Regression', 'Decision Trees'],
        'California': [0.01, 0.03, 0.04],
        'Texas': [0.02, 0.05, 0.06],
        'Florida': [0.015, 0.04, 0.045]}

df = pd.DataFrame(data).set_index('Models')

sns.heatmap(df, annot=True, cmap='Blues')
plt.title('RMSE Heatmap Across States and Models')
plt.ylabel('Models')
plt.xlabel('States')
plt.show()