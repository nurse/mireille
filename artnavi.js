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
var deX=-1,deY=50; //記事ナビのクライアント領域（ウィンドウ）上の初期座標
var drag_obj; //D&D用オブジェクト
var scrollObj; //IE標準準拠モード時に、有効なscrollTop/scrollLeftプロパティを持つオブジェクトを入れる
var naviwind,navibody;
var emufixedid; //position:fixed仮想化IDの格納用
var docmentObj; //clientWidthやclientHeightを取得するためのオブジェクト

function artnavi(p){
	//初期化
	if(!window.opera&&document.all){
		scrollObj=document.compatMode&&document.compatMode=='CSS1Compat'?document.documentElement:document.body;
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
	}else return false;
	docmentObj=
		document.documentElement&&document.documentElement.clientHeight&&document.body.clientHeight
		&&document.documentElement.clientHeight<document.body.clientHeight
		?document.documentElement:document.body;
	
	if(p=='popup'||!document.cookie.match(/(^|; )ArtNavi=([^;]+)/)){
		naviwind.style.width=maW+'px';
		resetXY(1);
		naviwind.style.display=navibody.style.display='block';
		if(document.cookie.match(/(^|; )ArtNavi=([^;]+)/))setcookie();
	}else{
		//ページ間移動
		var cook=unescape(RegExp.$2);
		navibody.style.display=(cook.match(/\tnavibodydisplay=\t(\w+);\t/))?RegExp.$1:'block';
		naviwind.style.width=(navibody.style.display=='none'?miW:maW)+'px';
		ncX=(cook.match(/\tncX=\t(\d+);\t/))?parseInt(RegExp.$1):
			(deX<0?docmentObj.clientWidth +deX+1-naviwind.offsetWidth :deX);
		ncY=(cook.match(/\tncY=\t(\d+);\t/))?parseInt(RegExp.$1):
			(deY<0?docmentObj.clientHeight+deY+1-naviwind.offsetHeight:deY);
		naviwind.style.left=(scrollObj?scrollObj.scrollLeft:0)+ncX+'px';
		naviwind.style.top =(scrollObj?scrollObj.scrollTop:0) +ncY+'px';
		naviwind.style.display=(cook.match(/\tnaviwinddisplay=\t(\w+);\t/))?RegExp.$1:'block';
	}
	window.onresize=refresh;
	return true;
}


//--------------------------------------
// フレームサイズ変更のときは再描画
function refresh(p){
	if(p=='popup');
	else if(ncX>docmentObj.clientWidth -naviwind.offsetWidth );
	else if(ncY>docmentObj.clientHeight-naviwind.offsetHeight);
	else return false;
	resetXY();
	if(document.cookie.match(/(^|; )ArtNavi=([^;]+)/))setcookie();
	return true;
}


