import numpy as np
from enum import Enum
import re
from typing import List, Tuple, Optional

# Define piece type enum
class PieceType(Enum):
    EMPTY = 0
    PAWN = 1
    ROOK = 2
    KNIGHT = 3 
    BISHOP = 4
    QUEEN = 5
    KING = 6

# Define piece color enum    
class Color(Enum):
    NONE = 0
    WHITE = 1
    BLACK = 2

# Represents a chess piece
class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False
        
    def __str__(self):
        # Unicode chess symbols for displaying pieces
        symbols = {
            (PieceType.PAWN, Color.WHITE): '♙',
            (PieceType.ROOK, Color.WHITE): '♖',
            (PieceType.KNIGHT, Color.WHITE): '♘', 
            (PieceType.BISHOP, Color.WHITE): '♗',
            (PieceType.QUEEN, Color.WHITE): '♕',
            (PieceType.KING, Color.WHITE): '♔',
            (PieceType.PAWN, Color.BLACK): '♟',
            (PieceType.ROOK, Color.BLACK): '♜',
            (PieceType.KNIGHT, Color.BLACK): '♞',
            (PieceType.BISHOP, Color.BLACK): '♝',
            (PieceType.QUEEN, Color.BLACK): '♛',
            (PieceType.KING, Color.BLACK): '♚',
        }
        return symbols.get((self.piece_type, self.color), ' ')

