import tkinter as tk
import os
from PIL import Image, ImageTk
import chess
import random



class ChessBoard(tk.Frame):
    def __init__(self, width=200, height=200, master=None):
        super().__init__(master)
        self.master = master
        self.width = width
        self.height = height
        self.board = chess.Board()
        self.tile_width = self.width / 8 - 4
        self.tile_height = self.height / 8 - 4
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.pack()
        self.piece_images = []
        self.drawn_images = []
        self.pack()
        self.initialize_board()

    def initialize_board(self):

        for i in range(8):
            for j in range(8):
                back_color = _from_rgb((181, 136, 99)) if (i + j) % 2 == 1 else _from_rgb((240, 217, 181))
                tile = self.canvas.create_rectangle(i * int(self.tile_width), j * int(self.tile_height),
                                                    (i + 1) * self.tile_width,
                                                    (j + 1) * self.tile_height, fill=back_color)

        for i in range(8):
            text = self.canvas.create_text((self.tile_width * (i + 1 / 2), self.height - 24),
                                           text=(chr((ord('A') + i))))
            text = self.canvas.create_text((self.width - 24, (i + 1 / 2) * self.tile_height), text=chr((ord('8') - i)))

        self.parse_fen_position(self.board.fen())
        self.after(1,self.update)

    def parse_fen_position(self, fen_str):
        self.piece_images = []
        for img in self.drawn_images:
            self.canvas.delete(img)

        data = fen_str.split(' ')
        board_data = data[0].split('/')
        row_count = 0
        for row_data in board_data:
            current_position = 0
            for tile_data in row_data:
                if tile_data.isdigit() and 0 < int(tile_data) < 9:
                    current_position += int(tile_data)
                else:
                    picture_path = convert_character_to_image(tile_data)
                    img = Image.open(picture_path)
                    img = img.resize((int(self.width / 8), int(self.height / 8)))
                    tk_img = ImageTk.PhotoImage(img)
                    board_img = self.canvas.create_image(
                        ((current_position + 0.5) * self.tile_width, (row_count + 0.5) * self.tile_height),
                        image=tk_img)
                    self.drawn_images.append(board_img)
                    self.piece_images.append(tk_img)

                    current_position += 1

            row_count += 1

    def update(self):
        moves = list(self.board.legal_moves)
        rand = random.randint(0,len(moves)-1)
        self.board.push(moves[rand])
        self.parse_fen_position(self.board.fen())
        print(moves)
        if not self.board.is_game_over():
            self.after(1, self.update)
        else:
            self.board.reset()
            self.after(1, self.update)


def convert_character_to_image(c):
    scriptDir = os.path.dirname(__file__)
    path = None
    if c == "r":
        path = "/Resources/br.png"
    elif c == "n":
        path = "/Resources/bn.png"
    elif c == "b":
        path = "/Resources/bb.png"
    elif c == "k":
        path = "/Resources/bk.png"
    elif c == "q":
        path = "/Resources/bq.png"
    elif c == "p":
        path = "/Resources/bp.png"
    elif c == "R":
        path = "/Resources/wr.png"
    elif c == "N":
        path = "/Resources/wn.png"
    elif c == "B":
        path = "/Resources/wb.png"
    elif c == "K":
        path = "/Resources/wk.png"
    elif c == "Q":
        path = "/Resources/wq.png"
    elif c == "P":
        path = "/Resources/wp.png"
    return (scriptDir + path)


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


root = tk.Tk()
app = ChessBoard(master=root, width=400, height=400)
app.mainloop()

