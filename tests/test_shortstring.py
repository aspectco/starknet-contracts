"""lib/ShortString.cairo test file."""
import pytest
import random
import sys

from utils.utils import str_to_felt, felt_to_str, uint256_to_int, uint256
from utils.generate import generate_random_felt_list, generate_random_uint256_list


"""Use global test contract instance."""
@pytest.fixture(scope="module")
async def test_shortstring(test_shortstring_factory):
    return await test_shortstring_factory()

@pytest.mark.asyncio
@pytest.mark.parametrize("test_felt", generate_random_felt_list())
async def test_felt_to_ss_partial(starknet, test_shortstring, test_felt):
    test_str = str(test_felt)
    expected_running_total_str = test_str[-31:]
    expected_remainder_str = test_str[:len(test_str)-31]
    if len(expected_remainder_str) == 0:
        expected_remainder_str = "0"

    # run function and decode results
    execution_info = await test_shortstring.Test_felt_to_ss_partial(test_felt).call()
    running_total = execution_info.result.running_total
    remainder = execution_info.result.remainder
    assert felt_to_str(running_total) == expected_running_total_str
    assert remainder == int(expected_remainder_str), "{} == {}".format(remainder, expected_remainder_str)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_felt", generate_random_felt_list())
async def test_felt_to_ss_full(starknet, test_shortstring, test_felt):
    test_str = str(test_felt)

    # Run function and decode results
    execution_info = await test_shortstring.Test_felt_to_ss(test_felt).call()
    res = execution_info.result.res
    final_res = ""
    for r in res:
        final_res += felt_to_str(r)

    assert final_res == test_str
    assert int(final_res) == test_felt


@pytest.mark.asyncio
@pytest.mark.parametrize("test_uint256", generate_random_uint256_list())
async def test_uint256_to_ss_partial(starknet, test_shortstring, test_uint256):
    test_uint256_value = uint256_to_int(test_uint256)
    test_uint256_str = str(test_uint256_value)
    expected_running_total_str = test_uint256_str[-31:]
    expected_remainder_str = test_uint256_str[:len(test_uint256_str)-31]
    if len(expected_remainder_str) == 0:
        expected_remainder_str = "0"

    # run function and decode results
    execution_info = await test_shortstring.Test_uint256_to_ss_partial(test_uint256).call()
    result = execution_info.result
    running_total = result.running_total
    remainder = uint256_to_int((result.remainder[0], result.remainder[1]))

    assert felt_to_str(running_total) == expected_running_total_str
    assert remainder == int(expected_remainder_str), "{} == {}".format(remainder, expected_remainder_str)


@pytest.mark.asyncio
@pytest.mark.parametrize("test_uint256", generate_random_uint256_list())
async def test_uint256_to_ss_full(starknet, test_shortstring, test_uint256):
    test_uint256_value = uint256_to_int(test_uint256)
    test_uint256_str = str(test_uint256_value)
    expected_running_total_str = test_uint256_str[-31:]
    expected_remainder_str = test_uint256_str[:len(test_uint256_str)-31]
    if len(expected_remainder_str) == 0:
        expected_remainder_str = "0"

    # Run function and decode results
    execution_info = await test_shortstring.Test_uint256_to_ss(test_uint256).call()
    res = execution_info.result.res
    final_res = ""
    for r in res:
        final_res += felt_to_str(r)

    assert final_res == test_uint256_str
    assert uint256(int(final_res)) == test_uint256

