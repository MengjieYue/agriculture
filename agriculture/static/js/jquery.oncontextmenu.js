if (!document.getElementById)
    document.getElementById = function() { return null; }
function initializeMenu(menuId, administratorId) {
    var menu = document.getElementById(menuId);
    var administrator = document.getElementById(administratorId);
    if (menu == null || administrator == null) return;
    administrator.parentNode.style.backgroundImage = "url()";
    administrator.onclick = function() {
        var display = menu.style.display;
        this.parentNode.style.backgroundImage =
            (display == "block") ? "url()" : "url()";
        menu.style.display = (display == "block") ? "none" : "block";

        return false;
    }
}
     var g_oDiv={};
     var oDiv=null;
     var g_iSpeed=0;
     var t=null;
     var clickid="";
var tipid="";
var NumThis=0;
var NumPre=0;
var page_index=1;
var totalpage=0;
var perPage=0;
var totalRows=0;
var Row_index=0;
var startpoint=0;
var Parent;
var Clicked;
var StationName;
<!--onload begin-->
window.onload=function(){

            $("#Pagearea").hide();

            $("#ControlButtons").hide();
            $("#pageline").hide();
            $("#ImgArea").hide();
            document.getElementById('datepicker1').value="";

            /*initializeMenu("AdministratorMenu", "FirLogedadmin");
            initializeMenu("OnlineMenu", "onlineAdministrator");
            initializeMenu("OfflineMenu", "offlineAdministrator");
            initializeMenu("pumpstation", "SecLogedadmin");*/
            /*opUl();*/

            /*oDiv=document.getElementById("div1");
            oDiv.style.height="0px";

            $('li.admin').contextmenu(function(ev){
                var oEvent=window.event||ev;
                clickid=$(this).attr('id');
                Clicked=this;
                Parent=$(this).parent()[0];
                cancelDefault(oEvent);
                var location=$("#newbodyPanel").offset();
                var left=location.left;
                var top=location.top;
                g_oDiv.MouseX=oEvent.clientX;
                g_oDiv.MouseY=oEvent.clientY;

                oDiv.style.left=g_oDiv.MouseX+"px";
                oDiv.style.top=g_oDiv.MouseY+10+"px";
                doRightClick();
            })*/

        document.body.onmousedown=function(ev){
            var oEvent=window.event||ev;
            clearInterval(t);
            g_iSpeed=0;
            g_oDiv.h=0;
            oDiv.style.height=g_oDiv.h+"px";
            oDiv.style.display="none";
        }
        oDiv.onmousedown=function(ev){
            var oEvent=window.event||ev;
            oEvent.cancelBubble=true;
        }
    <!-- 遍历tip-->
         $(".tip").each(function(){
            $(this).click(function(){
                tipid = $(this).attr('id');
                doclick();
             })
        });
}
<!--onload ending-->


    function doDiv(ev){
        var oEvent=window.event||ev;
        oDiv.style.display="block";
        t=setInterval(doMove,30);
    }
    function doMove(){
        if(oDiv.offsetHeight>=100){
            g_iSpeed*=-0.1;
            oDiv.style.height=100+"px";
        }
        g_oDiv.h=g_iSpeed+oDiv.offsetHeight;
        g_iSpeed+=10;
        oDiv.style.height=g_oDiv.h+"px";
    }
    function cancelDefault(oEvent){
        if(oEvent.preventDefault){
            oEvent.preventDefault();
        }
        else{
            oEvent.returnValue=false;
        }
    }
    /* 对li操作后的动作的定义 */
    function opUl(){

        var oUl=document.getElementById("ul");
        var aLi=oUl.getElementsByTagName("li");
        for(var i=0;i<aLi.length;i++){
            aLi[i].aIndex=i;
            aLi[i].onmouseover=function(){
                for(j=0;j<aLi.length;j++){
                    aLi[j].style.background="none";
                }
                aLi[this.aIndex].style.background="#ffbb66";
            }

        }
        aLi[0].onclick=function(){
                clearInterval(t);
                oDiv.style.display="none";
                moveBtnOff();

        }
        aLi[1].onclick=function(){
                clearInterval(t);
                oDiv.style.display="none";
                moveBtnOn();
        }
        aLi[2].onclick=function(){
            SearchThis();
        }
        aLi[3].onclick=function(){
            SearchPre();
        }
    }

    function moveBtnOff() {
        var parent1=document.getElementById("OnlineMenu");
        var parent2=document.getElementById("OfflineMenu");
        /*var obj=document.getElementById(clickid);*/
        parent1.removeChild(Clicked);
        Clicked.childNodes[0].setAttribute('src','../static/img/status_offline.png');
        /*var clone = Clicked.cloneNode(true);*/
		parent2.appendChild(Clicked);

        $(parent2.children).bind("click",function(){
             tipid = $(this).attr('id');
             doclick();
             });
        $(parent2.children).bind("contextmenu",function(ev){
            var oEvent=window.event||ev;
            /*clickid=$(this).attr('id');*/
            Parent=this.parentNode;
            cancelDefault(oEvent);

            g_oDiv.MouseX=oEvent.clientX;
            g_oDiv.MouseY=oEvent.clientY;

            oDiv.style.left=g_oDiv.MouseX+"px";
            oDiv.style.top=g_oDiv.MouseY+10+"px";
            doRightClick();
        });
        ChangeState();
        $('#ButtonThis').attr("disabled",true);
    }
