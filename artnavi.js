/*----------------------------------------------------------------------------*/
// 'Mireille' Bulletin Board System
// - Mireille Article Navigator JavaScript -
//
// $Revision$
// "This file is written in euc-jp, CRLF." ��
// Scripted by NARUSE,Yui.
/*----------------------------------------------------------------------------*/
var cvsid = "$Id$";

//--------------------------------------
// �����ʥӼ�ư��ư

/*
 ��ư��ư���������ʤ��Ȥ��ϡ�
 ���ιԤκǽ�� // ��񤤤ƥ����ȥ����Ȥ��Ƥ�������
*/
window.onload=artnavi;


//--------------------------------------
// �������
var ncX=0,ncY=0; //NaviClientX/Y:�����ʥӤΥ��饤������ΰ�ʥ�����ɥ��˾�κ�ɸ
var maW=300,miW=180; //���粽�������Ǿ�������
var deX=-maW,deY=50; //�����ʥӤΥ��饤������ΰ�ʥ�����ɥ��˾�ν����ɸ
var drag_obj; //D&D�ѥ��֥�������
var docele; //IEɸ����⡼�ɻ��ˡ�ͭ����scrollTop/scrollLeft�ץ�ѥƥ�����ĥ��֥������Ȥ������
var naviwind,navibody;
var emufixedid; //position:fixed���۲�ID�γ�Ǽ��

function artnavi(p){
	//�����
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
	}else return false;
	
	if(p=='popup'||!document.cookie.match(/(^|; )ArtNavi=([^;]+)/))refresh('popup');
	else{
		//�ڡ����ְ�ư
		var cook=unescape(RegExp.$2);
		ncX=(cook.match(/\tncX=\t(\d+);\t/))?parseInt(RegExp.$1):0;
		ncY=(cook.match(/\tncY=\t(\d+);\t/))?parseInt(RegExp.$1):0;
		naviwind.style.display=(cook.match(/\tnaviwinddisplay=\t(\w+);\t/))?RegExp.$1:'block';
		navibody.style.display=(cook.match(/\tnavibodydisplay=\t(\w+);\t/))?RegExp.$1:'block';
		if(navibody.style.display=='none')naviwind.style.width=miW+'px';
		naviwind.style.left=(docele?docele.scrollLeft:0)+ncX+'px';
		naviwind.style.top =(docele?docele.scrollTop:0) +ncY+'px';
	}
	window.onresize=refresh;
	return true;
}


//--------------------------------------
// �ե졼�ॵ�����ѹ��ΤȤ��Ϻ�����
function refresh(p){
	if(p=='popup');
	else if(ncX+naviwind.offsetWidth >document.body.clientWidth);
	else if(ncY+naviwind.offsetHeight>document.body.clientlHeight);
	else return false;
	ncX=deX<0?document.body.clientWidth +deX-5+(navibody.style.display=='none'?maW-miW:0):deX;
	ncY=deY<0?document.body.clientHeight+deY-5:deY;
	if(docele){
		naviwind.style.left=(docele.scrollLeft+ncX+naviwind.offsetWidth <document.body.scrollWidth ?
			docele.scrollLeft+ncX:document.body.scrollWidth -naviwind.offsetWidth )+'px';
		naviwind.style.top =(docele.scrollTop +ncY+naviwind.offsetHeight<document.body.scrollHeight?
			docele.scrollTop +ncY:document.body.scrollHeight-naviwind.offsetHeight)+'px';
	}else{
		naviwind.style.left=(ncX+naviwind.offsetWidth <document.body.scrollWidth ?
			ncX:document.body.scrollWidth -naviwind.offsetWidth )+'px';
		naviwind.style.top =(ncY+naviwind.offsetHeight<document.body.scrollHeight?
			ncY:document.body.scrollHeight-naviwind.offsetHeight)+'px';
	}
	naviwind.style.display='block';
	if(document.cookie.match(/(^|; )ArtNavi=([^;]+)/))setcookie();
	return true;
}


//--------------------------------------
// �����ʥ� (�Ǿ����å����ȥ벽�ú��粽��
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
	return true;
}


//--------------------------------------
// ���å������Ϥ�
function setcookie(){
	var data=escape(
		";\tncX=\t"+ncX
		+";\tncY=\t"+ncY
		+";\tnaviwinddisplay=\t"+naviwind.style.display
		+";\tnavibodydisplay=\t"+navibody.style.display
		+";\t");
	var expiresDate=new Date();
	expiresDate.setTime(expiresDate.getTime()+60*60*24*7*1000);
	data+="; expires="+expiresDate.toGMTString();
	document.cookie="ArtNavi="+data;
	return true;
}


//--------------------------------------
// �����ʥӤ�D&D�ǰ�ư
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
	ncX=parseInt(drag_obj.style.left)-(docele?docele.scrollLeft:0);
	ncY=parseInt(drag_obj.style.top) -(docele?docele.scrollTop:0);
	drag_obj=null;
	document.onmousemove=null;
	document.onmouseup=null;
	setcookie();
	return false;
}


//--------------------------------------
// ���硼�ȥ��åȥ���(accesskey)�����
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
	//���̤��Ф��Ƶ����ʥӤ�����position:fixed;���ϵ��ǡ�
	if(emufixedid)clearTimeout(emufixedid);
	if(docele){
		naviwind.style.left=(docele.scrollLeft+ncX+naviwind.offsetWidth <document.body.scrollWidth ?
			docele.scrollLeft+ncX:document.body.scrollWidth -naviwind.offsetWidth )+'px';
		naviwind.style.top =(docele.scrollTop +ncY+naviwind.offsetHeight<document.body.scrollHeight?
			docele.scrollTop +ncY:document.body.scrollHeight-naviwind.offsetHeight)+'px';
	}else return false;
	emufixedid=null;
	return true;
}

//--------------------------------------
//ChangeOpacity for IE5.5orLater
function naviwind::onmouseenter(){naviwind.filters['alpha'].enabled=0}
function naviwind::onmouseleave(){naviwind.filters['alpha'].enabled=1}

// @*/
