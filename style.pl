#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Style Module -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
#use strict;
#use vars qw(%CF %IN %CK);

#-----------------------------
# �ǥ��������
#�ǥ�������������Ѥ����顢Ŭ�ڤ��ѹ����Ƥ�������
$CF{'Design'}="Type: Mireille Default 1.2";

#-------------------------------------------------
# Mireille���HTML�ǥ�����

#-----------------------------
# Mireile��HEAD���������
$CF{'head'}=<<"_CONFIG_";
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="Start" href="$CF{'home'}">
<LINK rel="Index" href="$CF{'index'}">
<LINK rel="Help" href="$CF{'index'}?help">
<LINK rel="Stylesheet" type="text/css" href="$CF{'style'}">
<LINK rel="Alternate" type="application/rss+xml" title="RSS" href="$CF{'self'}?rss">
<TITLE>$CF{'title'}</TITLE>
_CONFIG_

#-----------------------------
# Mireile Menu
$CF{'menu'}=<<"_CONFIG_";
<TABLE align="center" border="1" cellspacing="3" class="menu" summary="MireilleMenu"><TR>
<TD class="menu"><A href="$CF{'index'}?new#Form">�������</A></TD>
<TD class="menu"><A href="$CF{'index'}">����</A></TD>
<TD class="menu"><A href="$CF{'index'}?rvs">����</A></TD>
<TD class="menu"><A href="$CF{'index'}?del">���</A></TD>
<TD class="menu"><A href="$CF{'index'}?icct">��������</A></TD>
<TD class="menu"><A href="$CF{'index'}?seek">����</A></TD>
<TD class="menu"><A href="$CF{'index'}?help">�إ��</A></TD>
<TD class="menu"><A href="$CF{'home'}" title="$CF{'name'}">�ۡ���</A></TD>
</TR></TABLE>
_CONFIG_

#-----------------------------
# Page Header
$CF{'pghead'}=<<"_CONFIG_";
<TABLE align="center" border="0" cellspacing="0" class="head" summary="PageHeader" width="90%"><TR>
<TH width="100%"><H1 class="head" align="left">$CF{'pgtitle'}</H1></TH>
<TD nowrap>��������������</TD>
</TR></TABLE>
_CONFIG_

#-----------------------------
# Page Footer
sub getPageFooter{
    return<<"_HTML_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageFooter" width="90%"><TR>
<TD nowrap>��������������</TD>
<TH width="100%"><DIV class="head"><A href="@{[
	$_[0]?qq($CF{'home'}">BACK to HOME):qq($CF{'index'}">BACK to INDEX)
]}</A></DIV></TH>
</TR></TABLE></DIV>
_HTML_
}
$CF{'pgfoot'}=&getPageFooter;

#-----------------------------
# ��ƥե�����ǻȤ�JavaScript
$CF{'jsWritingForms'}=sprintf<<'_CONFIG_',$CF{'icon'},($CF{'absoluteIcon'}?1:0)+($CF{'relativeIcon'}?2:0);
<SCRIPT type="text/javascript" defer>
<!--
var iconDirectory='%s',iconSetting=%d;
_CONFIG_

$CF{'jsWritingForms'}.=<<'_CONFIG_';
var isLoaded;
var autosaveId;
var oBody,oIcon,oCommand,oPreview;
window.onload=initialization;

/*========================================================*/
// Initialization
function initialization(){
	if(document.all){
		oBody=document.all('body');
		oIcon=document.all('icon');
		oCommand=document.all('cmd');
		if(typeof(oBody.addBehavior)=='object'){
			oBody.addBehavior('#default#userData');
			if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
			if(oBody.value&&oBody.getAttribute('MireilleAutosave'))
				status=removeBodyData('MireilleAutosave');
		}
	}else if(document.getElementById){
		oBody=document.getElementById('body');
		oIcon=document.getElementById('icon');
		oCommand=document.getElementById('cmd');
	}else return false;
	oPreview=document.images['Preview'];
	oldData=oBody.value;
	isLoaded=true;
	if(!autosaveId)autosaveId=setTimeout(autosaveBodyData,60000);
	return true;
}


/* ========================================================================== */
// General Routines

/*========================================================*/
// Change Icon Preview
function changePreviewIcon(){
	if(!oPreview&&!oIcon&&!initialization())return false;
	if(!oCommand||!oCommand.value){
		oIcon.disabled=false;
	}else if(iconSetting&1&&oCommand.value.match(/(^|;)absoluteIcon=([^;]*)/)){
		//���л��ꥢ������
		oPreview.src=RegExp.$2;
		oPreview.title='+'+RegExp.$2;
		oIcon.disabled=true;
	}else if(iconSetting&2&&oCommand.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//���л��ꥢ������
		oPreview.src=iconDirectory+RegExp.$2;
		oPreview.title=iconDirectory+'+'+RegExp.$2;
		oIcon.disabled=true;
	}else{
		oIcon.disabled=false;
	}
	if(oIcon.disabled){
		oPreview.style.visibility = "visible";
	}else if(oIcon.value==""){
		oPreview.style.visibility = "hidden";
	}else{
		oPreview.style.visibility = "visible";
		if(oPreview.src!=iconDirectory+oIcon.value)oPreview.src=iconDirectory+oIcon.value;
		if(oPreview.title!=oIcon.value)oPreview.title=iconDirectory+'+'+oIcon.value;
	}
	return true;
}


/*========================================================*/
// Autosave Body Data
function autosaveBodyData(){
	if(!isLoaded||!oBody||!oBody.value)return false;
	if(autosaveId)clearTimeout(autosaveId);
	if(oBody.value==oldData){
		return false;
	}else if(oBody.value.length>100){
		switch(saveBodyData('MireilleAutosave')){
		case'DeleteBodyData':
			status='as0: Something Wicked happened!';
			break;
		case'SavedBodyDataIE':
			status="���ߤ���ʸ�ǡ�����IE���Ǽ�ư��¸���ޤ�����";
			break;
		case'SavedBodyDataCookie':
			status="���ߤ���ʸ�ǡ�����ư��¸���ޤ�����";
			break;
		case'FailedToSave':
			status="��ư��¸�˼��Ԥ��ޤ�����Cookie����¸��ǽ�ʺ���ʸ����(��4KB)��Ķ�������餫�⤷��ޤ���";
			break;
		default:
			status='as1: Something Wicked happened!';
		}
		oldData=oBody.value;
	}
	autosaveId=setTimeout(autosaveBodyData,60000);
	return true;
}