function moveBtnOn(){
    var parent1=document.getElementById("OnlineMenu");
    var parent2=document.getElementById("OfflineMenu");

    parent2.removeChild(Clicked);
    Clicked.childNodes[0].setAttribute('src','../static/img/status_online.png');
    /*var clone=Clicked.cloneNode(true);*/
    parent1.appendChild(Clicked);

    $(parent1.children).bind("click",function(){
             tipid = $(this).attr('id');
             doclick();
             });
    $(parent1.children).bind("contextmenu",function(ev){
            var oEvent=window.event||ev;
            /*clickid=$(this).attr('id');*/
            Parent=this.parentNode;
            cancelDefault(oEvent);

            g_oDiv.MouseX=oEvent.clientX;
            g_oDiv.MouseY=oEvent.clientY;

            oDiv.style.left=g_oDiv.MouseX+"px";
            oDiv.style.top=g_oDiv.MouseY+10+"px";
            doRightClick();
        });
    ChangeState();
    $('#ButtonThis').attr("disabled",false);
}

function addTable(Rows) {
    $('#donelist').empty();
    var headrow='<tr id="headrow" style="height: 30px"><td style="width:30%">时间</td><td width="70%">操作</td></tr>';
    $('#donelist').append(headrow);
    var rowCount;
    if(tipid=="tip-1")
    {
        Row_index=startpoint+(page_index-1)*perPage;
        for(rowCount=0;rowCount<Rows;rowCount++)
        {
            var newRow='<tr id="row'+rowCount+'" style="height:30px"><td>'+members[Row_index+rowCount][0]+'</td><td>'+members[Row_index+rowCount][1]+'</td></tr>';
            $('#donelist').append(newRow);
            /*alert($(newRow).attr('id'));*/
        }
    }
    else
    {
        for(rowCount=0;rowCount<Rows;rowCount++)
        {
            var newRow='<tr id="row'+rowCount+'" style="height:30px"><td></td><td></td></tr>';
            $('#donelist').append(newRow);
            /*alert($(newRow).attr('id'));*/
        }
    }
}
function SearchThis(){
    $("#GridArea").show();
    $("#ImgArea").hide();
    startpoint=0;
    page_index=1;
    perPage=12;
    totalRows=NumThis;
    var obj=document.getElementById("ShowGrid");
    $(obj).css("height","500px");
    $("#Pagearea").show();
    var newobj=document.getElementById("ChooseMenu");
    $(newobj).css("display","none");
    if(NumThis>12)
    {
        $("#pageline").show();
        $("#Previous").attr("disabled",true);
        $("#Next").attr("disabled",false);
        addTable(perPage);
        totalpage=Math.ceil(NumThis/12);
    }
    else
    {
        $("#pageline").hide();
        addTable(NumThis);
    }

}
function SearchPre(){
    $("#GridArea").show();
    $("#ImgArea").hide();
    startpoint=startpoint+NumThis;
    page_index=1;
    perPage=10;
    totalRows=NumPre;
    var obj=document.getElementById("ShowGrid");
    $(obj).css("height","450px");
    $("#Pagearea").show();
    var newobj=document.getElementById("ChooseMenu");
    $(newobj).css("display","block");
    if(NumPre>10)
    {
        $("#pageline").show();
        $("#Previous").attr("disabled",true);
        $("#Next").attr("disabled",false);
        addTable(perPage);
        totalpage=Math.ceil(NumPre/10);
    }
    else
    {
        $("#pageline").hide();
        addTable(NumPre);
    }

}

