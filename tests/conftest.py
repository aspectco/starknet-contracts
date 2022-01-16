import pytest
import asyncio

from starkware.starknet.testing.starknet import Starknet
from utils.utils import str_to_felt, str_to_felt_array
from utils.constants import FPATH_TEST_SHORTSTRING, FPATH_ERC721, FPATH_ACCOUNT, ERC721_DEFAULT_TOKEN_URI
from utils.Signer import get_random_signer


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.new_event_loop()

"""Use global starknet instance."""
@pytest.fixture(scope="module")
async def starknet():
    return await Starknet.empty()

@pytest.fixture(scope="module")
async def account_factory(starknet):
    async def build(signer=None):
        if signer is None:
            signer = get_random_signer()
        account = await starknet.deploy(
            FPATH_ACCOUNT,
            constructor_calldata=[signer.public_key]
        )
        return account, signer
    return build

@pytest.fixture(scope="module")
async def erc721_factory(starknet):
    async def build(account, name=str_to_felt("Oasis"), symbol=str_to_felt("OASIS"), token_uri=ERC721_DEFAULT_TOKEN_URI):
        token_uri_felt_array = str_to_felt_array(token_uri)
        erc721 = await starknet.deploy(
            FPATH_ERC721,
            constructor_calldata=[name, symbol, account.contract_address, len(token_uri_felt_array), *token_uri_felt_array],
        )
        return erc721
    return build

@pytest.fixture(scope="module")
async def test_shortstring_factory(starknet):
    async def build():
        return await starknet.deploy(
            FPATH_TEST_SHORTSTRING,
            constructor_calldata=[],
        )
    return build

