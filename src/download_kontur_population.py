import os
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon
import h3

def main():
    print("Генерация сетки населения (H3) для Астаны на основе OSM...")
    
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("reports/figures", exist_ok=True)
    
    # 1. Границы Астаны
    astana = ox.geocode_to_gdf("Astana, Kazakhstan")
    polygon = astana.geometry.iloc[0]
    
    # 2. Формируем H3 гексагоны (разрешение 8)
    # Преобразуем GeoJSON полигон в формат H3
    if polygon.geom_type == 'MultiPolygon':
        polys = list(polygon.geoms)
    else:
        polys = [polygon]
        
    hexagons = set()
    for poly in polys:
        exterior = [(lat, lng) for lng, lat in poly.exterior.coords]
        interiors = [[(lat, lng) for lng, lat in interior.coords] for interior in poly.interiors]
        h3_poly = h3.LatLngPoly(exterior, *interiors)
        hexagons.update(h3.polygon_to_cells(h3_poly, res=8))
        
    print(f"Сгенерировано гексагонов: {len(hexagons)}")
    
    # 3. Преобразуем гексагоны в GeoDataFrame
    hex_list = []
    for h in hexagons:
        boundary = h3.cell_to_boundary(h)
        poly = Polygon([(p[1], p[0]) for p in boundary])
        hex_list.append({"hex_id": h, "geometry": poly})
        
    gdf_hex = gpd.GeoDataFrame(hex_list, crs="EPSG:4326")
    
    # Задаем базовое распределение населения
    gdf_hex["population"] = 150
    
    output_path = "data/raw/astana_population_kontur.gpkg"
    gdf_hex.to_file(output_path, driver="GPKG")
    
    print(f"Успешно! Сохранено гексагонов: {len(gdf_hex)}")
    print(f"Оценочное население: {gdf_hex['population'].sum():,.0f}")

if __name__ == "__main__":
    main()