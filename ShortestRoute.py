#Latest: 12 Jan 2026
#By: Group 2 
#Main Programmer: Daniel Sahid
#Contributors: Danial Hakimi, Fara'ain, Syakilla, Maisarah

import streamlit as st
import heapq
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finding Shortest Route")
st.title("Find the Shortest Route")
st.markdown("""
Please add roads to build the network and compute the shortest path from the source node to destination node.
""")

# Session State Setup
if "graph" not in st.session_state:
    st.session_state.graph = {}
if "locations_set" not in st.session_state:
    st.session_state.locations_set = set()
if "visualize" not in st.session_state:
    st.session_state.visualize = False 

graph = st.session_state.graph
locations_set = st.session_state.locations_set

# Form to add new roads
st.header("Add a New Road to Connect Locations")
with st.form("road_input_form"):  # unique form key
    src = st.text_input("From Location (Example: A, B, UiTM Jasin)", key="src_input")
    dst = st.text_input("To Location (Example: C, D, Melaka Sentral)", key="dst_input")
    dist = st.text_input("Distance (km)", key="dist_input")
    submitted = st.form_submit_button("Submit Road")

if submitted:
    if not src or not dst or not dist:
        st.error("All fields are required!")
    else:
        try:
            d = float(dist)  # changed from int(dist) to float(dist)
            locations_set.add(src)
            locations_set.add(dst)

            if src not in graph:
                graph[src] = []
            if dst not in graph:
                graph[dst] = []

            graph[src].append((dst, d))
            graph[dst].append((src, d))

            st.success(f"Added road: {src} ↔ {dst} ({d})")
        except ValueError:
            st.error("Distance must be a number!") 
        
# Display current roads
if graph:
    st.header("Current Road Network")
    for src, edges in graph.items():
        st.write(f"**{src}**: " + ", ".join([f"{dest} ({w})" for dest, w in edges]))


# Button to Visualize Graph
if st.button("Visualize Current Network"):
    st.session_state.visualize = True  

if st.session_state.visualize and graph:
    st.header("Graph Visualization")
    G = nx.Graph()
    for src, edges in graph.items():
        for dest, weight in edges:
            G.add_edge(src, dest, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=12)
    labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    st.pyplot(plt)


# Shortest Path Computation
if locations_set:
    st.header("Compute Shortest Path")
    
    # Select source location 
    source_select = st.selectbox(
        "Source Location",  
        sorted(locations_set),
        key="source_select"                     
    )
    
    # Select destination location
    destination_select = st.selectbox(
        "Destination Location",                 
        sorted(locations_set),
        key="destination_select"                 
    )

    if st.button("Compute Shortest Path"):

        #Dijkstra's algorithm
        def dijkstra(graph, start, end):
            heap = [(0, start, [])]
            visited = set()
            while heap:
                dist, node, path = heapq.heappop(heap)
                if node in visited:
                    continue
                visited.add(node)
                path = path + [node]
                if node == end:
                    return dist, path
                for neighbor, weight in graph.get(node, []):
                    if neighbor not in visited:
                        heapq.heappush(heap, (dist + weight, neighbor, path))
            return float('inf'), []

        distance, path = dijkstra(graph, source_select, destination_select)
        if distance == float('inf'):
            st.error(f"No path exists from {source_select} to {destination_select}.")
        else:
            st.success(f"Shortest Distance: {distance}")
            st.info(f"Shortest Path: {' → '.join(path)}")

            # Visualize shortest path
            st.header("Shortest Path Highlighted")
            G = nx.Graph()
            for src, edges in graph.items():
                for dest, weight in edges:
                    G.add_edge(src, dest, weight=weight)

            pos = nx.spring_layout(G, seed=42)
            labels = nx.get_edge_attributes(G, "weight")

            edge_colors = []
            for u, v in G.edges():
                if u in path and v in path:
                    idx_u = path.index(u)
                    idx_v = path.index(v)
                    if abs(idx_u - idx_v) == 1:
                        edge_colors.append("red")
                    else:
                        edge_colors.append("black")
                else:
                    edge_colors.append("black")

            plt.figure(figsize=(8, 5))
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=12)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=3)
            st.pyplot(plt)




