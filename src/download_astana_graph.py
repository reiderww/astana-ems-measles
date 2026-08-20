import os
import osmnx as ox
import matplotlib.pyplot as plt

def main():
    print("Загрузка графа дорожной сети Астаны из OpenStreetMap...")
    
    # 1. Скачиваем граф дорог для автомобильного транспорта
    place_name = "Astana, Kazakhstan"
    G = ox.graph_from_place(place_name, network_type="drive")
    
    print(f"Граф успешно загружен! Узлов: {len(G.nodes)}, Ребер: {len(G.edges)}")
    
    # 2. Сохраняем граф в файл GraphML
    graph_path = "data/raw/astana_drive_network.graphml"
    ox.save_graphml(G, filepath=graph_path)
    print(f"Граф сохранен в: {graph_path}")
    
    # 3. Строим и сохраняем карту дорожной сети
    fig, ax = ox.plot_graph(G, node_size=1, edge_color="#2b5c8f", edge_linewidth=0.5, show=False, close=False)
    fig_path = "reports/figures/astana_road_network.png"
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Карта дорожной сети сохранена в: {fig_path}")

if __name__ == "__main__":
    main()