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
<LINK rel="Index" href="index.cgi">
<LINK rel="Help" href="index.cgi?help">
<LINK rel="Stylesheet" type="text/css" href="$CF{'style'}">
<TITLE>$CF{'title'}</TITLE>
_CONFIG_

#-----------------------------
# Mireile Menu
$CF{'menu'}=<<"_CONFIG_";
<TABLE align="center" border="1" cellspacing="3" class="menu" summary="MireilleMenu"><TR>
<TD class="menu"><A href="index.cgi?new#Form">�������</A></TD>
<TD class="menu"><A href="index.cgi">����</A></TD>
<TD class="menu"><A href="index.cgi?rvs">����</A></TD>
<TD class="menu"><A href="index.cgi?del">���</A></TD>
<TD class="menu"><A href="index.cgi?icct">��������</A></TD>
<TD class="menu"><A href="index.cgi?seek">����</A></TD>
<TD class="menu"><A href="index.cgi?help">�إ��</A></TD>
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
<TH width="100%"><H1 class="head" align="right"><A href="@{[
	$_[0]?qq($CF{'home'}">BACK to HOME):qq(index.cgi">BACK to INDEX)
]}</A></H1></TH>
</TR></TABLE></DIV>
_HTML_
}
$CF{'pgfoot'}=&getPageFooter;

#-----------------------------
# ��ƥե�����ǻȤ�JavaScript
$CF{'jsWritingForms'}=<<"_CONFIG_";
<SCRIPT type="text/javascript" defer>
<!--
var iconDirectory='$CF{'icon'}';
var iconSetting=@{[$CF{'absoluteIcon'}?1:0]}+@{[$CF{'relativeIcon'}?1:0]}*2
_CONFIG_
$CF{'jsWritingForms'}.=<<'_CONFIG_';
/*========================================================*/
// Change Icon Preview
function changePreviewIcon(){
	var icon,cmd;
	if(document.all){
		icon=document.all('icon');
		cmd =document.all('cmd');
	}else if(document.getElementById){
		icon=document.getElementById('icon');
		cmd =document.getElementById('cmd');
	}else return false;
	var preview=document.images['Preview'];
	
	if(!cmd||!cmd.value){
		icon.disabled=false;
	}else if(iconSetting&1&&cmd.value.match(/(^|;)absoluteIcon=([^;]*)/)){
		//���л��ꥢ������
		preview.src=RegExp.$2;
		preview.title=RegExp.$2;
		icon.disabled=true;
	}else if(iconSetting&2&&cmd.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//���л��ꥢ������
		preview.src=iconDirectory+RegExp.$2;
		preview.title=RegExp.$2;
		icon.disabled=true;
	}else{
		icon.disabled=false;
	}
	if(!icon.disabled){
		if(preview.src!=iconDirectory+icon.value)preview.src=iconDirectory+icon.value;
		if(preview.title!=icon.value)preview.title=icon.value;
	}
	return true;
}