/*========================================================*/
// Quick Save Body Data
function quicksaveBodyData(){
	if(!isLoaded||!oBody)return false;
	if(!confirm("��������ʸ����¸����ȡ��Ť���ʸ�ǡ����Ͼä��Ƥ��ޤ��ޤ�\n����Ǥ���¸���Ƥ�����Ǥ�����"))
		return false;
	
	switch(saveBodyData('MireilleQuicksave')){
	case'DeleteBodyData':
		alert('�����¸����Ƥ�����ʸ�ǡ����������ޤ�����');
			break;
	case'SavedBodyDataIE':
		alert("���ߤ���ʸ�ǡ���������¸���ޤ�����\n�����ޤ�IE�ˤ��Ȱ����¸�ɤʤΤǲ΅���ʤ��Ǥ���������");
			break;
	case'SavedBodyDataCookie':
		alert("���ߤ���ʸ�ǡ���������¸���ޤ�����\n�����ޤǡȰ����¸�ɤʤΤǲ΅���ʤ��Ǥ���������");
			break;
	case'FailedToSave':
		alert("�����¸�˼��Ԥ��ޤ�����\n��¸��ǽ�ʺ���ʸ������Ķ�������餫�⤷��ޤ���\n"
				+'��ʸ��ե��������¸���ʤ���񤤤������褤���Ȼפ��ޤ���');
			break;
	default:
		alert('qs: Something Wicked happened!');
	}
	return true;
}

/*========================================================*/
// Save Body Data
function saveBodyData(key){
	if(!isLoaded||!oBody)return false;
	var expires=new Date();
	if(oBody.addBehavior){
		//bahavior�ǡ�IE��¸�ˡʥ���������:escape̵����128KB��
		if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
		if(!oBody.value.length){
			//value���������
			oBody.removeAttribute(key);
			if(oBody.getAttribute('MireilleQuicksave')||oBody.getAttribute('MireilleAutosave')){
				expires.setMonth(expires.getMonth()+1);
				oBody.expires=expires.toUTCString();
				oBody.setAttribute('MireilleBody',new Date().toUTCString());
				oBody.save('MireilleBody');
			}else{
				expires.setMonth(expires.getMonth()-1);
				oBody.expires=expires.toUTCString();
				oBody.save('MireilleBody');
			}
			return'DeleteBodyData';
		}else{
			//��¸
			expires.setMonth(expires.getMonth()+1);
			oBody.expires=expires.toUTCString();
			oBody.setAttribute(key,oBody.value);
			oBody.setAttribute('MireilleBody',new Date().toUTCString());
			oBody.save('MireilleBody');
			return'SavedBodyDataIE';
		}
	}else{
		//Cookie�ǡʥ���������:escape�������3KB�ۤɡ�
		if(!oBody.value.length){
			//value���������
			document.cookie=key+'=; expires=Thu, 01-Jan-1970 00:00:00 GMT; ';
			return'DeleteBodyData';
		}
		var backup='';
		var regexp=new RegExp('(^|; )'+key+'=([^;]+)')
		if(document.cookie.match(regexp))backup=unescape(RegExp.$2);
		expires=expires.toGMTString().replace('UTC','GMT').replace(/(\d) (\w{3}) (\d)/,"$1-$2-$3");
		document.cookie=key+'='+escape(oBody.value)+'; expires='+expGMT+'; ';
		if(document.cookie.match(regexp)&&oBody.value==unescape(RegExp.$2)){
			return'SavedBodyDataCookie';
		}else{
			//3850byte���٤ǥ��������¤������롣
			document.cookie=key+'='+backup+'; expires='+expGMT+'; ';
			return'FailedToSave';
		}
	}
	return true;
}

/*========================================================*/
// Load Body Data
function loadBodyData(key){
	if(!isLoaded||!oBody)return false;
	if(!confirm("Cookie������ʸ�ǡ������ɤ߽Ф��ȡ����ߤ���ʸ�Ͼä��Ƥ��ޤ��ޤ�\n����Ǥ��ɤ߽Ф��Ƥ�����Ǥ�����"))
		return false;
	
	if(key=='MireilleQuicksave'||key=='MireilleAutosave');
	else if(confirm("Quicksave�Υǡ�����Autosave�Υǡ������ɤ�����ɤ߽Ф��ޤ�����\n"
				+"Quicksave�ξ��ϡ�OK�ס�Autosave�ξ��ϡ֥���󥻥�פ�����Ǥ�������"))
		key='MireilleQuicksave';
	else key='MireilleAutosave';
	
	if(oBody.addBehavior){
		if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
		var temp=oBody.getAttribute(key);
		if(temp){
			oBody.value=temp;
		}else{
			alert('�ɤ߹��ߤ˼��Ԥ��ޤ���');
		}
	}else if(document.cookie.match(new RegExp('(^|; )'+key+'=([^;]+)'))){
		oBody.value=unescape(RegExp.$2);
	}else{
		alert('�ɤ߹��ߤ˼��Ԥ��ޤ���');
	}
	return true;
}


