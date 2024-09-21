import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import os
from fpdf import FPDF


def read_data():
    df = pl.read_csv("data/spotify.csv")
    df = df.with_columns((pl.col("duration_ms") / 1000).alias("duration_s"))
    df = df.drop("duration_ms")
    #print(df.head())
    return df


def calc_stats(df):
    numerical_columns = [
        "popularity",
        "duration_s",
        "explicit",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "time_signature"
    ]

    # initialize dict to store stats
    stats_dict = {
        "column": [],
        "mean": [],
        "median": [],
        "std_dev": []
    }

    # calculate stats for each column
    for col in numerical_columns:
        mean_value = round(df[col].mean(),2)
        median_value = round(df[col].median(),2)
        std_dev_value = round(df[col].std(),2)
        
        # store results to dict
        stats_dict["column"].append(col)
        stats_dict["mean"].append(mean_value)
        stats_dict["median"].append(median_value)
        stats_dict["std_dev"].append(std_dev_value)

    # convert dict to polars df (table format)
    stats_df = pl.DataFrame(stats_dict)
    # convert to pandas df
    stats_pd = stats_df.to_pandas()

    # save df as image
    fig, ax = plt.subplots(figsize=(12, len(stats_df) * 0.4))
    ax.axis("tight")
    ax.axis("off")
    # create table
    table = ax.table(
        cellText=stats_pd.values,
        colLabels=stats_pd.columns,
        cellLoc="center",
        loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(16)
    table.scale(1.5, 2.5)

    # save fig to folder
    fig.savefig("resources/stats_df.png", bbox_inches="tight", dpi=300)
    plt.close()
    print(stats_df)
    return stats_df


def create_viz(df):
    plt.figure(figsize=(8, 4))

    # first subplot: histogram of duration
    plt.subplot(1, 2, 1)
    sns.histplot(df["duration_s"], bins=100, kde=True)
    plt.title("Distribution of Track Duration")
    plt.xlabel("Duration (in seconds)")
    plt.xlim(0, 800)
    plt.ylabel("Frequency")
    plt.grid(True)

    # second subplot: scatterplot of loudness vs energy
    plt.subplot(1, 2, 2)
    sns.scatterplot(x="loudness", y="energy", data=df, s=20, alpha=0.3)
    plt.title("Song's Energy vs Volume")
    plt.xlabel("Loudness (in dB)")
    plt.ylabel("Energy")
    plt.grid(True)

    # save and output
    plt.tight_layout()
    plt.savefig("resources/plot.png", dpi=300, bbox_inches="tight")
    plt.show()


def create_report(csv_file):
    # read data and get info
    df = read_data()
    dataset_name = os.path.basename(csv_file)
    num_cols = df.width
    col_names = df.columns

    # generate stats and visualizations if not already saved
    if not os.path.exists("plot.png"):
        create_viz(df)
    if not os.path.exists("stats_df.png"):
        calc_stats(df)

    # create empty PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"Summary Report for {dataset_name}", ln=True, align="C")

    # data summary
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt=f"Dataset: {dataset_name}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Number of Columns: {num_cols}", ln=True, align="L")
    pdf.cell(200, 10, txt="Columns/Variables:", ln=True, align="L")
    col_names_str = ", ".join(col_names)

    # format
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=col_names_str)

    # summary stats
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Summary Statistics:", ln=True, align="L")
    pdf.image("resources/stats_df.png", x=10, y=None, w=180)

    # data viz
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, txt="Visualizations:", ln=True, align="L")
    pdf.image("resources/plot.png", x=10, y=None, w=180)

    # save report as pdf
    pdf_file = "spotify_report.pdf"
    pdf.output(pdf_file)

    print(f"Summary report written to {pdf_file}")
