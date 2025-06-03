from typing import Optional
from hypothesis import strategies as st, given, settings
from hypothesis.core import ConjectureData
from hypothesis.internal.conjecture.providers import HypothesisProvider, BytestringProvider

from partition_tree import PNode

# one million zeros
ZERO_BYTE_STRING = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1])

# TODO: make a provider the same as the BytestringProvider but has a specified bytestring
# TODO: make it fix the bytestring to a certain value, to check that things work
# TODO: then add a seeting to settings, perhaps, to adjust the bytestring
class CustomBytestringProvider(BytestringProvider):
    def __init__(
        self, 
        conjecturedata: Optional["ConjectureData"], 
        /, *, 
        input_bytes: bytes = ZERO_BYTE_STRING,
        verbose: bool = True
        ):
        super().__init__(conjecturedata, bytestring=input_bytes)
        self.partitions = PNode()
        self.current_partition = self.partitions
        self.verbose = verbose

    def span_start(self, label, /):
        self.current_partition = self.current_partition.down(label)
        if self.verbose:
            print("span_start", label)
            print(f"{self.partitions}")
            print(f"current: {self.current_partition}")

    def span_end(self, discard, /):
        self.current_partition = self.current_partition.up()
        if self.verbose:
            print("span_end")
            print(f"{self.partitions}")

    def draw_integer(self, *args, **kwargs):
        drawn = super().draw_integer(*args, **kwargs)
        if self.verbose:
            print(f"draw_integer({args} {kwargs}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_string(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_string(intervals, min_size=min_size, max_size=max_size)
        if self.verbose:
            print(f"draw_string({intervals}, {min_size}, {max_size}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_bytes(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_bytes(intervals, min_size=min_size, max_size=max_size)
        if self.verbose:
            print(f"draw_bytes({intervals} {min_size} {max_size}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_float(self, *args, **kwargs):
        drawn = super().draw_float(*args, **kwargs)
        if self.verbose:
            print(f"draw_float({args} {kwargs}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_boolean(self, p = 0.5):
        drawn = super().draw_boolean(p)
        if self.verbose:
            print(f"draw_boolean({p}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

@given(st.integers())
# @settings(backend="my_provider", database=None)
def f(n):
    pass