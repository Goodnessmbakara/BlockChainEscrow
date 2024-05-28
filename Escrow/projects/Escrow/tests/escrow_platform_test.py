import base64
import time
from functools import reduce
import pytest
from algosdk import account
from algokit_utils import (
    Account,
    EnsureBalanceParameters,
    TransactionParameters,
    TransferParameters,
    ensure_funded,
    get_account,
    transfer,
)
from algokit_utils.config import config
from algosdk import encoding
from algosdk.atomic_transaction_composer import(
    AccountTransactionSigner,
    TransactionWithSigner,
)
from algosdk.transaction import PaymentTxn, SuggestedParams
from algosdk.util import algos_to_microalgos
from algosdk.v2client.algod import AlgodClient
from algosdk.v2client.indexer import IndexerClient
from smart_contracts.artifacts.escrow_platform.client import EscrowPlatformClient
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    PayParams,
    
)

from algokit_utils.beta.account_manager import AddressAndSigner

@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClient to use throughout the tests"""

    return AlgorandClient.default_local_net()


@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> AddressAndSigner:
    """Get the dispenser to fund test addresses"""
    return algorand.account.dispenser()


@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    """A random account to be used throughout the test"""

    acct = algorand.account.random()
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )
    return acct

# @pytest.fixture(scope="session")
# def account() -> Account:
#     return Account()


@pytest.fixture(scope="session")
def app_client(creator:  AddressAndSigner, algod_client: AlgodClient, indexer_client: IndexerClient) -> EscrowPlatformClient:


    config.configure(debug=True)
    client = EscrowPlatformClient(
        algod_client,
        creator=creator,
        indexer_client=indexer_client,
    )
    client.create_start_transaction(
        invoice_id="diddsljdefieee",
        total_products_amount=algos_to_microalgos(1_000_000),

    )

    transfer(
        algod_client,
        TransferParameters(
            from_account=account,
            to_address=client.app_address,
            micro_algos=1_000_000,

        ),
    )
    return client

# def flat_fee(algod_client: AlgodClient, fee: int)-> SuggestedParams:
#     sp = algod_client.suggested_params()
#     sp.fee = fee
#     sp.flat_fee = True
#     return sp

def test_start_transaction(app_client: EscrowPlatformClient)-> None:
    """Tests the start transaction() method."""

    state = {k: getattr(v, "as_str", v) for k, v in app_client.get_global_state(). __dict__.items()}
    assert state["invoice_id"] == "diddsljdefieee", "Invoice ID does not exists"
    assert state["total_products_amount"] == algos_to_microalgos(1_000_000), "Incorrect total product amount"
