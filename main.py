import json

from bs4 import BeautifulSoup

from spec.openai import FunctionType, function_call, make_client

google = make_client(base_url="https://www.google.com", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"})

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



async def main():
    functions = [GoogleSearch]
    while True:
        text = input("Enter a math question: ")
        result = await function_call(text, functions)
        print(result)
    
        
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    