import os
import osmnx as ox
import geopandas as gpd

def main():
    print("Загрузка станций скорой помощи и больниц Астаны...")
    
    os.makedirs("data/raw", exist_ok=True)
    
    # 1. Запрос к OSM: больницы, клиники и станции скорой помощи
    tags = {
        "amenity": ["hospital", "clinic"],
        "emergency": ["ambulance_station", "yes"]
    }
    
    try:
        ems_data = ox.features_from_place("Astana, Kazakhstan", tags=tags)
        
        # Берем центроиды объектов
        ems_data["geometry"] = ems_data["geometry"].centroid
        
        cols = [c for c in ["name", "amenity", "emergency", "geometry"] if c in ems_data.columns]
        ems_gdf = ems_data[cols].copy()
        
        output_path = "data/raw/astana_ems_stations.gpkg"
        ems_gdf.to_file(output_path, driver="GPKG")
        
        print(f"Успешно! Сохранено объектов: {len(ems_gdf)}")
        print(f"Файл: {output_path}")
        
    except Exception as e:
        print(f"Ошибка загрузки: {e}")

if __name__ == "__main__":
    main()