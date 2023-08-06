import aiohttp

class NoSytx:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://nosytx.eu/api/"

    async def api(self, endpoint):
        if self.token is None or self.token == "":
            raise Exception("No token provided")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url + endpoint,
                                       headers={"Authorization": f"Bearer {self.token}"}) as response:
                    data = await response.json()
                    if response.status == 401:
                        raise PermissionError("No permission to access this endpoint")
                    elif data["image"] == "Error404":
                        raise Exception("Endpoint not found")
                    elif response.status == 200:
                        return data["image"]
                    else:
                        raise Exception("Something went wrong")
