import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        ratings = list(map(lambda x: float(x), ratings))
        ratingsOptions = list(map(lambda x: ft.dropdown.Option(x), ratings))
        self._view._ddrating1.options = ratingsOptions
        self._view._ddrating2.options = ratingsOptions
        self._view.update_page()

    def handleCreaGrafo(self, e):
        vMin = self._view._ddrating1.value
        vMax = self._view._ddrating2.value

        if vMin is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un voto minimo!", color="red"))
            self._view.update_page()
            return

        if vMax is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, seleziona un voto massimo!", color="red"))
            self._view.update_page()
            return

        vMinFloat = float(vMin)
        vMaxFloat = float(vMax)

        if vMinFloat > vMaxFloat:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, il voto minimo deve essere più piccolo del voto massimo!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(vMinFloat, vMaxFloat)
        nodes, edges = self._model.graphDetails()
        top5Archi = self._model.getTop5Edges()
        numComp, maxComp = self._model.getConnectedComponents()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {edges}"))
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for edge in top5Archi:
            self._view.txt_result.controls.append(ft.Text(f"{edge[0]} -> {edge[1]} : {edge[2]['weight']}"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numComp} componenti connesse."))
        self._view.txt_result.controls.append(ft.Text(f"La più grande componente connessa è lunga {len(maxComp)}:"))
        for node in maxComp:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()

    def handleCammino(self, e):
        if not self._model.isGraphOk():
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, devi prima creare il grafo!", color="red"))
            self._view.update_page()
            return

        bestPath, bestLun = self._model.bestPath()
        if bestPath is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Non è stato trovato alcun cammino!", color="red"))
            self._view.update_page()
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Trovato un cammino di lunghezza {bestLun}:"))
        for node in bestPath:
            self._view.txt_result.controls.append(ft.Text(node))
        self._view.update_page()