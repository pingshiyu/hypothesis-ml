from typing import Optional
from hypothesis import strategies as st, given, settings
from hypothesis.core import ConjectureData
from hypothesis.internal.conjecture.providers import HypothesisProvider

from partition_tree import PNode

class MyProvider(HypothesisProvider):

    def __init__(self, conjecturedata: Optional["ConjectureData"], /):
        super().__init__(conjecturedata)
        self.partitions = PNode()
        self.current_partition = self.partitions

    def span_start(self, label, /):
        self.current_partition = self.current_partition.down()
        print("span_start", label)
        print(f"\t{self.partitions}")

    def span_end(self, discard, /):
        self.current_partition = self.current_partition.up()
        print("span_end")
        print(f"\t{self.partitions}")

    def draw_integer(self, *args, **kwargs):
        drawn = super().draw_integer(*args, **kwargs)
        print(f"draw_integer({args} {kwargs}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_string(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_string(intervals, min_size=min_size, max_size=max_size)
        print(f"draw_string({intervals}, {min_size}, {max_size}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_bytes(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_bytes(intervals, min_size=min_size, max_size=max_size)
        print(f"draw_bytes({intervals} {min_size} {max_size}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_float(self, *args, **kwargs):
        drawn = super().draw_float(*args, **kwargs)
        print(f"draw_float({args} {kwargs}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

    def draw_boolean(self, p = 0.5):
        drawn = super().draw_boolean(p)
        print(f"draw_boolean({p}) = {drawn}")
        self.current_partition.add_value(drawn)
        return drawn

@given(st.integers())
# @settings(backend="my_provider", database=None)
def f(n):
    pass