/*========================================================*/
// Remove Body Data
function removeBodyData(key){
	if(!oBody)return false;
	if(document.cookie.match(/(^|; )MirBody=([^;]+)/))
		document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
	document.cookie=key+'=; expires=Thu, 01-Jan-1970 00:00:00; ';
	if(oBody.addBehavior){
		//bahavior�ǡ�IE��¸��
		var flag=0;
		var expires=new Date();
		expires.setMonth(expires.getMonth()-1);
		
		oBody.load('MireilleQuicksave');
		if(oBody.getAttribute('MireilleQuicksave')!=null){
			oBody.expires=expires.toUTCString();
			oBody.save('MireilleQuicksave');
			flag+=1;
		}
		
		oBody.load('MireilleAutosave');
		if(oBody.getAttribute('MireilleAutosave')!=null){
			oBody.expires=expires.toUTCString();
			oBody.save('MireilleAutosave');
			flag+=2;
		}
		
		oBody.load('MireilleBody');
		oBody.removeAttribute(key);
		if(oBody.getAttribute('MireilleQuicksave')||oBody.getAttribute('MireilleAutosave')){
			expires.setMonth(expires.getMonth()+2);
			oBody.expires=expires.toUTCString();
			oBody.setAttribute('MireilleBody',new Date().toUTCString());
			oBody.save('MireilleBody');
		}else{
			oBody.expires=expires.toUTCString();
			oBody.save('MireilleBody');
		}
		
		if(flag&1)oBody.load('MireilleQuicksave');
		if(flag&2)oBody.load('MireilleAutosave');
		if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
	}
	if(key=='MireilleQuicksave'){
		return'�����¸����Ƥ�����ʸ�ǡ����������ޤ�����';
	}else if(key=='MireilleAutosave'){
		return'��ư��¸����Ƥ�����ʸ�ǡ����������ޤ�����';
	}else{
		return'rbd: Something Wicked happened!';
	}
	return true;
}


-->
</SCRIPT>
_CONFIG_


#-----------------------------
# �ե�������°�����쥯������JScript
$CF{'jscript_AtSe'}=<<'_CONFIG_';
<SCRIPT type="text/JScript" defer>
<!--
// InternetExplorer with ConditionalCompilation
/*@cc_on
if(document.getElementsByTagName){
	var tags=document.getElementsByTagName('INPUT');
	for(var i in tags){
		if('button'==tags[i].className){
			tags[i].className='button';
			tags[i].onfocus=function()		{this.className='buttonover'};
			tags[i].onmouseover=function()	{this.className='buttonover'};
			tags[i].onblur=function()		{this.className='button'};
			tags[i].onmouseout=function()	{this.className='button'};
		}else if('submit'==tags[i].type){
			tags[i].className='submit';
			tags[i].onfocus=function()		{this.className='submitover'};
			tags[i].onmouseover=function()	{this.className='submitover'};
			tags[i].onblur=function()		{this.className='submit'};
			tags[i].onmouseout=function()	{this.className='submit'};
		}else if('reset'==tags[i].type){
			tags[i].className='reset';
			tags[i].onfocus=function()		{this.className='resetover'};
			tags[i].onmouseover=function()	{this.className='resetover'};
			tags[i].onblur=function()		{this.className='reset'};
			tags[i].onmouseout=function()	{this.className='reset'};
		}else if(tags[i].className&&tags[i].className.substr(0,6)=='button'){
			tags[i].onfocus=
				function(){if(this.className.substr(this.className.length-4)!='Over')this.className+='Over'}
			tags[i].onmouseover=
				function(){if(this.className.substr(this.className.length-4)!='Over')this.className+='Over'}
			tags[i].onblur=
				function(){if(this.className.substr(this.className.length-4)=='Over')
					this.className=this.className.substring(0,this.className.length-4)};
			tags[i].onmouseout=
				function(){if(this.className.substr(this.className.length-4)=='Over')
					this.className=this.className.substring(0,this.className.length-4)};
		}else if('text'==tags[i].type||'password'==tags[i].type){
			tags[i].className='blur';
			tags[i].onfocus=function()	{this.className='focus';};
			tags[i].onblur=function()	{this.className='blur';};
		}
	}
	tags=document.getElementsByTagName('BUTTON');
	for(var i in tags){
		if('button'==tags[i].className){
			tags[i].className='button';
			tags[i].onfocus=function()		{this.className='buttonover'};
			tags[i].onmouseover=function()	{this.className='buttonover'};
			tags[i].onblur=function()		{this.className='button'};
			tags[i].onmouseout=function()	{this.className='button'};
		}else if(tags[i].className&&tags[i].className.substr(0,6)=='button'){
			tags[i].onfocus=
				function(){if(this.className.substr(this.className.length-4)!='Over')this.className+='Over'}
			tags[i].onmouseover=
				function(){if(this.className.substr(this.className.length-4)!='Over')this.className+='Over'}
			tags[i].onblur=
				function(){if(this.className.substr(this.className.length-4)=='Over')
					this.className=this.className.substring(0,this.className.length-4)};
			tags[i].onmouseout=
				function(){if(this.className.substr(this.className.length-4)=='Over')
					this.className=this.className.substring(0,this.className.length-4)};
		}
	}
	tags=document.getElementsByTagName('TEXTAREA');
	for(var i in tags){
		if(tags[i].className)continue;
		tags[i].className='blur';
		tags[i].onfocus=function(){this.className='focus';};
		tags[i].onblur=function(){this.className='blur';};
	}
}
// @*/
-->
</SCRIPT>
_CONFIG_

#-----------------------------
# �إå���������
sub getHeader{
    my%DT=@_;
    return join"\n",$CF{'bodyHead'},($DT{'skyline'}||''),$CF{'pghead'},$CF{'menu'};
}

#-----------------------------
# �եå���������
sub getFooter{
    my$AiremixCopy=<<"_HTML_";
<DIV class="AiremixCopy"><SMALL>- $CF{'Design'} -</SMALL><BR>
- <A href="http://www.airemix.com/" target="_top" title="Airemix - Mireille -">Airemix Mireille</A>
<VAR title="times:@{[times]}">$CF{'Version'}</VAR> -</DIV>
_HTML_
    return$CF{'menu'}.&getPageFooter(defined$IN{'read'}).$AiremixCopy
	.$CF{'bodyFoot'}.$CF{'jscript_AtSe'}."</BODY>\n</HTML>\n";
}

