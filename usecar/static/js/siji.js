Mock.mock('/user/car',{
    'data': 
       [
		{
			"id":"9",//订单id
			"name":"李三",//申请人姓名
			"tel":"13789076890",//申请人电话号码
			"num":"4",//用车人数
			"aplace":"湖南农业大学",//出发地点
			"bplace":"湖南大学",//目的地
			"start":"1501070585",//用车开始时间（时间戳，注意转换）
			"ab_end":"86400",//预计用时（秒为单位，注意转换）
			"reason":"赴湖南农业大学调研",//申请原因
			"car":"丰田卡罗拉",//车辆品牌
			"lic":"湘A55989",//车牌号
			"driver":"肖莱",//司机姓名
			"driver_tel":"13987658908",//司机电话
			"end":null,//实际结束时间（时间戳）
			"att1":"1",//审批人1表态
			"att2":"1"//审批人2表态
		},
		{
			"id":"19",//订单id
			"name":"肖三",//申请人姓名
			"tel":"13789076890",//申请人电话号码
			"num":"4",//用车人数
			"aplace":"湖南农业大学",//出发地点
			"bplace":"湖南大学",//目的地
			"start":"1501070585",//用车开始时间（时间戳，注意转换）
			"ab_end":"86400",//预计用时（秒为单位，注意转换）
			"reason":"学习、调研。。。。",//申请原因
			"car":"丰田卡罗拉",//车辆品牌
			"lic":"湘A55989",//车牌号
			"driver":"肖莱",//司机姓名
			"driver_tel":"13987658908",//司机电话
			"end":null,//实际结束时间（时间戳）
			"att1":"1",//审批人1表态
			"att2":"1"//审批人2表态
		},
		{
			"id":"29",//订单id
			"name":"李四",//申请人姓名
			"tel":"13789076890",//申请人电话号码
			"num":"4",//用车人数
			"aplace":"湖南农业大学",//出发地点
			"bplace":"湖南大学",//目的地
			"start":"1501070585",//用车开始时间（时间戳，注意转换）
			"ab_end":"86400",//预计用时（秒为单位，注意转换）
			"reason":"赴五一广场调研",//申请原因
			"car":"丰田卡罗拉",//车辆品牌
			"lic":"湘A55989",//车牌号
			"driver":"肖莱",//司机姓名
			"driver_tel":"13987658908",//司机电话
			"end":null,//实际结束时间（时间戳）
			"att1":"1",//审批人1表态
			"att2":"1"//审批人2表态
		},
		{
			"id":"32",//订单id
			"name":"王九",//申请人姓名
			"tel":"13789076890",//申请人电话号码
			"num":"4",//用车人数
			"aplace":"湖南农业大学",//出发地点
			"bplace":"湖南大学",//目的地
			"start":"1501070585",//用车开始时间（时间戳，注意转换）
			"ab_end":"86400",//预计用时（秒为单位，注意转换）
			"reason":"赴郴州考察",//申请原因
			"car":"丰田卡罗拉",//车辆品牌
			"lic":"湘A55989",//车牌号
			"driver":"肖莱",//司机姓名
			"driver_tel":"13987658908",//司机电话
			"end":null,//实际结束时间（时间戳）
			"att1":"1",//审批人1表态
			"att2":"1"//审批人2表态
		},
	],
"count":"17",
});
function toDate(time){
	var date=new Date(time);
	var y=date.getFullYear();
	var M=date.getMonth()+1;
	var d=date.getDate();
	var h=date.getHours();
	var m=date.getMinutes();
	var s=date.getSeconds();
	return y + '年' +M +'月'+d;
}
$(function(){
	$.ajax({
		url:'/user/car',
        type:'POST',
        data:{
        },
        dataType:"json",
        success:function(data){
      var html="";
      $.each(data.data,function(i,v){
      var unixTimestamp =toDate( v.start*1000) ;
      	html+='<div class="weui-form-preview">';
      	html+='<div class="weui-form-preview__hd">';
      	html+='<div class="weui-form-preview__item">';
      	html+='<div class="weui-form-preview__label label_title">' + v.reason+'</div>';
      	html+='<div class="weui-form-preview__value">'+unixTimestamp +'</div>';
      	html+='</div>';
      	html+='</div>';
      	html+='<div class="weui-form-preview__bd">';
      	html+='<div class="weui-form-preview__item">';
      	html+='<div class="weui-form-preview__label">'+"出发地："+'</div>';
      	html+='<span class="weui-form-preview__value">'+v.aplace+'</div>';
      	html+='<div class="weui-form-preview__label">'+"目的地："+'</div>';
      	html+='<span class="weui-form-preview__value">'+v.bplace+'</div>';
      	html+='</div>';    	
      	html+='</div>';
      })
      $("#sj_content").append(html);
        }
	})
});