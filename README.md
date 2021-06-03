<h1 align="center">
  Generador de analizadores sintácticos
</h1>

<p align="center">Universidad del Valle de Guatemala</p>
<p align="center">Diseño de Lenguajes de Programación</p>
<p align="center">Proyecto # 3</p>
<p align="center">Rodrigo Samayoa - 17332</p>
<p align="center">02/06/2021</p>

<hr />

## De que trata

<h4>El proyecto consiste en la implementación de un generador de analizadores sintácticos, tomando como base un subconjunto de las características de COCOr. El programa aceptará como entrada un archivo en COCOl, con la especificación del  analizadores sintácticos a generar, y dará como salida un archivo fuente, el cual implementará el parser basado en la gramática ingresada.<h4>

# Descripción de herramientas  y archivos

## Listado de herramientas usadas para el proyecto

- Python 3.8.0
  - Una versión de Python igual o mayor a Python 3.8.1 64bits
- Graphviz
  - Es una librería que permite graficar los nodos. [link de descarga](https://graphviz.org/download/)
- pickle
  - Libreria para serializar objetos. [link de documentación](https://docs.python.org/3/library/pickle.html)
- pprint
  - Libreria para imprimir y mostrar los caracteres especiales
- Terminal
  - Terminal de la computadora o terminal de VS Code

## Archivos y carpetas
1. main.py: Programa principal donde se lee el archivo COCOl y se genera el scanner.py.
2. funciones.py: Programa con funciones auxiliares para poder operar y ordenar los Characters que se leen en main.py.
3. directo.py: Programa donde se genera el AFD con el algoritmo directo.
4. nodoD.py: Clase que contiene las propiedades necesarias que necesita el metodo de directo para poder ser generado.
5. tipoChar.py: Clase con las propiedades necesarias para poder guardar los caracteres o characters que tiene cada token.
6. postfix.py: Programa que contiene las funciones necesarias para pasar a postfix los tokens leídos en main.py.
7. scanner.py: Programa generado a partir del main.py para obtener los tokens que encuentra en el txt dependiendo de la gramatica ingresada.
8. tipoCharProd.py: Clase con las propiedades necesarias para poder guardar en un objeto cada elemento de las producciones.
9. tokenScanner.py: Clase con las propiedades necesarias para poder guardar en un objeto el token que lee el scanner.
10. postfixPod.py: Programa que contiene las funciones necesarias para pasar a postfix las producciones leídas en main.py.
11. parser.py: Programa generado a partir del main.py para obtener los resultados de la/s operacion/es que tiene el archivo de prueba.
8. cocols: Carpeta donde se encuentra la gramaticas que se puede usar al ejecutar main.py

## Link Youtube
#### Video que explica todo el programa y las funciones:
https://youtu.be/REMnOp17aFQ

## Orden de como correr el proyecto

- Abrir terminal.
    - Ir al path donde este todo el proyecto.
- Ejecutar en la consola el programa `main.py` por medio del comando `python3 main.py`.
    - Al correrlo debe escribr el nombre completo del archivo ATG que se encuentra en la carpeta "cocols" y tambien el nombre del archivo de prueba.
    - Esto generara o actualizara 7 diferentes archivos:
        - diccioAceptacion: Contiene un diccionario donde se definen los estados de aceptacion de cada token.
        - pilaFinal: Contiene el AFD.
        - arrayTokens: Array que contiene los diferentes tokens que estan definidos en el ATG. Tanto los anonimos como los que estan definidos en la seccion de tokens.
        - diccionarioTokensLeidos: Diccionario que tiene como key el caracter del token y como valor el numero en el que se encontro el token.
        - tokensLeidos: Array de objetos de los tokens que lee el scanner.
        - scanner.py: Programa que leyendo el archivo de prueba saca los tokens que encuentra .
        - parser.py: Programa a ejecutar en siguiente paso.
- Luego ejecutar `parser.py` por medio del comando `python3 parser.py`.
    - Esto le imprimira en consola el resultado que obtenga dependiendo del lenguaje del ATG y del archivo de prueba.