#-----------------------------
# ��ս񤭡�TOP�ڡ����Υ�˥塼�β���ɽ������ޤ���
$CF{'note'}=<<"_CONFIG_";
<DIV class="center">
<TABLE align="center" class="note" summary="��ս�"><TR><TD><UL class="note">
<LI>��Ƥ��줿����������ϴ����Ԥδ������ˤ�����ޤ���</LI>
<LI>̤�ɵ���������������֤�ɽ������ޤ���</LI>
<LI>24���ְ������Ƥˤ�$CF{'new'}�ޡ������դ��ޤ���</LI>
<LI>�����ʥ�С��򥯥�å�����ȡ����ε����ν������̤ˤʤ�ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE>
</DIV>
_CONFIG_



#----------------------------------------------------------------------------------------#
#
# ��������Style������
#

#-------------------------------------------------
#�Ƶ���
sub artprt{
=item ����
\% ����åɤε�������ϥå���Υ�ե����
$	���ε����ξ���
=cut
    #��������������ä�
    my%DT=(%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
    my@temp=qw(Name Home Date Icon Signature New accessUnread);
    @DT{map{'_'.$_}@temp}=map{''}@temp;
    #������줿���Τ餻��
    'del'eq$DT{'Mir12'}&&($DT{'body'}='Mireille: [���ε����Ϻ������ޤ���]');
    #�����ʥ�
    ArtNavi->addThreadHead(\%DT);
    ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
    #�������ܤ�Ĵ���򤷤�
    $DT{'_Name'}=sprintf'<SPAN class="name">%s</SPAN>'
	,$DT{'email'}?qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>):$DT{'name'};
    $DT{'_Home'}=qq(<SPAN class="home"><A href="$DT{'home'}" target="_top">��HOME��</A></SPAN>)if$DT{'home'};
    $DT{'_Date'}=sprintf$DT{'time'}>$CK{'time'}?'<SPAN class="new">%s</SPAN>':'%s',&date($DT{'time'});
    $DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
    $DT{'_Signature'}=sprintf'<SPAN class="signature">[&nbsp;%s&nbsp;]</SPAN><BR>'
	,&getSignatureView(\%DT)if$CF{'signature'}&&$DT{'signature'};
    if($DT{'time'}>$^T-$CF{'newnc'}){
	$DT{'_New'}=$CF{'new'};
	$DT{'_tabUnread'}=sprintf' tabindex="%d"',$DT{'-unreads'};
	++$DT{'-unreads'};
    }
    
    #�ե�����ź��
    my $attachments = getAttachedFiles(\%DT) if $DT{'attach'};
    
    #���褤����Ϥ���
    print<<"_HTML_";
<DIV class="thread" title="$DT{'i'}�֥���å�" align="center" width="99%">
<TABLE border="0" cellspacing="0" class="subject" summary="$DT{'i'}�֥���å�" width="100%"><TR>
<TH class="subject"><H2 class="subject"><A name="art$DT{'i'}" id="art$DT{'i'}" title="$DT{'i'}�֥���å�">$DT{'subject'}</A></H2></TH>
<TD class="arrow">
<A name="nav_n$DT{'ak'}" href="#nav_n@{[$DT{'ak'}-1]}" title="��Υ���åɤ�">��</A>
<A name="nav_r$DT{'i'}" href="$CF{'index'}?res=$DT{'i'}#Form" title="���ε���No.$DT{'i'}���ֿ�">��</A>
<A name="nav_s$DT{'ak'}" href="#nav_s@{[$DT{'ak'}+1]}" title="���Υ���åɤ�">��</A>
</TD>
</TR></TABLE>

<TABLE border="0" cellspacing="0" class="parent" summary="Article$DT{'i'}-0" title="$DT{'i'}-0" width="100%">
<COL class="number"><COL class="name"><COL class="date">
<TR class="info">
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number"
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}"$DT{'_tabUnread'}>��No.$DT{'i'}��</A></TH>
	<TD class="name">$DT{'_New'} $DT{'_Name'} $DT{'_Home'}</TD>
	<TD class="date"><SPAN class="date">$DT{'_Date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤοƵ�������"><A
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'_Signature'} $DT{'_Icon'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
$attachments</TABLE>

_HTML_
    return$DT{'-unreads'};
}


#-------------------------------------------------
#�ҵ���
sub artchd{
=item ����
\% ����åɤε�������ϥå���Υ�ե����
$	���ε����ξ���
=cut
    #��������������ä�
    my%DT=(%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
    my@temp=qw(Name Home Date Icon Signature New accessUnread);
    @DT{map{'_'.$_}@temp}=map{''}@temp;
    #�������Ƥ�Ȥ��Ϥ������������Ф����㤦��
    #�����ʥ�
    ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
    #�������ܤ�Ĵ���򤷤�
    $DT{'_Name'}=sprintf'<SPAN class="name">%s</SPAN>'
	,$DT{'email'}?qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>):$DT{'name'};
    $DT{'_Home'}=qq(<SPAN class="home"><A href="$DT{'home'}" target="_top">��HOME��</A></SPAN>)if$DT{'home'};
    $DT{'_Date'}=sprintf$DT{'time'}>$CK{'time'}?'<SPAN class="new">%s</SPAN>':'%s',&date($DT{'time'});
    $DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
    $DT{'_Signature'}=sprintf'<SPAN class="signature">[&nbsp;%s&nbsp;]</SPAN><BR>'
	,&getSignatureView(\%DT)if$CF{'signature'}&&$DT{'signature'};
    if($DT{'time'}>$^T-$CF{'newnc'}){
	$DT{'_New'}=$CF{'new'};
	$DT{'_tabUnread'}=sprintf' tabindex="%d"',$DT{'-unreads'};
	++$DT{'-unreads'};
    }
    
    #�ե�����ź��
    my $attachments = getAttachedFiles(\%DT) if $DT{'attach'};
    
    #���褤����Ϥ���
    print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}" title="$DT{'i'}-$DT{'j'}" width="100%">
<COL class="space"><COL class="number"><COL class="name"><COL class="date">
_HTML_

=pod �ҵ��������ȥ����Ѥ�����
	print<<"_HTML_";
	<TR><TH class="space">&nbsp;</TH>
<TH colspan="3" class="subject"><H3 class="subject">$DT{'subject'}</H3></TH></TR>
_HTML_
=cut

    print<<"_HTML_";
