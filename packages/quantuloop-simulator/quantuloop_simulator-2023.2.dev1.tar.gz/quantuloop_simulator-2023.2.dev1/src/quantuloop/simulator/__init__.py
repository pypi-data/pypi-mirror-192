from __future__ import annotations
from os import environ
# Copyright (C) 2023 Quantuloop - All rights reserved

from quantuloop.sparse import use_sparse
from quantuloop.dense import use_dense
from quantuloop.quest import use_quest


__all__ = ['use_sparse', 'use_dense', 'use_quest',
           'set_token', 'set_gpu_count', 'set_precision']


def set_token(token=None, file=None):
    """Set your Quantuloop token

    Args:
        token: token string.
        file: token file path.
    """
    if file is not None:
        with open(file, 'r') as file:
            token = file.read()
    environ['QULOOP_TOKEN'] = token


def set_gpu_count(gpu_count_hint: int | None):
    """Sets the maximum number of GPUs

    If set to 0 or None, simulation will use all available GPUs.
    """

    if gpu_count_hint is None:
        gpu_count_hint = 0

    environ['QULOOP_GPU'] = str(int(gpu_count_hint))


def set_precision(precision: int):
    """Sets the floating point precision used in the simulation

    Positive values are: 1 for single precision (float) and 2 for double precision.
    """

    environ['QULOOP_FP'] = str(int(precision))
