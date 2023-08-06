from TwitterGraph.datascrapper import DataScrapper
from networkx import strongly_connected_components as scc
from datascrapper import DataScrapper
import networkx as nx


class Tree():

    def __init__(self, user_0, batch_=10, depth_=1) -> None:
        self.root = user_0
        self.batch = batch_
        self.depth = depth_ if depth_ else -1
        self.path = f'tweets_{self.batch}_depth_{self.depth}'
        self.nx = nx.DiGraph()
        self.nx.add_node(self.root, color='red')
        self.build()
        self.add_missing_edges()
    

    def add_edge(self, node_from, node_to):
        if self.root == node_from == node_to:
            col = 'green'
        elif self.root == node_from:
            col = 'red'
        else:
            col = 'blue' if self.root == node_to else 'black'
        # creamos la arista
        self.nx.add_edge(node_from, node_to, color=col)
        

    def build(self, user_=None, batch_=None, depth_=None) -> None:

        # construye recursivamente el grafo de reaciones empezando en el nodo root
        if user_ is None:
            user_ = self.root
            batch_ = self.batch
            depth_ = self.depth

        # scrap los últimos tweets outputs de "user"
        replies = set()
        last_tweets = DataScrapper(user_, batch_).get_outputs()
        for _, row in last_tweets.iterrows():
            if row['Reply_to'] is not None:
                usr = row['Reply_to'].username.lower()
                replies.add(usr)
            if row['Mentions'] is not None:
                for m in row['Mentions']:
                    if m is not None:
                        usr = m.username.lower()
                        replies.add(usr)

        # recorrer las respuestas encontradas
        for child in replies:
            self.add_edge(user_, child)
            if depth_ > 0:
                # llamada recursiva
                self.build(child, max(batch_//2, 0), depth_-1)

    # add_missing_edges -> añadimos comunicaciones con la víctima no reflejadas de nodos presentes en el grafo
    def add_missing_edges(self):
        # verificamos si algún nodo tiene conexión con root
        for n in self.nx.nodes:
            if n != self.root:
                if not self.nx.has_edge(self.root, n) and not DataScrapper().are_mentions(self.root,n):
                    self.add_edge(self.root, n)

                if not self.nx.has_edge(n, self.root) and not DataScrapper().are_mentions(n,self.root):
                    self.add_edge(n, self.root)



    # TODO: REVISAR - NOT USED!!
    def clean_tree(self):
        # limpia los nodos del árbol con input_deg <= 1 si no son adyacentes a victim
        to_remove = [n for n in self.nx.nodes if self.nx.in_degree(
            n) <= 1 and not self.nx.has_edge(self.root, n)]
        self.nx.remove_nodes_from(to_remove)

    def get_shortest_path(self, nodo_1, nodo_2):
        assert (nodo_1 in self.nx.nodes) and (nodo_2 in self.nx.nodes)
        return nx.dijkstra_path(self.nx, nodo_1, nodo_2)

    def get_distance(self, nodo_1, nodo_2):
        return len(self.get_shortest_path(nodo_1, nodo_2))
