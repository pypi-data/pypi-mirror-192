from pydantic import BaseModel, StrictFloat, StrictStr


class Diamond(BaseModel):
    carat: StrictFloat
    cut: StrictStr
    color: StrictStr
    clarity: StrictStr
    depth: StrictFloat
    table: StrictFloat
    x: StrictFloat
    y: StrictFloat
    z: StrictFloat