class ChessBoard:
    def __init__(self):
        # Initialize empty board and game state
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = Color.WHITE
        self.last_move = None
        self.move_count = 0
        self.position_history = []
        self.en_passant_target = None
        self.initialize_board()
        
    def initialize_board(self):
        # Initialize white pieces
        self.board[7] = [
            Piece(PieceType.ROOK, Color.WHITE),
            Piece(PieceType.KNIGHT, Color.WHITE),
            Piece(PieceType.BISHOP, Color.WHITE),
            Piece(PieceType.QUEEN, Color.WHITE),
            Piece(PieceType.KING, Color.WHITE),
            Piece(PieceType.BISHOP, Color.WHITE),
            Piece(PieceType.KNIGHT, Color.WHITE),
            Piece(PieceType.ROOK, Color.WHITE)
        ]
        self.board[6] = [Piece(PieceType.PAWN, Color.WHITE) for _ in range(8)]
        
        # Initialize black pieces
        self.board[0] = [
            Piece(PieceType.ROOK, Color.BLACK),
            Piece(PieceType.KNIGHT, Color.BLACK),
            Piece(PieceType.BISHOP, Color.BLACK),
            Piece(PieceType.QUEEN, Color.BLACK),
            Piece(PieceType.KING, Color.BLACK),
            Piece(PieceType.BISHOP, Color.BLACK),
            Piece(PieceType.KNIGHT, Color.BLACK),
            Piece(PieceType.ROOK, Color.BLACK)
        ]
        self.board[1] = [Piece(PieceType.PAWN, Color.BLACK) for _ in range(8)]
        
        # Initialize empty squares
        for i in range(2, 6):
            self.board[i] = [None for _ in range(8)]
            
    def display(self):
        # Display the current board state
        print("   a  b  c  d  e  f  g  h")
        print("  -------------------------")
        for i in range(8):
            print(f"{8-i}|", end=" ")
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    print(".", end="  ")
                else:
                    print(piece, end=" ")
            print(f"|")

    def algebraic_to_index(self, algebraic: str) -> tuple:
        # Convert algebraic notation (e.g. 'e4') to array indices
        if not re.match(r'^[a-h][1-8]$', algebraic):
            raise ValueError("Invalid algebraic notation")
        col = ord(algebraic[0]) - ord('a')
        row = 8 - int(algebraic[1])
        return (row, col)

    def index_to_algebraic(self, row: int, col: int) -> str:
        # Convert array indices to algebraic notation
        return f"{chr(col + ord('a'))}{8-row}"

    def is_valid_position(self, row: int, col: int) -> bool:
        # Check if position is within board bounds
        return 0 <= row < 8 and 0 <= col < 8

    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        # Get piece at specified position
        if not self.is_valid_position(row, col):
            return None
        return self.board[row][col]

    def is_path_clear(self, from_row: int, from_col: int, to_row: int, to_col: int) -> bool:
        # Check if path between two points is clear of pieces
        row_step = 0 if from_row == to_row else (to_row - from_row) // abs(to_row - from_row)
        col_step = 0 if from_col == to_col else (to_col - from_col) // abs(to_col - from_col)
        
        row, col = from_row + row_step, from_col + col_step
        while (row, col) != (to_row, to_col):
            if self.get_piece(row, col) is not None:
                return False
            row += row_step
            col += col_step
        return True

    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        # Get all valid moves for piece at specified position
        piece = self.get_piece(row, col)
        if piece is None:
            return []
            
        valid_moves = []
        
        if piece.piece_type == PieceType.PAWN:
            direction = -1 if piece.color == Color.WHITE else 1
            if self.is_valid_position(row + direction, col) and self.get_piece(row + direction, col) is None:
                valid_moves.append((row + direction, col))
                if (not piece.has_moved and 
                    self.is_valid_position(row + 2*direction, col) and
                    self.get_piece(row + 2*direction, col) is None):
                    valid_moves.append((row + 2*direction, col))
            
            # Diagonal captures
            for c in [col-1, col+1]:
                if self.is_valid_position(row + direction, c):
                    target = self.get_piece(row + direction, c)
                    if target and target.color != piece.color:
                        valid_moves.append((row + direction, c))
                        
            # En passant
            if self.en_passant_target:
                if (row == self.en_passant_target[0] and 
                    abs(col - self.en_passant_target[1]) == 1):
                    valid_moves.append((row + direction, self.en_passant_target[1]))
                    
        elif piece.piece_type == PieceType.ROOK:
            # Horizontal and vertical moves
            for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
                r, c = row + direction[0], col + direction[1]
                while self.is_valid_position(r, c):
                    target = self.get_piece(r, c)
                    if target is None:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
                    
        elif piece.piece_type == PieceType.KNIGHT:
            # L-shaped moves
            moves = [
                (row+2, col+1), (row+2, col-1),
                (row-2, col+1), (row-2, col-1),
                (row+1, col+2), (row+1, col-2),
                (row-1, col+2), (row-1, col-2)
            ]
            for r, c in moves:
                if self.is_valid_position(r, c):
                    target = self.get_piece(r, c)
                    if target is None or target.color != piece.color:
                        valid_moves.append((r, c))
                        
        elif piece.piece_type == PieceType.BISHOP:
            # Diagonal moves
            for direction in [(1,1), (1,-1), (-1,1), (-1,-1)]:
                r, c = row + direction[0], col + direction[1]
                while self.is_valid_position(r, c):
                    target = self.get_piece(r, c)
                    if target is None:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
                    
        elif piece.piece_type == PieceType.QUEEN:
            # Combined rook and bishop moves
            directions = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]
            for direction in directions:
                r, c = row + direction[0], col + direction[1]
                while self.is_valid_position(r, c):
                    target = self.get_piece(r, c)
                    if target is None:
                        valid_moves.append((r, c))
                    elif target.color != piece.color:
                        valid_moves.append((r, c))
                        break
                    else:
                        break
                    r += direction[0]
                    c += direction[1]
                    
        elif piece.piece_type == PieceType.KING:
            # One square in any direction
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if (r,c) != (row,col) and self.is_valid_position(r, c):
                        target = self.get_piece(r, c)
                        if target is None or target.color != piece.color:
                            valid_moves.append((r, c))
            
            # Castling
            if not piece.has_moved and not self.is_in_check(piece.color):
                # Kingside castle
                rook = self.get_piece(row, 7)
                if (rook and rook.piece_type == PieceType.ROOK and 
                    not rook.has_moved and 
                    self.is_path_clear(row, col, row, 7) and
                    not self.is_square_attacked(row, col+1, piece.color) and
                    not self.is_square_attacked(row, col+2, piece.color)):
                    valid_moves.append((row, col+2))
                
                # Queenside castle
                rook = self.get_piece(row, 0)
                if (rook and rook.piece_type == PieceType.ROOK and 
                    not rook.has_moved and 
                    self.is_path_clear(row, col, row, 0) and
                    not self.is_square_attacked(row, col-1, piece.color) and
                    not self.is_square_attacked(row, col-2, piece.color)):
                    valid_moves.append((row, col-2))
                    
        # Filter moves that would result in check
        filtered_moves = []
        for move in valid_moves:
            original_piece = self.board[move[0]][move[1]]
            self.board[move[0]][move[1]] = piece
            self.board[row][col] = None
            
            if not self.is_in_check(piece.color):
                filtered_moves.append(move)
            
            # Restore position
            self.board[row][col] = piece
            self.board[move[0]][move[1]] = original_piece
            
        return filtered_moves

    def is_square_attacked(self, row: int, col: int, color: Color) -> bool:
        # Check if square is attacked by opponent
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color != color:
                    target = self.board[row][col]
                    self.board[row][col] = None
                    moves = self.get_valid_moves(r, c)
                    self.board[row][col] = target
                    
                    if (row, col) in moves:
                        return True
        return False

    def is_in_check(self, color: Color) -> bool:
        # Check if king is in check
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if (piece and piece.piece_type == PieceType.KING and 
                    piece.color == color):
                    king_pos = (r, c)
                    break
            if king_pos:
                break
                
        if not king_pos:
            return False
                
        return self.is_square_attacked(king_pos[0], king_pos[1], color)

    def is_checkmate(self, color: Color) -> bool:
        # Check if king is in checkmate
        if not self.is_in_check(color):
            return False
        
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == color:
                    if self.get_valid_moves(r, c):
                        return False
        return True

    def is_stalemate(self, color: Color) -> bool:
        # Check if position is stalemate
        if self.is_in_check(color):
            return False
            
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color == color:
                    if self.get_valid_moves(r, c):
                        return False
        return True

    def make_move(self, from_pos: str, to_pos: str) -> bool:
        # Make a move on the board
        try:
            from_row, from_col = self.algebraic_to_index(from_pos)
            to_row, to_col = self.algebraic_to_index(to_pos)
            
            piece = self.get_piece(from_row, from_col)
            if piece is None or piece.color != self.current_turn:
                return False
                
            valid_moves = self.get_valid_moves(from_row, from_col)
            if (to_row, to_col) not in valid_moves:
                return False
                
            # Special move handling
            if piece.piece_type == PieceType.KING and abs(from_col - to_col) == 2:
                # Castling
                rook_col = 7 if to_col > from_col else 0
                rook_new_col = 5 if to_col > from_col else 3
                rook = self.get_piece(from_row, rook_col)
                self.board[from_row][rook_new_col] = rook
                self.board[from_row][rook_col] = None
                rook.has_moved = True
                
            elif piece.piece_type == PieceType.PAWN:
                # Set en passant target
                if abs(to_row - from_row) == 2:
                    self.en_passant_target = (to_row, to_col)
                else:
                    if (self.en_passant_target and
                        (to_row, to_col) == (self.en_passant_target[0] + (-1 if piece.color == Color.WHITE else 1), 
                                           self.en_passant_target[1])):
                        self.board[self.en_passant_target[0]][self.en_passant_target[1]] = None
                
                # Promotion
                if to_row in [0, 7]:
                    print("Choose promotion piece:")
                    print("1. Queen")
                    print("2. Rook")
                    print("3. Bishop") 
                    print("4. Knight")
                    while True:
                        try:
                            choice = int(input("Enter number (1-4): "))
                            if 1 <= choice <= 4:
                                piece_types = {
                                    1: PieceType.QUEEN,
                                    2: PieceType.ROOK,
                                    3: PieceType.BISHOP,
                                    4: PieceType.KNIGHT
                                }
                                piece = Piece(piece_types[choice], piece.color)
                                break
                            else:
                                print("Please enter valid number (1-4)")
                        except ValueError:
                            print("Please enter valid number")
            else:
                self.en_passant_target = None
            
            # Record move
            self.last_move = ((from_row, from_col), (to_row, to_col))
            
            # Check if capturing king
            target = self.get_piece(to_row, to_col)
            if target and target.piece_type == PieceType.KING:
                self.board[to_row][to_col] = piece
                self.board[from_row][from_col] = None
                print(f"Game Over! {piece.color.name} wins!")
                return True
            
            # Execute move
            self.board[to_row][to_col] = piece
            self.board[from_row][from_col] = None
            piece.has_moved = True
            
            # Switch turn
            self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
            
            # Check for check
            if self.is_in_check(self.current_turn):
                print("Check!")
                print(f"{self.current_turn.name} king is under attack!")
            
            self.move_count += 1
            
            return True
            
        except ValueError:
            return False

