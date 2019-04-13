function drawBoard(canvas, boardState) {
    context = canvas.getContext('2d');
    numRows = boardState.length;
    numCols = boardState[0].length;
    console.log(numRows)
    console.log(numCols)

    width = 700;
    height = 600;
    
    // scale canvas resolution based on device DPI
    canvas.width = width * window.devicePixelRatio;
    canvas.height = height * window.devicePixelRatio;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';

    // color canvas yellow
    context.fillStyle = 'yellow';
    context.fillRect(0, 0, canvas.width, canvas.height);

    radius = (width/numRows)/2;
    margin = 25
    console.log(radius)

    for (var r = 0; r < numRows; r++) {
	for (var c = 0; c < numCols; c++) {
	    var centerX = (radius*2 + margin) * (c) + radius + margin;
	    var centerY = (radius*2 + margin) * (r) + radius + margin;
	    context.beginPath();
	    context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);

	    if (boardState[r][c] == 1) {
		context.fillStyle = 'red';
	    }
	    else if (boardState[r][c] == 2) {
		context.fillStyle = 'black';
	    }
	    else {
		context.fillStyle = 'white';
	    }
	    context.fill();
	}
    }
}
