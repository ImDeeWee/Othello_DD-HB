import numpy as np
import othello


def creer_table_heuristiques():
    """
    Retourne un dictionnaire des valeurs heuristiques pour chaque case (row, col) d'un plateau 8x8.
    """
    # On définit la matrice des valeurs telles que montrées dans l'image.
    valeurs = [
        [500,  -150,   30,   10,   10,   30, -150,  500],
        [-150, -250,    0,    0,    0,    0, -250, -150],
        [  30,    0,    2,    2,    2,    2,    0,   30],
        [  10,    0,    2,   16,   16,    2,    0,   10],
        [  10,    0,    2,   16,   16,    2,    0,   10],
        [  30,    0,    2,    2,    2,    2,    0,   30],
        [-150, -250,    0,    0,    0,    0, -250, -150],
        [ 500, -150,   30,   10,   10,   30, -150,  500]
    ]

    # On construit un dictionnaire dont la clé est (row, col) et la valeur est la pondération heuristique.
    heuristiques = {}
    for row in range(8):
        for col in range(8):
            heuristiques[(row, col)] = valeurs[row][col]

    return heuristiques

def getAllPlayerCases(board, player):
    """
    Retourne toutes les cases de player
    """
    return [(row, col) for row in range(8) for col in range(8) if board[row, col] == player]

def sum_players_cases_score(board, cases, heuristique):
    """ Prend en entrée une liste de positions (cases) et calcule la somme des heuristiques. """
    sum_scores = 0
    for position in cases:
        sum_scores += heuristique.get(position, 0)  # Utiliser .get() pour éviter KeyError
    return sum_scores



def new_evalute_board(board, player, heuristique):
    """ Meilleur fonction d'évaluation """

    playerCases = getAllPlayerCases(board, player)

    # Créer une instance du jeu et copier correctement l'état du plateau
    game = othello.Othello()
    game.board = np.copy(board)  # Utiliser np.copy() pour éviter des références partagées
    validMoves = game.get_valid_moves(player)

    sum_current_player_cases = sum_players_cases_score(board, playerCases, heuristique)
    sum_valid_moves = sum_players_cases_score(board, validMoves, heuristique)

    return np.sum(board == player) + sum_current_player_cases + sum_valid_moves


