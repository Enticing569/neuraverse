from eth_abi.abi import encode as abi_encode
from loguru import logger
from web3.types import TxParams

from data.models import Contracts
from libs.eth_async.client import Client
from libs.eth_async.data.models import TokenAmount
from libs.eth_async.utils.utils import wait_for_acceptable_gas_price
from utils.db_api.models import Wallet


class OmnihubNFT:
    __module__ = "Omnuhub nft"

    def __init__(self, client: Client, wallet: Wallet):
        self.client = client
        self.wallet = wallet

    def __repr__(self):
        return f"{self.__module__} | [{self.wallet.address}]"

    async def is_minting(self) -> int:
        nft_contract = await self.client.contracts.get(Contracts.OMNIHUB_NFT)
        return await nft_contract.functions.balanceOf(self.client.account.address).call()

    async def mint_nft(self, quantity: int, check_gas_price: bool = True) -> bool:
        logger.debug(f"{self.wallet} | Starting NFT minting: quantity={quantity}")

        nft_contract = await self.client.contracts.get(Contracts.OMNIHUB_NFT)
        native_balance = await self.client.wallet.balance()
        mint_price = TokenAmount(amount=0.01 * quantity, decimals=18)

        if mint_price.Ether > native_balance.Ether:
            logger.warning(f"{self.wallet} | Insufficient balance for minting: need {mint_price.Ether} ETH, have {native_balance.Ether} ETH")
            return False

        if check_gas_price:
            if not await wait_for_acceptable_gas_price(client=self.client, wallet=self.wallet):
                logger.warning(f"{self.wallet} | Gas price too high, aborting mint")
                return False

        encoded_args = abi_encode(["uint256", "uint256", "uint256", "bytes"], [0, quantity, 0, b""])

        data = bytes.fromhex("a25ffea8" + encoded_args.hex())

        transaction = await self.client.transactions.sign_and_send(TxParams(to=nft_contract.address, data=data, value=mint_price.Wei))

        recipient = await transaction.wait_for_receipt(client=self.client, timeout=300)

        if recipient["status"] != 1:
            logger.error(f"{self.wallet} | NFT mint transaction failed for quantity={quantity}")
            return False

        logger.debug(f"{self.wallet} | NFT minted successfully: quantity={quantity}")
        return True
