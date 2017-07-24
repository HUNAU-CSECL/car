$(function () {
         // 用车开始时间
    $("#startime").datetimePicker({
        title: '出发时间',
        min: "2017-07-10",
        max: "2022-12-12 12:12",
        onChange: function(picker, values, displayValues) {
            console.log(values);
        }
    });
      $(".select").each(function() {
        var s = $(this);
        var z = parseInt(s.css("z-index"));
        var dt = $(this).children("dt");
        var dd = $(this).children("dd");
        var _show = function() { dd.slideDown(200);
            dt.addClass("cur");
            s.css("z-index", z + 1); }; //展开效果
        var _hide = function() { dd.slideUp(200);
            dt.removeClass("cur");
            s.css("z-index", z); }; //关闭效果
        dt.click(function() { dd.is(":hidden") ? _show() : _hide(); });
        dd.find("a").click(function() { dt.html($(this).html());
            _hide(); }); //选择效果（如需要传值，可自定义参数，在此处返回对应的“value”值 ）
        $("body").click(function(i) {!$(i.target).parents(".select").first().is(s) ? _hide() : ""; });
    })

        $("#form").submit(function() {
        if ($("#startime").val() == "") {
            $.toptip('请选择出发时间', 'error');
            return false;
        }
        if ($("#endtime").val() == "") {
            $.toptip('请选择使用时间', 'error');
            return false;
        }
        if ($("#destination").val() == "") {
            $.toptip('请输入目的地', 'error');
            return false;
        }
        if ($("#number").val() == "") {
            $.toptip('请输入用车人数', 'error');
            return false;
        }
        if ($("#type").val() == "") {
            $.toptip('请选择车辆类型', 'error');
            return false;
        }
        if ($("#in").val() == "") {
            $.toptip('请选择审批人', 'error');
            return false;
        }
        if ($("#on").val() == "") {
            $.toptip('请选择抄送人', 'error');
            return false;
        }
        if (true) {
            $.toptip('申请成功', 'success');
        }
    });
        $("#on").select({
        title: "选择审批人",
        multi: true,
        min: 2,
        max: 5,
        items: [{
            title: "张三",
            value: 1,
            description: "额外的数据1"
        }, {
            title: "王五",
            value: 2,
            description: "额外的数据2"
        }, {
            title: "翠花",
            value: 3,
            description: "额外的数据3"
        }, {
            title: "欧阳",
            value: 4,
            description: "额外的数据4"
        }, {
            title: "谢娜",
            value: 5,
            description: "额外的数据5"
        }, {
            title: "张杰",
            value: 6,
            description: "额外的数据6"
        }, ],
        beforeClose: function(values, titles) {
            if (values.indexOf("6") !== -1) {
                $.toast("");
                return false;
            }
            return true;
        },
        onChange: function(d) {
            console.log(this, d);
        },
        onClose: function(d) {
            console.log('close')
        }
    });
    $("#in").select({
        title: "选择抄送人",
        items: ["姚敏", "周俊", "王望龙", "利用卢", "兰兰", "花花"],
        onChange: function(d) {
            console.log(this, d);
        },
        onClose: function() {
            console.log("close");
        },
        onOpen: function() {
            console.log("open");
        },
    });
        $("#in_a").select({
        title: "选择抄送人",
        items: ["姚敏", "周俊", "王望龙", "利用卢", "兰兰", "花花"],
        onChange: function(d) {
            console.log(this, d);
        },
        onClose: function() {
            console.log("close");
        },
        onOpen: function() {
            console.log("open");
        },
    });
        $(document).on("click", "#per-return", function() {
        $.confirm("", "您确定要退出登录吗?", function() {
            window.location.href = "login.html";
        }, function() {
            //取消操作
        });
    });
        // 同意申请
            $("input[name=radiobuttontwo]").click(function() {
        var value = $('input[name=radiobuttontwo]:checked').val();
        $(".apply-reason").show();
        $("input[name=radiobutton]").removeAttr("checked");
    });
    $("input[name=radiobutton]").click(function() {
        var value = $('input[name=radiobutton]:checked').val();
        $(".apply-reason").hide();
        $("input[name=radiobuttontwo]").removeAttr("checked");
    });
        var o_status = $("#o_status").val(); //获取隐藏框值
    var o_status = 3;
    var a = document.getElementsByClassName("lb");
    var b = document.getElementsByClassName("stepText");
    for (var i = 0; i < a.length; i++) {
        if (i < o_status) {
            a[i].style.background = "green";
            b[i].style.color = "green";
        }
    }
});