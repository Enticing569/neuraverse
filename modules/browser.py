
from curl_cffi import requests

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"

class BaseAsyncSession(requests.AsyncSession):
    def __init__(
            self,
            proxy: str = None,
            user_agent: str = DEFAULT_UA,
            *,
            impersonate: requests.BrowserType = requests.BrowserType.chrome136,
            **session_kwargs,
    ):
        proxies = {"http": proxy, "https": proxy}
        headers = session_kwargs.pop("headers", {})
        headers["user-agent"] = user_agent
        super().__init__(
            proxies=proxies,
            headers=headers,
            impersonate=impersonate,
            **session_kwargs,
        )

    @property
    def user_agent(self) -> str:
        return self.headers["user-agent"]

