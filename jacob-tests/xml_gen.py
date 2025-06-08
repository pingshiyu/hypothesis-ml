from hypothesis import strategies as st, given, settings
from hypothesis._settings import Phase
from hypothesis.internal.conjecture.providers import AVAILABLE_PROVIDERS
from ml_provider import run_with_prng

# generator for square integers
@st.composite
def square_int(draw) -> int:
    i0 = draw(st.integers())
    # print(f"called with {i0}")
    return i0 ** 2

# generate some combination of credit card infos: card number + names + cvv
@st.composite
def card_number(draw) -> str:
    digits = []
    for i in range(16):
        digits.append(str(draw(st.integers(min_value=0, max_value=9))))
    return ''.join(digits)

@st.composite
def card_name(draw) -> str:
    first_name = draw(st.from_regex(r'[A-Z][a-z]+', fullmatch=True))
    surname = draw(st.from_regex(r'[A-Z][a-z]+', fullmatch=True))
    return f"{surname}, {first_name}"

@st.composite
def card_cvv(draw) -> str:
    digits = []
    for i in range(3):
        digits.append(str(draw(st.integers(min_value=0, max_value=9))))
    return ''.join(digits)

@st.composite
def card_info(draw) -> dict:
    return {
        'number': draw(card_number()),
        'name': draw(card_name()),
        'cvv': draw(card_cvv())
    }

# call the generators
@given(square_int())
def test_square_int(i):
    print(f"called with {i}")
    assert i >= 0
    assert i == int(i ** 0.5) ** 2

@given(card_info())
def test_card_info(info):
    print(f"called with {info}")
    assert len(info['number']) == 16
    assert len(info['cvv']) == 3
    assert len(info['name'].split(',')) == 2

if __name__ == '__main__':
    zero = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    one = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,100])
    verylong = bytearray([0] * 10 + [1] * 10)
    verylongz = bytearray([0] * 50)
    run_with_prng(verylong, test_square_int)
    run_with_prng(verylongz, test_square_int)
    # run_with_prng(verylong, test_square_int)
    # set_prng(one)
    # test_square_int()
    # test_card_info()