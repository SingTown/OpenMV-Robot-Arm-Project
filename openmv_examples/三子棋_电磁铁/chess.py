# Copyright (c) SingTown Technology. All rights reserved.
# OpenMV.cc          SingTown.com


# 获取当前轮到谁下
def get_current_player(board, first_player='black'):
	black_count = sum(row.count('black') for row in board)
	white_count = sum(row.count('white') for row in board)
	if first_player == 'black':
		return 'black' if black_count == white_count else 'white'
	else:
		return 'white' if black_count == white_count else 'black'
 # 三子棋结算代码
# 棋盘坐标示意：
# [ (0,0) | (0,1) | (0,2) ]
# [ (1,0) | (1,1) | (1,2) ]
# [ (2,0) | (2,1) | (2,2) ]
# 棋盘为3x3二维列表，元素为'black'、'white'或None
def check_winner(board):
	"""
	检查三子棋棋盘胜负情况。
	:param board: 3x3列表，元素为'black'、'white'或None
	:return: 'black'胜, 'white'胜, 'Draw'平局, None未结束
	"""
	# 检查行
	for row in board:
		if row[0] == row[1] == row[2] and row[0] is not None:
			return row[0]
	# 检查列
	for col in range(3):
		if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
			return board[0][col]
	# 检查主对角线
	if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
		return board[0][0]
	# 检查副对角线
	if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
		return board[0][2]
	# 检查平局
	for row in board:
		for cell in row:
			if cell is None:
				return None  # 还有空位，未结束
	return 'Draw'  # 无空位且无人获胜，平局


# 三子棋AI算法（极大极小搜索）

def best_move(board, player, first_player='black'):
	"""
	计算当前棋局下player的最佳落子位置。
	:param board: 3x3列表，元素为'black'、'white'或None
	:param player: 'black'或'white'，表示AI执子
	:param first_player: 'black'或'white'，表示先手方，默认黑棋先走
	:return: (row, col) 最佳落子坐标
	"""
	opponent = 'white' if player == 'black' else 'black'

	def count_pieces(bd, color):
		return sum(row.count(color) for row in bd)

	def current_turn(bd):
		black_count = count_pieces(bd, 'black')
		white_count = count_pieces(bd, 'white')
		if first_player == 'black':
			return 'black' if black_count == white_count else 'white'
		else:
			return 'white' if black_count == white_count else 'black'

	def minimax(bd, turn):
		winner = check_winner(bd)
		if winner == player:
			return 1
		elif winner == opponent:
			return -1
		elif winner == 'Draw':
			return 0
		scores = []
		next_turn = opponent if turn == player else player
		for i in range(3):
			for j in range(3):
				if bd[i][j] is None:
					bd[i][j] = turn
					score = minimax(bd, next_turn)
					scores.append(score)
					bd[i][j] = None
		if turn == player:
			return max(scores) if scores else 0
		else:
			return min(scores) if scores else 0

	if current_turn(board) != player:
		return None
	best_score = -float('inf')
	move = None
	for i in range(3):
		for j in range(3):
			if board[i][j] is None:
				board[i][j] = player
				score = minimax(board, opponent)
				board[i][j] = None
				if score > best_score:
					best_score = score
					move = (i, j)
	if move is not None:
		return move
	return None

# # 示例用法
# if __name__ == "__main__":
# 	# black获胜
# 	board1 = [['black', 'white', 'white'],
# 			  ['black', 'black', 'white'],
# 			  ['black', None, None]]
# 	print(check_winner(board1))  # 输出: black
# 	# white获胜
# 	board2 = [['black', 'white', 'black'],
# 			  ['black', 'white', None],
# 			  [None, 'white', 'black']]
# 	print(check_winner(board2))  # 输出: white
# 	# 平局
# 	board3 = [['black', 'white', 'black'],
# 			  ['white', 'white', 'black'],
# 			  ['black', 'black', 'white']]
# 	print(check_winner(board3))  # 输出: Draw
# 	# 未结束
# 	board4 = [['black', 'white', None],
# 			  [None, 'white', 'black'],
# 			  ['black', None, 'white']]
# 	print(check_winner(board4))  # 输出: None

# 	# AI下棋示例
# 	board5 = [['black', 'white', None],
# 			  [None, 'white', 'black'],
# 			  ['black', None, None]]
# 	print("AI最佳落子:", best_move(board5, 'white'))
