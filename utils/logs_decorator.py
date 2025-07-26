from functools import wraps
from utils.logs import logger

def controller_log(action_name: str = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            try:
                wallet_name = getattr(getattr(self, "wallet", None), "id", "UnnamedWallet")
                #chain = getattr(getattr(getattr(self, "client", None), "network", None), "name", "unknown").capitalize()
                module = getattr(self, "__module_name__", self.__class__.__name__)
                action = action_name or func.__name__

                result = await func(self, *args, **kwargs)
                msg = f"[id: {wallet_name}] | {module} | {action} | {result}"

                if 'Failed' not in result:
                    #logger.success(msg)
                    return msg

                return msg

            except Exception as e:
                msg = f"[id: {wallet_name}] | {module} | {action} | Failed | {e}"
                logger.error(msg)
                raise
        return wrapper
    return decorator

