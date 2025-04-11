from collections import defaultdict
import math

class GrafoLogistica:
    def __init__(self):
        self.V = set()
        self.E = set()
        self.A = set()
        self.ER = set()
        self.AR = set()
        self.VR = set()
        self.adjacente = defaultdict(list)
        self.matriz_dist = []
        self.matriz_pred = []

    def adicionar_aresta(self, u, v, peso=1, requerida=False):
        self.E.add((u, v))
        self.E.add((v, u))
        self.adjacente[u].append((v, peso))
        self.adjacente[v].append((u, peso))
        if requerida:
            self.ER.add((u, v))
            self.ER.add((v, u))
        self.V.update([u, v])

    def adicionar_arco(self, u, v, peso=1, requerido=False):
        self.A.add((u, v))
        self.adjacente[u].append((v, peso))
        if requerido:
            self.AR.add((u, v))
        self.V.update([u, v])

    def adicionar_vertice_requerido(self, v):
        self.VR.add(v)
        self.V.add(v)

    def inicializar_matrizes(self):
        n = len(self.V)
        index = {v: i for i, v in enumerate(sorted(self.V))}
        self.idx_to_v = {i: v for v, i in index.items()}
        INF = math.inf
        self.matriz_dist = [[INF] * n for _ in range(n)]
        self.matriz_pred = [[None] * n for _ in range(n)]
        for v in self.V:
            i = index[v]
            self.matriz_dist[i][i] = 0
            self.matriz_pred[i][i] = None
        for u in self.adjacente:
            for v, peso in self.adjacente[u]:
                i, j = index[u], index[v]
                self.matriz_dist[i][j] = peso
                self.matriz_pred[i][j] = i

    def floyd_warshall(self):
        self.inicializar_matrizes()
        n = len(self.V)
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.matriz_dist[i][k] + self.matriz_dist[k][j] < self.matriz_dist[i][j]:
                        self.matriz_dist[i][j] = self.matriz_dist[i][k] + self.matriz_dist[k][j]
                        self.matriz_pred[i][j] = self.matriz_pred[k][j]

    def estatisticas(self):
        n = len(self.V)
        m = len(self.E) // 2
        a = len(self.A)
        r_vertices = len(self.VR)
        r_arestas = len(self.ER) // 2
        r_arcos = len(self.AR)
        densidade = (m + a) / (n * (n - 1)) if n > 1 else 0
        graus = {v: 0 for v in self.V}
        for u in self.adjacente:
            graus[u] += len(self.adjacente[u])
        grau_min = min(graus.values())
        grau_max = max(graus.values())
        self.floyd_warshall()
        dist_total = 0
        cont = 0
        diametro = 0
        for i in range(n):
            for j in range(n):
                if i != j and self.matriz_dist[i][j] < math.inf:
                    dist_total += self.matriz_dist[i][j]
                    cont += 1
                    diametro = max(diametro, self.matriz_dist[i][j])
        caminho_medio = dist_total / cont if cont > 0 else 0
        return {
            "num_vertices": n,
            "num_arestas": m,
            "num_arcos": a,
            "vertices_requeridos": r_vertices,
            "arestas_requeridas": r_arestas,
            "arcos_requeridos": r_arcos,
            "densidade": densidade,
            "grau_minimo": grau_min,
            "grau_maximo": grau_max,
            "caminho_medio": caminho_medio,
            "diametro": diametro,
        }

    def reconstruir_caminho(self, u, v):
        idx = {v: i for i, v in enumerate(sorted(self.V))}
        i, j = idx[u], idx[v]
        if self.matriz_dist[i][j] == math.inf:
            return []
        caminho = [v]
        while i != j:
            j = self.matriz_pred[i][j]
            caminho.insert(0, self.idx_to_v[j])
        return caminho
