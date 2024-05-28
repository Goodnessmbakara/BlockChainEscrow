import base64
import time
from functools import reduce
import pytest
from algokit_utils import (
    Account,
    EnsureBalanceParameters,
    TransactionParameters,
    TransferParameters,
    ensure_funded,
    get_account,
    transfer,
)
from algosdk.transaction im