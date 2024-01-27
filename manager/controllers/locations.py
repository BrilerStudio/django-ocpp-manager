from typing import List, Tuple

from fastapi import APIRouter, Depends, status

from app.database import get_contextual_session
from manager.ocpp_models import Account, Location
from manager.services.accounts import get_account
from manager.services.locations import (
    build_locations_query,
    create_location,
    list_simple_locations,
    remove_location,
)
from manager.utils import paginate, params_extractor
from manager.views.locations import (
    CreateLocationView,
    LocationView,
    PaginatedLocationsView,
    SimpleLocation,
)

locations_router = APIRouter(
    prefix='/{account_id}/locations',
    tags=['locations'],
)


@locations_router.get(
    '/autocomplete',
    status_code=status.HTTP_200_OK,
    response_model=List[SimpleLocation],
)
async def retrieve_simple_locations(
    account: Account = Depends(get_account),
) -> List[Location]:
    async with get_contextual_session() as session:
        locations = await list_simple_locations(session, account.id)
        await session.close()
        return locations


@locations_router.get('/', status_code=status.HTTP_200_OK)
async def retrieve_locations(
    search: str = '',
    account: Account = Depends(get_account),
    params: Tuple = Depends(params_extractor),
) -> PaginatedLocationsView:
    async with get_contextual_session() as session:
        locations = []
        items, pagination = await paginate(
            session,
            lambda: build_locations_query(account.id, search),
            *params,
        )
        for item in items:
            location = item[0]
            location.charge_points_count = item[1]
            locations.append(location)
        await session.close()
        return PaginatedLocationsView(
            items=locations,
            pagination=pagination,
        )


@locations_router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=LocationView,
)
async def add_location(
    data: CreateLocationView,
    account: Account = Depends(get_account),
) -> Location:
    async with get_contextual_session() as session:
        location = await create_location(session, account.id, data)
        await session.commit()
        await session.close()
        return location


@locations_router.delete(
    '/{location_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_location(
    location_id: str,
    account: Account = Depends(get_account),
):
    async with get_contextual_session() as session:
        await remove_location(session, location_id)
        await session.commit()
        await session.close()
