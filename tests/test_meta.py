import json

from spec.openai import FunctionType, function_call


class Sum(FunctionType):
    """
    Sums two numbers
    """
    a: int
    b: int
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        return obj.a + obj.b
    
    
class Subtract(FunctionType):
    """
    Subtracts two numbers
    """
    a: int
    b: int
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        return obj.a - obj.b
    
class Multiply(FunctionType):
    """
    Multiplies two numbers
    """
    a: int
    b: int
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        return obj.a * obj.b
    
    
class Divide(FunctionType):
    """
    Divides two numbers
    """
    a: int
    b: int
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        return obj.a / obj.b
    
    
class Power(FunctionType):
    """
    Raises a number to a power
    """
    a: int
    b: int
    @classmethod
    async def run(cls, json_str:str):
        data = json.loads(json_str)
        obj = cls(**data)
        return obj.a ** obj.b
    
async def main():
    functions = [Sum, Subtract, Multiply, Divide, Power]
    while True:
        text = input("Enter a math question: ")
        result = await function_call(text, functions)
        print(result)
        
        
        
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    