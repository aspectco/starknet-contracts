%lang starknet
%builtins range_check

from starkware.cairo.common.uint256 import Uint256, uint256_add, uint256_mul
from contracts.lib.ShortString import (
    felt_to_ss_partial,
    felt_to_ss,
    uint256_to_ss_partial,
    uint256_to_ss
)

@view
func Test_felt_to_ss_partial{
        range_check_ptr
    }(input: felt) -> (running_total: felt, remainder: felt):
    let (running_total, remainder) = felt_to_ss_partial(input)
    return (running_total=running_total, remainder=remainder)
end


@view
func Test_felt_to_ss{
        range_check_ptr
    }(input: felt) -> (res_len: felt, res: felt*):
    let (res_len, res) = felt_to_ss(input)
    return (res_len=res_len, res=res)
end

@view
func Test_uint256_to_ss_partial{
        range_check_ptr
    }(input: Uint256) -> (running_total: felt, remainder: Uint256):
    let (running_total, remainder) = uint256_to_ss_partial(input)
    return (running_total=running_total, remainder=remainder)
end

@view
func Test_uint256_to_ss{
        range_check_ptr
    }(input: Uint256) -> (res_len: felt, res: felt*):
    let (res_len, res) = uint256_to_ss(input)
    return (res_len=res_len, res=res)
end

