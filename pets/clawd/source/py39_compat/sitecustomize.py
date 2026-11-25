"""Provide Python 3.10 zip(strict=...) to the existing Pillow Python 3.9 venv."""

import builtins
import itertools


_original_zip = builtins.zip


def _zip_with_strict(*iterables, strict=False):
    if not strict:
        return _original_zip(*iterables)

    def _checked():
        iterators = [iter(value) for value in iterables]
        sentinel = object()
        while True:
            values = [next(iterator, sentinel) for iterator in iterators]
            if all(value is sentinel for value in values):
                return
            if any(value is sentinel for value in values):
                raise ValueError("zip() argument lengths differ")
            yield tuple(values)

    return _checked()


builtins.zip = _zip_with_strict

if not hasattr(itertools, 'pairwise'):
    def _pairwise(iterable):
        first, second = itertools.tee(iterable)
        next(second, None)
        return _original_zip(first, second)
    itertools.pairwise = _pairwise
