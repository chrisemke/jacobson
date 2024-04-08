from api.address.inputs import AddressInput
from database import functions
from database.models.brazil import Address


async def get_address(filter: AddressInput) -> list[Address | None]:
    result = await functions.get_address_by_dc_join_state_join_city(filter)
    if not result:
        try:
            ...
            # result = async get from plugins
        except Exception as e:
            ...
            # there is no address found
        else:
            ...
            # async insert on database
    return result
