# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


import multiprocessing

from .distribution import (
    single_process,
    joblib_wrapper,
    multiprocessing_wrapper,
)
from .process import _process_


def proxy(kwargs):
    return _process_(**kwargs)


dist_dict = {
    "joblib": (joblib_wrapper, _process_),
    "multiprocessing": (multiprocessing_wrapper, proxy),
}


def _get_distribution(distribution):
    if hasattr(distribution, "__call__"):
        return (distribution, _process_), {}

    elif isinstance(distribution, dict):
        dist_key = list(distribution.keys())[0]
        dist_paras = list(distribution.values())[0]

        return dist_dict[dist_key], dist_paras

    elif isinstance(distribution, str):
        return dist_dict[distribution], {}


def run_search(search_processes_infos, distribution, n_processes):
    process_infos = list(search_processes_infos.values())

    if n_processes == "auto":
        n_processes = len(process_infos)

    if n_processes == 1:
        results_list = single_process(_process_, process_infos)
    else:
        (distribution, process_func), dist_paras = _get_distribution(distribution)

        results_list = distribution(
            process_func, process_infos, n_processes, **dist_paras
        )

    return results_list
