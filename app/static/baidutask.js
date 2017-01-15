var dbinfo = document.querySelector("#debug-info");
function initBaiduTask18(){
    var btns = document.querySelectorAll(".entry");
    for(var i=0;i<btns.length;i++){
        btns[i].onclick=clickRemove;
    }

    var inputNum = document.querySelector("#number-input");

    var rightIn = document.querySelector("#right-in");
    var leftIn = document.querySelector("#left-in");
    var leftOut = document.querySelector("#left-out");
    var rightOut = document.querySelector("#right-out");

    var btnArray = document.querySelector("#btn-array");
    var bubbleSort = document.querySelector("#bubble-sort");

    rightIn.onclick= clickInsert;
    leftIn.onclick= clickInsert;
    leftOut.onclick = clickOut;
    rightOut.onclick = clickOut;
    bubbleSort.onclick = clickBubbleSort;

    function clickInsert(){
        var iv = inputNum.value;
        if(/\d+/.test(iv)&& iv>9 && iv<101){
            var addedBtn = document.createElement("div");
            addedBtn.innerHTML = iv;
            inputNum.value = "";
            addedBtn.className = "entry";
            addedBtn.style.height = iv+"%";
            addedBtn.style.width = "auto";
            addedBtn.onclick = clickRemove;

            if(this.id==="left-in"){
                btnArray.insertBefore(addedBtn,btnArray.children[0]);
            }else if(this.id==="right-in"){
                btnArray.appendChild(addedBtn);
            }
        }
    }
    function clickOut(){
        if(btnArray.children.length!==0){
            if(this.id==="left-out"){
                btnArray.removeChild(btnArray.firstElementChild);
            }else if(this.id==="right-out"){
                btnArray.removeChild(btnArray.lastElementChild);
            }
        }
    }
    function clickRemove(){
        var pp = this.parentNode;
        pp.removeChild(this);
    }
    function clickBubbleSort(){
        var btnLength = btnArray.children.length;
        var j=0;
        var i=btnLength-1;
        var t;
        console.log("constructor:"+btnArray.constructor);
        console.log("constructor:"+btnArray.children[0].constructor);
        for(var l=0;l<=i;l++){
            btnArray.children[l].style.backgroundColor="red";
        }
        exchangeItem();

            function exchangeItem(){

                var aa = btnArray.children[j];
                var bb = btnArray.children[j+1];
                if(aa.style.height>bb.style.height){
                    btnArray.insertBefore(bb,aa);
                }
                j +=1;
                if(j===i){
                    j=0;
                    btnArray.children[i].style.backgroundColor="grey";
                    i--;
                }
                if(i===0){
                    btnArray.children[i].style.backgroundColor="grey";
                    return true;
                }
                t=setTimeout(exchangeItem,1000);
            }
    }

}
function initBaiduTask20(){
    var dbi = document.querySelector("#debug-info");
    var mi = document.querySelector("#multi-in");
    var sb = document.querySelector("#search-button");
        sb.onclick = function(){
        console.log("we in");
        var multiInput = document.querySelector("#multi-array");
        var divItem;
        console.log("multi-input length:"+multiInput.children.length);
        for(var i=0;i<multiInput.children.length;i++){
            divItem = multiInput.children[i];
            console.log("div item"+divItem);
            var reg = new RegExp(document.querySelector("#search-text").value);
            if(reg.test(divItem.innerHTML)){
                divItem.style.backgroundColor="red";
            }
        }
    }

    mi.onclick = function(){
        var multiInput = document.querySelector("#multi-input").value;
        var divContents = multiInput.split(/[\s\,\.\u3002\uff0c\u3001]+/);
        console.log(divContents);
        for(var item of divContents){

            addDiv(item);
        }
    };
    function addDiv(content){
        var ma = document.querySelector("#multi-array");
        var newDiv = document.createElement("div");
        newDiv.innerHTML = content;
        newDiv.className = "multi-divs btn btn-primary";
        ma.appendChild(newDiv);
    }

}

function initBaiduTask21(){
    var tags=document.querySelector("#tags");
    var tagDiv = document.querySelector("#tag-div");

    tags.onkeyup=function(){
        var tagsReg = /[\s\r\,\.\u3002\uff0c\u3001]+/;

        tagArray = tags.value.split(tagsReg);
        if(tagArray.length>1||event.keyCode===13){//keyCode === 13即用户按回车键
            if(tagArray[0]!==""){
                if(tagDiv.children.length===10){
                    tagDiv.removeChild(tagDiv.firstElementChild);
                }
                addDiv(tagDiv,tagArray[0]);
            }
            tags.value="";
        }
    };
    function addDiv(element, content){

        var newDiv = document.createElement("div");
        newDiv.innerHTML = content;
        newDiv.className = "btn btn-primary";
        element.appendChild(newDiv);
        newDiv.onmouseover=function(){
            this.style.backgroundColor="red";
            this.innerText="点击删除"+this.innerText;
        };
        newDiv.onmouseout = function(){
            this.style.backgroundColor = "grey";
        };
    }
}

initBaiduTask18();
initBaiduTask20();
initBaiduTask21();