from pathlib import Path

import numpy as np
import pandas as pd


def load_un_data(
    raw_data_dir,
    interim_data_dir,
    un_data_filename="un_energy_data.csv",
    file_prefix="all_energy_statistics",
    first_suffix=1,
    force_refresh=False,
):
    """
    Returns combined energy data as a pandas DataFrame; if necessary, compiles combined .csv from several raw files.

    If no existing combined data file exists (or force_refresh = True): combines .csv files in a given directory
    that match an input prefix-suffix convention; returns as a DataFrame and saves the combined file to the interim
    data directory.

    Parameters
    ----------
    raw_data_dir : str / pathlib.PosixPath
        The path to the directory containing all .csv files to be combined.
    interim_data_dir : str / pathlib.PosixPath
        The path to the directory where combined .csv file will be saved.
    un_data_filename : str
        The filename for the combined energy data .csv file;
        default value = 'un_energy_data.csv'.
    file_prefix : str
        The consistent filename prefix used to identify those .csv files to be combined;
        default value = 'all_energy_statistics'.
    first_suffix : int / str
        The numeric suffix found in the first .csv's filename (function assumes numerically ordered filenames);
        default value = 1. The function assumes that only this file contains column titles and that column order
        in all subsequent files is identical to that of the first file.
    force_refresh : bool
        If True, forces the function to compile a new combined .csv file from the constituent raw files;
        default value = False

    Returns
    -------
    combined_df : pandas.DataFrame
        A pandas DataFrame containing data from all .csv files matching the convention defined via prefix and
        suffix arguments.

    """
    combined_file_path = Path(interim_data_dir) / un_data_filename

    if not combined_file_path.is_file():
        print(
            f"No existing combined data found at: {combined_file_path}\n"
            f"Attempting to combine split data from: {raw_data_dir}...\n"
        )
        combined_df = combine_split_data(
            raw_data_dir, file_prefix=file_prefix, first_suffix=first_suffix
        )  # execute code to pre-process data and save to the interim directory
        print(f"Saving combined data set to: {combined_file_path}\n")
        combined_df.to_csv(combined_file_path, index=False)
    elif force_refresh:
        print(
            f"FORCED DATA REFRESH\n"
            f"Attempting to combine split data from: {raw_data_dir}...\n"
        )
        combined_df = combine_split_data(
            raw_data_dir, file_prefix=file_prefix, first_suffix=first_suffix
        )  # execute code to pre-process data and save to the interim directory
        print(f"Saving new combined data set to: {combined_file_path}\n")
        combined_df.to_csv(combined_file_path, index=False)
    else:
        print(f"Loading combined data from {interim_data_dir}...")
        combined_df = pd.read_csv(combined_file_path)

    return combined_df


def combine_split_data(raw_data_dir, file_prefix, first_suffix):
    """
    Combines .csv files in a given directory that match an input prefix-suffix convention; returns as a DataFrame.

    Parameters
    ----------
    raw_data_dir : str / pathlib.PosixPath
        The path to the directory containing all .csv files to be combined.
    file_prefix : str
        The consistent filename prefix used to identify those .csv files to be combined;
        default value = 'all_energy_statistics'.
    first_suffix : int / str
        The numeric suffix found in the first .csv's filename (function assumes numerically ordered filenames);
        default value = 1. The function assumes that only this file contains column titles and that column order
        in all subsequent files is identical to that of the first file.

    Returns
    -------
    combined_df : pandas.DataFrame
        A pandas DataFrame containing data from all .csv files matching the convention defined via prefix and
        suffix arguments.

    Raises
    ------
    ValueError
        Raised when the initial .csv file cannot be found based on input 'raw_data_dir', 'file_prefix' and 'first_suffix'.

    """
    indv_files = []
    live_suffix = int(first_suffix)
    while True:
        try:
            live_filename = f"{file_prefix}{live_suffix}.csv"
            live_path = raw_data_dir / live_filename
            if len(indv_files) == 0:
                first_file = pd.read_csv(live_path, header=0)
                column_titles = first_file.columns.to_list()
                indv_files.append(first_file)
            else:
                subsequent_file = pd.read_csv(live_path, header=0, names=column_titles)
                indv_files.append(subsequent_file)
            live_suffix += 1
        except FileNotFoundError as err:
            if len(indv_files) == 0:
                raise ValueError(
                    f"No initial .csv file found at: {live_path}\n"
                    f"Please check the 'raw_data_dir', 'file_prefix' and 'first_suffix' arguments."
                ) from err
            else:
                print(f"Successfully combined {len(indv_files)} files.")
                break

    combined_df = pd.concat(indv_files, axis="index", ignore_index=True)

    return combined_df
