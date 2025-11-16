from loguru import logger
from web3.types import TxParams

from data.models import Contracts
from data.settings import Settings
from libs.eth_async.client import Client
from libs.eth_async.data.models import TokenAmount, TxArgs
from utils.db_api.models import Wallet


class OmnihubNFT:
    __module__ = "Omnuhub nft"

    def __init__(self, client: Client, wallet: Wallet):
        self.client = client
        self.wallet = wallet
        self.settings = Settings()

    async def is_minting(self) -> bool:
        nft_contract = await self.client.contracts.get(Contracts.OMNIHUB_NFT)
        return await nft_contract.functions.balanceOf(self.client.account.address).call()

    async def mint_nft(self, quantity: int) -> bool:
        logger.debug(f"{self.wallet} | Starting NFT minting: quantity={quantity}")

        nft_contract = await self.client.contracts.get(Contracts.OMNIHUB_NFT)

        native_balance = await self.client.wallet.balance()

        mint_price = TokenAmount(amount=await nft_contract.functions.getMintPrice(0, quantity).call(), decimals=18)

        if mint_price.Ether > native_balance.Ether:
            logger.warning(f"{self.wallet} | Insufficient balance for minting: need {mint_price.Ether} ETH, have {native_balance.Ether} ETH")
            return False

        tx_params = TxArgs(phaseId=0, quantity=quantity, paymentToken=0, data=b"").tuple()

        data = await nft_contract.encode_abi("mintNFT", args=tx_params)

        transaction = await self.client.transactions.sign_and_send(TxParams(to=nft_contract.address, data=data, value=mint_price.Wei))

        recipient = await transaction.wait_for_receipt(client=self.client, timeout=300)

        if recipient["status"] != 1:
            logger.error(f"{self.wallet} | NFT mint transaction failed for quantity={quantity}")
            return False

        logger.debug(f"{self.wallet} | NFT minted successfully: quantity={quantity}")
        return True
