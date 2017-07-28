
Mock.mock('/user/car',{
    'data': [
        {
            "lic":"湘A56989",
            "stype":"丰田霸道",
            "cap":"7"
        },
        {
            "lic":"湘A50989",
            "stype":"丰田瑞美德",
            "cap":"5"
        },
        {
            "lic":"湘A55539",
            "stype":"丰田yi",
            "cap":"5"
        },
         {
            "lic":"湘A55989",
            "stype":"丰田红杉",
            "cap":"7"
        },
    ],
    "count":"15",
});

$(function(){

    // $.get("/user/car",function(result){

    //     var res = $.parseJSON(result); // 将字符串转换成json格式的对象

    //     var data = res.data;/*获取json的值*/

    //     var html='';/*给html赋值*/

    //     $.each(data, function(index,value){/*index表示有几个值，value表示值，还可以用其他的参数*/

    //          console.log(value);

    //         html+='<div class="weui-col-33">'+value.lic+'</div>';
    //         html+='<div class="weui-col-33">'+value.stype+'</div>';
    //         html+='<div class="weui-col-33">'+value.cap+'</div>';

    //     });
          
    //     $("#content").append(html);
    // });
    // 添加车辆信息提交
    $.ajax({
        url:'',
        type:'POST',
        data:{
            lic : $("#lic").val(),
            brand : $("#brand").val(),
            style :$("#style").val(),
            num :$("#num").val(),
        },
        dataType:"json",
        success:function(data){
         $("#show-toast").click(function(){
            return false;
         })
        }
    });
    // 点击加载更多
    $.ajax({
        url:'/user/car',
        type:'POST',
        data:{
            last:0,
            amout:4
        },
        dataType:"json",
        success:function(data){
            var html='';
            $.each(data.data,function(i,v){
                if(i<4){
                    html+='<div class="weui-col-33">'+v.lic+'</div>';
                    html+='<div class="weui-col-33">'+v.stype+'</div>';
                    html+='<div class="weui-col-33">'+v.cap+'</div>';
                }
            });
            $("#content").append(html);
            if(data.count<=last){
                $("#more").hide();
            }
        }
    });
    var last=4;
    $("#more").click(function(){
        $.ajax({
            url:'/user/car',
            type:'POST',
            data:{
               last:last,
               amout:4
            },
            dataType:'json',
            success:function(data){
                var html="";
                $.each(data.data,function(i,v){
                    if(i<4){
                        html+='<div class="weui-col-33">'+v.lic+'</div>';
                        html+='<div class="weui-col-33">'+v.stype+'</div>';
                        html+='<div class="weui-col-33">'+v.cap+'</div>';  
                    }
                });
                $("#content").append(html);
                if(data.count <= last){
                    $("#more").hide();
                }
            }
        });
        last +=4;
    });
});