/*========================================================*/
// Save/Load BodyData from Cookie
function saveBodyCk(){
	if(!confirm("��������ʸ����¸����ȡ��Ť���ʸ�ǡ����Ͼä��Ƥ��ޤ��ޤ�\n����Ǥ���¸���Ƥ�����Ǥ�����"))
		return false;
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	
	var backup='';
	if(document.cookie.match(/(^|; )MirBody=([^;]+)/))backup=unescape(RegExp.$2);
	if(!bodyObj.value.length){
		//value����
		document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
		if(bodyObj.addBehavior){
			//bahavior�ǡ�IE��¸��
			if(!bodyObj.getAttribute('MireilleBody'))bodyObj.addBehavior('#default#userData');
			bodyObj.setAttribute('MireilleBody','');
			bodyObj.save('MireilleBody');
		}
		alert('�����¸����Ƥ�����ʸ�ǡ����������ޤ���');
		return;
	}else if(bodyObj.addBehavior){
		//bahavior�ǡ�IE��¸�ˡʥ���������128KB��
		if(!bodyObj.getAttribute('MireilleBody'))bodyObj.addBehavior('#default#userData');
		bodyObj.setAttribute('MireilleBody',bodyObj.value);
		bodyObj.save('MireilleBody');
		alert("������ʸ�ǡ���������¸���ޤ���\n�����ޤ�IE�ˤ��Ȱ����¸�ɤ�����΅���ʤ��Ǥ�������");
	}else{
		//Cookie�ǡʥ���������3KB�ۤɡ�
		document.cookie='MirBody='+escape(bodyObj.value)+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';
		if(document.cookie.match(/(^|; )MirBody=([^;]+)/)&&bodyObj.value==unescape(RegExp.$2)){
			alert("������ʸ�ǡ���������¸���ޤ�����\n�����ޤǡȰ����¸�ɤ�����΅���ʤ��Ǥͤ�");
		}else{
			//3850byte���٤ǥ��������¤������롣
			document.cookie='MirBody='+backup+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//��������
			alert("save����\n�����������С����⡣");
			return false;
		}
	}
}
function loadBodyCk(){
	if(!confirm("Cookie������ʸ�ǡ������ɤ߽Ф��ȡ����ߤ���ʸ�Ͼä��Ƥ��ޤ��ޤ�\n����Ǥ��ɤ߽Ф��Ƥ�����Ǥ�����"))
		return false;
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	
	if(bodyObj.addBehavior){
		if(!bodyObj.getAttribute('MireilleBody'))bodyObj.addBehavior('#default#userData');
		bodyObj.load('MireilleBody');
		var temp=bodyObj.getAttribute('MireilleBody');
		if(temp)bodyObj.value=temp;
	}else if(document.cookie.match(/(^|; )MirBody=([^;]+)/)){
		bodyObj.value=unescape(RegExp.$2);
	}else{
		alert('load����');
		return false;
	}
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
		if('button'==tags[i].type||'button'==tags[i].className){
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
		}else if('text'==tags[i].type||'password'==tags[i].type){
			tags[i].className='blur';
			tags[i].onfocus=function()	{this.className='focus';};
			tags[i].onblur=function()	{this.className='blur';};
		}
	}
	tags=document.getElementsByTagName('TEXTAREA');
	for(var i in tags){
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
<TABLE align="center" class="note" summary="��ս�"><TR><TD><UL class="note">
<LI>��Ƥ��줿����������ϴ����Ԥδ������ˤ�����ޤ���</LI>
<LI>̤�ɵ���������������֤�ɽ������ޤ���</LI>
<LI>24���ְ������Ƥˤ�$CF{'new'}�ޡ������դ��ޤ���</LI>
<LI>�����ʥ�С��򥯥�å�����ȡ����ε����ν������̤ˤʤ�ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE>

_CONFIG_

#-----------------------------
# �������/�Խ��ե�����
$CF{'wrtfm'}=<<'_CONFIG_';
<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>��ʸ�ʳ��Ǥϥ����ϰ��ڻ��ѤǤ��ޤ���</LI>
<LI>HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���</LI>
<LI>����Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤���<BR>���Ф餯�ԤĤȴ�ñ���������ФƤ��ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE></DIV>

<DIV class="center"><TABLE border="2" cellspacing="0" class="write" summary="MainForm">
<COL span="3">
<THEAD><TR><TH colspan="3" class="caption"><A name="Form"></A>$DT{'caption'}</TH></TR></THEAD>

<TBODY>
<TR title="subJect&#10;��������̾�����Ϥ��ޤ�&#10;�ǹ�����100ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon&#10;������������򤷤ޤ�" style="text-align:center">
<LABEL accesskey="i" for="icon">�� <A href="index.cgi?icct" title="����������&#10;��������򳫤��ޤ�" target="_blank">��������</A>��<KBD class="ak">��</KBD>�ˢ�</LABEL>
</TH>
</TR>
<TR title="Name&#10;̾�������Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�����50ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;���å�����¸��ON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL&#10;�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme&#10;��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password&#10;���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
��
<SPAN title="Color&#10;��ʸ�ο������Ϥ��ޤ�">
<SPAN class="item">
<LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand&#10;���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�&#10;'command=value'�Τ褦�˻��ꤷ�ޤ�">
<TH class="item">
<LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()">
</TD>
<TD class="input" title="Icon&#10;������������򤷤ޤ�">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>

<TBODY title="Body&#10;��������ʸ�����Ϥ��ޤ�&#10;������10000ʸ���ޤǤǤ�&#10;���ѤǤ��륿���ϥإ�פ򻲾Ȥ��Ƥ�������">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center">
<TEXTAREA name="body" id="body" cols="80" rows="8">$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY><TR title="Submit&#10;��������Ƥ��ޤ�">
<TD colspan="3" class="foot">
<INPUT type="submit" class="submit" accesskey="s" value="��Ƥ���">
<!-- <INPUT type="reset" class="reset" value="�ꥻ�å�"> -->
<INPUT type="button" class="button" accesskey="," value="�����¸," onclick="saveBodyCk()" onkeypress="saveBodyCk()">
<INPUT type="button" class="button" accesskey="." value="�ɤ߹���." onclick="loadBodyCk()" onkeypress="loadBodyCk()">
</TD></TR></TBODY>

</TABLE>
</DIV>

$CF{'jsWritingForms'}
_CONFIG_

#-----------------------------
# �ֿ��ե�����
$CF{'resfm'}=<<'_CONFIG_';
<DIV class="center"><TABLE border="2" cellspacing="0" class="write" summary="ResForm">
<COL span="3">
<THEAD><TR><TH colspan="3" class="caption"><A name="Form"></A>$DT{'caption'}</TH></TR></THEAD>

<TBODY title="Body&#10;��������ʸ�����Ϥ��ޤ�&#10;������10000ʸ���ޤǤǤ�&#10;���ѤǤ��륿���ϥإ�פ򻲾Ȥ��Ƥ�������">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center">
<TEXTAREA name="body" id="body" cols="80" rows="8">$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY>
<TR title="subJect&#10;��������̾�����Ϥ��ޤ�&#10;�ǹ�����100ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL></TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon&#10;������������򤷤ޤ�" style="text-align:center">
<LABEL accesskey="i" for="icon">�� <A href="index.cgi?icct" title="����������&#10;��������򳫤��ޤ�" target="_blank">��������</A>��<KBD class="ak">��</KBD>�ˢ�</LABEL>
</TH>
</TR>
<TR title="Name&#10;̾�������Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�����50ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;���å�����¸��ON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL&#10;�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme&#10;��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password&#10;���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�&#10;�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
��
<SPAN title="Color&#10;��ʸ�ο������Ϥ��ޤ�">
<SPAN class="item">
<LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand&#10;���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�&#10;'command=value'�Τ褦�˻��ꤷ�ޤ�">
<TH class="item">
<LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()">
</TD>
<TD class="input" title="Icon&#10;������������򤷤ޤ�">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>
<TBODY>
<TR title="Submit&#10;��������Ƥ��ޤ�">
<TD colspan="3" class="foot">
<INPUT type="submit" class="submit" accesskey="s" value="��Ƥ���">
<!-- <INPUT type="reset" class="reset" value="�ꥻ�å�"> -->
<INPUT type="button" class="button" accesskey="," value="�����¸," onclick="saveBodyCk()" onkeypress="saveBodyCk()">
<INPUT type="button" class="button" accesskey="." value="�ɤ߹���." onclick="loadBodyCk()" onkeypress="loadBodyCk()">
</TD></TR>
</TBODY>
</TABLE>
<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>���ɽ������Ƥ��륹��åɡ�No.$DT{'i'}�ۤؤ��ֿ���Ԥ��ޤ���</LI>
<LI>��ʸ�ʳ��Ǥϥ����ϰ��ڻ��ѤǤ��ޤ���</LI>
<LI>HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���</LI>
<LI>����Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤���<BR>���Ф餯�ԤĤȹ��ܤδ�ñ���������ФƤ��ޤ���</LI>
<LI>����¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������</LI>
</UL></TD></TR></TABLE></DIV>

$CF{'jsWritingForms'}
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
	my%DT=(new=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
	#������줿���Τ餻��
	'del'eq$DT{'Mir12'}&&($DT{'body'}='Mireille: [���ε����Ϻ������ޤ���]');
	#�����ʥ�
	ArtNavi->addThreadHead(\%DT);
	ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
	#�������ܤ�Ĵ���򤷤�
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">��HOME��</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
	$DT{'-iconTag'}=&getIconTag(\%DT)||'&nbsp;';
	#̤�ɵ����˰�
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#���褤����Ϥ���
	print<<"_HTML_";
<DIV class="thread" title="$DT{'i'}�֥���å�">
<TABLE cellspacing="0" class="subject" summary="$DT{'i'}�֥���å�"><TR>
<TH class="subject"><H2 class="subject"><A name="art$DT{'i'}" id="art$DT{'i'}" title="$DT{'i'}�֥���å�">$DT{'subject'}</A></H2></TH>
<TD class="arrow">
<A name="nav_n$DT{'ak'}" href="#nav_n@{[$DT{'ak'}-1]}" title="��Υ���åɤ�">��</A>
<A name="nav_r$DT{'i'}" href="index.cgi?res=$DT{'i'}#Form" title="���ε���No.$DT{'i'}���ֿ�">��</A>
<A name="nav_s$DT{'ak'}" href="#nav_s@{[$DT{'ak'}+1]}" title="���Υ���åɤ�">��</A>
</TD>
</TR></TABLE>

<TABLE cellspacing="0" class="parent" summary="Article$DT{'i'}-0" title="$DT{'i'}-0">
<COL class="number"><COL class="name"><COL class="date">
<TR class="info">
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">��No.$DT{'i'}��</A></TH>
	<TD class="name">$DT{'new'} <SPAN class="name">$DT{'name'}</SPAN>
	<SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤοƵ�������"><A
	 href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'-iconTag'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
</TABLE>

_HTML_
	return;
}


#-------------------------------------------------
#�ҵ���
sub artchd{
=item ����
\% ����åɤε�������ϥå���Υ�ե����
$	���ε����ξ���
=cut
	#��������������ä�
	my%DT=(new=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));

	#�������Ƥ�Ȥ��Ϥ������������Ф����㤦��
	#�����ʥ�
	ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
	#�������ܤ�Ĵ���򤷤�
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">��HOME��</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
	$DT{'-iconTag'}=&getIconTag(\%DT)||'&nbsp;';
	#̤�ɵ����˰�
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#���褤����Ϥ���
	print<<"_HTML_";
<TABLE cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}" title="$DT{'i'}-$DT{'j'}">
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
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">��Re:$DT{'j'}��</A></TH>
	<TD class="name">$DT{'new'} <SPAN class="name">$DT{'name'}</SPAN>
	<SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤλҵ���$DT{'j'}����"
	><A href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'-iconTag'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
