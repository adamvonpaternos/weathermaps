import logging
from enum import Enum, auto
import xml.etree.ElementTree as ET

from fastapi import APIRouter, Query, Depends, Response
import requests

from weathermaps.dependencies import OPEN_WEATHER_API_CONFIG


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/open-weather",
    tags=["open-weather"],
    responses={404: {"description": "Not found"}},
)


class Mode(str, Enum):
    json = "json"
    xml = "xml"


class Units(str, Enum):
    standard = "standard"
    metric = "metric"
    imperial = "imperial"


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Lang(str, AutoName):
    af = auto()
    al = auto()
    ar = auto()
    az = auto()
    bg = auto()
    ca = auto()
    cz = auto()
    da = auto()
    de = auto()
    el = auto()
    en = auto()
    eu = auto()
    fa = auto()
    fi = auto()
    fr = auto()
    gl = auto()
    he = auto()
    hi = auto()
    hr = auto()
    hu = auto()
    id = auto()
    it = auto()
    ja = auto()
    kr = auto()
    la = auto()
    lt = auto()
    mk = auto()
    no = auto()
    nl = auto()
    pl = auto()
    pt = auto()
    pt_br = auto()
    ro = auto()
    ru = auto()
    sv = auto()
    se = auto()
    sk = auto()
    sl = auto()
    sp = auto()
    es = auto()
    sr = auto()
    th = auto()
    tr = auto()
    ua = auto()
    uk = auto()
    vi = auto()
    zh_cn = auto()
    zh_tw = auto()
    zu = auto()


class CommonQueryParams:
    def __init__(
        self,
        mode: Mode | None = None,
        cnt: int | None = None,
        units: Units | None = None,
        lang: Lang | None = None,
    ):
        self.mode = mode
        self.cnt = cnt
        self.units = units
        self.lang = lang


async def get_open_weather(
    endpoint: str, params: dict, common_params: CommonQueryParams
) -> Response:
    if common_params.mode:
        params["mode"] = common_params.mode.value
    if common_params.cnt:
        params["cnt"] = common_params.cnt
    if common_params.units:
        params["units"] = common_params.units.value
    if common_params.lang:
        params["lang"] = common_params.lang.value
    url = f"{OPEN_WEATHER_API_CONFIG.base_url}/{endpoint}"
    logger.info(url, params)

    params["appid"] = OPEN_WEATHER_API_CONFIG.api_key

    response = requests.get(
        url=f"{OPEN_WEATHER_API_CONFIG.base_url}/{endpoint}",
        params=params,
    )
    if params["mode"] == Mode.xml:
        xml = ET.tostring(
            ET.fromstring(response.text)
        )  # parse out XML declaration
        return Response(
            content=xml, media_type="application/xml", status_code=200
        )
    else:
        return Response(
            content=response.json(),
            media_type="application/json",
            status_code=200,
        )


@router.get(
    "/city_name/",
    response_class=Response,
)
async def current_weather_by_city_name(
    city_name: str = Query(...),
    state_code: str = Query(None),
    country_code: str = Query(None),
    common_params: CommonQueryParams = Depends(CommonQueryParams),
):
    params = {}
    params["q"] = city_name
    if state_code:
        params["q"] += f",{state_code}"
    if country_code:
        params["q"] += f",{country_code}"

    return await get_open_weather(
        endpoint="weather", params=params, common_params=common_params
    )


@router.get("/city_id/")
async def current_weather_by_city_id(
    city_id: str = Query(...),
    common_params: CommonQueryParams = Depends(CommonQueryParams),
):
    params = {}
    params["id"] = city_id
    return await get_open_weather(
        endpoint="weather", params=params, common_params=common_params
    )


@router.get("/geographic_coords/")
async def current_weather_by_geographic_coords(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    common_params: CommonQueryParams = Depends(CommonQueryParams),
):
    params = {}
    params["lat"] = lat
    params["lon"] = lon
    print(params)
    return await get_open_weather(
        endpoint="weather", params=params, common_params=common_params
    )


@router.get("/zip_code/")
async def current_weather_by_zip_code(
    zip_code: int = Query(..., description="Zip code"),
    common_params: CommonQueryParams = Depends(CommonQueryParams),
):
    params = {}
    params["zip"] = zip_code
    print(params)
    return await get_open_weather(
        endpoint="weather", params=params, common_params=common_params
    )
