import pandas as pd

should_reverse_obj = {
    "Exposure Time [%]": True,
    "Equity Final [$]": False,
    "Equity Peak [$]": False,
    "Return [%]": False,
    "Buy & Hold Return [%]": False,
    "Return (Ann.) [%]": False,
    "Volatility (Ann.) [%]": True,
    "Sharpe Ratio": False,
    "Sortino Ratio": False,
    "Calmar Ratio": "DROP",
    "Max. Drawdown [%]": True,
    "Avg. Drawdown [%]": True,
    "Max. Drawdown Duration": True,
    "Avg. Drawdown Duration": True,
    "# Trades": True,
    "Win Rate [%]": False,
    "Best Trade [%]": False,
    "Worst Trade [%]": True,
    "Avg. Trade [%]": False,
    "Max. Trade Duration": True,
    "Avg. Trade Duration": True,
    "Profit Factor": False,
    "Expectancy [%]": "DROP",
    "SQN": False,
    "_strategy": "",
    "Name": "",
    "source": "",
}


def get_cell_color(val, ref, reverse=False):
    positive_color = "green"
    negative_color = "red"
    if reverse:
        positive_color = "red"
        negative_color = "green"

    if (
        isinstance(val, float)
        and not isinstance(val, pd.Timestamp)
        and (isinstance(val, float) and not isinstance(ref, str))
    ):
        if val > ref:
            return positive_color
        elif val < ref:
            return negative_color
    return ""



def color_all_cells(df_me):
    df_colored = df_me.copy()
    colours = []
    for index, row in df_colored.iterrows():
        inner_colors = ["yellow"] * len(df_colored.columns)

        if row["source"] == "Test":
            filtered_row = df_colored[
                (df_colored["Name"] == row["Name"])
                & (df_colored["source"] == "Reference")
            ]

            for col in df_colored.columns:
                if col in should_reverse_obj and should_reverse_obj[col] != "DROP":
                    cell_value = row[col]
                    color = get_cell_color(
                        cell_value,
                        filtered_row[col].iloc[0],
                        should_reverse_obj[col],
                    )
                    inner_colors[df_colored.columns.get_loc(col)] = color

        colours.append(inner_colors)
    return colours


def create_colored_html_table(df_me):
    # Drop columns marked as "DROP"
    cols_to_drop = [
        col for col, action in should_reverse_obj.items() if action == "DROP"
    ]

    df_me = df_me.drop(columns=cols_to_drop)

    colors = color_all_cells(df_me)

    def apply_colors_to_html(row, colors):
        return ["background-color: {}".format(color) for color in colors[row.name]]

    styled_df = df_me.style.apply(apply_colors_to_html, colors=colors, axis=1)

    html_table = styled_df._repr_html_()
    with open("colored_table.html", "w") as f:
        f.write(html_table)

    print("HTML table created and saved as 'colored_table.html'.")


def merge_reference_with_test(df_test):
    df_reference = pd.read_csv("csvs/reference.csv")
    df_reference["source"] = "Reference"
    df_test["source"] = "Test"

    df_me = pd.concat([df_reference, df_test], ignore_index=True)
    df_me = df_me.sort_values(by=["Name", "source"])
    df_me.drop("_trades", axis=1, inplace=True)
    df_me.drop(["_equity_curve", "Start", "End", "Duration"], axis=1, inplace=True)
    df_me.to_csv("csvs/df_merged.csv")

    create_colored_html_table(df_me)


# Example usage
# df_test = pd.read_csv('csvs/test.csv')
# merge_reference_with_test(df_test)