</TABLE>

_HTML_
	return;
}


#-------------------------------------------------
#�����եå�
sub artfot{
=item ����
\% �������� �ϥå���Υ�ե����
=cut
	#��������������ä�
	my%DT=%{shift()};
	
	if($DT{'res'}||$CF{'readOnly'}){
		#�ֿ��⡼�ɤΤȤ�
			print<<'_HTML_';
</DIV>


_HTML_
	}else{
		#����ɽ��
		if($CF{'maxChilds'}&&$DT{'j'}>=$CF{'maxChilds'}){
			#�ҵ��������¤�Ķ����
			print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}" class="warning"
 href="#res$DT{'i'}">���ε�������å�No.$DT{'i'}�ϻҵ��������¤�ã�����Τ��ֿ��Ǥ��ޤ���(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
#memo.
#�ֿ��⡼�ɤ��ʤ��Τˡ�href="#res$DT{'i'}"�פȥ�󥯤�ĥ�äƤ���Τϡ�����������������Ѳ�ǽ�ˤ��뤿��
		}else{
			#���ε�������å�No.???���ֿ�����(?)
		print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}"
 href="index.cgi?res=$DT{'i'}#art$DT{'i'}-$DT{'j'}">���ε�������å�No.$DT{'i'}���ֿ�����(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
		}
	}
	#�����ʥ�
	ArtNavi->addThreadFoot(\%DT);
}


