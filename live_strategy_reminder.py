import time
import winsound  # For Windows; use pygame for cross-platform support
from helpers import fetch_latest_data, fill_with_ta, check_crossover
from helpers import Momentum


def main():
    previous = Momentum.DOWNWARD
    while True:
        symbols_list = ['ARM']
        df = fetch_latest_data(symbols_list)
        sma_value = fill_with_ta(df)  # Adjust with your data
        crossover_status = check_crossover(df)

        if crossover_status != previous:
            # Trigger the beep sound (implement this part)
            print(f"Momentum has swifted! We now have an {crossover_status} momentum for {symbols_list[0]}")
            previous = crossover_status
            winsound.Beep(1000, 500)  # Example beep sound

        time.sleep(60)  # Sleep for 1 minute


if __name__ == "__main__":
    main()
