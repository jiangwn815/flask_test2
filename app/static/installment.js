function ajax_func() {
    var jsonsub={};
    jsonsub={a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val(),
        c: $('input[name="mobile"]').val()};
    $('#ins-form [type!=null]').map(function(){
        jsonsub[this.name]=this.type+this.value;
        //jsonsub[this.id]=this.innerHTML;
    });

    $.getJSON('/_add_numbers', jsonsub, function(data) {
        $("#result").text(data.result);
        $("#s4").text(data.str);
    });
    return false;
}

function Dsy() {
        this.Items = {};
}
Dsy.prototype.add = function (id, iArray) {
    this.Items[id] = iArray;
}
Dsy.prototype.Exists = function (id) {
    if (typeof(this.Items[id]) == "undefined")
        return false;
    return true;
}

var s = ["s1", "s2", "s3"];
var opt0 = ["请选择", "请选择", "请选择"];

function change(v) {
    console.log("change "+v+"  start!!!!!!!");
    var i=0;
    var str = "0";

    for (i = 1; i < v; i++) {
    str += ("_" + (document.getElementById("s"+i).selectedIndex - 1));
    }

    var ss = document.getElementById("s"+v);
    with (ss) {
        length = 0;
        options[0] = new Option(opt0[v-1], opt0[v-1]);
        if (v && document.getElementById("s"+(v - 1)).selectedIndex > 0 || !v) {
            if (dsy.Exists(str)) {
                ar = dsy.Items[str];
                for (i = 0; i < ar.length; i++)options[length] = new Option(ar[i], ar[i]);
                if (v)options[0].selected = true;
            }
        }
        //if (++v < s.length) {change(v);}
    }
    }
    var dsy = new Dsy();

    dsy.add("0", ["东城区", "西城区", "朝阳区", "丰台区", "石景山区", "海淀区", "门头沟区", "房山区", "通州区", "顺义区", "昌平区", "大兴区", "怀柔区", "平谷区", "密云县", "延庆县"]);

    dsy.add("0_0", ["二环内"]);
    dsy.add("0_0_0", ["朝阳门营业厅","广渠门营业厅","小街桥营业厅"]);


    dsy.add("0_1", ["内环到二环里","二环外到三环"]);
    dsy.add("0_1_0", ["新街口营业厅","西单营业厅"]);
    dsy.add("0_1_1", ["官园营业厅","德胜营业厅","虎坊路营业厅","马连道营业厅","三里河营业厅"]);


    dsy.add("0_2", ["朝二环内","三环内","四环五环内"]);
    dsy.add("0_2_0", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_2_1", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_2_2", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);

    dsy.add("0_3", ["丰二环内","三环内","四环五环内"]);
    dsy.add("0_3_0", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_3_1", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_3_2", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);

    dsy.add("0_4", ["石二环内","三环内","四环五环内"]);
    dsy.add("0_4_0", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_4_1", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);
    dsy.add("0_4_2", ["xx营业厅","小现营业厅","想法士大夫营业厅"]);

function changeAddress(){
    console.log("changeText start!");
    var textDict={"xx营业厅":"不知道在哪里","小现营业厅":"还没有开","想法士大夫营业厅":"wow"};
    if(document.getElementById("s3").selectedIndex>0){
        document.getElementById("text").innerHTML=textDict[document.getElementById("s3").value];
	}
}
function checkMobile(){
    var mobilereg=/^1[35789]\d{9}$/;
    var no=document.getElementById("mobile").value.replace(/\s*/g,"");
    document.getElementById("mobile").value=no;
    if (!mobilereg.test(no)){
        document.getElementById("text").innerHTML="请输入11位手机号码";
    }
}
function jqcheckMobile(){
    var mobilereg=/^1[35789]\d{9}$/;
    var no=$('#mobile').val().replace(/\s*/g,"");
    $('#mobile').val(no);
    if (!mobilereg.test(no)){
        $("#text").text('请输入11位手机号码');
    }
}
function cleanWarning(){
    document.getElementById("s5").innerHTML="";
}
function jqcleanWarning(){
    $('#text').text('');
}

function setup() {
    document.getElementById("s3").onchange = changeAddress;
    document.getElementById("mobile").onblur = checkMobile;
    document.getElementById("mobile").onfocus = cleanWarning;
    document.getElementById("calculate").onclick = ajax_func;

    for (i = 1; i < s.length ; i++){
    //new Function为包装对象 这样再typeof结果就是object而不是function
        document.getElementById("s"+i).onchange = new Function("change(" + (i + 1) + ");");
    }
}
function jqsetup() {
    $('#s3').change(changeAddress);
    $('#mobile').blur(jqcheckMobile);
    $('#mobile').focus(jqcleanWarning);
    $('#calculate').click(ajax_func);

    for (i = 1; i < s.length ; i++){
    //new Function为包装对象 这样再typeof结果就是object而不是function
        //document.getElementById("s"+i).onchange = new Function("change(" + (i + 1) + ");");
        $('#s'+i).change(new Function("change(" + (i + 1) + ");"));
    }
}
//window.onload = jqsetup;
$(function(){
    jqsetup();
});