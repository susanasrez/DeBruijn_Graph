# Ensamblado a partir de fragmentos utilizando grafos de Bruijn y algoritmos de grafos

<div align="justify">
  
  ## 1. Creación de la definición del grafo
  
  Para dfinir el grafo de Bruijn, se utiliza el módulo `create`, que contiene la clase necesaria para este proceso. Esta clase, a partir de una lista de $k$-mers, genera un diccionario en el que las claves representan los prefijos de los $k-mers$ y los valores corresponden a los sufijos asociados. 
  
  ## 2. Construcción del grafo
  
  Para este propósito, se dispone de dos módulos con implementaciones distintas: uno basado en la biblioteca `NetworkX` y otro en la biblioteca `IGraph`. Cada módulo incluye una clase principal que gestiona todos los métodos de las clases, una clase dedicada al cálculo del ciclo o camino Euleriano y otra clase destinada a la visualización del grafo. La Figura 1 presenta un resumen general del paquete `de_bruijn_algorithm`, el cual se detallará en profundidad a continuación.
  
  <div align="center">
    <img src="images/uml_model.png" alt="Modelo completo" />
      <p><strong>Figura 1.</strong> Diagrama de clases del algoritmo.</p> 
  </div>

  ### 2.1. Paquete `networkx`

  Este paquete implementa toda la lógica necesaria para construir un grafo, calcular su ciclo o camino euleriano, y representarlo gráficamente mediante la librería `networkx` de Python. A continuación se detallan las tres clases principales que componen el paquete:
  - **`NetworkxGraph`**: Esta clase es responsable de construir el grafo, llamar a la clase encargada de su representación gráfica y ejecutar el cálculo del ciclo o camino euleriano. Además, es la interfaz principal para proporcionar los resultados o detalles al usuario final.
  - **`GraphDrawer`**: Esta clase se encarga de dibujar el grafo, mostrando o no el camino euleriano, según corresponda.
  - **`EulerianPathFinder`**: Esta clase es la responsable de verificar la existencia de un ciclo euleriano. Si no se cumple esta condición, verifica si existen las condiciones necesarias para un camino euleriano y, de ser posible, lo devuelve. En caso de que no exista un camino euleriano, devuelve el camino entre dos nodos especificados como inicio y fin, aunque este no sea euleriano. También muestra qué condiciones se cumplen o no para los distintos tipos de caminos.

  ### 2.2. Paquete `igraph`

  Este paquete implementa una lógica similar al paquete anterior, con la salvedad de que 

</div>
