function drawBoard(canvas, gameState) {
    context = canvas.getContext('2d');
    boardState = gameState.boardState;
    numRows = boardState.length;
    numCols = boardState[0].length;

    width = 100 * numRows;
    height = 100 * numCols;
    
    // scale canvas resolution based on device DPI
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';

    // color canvas white
    context.fillStyle = 'white';
    context.fillRect(0, 0, canvas.width, canvas.height);

    rectSize = canvas.width/numRows;
    context.font = '30px monospace';

    player1Pos = gameState.player1Pos;
    player2Pos = gameState.player2Pos;

    context.fillStyle = 'green';
    context.strokeStyle = 'white';
    context.beginPath();
    context.rect(player1Pos[0] * rectSize + rectSize/3, player1Pos[1] * rectSize + rectSize/3, rectSize/3, rectSize/3);
    context.fill();
    context.stroke();

    context.fillStyle = 'red';
    context.strokeStyle = 'white';
    context.beginPath();
    context.rect(player2Pos[0] * rectSize + rectSize/3, player2Pos[1] * rectSize + rectSize/3, rectSize/3, rectSize/3);
    context.fill();
    context.stroke();
    
    for (var r = 0; r < numRows; r++) {
	for (var c = 0; c < numCols; c++) {
	    var xPos = c * rectSize;
	    var yPos = r * rectSize;
	    context.strokeStyle = 'black';
	    context.beginPath();
	    context.rect(xPos, yPos, rectSize, rectSize);
	    context.stroke();
	    context.fillStyle = 'black';
	    context.fillText(boardState[r][c], xPos + rectSize/2 + 40, yPos + rectSize/2 - 40);
	}
    }
}
