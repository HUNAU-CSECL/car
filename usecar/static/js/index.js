$(function () {
    $.ajax({
        type:"POST",
        url:'/usecar/cc_persons/',
        data:{},
        cache:false,
        dataType:'json',
        success:function(json){
            alert(json);
        }
    });
});