function Next()
{
    page_index=page_index+1;
    ShowPage();
    if(page_index==totalpage)
    {
        $("#Next").attr("disabled",true);
        $("#Previous").attr("disabled",false);
    }
    else if(page_index==1)
    {
        $("#Previous").attr("disabled",true);

    }
    else{
        $("#Next").attr("disabled",false);
        $("#Previous").attr("disabled",false);

    }


}
function Previous()
{
    page_index=page_index-1;
    ShowPage();
    if(page_index==totalpage)
    {
        $("#Next").attr("disabled",true);

    }
    else if(page_index==1)
    {
        $("#Previous").attr("disabled",true);
        $("#Next").attr("disabled",false);
    }
    else{
        $("#Next").attr("disabled",false);
        $("#Previous").attr("disabled",false);

    }


}
function ShowPage()
{
    if(page_index*perPage>totalRows)
    {
        addTable(page_index*perPage-totalRows);
    }
    else
    {
        addTable(perPage);
    }
}
function Initialise()
{
    $("#ControlButtons").show();
    /*$('#donelist').empty();
    $("#pageline").hide();
    $("#ChooseMenu").hide();*/
    startpoint=0;
}
function doclick(e){

    $("#GridArea").hide();
    $("#ImgArea").show();
    /*switch (tipid)
    {
        case "tip-1":
            $("#ImgArea").css({"background": "url('../static/images/farm1.jpg') no-repeat" });
            $("#svg-2").css("display","none");
            $("#svg-3").css("display","none");
            var parentid=document.getElementById("tip-1").parentNode.getAttribute('id');
            if(parentid=="OnlineMenu"){
                var svgnodes=document.getElementById("svg-1").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node.png');

                    }

                }
            }
            else{
                var svgnodes=document.getElementById("svg-1").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node2.png');
                    }
                }
            }
            $("#svg-1").css("display","block");
            $("#svg-1").show();
            $("#svg-2").hide();
            $("#svg-3").hide();
            Initialise();
            NumThis=5;
            NumPre=15;
            setInterval(RefreshState(),20000);//定时刷新状态
            break;
        case "tip-2":
            $('#ImgArea').css({"background": "url('../static/images/farm2.jpg') no-repeat" });
            $("#svg-1").css("display","none");
            $("#svg-3").css("display","none");
            var parentid=document.getElementById("tip-2").parentNode.getAttribute('id');
            if(parentid=="OnlineMenu"){
                var svgnodes=document.getElementById("svg-2").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node.png');

                    }

                }
            }
            else{
                var svgnodes=document.getElementById("svg-2").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node2.png');
                    }
                }
            }
            $("#svg-2").css("display","block");
            $("#svg-2").show();
            $("#svg-1").hide();
            $("#svg-3").hide();
            Initialise();
            NumThis=15;
            NumPre=8;

            break;
        case "tip-3":
            $('#ImgArea').css({"background": "url('../static/images/farm3.jpg') no-repeat" });

            $("#svg-1").css("display","none");
            $("#svg-2").css("display","none");
            var parentid=document.getElementById("tip-3").parentNode.getAttribute('id');
            if(parentid=="OnlineMenu"){
                var svgnodes=document.getElementById("svg-3").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node.png');

                    }

                }
            }
            else{
                var svgnodes=document.getElementById("svg-3").children;
                for(var i=0;i<svgnodes.length-1;i++)
                {
                    var grandnodes=svgnodes[i].children;
                    for(var j=0;j<grandnodes.length;j++){
                        grandnodes[j].childNodes[1].setAttribute('src','../static/img/node2.png');
                    }
                }
            }
            $("#svg-3").css("display","block");
            $("#svg-3").show();
            $("#svg-2").hide();
            $("#svg-1").hide();
            Initialise();
            NumThis=22;
            NumPre=12;

            break;
        case "tip-4":
            $('#ImgArea').css({"background": "url('../static/images/farm4.jpg') no-repeat" });
            Initialise();
            NumThis=10;
            NumPre=28;

            break;
    }*/
    /*var parent=document.getElementById(tipid).parentNode;
    if(parent.getAttribute('id')=="OfflineMenu")
    {
        $('#ButtonThis').attr("disabled",true);
    }
    else
    {
        $('#ButtonThis').attr("disabled",false);
    }*/

    var svgnodes=document.getElementById("svg-1").children;
    for(var i=0;i<svgnodes.length-1;i++)
    {
        var grandnodes=svgnodes[i].children;
        for(var j=0;j<grandnodes.length;j++){
            grandnodes[j].childNodes[1].setAttribute('src','../static/img/node.png');

        }

    }

    /*$("#svg-1").css("display","block");*/
    $("#svg-1").show();

    Initialise();
    NumThis=5;
    NumPre=15;
    StationName= e.innerHTML;
    setInterval('RefreshState(StationName)',1000);//定时刷新状态

}
function doRightClick(){

        /* 初始化经过背景为空 */
        var oUl=document.getElementById("ul");
        var aLi=oUl.getElementsByTagName("li");
        for(var i=0;i<aLi.length;i++){
            aLi[i].style.background="none";
        }
        /*var obj=document.getElementById(clickid);
        var parent=obj.parentNode;*/

        if(Parent.getAttribute('id')=="OnlineMenu")
        {
            aLi[1].style.color="grey";
            aLi[1].onclick=function(){return false;}
            aLi[0].style.color="black";
            aLi[0].onclick=function(){
                clearInterval(t);
                oDiv.style.display="none";
                moveBtnOff();
            }
        }
        else
        {
            aLi[0].style.color="grey";
            aLi[0].onclick=function(){return false;}
            aLi[1].style.color="black";
            aLi[1].onclick=function(){
                clearInterval(t);
                oDiv.style.display="none";
                moveBtnOn();
            }
        }
        clearInterval(t);
        doDiv();
}
function ChangeState(){
    var parentid=document.getElementById(clickid).parentNode.getAttribute('id');
    switch (clickid)
    {
        case "tip-1":
            var svgnodes=document.getElementById("svg-1").children;
            break;
        case "tip-2":
            var svgnodes=document.getElementById("svg-2").children;
            break;
        case "tip-3":
            var svgnodes=document.getElementById("svg-3").children;
            break;
    }
    if(parentid=="OnlineMenu"){

        for(var i=0;i<svgnodes.length-1;i++)
        {
            var grandnodes=svgnodes[i].children;
            for(var j=0;j<grandnodes.length;j++){
                grandnodes[j].childNodes[1].setAttribute('src','../static/img/node.png');

            }

        }
    }
    else{

        for(var i=0;i<svgnodes.length-1;i++)
        {
            var grandnodes=svgnodes[i].children;
            for(var j=0;j<grandnodes.length;j++){
                grandnodes[j].childNodes[1].setAttribute('src','../static/img/node2.png');
            }
        }
    }
    /*setInterval(RefreshState(),1000);//定时刷新状态*/
}

