"""
Asynchronously download data used in this tutorial.
"""

import asyncio
import datetime as dt
from pathlib import Path
import urllib.parse
from zoneinfo import ZoneInfo


import httpx


# Files are published monthly, with a 2-month delay. For simplicity,
# I use a 3-month delay to ensure that the data is available.
def get_data_urls(year: int = None, **kwargs) -> list[str]:
    """Get the URLs for all months of Yellow Taxi data in a given year."""
    if not year:
        year = dt.date.today().year
    current_year = dt.date.today().year
    assert (year >= 2009) and (
        year <= current_year
    ), f"year must be >= 2009 and <= {current_year}, but {year} was given"
    end_month = 12
    if year == current_year:
        if dt.date.today().month <= 3:
            print(
                "The current year was requested, but data may not yet "
                f"be available. Using last year ({current_year - 1}) instead."
            )
            year = current_year - 1
        else:
            end_month = dt.date.today().month - 3
    data_urls = [
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-{month:0>2d}.parquet"
        for month in range(1, end_month + 1)
    ]
    return data_urls


async def download_taxi_data(
    urls: list[str] | None = None, save_dir: str = "data", **kwargs
) -> None:
    """
    Download NYC Yellow Cab taxi dataset to the "data/" directory in the current working directory.

    Parameters
    ----------
    urls: list of str
        The URLs for which data will be downloaded.

    save_dir: str
        The directory where the downloaded data will be saved.
        If a relative filepath is provided, this is assumed to be
        relative to the current working directory.

    kwargs: keyword-only arguments
        `year`: the year for which data will be downloaded,
            passed along to get_data_urls()

    Returns
    -------
    None
    """
    if not urls:
        urls = get_data_urls(year=kwargs.get("year"))
    # Ensure the urls variable is a list for consistency
    if isinstance(urls, str):
        urls = [urls]
    # Create the folder for saving the data
    if not save_dir:
        save_dir = "data"
    Path(save_dir).mkdir(parents=True, exist_ok=True)

    async def download_single_file(client, url, save_dir) -> str:
        """Download a file from a URL, save it, and return its filepath."""
        filepath = Path(save_dir) / Path(url).name
        with open(filepath, mode="ba" if not filepath.exists else "bw") as data_file:
            async with client.stream("GET", url) as response:
                async for chunk in response.aiter_bytes():
                    data_file.write(chunk)
        return filepath

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(
            *[download_single_file(client, url, save_dir) for url in urls]
        )
    total_files = len(urls)
    max_digits = len(str(total_files))
    for i, result in enumerate(results):
        print(
            f"{i+1:>0{max_digits}}/{total_files:>0{max_digits}} | Downloaded file: {result}"
        )


def download_weather_data(
    start_date: dt.date | None = None,
    end_date: dt.date | None = None,
    latitude: float = 40.7128,
    longitude: float = 74.006,
    time_zone: str | ZoneInfo = "America/New_York",
    save_dir: str = "data",
    filename: str = "weather.json",
) -> str:
    """
    Download hourly weather data from Open-Meteo.com

    Parameters
    ----------
    start_date: datetime.date
        The start date for historical weather data.
        If not set, the first day of the current year
        will be used if the current date is after the
        third month of the year, otherwise, the start
        date will be the first day of the previous year.
        This aligns the weather data to the NYC Yellow
        Cab Taxi dataset, which has a 2-month delay in
        availability (I use a 3-month delay as a buffer).

    end_date: datetime.date
        The end date for historical weather data.
        If not set, this defaults to the current date if
        the current date is after the third month of the
        year, otherwise it is the last day of the previous
        year.

    latitude: float
        The latitude (North/South) coordinate for the location
        of interest. Defaults to the coordinate for New York City.

    longitude: float
        The longitude (East/West) coordinate for the location
        of interest. Defaults to the coordinate for New York City.

    time_zone: str or ZoneInfo object, default = "America/New_York"
        The time zone in which the data will be returned. If set to
        an emptry string or None, then UTC will be used.

    save_dir: str, default = "data"
        The directory (relative to the current working directory)
        where the data will be saved.

    filename: str, default = "weather.json"

    Returns
    -------
    str: filepath to downloaded data

    Notes
    -----
    Data source: https://open-meteo.com/.  Open-Meteo's
    license permits non-commercial use for up to
    10,000 API calls per day. Since this repository is
    used [for educational purposes](https://open-meteo.com/en/terms), it qualifies as
    non-commercial use. This function uses the
    equivalent of 6-8 API calls because of its long
    time horizon. Please respect Open-Meteo's restrictions
    and do not repeatedly run this function beyond the
    limits set by Open-Meteo, including ensuring that
    your use of this API call is non-commercial.

    See also:
    - [Open-Meteo's terms of use](https://open-meteo.com/en/terms)
    - [Open-Meteo's license]()
    - [Open-Meteo's historical data API docs](https://open-meteo.com/en/docs/historical-weather-api)
    """
    today = dt.date.today()
    if not start_date:
        if today.month >= 3:
            start_date = dt.date(today.year, 1, 1)
        else:
            start_date = dt.date(today.year - 1, 1, 1)
    if not end_date:
        if today.month >= 3:
            end_date = today
        else:
            end_date = dt.date(today.year - 1, 12, 31)

    api_url = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={latitude}"
        f"&longitude={longitude}"
        f"&start_date={start_date}"  # must be ISO-8601: yyyy-mm-dd, i.e., %Y-%m-%d
        f"&end_date={end_date}"
        "&hourly=temperature_2m,weather_code,is_day"
    )
    if time_zone:
        tz_url_encoded = urllib.parse.quote(str(time_zone), safe="")
        api_url += f"&timezone={tz_url_encoded}"
    # Create the folder if it does not exist
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    filepath = Path(save_dir) / filename

    response = httpx.get(api_url)

    with open(filepath, mode="wt", encoding="utf8") as data_file:
        data_file.write(response.text)
    print(f"Saved weather data to: {filepath}")
    return str(filepath)


def download_weather_codes(save_dir: str = "data") -> str:
    """
    Download WMO weather interpretation codes from: https://gist.github.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c

    Parameters
    ----------
    save_dir: str, default = "data"
        The directory (relative to the current working directory)
        where the data will be saved.

    Returns
    -------
    str: filepath to downloaded data
    """
    url = "https://gist.githubusercontent.com/stellasphere/9490c195ed2b53c707087c8c2db4ec0c/raw/76b0cb0ef0bfd8a2ec988aa54e30ecd1b483495d/descriptions.json"
    filepath = Path(save_dir) / "weather_codes.json"

    response = httpx.get(url)

    with open(filepath, mode="wt", encoding="utf8") as data_file:
        data_file.write(response.text)
    print(f"Saved weather codes to: {filepath}")
    return str(filepath)


def download_all():
    asyncio.run(download_taxi_data())
    _ = download_weather_data()
    _ = download_weather_codes()


# Download data
if __name__ == "__main__":
    download_all()
