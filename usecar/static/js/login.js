$(function () {
    $('#send_sms').click(function () {
        tel = $('#tel').val();
        $.ajax({
            type:"POST",
            url:'/usecar/send_mes/',
            data:{
                tel:tel,
            },
            cache:false,
            dataType:'json',
            success:function(json){
                if (json.tel_exist==1) {
                    alert("success!");
                }else{
                    alert("failed!");
                }
            }
        });
    });
    $('#login').click(function () {
        tel = $('#tel').val();
        code = $('#code').val();
        $.ajax({
            type:"POST",
            url:'/usecar/login_check/',
            data:{
                tel:tel,
                code:code,
            },
            cache:false,
            dataType:'json',
            success:function(json){
                if (json.msg=='ok') {
                    location.href = '/usecar/login_success/'
                }else if (json.msg=='fail_code') {
                    alert("验证码有误！");
                }else{
                    alert("帐号有误！");
                }
            }
        });
    });
});