<TR class="info"><TH class="space" rowspan="2">&nbsp;</TH>
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number"
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}"$DT{'_tabUnread'}>��Re:$DT{'j'}��</A></TH>
	<TD class="name">$DT{'_New'} $DT{'_Name'} $DT{'_Home'}</TD>
	<TD class="date"><SPAN class="date">$DT{'_Date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤλҵ���$DT{'j'}����"
	><A href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'_Signature'} $DT{'_Icon'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
$attachments</TABLE>

_HTML_
    return$DT{'-unreads'};
}


#-------------------------------------------------
#�����եå�
sub artfot{
=item ����
\% �������� �ϥå���Υ�ե����
=cut
    #��������������ä�
    my%DT=%{shift()};
	
    if($DT{'res'}){
	#�ֿ��⡼�ɤΤȤ�
	print<<'_HTML_';
</DIV>


_HTML_
    }elsif($CF{'readOnly'}||$DT{'-isLocked'}||$DT{'-isOverflowed'}){
	#���餫����ͳ�Ǳ�������
	my$message=sprintf
	    +($CF{'readOnly'}?'�ɤ߹������ѥ⡼�ɤʤΤǤ��ε�������å�No.%d�α������ѤǤ�'
	      :$DT{'-isLocked'}?'���ε�������å�No.%d�ϥ�å�����Ƥ���ΤǱ������ѤǤ�'
	      :$DT{'-isOverflowed'}?'���ε�������å�No.%d�ϻҵ��������¤�ã�����ΤǱ������ѤǤ�'
	      :'�ʤˤϤȤ⤢��Ȥꤢ�������ε�������å�No.%d�ϱ������ѤǤ�'),$DT{'i'};
	print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}" class="warning"
 href="$CF{'index'}?res=$DT{'i'}">$message(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
    }else{
	#���ε�������å�No.???���ֿ�����(?)
	print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}"
 href="$CF{'index'}?res=$DT{'i'}#Form">���ε�������å�No.$DT{'i'}���ֿ�����(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
    }
    #�����ʥ�
    ArtNavi->addThreadFoot(\%DT);
}


#-------------------------------------------------
# �����ե�����ź����
#
sub getAttachedFiles{
    my %DT = %{shift()};
    my $attachments = '';
    my $thumbnails = '';
    if($DT{'attach'}){
	my $attach = MirString::urldecode($DT{'attach'});
	my @array;
	if( ref$attach eq 'ARRAY' ){
	    @array = @{$attach};
	}elsif( ref$attach eq 'HASH' ){
	    push @array, $attach;
	}
	my $length = !$DT{'j'} ? $CF{'AttachParentLength'} : $CF{'AttachChildLength'};
	$#array = $length - 1 if @array > $length;
	for( grep{ref$_ eq 'HASH'}@array ){
	    my $item = $_;
	    my $filename = $item->{'filename'} || "$item->{'hash'}.$item->{'ext'}";
	    my $attach = sprintf('%s?mode=download&hash=%s',$CF{'index'},$item->{'hash'});
	    my $thumbnail = sprintf('%s/%s.%s',$CF{'AttachThumbnailDir'},$item->{'hash'},$item->{'ext'});
	    if($CF{'AttachThumbnail'}&&-s$thumbnail){
		$thumbnails .= <<"_HTML_";
<a href="$attach" title="$filename"><img src="$thumbnail" alt="$filename"></a>
_HTML_
	    }else{
		$attachments .= <<"_HTML_";
<a href="$attach" title="$filename">$filename</a>
_HTML_
	    }
	}
    }
    $attachments .= $thumbnails if $thumbnails;
    if($attachments){
	$attachments = <<"_HTML_";
<TR><TD>&nbsp;</TD><TD>Attachements:</TD><TD class="attachments">
$attachments</TD></TR>
_HTML_
    }
    return $attachments;
}


#-------------------------------------------------
# �Ƶ�����ƥե�����
#
sub prtfrm{
    my%DT=%CK;
    $DT{'_type'} = 'Parent';
    
    #��������ν������
    &iptico($DT{'icon'})if$CF{'prtitm'}=~/\bicon\b/o;
    #���ν������
    #	&iptcol($DT{'color'})if$CF{'prtitm'}=~/\bcolor\b/o;
	
    #�ɲþ���
    $DT{'Sys'}=qq(<INPUT name="j" type="hidden" value="0">\n);
    if(defined$DT{'i'}){
	$DT{'caption'}='�� �Ƶ��������ե����� ��';
	$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
	$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
    }else{
	$DT{'caption'}='�� ������ƥե����� ��';
    }
	
    #���ܤν������
    $DT{'home'}='http://'unless$DT{'home'}; #http://��������Ƥ���
    $DT{'cook'}=$DT{'cook'}||!exists$DT{'cook'}?' checked':'';
	
    #�ե�����ź��
    my $attachForm = getAttachForm(\%DT);
    
    print<<"_HTML_";
<FORM accept-charset="euc-jp" id="artform" method="post" action="$CF{'index'}" enctype="multipart/form-data">
<DIV class="center"><TABLE align="center" class="note"><TR><TD><UL class="note">
<LI>��ʸ�ʳ��Ǥϥ����ϰ��ڻ��ѤǤ��ޤ���</LI>
<LI>HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���</LI>
<LI>����Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤���<BR>���Ф餯�ԤĤȴ�ñ���������ФƤ��ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE></DIV>



<DIV id="writingForm" class="box">
<H2 class="h"><A name="Form">$DT{'caption'}</A></H2>


<TABLE class="inputOthers">
<TR title="subJect&#10;��������̾�����Ϥ��ޤ�&#10;�ǹ�Ⱦ��70ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}"></TD>
<TH class="iconInputLabel" title="Icon&#10;������������򤷤ޤ�">
<LABEL accesskey="i" for="icon">�� <A href="$CF{'index'}?icct" title="�������󥫥���&#10;��������򳫤��ޤ�"
 target="_blank">��������</A>��<KBD class="ak">I</KBD>�ˢ�</LABEL></TH>
</TR>

<TR title="Name&#10;̾�������Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�Ⱦ��40ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="name" id="name" maxlength="40" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;���å�����¸��ON/OFF"
 >���å���¸<INPUT name="cook" id="cook" type="checkbox"$DT{'cook'}></LABEL></TD>
<TD rowspan="4" class="iconPreview" title="Icon Preview"
 ><IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
</TR>

<TR title="e-maiL&#10;�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item"><LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}"></TD>
</TR>

