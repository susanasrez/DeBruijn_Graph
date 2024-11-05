# Ensamblado a partir de fragmentos utilizando grafos de Bruijn y algoritmos de grafos

<div align="justify">
  
  ## 1. Creación de la definición del grafo
  
  Para dfinir el grafo de Bruijn, se utiliza el módulo `create`, que contiene la clase necesaria para este proceso. Esta clase, a partir de una lista de $k-mers$, genera un diccionario en el que las claves representan los prefijos de los $k-mers$ y los valores corresponden a los sufijos asociados. 
  
  ## 2. Implementación del algoritmo
  
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

  Este paquete implementa una lógica similar a la del paquete anterior, con la diferencia de que la biblioteca `igraph` no incluye algoritmos para calcular ciclos o caminos eulerianos; en su lugar, proporciona funcionalidad para calcular caminos entre dos nodos. Por lo tanto, las clases del paquete son similares a las del paquete `networkx`, con la particularidad de que la clase **`EulerianPathFinder`** implementa métodos para calcular manualmente los ciclos o caminos eulerianos, cuando estos existen.

  ## 3. Determinación de un Ciclo o Camino Euleriano

  Como bien ya se ha explicado previamente, en cada paquete se contiene una clase la cual es la encargada de realizar la búsqueda. A continuación se explicará únicamente la implementación del paquete `networkx` ya que es aquel más simple puesto que la librería proporciona algoritmos y funciones que lo facilitan:
  - `_is_eulerian_cycle()`: etermina si el grafo tiene un ciclo euleriano verificando que, para cada nodo, los grados de entrada y salida sean iguales y si el grafo es fuertemente conexo. Si no se cumplen estas condiciones, `cycle_conditions` explica por qué no existe un ciclo euleriano, y el método devuelve `False`.
  - `_is_eulerian_path()`: determina si el grafo tiene un camino euleriano. Para ello verificatres condiciones:
    1. La mayoría de nodos deben tener el mismo grado de entrada y salida.
    2. Debe haber exactamente un nodo con un grado de salida mayor en 1 (nodo de inicio).
    3. Debe haber exactamente un nodo con un grado de entrada mayor en 1 (nodo de fin).
    Si las condiciones no se cumplen, se proporciona una explicación en `path_conditions` sobre la falta de nodos válidos o grados no coincidentes. El método devuelve `False`.
  - `find_eulerian_path(graph)`: Este método busca un ciclo o camino euleriano en el grafo proporcionado.
    1. Intenta primero encontrar un ciclo euleriano llamando a `_is_eulerian_cycle`.
       - Si existe, usa `nx.eulerian_circuit` para obtener el ciclo y lo guarda en `self.eulerian_paths`.
    2. Si no existe un ciclo, intenta encontrar un camino euleriano llamando a `_is_eulerian_path`.
       - Si existe un camino, llama al método `find_all_eulerian_paths` para encontrar todos los caminos posibles y los almacena en `self.eulerian_paths`.
    3. Finalmente, devuelve `self.eulerian_paths` con los caminos o ciclos encontrados.
  - `find_all_eulerian_paths()`: Este método encuentra todos los posibles caminos eulerianos entre nodos válidos de inicio y fin.
    1. Identifica los nodos de inicio y fin posibles (aquellos que tienen un grado de entrada y salida desbalanceado).
  2. Si hay un solo par de nodos de inicio y fin, utiliza `nx.eulerian_path` para obtener el camino y lo agrega a `self.eulerian_paths`.
  3. Si hay múltiples pares de nodos de inicio y fin, genera combinaciones posibles de ellos y usa `nx.all_simple_paths` para encontrar caminos simples entre estos nodos.
     - De estos caminos simples, selecciona el camino más largo y lo convierte en una lista de aristas.
     - Agrega el camino a `self.eulerian_paths`.
  4. Si se encuentran varios caminos eulerianos, `path_conditions` señala que el grafo tiene múltiples caminos posibles. Finalmente, devuelve `self.eulerian_paths`.
  - `get_conditions()`: Este método devuelve las condiciones para los ciclos y caminos eulerianos calculados en los métodos `_is_eulerian_cycle` y `_is_eulerian_path`. Proporciona la justificación sobre si el grafo cumple o no con las condiciones necesarias para tener un ciclo o un camino euleriano.

  ## 4. Reconstrucción de la Secuencia Original: Clase `SequenceAssembler`
  
  Esta clase es la responsable de ensamblar la secuencia original de ADN con la particularidad de que, a pesar de no haber encontrado un camino euleriano o ciclo exacto, intenta aproximar la secuencia añadiendo huecos de los $kmers$ faltantes. En el notebook se porprociona un ejemplo claro que permite visualizar la aporximación. Para ello, implementa los siguientes métodos:
  - `assemble_sequence`: Este método realiza el ensamblaje de las secuencias de ADN a partir de los caminos eulerianos.
    1. Verifica si hay caminos eulerianos (`self.eulerian_paths`). Si no hay, devuelve `None`.
    2. Para cada camino en `self.eulerian_paths`, construye una secuencia de ADN agregando las últimas letras de cada nodo en el camino. Cada secuencia ensamblada se agrega a `self.dna_sequences`.
    3. Si solo hay una secuencia en `self.dna_sequences`, la devuelve directamente.
    4. Si hay varias secuencias, toma la más larga y la alinea con los $kmers$ restantes para asegurar la continuidad, llamando al método `align_kmers_with_gaps`.
  - `align_kmers_with_gaps(sequence)`: Este método alinea los $kmers$ faltantes con la secuencia dada para completar la secuencia ensamblada.
    1. Encuentra los $kmers$ que ya están en la secuencia y los que no, con el método `all_kmers_sequence`.
    2. Los $kmers$ faltantes se superponen para formar secuencias continuas usando `superpose_kmers`.
    3. Utiliza un bucle para verificar si el sufijo de la secuencia actual coincide con el prefijo de algún $kmer$ en los $kmers$ superpuestos. Si encuentra coincidencias, se agrega el $kmer$ a la secuencia ensamblada. Si no encuentra coincidencias, agrega un guion (`-`) seguido del primer $kmer$ faltante.
    4. Devuelve la secuencia resultante con los $kmers$ alineados.
  - `check_prefix(suffix, kmer, k)`: Este método verifica si el `suffix` (sufijo) coincide con el `prefix` (prefijo) de un $kmer$ dado.
  - `all_kmers_sequence(sequence)`: Este método verifica cuáles de los $kmers$ están presentes en la secuencia dada.
  - `superpose_kmers(kmers_not_in_sequence)`: Este método toma los $kmers$ que no están en la secuencia y trata de superponerlos para formar secuencias continuas.
  - `find_overlap(self, kmer1, kmer2)`: Este método encuentra el mayor solapamiento entre dos $kmers$.

