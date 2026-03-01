# app.py

from flask import Flask, render_template, request, redirect, session
from board import Board
import os

app = Flask(__name__)
app.secret_key = "neuralgridsecret"


def get_board():
    if "board" not in session:
        board = Board()
        session["board"] = board.to_list()
        return board

    board = Board()
    board.grid = [
        [
            None if cell is None else __import__("tile").Tile(cell["gate_type"], cell["level"])
            for cell in row
        ]
        for row in session["board"]
    ]
    return board


@app.route("/", methods=["GET", "POST"])
def index():
    board = get_board()

    if request.method == "POST":
        direction = request.form.get("move")
        board.move(direction)
        session["board"] = board.to_list()
        return redirect("/")

    session["board"] = board.to_list()

    return render_template(
        "index.html",
        grid=board.to_list(),
        win=board.check_win(),
        game_over=board.check_game_over()
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)