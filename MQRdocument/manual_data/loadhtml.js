var keynum = new Array("Manual-0.html","Manual-1.html","Manual-2.html","Manual-3.html","Manual-4.html");
var fname_cnt = 0;
var rcv_cnt = 0;
var myTim = "";
var bodys = new Array();
var fnames = new Array();

function myTimer(){
	clearInterval(myTim); // setInterval()を解除する
	freadstart()
}

function getPage(pageURL,count) {
	jQuery.ajax({
		url:pageURL,
		type:"get",
		dataType:"html",
		async:false,
		success:function(data){ 
			bodys[count]=data; 
		},
		error: function( data ) {
			alert( 'データの読み込みを失敗しました。ページを再読み込みしてください。' );
		}
	});
}

// XMLHttpsオブジェクト作成
function createXMLHttp()
{
	try {
		return new ActiveXObject ("Microsoft.XMLHTTP");
	}catch(e){
		try {
		return new XMLHttpRequest();
		}catch(e) {
			return null;
		}
	}
	return null;
}

function loadFile(url,count)
{
	getPage(url,count)
return;

}

function freadstart(){

	var fname = keynum[fname_cnt];
	fnames[fname_cnt]=fname;
	var url = fname;
	loadFile(url,fname_cnt);
	if( ++fname_cnt < keynum.length ){
		myTim = setInterval("myTimer()",100);
	}else{
	    var invis = document.getElementById( 'invis' );
	    for ( var hdoc = 0; hdoc < bodys.length; hdoc ++ ) {
			invis.innerHTML += bodys[hdoc];
		}
	}
}
