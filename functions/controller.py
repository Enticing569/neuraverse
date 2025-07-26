from libs.eth_async.client import Client

from utils.db_api.models import Wallet
from utils.db_api.wallet_api import db
from utils.logs_decorator import controller_log


class Controller:

    def __init__(self, client: Client, wallet: Wallet):
        super().__init__(client)
        self.wallet = wallet
