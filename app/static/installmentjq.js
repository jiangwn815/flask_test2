function ajax_func() {
    var jsonsub={};
    jsonsub={a: $('input[name="a"]').val(),
        b: $('input[name="b"]').val()};
    $('#ins-form [type!=null]').map(function(){
        jsonsub[this.name]=this.value;
        jsonsub['Type:'+this.type]=this.value;

    });

    $.getJSON('/_add_numbers', jsonsub, function(data) {
        $("#result").text(data.result);

       add_option($('#testid'),data.di);

    });
    return false;
}

function changeArea(){

    var pro_val={};
    pro_val["pval"]=$('#provincejq').val();

    $.getJSON('/get_area',pro_val,function(data){
        add_option($('#areajq'),data.di);
    });
}

function add_option(id,opts){
    var opss='<option>请选择</option>';
    var count=0;
    var lis=id.find('[value!=""]').remove();
    if(opts) count=opts.length;

        for(var i=0;i<count;i++){
            opss+= '<option>'+opts[i]+'</option>';
        }

        id.append(opss);
}


function jqcheckMobile(){
    var mobilereg=/^1[35789]\d{9}$/;
    var no=$('#mobile').val().replace(/\s*/g,"");
    $('#mobile').val(no);
    if (!mobilereg.test(no)){
        $("#text").text('请输入11位手机号码');
        $('#mobile').css('background-color','#FFF200');
        return false;
    }
    return true;
}

function jqcleanWarning(){
    $('#text').text('');
    $('#mobile').css('background-color','white');
}


function jqsetup() {
    //$('#s3').change(changeAddress);
    $('#mobile').blur(jqcheckMobile);
    $('#mobile').focus(jqcleanWarning);
    $('#calculate').click(ajax_func);
    $('#provincejq').change(changeArea);

}

$(function(){
    jqsetup();
});