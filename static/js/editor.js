class object {
    constructor(obj) {
        this.x1 = 0;
        this.y1 = 0;
        this.x2 = obj.width;
        this.y2 = obj.height;
        this.width = obj.width;
        this.height = obj.height;
        this.z = max_z;
        this.isDragging = false;
        this.isResizing = false;
        this.resizeType = -1;
    }
}

class Text extends object {
    constructor(obj) {
        super(obj);
        this.text = obj.text;
        this.font = obj.font;
        this.size = obj.size;
        this.color = obj.color;
        this.bold = obj.bold;
        this.cursive = obj.cursive;
        this.underline = obj.underline;
    }
}

class Img extends object {
    constructor(obj) {
        super(obj);
        this.img = obj;
        this.originalPropotion = obj.height / obj.width;
    }
}


let canvas, context,
    canvasWidth = 800, canvasHeight = 800,
    minWidth = 50, minHeight = 50,
    objects = [],
    dragOK = false,
    startX, startY,
    offsetX, offsetY,
    max_z = 0,
    selected = null;

function init() {
    canvas = document.getElementById("editor");
    context = canvas.getContext("2d");
    canvas.width = canvasWidth;
    canvas.height = canvasHeight;
    canvas.style.background = "#444444";

    [...document.querySelectorAll('canvas')].forEach(canvas => {
        canvas.addEventListener('mousemove', function (e) {
            offsetX = e.target.offsetLeft;
            offsetY = e.target.offsetTop;
        });
    });

    canvas.onmousedown = myDown;
    canvas.onmouseup = myUp;
    canvas.onmousemove = myMove;
    draw();
}

function myMove(e) {
    if (dragOK) {
        let mx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft - offsetX;
        let my = e.clientY + document.body.scrollTop + document.documentElement.scrollTop - offsetY;

        let dx = mx - startX;
        let dy = my - startY;
        console.log(startX, mx);
        if (selected != null && objects[selected].isDragging) {
            objects[selected].x1 += dx;
            objects[selected].y1 += dy;
            objects[selected].x2 = objects[selected].x1 + objects[selected].width;
            objects[selected].y2 = objects[selected].y1 + objects[selected].height;
        } else if (selected != null && objects[selected].isResizing) {
            if (objects[selected].resizeType === 0) {
                dx = Math.min(dx, objects[selected].width - minWidth);
                dy = Math.min(dy, objects[selected].height - minHeight);
                objects[selected].width -= dx;
                objects[selected].height -= dy;
                objects[selected].x1 += dx;
                objects[selected].y1 += dy;
            } else if (objects[selected].resizeType === 1) {
                dx = Math.max(dx, minWidth - objects[selected].width);
                dy = Math.min(dy, objects[selected].height - minHeight);
                objects[selected].width += dx;
                objects[selected].height -= dy;
                objects[selected].x2 += dx;
                objects[selected].y1 += dy;
            } else if (objects[selected].resizeType === 2) {
                dx = Math.max(dx, minWidth - objects[selected].width);
                dy = Math.max(dy, minHeight - objects[selected].height);
                objects[selected].width += dx;
                objects[selected].height += dy;
                objects[selected].x2 += dx;
                objects[selected].y2 += dy;
            } else if (objects[selected].resizeType === 3) {
                dx = Math.min(dx, objects[selected].width - minWidth);
                dy = Math.max(dy, minHeight - objects[selected].height);
                objects[selected].width -= dx;
                objects[selected].height += dy;
                objects[selected].x1 += dx;
                objects[selected].y2 += dy;
            }
        }

        draw();
        startX = mx;
        startY = my;
    }
}

function myUp(e) {
    dragOK = false;
    for (let i = 0; i < objects.length; i++) {
        objects[i].isDragging = false;
        objects[i].isResizing = false;
    }
}

function myDown(e) {
    let mx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft - offsetX;
    let my = e.clientY + document.body.scrollTop + document.documentElement.scrollTop - offsetY;

    dragOK = true;
    console.log('down', mx, my);
    let clicked = null;
    for (let i = 0; i < objects.length; i++) {
        if (mx > objects[i].x1 && mx < objects[i].x2 && my > objects[i].y1 && my < objects[i].y2) {
            if (clicked == null || objects[i].z > objects[clicked].z)
                clicked = i;
        } else if (i === selected) {
            if (0 <= objects[i].x1 - mx && objects[i].x1 - mx < 5 && 0 <= objects[i].y1 - my && objects[i].y1 - my < 5) {
                objects[i].isResizing = true;
                objects[i].resizeType = 0;
            } else if (0 <= mx - objects[i].x2 && mx - objects[i].x2 < 5 && 0 <= objects[i].y1 - my && objects[i].y1 - my < 5) {
                objects[i].isResizing = true;
                objects[i].resizeType = 1;
            } else if (0 <= mx - objects[i].x2 && mx - objects[i].x2 < 5 && 0 <= my - objects[i].y2 && my - objects[i].y2 < 5) {
                objects[i].isResizing = true;
                objects[i].resizeType = 2;
            } else if (0 <= objects[i].x1 - mx && objects[i].x1 - mx < 5 && 0 <= my - objects[i].y2 && my - objects[i].y2 < 5) {
                objects[i].isResizing = true;
                objects[i].resizeType = 3;
            } else {
                objects[i].isResizing = false;
                objects[i].resizeType = -1;
            }
            if (objects[i].isResizing) {
                objects[i].isDragging = false;
                startX = mx;
                startY = my;
                return;
            }
        }
    }

    selected = clicked;
    if (clicked != null) {
        objects[clicked].isDragging = true;
        startX = mx;
        startY = my;
    }
    draw();
}

function drawSquares(img) {
    context.fillStyle = "#23FFCB";
    context.fillRect(img.x1 - 5, img.y1 - 5, 5, 5);
    context.fillRect(img.x2, img.y1 - 5, 5, 5);
    context.fillRect(img.x2, img.y2, 5, 5);
    context.fillRect(img.x1 - 5, img.y2, 5, 5);
}

function drawImage(e) {
    context.drawImage(e.img, e.x1, e.y1, e.width, e.height);
}

function drawText(e) {
    context.font = e.size + ' ' + e.font;
    context.fillStyle = e.color;
    e.width = context.measureText(e.text).width;
    e.height = parseInt(e.size.match(/\d+/), 10);
    e.x2 = e.x1 + e.width;
    e.y2 = e.y1 + e.height;
    context.fillText(e.text, e.x1, e.y2);
}

function draw() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    objects.sort(function (a, b) {
        if (a.z < b.z)
            return -1;
        else if (a.z === b.z)
            return 0;
        else
            return 1;
    });

    for (let i = 0; i < objects.length; i++) {
        if (objects[i].constructor.name === 'Img') {
            drawImage(objects[i]);
            if (i === selected)
                drawSquares(objects[i]);
        }
        else {
            drawText(objects[i]);
        }
    }
}

function addImage(img) {
    objects.push(new Img(img));
    max_z += 1;
}

function addText(text) {
    let a = new Text(text);
    objects.push(a);
    max_z += 1;
}