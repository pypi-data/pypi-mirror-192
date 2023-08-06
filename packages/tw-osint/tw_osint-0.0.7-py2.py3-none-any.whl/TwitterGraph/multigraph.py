from manager import GraphManager
import networkx as nx
from os import path
import os

# politica españa:
# derecha : vox_es, santi_abascal, macarena_olona, ivanedlm
# izquierda: irenemontero, podemos, agarzon, pabloiglesias, sanchezcastejon

# política eeuu:
# derecha: realdonaldtrump, speakermccarthy, repmikegarcia
# izquierda: joebiden, barackobama, hillaryclinton

# actores eeuu:
# aaronpaul_8, bryancranston, breakingbad


class MultiG:

    def __init__(self, victims, n_tweets=10, depth_=1, ruta=None) -> None:

        self.victims = ('_').join(victims)
        self.n_tweets = n_tweets
        self.depth = depth_ if depth_ else 1
        self.graph = nx.DiGraph()

        # RUTA - CARPETA Y ARCHIVO
        if ruta is None:
            self.path = f'{os.getcwd()}/resources/multi/' + ('_').join(victims)
            self.path += f'/tweets_{self.n_tweets}_depth_{self.depth}'
        else:
            self.path = ruta
        # SI EXISTE EL ARCHIVO - SE CARGA
        if path.exists(self.path + '.dot'):
            self.manager = GraphManager('', -1, -1, self.path + '.dot')
            if not path.exists(self.path + '.png'):
                self.manager.save(self.path)
                self.manager.save_friends(self.path)
        else:
            # NO EXISTE EL ARCHIVO
            for v in victims:
                # se calcula y se guarda el árbol de forma ind para cada victima
                man = GraphManager(v, n_tweets, depth_)
                self.graph = nx.compose(self.graph, nx.DiGraph(man.nx))
            
            if not path.exists(f'{os.getcwd()}/resources/multi'):
                # Create a new directory because it does not exist
                os.makedirs(f'{os.getcwd()}/resources/multi')
                
            if not path.exists(f'{os.getcwd()}/resources/multi/' + ('_').join(victims)):
                os.makedirs(f'{os.getcwd()}/resources/multi/' + ('_').join(victims))
                
            nx.nx_pydot.write_dot(self.graph, self.path + '.dot')
            self.manager = GraphManager('', -1, -1, self.path + '.dot')
            self.manager.save(self.path + '.dot')
            self.manager.save_friends(self.path + '_amigos.dot')