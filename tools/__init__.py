import json

from spec.openai import (FunctionType, chain_of_thoughts, function_call,
                         make_client)


class GoogleSearch(FunctionType):
    """
    Searches Google for a query
    """
    query: str
    lang: str = "en"
    limit: int = 10
    offset: int = 0
    
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        text = await google.text(
            f"/search?q={obj.query}&hl={obj.lang}&num={obj.limit}&start={obj.offset}"
        )
        soup = BeautifulSoup(text, "html.parser")
        results = soup.find_all("div", class_="yuRUbf")
        return [i.a["href"] for i in results]

