import pandas as pd
from Data import Data as D
import matplotlib.pyplot as plt

# Load in the main data file
df, _ = D.getData()

# Test some data queries
amy = df[df['PlayerName'] == 'Amy']
fall24 = amy[amy['Season'] == 'Fall24']
# plt.plot(fall24['Week'], fall24['Player PPR'], label='Amy')
# plt.plot(fall24['Week'], fall24['Opponent PPR'], label='Opponent')
# plt.legend()
# plt.xlabel('Week')
# plt.ylabel('PPR')
# plt.title('PPR Fall 2024')
# plt.show()

# ppr over time
amy.sort_values(by=['Season Sort', 'Week'], inplace=True)
plt.plot(list(range(0, len(amy))), amy['Player PPR'], label='Amy')
plt.plot(list(range(0, len(amy))), amy['Opponent PPR'], label='Opponent')
plt.legend()
plt.xlabel('Week')
plt.ylabel('PPR')
plt.title('League PPR')
plt.show()