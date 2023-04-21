""" Este modulo incluye todas las funciones para obtener la entrada del usuario. """

import random

def ingresar_jugadores():
    """ Se solicita al usuario inicial que ingrese los nombres de los jugadores separados por
        coma. La cantidad mínima es 3, y la máxima 7. """

    jugadores=list()
    condicion = True
    while condicion:
        entrada_usuario = input("Ingrese los nombres de los jugadores separados por coma: ")
        jugadores_lista = entrada_usuario.split(',')
        jugadores = [jugador.replace(' ', '') for jugador in jugadores_lista]
        if len(jugadores) < 3 or len(jugadores) > 7:
            print("La cantidad de jugadores no es correcta, debe ser de 3 a 7 jugadores."
                  " Vuelva a intentarlo.")
        else:
            random.shuffle(jugadores)
            condicion = False
    return jugadores


def ingresar_prediccion(jugador: str, numero_bazas: int) -> "dict[str, int]":
    """ Dado un jugador y la cantidad de bazas que se va a jugar, se solicita
        al usuario el ingreso de su prediccion. Se impide que la prediccion supere
        la cantidad de bazas. """

    jugador_prediccion = dict()
    condicion = True
    while condicion:
        try:
            prediccion = int(input(f"{jugador}, cuantas bazas cree que ganará?: "))
            # Hay que corroborar que se ingrese un número Y que se encuentre en el rango.
            if prediccion >= 0 and prediccion <= numero_bazas:
                jugador_prediccion[jugador] = prediccion
                condicion = False
            else: print("El número excede la cantidad de bazas posible")
        except ValueError:
            print("Debe ingresar un número")
    return jugador_prediccion


def ingresar_jugada(jugador: str) -> int:
    condicion = True
    jugada=1
    while condicion:
        try:
            jugada = int(input(f"\n{jugador}, qué carta desea jugar?: "))
            condicion = False
        except ValueError:
            input("Debe ingresar un número.")
    return jugada