function RefreshState(station){
    $.getJSON("/station/"+station+"",function(data){   //使用getJSON()方法发送请求并接收JSON格式数据
        var alldata  = data;   //获取响应数据
        for(var i=0;i<alldata.length;i++)
        {
            var num=alldata[i].index;
            var nodeid;
            nodeid="node"+num;

            newnode=document.getElementById(nodeid);

            switch(alldata[i].status)
            {
                case true:
                       newnode.childNodes[1].setAttribute('src','../static/img/node.png');
                    break;
                case false:

                       newnode.childNodes[1].setAttribute('src','../static/img/node1.png');

                    break;
                default :
                    newnode.childNodes[1].setAttribute('src','../static/img/node2.png');
                    break;
            }
        }

    })

}
function AddToLine(){
    var Online=document.getElementById("OnlineMenu");
    Online.innerHTML="";
    var OnlineNum=1;
    var i;
    for(i=1;i<=OnlineNum;i++)
    {
        var name="张三";
        var AdminName=document.createElement("li");
        AdminName.innerHTML="<img src='../static/img/status_online.png'/><a href='#'>"+name+"</a>";
        AdminName.setAttribute("id","tip-"+i+"");
        AdminName.setAttribute("class","tip");
        Online.appendChild(AdminName);
        $(AdminName).bind("click",function(){
             tipid = $(this).attr('id');
             doclick();
         });
        $(AdminName).bind("contextmenu",function(ev){
            var oEvent=window.event||ev;
            clickid=$(this).attr('id');
            cancelDefault(oEvent);

            g_oDiv.MouseX=oEvent.clientX;
            g_oDiv.MouseY=oEvent.clientY;

            oDiv.style.left=g_oDiv.MouseX+"px";
            oDiv.style.top=g_oDiv.MouseY+10+"px";
            doRightClick();
        });
    }


}

