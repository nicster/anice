window.onload = draw_cubic;

function draw_cubic() {
    var dcanvas = document.getElementById("cubic");    
    var cxt = dcanvas.getContext("2d");
    cxt.lineWidth = 4;

    var offset_x = 5;
    var offset_y = 5;

    var cds = [[59 + offset_x, 0 + offset_y], [118 + offset_x, 25 + offset_y], 
                [59 + offset_x, 50 + offset_y], [0 + offset_x, 25 + offset_y], 
                [59 + offset_x, 68 + offset_y], [118 + offset_x, 93 + offset_y], 
                [59 + offset_x, 118 + offset_y], [0 + offset_x, 93 + offset_y]];

    var clr = [[cds[0], cds[1], cds[5], cds[4]], [cds[3], cds[0], cds[4], cds[7]], 
                [cds[3], cds[2], cds[6], cds[7]], [cds[1], cds[2], cds[6], cds[5]],
                [cds[4], cds[5], cds[6], cds[7]], [cds[0], cds[1], cds[2], cds[3]]];

    cxt.fillStyle = "#FF0000";
    cxt.beginPath();
    cxt.moveTo(clr[0][3][0], clr[0][3][1]);
    for (var i = 0; i < 4; i++) {
        cxt.lineTo(clr[0][i][0], clr[0][i][1]);
    }
    cxt.closePath();
    cxt.fill();

    cxt.beginPath();            
    cxt.moveTo(cds[0][0], cds[0][1]);
    cxt.lineTo(cds[3][0], cds[3][1]);
    cxt.lineTo(cds[7][0], cds[7][1]);
    cxt.lineTo(cds[6][0], cds[6][1]);
    cxt.lineTo(cds[5][0], cds[5][1]);
    cxt.lineTo(cds[1][0], cds[1][1]);
    cxt.closePath();
    cxt.moveTo(cds[7][0], cds[7][1]);
    cxt.lineTo(cds[4][0], cds[4][1]);
    cxt.lineTo(cds[5][0], cds[5][1]);
    cxt.moveTo(cds[4][0], cds[4][1]);
    cxt.lineTo(cds[0][0], cds[0][1]);
    cxt.stroke();
}
