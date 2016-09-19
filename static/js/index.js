/**
 * Created by Chunyuan on 16-5-11.
 */
function click_type(obj){
    var id = $(obj).attr("id");
    var color = "597AB9";
    for(var i=1;i<7;i++){
        $("#"+i).css("color","#597AB9");
    }
    $('#type_cache').val(id);
    $("#"+id).css("color","#000000");
}

function banding(){
    var query_input=document.getElementById("query_input").value;
    //var filter=document.getElementById("filter").checked;
    var filter=false
/*    var baidu=document.getElementById("baidu").checked;
    var s360=document.getElementById("s360").checked;
    var sogou=document.getElementById("sogou").checked;

    var china_so=document.getElementById("china_so").checked;
    var bing=document.getElementById("bing").checked;
    var shen_ma=document.getElementById("shen_ma").checked;
*/
    var huajiao=document.getElementById("huajiao").checked;
    var douyu=document.getElementById("douyu").checked;
    var meipai=document.getElementById("meipai").checked;
    var zhanqi=document.getElementById("zhanqi").checked;
    var bili=document.getElementById("bili").checked;
    var huya=document.getElementById("huya").checked;
    var yy=document.getElementById("yy").checked;

    var content_type = $('#type_cache').val();

  //  url1='/queryAll?'+'q='+query_input+'&douyu='+douyu+'&meipai='+meipai+'&zhanqi='+zhanqi+'&bili='+bili+'&huya='+huya+'&yy='+yy+'&baidu='+baidu+"&s360="+s360+'&sogou='+sogou+"&china_so="+china_so+'&bing='+bing+'&huajiao='+huajiao+"&shen_ma="+shen_ma+'&filte='+filter+'&content_type='+content_type+"&pn=1"
    url1='/queryAll?'+'q='+query_input+'&douyu='+douyu+'&meipai='+meipai+'&zhanqi='+zhanqi+'&bili='+bili+'&huya='+huya+'&yy='+huya+'&huajiao='+huajiao+'&filte='+filter+'&content_type='+content_type+"&pn=1"
    url2='/filted?'+'q='+query_input+'&baidu='+baidu+"&s360="+s360+'&sogou='+sogou+"&china_so="+china_so+'&bing='+bing+"&shen_ma="+shen_ma+'&filte='+filter

    if(!filter){
        //alert("before window location");
        window.location.href=url1;
    }
    else{
        window.location.href=url2;
    }
}


$(function () {
    $.fn.bootstrapSwitch.defaults.size = 'mini';
    $.fn.bootstrapSwitch.defaults.onColor = 'info';
    $.fn.bootstrapSwitch.defaults.offColor = 'info';
    $('[type="checkbox"]').bootstrapSwitch();

    $("input").keydown(function (e) {
        if (e.keyCode == 13) {
            banding();
        }

    });

    $('#form_sub').click( function() {
        banding();
    });


    //输入提示
    /*
    $( "#query_input" ).autocomplete({
        width: 260,
        minLength: 0,
        selectFirst:true,
        source: function(request, response){
            //val i = 1;
            // request对象只有一个term属性，对应用户输入的文本
            // response是一个函数，在你自行处理并获取数据后，将JSON数据交给该函数处理，以便于autocomplete根据数据显示列表
            $.ajax( {
                url: "/suggest",
                data : { "term" :request.term },
                dataType: 'json',
                success: function(dataObj){

                  //  $.cookie("suggest" , $.toJSON(dataObj));
                    response(dataObj); //将数据交给autocomplete去展示
                    //if(i==1){
                    //    $("#query_input").val(dataObj[0].split("--")[0]);
                    //}

                }
            } );

	    },
        focus: function() {
          // 防止在获得焦点时插入值
          return false;
        },
        select: function( event, ui ) {

            console.log(ui.item.value.split("--")[0]);
            $("#query_input").val(ui.item.value.split("--")[0]);
            $('#form_sub').click();
            event.preventDefault();  //阻止默认浏览器动作(W3C)
            event.stopPropagation();
        }
    }).focus(function() {
        $(this).autocomplete("search");
        return false;
    });
    */

});
