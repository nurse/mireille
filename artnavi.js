/*----------------------------------------------------------------------------*/
// 'Mireille' Bulletin Board System
// - Mireille Article Navigator JavaScript -
//
// $Revision$
// "This file is written in euc-jp, CRLF." 空
// Scripted by NARUSE,Yui.
/*----------------------------------------------------------------------------*/
var cvsid = "$Id$";

//--------------------------------------
// 記事ナビ自動起動

/*
 自動起動させたくないときは、
 次の行の最初に // を書いてコメントアウトしてください
*/
window.onload=artnavi;


//--------------------------------------
// 初期設定
var ncX=0,ncY=0; //NaviClientX/Y:記事ナビのクライアント領域（ウィンドウ）上の座標
var maW=300,miW=180; //最大化横幅、最小化横幅
var deX=-maW,deY=20; //記事ナビのクライアント領域（ウィンドウ）上の初期座標
var drag_obj; //D&D用オブジェクト
var docele; //IE標準準拠モード時に、有効なscrollTop/scrollLeftプロパティを持つオブジェクトを入れる
var naviwind,navibody;

function artnavi(p){
	//初期化
	if(!window.opera&&document.all){
		docele=(document.compatMode=="CSS1Compat")?document.documentElement:document.body;
		naviwind=document.all('naviwind');
//		navititl=document.all('navititl');
//		navibutt=document.all('navibutt');
		navibody=document.all('navibody');
		window.onscroll=function(){emufixedid||(emufixedid=setTimeout(emufixed,300))};
		
		//ChangeOpacity for IE LessThan 5.5
		if(!window.createPopup&&naviwind.filters){
			naviwind.onmouseover=function(){naviwind.filters['alpha'].enabled=0}
			naviwind.onmouseout =function(){naviwind.filters['alpha'].enabled=1}
		}
	}else if(document.getElementById){
		naviwind=document.getElementById('naviwind');
//		navititl=document.getElementById('navititl');
//		navibutt=document.getElementById('navibutt');
		navibody=document.getElementById('navibody');
	}else{return}
	INIT:{
		do{
			if((document.location.href.lastIndexOf('?')<0)||(p=='popup')){break;}
			if(!document.cookie.match(/(^|; )ArtNavi=([^;]+)/)){break;}
			//ページ間移動
			var cook=unescape(RegExp.$2);
			ncX=(cook.match(/\tncX=\t(\d+);\t/))?parseInt(RegExp.$1):0;
			ncY=(cook.match(/\tncY=\t(\d+);\t/))?parseInt(RegExp.$1):0;
			naviwind.style.display=(cook.match(/\tnaviwinddisplay=\t(\w+);\t/))?RegExp.$1:'block';
			navibody.style.display=(cook.match(/\tnavibodydisplay=\t(\w+);\t/))?RegExp.$1:'block';
			if(navibody.style.display=='none'){naviwind.style.width=miW+'px';}
			naviwind.style.left=(docele?docele.scrollLeft:0)+ncX+'px';
			naviwind.style.top =(docele?docele.scrollTop:0) +ncY+'px';
			break INIT;
		}while(0);
		refresh('popup');
	}
	window.onresize=refresh;
//	frames.onresize=refresh;
}


//--------------------------------------
// フレームサイズ変更のときは再描画
function refresh(p){
	ncX=(deX<0?document.body.clientWidth +deX-5+(navibody.style.display=='none'?maW-miW:0):deX);
	ncY=(deY<0?document.body.clientHeight+deY-5:deY);
	naviwind.style.left=(docele?docele.scrollLeft:0)+ncX+'px';
	naviwind.style.top =(docele?docele.scrollTop:0) +ncY+'px';
	if(p=='popup'){
		naviwind.style.display='block';
		if(document.cookie.match(/(^|; )ArtNavi=([^;]+)/)){setcookie();}
	}
}


