/*----------------------------------------------------------------------------*/
// 'Mireille' Bulletin Board System
// - Mireille Article Navigator Java Script -
//
// $Revision$
// "This file is written in euc-jp, CRLF." ��
// Scripted by NARUSE Yui.
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
var nX=0,nY=0,max,may;
var maW=300,miW=180; //���粽�������Ǿ�������
var maX=-maW,maY=20; //�����ʥӤν�������֡��İ���
var drag_obj;

function artnavi(p){
  //�����
  if(document.all){
  }else if(document.getElementById){
    naviwind=document.getElementById('naviwind');
//    navititl=document.getElementById('navititl');
//    navibutt=document.getElementById('navibutt');
    navibody=document.getElementById('navibody');
  }else{return}
  if((document.location.href.lastIndexOf('?')>-1)&&(p!='popup')){
    //�ڡ����ְ�ư
    var cook=unescape(document.cookie);
    nX=(cook.match(/\tnX=\t(\d+);\t/))?parseInt(RegExp.$1):0;
    nY=(cook.match(/\tnY=\t(\d+);\t/))?parseInt(RegExp.$1):0;
    naviwind.style.display=(cook.match(/\tnaviwinddisplay=\t(\w+);\t/))?RegExp.$1:'';
    navibody.style.display=(cook.match(/\tnavibodydisplay=\t(\w+);\t/))?RegExp.$1:'';
//    navititl.style.display=(cook.match(/\tnavititldisplay=\t(\w+);\t/))?RegExp.$1:'';
    if(navibody.style.display=='none'){naviwind.style.width=miW+'px';}
    naviwind.style.left=document.body.scrollLeft+nX+'px';
    naviwind.style.top =document.body.scrollTop +nY+'px';
  }else{
    refresh();
    naviwind.style.display='';
    setcookie();
  }
  frames.onresize=refresh;
  emufixedid=setTimeout(emufixed,500);
}

//--------------------------------------
// �ե졼�ॵ�����ѹ��ΤȤ��Ϻ�����
function refresh(){
  var bW,bH;
  if(document.all){
    bW=document.body.clientWidth;
    bH=document.body.clientHeight;
  }else if(document.getElementById){
    naviwind.style.position='fixed';
    bW=window.innerWidth; if(maX<0){bW-=20;} //-20�ϥ�������С�����
    bH=window.innerHeight;if(maY<0){bH-=20;}
  }else{return}
  if(maX<0){
    max=bW+maX;
  }else{
    max=maX;
  }
  if(maY<0){
    may=bH+maY;
  }else{
    may=maY;
  }
  if(navibody.style.display==''){
    nX=max,nY=may;
  }else{
    nX=max+maW-miW,nY=may;
  }
  naviwind.style.left=document.body.scrollLeft+nX+'px';
  naviwind.style.top =document.body.scrollTop +nY+'px';
}

//--------------------------------------
// �����ʥӡ�(�Ǿ����å����ȥ벽�ú��粽��
function view(id){
  var viewobj;
  if(document.all){
    viewobj=document.all(id);
  }else if(document.getElementById){
    viewobj=document.getElementById(id);
  }else{return}
  if(viewobj.style.display=='none'){
    if(id=='naviwind'){
    }else if(id=='navibody'){
      nX=nX-(maW-miW);
      naviwind.style.left=document.body.scrollLeft+nX+'px';
      naviwind.style.width=maW+'px';
//      navititl.style.display='';
    }
    viewobj.style.display='';
  }else{
    viewobj.style.display='none';
    if(id=='naviwind'){
    }else if(id=='navibody'){
      nX=nX+maW-miW;
//      navititl.style.display='none';
      naviwind.style.width=miW+'px';
      naviwind.style.left=document.body.scrollLeft+nX+'px';
    }
  }
  setcookie();
}

//--------------------------------------
// Ʃ��������
function opacity(e,obj){
  if(document.all){
    if(e.type=='mouseover'){
      obj.filters['alpha'].opacity=100;
    }else if(e.type=='mouseout'){
      obj.filters['alpha'].opacity=60;
    }
  }else if(document.getElementById){
    if(e.type=='mouseover'){
      obj.style.MozOpacity=1;
    }else if(e.type=='mouseout'){
      obj.style.MozOpacity=0.6;
    }
  }else{return}
}

//--------------------------------------
// ���å������Ϥ�
function setcookie(){
  var expiresDate=new Date();
  expiresDate.setTime(expiresDate.getTime()+60*60*24*7*1000);
  document.cookie="ArtNavi="+escape(
    ";\tnX=\t"+(nX-document.body.scrollLeft)
   +";\tnY=\t"+(nY-document.body.scrollTop)
   +";\tnaviwinddisplay=\t"+naviwind.style.display
   +";\tnavibodydisplay=\t"+navibody.style.display
//   +";\tnavititldisplay=\t"+navititl.style.display
   +";\t")
   +"; expires="+expiresDate.toGMTString();
}

//--------------------------------------
// �����ʥӤ�D&D�ǰ�ư
function beginDrag(e,id){
  if(document.all){
    clearTimeout(emufixedid);
    drag_obj=document.all(id);
  }else if(document.getElementById){
    drag_obj=document.getElementById(id);
  }else{return}
  nX=e.clientX,nY=e.clientY;
  document.onmousemove=doDrag;
  document.onmouseup=endDrag;
  return false;
}
function doDrag(e){
  if(document.all){
    e=event;
  }else if(document.getElementById){
  }else{return}
  drag_obj.style.left=e.clientX-nX+parseInt(drag_obj.style.left)+'px';
  drag_obj.style.top =e.clientY-nY+parseInt(drag_obj.style.top) +'px';
  nX=e.clientX,nY=e.clientY;
  return false;
}
function endDrag(){
  if(document.all){
    emufixedid=setTimeout(emufixed,500);
  }else if(document.getElementById){
  }else{return}
  nX=parseInt(drag_obj.style.left)-document.body.scrollLeft;
  nY=parseInt(drag_obj.style.top) -document.body.scrollTop;
  document.onmousemove=null;
  document.onmouseup=null;
  setcookie();
  return false;
}

//--------------------------------------
// "position:fixed;"���ߥ�졼��
function emufixed(){
  //���̤��Ф��Ƶ����ʥӤ�����position:fixed;������
  clearTimeout(emufixedid);
  if(document.all){
    naviwind.style.left=document.body.scrollLeft+nX+'px';
    naviwind.style.top =document.body.scrollTop +nY+'px';
    emufixedid=setTimeout(emufixed,500);
  }else if(document.getElementById){
  }else{return}
}
