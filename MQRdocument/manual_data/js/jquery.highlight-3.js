/*

highlight v3

Highlights arbitrary terms.

<http://johannburkard.de/blog/programming/javascript/highlight-javascript-text-higlighting-jquery-plugin.html>

MIT license.

Johann Burkard
<http://johannburkard.de>
<mailto:jb@eaio.com>

*/

var Url = {
	// public method for url encoding
	encode : function (string) {
		return escape(this._utf8_encode(string));
	},
	// public method for url decoding
	decode : function (string) {
		return this._utf8_decode(unescape(string));
	},
	// private method for UTF-8 encoding
	_utf8_encode : function (string) {
		string = string.replace(/\r\n/g,"\n");
		var utftext = "";
		for (var n = 0; n < string.length; n++) {
			var c = string.charCodeAt(n);
			if (c < 128) {
				utftext += String.fromCharCode(c);
			}
			else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			}
			else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}
		}
		return utftext;
	},
 
	// private method for UTF-8 decoding
	_utf8_decode : function (utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
		while ( i < utftext.length ) {
			c = utftext.charCodeAt(i);
			if (c < 128) {
				string += String.fromCharCode(c);
				i++;
			}
			else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i+1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			}
			else {
				c2 = utftext.charCodeAt(i+1);
				c3 = utftext.charCodeAt(i+2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
		}
		return string;
	}
}

jQuery.fn.highlight = function(pat) {
 function innerHighlight(node, pat) {
  var skip = 0;
  if (node.nodeType == 3) {
	reg = new RegExp(pat);
    matchstr = node.data.toUpperCase().match(reg);
	if(matchstr){
	   var pos = node.data.toUpperCase().indexOf(matchstr[0]);
	   if (pos >= 0) {
	    var spannode = document.createElement('span');
	    spannode.className = 'highlight';
	    var middlebit = node.splitText(pos);
	    var endbit = middlebit.splitText(matchstr[0].length);
	    var middleclone = middlebit.cloneNode(true);
	    spannode.appendChild(middleclone);
	    middlebit.parentNode.replaceChild(spannode, middlebit);
	    skip = 1;
	   }
	}
  }
  else if (node.nodeType == 1 && node.childNodes && !/(script|style)/i.test(node.tagName)) {
   for (var i = 0; i < node.childNodes.length; ++i) {
    i += innerHighlight(node.childNodes[i], pat);
   }
  }
  return skip;
 }
 return this.each(function() {
  innerHighlight(this, pat );
 });
};

jQuery.fn.removeHighlight = function() {
 return this.find("span.highlight").each(function() {
  this.parentNode.firstChild.nodeName;
  with (this.parentNode) {
   replaceChild(this.firstChild, this);
   normalize();
  }
 }).end();
};


function getUrlVars()
{ 
    var vars = [], hash; 
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&'); 
    for(var i = 0; i < hashes.length; i++) { 
        hash = hashes[i].split('='); 
        vars.push(hash[0]); 
        vars[hash[0]] = hash[1]; 
    } 
    return vars; 
}
var poshighlight=0;
var querywords = "";
var flgcls=false;

$(document).ready(function(){

var getparams = getUrlVars();
querywords = getparams["query"];
var opt_mode = getparams["mode"];
querywords = Url.decode(querywords);

var elms = $("#docs");
elms.each(function(){
	$(this).removeHighlight();
})

var words = [];
words = querywords
    .replace(/^\s+|\s+$/g,"")
    .replace(/\s+/g, " ")
    .split(" ");
	for (i in words) {
	    if (words[i] != "") {
			var elms = "";
			if(opt_mode != "m"){
				elms = $(".contents_main");
			}else{
				elms = $(".sectionDiv1_title,.sectionDiv2_title,.sectionDiv3_title,.sectionDiv4_title,.sectionDiv5_title,.sectionDiv6_title,.sectionDiv7_title,.block_text,.block_item,.block_title");
			}
			elms.each(function(){
				qword = words[i].toUpperCase();
				qword = qword.replace(/\W/g,'\\$&');
				qword = qword.replace(/[A-Z0-9]|\\[Ａ-Ｚ０-９]/g, function(s) {
					if( s.charCodeAt(0) < 0x80 && s.charCodeAt(0) != 0x5c ){
					    return "["+s+String.fromCharCode(s.charCodeAt(0) + 0xFEE0)+"]";
					}else{
					    return "["+String.fromCharCode(s.charCodeAt(1) - 0xFEE0)+s.charAt(1)+"]";
					}
				});
				$(this).highlight(qword);
			})
	    }
	}
});

$(window).load(function(){
    scrollinit(poshighlight);
    var anchor = window.location.hash;
	anchor = anchor.replace("#", "");  
	//var element = document.getElementById(anchor);
	//alert(anchor);
	location.hash=anchor;
	//element.focus();
//	if($.cookie("c_redisp") != "no" ){
//		setTimeout( 'dispguide()', 100 );
//	}

});

function scrollinit(num){
	if( $(".highlight").length ){

	var divOffset = $(".highlight").eq(num).offset().top;
	$(".highlight").eq(num).addClass("currenthighlight");

	divOffset = (divOffset > 5) ? divOffset-5:divOffset;
//		$($.browser.opera ? document.compatMode == 'BackCompat' ? 'body' : 'html' :'html,body').animate({scrollTop: divOffset + 'px'}, 1);
	}
}

function dispguide(){
	var getparams = getUrlVars();
	if( typeof(getparams["query"]) == "undefined"){
		return;
	}
	if( querywords == ''){
		return;
	}

	$("#docs").after('<div id="dialog-message" title="＜操作方法＞"><div style="text-align:left;">キーワードにマッチした次の箇所にジャンプするには「Ｆ」キーを、１つ前にマッチした箇所に戻るには「Ｂ」キーを押してください。<br/><br/><input id="askredisp" type="checkbox" value="no">次回から表示しない</div></div>');
	flgcls=true;
	$('#dialog-message').dialog({
		close: function(){
			flgcls=false;
			if( $("#askredisp").attr("checked") ){
				$.cookie( "c_redisp","no",null );
			}
		}
	});
}


$(document).keydown(function(e){
/*
	if( $(".highlight").length >= 1){
		var kcode = e.keyCode ? e.keyCode:event.keyCode;
	 	switch(kcode){
			case 70://F
			case 102://f
				if( poshighlight < $(".highlight").length - 1){
					$(".highlight").removeClass("currenthighlight")
					scrollinit(++poshighlight);
				}else{
					if(window.confirm('最後まで検索しました。先頭へ戻りますか？')){
						$(".highlight").removeClass("currenthighlight")
						poshighlight=0;
						scrollinit(poshighlight);
					}
				}
				break;
			case 66://B
			case 98://b
				if( poshighlight > 0){
					$(".highlight").removeClass("currenthighlight")
					scrollinit(--poshighlight);
				}else{
					if(window.confirm('先頭まで検索しました。最後へ戻りますか？')){
						$(".highlight").removeClass("currenthighlight")
						poshighlight=$(".highlight").length - 1;
						scrollinit(poshighlight);
					}
				}
			break;
		}
		if( flgcls==true ){
			$('#dialog-message').dialog('close');
			flgcls=false;
		}
	}
*/
  return false;
});