<TR title="hOme&#10;��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item"><LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}"></TD>
</TR>

<TR title="Password&#10;���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�&#10;����8ʸ�����ǹ�128ʸ���Ǥ�">
<TH class="item"><LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="pass" id="pass" maxlength="128" value="$DT{'pass'}">
��
<SPAN title="Color&#10;��ʸ�ο������Ϥ��ޤ�">
	<SPAN class="item"><LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL></SPAN>
	<SPAN class="input">@{[&iptcol($DT{'color'})]}</SPAN>
</SPAN>
</TD>
</TR>

<TR title="coMmand&#10;���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�&#10;'command=value'�Τ褦�˻��ꤷ�ޤ�">
<TH class="item"><LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()"></TD>
<TD class="input" title="Icon&#10;������������򤷤ޤ�">@{[&iptico($DT{'icon'})]}</TD>


$attachForm

</TABLE>


<TABLE class="inputBody">
<TR><TD class="leftColumn">&nbsp;</TD>
<TH class="item"
 title="Body:��������ʸ�����Ϥ��ޤ�&#10;������10000ʸ���ޤǤǤ�&#10;���ѤǤ��륿���ϥإ�פ򻲾�"
><LABEL accesskey="b" for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH>
<TD class="rightColumn">
<BUTTON accesskey="," class="buttonQuicksave"  title="��ʸ�ǡ�����QuickSave���ޤ�"
 onclick="quicksaveBodyData();return false" onkeypress="quicksaveBodyData();return false"
 >QSave(<KBD class="ak">,</KBD>)</BUTTON>
<BUTTON accesskey="." class="buttonLoadQuicksave" title="Quicksave�����ǡ������ɤ߹��ߤޤ�"
 onclick="loadBodyData('MireilleQuicksave');return false" onkeypress="loadBodyData('MireilleQuicksave');return false"
 >QLoad(<KBD class="ak">.</KBD>)</BUTTON>
<BUTTON accesskey="/" class="buttonLoadAutosave" title="Autosave�����ǡ������ɤ߹��ߤޤ�"
 onclick="loadBodyData('MireilleAutosave');return false" onkeypress="loadBodyData('MireilleAutosave');return false"
 >ALoad(<KBD class="ak">/</KBD>)</BUTTON>
</TD></TR>
<TR><TD colspan="3"><TEXTAREA name="body" id="body" cols="80" rows="8" onchange="if(!isLoaded)initialization()">$DT{'body'}</TEXTAREA></TD></TR>
</TABLE>


<P class="footer">$DT{'Sys'}
<INPUT type="submit" class="submit" accesskey="s" value="��Ƥ���">
<!-- <INPUT type="reset" class="reset" value="�ꥻ�å�"> --></P>


</DIV>



$CF{'jsWritingForms'}
</FORM>

_HTML_
    return 1;
}


#-------------------------------------------------
# �ҵ����ե�����
#
sub chdfrm{
    #�ֿ��ե��������
    my%DT=%CK;
    $DT{'_type'} = 'Child';
    
    #��������ν������
    &iptico($DT{'icon'})if$CF{'chditm'}=~/\bicon\b/o;
    #���ν������
    #	&iptcol($DT{'color'})if$CF{'chditm'}=~/\bcolor\b/o;
	
    #�ɲþ���
    $DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
    if(defined$DT{'j'}){
	$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
	$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
	$DT{'caption'}='�� �ҵ��������ե����� ��';
    }else{
	$DT{'caption'}='�� �ֿ���ƥե����� ��';
    }
	
    #���ܤν������
    $DT{'home'}='http://'unless$DT{'home'}; #http://��������Ƥ���
    $DT{'cook'}=$DT{'cook'}||!exists$DT{'cook'}?' checked':'';
    #note01:Res����̾�ʤ����Ȥ�
    if($CF{'chditm'}!~/\bsubject\b/o){
	$DT{'subject'}='disabled';
	$DT{'_isSubjectDisabled'}=' disabled';
    }else{
	$DT{'_isSubjectDisabled'}='';
    }
    
    #�ե�����ź��
    my $attachForm = getAttachForm(\%DT);
    
    
    print<<"_HTML_";
<FORM accept-charset="euc-jp" id="artform" method="post" action="$CF{'index'}" enctype="multipart/form-data">



<DIV id="writingForm" class="box">
<H2 class="h"><A name="Form">$DT{'caption'}</A></H2>


<TABLE class="inputBody">
<TR><TD class="leftColumn">&nbsp;</TD>
<TH class="item"
 title="Body:��������ʸ�����Ϥ��ޤ�&#10;������10000ʸ���ޤǤǤ�&#10;���ѤǤ��륿���ϥإ�פ򻲾�"
><LABEL accesskey="b" for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH>
<TD class="rightColumn">
<BUTTON accesskey="," class="buttonQuicksave"  title="��ʸ�ǡ�����QuickSave���ޤ�"
  onclick="quicksaveBodyData();return false" onkeypress="quicksaveBodyData();return false"
 >QSave(<KBD class="ak">,</KBD>)</BUTTON>
<BUTTON accesskey="." class="buttonLoadQuicksave" title="Quicksave�����ǡ������ɤ߹��ߤޤ�"
 onclick="loadBodyData('MireilleQuicksave');return false" onkeypress="loadBodyData('MireilleQuicksave');return false"
 >QLoad(<KBD class="ak">.</KBD>)</BUTTON>
<BUTTON accesskey="/" class="buttonLoadAutosave" title="Autosave�����ǡ������ɤ߹��ߤޤ�"
 onclick="loadBodyData('MireilleAutosave');return false" onkeypress="loadBodyData('MireilleAutosave');return false"
>ALoad(<KBD class="ak">/</KBD>)</BUTTON>
</TD></TR>
<TR><TD colspan="3"><TEXTAREA name="body" id="body" cols="80" rows="8" onchange="if(!isLoaded)initialization()">$DT{'body'}</TEXTAREA></TD></TR>
</TABLE>


<TABLE class="inputOthers">
<TR title="subJect&#10;��������̾�����Ϥ��ޤ�&#10;�ǹ�Ⱦ��70ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}"$DT{'_isSubjectDisabled'}></TD>
<TH class="iconInputLabel" title="Icon&#10;������������򤷤ޤ�">
<LABEL accesskey="i" for="icon">�� <A href="$CF{'index'}?icct" title="�������󥫥���&#10;��������򳫤��ޤ�"
 target="_blank">��������</A>��<KBD class="ak">I</KBD>�ˢ�</LABEL></TH>
</TR>

<TR title="Name&#10;̾�������Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�Ⱦ��40ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="name" id="name" maxlength="40" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;���å�����¸��ON/OFF"
 >���å���¸<INPUT name="cook" id="cook" type="checkbox"$DT{'cook'}></LABEL></TD>
<TD rowspan="4" class="iconPreview" title="Icon Preview"
 ><IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
</TR>

<TR title="e-maiL&#10;�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item"><LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}"></TD>
</TR>

