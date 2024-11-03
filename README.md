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

  
</div>
