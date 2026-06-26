from collections import Counter
from typing import Any

from .configuration import Configuration
from .dict_configuration import DictConfiguration

__all__ = ["MergedConfiguration"]


def merge(*args: Any) -> Any:
    assert len(args) > 0

    if all(arg is None for arg in args):
        return None

    valid_args = [arg for arg in args if arg is not None]

    first_valid_entry = valid_args[0]
    assert all(isinstance(d, type(first_valid_entry)) for d in valid_args)

    if isinstance(first_valid_entry, list):
        return [e for d in valid_args for e in d]
    if isinstance(first_valid_entry, dict):
        count_fields = Counter([k for d in valid_args for k in d.keys()])

        # merge fields that occur in multiple dicts
        overlapping_fields = [k for k, v in count_fields.items() if v > 1]
        merged_overlapping_fields = {
            k: merge(*[d[k] for d in valid_args if k in d]) for k in overlapping_fields
        }

        # collect fields that occur in only one dict
        non_overlapping_fields = [k for k, v in count_fields.items() if v == 1]
        merged_non_overlapping_fields = {
            k: v for d in valid_args for k, v in d.items() if k in non_overlapping_fields
        }

        return {
            **merged_non_overlapping_fields,
            **merged_overlapping_fields,
        }
    else:
        # merge all configurations starting from the first one
        # --> last configuration has the highest priority
        return valid_args[-1]


class MergedConfiguration(DictConfiguration):
    def __init__(self, *configs: Configuration):
        super().__init__(merge(*[c._get_dict() for c in configs]))
