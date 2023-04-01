import tkinter
import tkinter.filedialog

from graph.graph import SpringMassGraph

def main() -> None:
    graph = SpringMassGraph()
    # wheels
    graph.create_wheel(3, 100)
    graph.save_to_csv('data/w3.csv')
    graph.create_wheel(4, 100)
    graph.save_to_csv('data/w4.csv')
    graph.create_wheel(5, 100)
    graph.save_to_csv('data/w5.csv')
    graph.create_wheel(6, 100)
    graph.save_to_csv('data/w6.csv')
    graph.create_wheel(8, 100)
    graph.save_to_csv('data/w8.csv')
    graph.create_wheel(10, 100)
    graph.save_to_csv('data/w10.csv')
    graph.create_wheel(20, 100)
    graph.save_to_csv('data/w20.csv')

    # complete graphs
    graph.create_complete_graph(3, 100)
    graph.save_to_csv('data/k3.csv')
    graph.create_complete_graph(4, 100)
    graph.save_to_csv('data/k4.csv')
    graph.create_complete_graph(7, 100)
    graph.save_to_csv('data/k7.csv')
    graph.create_complete_graph(10, 100)
    graph.save_to_csv('data/k10.csv')

if __name__ == "__main__":
    main()