# BayesIA

Librerias para su funcionamiento
NewtorkX 3.0.0

Esta librería usa redes de bayes simples con construcción probabilistica.

Cuenta con dos métodos.
Nodo, en el cual definimos y recibe lo siguiente.
name: Nombre del nodo.
connections: los nodos a los que esta conectado este, también puede definirse la probabilidad de estos.
El grafo se construye automaticamente con los nodos creados. Es un grafo dirigido así que el orden de las conexiones importa.

BayesianNetwork.
Verifica los nodos y su construcción, además si la red esta completamente descrrita.