<TR title="hOme&#10;��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item"><LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}"></TD>
</TR>

<TR title="Password&#10;���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�&#10;����8ʸ�����ǹ�128ʸ���Ǥ�">
<TH class="item"><LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="pass" id="pass" maxlength="128" value="$DT{'pass'}">
��
<SPAN title="Color&#10;��ʸ�ο������Ϥ��ޤ�">
	<SPAN class="item"><LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL></SPAN>
	<SPAN class="input">@{[&iptcol($DT{'color'})]}</SPAN>
</SPAN>
</TD>
</TR>

<TR title="coMmand&#10;���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�&#10;'command=value'�Τ褦�˻��ꤷ�ޤ�">
<TH class="item"><LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL></TH>
<TD class="input"><INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()"></TD>
<TD class="input" title="Icon&#10;������������򤷤ޤ�">@{[&iptico($DT{'icon'})]}</TD>
</TR>

$attachForm

</TABLE>


<P class="footer">$DT{'Sys'}
<INPUT type="submit" class="submit" accesskey="s" value="��Ƥ���">
<!-- <INPUT type="reset" class="reset" value="�ꥻ�å�"> --></P>


</DIV>



<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>���ɽ������Ƥ��륹��åɡ�No.$DT{'i'}�ۤؤ��ֿ���Ԥ��ޤ���</LI>
<LI>��ʸ�ʳ��Ǥϥ����ϰ��ڻ��ѤǤ��ޤ���</LI>
<LI>HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���</LI>
<LI>����Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤���<BR>���Ф餯�ԤĤȹ��ܤδ�ñ���������ФƤ��ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE></DIV>

$CF{'jsWritingForms'}
</FORM>
_HTML_
    return 1;
}


#-------------------------------------------------
# �ե�����ź�եե�����
sub getAttachForm{
    $CF{'Attach'} > 0 or return '';
    my %DT = %{shift()};
    my $length = $CF{'Attach'.$DT{'_type'}.'Length'};
    my $html = '';
    my @array;
    if($DT{'attach'}){
	my $attach = MirString::urldecode($DT{'attach'});
	if( ref$attach eq 'ARRAY' ){
	    @array = @{$attach};
	}elsif( ref$attach eq 'HASH' ){
	    push @array, $attach;
	}
	$#array = $length - 1 if @array > $length;
	for( grep{ref$_ eq 'HASH'}@array ){
	    my $item = $_;
	    my $filename = $item->{'filename'} || "$item->{'hash'}.$item->{'ext'}";
	    my $attach = sprintf('%s?mode=download&hash=%s',$CF{'index'},$item->{'hash'});
	    $html .= <<"_HTML_";
<A href="$attach">$filename</A>
[<LABEL for="remove_attach__$item->{'hash'}"><INPUT type="checkbox" id="remove_attach__$item->{'hash'}" name="remove_attach__$item->{'hash'}" value="$item->{'hash'}">���</LABEL>]
_HTML_
	}
    }
    for( my $i = 0; $i < $length - @array; $i++ ){
	$html .= qq{<INPUT id="attach__$i" name="attach__$i" type="file">\n};
    }
    
    return <<"_HTML_";
<TR title="attach&#10;�ե������ź�դ��ޤ�">
<TH class="item"><LABEL>���ե�����ź�ա�</LABEL></TH>
<TD class="input" colspan="2">$html</TD>
</TR>
_HTML_
}


#-------------------------------------------------
# �ڡ�������BOX
sub getPageSelectorSkin{
    my$following=shift;
    my$pageList =shift;
    my$preceding=shift;
    #	my($str,$end,$pags,$mode)=@_; #���Ϥ��Ȥ�Ω�Ƥ�������
    return<<"_HTML_";
<TABLE align="center" border="1" cellspacing="0" class="pageSelector">
<TR>
<TD class="following">$following</TD>
<TD class="pageList">[ $pageList ]</TD>
<TD class="preceding">$preceding</TD>
</TR>
</TABLE>
_HTML_
}


#-------------------------------------------------
# ɽ��ε�������ɽ����
sub getArticoleInfomationA{
    my%data=@_;
    return<<"_HTML_";
<DIV class="artinfo">
$data{'unread'}
$data{'pageSelector'}
<P class="artinfo">���Υڡ����Υ���å�<BR>\n[ $data{'this'}]<BR>
<A name="nav_n0" href="#nav_s1" title="���Υ���åɤ�" accesskey="0">��</A></P>
</DIV>
_HTML_
}


#-------------------------------------------------
# ɽ��ε�������ɽ����
sub getArticoleInfomationB{
    my%data=@_;
    return<<"_HTML_";
<DIV class="artinfo">
<P class="artinfo"><A name="nav_s@{[$data{'view'}+2]}" href="#nav_n@{[$data{'view'}+1]}" title="��Υ���åɤ�" accesskey="&#@{[$data{'view'}+50]};">��</A><BR>
���Υڡ����Υ���å�<BR>\n[ $data{'this'}]</P>

$data{'pageSelector'}
</DIV>
_HTML_
}


