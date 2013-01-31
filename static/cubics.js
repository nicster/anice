function draw_cubic(k) {
    var dcanvas = document.getElementById("cubic");
    var cxt = dcanvas.getContext("2d");
    cxt.lineWidth = 4;
    cxt.lineCap = 'round';
    cxt.lineJoin = 'round';

    var offset_x = 5;
    var offset_y = 5;
    var change_width = 4;

    var cds = [[59 + offset_x, 0 + offset_y], [118 + offset_x, 25 + offset_y],
               [59 + offset_x, 50 + offset_y], [0 + offset_x, 25 + offset_y],
               [59 + offset_x, 68 + offset_y], [118 + offset_x, 93 + offset_y],
               [59 + offset_x, 118 + offset_y], [0 + offset_x, 93 + offset_y]];

    var clr = [[cds[0], cds[1], cds[5], cds[4], 'rgba(234, 0, 1, 0.7)'],
                [cds[3], cds[0], cds[4], cds[7], 'rgba(132, 206, 208, 0.7)'],
                [cds[3], cds[2], cds[6], cds[7], 'rgba(255, 236, 71, 0.7)'], 
                [cds[1], cds[2], cds[6], cds[5], 'rgba(247, 171, 202, 0.7)'],
                [cds[4], cds[5], cds[6], cds[7], 'rgba(236, 214, 193, 0.7)'], 
                [cds[0], cds[1], cds[2], cds[3], 'rgba(73, 72, 72, 0.7)']];

    if (k === 0 || k == 1 || k == 4) {
        cxt.fillStyle = clr[k][4];
        cxt.lineWidth = 1;
        cxt.beginPath();
        cxt.moveTo(clr[k][3][0], clr[k][3][1]);
        for (i = 0; i < 4; i++) {
            cxt.lineTo(clr[k][i][0], clr[k][i][1]);
        }
        cxt.closePath();
        cxt.fill();
        cxt.stroke();
    }

    cxt.beginPath();
    cxt.lineWidth = change_width;
    cxt.moveTo(cds[7][0], cds[7][1]);
    cxt.lineTo(cds[4][0], cds[4][1]);
    cxt.lineTo(cds[5][0], cds[5][1]);
    cxt.moveTo(cds[4][0], cds[4][1]);
    cxt.lineTo(cds[0][0], cds[0][1]);
    cxt.closePath();
    cxt.stroke();

    if (k == 2 || k == 3 || k == 5){
        cxt.fillStyle = clr[k][4];
        cxt.lineWidth = 1;
        cxt.beginPath();
        cxt.moveTo(clr[k][3][0], clr[k][3][1]);
        for (i = 0; i < 4; i++) {
            cxt.lineTo(clr[k][i][0], clr[k][i][1]);
        }
        cxt.closePath();
        cxt.fill();
        cxt.stroke();
    }

    cxt.beginPath();
    cxt.lineWidth = change_width;
    cxt.moveTo(cds[0][0], cds[0][1]);
    cxt.lineTo(cds[3][0], cds[3][1]);
    cxt.lineTo(cds[7][0], cds[7][1]);
    cxt.lineTo(cds[6][0], cds[6][1]);
    cxt.lineTo(cds[5][0], cds[5][1]);
    cxt.lineTo(cds[1][0], cds[1][1]);
    cxt.closePath();
    cxt.stroke();

    cxt.beginPath();
    cxt.lineWidth = change_width;
    cxt.moveTo(cds[6][0], cds[6][1]);
    cxt.lineTo(cds[2][0], cds[2][1]);
    cxt.lineTo(cds[1][0], cds[1][1]);
    cxt.moveTo(cds[2][0], cds[2][1]);
    cxt.lineTo(cds[3][0], cds[3][1]);
    cxt.closePath();
    cxt.stroke();

}
