import os
import polars as pl
import pandas as pd
from main import read_data, calc_stats, create_viz, create_report


def test_read_data():
    df = read_data()
    # test that result is a df
    assert isinstance(df, pl.DataFrame) and not df.is_empty(), "Error reading data"
    print("Data loaded successfully.")


def test_calc_stats():
    # creating test df
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
    df = pl.DataFrame(data)

    # call calc_stats function
    stats_df = calc_stats(df)
    pl.Config.set_tbl_rows(50)
    print(stats_df)

    # assert function with polars
    def assert_value(column, metric, expected_value, tolerance=0.01):
        # Get the value for the specified column and metric
        actual_value = stats_df.filter(pl.col("column") == column).select(pl.col(metric)).to_numpy()[0][0]
        assert abs(actual_value - expected_value) <= tolerance, f"{metric} for {column} does not match. Expected: {expected_value}, Got: {actual_value}"
    
    # run assertions
    assert_value("popularity", "mean", 12.50)
    assert_value("duration_s", "median", 300.00)
    assert_value("energy", "std_dev", 0.24)
    assert_value("key", "mean", 2.50)
    assert_value("loudness", "median", -6.50)
    assert_value("tempo", "std_dev", 12.91)

    print("All assertions passed for calc_stats.")


def test_create_viz():
    df = read_data()
    create_viz(df)

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
