from typing import Optional
from hypothesis import strategies as st, given, settings
from hypothesis._settings import Phase
from hypothesis.core import ConjectureData
from hypothesis.internal.conjecture.providers import BytestringProvider, AVAILABLE_PROVIDERS

from partition_tree import PNode

AVAILABLE_PROVIDERS["bytestring"] = "ml_provider.CustomBytestringProvider"

# one million zeros
ZERO_BYTE_STRING = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

class CustomBytestringProvider(BytestringProvider):
    def __init__(
        self, 
        conjecturedata: Optional["ConjectureData"], 
        /, *, 
        input_bytes: bytes = ZERO_BYTE_STRING,
        verbose: bool = True
        ):
        super().__init__(conjecturedata, bytestring=input_bytes)
        self.verbose = verbose
        self.partitions = PNode()
        self.current_partition = self.partitions
        self.start_fresh = True

    def show_state(self):
        print(f"overall:\n{self.partitions}\n")
        print(f"current:\n{self.current_partition}\n")

    def span_start(self, label, /):
        if self.start_fresh:
            print("## starting fresh.")
            self.partitions._reset()
            self.current_partition = self.partitions
            self.start_fresh = False
        self.current_partition = self.current_partition.down(label)
        if self.verbose:
            print("## span_start", label)
            self.show_state()

    def span_end(self, discard, /):
        self.current_partition = self.current_partition.up()
        if self.verbose:
            print("## span_end")
            self.show_state()
        if self.current_partition.parent is None:
            # print the partition if we finished construction the tree (when we close out the final level)
            print("associated generation tree:")
            print(self.partitions)
            self.start_fresh = True

    def draw_integer(self, *args, **kwargs):
        drawn = super().draw_integer(*args, **kwargs)
        self.current_partition.add_value(drawn)
        if self.verbose:
            print(f"## draw_integer({args} {kwargs}) = {drawn}")
            self.show_state()
        return drawn

    def draw_string(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_string(intervals, min_size=min_size, max_size=max_size)
        self.current_partition.add_value(drawn)
        if self.verbose:
            print(f"## draw_string({intervals}, {min_size}, {max_size}) = {drawn}")
            self.show_state()
        return drawn

    def draw_bytes(self, intervals, *, min_size = 0, max_size = ...):
        drawn = super().draw_bytes(intervals, min_size=min_size, max_size=max_size)
        self.current_partition.add_value(drawn)
        if self.verbose:
            print(f"## draw_bytes({intervals} {min_size} {max_size}) = {drawn}")
            self.show_state()
        return drawn

    def draw_float(self, *args, **kwargs):
        drawn = super().draw_float(*args, **kwargs)
        self.current_partition.add_value(drawn)
        if self.verbose:
            print(f"## draw_float({args} {kwargs}) = {drawn}")
            self.show_state()
        return drawn

    def draw_boolean(self, p = 0.5):
        drawn = super().draw_boolean(p)
        self.current_partition.add_value(drawn)
        if self.verbose:
            print(f"## draw_boolean({p}) = {drawn}")
            self.show_state()
        return drawn
    
def run_with_prng(prng: bytearray, test):
    return settings(
        backend="bytestring", 
        backend_kwargs={"input_bytes": prng, "verbose": False}, 
        phases=[Phase.generate], 
        max_examples=1, 
        derandomize=True)(test)()