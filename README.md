# Intro to [polars](https://pola.rs)
A short demo to introduce the polars dataframe library.

# Getting started
1. Clone the repo and move into the folder

```shell
git clone https://github.com/rparkr/polars-intro.git
cd polars-intro
```

2. Create a virtual environment and install requirements. I recommend using [uv](https://docs.astral.sh/uv/), but you can also use Python's built-in `venv` module and `pip`:

    <details>
    <summary>Using <a href="https://docs.astral.sh/uv/">uv</a> </summary>

    ```shell
    uv venv
    uv pip install -e .
    ```

    </details>

    <details>
    <summary>Using `venv` and `pip`</summary>

    ```shell
    python -m venv .venv
    source .venv/bin/activate
    pip install -e .

    # Or:
    # pip install -r requirements.txt
    ```
    </details>

3. Run the app...
    ```shell
    marimo run polars_intro/polars_intro.py
    ```

4. Or edit the notebook:
    ```shell
    marimo edit polars_intro/polars_intro.py
    ```
