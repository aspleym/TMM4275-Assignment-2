
var mLength = 100;
var mWidth = 100;
var mazeComplexity = 4;
var mazeName = null;
var fileList = [];

const lengthInput = document.getElementById("mLength");
const widthInput = document.getElementById("mWidth");

lengthInput.addEventListener("change", () => {
  mLength = lengthInput.value;
});

widthInput.addEventListener("change", () => {
  mWidth = widthInput.value;
  console.log(mWidth);
});

const fileInput = document.getElementById("import");

fileInput.addEventListener("change", () => {
    fileList = fileInput.files;
    console.log(fileList[0]);
    mazeName = null;
    changeMazeComplexity(4);
})

const lowButton = document.getElementById("low-btn");

lowButton.addEventListener("click", () => {
    mazeComplexity = 0;
    changeMazeComplexity(0);
  });

const mediumButton = document.getElementById("medium-btn");

mediumButton.addEventListener("click", () => {
    mazeComplexity = 1;
    changeMazeComplexity(1);
  });

const highButton = document.getElementById("high-btn");

highButton.addEventListener("click", () => {
    mazeComplexity = 2;
    changeMazeComplexity(2);
  });

const extremeButton = document.getElementById("extreme-btn");
extremeButton.addEventListener("click", () => {
    mazeComplexity = 3;
    changeMazeComplexity(3);
  });

const btnGroup = [lowButton, mediumButton, highButton, extremeButton];

function changeMazeComplexity(value) {
    for (var i in btnGroup) {
        if (i == parseInt(value)) {
            btnGroup[i].style.backgroundColor = "#008cff";
            btnGroup[i].style.color = "#fff";
            mazeName = "url=../Maze/maze" + value + ".csv"
            console.log("changed to " + value);

        } else {
            btnGroup[i].style.backgroundColor = "#fff";
            btnGroup[i].style.color = "#008cff";
        }
    }
}

window.onload = () => {
    changeMazeComplexity(0);
}

window.onsubmit = (e) => {
    e.preventDefault();
    console.log("Submited");
    var request = new XMLHttpRequest();
    
    request.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log("done")
            //window.location.assign("Wall-E/order.html");
        }
    };
    if (mazeName !== null) {
        console.log(mazeName);
        request.open("POST", "");
        request.setRequestHeader("content-type", "text/plain; charset=utf-8");
        request.setRequestHeader('Access-Control-Allow-Origin', '*');
        request.send(mazeName);
    } else if (mazeName === null && fileList !== []) {
        console.log("sending file");
        var formData = new FormData();
        formData.append("file", fileList[0]);
        request.open("POST", "");
        request.setRequestHeader('Access-Control-Allow-Origin', '*');
        request.send(formData);
    }
}
