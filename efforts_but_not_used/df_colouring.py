import pandas as pd
import matplotlib.pyplot as plt


# We 'll try to do the equivalent of feqos so that we judge whether a new strategy is better or worse
# then take the data from the backtesting and compare them towards the previous golden strategy
# https://stackoverflow.com/questions/11623056/matplotlib-using-a-colormap-to-color-table-cell-background


# Sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 22],
        'Score': [85, 92, 78]}

df = pd.DataFrame(data)

# Create a table with colored cells
fig, ax = plt.subplots(figsize=(6, 3))
ax.axis('off')  # Hide axes

colors = [['#FFD700', '#98FB98', '#FFA07A']] * len(df)

ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center', cellColours=colors)

# Save the table as a PNG image
plt.savefig('colored_table.png', bbox_inches='tight', dpi=300)
plt.show()

print("Colored table saved as colored_table.png")