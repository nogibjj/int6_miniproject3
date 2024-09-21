import os
import pandas as pd
from main import read_data, calc_stats, create_viz, create_report

def test_read_data():
    df = read_data()

    # Assert that the result is a DataFrame
    assert isinstance(df, pd.DataFrame) and not df.empty, "Error reading data"


def test_calc_stats():
    # Create test df
    data = {
        "popularity": [5, 10, 15, 20],
        "duration_s": [120, 240, 360, 480],
        "explicit": [0, 1, 0, 1],
        "danceability": [0.5, 0.6, 0.7, 0.8],
        "energy": [0.3, 0.6, 0.9, 0.6],
        "key": [1, 2, 3, 4],
        "loudness": [-5, -6, -7, -8],
        "mode": [1, 0, 1, 0],
        "speechiness": [0.04, 0.05, 0.06, 0.07],
        "acousticness": [0.1, 0.2, 0.3, 0.4],
        "instrumentalness": [0.0, 0.1, 0.2, 0.3],
        "liveness": [0.2, 0.3, 0.4, 0.5],
        "valence": [0.3, 0.4, 0.5, 0.6],
        "tempo": [100, 110, 120, 130],
        "time_signature": [4, 4, 3, 3],
    }
    df = pd.DataFrame(data)

    # Call the function to calculate stats
    stats_df = calc_stats(df)
    print(stats_df)

    # Testing values
    assert round(stats_df.at["popularity", "mean"], 2) == 12.50, "Mean popularity does not match"
    assert round(stats_df.at["duration_s", "median"], 2) == 300.00, "Median duration_s does not match"
    assert round(stats_df.at["energy", "std_dev"], 2) == 0.24, "Standard deviation of energy does not match"
    assert round(stats_df.at["key", "mean"], 2) == 2.50, "Mean key does not match"
    assert round(stats_df.at["loudness", "median"], 2) == -6.50, "Median loudness does not match"
    assert round(stats_df.at["tempo", "std_dev"], 2) == 12.91, "Standard deviation of tempo does not match"

    print("All assertions passed for calc_stats.")

def test_create_viz():
    df = read_data()
    create_viz(df)
    print()

    # verify file was created and not empty
    assert os.path.exists("resources/plot.png"), "The plot.png file does not exist."
    assert os.path.getsize("resources/plot.png") > 0, "The plot.png file is empty."

    print("All assertions passed for test_create_viz.")

def test_generate_report():
    create_report("data/spotify.csv")

if __name__ == "__main__":
    test_read_data()
    test_calc_stats()
    test_create_viz()
    test_generate_report()