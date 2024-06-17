import pandas as pd
import matplotlib.pyplot as plt

def color_cell(val, ref):
    if isinstance(val, float) and not isinstance(val, pd.Timestamp) and (isinstance(val, float) and not isinstance(ref, str)):
        print(f"Val {val} Ref {ref} Val {type(val)} Ref {type(ref)}")
        if val < ref:
            return 'green'
        elif val > ref:
            return 'red'
    else:
        print(f"Val {val} Ref {ref} Val {type(val)} Ref {type(ref)}")
    return 'yellow'


def color_all_cells(df_me):
    df_colored = df_me.copy()
    colours = []
    for index, row in df_colored.iterrows():
        inner_colors = ["yellow"] * len(df_colored.columns)  # Initialize with "yellow"
        print(f"len(inner_colors){len(inner_colors)}")
        print(f"len(columns){len(df_colored.columns)}")

        if row['source'] == "Test":
            filtered_row = df_colored[(df_colored['Name'] == row['Name']) & (df_colored['source'] == 'Reference')]
            for col in df_colored.columns:
                cell_value = row[col]
                color = color_cell(cell_value, filtered_row[col].iloc[0])
                print(color)
                inner_colors[df_colored.columns.get_loc(col)] = color
        colours.append(inner_colors)
    return colours


def create_coloured_plot(df_me):
    colors = color_all_cells(df_me)

    # Create a table with colored cells
    fig, ax = plt.subplots(figsize=(50, 30))
    ax.axis('off')  # Hide axes
    table = ax.table(cellText=df_me.values, colLabels=df_me.columns, cellLoc='center', loc='center', cellColours=colors)
    #table.auto_set_font_size(False)
    #table.set_fontsize(5)  # Increase font size
    # Save the table as a PNG image
    # Adjust the cell dimensions
    for (i, j), cell in table.get_celld().items():
        cell.set_height(0.12)
        cell.set_width(0.04)
    plt.savefig('colored_table.png', bbox_inches='tight', dpi=200)
    plt.title("Colored Plot Table (Test vs. Reference)")

    plt.show()

def merge_reference_with_test(df_test):
    df_reference = pd.read_csv('csvs/reference.csv')
    df_reference['source'] = 'Reference'
    df_test['source'] = 'Test'

    # Define a function to apply colors based on the comparison
    df_me = pd.concat([df_reference, df_test], ignore_index=True)
    df_me = df_me.sort_values(by=['Name', 'source'])
    df_me.drop("_trades", axis=1, inplace=True)
    df_me.drop(["_equity_curve", "Start", "End", "Duration"], axis=1, inplace=True)
    df_me.to_csv("csvs/df_merged.csv")

    create_coloured_plot(df_me)

