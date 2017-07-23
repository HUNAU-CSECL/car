$(function() {
        FastClick.attach(document.body);
});
function clickButton(obj){
    var obj = $(obj);
    obj.attr("disabled","disabled");/*按钮倒计时*/
    var time = 60;
    var set=setInterval(function(){
    obj.val(--time+"(s)");
    }, 1000);/*等待时间*/
    setTimeout(function(){
    obj.attr("disabled",false).val("重新获取验证码");/*倒计时*/
    clearInterval(set);
    }, 60000);
}
$(function() {
    $('#login_get').click(function() {
        tel = $('#tel-input').val();
        if (tel.length != 11){
            alert("手机号格式不正确！");
        }else{
         $.ajax({
            type: "POST",
            url: '/usecar/send_mes/',
            data: {
                tel: tel,
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
            },
            cache: false,
            dataType: 'json',
            success: function(json) {
                if (json.tel_exist == 0) {
                    alert("用户不存在");
                }
            }
        });   
        }
    });
    $('#btn-color').click(function() {
        tel = $('#tel-input').val();
        code = $('#code-input').val();
        if (tel.length != 11) {
            alert("手机号格式不正确！");
        }else if(code.length != 6){
            alert("验证码格式不正确！");
        } else {
            $.ajax({
                type: "POST",
                url: '/usecar/login_check/',
                data: {
                    tel: tel,
                    code: code,
                    csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                },
                cache: false,
                dataType: 'json',
                success: function(json) {
                    if (json.msg == 'ok') {
                        location.href = '/usecar/login_success/'
                    } else if (json.msg == 'fail_code') {
                        alert("验证码有误！");
                    } else {
                        alert("手机号有误！");
                    }
                }
            });
        }
    });
});