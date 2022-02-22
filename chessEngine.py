import chess
import chess.engine

engine = chess.engine.SimpleEngine.popen_uci("D:\Projects\Python\AutoChess\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
board=chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    print(result.move)
    board.push(result.move)

engine.quit()