## 4. Manejo de casos erróneos

### 4.1. Construcción de un Grafo con Múltiples Caminos de Salida desde un Nodo

Inicialmente, se propuso definir la estructura del grafo utilizando un diccionario en Python. Sin embargo, dado que en un diccionario las claves son únicas, solo se permite asignar un único valor a cada clave. Para solucionar este inconveniente, en lugar de asociar un único nodo como valor, se definirá el valor como una lista de nodos, permitiendo así especificar todas las aristas salientes de cada nodo.

### 4.2. Manejo y explicación de las condiciones de conectividad o grado de los nodos
Para ello, se han definido dos variables de clase que permiten identificar, en caso de ausencia de alguno de los tipos de caminos, las condiciones que no se cumplen.

En primer lugar, para los ciclos eulerianos, estas variables especifican qué nodos no cumplen con la condición de tener igual número de aristas de entrada y de salida. También indican si el grafo no es fuertemente conexo, es decir, que para cualquier par de nodos $u$ y $v$ en el grafo, existe un camino dirigido de  $u$ a $v$ y otro de $v$ a  $u$. Un ejemplo de grafo que no cumple las condiciones para un ciclo euleriano, pero sí para un camino euleriano, es el de la Figura 2. Las condiciones específicas que no se cumplen en este grafo son las siguientes:

<div align="center">
    <img src="images/grafo_camino.png" alt="Grafo camino" width = 700 />
      <p><strong>Figura 2.</strong> Grafo que no contiene un ciclo euleriano.</p> 
  </div>

<h4> No tiene un ciclo euleriano porque: </h4> <li> El nodo AGT tiene 0 aristas de entrada y 1 aristas de salida. </li> <li> El nodo ACG tiene 2 aristas de entrada y 1 aristas de salida. </li> <li> El grafo no es fuertemente conexo. </li>

En segundo lugar, para los caminos eulerianos, se deben cumplir las siguientes condiciones:
- Existe un nodo cuyo grado de salida excede en una unidad al grado de entrada, siendo este nodo el punto de inicio del camino euleriano.
- Existe un nodo cuyo grado de entrada es una unidad mayor que su grado de salida, y este nodo representa el final del camino euleriano.
- Todos los demás nodos deben tener grados de entrada y salida iguales.

Un caso atípico es la Figura 3, que muestra un grafo con múltiples nodos de inicio y fin, lo que implica caminos entre combinaciones de estos nodos. Las condiciones específicas que no se cumplen en este caso son las siguientes:

<div align="center">
    <img src="images/grafo_no_camino.png" alt="Grafo camino" width = 700 />
      <p><strong>Figura 3.</strong> Grafo que no contiene un camino euleriano.</p> 
  </div>


<h4> El grafo tiene múltiples caminos entre los nodos. </h4>
<li>Camino Euleriano 1: GA -> AC -> CT -> TT -> TA -> AT -> TG -> GT</li>
<li>Camino Euleriano 2: GA -> AC -> CT -> TT -> TA -> AT -> TG</li>
<li>Camino Euleriano 3: CT -> TT -> TA -> AC -> CG -> GT</li>
<li>Camino Euleriano 4: CT -> TT -> TA -> AC -> CG -> GT -> TG</li>


### 4.3. Posibilidad de Ensamblar la Secuencia Original y Método de Corrección o Compleción de la Secuencia

Como se ha presentado previamente, el caso atípico corresponde al ejemplo 3 del notebook. En consecuencia, dado que no es posible ensamblar la secuencia original mediante un camino euleriano, se propone emplear el algoritmo descrito en el apartado cuatro para intentar completar la secuencia. De este modo, la secuencia final ensamblada, aunque incompleta y con huecos, sería la siguiente:

<h4>Secuencia original:</h4>Secuencia posible: GACTTATGT-TACGT-ACGTG-CTA

 
</div>
