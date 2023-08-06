from pathlib import Path
from typing import Dict, Union
import h5py
import numpy as np
import pandas as pd


class Dataset:
    """The `Dataset` class is a base class for datasets used directly or indirectly for microsimulation models.
    A dataset defines a generation function to create it from other data, and this class provides common features
    like storage, metadata and loading."""

    name: str = None
    """The name of the dataset. This is used to generate filenames and is used as the key in the `datasets` dictionary."""
    label: str = None
    """The label of the dataset. This is used for logging and is used as the key in the `datasets` dictionary."""
    data_format: str = None
    """The format of the dataset. This can be either `Dataset.ARRAYS`, `Dataset.TIME_PERIOD_ARRAYS` or `Dataset.TABLES`. If `Dataset.ARRAYS`, the dataset is stored as a collection of arrays. If `Dataset.TIME_PERIOD_ARRAYS`, the dataset is stored as a collection of arrays, with one array per time period. If `Dataset.TABLES`, the dataset is stored as a collection of tables (DataFrames)."""
    file_path: Path = None
    """The path to the dataset file. This is used to load the dataset from a file."""

    # Data formats
    TABLES = "tables"
    ARRAYS = "arrays"
    TIME_PERIOD_ARRAYS = "time_period_arrays"

    _table_cache: Dict[str, pd.DataFrame] = None

    def __init__(self):
        # Setup dataset
        if self.file_path is None:
            raise ValueError(
                "Dataset file_path must be specified in the dataset class definition."
            )
        elif isinstance(self.file_path, str):
            self.file_path = Path(self.file_path)

        assert (
            self.name
        ), "You tried to instantiate a Dataset object, but no name has been provided."
        assert (
            self.label
        ), "You tried to instantiate a Dataset object, but no label has been provided."

        assert self.data_format in [
            Dataset.TABLES,
            Dataset.ARRAYS,
            Dataset.TIME_PERIOD_ARRAYS,
        ], "You tried to instantiate a Dataset object, but your data_format attribute is invalid."

        self._table_cache = {}

    def load(
        self, key: str = None, mode: str = "r"
    ) -> Union[h5py.File, np.array, pd.DataFrame, pd.HDFStore]:
        """Loads the dataset for a given year, returning a H5 file reader. You can then access the
        dataset like a dictionary (e.g.e Dataset.load(2022)["variable"]).

        Args:
            key (str, optional): The key to load. Defaults to None.
            mode (str, optional): The mode to open the file with. Defaults to "r".

        Returns:
            Union[h5py.File, np.array, pd.DataFrame, pd.HDFStore]: The dataset.
        """
        file = self.file_path
        if self.data_format in (Dataset.ARRAYS, Dataset.TIME_PERIOD_ARRAYS):
            if key is None:
                # If no key provided, return the basic H5 reader.
                return h5py.File(file, mode=mode)
            else:
                # If key provided, return only the values requested.
                with h5py.File(file, mode=mode) as f:
                    values = np.array(f[key])
                return values
        elif self.data_format == Dataset.TABLES:
            if key is None:
                # Non-openfisca datasets are assumed to be of the format (table name: [table], ...).
                return pd.HDFStore(file)
            else:
                if key in self._table_cache:
                    return self._table_cache[key]
                # If a table name is provided, return that table.
                with pd.HDFStore(file) as f:
                    values = f[key]
                self._table_cache[key] = values
                return values
        else:
            raise ValueError(
                f"Invalid data format {self.data_format} for dataset {self.label}."
            )

    def save(self, key: str, values: Union[np.array, pd.DataFrame]):
        """Overwrites the values for `key` with `values`.

        Args:
            key (str): The key to save.
            values (Union[np.array, pd.DataFrame]): The values to save.
        """
        file = self.file_path
        if self.data_format in (Dataset.ARRAYS, Dataset.TIME_PERIOD_ARRAYS):
            with h5py.File(file, "a") as f:
                # Overwrite if existing
                if key in f:
                    del f[key]
                f.create_dataset(key, data=values)
        elif self.data_format == Dataset.TABLES:
            with pd.HDFStore(file, "a") as f:
                f.put(key, values)
            self._table_cache = {}
        else:
            raise ValueError(
                f"Invalid data format {self.data_format} for dataset {self.label}."
            )

    def save_dataset(self, data) -> None:
        """Writes a complete dataset to disk.

        Args:
            data: The data to save.

        >>> example_data: Dict[str, Dict[str, Sequence]] = {
        ...     "employment_income": {
        ...         "2022": np.array([25000, 25000, 30000, 30000]),
        ...     },
        ... }
        >>> example_data["employment_income"]["2022"] = [25000, 25000, 30000, 30000]
        """
        file = self.file_path
        if self.data_format == Dataset.TABLES:
            for table_name, dataframe in data.items():
                self.save(table_name, dataframe)
        elif self.data_format == Dataset.TIME_PERIOD_ARRAYS:
            with h5py.File(file, "a") as f:
                for variable, values in data.items():
                    for time_period, value in values.items():
                        key = f"{variable}/{time_period}"
                        # Overwrite if existing
                        if key in f:
                            del f[key]
                        f.create_dataset(key, data=value)
        elif self.data_format == Dataset.ARRAYS:
            with h5py.File(file, "a") as f:
                for variable, value in data.items():
                    # Overwrite if existing
                    if variable in f:
                        del f[variable]
                    f.create_dataset(variable, data=value)

    def load_dataset(
        self,
    ):
        """Loads a complete dataset from disk.

        Returns:
            Dict[str, Dict[str, Sequence]]: The dataset.
        """
        file = self.file_path
        if self.data_format == Dataset.TABLES:
            with pd.HDFStore(file) as f:
                data = {table_name: f[table_name] for table_name in f.keys()}
        elif self.data_format == Dataset.TIME_PERIOD_ARRAYS:
            with h5py.File(file, "r") as f:
                data = {}
                for variable in f.keys():
                    data[variable] = {}
                    for time_period in f[variable].keys():
                        key = f"{variable}/{time_period}"
                        data[variable][time_period] = np.array(f[key])
        elif self.data_format == Dataset.ARRAYS:
            with h5py.File(file, "r") as f:
                data = {
                    variable: np.array(f[variable]) for variable in f.keys()
                }
        return data

    def generate(self):
        """Generates the dataset for a given year (all datasets should implement this method).

        Raises:
            NotImplementedError: If the function has not been overriden.
        """
        raise NotImplementedError(
            f"You tried to generate the dataset for {self.label}, but no dataset generation implementation has been provided for {self.label}."
        )

    @property
    def exists(self) -> bool:
        """Checks whether the dataset exists.

        Returns:
            bool: Whether the dataset exists.
        """
        return self.file_path.exists()

    def __getattr__(self, name):
        """Allows the dataset to be accessed like a dictionary.

        Args:
            name (str): The key to access.

        Returns:
            Union[np.array, pd.DataFrame]: The dataset.
        """
        return self.load(name)
