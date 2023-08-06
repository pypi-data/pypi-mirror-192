from requests import Response
from pandas import DataFrame
from typing import Union, Optional, Collection, List
from spgci.api_client import get_data, Paginator
from spgci.utilities import list_to_filter
from .types import WOSRefType


class WorldOilSupply:
    _path = "wos/v2/"

    @staticmethod
    def _paginate(resp: Response) -> Paginator:
        j = resp.json()
        count = j["metadata"]["count"]
        size = j["metadata"]["pageSize"]

        total_pages = (count // size) + 1

        if total_pages <= 1:
            return Paginator(False, "page", 1)

        return Paginator(True, "page", total_pages=total_pages)

    def get_cost_of_supplies(
        self,
        *,
        ref_year: Optional[Union[int, Collection[int]]] = None,
        region: Optional[Union[str, Collection[str]]] = None,
        country: Optional[Union[str, Collection[str]]] = None,
        reserve_type: Optional[Union[str, Collection[str]]] = None,
        supply_type: Optional[Union[str, Collection[str]]] = None,
        supply_subtype: Optional[Union[str, Collection[str]]] = None,
        reserve_location: Optional[Union[str, Collection[str]]] = None,
        cost_of_supplies_type: Optional[Union[str, Collection[str]]] = None,
        production_element: Optional[Union[str, Collection[str]]] = None,
        cost_production_element: Optional[Union[str, Collection[str]]] = None,
        units: Optional[Union[str, Collection[str]]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        endpoint_path = "cost-of-supplies"

        filter_param: List[str] = []

        filter_param.append(list_to_filter("referenceYear", ref_year))
        filter_param.append(list_to_filter("regionName", region))
        filter_param.append(list_to_filter("countryName", country))
        filter_param.append(list_to_filter("reserveTypeName", reserve_type))
        filter_param.append(list_to_filter("supplyTypeName", supply_type))
        filter_param.append(list_to_filter("supplySubTypeName", supply_subtype))
        filter_param.append(list_to_filter("reserveLocationName", reserve_location))
        filter_param.append(list_to_filter("productionElementName", production_element))
        filter_param.append(list_to_filter("gradeElementName", units))
        filter_param.append(
            list_to_filter("costOfSuppliesTypeName", cost_of_supplies_type)
        )
        filter_param.append(
            list_to_filter("costProductionElementName", cost_production_element)
        )

        filter_param = [fp for fp in filter_param if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_param)
        else:
            filter_exp += " AND " + " AND ".join(filter_param)

        params = {
            "pageSize": page_size,
            "filter": filter_exp,
            "page": page,
        }
        return get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            paginate=paginate,
            paginate_fn=self._paginate,
            raw=raw,
        )

    def get_ownership(
        self,
        *,
        year: Optional[Union[int, Collection[int]]] = None,
        region: Optional[Union[str, Collection[str]]] = None,
        country: Optional[Union[str, Collection[str]]] = None,
        state: Optional[Union[str, Collection[str]]] = None,
        padd: Optional[Union[str, Collection[str]]] = None,
        reserve_type: Optional[Union[str, Collection[str]]] = None,
        supply_type: Optional[Union[str, Collection[str]]] = None,
        supply_subtype: Optional[Union[str, Collection[str]]] = None,
        reserve_location: Optional[Union[str, Collection[str]]] = None,
        production_type: Optional[Union[str, Collection[str]]] = None,
        production_element: Optional[Union[str, Collection[str]]] = None,
        grade_element: Optional[Union[str, Collection[str]]] = None,
        ownership_type: Optional[Union[str, Collection[str]]] = None,
        company_type: Optional[Union[str, Collection[str]]] = None,
        units: Optional[Union[str, Collection[str]]] = None,
        vintage: Optional[int] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        endpoint_path = "ownership"

        filter_param: List[str] = []

        filter_param.append(list_to_filter("year", year))
        filter_param.append(list_to_filter("regionName", region))
        filter_param.append(list_to_filter("countryName", country))
        filter_param.append(list_to_filter("stateName", state))
        filter_param.append(list_to_filter("paddName", padd))
        filter_param.append(list_to_filter("reserveTypeName", reserve_type))
        filter_param.append(list_to_filter("supplyTypeName", supply_type))
        filter_param.append(list_to_filter("supplySubTypeName", supply_subtype))
        filter_param.append(list_to_filter("reserveLocationName", reserve_location))
        filter_param.append(list_to_filter("productionTypeName", production_type))
        filter_param.append(list_to_filter("productionElementName", production_element))
        filter_param.append(list_to_filter("gradeElementName", grade_element))
        filter_param.append(list_to_filter("ownershipType", ownership_type))
        filter_param.append(list_to_filter("companyType", company_type))
        filter_param.append(list_to_filter("gradeElementName", units))
        filter_param.append(list_to_filter("vintage", vintage))

        filter_param = [fp for fp in filter_param if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_param)
        else:
            filter_exp += " AND " + " AND ".join(filter_param)

        params = {
            "pageSize": page_size,
            "filter": filter_exp,
            "page": page,
        }
        return get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            paginate=paginate,
            paginate_fn=self._paginate,
            raw=raw,
        )

    def get_production(
        self,
        *,
        scenario_term_id: int = 2,
        region: Optional[Union[str, Collection[str]]] = None,
        country: Optional[Union[str, Collection[str]]] = None,
        state: Optional[Union[str, Collection[str]]] = None,
        padd: Optional[Union[str, Collection[str]]] = None,
        reserve_type: Optional[Union[str, Collection[str]]] = None,
        supply_type: Optional[Union[str, Collection[str]]] = None,
        supply_subtype: Optional[Union[str, Collection[str]]] = None,
        reserve_location: Optional[Union[str, Collection[str]]] = None,
        production_type: Optional[Union[str, Collection[str]]] = None,
        grade: Optional[Union[str, Collection[str]]] = None,
        production_element: Optional[Union[str, Collection[str]]] = None,
        grade_element: Optional[Union[str, Collection[str]]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        endpoint_path = "production"

        filter_param: List[str] = []

        filter_param.append(list_to_filter("regionName", region))
        filter_param.append(list_to_filter("countryName", country))
        filter_param.append(list_to_filter("stateName", state))
        filter_param.append(list_to_filter("paddName", padd))
        filter_param.append(list_to_filter("reserveTypeName", reserve_type))
        filter_param.append(list_to_filter("supplyTypeName", supply_type))
        filter_param.append(list_to_filter("supplySubTypeName", supply_subtype))
        filter_param.append(list_to_filter("reserveLocationName", reserve_location))
        filter_param.append(list_to_filter("productionTypeName", production_type))
        filter_param.append(list_to_filter("gradeName", grade))
        filter_param.append(list_to_filter("productionElementName", production_element))
        filter_param.append(list_to_filter("gradeElementName", grade_element))

        filter_param = [fp for fp in filter_param if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_param)
        else:
            filter_exp += " AND " + " AND ".join(filter_param)

        params = {
            "scenarioTermId": scenario_term_id,
            "pageSize": page_size,
            "filter": filter_exp,
            "page": page,
        }
        return get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            paginate=paginate,
            paginate_fn=self._paginate,
            raw=raw,
        )

    def get_production_archive(
        self,
        *,
        scenario_id: int,
        scenario_term_id: int = 1,
        year: Optional[Union[int, Collection[int]]] = None,
        month: Optional[Union[int, Collection[int]]] = None,
        region: Optional[Union[str, Collection[str]]] = None,
        country: Optional[Union[str, Collection[str]]] = None,
        state: Optional[Union[str, Collection[str]]] = None,
        padd: Optional[Union[str, Collection[str]]] = None,
        reserve_type: Optional[Union[str, Collection[str]]] = None,
        supply_type: Optional[Union[str, Collection[str]]] = None,
        supply_subtype: Optional[Union[str, Collection[str]]] = None,
        reserve_location: Optional[Union[str, Collection[str]]] = None,
        production_type: Optional[Union[str, Collection[str]]] = None,
        grade: Optional[Union[str, Collection[str]]] = None,
        production_element: Optional[Union[str, Collection[str]]] = None,
        grade_element: Optional[Union[str, Collection[str]]] = None,
        units: Optional[Union[str, Collection[str]]] = None,
        filter_exp: Optional[str] = None,
        page: int = 1,
        page_size: int = 1000,
        paginate: bool = False,
        raw: bool = False,
    ) -> Union[Response, DataFrame]:
        endpoint_path = "production-archive"

        filter_param: List[str] = []

        filter_param.append(list_to_filter("year", year))
        filter_param.append(list_to_filter("month", month))
        filter_param.append(list_to_filter("units", units))
        filter_param.append(list_to_filter("regionName", region))
        filter_param.append(list_to_filter("countryName", country))
        filter_param.append(list_to_filter("stateName", state))
        filter_param.append(list_to_filter("paddName", padd))
        filter_param.append(list_to_filter("reserveTypeName", reserve_type))
        filter_param.append(list_to_filter("supplyTypeName", supply_type))
        filter_param.append(list_to_filter("supplySubTypeName", supply_subtype))
        filter_param.append(list_to_filter("reserveLocationName", reserve_location))
        filter_param.append(list_to_filter("productionTypeName", production_type))
        filter_param.append(list_to_filter("gradeName", grade))
        filter_param.append(list_to_filter("productionElementName", production_element))
        filter_param.append(list_to_filter("gradeElementName", grade_element))

        filter_param = [fp for fp in filter_param if fp != ""]

        if filter_exp is None:
            filter_exp = " AND ".join(filter_param)
        else:
            filter_exp += " AND " + " AND ".join(filter_param)

        params = {
            "scenarioTermId": scenario_term_id,
            "scenarioId": scenario_id,
            "pageSize": page_size,
            "filter": filter_exp,
            "page": page,
        }
        return get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            paginate=paginate,
            paginate_fn=self._paginate,
            raw=raw,
        )

    def get_reference_data(
        self, type: WOSRefType, raw: bool = False
    ) -> Union[Response, DataFrame]:
        endpoint_path = type.value

        params = {"pageSize": 1000}

        return get_data(
            path=f"{self._path}{endpoint_path}",
            params=params,
            paginate=True,
            paginate_fn=self._paginate,
            raw=raw,
        )