#-------------------------------------------------
# �񤭹��ߤ����������ĥ����������
sub exprewrt{
    return 0;
}


#-------------------------------------------------
# �������ɽ���Ѥ˥ե����ޥåȤ��줿���ռ������֤�
sub date{
=item ����
$ time��������
=cut
    $CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
    my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($_[0]+$CF{'timeOffset'});
    #sprintf�������ϡ�Perl�β���򸫤Ƥ�������^^;;
    return sprintf("%4dǯ%02d��%02d��(%s) %02d��%02dʬ%s" #"1970ǯ01��01��(��) 09��00ʬ"����
		   ,$year+1900,$mon+1,$day,('��','��','��','��','��','��','��')[$wday],$hour,$min,$ENV{'TZ'});
    #	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"����
    #	,$hour,$min,$sec,$year+1900,$mon+1,$day,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
#�����ʥ�
sub artnavi{
=item ����
$ �����ʥӤΥ⡼��
=cut
    return if defined$::CF{'artnavi'}&&!$::CF{'artnavi'};
	
    #Netscape4�ϵ����ʥ�̵��
    return($::CF{'artnavi'}=0)if$::IN{'hua'}=~/^Mozilla\/4.*(?:;\s*|\()[UI](?:;|\))/;
	
    unless(@_){
	#�����ʥ�����
	#------------------------------------------------------------------------------------
	#�֥饦��Ƚ��
	my$style='display:none;position:fixed';
	unless($::IN{'hua'}){
	    #guess to be WinIEorMozilla
	}elsif(index($::IN{'hua'},'Opera 6')>-1||index($::IN{'hua'},'Opera/6')>-1){
	    #guess to be Opera6
	    $style='display:block;position:fixed;top:-1000;left:-1000;visibility:visible;/*Opera6*/';
	}elsif(index($::IN{'hua'},'MSIE 4')>-1){
	    #guess to be MSIE 4
	    $style='display:none;position:absolute;position:fixed;filter:alpha(opacity=60)';
	}
		
	print<<"_HTML_";
<!--[if gte IE 7]>
<DIV id="naviwind" style="display:none;position:fixed;filter:alpha(opacity=60)">
<![endif]-->
<!--[if lt IE 7]>
<DIV id="naviwind" style="display:none;position:absolute;filter:alpha(opacity=60)">
<![endif]-->
<![if ! IE]>
<DIV id="naviwind" style="$style">
<![endif]>
<TABLE id="navihead" cellspacing="1" summary="ArtNavi Header">
<COL span="2">
<TR>
<TH id="navititl" onmousedown="beginDrag(event,'naviwind')">�������ʥ� - Mireille</TH>
<TD id="navibutt" style="width:35px" onmousedown="beginDrag(event,'naviwind')">
<A accesskey="m" onclick="void(view(event,'navibody'))" onkeydown="acskey(event,'navibody')"
 href="#����/�̾�" title="����/�̾�(&amp;M)">��</A>
<A accesskey="c" onclick="void(view(event,'naviwind'))" onkeydown="acskey(event,'naviwind')"
 href="#�Ĥ���" title="�Ĥ���(&amp;C)">��</A></TD>
</TR>
</TABLE>
<DIV id="navibody" style="display:block">
@{[ArtNavi->body]}</DIV>
</DIV>
<SCRIPT type="text/javascript" src="$::CF{'navjs'}" defer></SCRIPT>
_HTML_
	#------------------------------------------------------------------------------------
    }elsif('button'eq$_[0]){
	print<<"_HTML_";
<DIV><BUTTON onclick="setTimeout(&#34;artnavi('popup')&#34;,500);return false;" accesskey="n"
onkeypress="setTimeout(&#34;artnavi('popup')&#34;,500);return false;">�����ʥ�(<SPAN class="ak">N</SPAN>)</BUTTON></DIV>
_HTML_
    }
    return;
}

#-------------------------------------------------
# �����ʥӥ��饹
{package ArtNavi;
    my$ArtNaviBody='';
    #�����ʥӤ���ʸ -- ���饹�᥽�å�
    sub ArtNavi::body{
	my$class=shift;
	$ArtNaviBody=shift if@_>0;
	$ArtNaviBody
    }
	
    #�����ʥӤΥ���åɥإå��ɲ� -- ���饹�᥽�å�
    sub ArtNavi::addThreadHead{
	my$class=shift;
	my%DT=%{shift()};
	my$subject=$DT{'subject'}; #MirString->getTruncated($DT{'subject'},45);
	$ArtNaviBody.=<<"_HTML_";
<DIV class="navithre">
<DIV class="navisubj">
<A href="#nav_r$DT{'i'}" title="�ֿ�"><STRONG>$DT{'i'}</STRONG></A>:
<A href="#art$DT{'i'}">$subject</A>
</DIV>
<DIV class="navinums">
_HTML_
    }
	
    #�����ʥӤΥ���åɥեå��ɲ� -- ���饹�᥽�å�
    sub ArtNavi::addThreadFoot{
	my$class=shift;
	my%DT=%{shift()};
	$ArtNaviBody.=<<"_HTML_";
<A href="$CF{'index'}?res=$DT{'i'}#Form" title="�ֿ�" style="color:green;">Re</A>
</DIV>
</DIV>
_HTML_
    }
	
    #�����ɲ� -- ���饹�᥽�å�
    sub ArtNavi::addArticle{
	my$class=shift;
	my%DT=%{shift()};
	my$isNew=shift;
	if($isNew){
	    #̤��
	    $ArtNaviBody.=qq(<A class="new" href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A> );
	    return;
	}else{
	    #����
	    $ArtNaviBody.=qq(<A href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A> );
	    return;
	}
    }
}
package main;

$CF{'_HiraganaLetterA'}->{'Style'}='��';
#require��style.cgi��Revision���֤�
($CF{'Style'}=qq$Revision$)=~/(\d+(?:\.\d+)*)/o;
$CF{'StyleRevision'}=$1;
__END__
