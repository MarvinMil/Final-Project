from pathlib import Path
import io, requests, geopandas as gpd, numpy as np, rasterio
from rasterio.features import geometry_mask
from rasterio.transform import from_origin
from shapely.geometry import mapping

APP_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RASTER = APP_ROOT / "data" / "raster" / "synthetic_lst.tif"
NUTS3_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326_LEVL_3.geojson"
NUTS_ALL_URL = "https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326.geojson"

def ensure_data_ready(data_dir: Path):
    data_dir.mkdir(parents=True, exist_ok=True)
    nei = data_dir / "neighborhoods.geojson"
    if not nei.exists() or nei.stat().st_size == 0:
        try:
            r = requests.get(NUTS3_URL, timeout=60); r.raise_for_status()
            gdf = gpd.read_file(io.BytesIO(r.content))
        except Exception:
            r = requests.get(NUTS_ALL_URL, timeout=60); r.raise_for_status()
            gdf = gpd.read_file(io.BytesIO(r.content))
            if "LEVL_CODE" in gdf.columns:
                gdf = gdf[gdf["LEVL_CODE"] == 3]
        gdf = gdf[gdf["CNTR_CODE"] == "AT"].copy()
        gdf = gdf.rename(columns={"NAME_LATN":"name","NUTS_ID":"id"})[["id","name","geometry"]]
        gdf = gdf.to_crs(4326)
        gdf.to_file(nei, driver="GeoJSON")
    (data_dir / "raster").mkdir(parents=True, exist_ok=True)
    if not DEFAULT_RASTER.exists():
        _generate_synthetic_raster(nei, DEFAULT_RASTER)

def _generate_synthetic_raster(neighborhoods_path: Path, out_path: Path):
    gdf = gpd.read_file(neighborhoods_path)
    if gdf.crs is None or gdf.crs.to_epsg() != 3857:
        gdf = gdf.to_crs(3857)
    minx, miny, maxx, maxy = gdf.total_bounds
    buf = 5000
    minx, miny, maxx, maxy = minx-buf, miny-buf, maxx+buf, maxy+buf
    pix = 1000
    width = max(1, int((maxx - minx) / pix))
    height = max(1, int((maxy - miny) / pix))
    transform = from_origin(minx, maxy, pix, pix)
    x = np.linspace(0,1,width); y = np.linspace(0,1,height); xx,yy = np.meshgrid(x,y)
    base = 18 + 20*(xx*0.6 + yy*0.4)
    noise = np.random.default_rng(42).normal(0, 1.0, size=(height, width))
    arr = base + noise
    with rasterio.open(out_path, 'w', driver='GTiff', height=height, width=width, count=1,
                       dtype=arr.dtype, crs='EPSG:3857', transform=transform, compress='lzw') as dst:
        dst.write(arr, 1)

def load_neighborhoods_with_stats(geojson_path: Path):
    gdf = gpd.read_file(geojson_path)
    with rasterio.open(DEFAULT_RASTER) as src:
        if gdf.crs != src.crs:
            gdf = gdf.to_crs(src.crs)
        data = src.read(1)
        means, mins, maxs = [], [], []
        for geom in gdf.geometry:
            if geom is None or geom.is_empty:
                means.append(None); mins.append(None); maxs.append(None); continue
            mask = geometry_mask([mapping(geom)], out_shape=(src.height, src.width),
                                 transform=src.transform, invert=True)
            vals = np.where(mask, data, np.nan); vals = vals[~np.isnan(vals)]
            if vals.size == 0:
                means.append(None); mins.append(None); maxs.append(None)
            else:
                means.append(float(np.nanmean(vals)))
                mins.append(float(np.nanmin(vals)))
                maxs.append(float(np.nanmax(vals)))
    gdf = gdf.to_crs(4326)
    gdf["lst_mean"] = means; gdf["lst_min"] = mins; gdf["lst_max"] = maxs
    q = gdf["lst_mean"].dropna()
    if len(q) >= 5:
        import numpy as _np
        bins = _np.quantile(q, [0,0.2,0.4,0.6,0.8,1.0])
    else:
        import math, numpy as _np
        if len(q)==0: bins = _np.linspace(0,1,6)
        else: bins = _np.linspace(q.min(), q.max() if not math.isclose(q.min(), q.max()) else q.min()+1, 6)
    import numpy as _np
    gdf["lst_class"] = _np.digitize(gdf["lst_mean"], bins, right=True)
    return gdf
