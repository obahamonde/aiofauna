from random import randint

from aiofauna import *


class Loc(FaunaModel):
    x: int = Field(index=True)
    y: int = Field(index=True)
    z :Optional[int] = Field(index=True)

    
app = AioFauna()

@app.get("/")
async def index():
    x = randint(0, 100)
    y = randint(0, 100)
    z = randint(0, 100)
    
    loc = await Loc(x=x, y=y, z=z).save()
    assert isinstance(loc, Loc)
    app.logger.info(loc.json())
    
    return loc.dict()



app.run()