#-------------------------------------------------
# �Ƶ����ե�����
#
sub prtfrm{
	my%DT=%CK;

	#��������ν������
	($CF{'prtitm'}=~/\bicon\b/o)&&(&iptico($DT{'icon'}));
	#���ν������
#	($CF{'prtitm'}=~/\bcolor\b/o)&&(&iptcol($DT{'color'}));

=item ���ν������ΰյ�

���ν���������ϰ츫ɬ�פʤ������Ǥ�
�������ץ�ӥ塼��ǽ�Ȥ�����Τ����ηǼ��ĤˤϤ���ޤ�
�̾��<IMG src="$DT{'icon'}">�Ȥ��Ƥ���櫓�Ǥ�����
$DT{'icon'}�������ä��顢�⤷����¸�ߤ��ʤ�����������ä���ɤ����ޤ��礦
���������ä����ꤹ�뤿��ˤ����ǥꥹ�ȤȾȹ礷�Ƥ����櫓�Ǥ�
â��������Ͻ���ǥ�����Τ褦�ˤ���IMG��������������ꥹ�Ȥ�SELECT������ꡢ
���ˤ����������ǡ��ץ�ӥ塼��ʬ���������ʬ�����ξ��ϡ�
�������򥳥��ȥ����Ȥ��Ƥ����ꤢ��ޤ���

=cut

	my$wrtfm=$CF{'wrtfm'};
	chomp$wrtfm;
	if(defined$DT{'body'}){
		$DT{'caption'}='�� ���������ե����� ��';
		$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
	}else{
		$DT{'caption'}='�� ���������ե����� ��';
		$DT{'home'}||($DT{'home'}='http://');
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="0">\n);
	}
	$DT{'Sys'}&&($wrtfm=~s/<INPUT/$DT{'Sys'}<INPUT/io);
	
	print qq(<FORM accept-charset="euc-jp" id="artform" method="post" action="index.cgi">\n);
	eval qq(print<<"_HTML_";\n$wrtfm\n_HTML_);
	print"</FORM>\n";
}


