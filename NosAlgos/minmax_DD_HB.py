# MEME SI IL Y A DES ERREURS DE SYNTAXE DANS LE FICHIER, IL DEVRAIT FONCTIONNER DANS LA PAGE WEB AVEC UN COPY/PASTE.

# 1ER AVIS: Le minmax fonctionne, mais il est fucking long. On peut essayer d'ameliorer la complexite de l'algo (tant qu'en espace qu'en temps)

myPlayer = None
def creer_table_heuristiques():
    """
    Retourne un dictionnaire des valeurs heuristiques pour chaque case (row, col) d'un plateau 8x8.
    """
    valeurs = [
        [500, -150, 30, 10, 10, 30, -150, 500],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [30, 0, 2, 2, 2, 2, 0, 30],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [10, 0, 2, 16, 16, 2, 0, 10],
        [30, 0, 2, 2, 2, 2, 0, 30],
        [-150, -250, 0, 0, 0, 0, -250, -150],
        [500, -150, 30, 10, 10, 30, -150, 500]
    ]

    heuristiques = {}
    for row in range(8):
        for col in range(8):
            heuristiques[(row, col)] = valeurs[row][col]
    return heuristiques


heuristique_table = creer_table_heuristiques()

def getAllPlayerCases(board, player):
    """
    Retourne toutes les positions sur le plateau occupées par le joueur.
    """
    # np.argwhere retourne un tableau de coordonnées (row, col)
    positions = np.argwhere(board == player)

    return [tuple(pos) for pos in positions]


def sum_players_cases_score(board, cases):
    """
    Calcule la somme des valeurs heuristiques pour une liste de positions.
    """
    sum_scores = 0
    for position in cases:
        sum_scores += heuristique_table.get(position, 0)
    return sum_scores


def new_evalute_board(board, player):
    """
    Fonction d'évaluation améliorée qui combine :
      - le nombre de pièces du joueur,
      - la somme des heuristiques des cases occupées,
      - et la somme du nombre de coups possibles.
    """
    playerCases = getAllPlayerCases(board, player)
    game = Othello()
    game.board = board

    if myPlayer == BLACK:
        critere_1 = np.sum(board == BLACK) - np.sum(board == WHITE)
    else:
        critere_1 = np.sum(board == WHITE) - np.sum(board == BLACK)

    critere_2 = sum_players_cases_score(board, playerCases)
    critere3 = len(game.get_valid_moves(player))

    return   critere_1 + critere_2 + critere3


def minimax_upgraded(board, depth, maximizing, player):
    """
    Minimax amélioré avec limite de profondeur.

    Arguments :
      - board : l'état actuel du plateau
      - depth : la profondeur restante d'exploration
      - maximizing : booléen indiquant si c'est le tour du joueur maximisant
      - player : le joueur courant (par exemple, BLACK ou WHITE)

    Retourne un tuple (score, meilleur_coup).
    """
    # Créer une instance de jeu pour exploiter les méthodes existantes
    game = Othello()
    game.board = board.copy()

    if depth == 0 or game.is_game_over():
        return new_evalute_board(game.board, player), None

    valid_moves = game.get_valid_moves(player)

    # Si aucun coup n'est possible, on passe le tour (en diminuant la profondeur)
    if not valid_moves:
        return minimax_upgraded(board, depth - 1, not maximizing, -player)

    best_move = None

    if maximizing:
        max_eval = float("-inf")
        for move in valid_moves:
            # Simuler le coup sur une copie du plateau
            new_game = Othello()
            new_game.board = board.copy()
            new_game.apply_move(move, player)
            eval_score, _ = minimax_upgraded(new_game.board, depth - 1, False, -player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in valid_moves:
            new_game = Othello()
            new_game.board = board.copy()
            new_game.apply_move(move, player)
            eval_score, _ = minimax_upgraded(new_game.board, depth - 1, True, -player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move





def user_ai(board, player):
    """
    Wrapper de l'IA qui initialise la table d'heuristiques et lance le minimax amélioré.
    """
    myPlayer = player
    depth = 6
    maximizingBool = (depth % 2 == 0)
    _, best_move = minimax_upgraded(board, depth, maximizingBool, player)
    return best_move
