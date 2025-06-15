#-_-

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph, indices, low, stack, sccs, current=None, step=0, fig=None):
    fig.clf()
    G = nx.DiGraph()
    for u in range(1, len(graph)):
        for v in graph[u]:
            G.add_edge(u, v)
    pos = nx.spring_layout(G, seed = 1)
    node_colors = []
    for node in G.nodes():
        if node == current:
            node_colors.append('orange')
        elif node in stack:
            node_colors.append('yellow')
        else:
            node_colors.append('lightgray')
    # Подсветка компонент сильной связности
    for scc in sccs:
        for node in scc:
            if node in G.nodes():
                node_colors[list(G.nodes()).index(node)] = 'lightgreen'
    labels = {node: f'{node}\n({indices[node]},{low[node]})' for node in G.nodes()}
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=1000, font_size=10, ax=fig.gca())
    fig.suptitle(f'Step {step}')
    fig.canvas.draw()
    plt.pause(1)

def tarjan(graph, n, fig):
    # Инициализация переменных
    index = 1
    indices = [0] * (n + 1)
    low = [0] * (n + 1)
    on_stack = [False] * (n + 1)
    stack = []
    components = []
    step = 0
    
    def strong_connect(v):
        nonlocal index, step
        # Устанавливаем индекс и low-link для текущей вершины
        indices[v] = index
        low[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True
        step += 1
        draw_graph(graph, indices, low, stack, components, current=v, step=step, fig=fig)
        
        # Рассматриваем всех соседей текущей вершины
        for w in graph[v]:
            if indices[w] == 0:
                # Сосед еще не посещен
                strong_connect(w)
                low[v] = min(low[v], low[w])
                step += 1
                draw_graph(graph, indices, low, stack, components, current=v, step=step, fig=fig)
            elif on_stack[w]:
                # Сосед находится в стеке - нашли цикл
                low[v] = min(low[v], indices[w])
                step += 1
                draw_graph(graph, indices, low, stack, components, current=v, step=step, fig=fig)
        
        # Если v является корнем компоненты сильной связности
        if low[v] == indices[v]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == v:
                    break
            # Проверяем, является ли компонента циклом
            if len(component) > 1 or v in graph[v]:
                components.append(component)
            step += 1
            draw_graph(graph, indices, low, stack, components, current=None, step=step, fig=fig)
    
    # Запускаем DFS для каждой непосещенной вершины
    for v in range(1, n + 1):
        if indices[v] == 0:
            strong_connect(v)
    
    return components

if __name__ == '__main__':
    plt.ion()
    fig = plt.figure(figsize=(8, 5))
    n = int(input())
    graph = [[] for _ in range(n + 1)]
    
    # Чтение входных данных
    for i in range(1, n + 1):
        line = list(map(int, input().split()))
        k = line[0]
        for j in range(1, k + 1):
            graph[i].append(line[j])
    
    # Поиск компонент сильной связности
    components = tarjan(graph, n, fig)
    
    plt.ioff()
    plt.show()
    # Вывод результата
    if not components:
        print(-1)
    else:
        for component in components:
            print(' '.join(map(str, sorted(component))))

