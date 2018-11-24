var is_nwjs = (typeof nw != 'undefined');
var is_nwjsdev = is_nwjs && (window.navigator.plugins.namedItem('Native Client') !== null);
if (is_nwjsdev)
    nw.Window.get().showDevTools();

ntf_win = null;
if(typeof($)!='undefined'){
$(document).ready(function(){
	if($('#gtitle_div').size()==0)
		return;
	console.log('B');
	nw.Window.open('notify.html',{"show":false}, function(new_win){ntf_win=new_win;});
	setInterval(function(){loadAlert();},5000);
	loadAlert();
});
}

function loadAlert() {
	$.ajax({
		url:'/alert', 
        cache:false, 
        dataType:'text',
        //mimeType:'application/json',
        async: true,
		method: "POST",
		data: {
			action:"myalert",
			"alertrecordbean.keywords":"",
			"alertrecordbean.mixids":"",
			"alertrecordbean.my":true,
			limit:100,
			moduleid:1
		},
        success:function(t){
			console.log('C');
			t = t.replace(/(['"])?([a-z0-9A-Z_]+)(['"])?:/g, '"$2": ');
			var data = JSON.parse(t);
            if (data && data.data) {
				updateAlertList(data.data);
			}
        },
        error:function(){
            console.log('加载报警数据出错');
        }
	});
}
var prevAlertList = null;
var latestAlertList = null;
function updateAlertList(list) {
	console.log('D');
	if (latestAlertList!=null)
		prevAlertList = latestAlertList;
	latestAlertList = list;
	//$('#ext-gen291').find('td');
	if (list.length>0)
		desktopNotify(list[0]);
}

function desktopNotify(rec) {
	console.log('E, ntf_win='+ntf_win);
	ntf_win.window.notify(rec.mixname, rec.alertmsg);
	//var notification = new Notification(rec.mixname, {
	//	body:rec.alertmsg
	//});
}