#-------------------------------------------------
# �ҵ����ե�����
#
sub chdfrm{
	#�ֿ��ե��������
	my%DT=%CK;
	
	#��������ν������
	($CF{'chditm'}=~/\bicon\b/o)&&(&iptico($DT{'icon'}));
	#���ν������
#	($CF{'chditm'}=~/\bcolor\b/o)&&(&iptcol($DT{'color'}));
	
	#�ǥ������ɤ߹���
	my$resfm=$CF{'resfm'};
	chomp$resfm;#�Ǹ�β��Ԥ��ڤ���Ȥ�
	#�ɲþ����������
	$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
	if(defined$DT{'j'}){
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
		$DT{'caption'}='�� �����ե����� ��';
	}else{
		$DT{'caption'}='�� �ֿ��ե����� ��';
	}
	$DT{'Sys'}&&($resfm=~s/<INPUT/$DT{'Sys'}<INPUT/io);

	#���ܤν������
	$DT{'home'}||($DT{'home'}='http://'); #http://��������Ƥ���
	#note01:Res����̾�ʤ����Ȥ�
	if($CF{'chditm'}!~/\bsubject\b/o){
		$DT{'subject'}='disabled';
		$resfm=~s/name="subject"/name="subject" disabled="disabled"/io;
	}
	
	print<<"_HTML_";
<FORM accept-charset="euc-jp" id="artform" method="post" action="index.cgi">
_HTML_
	eval qq(print<<"_HTML_";\n$resfm\n_HTML_);
	print"</FORM>\n";
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
	if($::IN{'hua'}=~/^Mozilla\/4.*(?:;\s*|\()[UI](?:;|\))/){
		$::CF{'artnavi'}=0;
		return; #�����ʥӤ���Ϥ��ʤ�
	}
	
	unless($_[0]){
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
			$style='display:none;position:absolute;filter:alpha(opacity=60)';
		}
		
		print<<"_HTML_";
<!--[if IE]>
<DIV id="naviwind" style="display:none;position:absolute;filter:alpha(opacity=60)">
<![endif]--><![if ! IE]>
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
		return;
	}elsif('button'eq$_[0]){
		print<<"_HTML_";
<DIV><BUTTON onclick="setTimeout(&#34;artnavi('popup')&#34;,500);return false;" accesskey="n"
onkeypress="setTimeout(&#34;artnavi('popup')&#34;,500);return false;">�����ʥ�(<SPAN class="ak">N</SPAN>)</BUTTON></DIV>
_HTML_
		return;
	}
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
		$ArtNaviBody.=<<"_HTML_";
<DIV class="navithre">
<DIV class="navisubj">
<A href="#nav_r$DT{'i'}" title="�ֿ�"><STRONG>$DT{'i'}</STRONG></A>:
<A href="#art$DT{'i'}">$DT{'subject'}</A>
</DIV>
<DIV class="navinums">
_HTML_
	}
	
	#�����ʥӤΥ���åɥեå��ɲ� -- ���饹�᥽�å�
	sub ArtNavi::addThreadFoot{
		my$class=shift;
		my%DT=%{shift()};
		$ArtNaviBody.=<<"_HTML_";
<A href="index.cgi?res=$DT{'i'}#Form" title="�ֿ�" style="color:green;">Re</A>
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

#require��style.cgi��Revision���֤�
($CF{'Style'}=qq$Revision$)=~/(\d+(?:\.\d+)*)/o;
$CF{'StyleRevision'}=$1;
__END__