def play_chess():
    board = ChessBoard()
    while True:
        try:
            board.display()
            current_player = "White" if board.current_turn == Color.WHITE else "Black"
            print(f"\n{current_player}'s turn")
            
            # Check if any king is captured
            white_king_exists = False
            black_king_exists = False
            for r in range(8):
                for c in range(8):
                    piece = board.get_piece(r, c)
                    if piece and piece.piece_type == PieceType.KING:
                        if piece.color == Color.WHITE:
                            white_king_exists = True
                        else:
                            black_king_exists = True
            
            if not white_king_exists:
                print("Black wins!")
                break
            elif not black_king_exists:
                print("White wins!")
                break
            
            if board.is_checkmate(board.current_turn):
                print(f"Checkmate! {'Black' if board.current_turn == Color.WHITE else 'White'} wins!")
                break
                
            if board.is_stalemate(board.current_turn):
                print("Stalemate!")
                break
                
            # Check if king is in check
            if board.is_in_check(board.current_turn):
                print(f"{current_player}'s king is in check!")
                
            from_pos = input("Enter piece to move (e.g. e2): ").strip()
            if from_pos.lower() == 'resign':
                print(f"{current_player} resigns! {'Black' if board.current_turn == Color.WHITE else 'White'} wins!")
                break
                
            to_pos = input("Enter destination (e.g. e4): ").strip()
            
            if board.make_move(from_pos, to_pos):
                print("Move successful!")
            else:
                print("Invalid move!")
                
        except KeyboardInterrupt:
            print("\nGame ended!")
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            continue

if __name__ == "__main__":
    play_chess()
