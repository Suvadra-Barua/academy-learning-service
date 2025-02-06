# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2023-2024 Valory AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the class to connect to an Storage contract."""

from typing import Dict

from aea.common import JSONLike
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea_ledger_ethereum import EthereumApi


PUBLIC_ID = PublicId.from_str("valory/storage:0.1.0")


class Storage(Contract):
    """The storage contract."""

    contract_id = PUBLIC_ID

    @classmethod
    def get_stored_number(
        cls,
        ledger_api: EthereumApi,
        contract_address: str,
    ) -> JSONLike:
        """Check the stored number."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        retrieve = getattr(contract_instance.functions, "retrieve")  # noqa
        stored_number = retrieve().call()
        return dict(number=stored_number)

    @classmethod
    def build_store_tx(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        number: int,
    ) -> Dict[str, bytes]:
        """Store a number."""
        contract_instance = cls.get_instance(ledger_api, contract_address)
        data = contract_instance.encodeABI("store", args=(number,))
        return {"data": bytes.fromhex(data[2:])}