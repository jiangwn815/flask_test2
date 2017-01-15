function updateSelect(target, items){
    var sl = document.querySelector(target);
    while(sl.children.length>1){
        sl.removeChild(sl.children[sl.children.length-1]);
    }
    for(var key in items){
        var item=document.createElement("option");
        item.innerText=items[key];
        item.value=key;
        sl.appendChild(item);
    }
}
function ajax(method, url, data) {
    var request = new XMLHttpRequest();
    return new Promise(function (resolve, reject) {
        request.onreadystatechange = function () {
            if (request.readyState === 4) {
                if (request.status === 200) {
                    resolve(request.responseText);
                } else {
                    reject(request.status);
                }
            }
        };
        request.open(method, url);
        request.send(data);
    });
}


function changeArea(){


    function success(info){
        var jsonInfo = eval("("+info+")");
        var areas={};
        for(var index in jsonInfo.di){
            var item = jsonInfo.di[index];
            areas[item.slice(item.length-3,item.length)] = item.slice(0,item.length-3);
        }
        updateSelect("#area", areas);
    }
    var re;
    /*
    if(window.XMLHttpRequest){
        re = new XMLHttpRequest();
    }else{
        re = new ActiveXObject('Microsoft.XMLHTTP');
    }

    re.onreadystatechange=function(){
        if(re.readyState === 4){
            if(re.status === 200){
                return success(re.responseText);
            }
        }
    }

    re.open("GET","/get_area?pval="+document.querySelector("#district").value);
    re.send();*/
    re = ajax("GET","/get_area?pval="+document.querySelector("#district").value);
    re.then(success);

}

function init(){
    var districts={
        cy:"朝阳",
        dc:"东城",
        xc:"西城",
        hd:"海淀",
        ft:"丰台",
        sjs:"石景山",
        mtg:"门头沟",
        fs:"房山",
        dx:"大兴",
        tz:"通州",
        hr:"怀柔",
        pg:"平谷",
        sy:"顺义",
        my:"密云",
        cp:"昌平",
        yq:"延庆",
    };
    updateSelect("#district", districts);

    var sl=document.querySelector("#district");
    sl.onchange = changeArea;
}
init();