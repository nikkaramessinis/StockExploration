import os
import webbrowser

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
                        filtered_row[col].iloc[0] if not filtered_row.empty else None,
                        should_reverse_obj[col],
                    )
                    inner_colors[df_colored.columns.get_loc(col)] = color

        colours.append(inner_colors)
    return colours


def calculate_average(df):
    averages = []

    for source_value in df["source"].unique():
        source_df = df[df["source"] == source_value]
        source_avg = {}

        for col in df.columns:
            if col in ["_strategy", "Name", "source"]:
                continue  # Skip these columns for averaging

            values = source_df[col].replace("nan", pd.NA)

            if values.dtype == "object":
                # For non-numeric columns, use mode if possible, otherwise 'N/A'
                mode = values.mode()
                source_avg[col] = mode.iloc[0] if not mode.empty else "N/A"
            else:
                # For numeric columns, calculate mean, ignoring NAs
                mean = values.mean()
                source_avg[col] = mean if pd.notna(mean) else "N/A"

        source_avg["source"] = f"Average ({source_value})"
        source_avg["Name"] = f"Average {source_value}"
        source_avg["_strategy"] = ""

        averages.append(source_avg)

    return pd.DataFrame(averages)


def create_colored_html_table(df_me):
    cols_to_drop = [
        col for col, action in should_reverse_obj.items() if action == "DROP"
    ]
    df_me = df_me.drop(columns=cols_to_drop)

    colors = color_all_cells(df_me)

    averages = calculate_average(df_me)

    # Ensure averages DataFrame has the same columns as df_me
    for col in df_me.columns:
        if col not in averages.columns:
            averages[col] = pd.NA

    # Reorder columns in averages to match df_me
    averages = averages[df_me.columns]

    df_me = pd.concat([df_me, averages], ignore_index=True)

    # Reorder columns to move source, Name, and _strategy to the left
    left_columns = ["source", "Name", "_strategy"]
    other_columns = [col for col in df_me.columns if col not in left_columns]
    df_me = df_me[left_columns + other_columns]

    def apply_colors_to_html(row, colors):
        try:
            return ["background-color: {}".format(color) for color in colors[row.name]]
        except IndexError:
            return [""] * len(row)

    styled_df = df_me.style.apply(apply_colors_to_html, colors=colors, axis=1)

    # Hide the index when generating the HTML
    styled_df = styled_df.hide(axis="index")

    html_table = styled_df.to_html()

    # Get the absolute path for the HTML file
    html_path = os.path.abspath("colored_table.html")

    with open(html_path, "w") as f:
        f.write(html_table)

    print(f"HTML table created and saved as '{html_path}'.")
    return html_path


def merge_reference_with_test(df_test):
    df_reference = pd.read_csv("csvs/reference.csv")
    df_reference["source"] = "Reference"
    df_test["source"] = "Test"

    df_me = pd.concat([df_reference, df_test], ignore_index=True)
    df_me = df_me.sort_values(by=["Name", "source"])
    df_me.drop("_trades", axis=1, inplace=True)
    df_me.drop(["_equity_curve", "Start", "End", "Duration"], axis=1, inplace=True)
    df_me.to_csv("csvs/df_merged.csv")

    html_file = create_colored_html_table(df_me)
    # Open the HTML file in the default web browser
    webbrowser.open("file://" + html_file)
