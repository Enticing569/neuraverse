from typing import Any, cast

from data.config import ABIS_DIR
from libs.eth_async.classes import Singleton
from libs.eth_async.data.models import DefaultABIs, RawContract
from libs.eth_async.utils.files import read_json


class Contracts(Singleton):
    ANKR = RawContract(title="ANKR", address="0xBd833b6eCC30CAEaBf81dB18BB0f1e00C6997E7a", abi=DefaultABIs.Token)

    ZOTTO_ROUTER_ADDRESS = RawContract(
        title="Zotto swap",
        address="0x5AeFBA317BAba46EAF98Fd6f381d07673bcA6467",
        abi=cast(list[dict[str, Any]], read_json((ABIS_DIR, "zotto_router.json"))),
    )

    ZOTTO_POOLS_ADRESS = RawContract(
        title="Zotto pools",
        address="0x03f8B4b140249Dc7B2503C928E7258CCe1d91F1A",
        abi=cast(list[dict[str, Any]], read_json((ABIS_DIR, "zotto_pools.json"))),
    )

    NEURA_BRIDGE = RawContract(
        title="Neura bridge",
        address="0xc6255a594299F1776de376d0509aB5ab875A6E3E",
        abi=cast(list[dict[str, Any]], read_json((ABIS_DIR, "neura_bridge.json"))),
    )

    SEPOLIA_BRIDGE = RawContract(
        title="Sepolia bridge",
        address="0xc6255a594299F1776de376d0509aB5ab875A6E3E",
        abi=cast(list[dict[str, Any]], read_json((ABIS_DIR, "sepolia_bridge.json"))),
    )

    SEPOLIA_TANKR = RawContract(title="ANKR on Sepolia", address="0xB88Ca91Fef0874828e5ea830402e9089aaE0bB7F", abi=DefaultABIs.Token)

    OMNIHUB_NFT = RawContract(
        title="Omnihub_nft",
        address="0x6f38636175e178e1d2004431ffcb91a1030282ac",
        abi=cast(list[dict[str, Any]], read_json((ABIS_DIR, "omnihub_nft.json"))),
    )
