"""token/ERC721.cairo test file."""
import pytest
from urllib.parse import urljoin

from utils.utils import str_to_felt_array, felt_to_str, uint256_to_int
from utils.generate import generate_random_uint256_list
from utils.constants import ERC721_DEFAULT_TOKEN_URI

"""Use global erc721 contract instance."""
@pytest.fixture(scope="module")
async def setup_erc721(erc721_factory, account_factory):
    account, signer = await account_factory()
    erc721 =  await erc721_factory(account)
    return erc721, account, signer

"""Use global account contract instance."""
@pytest.fixture(scope="module")
async def setup_account(account_factory):
    return await account_factory()

@pytest.mark.asyncio
@pytest.mark.parametrize("token_id", generate_random_uint256_list())
async def test_erc721_token_uri(starknet, setup_erc721, setup_account, token_id):
    erc721, erc721_account, erc721_signer = setup_erc721
    account, signer = setup_account

    await erc721_signer.send_transaction(erc721_account, erc721.contract_address, "mint", [
        account.contract_address, token_id
    ])

    execution_info = await erc721.tokenURI(token_id).call()

    token_uri = ""
    for tu in execution_info.result.token_uri:
        token_uri += felt_to_str(tu)
    expected_token_uri = urljoin(ERC721_DEFAULT_TOKEN_URI, str(uint256_to_int(token_id)))
    assert token_uri == expected_token_uri

    return

    await erc721.mint(123, token_id).invoke()
    execution_info = await erc721.tokenURI(token_id).call()

    token_uri = ""
    for tu in execution_info.result.token_uri:
        token_uri += felt_to_str(tu)
    expected_token_uri = urljoin(ERC721_DEFAULT_TOKEN_URI, str(uint256_to_int(token_id)))
    assert token_uri == expected_token_uri

