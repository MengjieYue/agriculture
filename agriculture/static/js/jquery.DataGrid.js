function addTable(totalRows) {
    $('#donelist').empty();
    var headrow='<tr id="headrow" style="height: 30px"><td style="width:30%">时间</td><td width="70%">操作</td></tr>';
    $('#donelist').append(headrow);
    var rowCount;
    for(rowCount=1;rowCount<=totalRows;rowCount++)
    {
        var newRow='<tr id="row'+rowCount+'" style="height:30px"><td></td><td></td></tr>';
        $('#donelist').append(newRow);
        /*alert($(newRow).attr('id'));*/
    }

   }
function SearchThis(){
    var obj=document.getElementById("ShowGrid");
    $(obj).css("height","500px");
    $("#Pagearea").show();
    var newobj=document.getElementById("ChooseMenu");
    $(newobj).css("display","none");
    addTable(12);
}
function SearchPre(){
    var obj=document.getElementById("ShowGrid");
    $(obj).css("height","450px");
    $("#Pagearea").show();
    var newobj=document.getElementById("ChooseMenu");
    $(newobj).css("display","block");

    addTable(10);
}
function SearchByTime(){
    if(document.getElementById('datepicker1').value>=document.getElementById('datepicker2').value)
    {
        alert("起始时间不能大于终止时间，请重新选择");
        document.getElementById('datepicker1').value="";
        document.getElementById('datepicker2').value="";
    }

}
/**
 * Created by yuemengjie on 14-5-22.
 */
