import marimo

__generated_with = "0.9.4"
app = marimo.App(
    app_title="Polars intro",
    layout_file="layouts/polars_intro.slides.json",
    css_file="custom.css",
)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Intro to [polars](https://pola.rs)

        A brief introduction to the incredible `polars` dataframe library.

        ![polars logo](https://raw.githubusercontent.com/pola-rs/polars-static/master/banner/polars_github_banner.svg)

        Created by: [Ryan Parker](https://github.com/rparkr), August 2024.
        """
    )
    return


@app.cell
async def __(mo):
    from pathlib import Path

    import polars as pl
    from polars_intro import download_data

    # Download data
    if not Path("data/").exists:
        mo.callout(kind="info", value="Downloading NYC Taxi and weather data")
        await download_data.download_data()
        download_data.download_weather_data()
    return Path, download_data, pl


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""
    # Data analysis in Python
    As an interpreted language with an easy-to-read syntax, Python is fantastic for data analysis, where rapid iteration enables exploration and accelerates development.

    Since its first release in 2008, [pandas](https://pandas.pydata.org/docs/) has been the de-facto standard for data analysis in Python, but in recent years other libraries have been created which offer distinct advantages. Some of those include:

    - [cuDF](https://docs.rapids.ai/api/cudf/stable/): GPU-accelerated dataframe operations with pandas API support
    - [modin](https://modin.readthedocs.io/en/stable/): pandas API running on distributed compute using [Ray](https://www.ray.io/) or [Dask](https://www.dask.org/) as a backend
    - [ibis](https://ibis-project.org/): dataframe library supporting dozens of backends (including pandas, polars, DuckDB, and many SQL databases)
    - [DuckDB](https://duckdb.org/): in-process database engine for running SQL queries on local or remote data
    - [temporian](https://temporian.readthedocs.io/en/stable/): efficient data processing for timeseries data
    - [polars](https://pola.rs/): ultra-fast dataframe library written in Rust
    - and others...
    """)
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Polars advantages
        - Easy to use
        - Parallelized across all CPU cores
        - Zero dependencies
        - Built on the Apache Arrow in-memory data format: enables zero-copy interoperability with other libraries (e.g., DuckDB, Snowflake)
        - Handles datasets larger than RAM
        - Powerful query optimizer
        - Fully compatible with scikit-learn, thanks to the [Dataframe Interchange Protocol](https://data-apis.org/dataframe-protocol/latest/)

        - <img src="https://www.rust-lang.org/static/images/rust-logo-blk.svg" width=30 style="display: inline; vertical-align: middle;"> written in [Rust](https://rust-lang.org), a compiled language that has experienced rapid adoption since its first stable release in 2015 thanks to its C/C++ performance, concurrency, and memory safety
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Key concepts
        
        Polars uses the Apache Arrow in-memory data format, which is column-oriented. The primary data structures for polars are Series and DataFrames, similar to pandas.
        
        - Apache Arrow supports many useful data types (many more than those which are supported by NumPy), so you can perform fast, vectorized operations on all kinds of data (nested JSON `structs`, strings, datetimes, etc.)
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Contexts
        In Polars, a _context_ refers to the data available to operate on.
        
        The primary contexts are:
        
        **Selection**:
        
        - `.select()`: choose a subset of columns and perform operations on them
        - `.with_columns()`: add to the columns already available
        
        **Filtering**:
        
        - `.filter()`: filter the data using boolean conditions on row values
        
        **Aggregation**:
        
        - `.group_by()`: perform aggregations on groups of values
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Expressions

        _Expressions_ are the operations performed in Polars, things like:

        - `.sum()`
        - `.len()`
        - `.mean().over()...`
        - `when().then().otherwise()`
        - `.str.replace()`
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Lazy vs. Eager mode
        - `scan_csv()` vs. `read_csv()`

        ### Recommendation: use Lazy mode
        - In Lazy mode, Polars will optimize the query plan
        """
    )
    return


@app.cell
def __(mo):
    mo.vstack(
        [
            mo.md(
                r"""
                # Plugin ecosystem
                You can create custom expressions to use in Polars, which will also be vectorized and run in parallel like standard Polars expressions. If there's an operation you'd like to run on your data, chances are someone has already implemented it and it's just a `pip install` away. Here are [some examples](https://docs.pola.rs/user-guide/expressions/plugins/#community-plugins)...
                """
            ),
            mo.accordion(
                {
                    "### [`polars_ds`](https://github.com/abstractqqq/polars_ds_extension)": (
                        r"""
                        Polars extension for data science tasks
                        
                        - A combination of functions and operations from scikit-learn, SciPy, and edit distance
                        - Polars is the only dependency (unless you want to create plots; that adds Plotly as a dependency)
                        - Can create bar plots within dataframe outputs (HTML `__repr__` in a notebook) -- like sparklines, and similar to what is available in pandas' advanced dataframe styling options
                        """
                    ),
                    "### [`polars_distance`](https://github.com/ion-elgreco/polars-distance)": (
                        r"""
                        Distance calculations (e.g., word similarity) in polars. Also includes haversine distance (lat/lon), cosine similarity, etc.
                        """
                    ),
                    "### [`polars_reverse_geocode`](https://github.com/MarcoGorelli/polars-reverse-geocode)": (
                        r"""
                        Offline reverse geocoding: find a city based on provided lat/lon; using an offline lookup table
                        """
                    ),
                    "### Tutorial: [how to create a polars plugin](https://marcogorelli.github.io/polars-plugins-tutorial/)": (
                        r"""
                        You can create your own plugin! This tutorial teaches you enough Rust to write a polars plugin, which can published to PyPI and installed by other Polars users.
                        """
                    ),
                }
            ),
        ]
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Final thoughts

        ## Upgrade weekly
        ⭐ Polars development [advances rapidly](https://github.com/pola-rs/polars/releases), so I recommend upgrading often (weekly) to get the latest features

        ## Try it out
        The best way to learn is by doing. Try using Polars any time you create a new notebook or start a new project.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        # Resources
        - [Polars user guide](https://docs.pola.rs/user-guide/migration/pandas/): fantastic guide to learning Polars alongside helpful explanations
        - [Coming from `pandas`](https://docs.pola.rs/user-guide/migration/pandas/): are you familiar with `pandas` and want to learn the differences you'll notice when switching to polars? This guide translates common concepts to help you.
          - [This series of articles from 2022](https://kevinheavey.github.io/modern-polars/) demonstrates some operations in pandas and polars, side-by-side. _Polars development advances rapidly, so many of the concepts covered in that series are already different. Still it will help you get a general feel for the flow of using Polars compared to pandas._
        - [Polars Python API](https://docs.pola.rs/api/python/stable/reference/index.html): detailed info on every expression, method, and function in Polars. I recommend browsing this list to get a feel for what Polars can do.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.vstack(
        [
            mo.md(r"""
    # Demo
    In this section, I demonstrate basic Polars usage on the NYC Taxi Yellow Cab dataset. You can find more information about that dataset on the [NYC Trip Record Data page](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).
    """),
            mo.accordion(
                {
                    "## Data dictionary (from the [PDF file published by NYC Trip Record Data](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf))": r"""
    1. **VendorID**: A code indicating the TPEP provider that provided the record. 1= Creative Mobile Technologies, LLC; 2= VeriFone Inc.
    2. **tpep_pickup_datetime**: The date and time when the meter was engaged
    3. **tpep_dropoff_datetime**: The date and time when the meter was disengaged
    4. **Passenger_count**: The number of passengers in the vehicle. This is a driver-entered value.
    5. **Trip_distance**: The elapsed trip distance in miles reported by the taximeter
    6. **PULocationID**: TLC Taxi Zone in which the taximeter was engaged
        - [See here](http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml) for a map of the TLC Taxi Zones
    7. **DOLocationID**: TLC Taxi Zone in which the taximeter was disengaged
    8. **RateCodeID**: The final rate code in effect at the end of the trip.
        - 1 = Standard rate
        - 2 = JFK
        - 3 = Newark
        - 4 = Nassau or Westchester
        - 5 = Negotiated fare
        - 6 = Group ride
    9. **Store_and_fwd_flag**: This flag indicates whether the trip record was held in vehicle memory before sending to the vendor, aka “store and forward,” because the vehicle did not have a connection to the server
        - Y = store and forward trip
        - N = not a store and forward trip
    10. **Payment_type**: A numeric code signifying how the passenger paid for the trip
        - 1 = Credit card
        - 2 = Cash
        - 3 = No charge
        - 4 = Dispute
        - 5 = Unknown
        - 6 = Voided trip
    11. **Fare_amount**: The time-and-distance fare calculated by the meter
    12. **Extra**: Miscellaneous extras and surcharges. Currently, this only includes the $0.50 and $1 rush hour and overnight charges.
    13. **MTA_tax**: $0.50 MTA tax that is automatically triggered based on the metered rate in use
    14. **Improvement_surcharge**: $0.30 improvement surcharge assessed trips at the flag drop. The improvement surcharge began being levied in 2015.
    15. **Tip_amount**: Tip amount – This field is automatically populated for credit card tips. Cash tips are not included.
    16. **Tolls_amount**: Total amount of all tolls paid in trip.
    17. **Total_amount**: The total amount charged to passengers. Does not include cash tips
    18. **Congestion_Surcharge**: Total amount collected in trip for NYS congestion surcharge.
    19. **Airport_fee**: $1.25 for pick up only at LaGuardia and John F. Kennedy Airports
    """
                }
            ),
        ]
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Lazy-load the data
        Polars can read Parquet files (local or hosted on a network), determine their schema (columns and data types), apply filter pushdowns, and download only the data that is needed for the operations being performed.
        """
    )
    return


@app.cell
def __(get_data_urls, pl):
    # Create a LazyFrame that will use the data from all the files specified above
    df = pl.scan_parquet(get_data_urls())
    return (df,)


@app.cell
def __(df):
    # Find out what columns are available and their data types
    df.collect_schema()

    # If this were a local Parquet file, you could get just the schema
    # without reading data:
    # pl.read_parquet_schema("path/to/a/local/file.parquet")
    return


@app.cell
def __():
    # Preview the first few rows.

    # This is a somewhat expensive operation, since all files will need to be
    # queried.
    # df.head().collect()

    # With an in-memory DataFrame, you can run: df.glimpse() for a more compact
    # view.
    return


@app.cell
def __(df, pl):
    # Find the average cost per trip, by month
    # Note that the operations below are performed in parallel across
    # all available CPU cores, and that only the data needed will be downloaded.
    # In this case, since I have filtered to 3 months, only those months of data
    # will be downloaded. Also notice that only 5 columns will be downloaded, since
    # those are the ones I have requested.
    query_plan = (
        df.filter(pl.col("tpep_pickup_datetime").dt.month() <= 3)
        .group_by(
            by=pl.col("tpep_pickup_datetime").dt.strftime("%Y-%m").alias("month")
        )
        .agg(
            num_trips=pl.len(),  # count the number of trips
            cost_per_trip=pl.col("total_amount").mean(),
            avg_passengers_per_trip=pl.col("passenger_count").mean(),
            avg_distance=pl.col("trip_distance").mean(),
            num_airport_trips=(pl.col("Airport_fee") > 0).sum(),
        )
    )

    # See what Polars will execute
    print(query_plan.explain())

    # You could also run this in streaming mode for memory-constrained systems
    # print(
    #     "\n",
    #     " Query plan with streaming mode ".center(80, "-"),
    #     query_plan.explain(streaming=True),
    #     sep="",
    # )
    return (query_plan,)


@app.cell
def __(query_plan):
    # Now, run the query. This uses ~150MB of data transfer.
    # Some options to .collect(): engine="cpu", streaming=False, background=False
    df_avg = query_plan.collect()

    df_avg
    return (df_avg,)


@app.cell
def __(pl):
    pl.read_parquet("data/yellow_tripdata_2024-01.parquet").head()
    return


@app.cell
def __():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