//--------------------------------------
// 記事ナビを表示する座標を再設定
function resetXY(){
	ncX=deX<0?docmentObj.clientWidth +deX+1-naviwind.offsetWidth :deX;
	ncY=deY<0?docmentObj.clientHeight+deY+1-naviwind.offsetHeight:deY;
	if(scrollObj){
		naviwind.style.left=scrollObj.scrollLeft+ncX+'px';
		naviwind.style.top =scrollObj.scrollTop +ncY+'px';
	}else{
		naviwind.style.left=ncX+'px';
		naviwind.style.top =ncY+'px';
	}
	return true;
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
	}else return false;
	e.cancelBubble=true;
	
	if(!viewobj.style){
	}else if(!viewobj.style.display){
		//Opera6
		e.preventDefault=true;
		if(!viewobj.style.visibility){
		}else if(viewobj.style.visibility=='hidden'){
			if(id=='naviwind');
			else if(id=='navibody')naviwind.style.pixelHeight=200;
			viewobj.style.visibility='visible';
		}else{
			viewobj.style.visibility='hidden';
			if(id=='naviwind');
			else if(id=='navibody')naviwind.style.pixelHeight=navititl.style.pixelHeight+5;
		}
		return false;
	}else if(viewobj.style.display=='none'){
		if(id=='naviwind'){
		}else if(id=='navibody'){
			ncX=ncX-(maW-miW);
			naviwind.style.left=(scrollObj?scrollObj.scrollLeft:0)+ncX+'px';
			naviwind.style.width=maW+'px';
		}
		viewobj.style.display='block';
	}else{
		viewobj.style.display='none';
		if(id=='naviwind'){
		}else if(id=='navibody'){
			naviwind.style.width=miW+'px';
			ncX=ncX+maW-miW;
			naviwind.style.left=(scrollObj?scrollObj.scrollLeft:0)+ncX+'px';
		}
	}
	setcookie();
	return true;
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
	var expiresDate=new Date();
	expiresDate.setTime(expiresDate.getTime()+75*24*60*60); //人の噂も七十五日
	data+="; expires="+expiresDate.toGMTString();
	document.cookie="ArtNavi="+data;
	return true;
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
	}else return false;
	e.cancelBubble=true;
	
	ncX=parseInt(drag_obj.style.left)-e.clientX;
	ncY=parseInt(drag_obj.style.top )-e.clientY;
	document.onmousemove=doDrag;
	document.onmouseup=endDrag;
	return false;
}
function doDrag(e){
	if(!drag_obj)return false;
	else if(document.all)e=event;
	else if(document.getElementById);
	else return false;
	drag_obj.style.left=e.clientX+ncX+'px';
	drag_obj.style.top =e.clientY+ncY+'px';
	return false;
}
function endDrag(){
	if(!drag_obj)return false;
	ncX=parseInt(drag_obj.style.left)-(scrollObj?scrollObj.scrollLeft:0);
	ncY=parseInt(drag_obj.style.top) -(scrollObj?scrollObj.scrollTop:0);
	drag_obj=null;
	document.onmousemove=null;
	document.onmouseup=null;
	setcookie();
	return false;
}


//--------------------------------------
// ショートカットキー(accesskey)の捕獲
function acskey(e,id){
	if(document.all);
	else if(document.getElementById);
	else return false;
	e.cancelBubble=true;
	
	if(e.type=='keypress'||e.type=='keydown'){
		switch(document.all?e.keyCode:document.getElementById?e.which:0){
		case/*'C'*/0x43:if('naviwind'!=id)return false;break;
		case/*'c'*/0x63:if('naviwind'!=id)return false;break;
		case/*'M'*/0x4d:if('navibody'!=id)return false;break;
		case/*'m'*/0x6d:if('navibody'!=id)return false;break;
		case/*'Enter'*/0x0d:if('naviwind'!=id&&'navibody'!=id)return false;break;
		case/*'Space'*/0x20:if('naviwind'!=id&&'navibody'!=id)return false;break;
		case/*'Tab'*/0x09:return true;break;
		default:return false;break;
		}
	}else{
		return false;
	}
	view(e,id);
	return true;
}


//------------------------------------------------------------------------------
// InternetExplorer with ConditionalCompilation
/*@cc_on
emufixedid=null;
//--------------------------------------
// Emulating"position:fixed;"
function emufixed(){
	//画面に対して記事ナビを固定（position:fixed;を力技で）
	if(emufixedid)clearTimeout(emufixedid);
	if(scrollObj){
		if( ncX>docmentObj.scrollWidth -naviwind.offsetWidth -scrollObj.scrollLeft)
			ncX=docmentObj.scrollWidth -naviwind.offsetWidth -scrollObj.scrollLeft;
		if( ncY>docmentObj.scrollHeight-naviwind.offsetHeight-scrollObj.scrollTop )
			ncY=docmentObj.scrollHeight-naviwind.offsetHeight-scrollObj.scrollTop ;
		naviwind.style.left=scrollObj.scrollLeft+ncX+'px';
		naviwind.style.top =scrollObj.scrollTop +ncY+'px';
	}else return false;
	emufixedid=null;
	return true;
}

//--------------------------------------
//ChangeOpacity for IE5.5orLater
function naviwind::onmouseenter(){naviwind.filters['alpha'].enabled=0}
function naviwind::onmouseleave(){naviwind.filters['alpha'].enabled=1}

// @*/
