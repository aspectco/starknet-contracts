"""Utility for sending signed transactions to an Account on Starknet."""
import random

from starkware.crypto.signature.signature import private_to_stark_key, sign
from starkware.starknet.public.abi import get_selector_from_name
from starkware.cairo.common.hash_state import compute_hash_on_elements

class Signer():
    """
    Utility for sending signed transactions to an Account on Starknet.

    Parameters
    ----------

    private_key : int

    Examples
    ---------
    Constructing a Singer object

    >>> signer = Signer(1234)

    Sending a transaction

    >>> await signer.send_transaction(account,
                                      account.contract_address,
                                      'set_public_key',
                                      [other.public_key]
                                     )

    """

    def __init__(self, private_key):
        self.private_key = private_key
        self.public_key = private_to_stark_key(private_key)

    def sign(self, message_hash):
        return sign(msg_hash=message_hash, priv_key=self.private_key)

    async def send_transaction(self, account, to, selector_name, calldata, nonce=None):
        if nonce is None:
            execution_info = await account.get_nonce().call()
            nonce, = execution_info.result

        calldata = flatten_calldata(calldata)

        selector = get_selector_from_name(selector_name)
        message_hash = hash_message(account.contract_address, to, selector, calldata, nonce)
        sig_r, sig_s = self.sign(message_hash)
        return await account.execute(to, selector, calldata, nonce).invoke(signature=[sig_r, sig_s])

def flatten_calldata(calldata):
    """Given a list of calldata. Flatten any uint256 tuples that might appear."""
    flat_calldata = []
    for cd in calldata:
        if type(cd) is tuple:
            assert len(cd) == 2, "cd: {}".format(cd)
            flat_calldata.append(cd[0])
            flat_calldata.append(cd[1])
        else:
            flat_calldata.append(cd)
    return flat_calldata

def hash_message(sender, to, selector, calldata, nonce):
    message = [
        sender,
        to,
        selector,
        compute_hash_on_elements(calldata),
        nonce
    ]
    return compute_hash_on_elements(message)

def get_random_signer():
    private_key = random.randint(10000, 10000000)
    return Signer(private_key)