//--------------------------------------
// 記事ナビ (最小化｜タイトル化｜最大化）
function view(e,id){
	var viewobj;
	if(document.all){
		viewobj=document.all(id);
		e.returnValue=false;
	}else if(document.getElementById){
		viewobj=document.getElementById(id);
		e.preventDefault();
	}else{return false;}
	e.cancelBubble=true;
	
	if(!viewobj.style){
	}else if(!viewobj.style.display){
		//Opera
		e.preventDefault=true;
		if(!viewobj.style.visibility){
		}else if(viewobj.style.visibility=='hidden'){
			if(id=='naviwind'){
			}else if(id=='navibody'){
				naviwind.style.pixelHeight=200;
			}
			viewobj.style.visibility='visible';
		}else{
			viewobj.style.visibility='hidden';
			if(id=='naviwind'){
			}else if(id=='navibody'){
				naviwind.style.pixelHeight=navititl.style.pixelHeight+5;
			}
		}
		return false;
	}else if(viewobj.style.display=='none'){
		if(id=='naviwind'){
		}else if(id=='navibody'){
			ncX=ncX-(maW-miW);
			naviwind.style.left=(docele?docele.scrollLeft:0)+ncX+'px';
			naviwind.style.width=maW+'px';
		}
		viewobj.style.display='block';
	}else{
		viewobj.style.display='none';
		if(id=='naviwind'){
		}else if(id=='navibody'){
			naviwind.style.width=miW+'px';
			ncX=ncX+maW-miW;
			naviwind.style.left=(docele?docele.scrollLeft:0)+ncX+'px';
		}
	}
	setcookie();
}


//--------------------------------------
// クッキーを渡す
function setcookie(){
	var data=escape(
		";\tncX=\t"+ncX
		+";\tncY=\t"+ncY
		+";\tnaviwinddisplay=\t"+naviwind.style.display
		+";\tnavibodydisplay=\t"+navibody.style.display
		+";\t");
/* //SessionCookie化
	var expiresDate=new Date();
	expiresDate.setTime(expiresDate.getTime()+60*60*24*7*1000);
	data+="; expires="+expiresDate.toGMTString();
*/
	document.cookie="ArtNavi="+data;
}


//--------------------------------------
// 記事ナビをD&Dで移動
function beginDrag(e,id){
	if(document.all){
		drag_obj=document.all(id);
		e.returnValue=false;
	}else if(document.getElementById){
		drag_obj=document.getElementById(id);
		e.preventDefault();
	}else{return false;}
	e.cancelBubble=true;
	
	ncX=parseInt(drag_obj.style.left)-e.clientX;
	ncY=parseInt(drag_obj.style.top )-e.clientY;
	document.onmousemove=doDrag;
	document.onmouseup=endDrag;
	return false;
}
function doDrag(e){
	if(!drag_obj){return
	}else if(document.all){
		e=event;
	}else if(document.getElementById){
	}else{return}
	drag_obj.style.left=e.clientX+ncX+'px';
	drag_obj.style.top =e.clientY+ncY+'px';
	return false;
}
function endDrag(){
	if(!drag_obj){return}
	ncX=parseInt(drag_obj.style.left)-(docele?docele.scrollLeft:0);
	ncY=parseInt(drag_obj.style.top) -(docele?docele.scrollTop:0);
	drag_obj=null;
	document.onmousemove=null;
	document.onmouseup=null;
	setcookie();
	return false;
}


//--------------------------------------
// ショートカットキー(accesskey)の捕獲
function acskey(e,id){
	if(document.all){
		e.returnValue=false;
	}else if(document.getElementById){
		e.preventDefault();
	}else{return false;}
	e.cancelBubble=true;
	
	var which;
	which=document.all?e.keyCode:document.getElementById?e.which:null;
	if(!which)return false;
	
	switch(String.fromCharCode(which)){
	case 'C': if('naviwind'!=id)return;break;
	case 'c': if('naviwind'!=id)return;break;
	case 'M': if('navibody'!=id)return;break;
	case 'm': if('navibody'!=id)return;break;
	default : return;
	}
	view(e,id);
}


//------------------------------------------------------------------------------
// InternetExplorer with ConditionalCompilation
/*@cc_on

var emufixedid; //position:fixed仮想化IDの格納用
//--------------------------------------
// Emulating"position:fixed;"
function emufixed(){
	//画面に対して記事ナビを固定（position:fixed;を力技で）
	clearTimeout(emufixedid);
	if(docele){
		//WinIE4-6
		naviwind.style.left=docele.scrollLeft+ncX+'px';
		naviwind.style.top =docele.scrollTop +ncY+'px';
	}else{return}
	emufixedid=null;
}

//--------------------------------------
//ChangeOpacity for IE5.5orLater
function naviwind::onmouseenter(){naviwind.filters['alpha'].enabled=0}
function naviwind::onmouseleave(){naviwind.filters['alpha'].enabled=1}

// @*/
