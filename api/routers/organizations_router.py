# @Author: Rafael Direito
# @Date:   2022-08-03 18:45:14 (WEST)
# @Email:  rdireito@av.it.pt
# @Copyright: Insituto de Telecomunicações - Aveiro, Aveiro, Portugal
# @Last Modified by:   Rafael Direito
# @Last Modified time: 2023-04-10 15:59:02

# generic imports
from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database.crud import crud
from http import HTTPStatus
from typing import Optional
import logging

# custom imports
import database.crud.exceptions as CRUDExceptions
import schemas.tmf632_party_mgmt as TMF632Schemas
import main
from routers.aux import (
    GetOrganizationFilters,
    filter_organization_fields,
    parse_organization_query_filters,
    create_http_response,
    organization_to_organization_schema,
    exception_to_http_response
)

# Logger
logger = logging.getLogger(__name__)


router = APIRouter()


# Dependency
def get_db():
    return next(main.get_db())


@router.post(
    "/organization/",
    tags=["organization"],
    summary="Creates a Organization",
    description="This operation creates a Organization entity.",
    responses={
    }
)
async def create_organization(
    organization: TMF632Schemas.OrganizationCreate,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Someone is trying to create a new organization...")

        organization = crud.create_organization(db, organization)

        logger.info("The following organization was created: " +
                    f"{organization}")
        return create_http_response(
            http_status=HTTPStatus.CREATED,
            # Return parsed
            content=jsonable_encoder(
                organization_to_organization_schema(organization)
            )
        )
    except Exception as exception:
        return exception_to_http_response(exception)


@router.get(
    "/organization/",
    tags=["organization"],
    summary="List or find Organization objects",
    description="This operation list or find Organization entities.",
    response_model=list[TMF632Schemas.Organization],
)
@router.get(
    "/organization/{id}",
    tags=["organization"],
    summary="List or find Organization objects",
    description="This operation list or find Organization entities.",
    response_model=list[TMF632Schemas.Organization],
)
async def get_organization(
    id: Optional[int] = None,
    fields: Optional[str] = Query(
        default=None,
        regex="^(("
        + '|'.join(TMF632Schemas.Organization.__fields__.keys())
        + ")(,)?)+$"
    ),
    filter: GetOrganizationFilters = Depends(),
    db: Session = Depends(get_db),
):
    try:
        # Parse all query parameters
        fields = fields.split(",") if fields else None
        filter_dict = parse_organization_query_filters(filter)

        # Operations for when the client requests a specific organization
        # These operations ignore all query filters, since the organization is
        # already 'filtered' using its id
        if id:
            logger.info("Someone is trying to obtain information " +
                        f"regarding  organization with id={id}...")
            organizations = [crud.get_organization_by_id(db, id)]
            if not organizations[0]:
                organizations[0] = {}


        # Operations for when the client requests all organization
        else:
            logger.info("Soemone is trying to obtain information " +
                        "regarding all organizations...")
            organizations = crud.get_all_organizations(db, filter_dict)

        # Parse to Pydantic Model
        tmf632_organizations = []
        for organization in organizations:
            if organization != {}:
                tmf632_organizations.append(
                    organization_to_organization_schema(organization)
                )
            else:
                tmf632_organizations.append(organization)

        logger.info(f"Obtained information regarding the " +
                    f"following organizations {tmf632_organizations}")

        # Apply 'fields' filter and encode/parse to dict
        encoded_organizations = [
            filter_organization_fields(
                fields,
                jsonable_encoder(encoded_organization)
            )
            for encoded_organization
            in tmf632_organizations
        ]

        # Response
        return create_http_response(
                http_status=HTTPStatus.OK,
                content=encoded_organizations[0]
                if id
                else encoded_organizations
        )
    except Exception as exception:
        return exception_to_http_response(exception)


@router.delete(
    "/organization/{id}",
    tags=["organization"],
    summary="Deletes a Organization",
    description="This operation deletes a Organization entity.",
)
async def delete_organization(
    id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    try:
        logger.info("Someone is trying to delete the organization with " +
                    f"the id {id}...")

        crud.delete_organization(db, id)

        logger.info("Someone deleted the organization with " +
                    f"the id {id}")
        # Response
        return create_http_response(
                http_status=HTTPStatus.NO_CONTENT
        )
    except Exception as exception:
        return exception_to_http_response(exception)


@router.patch(
    "/organization/{id}",
    tags=["organization"],
    summary="Updates partially a Organization",
    description="This operation updates partially a Organization entity.",
)
async def update_organization(
    id: int,
    organization: TMF632Schemas.OrganizationCreate,
    db: Session = Depends(get_db),
):
    try:
        logger.info("Someone is trying to patch the organization with " +
                    f"the id {id}...")

        current_organization = crud.get_organization_by_id(db, id)
        updated_organization = crud.update_organization(db, id, organization)

        logger.info("Someone patched the organization with the id " +
                    f"{id}. Updated organization: {updated_organization}")
        # Response
        return create_http_response(
                http_status=HTTPStatus.OK,
                # Parse Organization to TM632 Organization
                # And encode it
                content=jsonable_encoder(
                    organization_to_organization_schema(
                        updated_organization
                    )
                )
        )
    except Exception as exception:
        return exception_to_http_response(exception)