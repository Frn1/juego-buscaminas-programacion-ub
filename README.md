# Buscsaminas

Celda:

- Desconocida
- Marcada/Con bandera
- Revelada

Tablero:

- Dimensiones del tablero
- Distribuir las minas de forma aleatoria (Evitando poner minas donde ya fue revelado, ya que el primer toque debe ser seguro)
- - Cuando se revela una posicion, se marca como revelada, se utilizaría la función de arriba (si es necesario/no hay minas todavía), y se sigue con el resto
- Funcion que dice si hay una mina en una posicion
- Si una posicion fue revelada o si tiene una bandera (El estado de la celda)

Partida:

- Cuente las minas alrededor de una posicion
- Cambiar el estado de una Celda a otro estado, y que devuelva si el juego sigue, o tocaste una mina
- - Si una celda estaba "desconocida", se puede cambiar a "marcada" o "revelada"
- - Si una celda estaba "marcada", se puede cambiar a "desconocida"
- - Si una celda estaba "revelada", no se puede cambiar de ese estado
- Una funcion para determinar si ganaste (Cuando la cantidad de celdas no reveladas == la cantidad de minas en el tablero)

<!--* Despejo automatico (Si la cantidad de celdas no reveladas == la cantidad de minas alrededor de esa posicion, marcar/poner bandera las no reveladas)-->

Intefaz:

- Mostrar tablero
- Revelar celda
- Marcar/poner bandera en celda
- etc. no se, lo vamos viendo
