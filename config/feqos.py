import pandas as pd

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
                inner_colors[df_colored.columns.get_loc(col)] = color
        colours.append(inner_colors)
    return colours


def create_colored_html_table(df_me):
    colors = color_all_cells(df_me)

    # Convert DataFrame to HTML with styles
    def apply_colors_to_html(row, colors):
        return ['background-color: {}'.format(color) for color in colors[row.name]]
    
    styled_df = df_me.style.apply(apply_colors_to_html, colors=colors, axis=1)
    
    # Save the table as an HTML file
    html_table = styled_df._repr_html_()
    with open('colored_table.html', 'w') as f:
        f.write(html_table)

    print("HTML table created and saved as 'colored_table.html'.")


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

    create_colored_html_table(df_me)

# Example usage
# df_test = pd.read_csv('csvs/test.csv')
# merge_reference_with_test(df_test)
