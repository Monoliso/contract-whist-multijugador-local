""" Este módulo contiene toda la lógica para jugar una partida de Contract Whist """

import random


PALOS = ['♣️', '♥️', '♦️', '♠️']
VALORES = [str(i+1) for i in range(1, 10)] + ['J', 'Q', 'K', 'A']


def repartir_cartas(jugadores: "list[str]", numero_bazas: int) -> "tuple[dict, tuple[str, str]]":
    """ Dada una lista de jugadores y la cantidad de bazas que se juega,
        se le reparten la cantidad de cartas correspondiente a cada jugador y
        se devuelve el triunfo de la baza. """

    cartas_jugadores = dict.fromkeys(jugadores, None)
    mazo = {(x, y) for y in PALOS for x in VALORES}

    for jugador in jugadores:
        cartas_jugador = list()
        for numero_carta in range(numero_bazas):
            carta = random.choice(list(mazo))
            mazo.remove(carta)
            cartas_jugador = insertar_carta_por_palo(cartas_jugador, carta)
        cartas_jugadores[jugador] = cartas_jugador
    triunfo = random.choice(list(mazo))
    return cartas_jugadores, triunfo


def insertar_carta_por_palo(mazo_jugador: list, nueva_carta: tuple) -> "list[tuple]":
    """ Devuelve un mazo con la carta insertada en función del palo. """
    # Invirtiendo cada expresión se puede obtener un orden por valor.
    
    if mazo_jugador == []:
        return [nueva_carta]
    if mazo_jugador[0][1] == nueva_carta[1] and\
       VALORES.index(mazo_jugador[0][0]) > VALORES.index(nueva_carta[0]):
        return [nueva_carta] + mazo_jugador
    if PALOS.index(mazo_jugador[0][1]) > PALOS.index(nueva_carta[1]):
        return [nueva_carta] + mazo_jugador
    else:
        return [mazo_jugador[0]] + insertar_carta_por_palo(mazo_jugador[1:], nueva_carta)


def determinar_ganador_baza(mesa: dict, carta_baza: tuple, triunfo: tuple) -> str:
    """ Devuelve el jugador que ganó la baza. """

    palo_triunfo = triunfo[1]
    palo_baza = carta_baza[1]
    ganador = carta_baza
    for carta in mesa.keys():
        if carta[1] == palo_triunfo and\
                       (ganador[1] != palo_triunfo or
                        VALORES.index(carta[0]) > VALORES.index(ganador[0])):
            ganador = carta
        if carta[1] == palo_baza and\
                       ganador[1] != palo_triunfo and\
                       VALORES.index(carta[0]) > VALORES.index(ganador[0]):
            ganador = carta
    jugador_ganador = mesa[ganador]
    return jugador_ganador


def corroborar_jugada(cartas_jugador: "list[tuple]", jugada: int,
                      palo_baza: str, palo_triunfo: str) -> tuple:

    carta_seleccionada = cartas_jugador[jugada-1]
    palo_carta = carta_seleccionada[1]
    if palo_carta == palo_baza:
        return (True, "", [])
    if palos_baza_disponibles := obtener_indices_cartas_cierto_palo(cartas_jugador, palo_baza):
        return (False, "palo_baza", palos_baza_disponibles)
    if palo_carta == palo_triunfo:
        return (True, "", [])
    if triunfos_disponibles := obtener_indices_cartas_cierto_palo(cartas_jugador, palo_triunfo):
        return (False, "palo_triunfo", triunfos_disponibles)
    return (True, "", [])


def obtener_indices_cartas_cierto_palo(cartas: list, palo: str) -> list:
    resultado = list()
    for indice, carta in enumerate(cartas):
        if carta[1] == palo:
            resultado += [indice+1]
    return resultado


def determinar_ganador_juego(puntaje_juego: dict) -> tuple:
    """ Devuelve el o los jugadores con mayor puntaje. """

    mayor_puntaje = max(puntaje_juego.values())
    ganador_es = [jugador for jugador, puntaje in puntaje_juego if puntaje == mayor_puntaje]
    return (ganador_es, mayor_puntaje)


def determinar_puntos_mano(bazas_ganadas: dict, predicciones: dict) -> "dict[str, int]":
    """ Computa si las bazas ganadas coinciden con la predicción. Devuelve los puntos
        finales de la mano. """

    puntos_mano = dict()
    for jugador, prediccion in predicciones.items():
        if bazas_ganadas[jugador] == prediccion:
            puntos_mano[jugador] = 10 + bazas_ganadas[jugador]
        else:
            puntos_mano[jugador] = bazas_ganadas[jugador]
    return puntos_mano


def actualizar_orden_jugadores(jugadores: "list[str]", ganador_baza: str) -> "list[str]":
    """ Devuelve una lista con el orden actualizado de los jugadores en una mano. """

    numero_ganador = jugadores.index(ganador_baza)
    nueva_lista = jugadores[numero_ganador:] + jugadores[:numero_ganador]
    return nueva_lista