const boardElement = document.getElementById("board");
const resetButton = document.getElementById("reset");
const statusElement = document.getElementById("status");
let gameOver = false;
function renderBoard(board) {
    boardElement.innerHTML = "";
    board.forEach((row, i) => {
        row.forEach((cell, j) => {
            const button = document.createElement("button");
            button.textContent = gameOver?"":cell;
            button.addEventListener("click", () => makeMove(i, j));
            boardElement.appendChild(button);
        });
    });
}

async function makeMove(row, col) {
    if (gameOver) return;
    const response = await fetch("/play", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ row, col }),
    });

    const data = await response.json();
    if (response.ok) {
        renderBoard(data.board);
        if (data.status === "win") {
            statusElement.textContent="You win!";
            gameOver = true;
            
        }
        else if (data.status === "loss") {
            statusElement.textContent="AI wins!";
            gameOver = true;
            
        }
        else if (data.status === "draw") {
            statusElement.textContent="It's a draw!";
            gameOver = true;
        }
        else statusElement.textContent="";
    } else {
        alert(data.error);
    }
}

resetButton.addEventListener("click", async () => {
    const response = await fetch("/reset", { method: "POST" });
    const data = await response.json();
    renderBoard(data.board);
    statusElement.textContent="";
    gameOver = false;
});

(async () => {
    const response = await fetch("/reset", { method: "POST" });
    const data = await response.json();
    renderBoard(data.board);
})();