function ChangeColor(e){
    switch (e.getAttribute('src'))
    {
        case "../static/img/node1.png":
            e.setAttribute('src','../static/img/node.png');
            break;
        case "../static/img/node.png":
            e.setAttribute('src','../static/img/node1.png');
            break;
        case "../static/img/node2.png":
            break;
    }

}

function OpenAll(){
    var obj=document.getElementsByClassName('Node');
    var i;
    for(i=0;i<obj.length;i++)
    {
        obj[i].setAttribute('src','../static/img/node.png');
    }
}

function CloseAll(){
    var obj=document.getElementsByClassName('Node');
    var i;
    for(i=0;i<obj.length;i++)
    {
        obj[i].setAttribute('src','../static/img/node1.png');
    }
}

function ReadState(){
    /*var xmlhttp;
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
      xmlhttp=new XMLHttpRequest();
      }
    else
      {// code for IE6, IE5
      xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    xmlhttp.onreadystatechange=function()
      {
      if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
        alert(xmlhttp.responseText);
        }
      }
    xmlhttp.open("GET","/data/3",true);
    xmlhttp.send();*/
    $.getJSON("/data/3",function(data){
        alert(data[0].status);
    })
}

function ShowPump(e){
    var ul= e.nextElementSibling;
    var name= e.childNodes[1].innerHTML;
    $(ul).find('li').remove();
    $.getJSON("/operation/"+name+"",function(data){
        for(var i=0;i<data.length;i++)
        {
            var newli=document.createElement('li');
            newli.innerHTML="<a>泵站：</a><a>"+data[i]+"</a>";
            newli.style.marginLeft="20px";
            newli.style.cursor="pointer";
            newli.childNodes[0].style.textDecoration="none";

            ul.appendChild(newli);
            $(newli).bind('click',function(){
                doclick(this.childNodes[1]);
            });
        }
    })


}


/**
 * Created by yuemengjie on 14-5-15.
 */
