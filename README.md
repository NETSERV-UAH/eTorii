# eTorii
Enhanced Torii (eTorii), a distributed, multiaddress and fault-tolerant layer two network fabric protocol
```eTorii = eGA3 + Torii```

### eGA3
##### Simulator of the eGA3 address assignment implemented in Python

##### Generador de topologias para el Simulador

##### Pintor de Topolgias
###### Descripcion:
#
    * Obtiene desde un fichero de topologias generado por el generador anterior una descripcion de la topologia, 
        la analiza obteniendo de ella 2 parametros: 
        * Nodos: son representados mediante circulos, 
        * Enlaces: representados media lienas que van desde un nodo origen a un nodo destino.
    * El resultado son 4 archivos: un png, un pdf, un eps y un sgv, todos ellos con la representación de la topologia
###### Uso:
#
```sh
            python pintar_topologia.py 
```
