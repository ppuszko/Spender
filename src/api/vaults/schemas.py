from pydantic import BaseModel, ConfigDict




class VaultPublic(BaseModel):
    

    model_config = ConfigDict(from_attributes=True)