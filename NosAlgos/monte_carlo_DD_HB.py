# Node dans l'arbre de recherche
class Node:
    def __init__(self, board, parent, move, playerJustMoved):
        self.board = board.copy()
        self.parent = parent
        self.move = move
        self.playerJustMoved = playerJustMoved
        self.children = []
        self.wins = 0.0
        self.visits = 0
        self.untried_moves = None
        self.game = Othello()

    # Calcule et renvoie les coups légaux du prochain joueur
    def get_untried_moves(self):
        if self.untried_moves is None:
            next_player = -self.playerJustMoved
            self.game.board = self.board
            self.untried_moves = self.game.get_valid_moves(next_player)
        return self.untried_moves

    # Développe un nouvel enfant
    def expand(self):
        moves = self.get_untried_moves()
        if not moves:
            return None
        idx = np.random.randint(len(moves))
        move = moves.pop(idx)
        next_player = -self.playerJustMoved
        self.game.board = self.board.copy()
        self.game.apply_move(move, next_player)
        child_node = Node(self.game.board, parent=self, move=move, playerJustMoved=next_player)
        self.children.append(child_node)
        return child_node

    # Vérifie si le noeud est terminal
    def is_terminal_node(self):
        self.game.board = self.board
        black_moves = self.game.get_valid_moves(BLACK)
        white_moves = self.game.get_valid_moves(WHITE)
        return len(black_moves) == 0 and len(white_moves) == 0

    # Sélectionne le meilleur enfant en utilisant UCB
    def best_child(self, c_param=1.414):
        best_child = None
        best_value = -float('inf')
        
        explore_factor = min(1.0, 5.0 / np.sqrt(self.visits + 1))
        
        for child in self.children:
            exploit = child.wins / child.visits if child.visits > 0 else 0
            explore = c_param * np.sqrt(np.log(self.visits) / child.visits) if child.visits > 0 else float('inf')
            
            position_value = 0
            if child.move:
                r, c = child.move
                if (r == 0 and c == 0) or (r == 0 and c == 7) or (r == 7 and c == 0) or (r == 7 and c == 7):
                    position_value = 0.5

                elif ((r <= 1 and c <= 1) or (r <= 1 and c >= 6) or 
                      (r >= 6 and c <= 1) or (r >= 6 and c >= 6)):
                    position_value = -0.3

                elif r == 0 or c == 0 or r == 7 or c == 7:
                    position_value = 0.2
            
            value = exploit + explore_factor * explore + 0.1 * position_value
            
            if value > best_value:
                best_value = value
                best_child = child
                
        return best_child


def rollout(board, player):
    game = Othello()
    game.board = board.copy()
    current_player = player
    depth = 0
    max_depth = 50  
    
    while not game.is_game_over() and depth < max_depth:
        valid_moves = game.get_valid_moves(current_player)
        if valid_moves:

            corner_moves = []
            edge_moves = []
            other_moves = []
            
            for move in valid_moves:
                r, c = move
                if (r == 0 and c == 0) or (r == 0 and c == 7) or (r == 7 and c == 0) or (r == 7 and c == 7):
                    corner_moves.append(move)
                elif r == 0 or c == 0 or r == 7 or c == 7:
                    edge_moves.append(move)
                else:
                    other_moves.append(move)
            
           
            if corner_moves and np.random.random() < 0.9:  
                move = corner_moves[np.random.randint(len(corner_moves))]
            elif edge_moves and np.random.random() < 0.7:  
                move = edge_moves[np.random.randint(len(edge_moves))]
            else:
                move = valid_moves[np.random.randint(len(valid_moves))]
                
            game.apply_move(move, current_player)
        current_player = -current_player
        depth += 1
    
    
    black_count = np.sum(game.board == BLACK)
    white_count = np.sum(game.board == WHITE)
    
    
    if depth == max_depth and not game.is_game_over():
        
        corners = [(0,0), (0,7), (7,0), (7,7)]
        black_corners = sum(1 for r, c in corners if game.board[r][c] == BLACK)
        white_corners = sum(1 for r, c in corners if game.board[r][c] == WHITE)
        
        
        black_mobility = len(game.get_valid_moves(BLACK))
        white_mobility = len(game.get_valid_moves(WHITE))
        
        
        black_score = black_count + 5 * black_corners + 0.5 * black_mobility
        white_score = white_count + 5 * white_corners + 0.5 * white_mobility
        
        score = black_score - white_score
    else:
        score = black_count - white_count
    
    if score > 0:
        return BLACK
    elif score < 0:
        return WHITE
    else:
        return None  

# remonte résultat de simulation dans l'arbre
def backpropagate(node, result):
    while node is not None:
        node.visits += 1
        
        if result is None:
            node.wins += 0.5
        elif node.playerJustMoved == result:
            node.wins += 1.0
        else:
            
            node.wins += 0.1
        node = node.parent

# Exécute algorithme Monte Carlo Tree Search
def mcts(root, iterations):
    
    remaining_time = iterations
    early_iterations = min(int(iterations * 0.2), 2000)  
    
    
    for _ in range(early_iterations):
        node = root
        
        while node.get_untried_moves() == [] and node.children and not node.is_terminal_node():
            node = node.best_child(c_param=1.8)  
        
        if node.get_untried_moves() and not node.is_terminal_node():
            node = node.expand()
            if node is None:  
                continue
        
        next_player = -node.playerJustMoved
        result = rollout(node.board, next_player)
        
        backpropagate(node, result)
    
    
    remaining_time -= early_iterations
    for _ in range(remaining_time):
        node = root
        
        while node.get_untried_moves() == [] and node.children and not node.is_terminal_node():
            node = node.best_child(c_param=1.0)  
       
        if node.get_untried_moves() and not node.is_terminal_node():
            node = node.expand()
            if node is None:
                continue
        
        next_player = -node.playerJustMoved
        result = rollout(node.board, next_player)
        
        backpropagate(node, result)
    
    
    if not root.children:
        return None
    
    
    total_pieces = np.sum(np.abs(root.board))
    if total_pieces < 20:  
       
        for child in root.children:
            if child.move:
                r, c = child.move
                if (r == 0 and c == 0) or (r == 0 and c == 7) or (r == 7 and c == 0) or (r == 7 and c == 7):
                    if child.visits > root.children[0].visits * 0.7: 
                        return child.move
    

    best_child_node = max(root.children, key=lambda n: n.visits)
    return best_child_node.move


def user_ai(board, player):
    iterations = 10000 # Set a 10k pour ce tp mais augmenter donne meilleur résultat (Exemple 15k donne 54 points)
    root = Node(board, parent=None, move=None, playerJustMoved=-player)
    return mcts(root, iterations)