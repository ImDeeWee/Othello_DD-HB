

# Supposons que vous importiez Othello, BLACK, WHITE, etc. depuis othello.py
# from othello import Othello, BLACK, WHITE, EMPTY

myPlayer = None
def creer_table_heuristiques():
    """
    Retourne un dictionnaire des valeurs heuristiques pour chaque case (row, col) d'un plateau 8x8.
    """
    valeurs = [
        [500,  -150,   30,   10,   10,   30,  -150,  500],
        [-150, -250,    0,    0,    0,    0,  -250, -150],
        [  30,    0,    2,    2,    2,    2,     0,   30],
        [  10,    0,    2,   16,   16,    2,     0,   10],
        [  10,    0,    2,   16,   16,    2,     0,   10],
        [  30,    0,    2,    2,    2,    2,     0,   30],
        [-150, -250,    0,    0,    0,    0,  -250, -150],
        [ 500,  -150,   30,   10,   10,   30,  -150,  500]
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
    s = 0
    for position in cases:
        s += heuristique_table.get(position, 0)
    return s

def new_evaluate_board(board, player):
    """
    Fonction d'évaluation améliorée combinant :
      - la différence de pions (critère 1),
      - la somme des heuristiques associées à chaque position occupée (critère 2),
      - la mobilité (nombre de coups possibles) (critère 3).
    """
    # On crée une instance Othello pour avoir accès à get_valid_moves()
    game = Othello()
    game.board = board

    # Critère 1 : différence (pions NOIRS - pions BLANCS)
    #  (ou l’inverse si vous préférez, selon qui est "player")
    if myPlayer == BLACK:
        critere_1 = np.sum(board == BLACK) - np.sum(board == WHITE)
    else:
        critere_1 = np.sum(board == WHITE) - np.sum(board == BLACK)

    # Critère 2 : somme des heuristiques du joueur
    player_positions = getAllPlayerCases(board, player)
    critere_2 = sum_players_cases_score(board, player_positions)

    # Critère 3 : mobilité (nombre de coups possibles pour 'player')
    valid_moves_count = len(game.get_valid_moves(player))

    # Combinaison linéaire simple (vous pouvez ajuster les coefficients)
    return critere_1 + critere_2 + valid_moves_count


def alpha_beta_upgraded(board, depth, alpha, beta, maximizing, player):
    """
    Implémentation de l'algorithme alpha-beta avec évaluation améliorée.

    :param board:  l’état courant du plateau (numpy array 8x8)
    :param depth:  profondeur restante à explorer
    :param alpha:  valeur alpha pour l'elagage
    :param beta:   valeur beta pour l'elagage
    :param maximizing: booléen pour savoir si on est dans la branche de maximisation
    :param player: le joueur courant (BLACK ou WHITE)

    :return: (score, best_move)
    """
    game = Othello()
    game.board = board.copy()

    # Condition d'arrêt si profondeur == 0 ou le jeu est fini
    if depth == 0 or game.is_game_over():
        return new_evaluate_board(game.board, player), None

    valid_moves = game.get_valid_moves(player)
    if not valid_moves:
        # Si aucun coup n'est disponible, on "passe" : on diminue la profondeur
        return alpha_beta_upgraded(board, depth - 1, alpha, beta, not maximizing, -player)

    best_move = None

    if maximizing:
        value = float("-inf")
        for move in valid_moves:
            # Simuler le coup
            new_game = Othello()
            new_game.board = board.copy()
            new_game.apply_move(move, player)

            eval_score, _ = alpha_beta_upgraded(
                new_game.board,
                depth - 1,
                alpha,
                beta,
                False,     # on passe en mode minimizing
                -player    # l’adversaire
            )

            if eval_score > value:
                value = eval_score
                best_move = move

            alpha = max(alpha, value)
            # Coupure (élagage) si alpha >= beta
            if alpha >= beta:
                break
        return value, best_move
    else:
        value = float("inf")
        for move in valid_moves:
            # Simuler le coup
            new_game = Othello()
            new_game.board = board.copy()
            new_game.apply_move(move, player)

            eval_score, _ = alpha_beta_upgraded(
                new_game.board,
                depth - 1,
                alpha,
                beta,
                True,      # on passe en mode maximizing
                -player
            )

            if eval_score < value:
                value = eval_score
                best_move = move

            beta = min(beta, value)
            if beta <= alpha:
                break
        return value, best_move


def user_ai(board, player):
    """
    IA utilisant l'algorithme alpha-beta pour choisir un coup.
    On utilise 7 plis comme suggéré. Vous pouvez ajuster.
    """
    myPlayer = player
    depth = 7
    maximizingBool = (depth % 2 == 0)
    alpha = float("-inf")
    beta = float("inf")
    best_score, best_move = alpha_beta_upgraded(board, depth, alpha, beta, maximizingBool, player)
    return best_move
