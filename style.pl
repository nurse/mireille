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
use strict;
use vars qw(%CF %IC %IN %CK);

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
# �ե�������JavaScript
$CF{'form_jscript'}=<<'_CONFIG_';
<SCRIPT type="text/javascript" defer>
<!--
// Save/Load BodyData from Cookie
function saveBodyCk(){
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	if(confirm("��������ʸ����¸����ȡ��Ť���ʸ�ǡ����Ͼä��Ƥ��ޤ��ޤ�\n����Ǥ���¸������äƤ褤�Ǥ�����")){
		var backup='';
		if(document.cookie.match(/(^|; )MirBody=([^;]+)/))backup=unescape(RegExp.$2);
		if(bodyObj.value.length){
			document.cookie='MirBody='+escape(bodyObj.value)+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';
		}else{
			document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
			alert('�����¸����Ƥ�����ʸ�ǡ����������ޤ�����');
			return;
		}
		if(!document.cookie.match(/(^|; )MirBody=([^;]+)/)){
			//3850byte���٤ǥ��������¤������롣
			document.cookie='MirBody='+backup+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//��������
			alert("save����\n�����������С����⡣");
			return false;
		}
		alert("������ʸ�ǡ���������¸���ޤ�����\n�����ޤǡȰ����¸�ɤ�����΅���ʤ��Ǥͤ�");
	}
}
function loadBodyCk(){
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	if(!confirm('Cookie������ʸ�ǡ�������ɤ��ޤ��衩��'))return;
	if(!document.cookie.match(/(^|; )MirBody=([^;]+)/)){
		alert('load����');
		return false;
	}
	bodyObj.value=unescape(RegExp.$2);
}


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
	.$CF{'bodyFoot'}.$CF{'form_jscript'}."</BODY>\n</HTML>\n";
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
# �Ƶ���
$CF{'artprt'}=<<'_CONFIG_';
<DIV class="thread" title="$DT{'i'}�֥���å�">
<TABLE border="0" cellspacing="0" class="subject" summary="$DT{'i'}�֥���å�" width="100%">
<TR>
<TH class="subject"><H2 class="subject"><A name="art$DT{'i'}" id="art$DT{'i'}" title="$DT{'i'}�֥���å�">$DT{'subject'}</A></H2></TH>
<TD class="arrow">
<A name="nav_n$DT{'ak'}" href="#nav_n@{[$DT{'ak'}-1]}" title="��Υ���åɤ�">��</A>
<A name="nav_r$DT{'i'}" href="index.cgi?res=$DT{'i'}#Form" title="���ε���No.$DT{'i'}���ֿ�">��</A>
<A name="nav_s$DT{'ak'}" href="#nav_s@{[$DT{'ak'}+1]}" title="���Υ���åɤ�">��</A>
</TD></TR>
</TABLE>

<TABLE border="0" cellspacing="0" class="parent" summary="Article$DT{'i'}-0" title="$DT{'i'}-0" width="100%">
<COL class="number"><COL class="name"><COL class="date">
<TR class="info">
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" id="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">��No.$DT{'i'}��</A></TH>
	<TD class="name">$DT{'new'}&nbsp;<SPAN class="name">$DT{'name'}</SPAN><SPAN class="nbsp">&nbsp;&nbsp;</SPAN><SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN><SPAN class="nbsp">&nbsp;&nbsp;</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤοƵ�����������"><A
	 href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR>
	<!-- �����������Ѥ����礳������ -->
	<TD class="icon"><IMG src="$CF{'icon'}$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD>
	<!-- �����������Ѥ����礳���ޤ� -->
	<!-- �����������Ѥ��ʤ���礳������ -->
	<!-- <TD colspan="3" class="body" style="color:\$DT{'color'}">\$DT{'body'}</TD> -->
	<!-- �����������Ѥ��ʤ���礳���ޤ� -->
</TR>
</TABLE>

_CONFIG_

#-----------------------------
# �ҵ���
$CF{'artchd'}=<<'_CONFIG_';
<TABLE border="0" cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}" title="$DT{'i'}-$DT{'j'}">
<COL class="space"><COL class="number"><COL class="name"><COL class="date">
<!-- �ҵ��������ȥ����Ѥ����硢����1�Ԥ򥳥��ȳ��� -->
<!-- <TR><TH class="space" rowspan="3">&nbsp;</TH>
<TH colspan="3" class="subject"><H3 class="subject">\$DT{'subject'}</H3></TH></TR> -->
<TR class="info">
	<!-- �ҵ��������ȥ����Ѥ����硢�����ȥ����� --><TH class="space" rowspan="2">&nbsp;</TH><!-- -->
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" id="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">��Re:$DT{'j'}��</A></TH>
	<TD class="name">$DT{'new'}&nbsp;<SPAN class="name">$DT{'name'}</SPAN>
	<SPAN class="nbsp">&nbsp;&nbsp;</SPAN><SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN><SPAN class="nbsp">&nbsp;&nbsp;</SPAN>
	<SPAN class="revise" title="$DT{'i'}�֥���åɤοƵ�����������"><A
	 href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">�ڽ�����</A></SPAN></TD>
</TR>
<TR>
	<!-- �����������Ѥ����礳������ -->
		<TD class="icon"><IMG src="$CF{'icon'}$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
		<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD>
	<!-- �����������Ѥ����礳���ޤ� -->
	<!-- �����������Ѥ��ʤ���礳������ -->
	<!-- <TD colspan="3" class="body" style="color:\$DT{'color'}">\$DT{'body'}</TD> -->
	<!-- �����������Ѥ��ʤ���礳���ޤ� -->
</TR>
</TABLE>

_CONFIG_

#-----------------------------
# �����Υեå����ʵ���ɽ���⡼�ɡ�
$CF{'artfot'}=<<'_CONFIG_';
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}"
 href="index.cgi?res=$DT{'i'}#art$DT{'i'}-$DT{'j'}">���ε�������å�No.$DT{'i'}���ֿ�����(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_CONFIG_

#-----------------------------
# �����Υեå����ʻҵ���������Ķ���
$CF{'artfoto'}=<<'_CONFIG_';
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}" class="warning"
 href="#res$DT{'i'}">���ε�������å�No.$DT{'i'}�ϻҵ��������¤�ã�����Τ��ֿ��Ǥ��ޤ���(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_CONFIG_
#memo.
#�ֿ��⡼�ɤ��ʤ��Τˡ�href="#res$DT{'i'}"�פȥ�󥯤�ĥ�äƤ���Τϡ�����������������Ѳ�ǽ�ˤ��뤿��

#-----------------------------
# �����Υեå������ֿ��⡼�ɡ�
$CF{'artfotr'}=<<'_CONFIG_';
</DIV>


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
<TR title="subJect\n��������̾�����Ϥ��ޤ�\n�ǹ�����100ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon\n������������򤷤ޤ�" style="text-align:center">
<LABEL accesskey="i" for="icon">�� <A href="index.cgi?icct" title="����������\n��������򳫤��ޤ�" target="_blank">��������</A>��<KBD class="ak">��</KBD>�ˢ�</LABEL>
</TH>
</TR>
<TR title="Name\n̾�������Ϥ��ޤ���ɬ�ܡ�\n�ǹ�����50ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie\n���å�����¸��ON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$CF{'icon'}$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL\n�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme\n��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password\n���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�\n�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
��
<SPAN title="Color\n��ʸ�ο������Ϥ��ޤ�">
<SPAN class="item">
<LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand\n���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�">
<TH class="item">
<LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}">
</TD>
<TD class="input" title="Icon\n������������򤷤ޤ�">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>

<TBODY title="Body\n��������ʸ�����Ϥ��ޤ�\n������10000ʸ���ޤǤǤ�\n���ѤǤ��륿���ϥإ�פ򻲾Ȥ��Ƥ�������">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center"><TEXTAREA name="body" id="body" cols="80" rows="8">$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY><TR title="Submit\n��������Ƥ��ޤ�"><TD colspan="3" class="foot">
<INPUT type="submit" class="submit" accesskey="s" value="��Ƥ���">
<!-- <INPUT type="reset" class="reset" value="�ꥻ�å�"> -->
<INPUT type="button" class="button" accesskey="," value="�����¸," onclick="saveBodyCk()" onkeypress="saveBodyCk()">
<INPUT type="button" class="button" accesskey="." value="�ɤ߹���." onclick="loadBodyCk()" onkeypress="loadBodyCk()">
</TD></TR></TBODY>

</TABLE>
</DIV>

_CONFIG_

#-----------------------------
# �ֿ��ե�����
$CF{'resfm'}=<<'_CONFIG_';
<DIV class="center"><TABLE border="2" cellspacing="0" class="write" summary="ResForm">
<COL span="3">
<THEAD><TR><TH colspan="3" class="caption"><A name="Form"></A>$DT{'caption'}</TH></TR></THEAD>

<TBODY title="Body\n��������ʸ�����Ϥ��ޤ�\n������10000ʸ���ޤǤǤ�\n���ѤǤ��륿���ϥإ�פ򻲾Ȥ��Ƥ�������">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">�� ��ʸ(<SPAN class="ak">B</SPAN>) ��</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center"><TEXTAREA name="body" id="body" cols="80" rows="8"
>$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY>
<TR title="subJect\n��������̾�����Ϥ��ޤ�\n�ǹ�����100ʸ���ޤǤǤ�">
<TH class="item"><LABEL accesskey="j" for="subject">����̾(<SPAN class="ak">J</SPAN>)��</LABEL></TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon\n������������򤷤ޤ�" style="text-align:center">
<LABEL accesskey="i" for="icon">�� <A href="index.cgi?icct" title="����������\n��������򳫤��ޤ�" target="_blank">��������</A>��<KBD class="ak">��</KBD>�ˢ�</LABEL>
</TH>
</TR>
<TR title="Name\n̾�������Ϥ��ޤ���ɬ�ܡ�\n�ǹ�����50ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="n" for="name">��̾��(<SPAN class="ak">N</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie\n���å�����¸��ON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$CF{'icon'}$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL\n�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="l" for="email">��E-mail(<SPAN class="ak">L</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme\n��ʬ�Υ����Ȥ�URL�����Ϥ��ޤ�">
<TH class="item">
<LABEL accesskey="o" for="home">���ۡ���(<SPAN class="ak">O</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password\n���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�\n�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<TH class="item">
<LABEL accesskey="p" for="pass">���ѥ����(<SPAN class="ak">P</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
��
<SPAN title="Color\n��ʸ�ο������Ϥ��ޤ�">
<SPAN class="item">
<LABEL accesskey="c" for="color">����(<SPAN class="ak">C</SPAN>)��</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand\n���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�">
<TH class="item">
<LABEL accesskey="m" for="cmd">�����ޥ��(<SPAN class="ak">M</SPAN>)��</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}">
</TD>
<TD class="input" title="Icon\n������������򤷤ޤ�">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>
<TBODY>
<TR title="Submit\n��������Ƥ��ޤ�"><TD colspan="3" class="foot">
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
	my%DT=('new'=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
	#������줿���Τ餻��
	'del'eq$DT{'Mir12'}&&($DT{'body'}='Mireille: [���ε����Ϻ������ޤ���]');
	#�����ʥ�
	&artnavi(\%DT,'head',($DT{'time'}>$CK{'time'}));
	#�������ܤ�Ĵ���򤷤�
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">��HOME��</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
	#̤�ɵ����˰�
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#���褤����Ϥ���
	eval qq(print<<"_HTML_";\n$CF{'artprt'}\n_HTML_); #OLDSTYLE
	#�Ƶ������ä���夬��
	
}


#-------------------------------------------------
#�ҵ���
sub artchd{
=item ����
\% ����åɤε�������ϥå���Υ�ե����
$	���ε����ξ���
=cut
	#��������������ä�
	my%DT=('new'=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));

	#�������Ƥ�Ȥ��Ϥ������������Ф����㤦��
	#�����ʥ�
	&artnavi(\%DT,($DT{'time'}>$CK{'time'}));
	#�������ܤ�Ĵ���򤷤�
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">��HOME��</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
	#̤�ɵ����˰�
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#���褤����Ϥ���
	eval qq(print<<"_HTML_";\n$CF{'artchd'}\n_HTML_); #OLDSTYLE
	#�ҵ������ä���夬��
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
		eval qq(print<<"_HTML_";\n$CF{'artfotr'}\n_HTML_);
	}else{
		#����ɽ��
		if($CF{'maxChilds'}&&$DT{'j'}>=$CF{'maxChilds'}){
			#�ҵ��������¤�Ķ����
			eval qq(print<<"_HTML_";\n$CF{'artfoto'}\n_HTML_);
		}else{
			#���ε�������å�No.???���ֿ�����(?)
			eval qq(print<<"_HTML_";\n$CF{'artfot'}\n_HTML_);
		}
	}
	#�����ʥ�
	&artnavi(\%DT,'foot');
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
�̾��<IMG src="$CF{'icon'}$DT{'icon'}">�Ȥ��Ƥ���櫓�Ǥ�����
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
	my$time=shift();
	$CF{'timeZone'}||&cfgTimeZone($ENV{'TZ'});
	my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($time+$CF{'timeOffset'});
	#sprintf�������ϡ�Perl�β���򸫤Ƥ�������^^;;
	return sprintf("%4dǯ%02d��%02d��(%s) %02d��%02dʬ%s" #"1970ǯ01��01��(��) 09��00ʬ"����
	,$year+1900,$mon+1,$day,('��','��','��','��','��','��','��')[$wday],$hour,$min,$ENV{'TZ'});
#	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"����
#	,$hour,$min,$sec,$year+1900,$mon+1,$day,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# ��������ꥹ��
#
sub iptico{
=item ����
$ �ǥե���Ȼ���ˤ�������������ե�����̾�����줿�񤭴�����ǽ���ѿ�
;
$ SELECT�������ɲä�����°��
$ ��ĥ���ޥ��
=cut
	my$opt='';
	($_[1])&&($opt=" $_[1]");

=item ʣ����������ꥹ��
$CF{'icls'}�κǽ�ΰ�ʸ����' '��Ⱦ�Ѷ���ˤ��ä����ʣ���ꥹ�ȥ⡼�ɤˤʤ�ޤ�
����Ū�����Ф��ȡ�
��ñ��Ȥߤʤ������
'icon.txt'
'icon1.txt icon2.txt' #"icon1.txt icon2"�Ȥ����ƥ����ȥե�������Ȥߤʤ��ޤ�
'"icon.txt" "exicon.txt"'
��ʣ���Ȥߤʤ������
' "icon.txt" "exicon.txt"'
' "icon.txt" exicon.txt'
' icon.txt exicon.txt'
=cut

	if($CK{'iconlist'}&&('reset'ne$_[2])){
		#����å���Ǥ���$CK{'iconlist'}���֤�
		return$CK{'iconlist'};
	}
	
	#��������ꥹ���ɤ߹���
	my$iconlist='';
	if($CK{'cmd'}=~/\biconlist=nolist(;|$)/o){
	 #`icon=nolist`�ǥ�������ꥹ�Ȥ��ɤ߹��ޤʤ�
	}elsif($CF{'icls'}=~/^ /o){
		#ʣ����������ꥹ���ɤ߹���
		for($CF{'icls'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
			$_||next;
			my$tmp;
			open(RD,"<$_")||die"Can't open multi-iconlist($_).";
			eval{flock(RD,1)};
			read(RD,$tmp,-s$_);
			close(RD);
			$iconlist.=$tmp;
		}
	}else{
		#ñ�쥢������ꥹ���ɤ߹���
		open(RD,"<$CF{'icls'}")||die"Can't open single-iconlist.";
		eval{flock(RD,1)};
		read(RD,$iconlist,-s$CF{'icls'});
		close(RD);
	}

	#���򥢥�����η����SELECT���������
	unless(@_){
	}elsif($CF{'exicon'}&&($CK{'cmd'}=~/\bicon=([^;]*)/o)&&$IC{$1}){
		#�ѥ���ɷ�
		$_[0]=$IC{$1};
		$iconlist.=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}elsif($_[0]and$iconlist=~s/(value=(["'])$_[0]\2)/$1 selected/io){
	}elsif($iconlist=~s/value=(["'])(.+?)\1/value=$1$2$1 selected/io){
		$_[0]=$2;
	}
	
	$CK{'iconlist'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="document.images['Preview'].src='$CF{'icon'}'+this.value;document.images['Preview'].title=this.value;"$opt>
$iconlist</SELECT>
_HTML_
	return$CK{'iconlist'};
}


#-------------------------------------------------
# ���顼�ꥹ���ɤ߹���
#
sub iptcol{
=item ����
$ �ǥե���Ȼ���ˤ�������̾
=cut
	if('input'eq$CF{'colway'}){
		return<<"_HTML_";
<INPUT type="text" name="color" id="color" maxlength="20" style="ime-mode:disabled"
 title="Color\n��ʸ�ο������Ϥ��ޤ�\n��#0f0��#00ff00��rgb(0,255,0)��WebColor(green�Ȥ�)\n�Τɤη����Ǥ�Ȥ��ޤ�"
 value="$_[0]">
_HTML_
	}else{
		my$list=$CF{'colorList'}=~/\S/o?$CF{'colorList'}:<<"_HTML_";#1.2.5�ʲ���index.cgi�Ȥθߴ����Τ���
<OPTION value="#000000" style="color:#000000">��Black</OPTION>
<OPTION value="#696969" style="color:#696969">��DimGray</OPTION>
<OPTION value="#808080" style="color:#808080">��Gray</OPTION>
<OPTION value="#A9A9A9" style="color:#A9A9A9">��DarkGray</OPTION>
<OPTION value="#C0C0C0" style="color:#C0C0C0">��Silver</OPTION>
<OPTION value="#D3D3D3" style="color:#D3D3D3">��LightGrey</OPTION>
<OPTION value="#D8BFD8" style="color:#D8BFD8">��Thistle</OPTION>
<OPTION value="#DCDCDC" style="color:#DCDCDC">��Gainsboro</OPTION>
<OPTION value="#F5F5DC" style="color:#F5F5DC">��Beige</OPTION>
<OPTION value="#F5F5F5" style="color:#F5F5F5">��WhiteSmoke</OPTION>
<OPTION value="#E6E6FA" style="color:#E6E6FA">��Lavender</OPTION>
<OPTION value="#FAF0E6" style="color:#FAF0E6">��Linen</OPTION>
<OPTION value="#FDF5E6" style="color:#FDF5E6">��Oldlace</OPTION>
<OPTION value="#FFE4E1" style="color:#FFE4E1">��Mistyrose</OPTION>
<OPTION value="#F0FFF0" style="color:#F0FFF0">��Honeydew</OPTION>
<OPTION value="#FFF5EE" style="color:#FFF5EE">��Seashell</OPTION>
<OPTION value="#FFF0F5" style="color:#FFF0F5">��LavenderBlush</OPTION>
<OPTION value="#F0F8FF" style="color:#F0F8FF">��AliceBlue</OPTION>
<OPTION value="#F8F8FF" style="color:#F8F8FF">��GhostWhite</OPTION>
<OPTION value="#FFFAF0" style="color:#FFFAF0">��FloralWhite</OPTION>
<OPTION value="#F5FFFA" style="color:#F5FFFA">��Mintcream</OPTION>
<OPTION value="#FFFAFA" style="color:#FFFAFA">��Snow</OPTION>
<OPTION value="#FFFFE0" style="color:#FFFFE0">��LightYellow</OPTION>
<OPTION value="#E0FFFF" style="color:#E0FFFF">��LightCyan</OPTION>
<OPTION value="#FFFFF0" style="color:#FFFFF0">��Ivory</OPTION>
<OPTION value="#F0FFFF" style="color:#F0FFFF">��Azure</OPTION>
<OPTION value="#FFFFFF" style="color:#FFFFFF">��White</OPTION>
<OPTION value="#9370DB" style="color:#9370DB">��MediumPurple</OPTION>
<OPTION value="#6A5ACD" style="color:#6A5ACD">��SlateBlue</OPTION>
<OPTION value="#483D8B" style="color:#483D8B">��DarkSlateBlue</OPTION>
<OPTION value="#7B68EE" style="color:#7B68EE">��MediumSlateBlue</OPTION>
<OPTION value="#BA55D3" style="color:#BA55D3">��MediumOrchid</OPTION>
<OPTION value="#9932CC" style="color:#9932CC">��DarkOrchid</OPTION>
<OPTION value="#8A2BE2" style="color:#8A2BE2">��BlueViolet</OPTION>
<OPTION value="#9400D3" style="color:#9400D3">��DarkViolet</OPTION>
<OPTION value="#4B0082" style="color:#4B0082">��Indigo</OPTION>
<OPTION value="#000080" style="color:#000080">��Navy</OPTION>
<OPTION value="#00008B" style="color:#00008B">��DarkBlue</OPTION>
<OPTION value="#0000CD" style="color:#0000CD">��MediumBlue</OPTION>
<OPTION value="#0000FF" style="color:#0000FF">��Blue</OPTION>
<OPTION value="#191970" style="color:#191970">��MidnightBlue</OPTION>
<OPTION value="#00BFFF" style="color:#00BFFF">��DeepSkyBlue</OPTION>
<OPTION value="#00CED1" style="color:#00CED1">��DarkTurquoise</OPTION>
<OPTION value="#1E90FF" style="color:#1E90FF">��DodgerBlue</OPTION>
<OPTION value="#4169E1" style="color:#4169E1">��RoyalBlue</OPTION>
<OPTION value="#4682B4" style="color:#4682B4">��SteelBlue</OPTION>
<OPTION value="#6495ED" style="color:#6495ED">��CornflowerBlue</OPTION>
<OPTION value="#87CEFA" style="color:#87CEFA">��LightSkyblue</OPTION>
<OPTION value="#5F9EA0" style="color:#5F9EA0">��CadetBlue</OPTION>
<OPTION value="#87CEEB" style="color:#87CEEB">��SkyBlue</OPTION>
<OPTION value="#B0E0E6" style="color:#B0E0E6">��PowderBlue</OPTION>
<OPTION value="#ADD8E6" style="color:#ADD8E6">��LightBlue</OPTION>
<OPTION value="#708090" style="color:#708090">��SlateGray</OPTION>
<OPTION value="#778899" style="color:#778899">��LightSlateGray</OPTION>
<OPTION value="#B0C4DE" style="color:#B0C4DE">��LightSteelBlue</OPTION>
<OPTION value="#008080" style="color:#008080">��Teal</OPTION>
<OPTION value="#008B8B" style="color:#008B8B">��DarkCyan</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Aqua</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Cyan</OPTION>
<OPTION value="#2F4F4F" style="color:#2F4F4F">��DarkSlateGray</OPTION>
<OPTION value="#AFEEEE" style="color:#AFEEEE">��PaleTurquoise</OPTION>
<OPTION value="#7FFFD4" style="color:#7FFFD4">��Aquamarine</OPTION>
<OPTION value="#66CDAA" style="color:#66CDAA">��MediumAquamarine</OPTION>
<OPTION value="#3CB371" style="color:#3CB371">��MediumSeagreen</OPTION>
<OPTION value="#2E8B57" style="color:#2E8B57">��SeaGreen</OPTION>
<OPTION value="#48D1CC" style="color:#48D1CC">��MediumTurquoise</OPTION>
<OPTION value="#40E0D0" style="color:#40E0D0">��Turquoise</OPTION>
<OPTION value="#20B2AA" style="color:#20B2AA">��LightSeagreen</OPTION>
<OPTION value="#00FA9A" style="color:#00FA9A">��MediumSpringGreen</OPTION>
<OPTION value="#00FF7F" style="color:#00FF7F">��SpringGreen</OPTION>
<OPTION value="#006400" style="color:#006400">��DarkGreen</OPTION>
<OPTION value="#008000" style="color:#008000">��Green</OPTION>
<OPTION value="#00FF00" style="color:#00FF00">��Lime</OPTION>
<OPTION value="#32CD32" style="color:#32CD32">��LimeGreen</OPTION>
<OPTION value="#228B22" style="color:#228B22">��ForestGreen</OPTION>
<OPTION value="#90EE90" style="color:#90EE90">��LightGreen</OPTION>
<OPTION value="#98FB98" style="color:#98FB98">��PaleGreen</OPTION>
<OPTION value="#7CFC00" style="color:#7CFC00">��LawnGreen</OPTION>
<OPTION value="#7FFF00" style="color:#7FFF00">��Chartreuse</OPTION>
<OPTION value="#ADFF2F" style="color:#ADFF2F">��GreenYellow</OPTION>
<OPTION value="#9ACD32" style="color:#9ACD32">��YellowGreen</OPTION>
<OPTION value="#6B8E23" style="color:#6B8E23">��Olivedrab</OPTION>
<OPTION value="#556B2F" style="color:#556B2F">��DarkOlivegreen</OPTION>
<OPTION value="#8FBC8B" style="color:#8FBC8B">��DarkSeaGreen</OPTION>
<OPTION value="#808000" style="color:#808000">��Olive</OPTION>
<OPTION value="#FFFF00" style="color:#FFFF00">��Yellow</OPTION>
<OPTION value="#FAFAD2" style="color:#FAFAD2">��LightGoldenrodYellow</OPTION>
<OPTION value="#FAEBD7" style="color:#FAEBD7">��AntiqueWhite</OPTION>
<OPTION value="#FFF8DC" style="color:#FFF8DC">��Cornsilk</OPTION>
<OPTION value="#FFEFD5" style="color:#FFEFD5">��PapayaWhip</OPTION>
<OPTION value="#FFEBCD" style="color:#FFEBCD">��BlanchedAlmond</OPTION>
<OPTION value="#FFFACD" style="color:#FFFACD">��LemonChiffon</OPTION>
<OPTION value="#FFE4C4" style="color:#FFE4C4">��Bisque</OPTION>
<OPTION value="#FFDAB9" style="color:#FFDAB9">��PeachPuff</OPTION>
<OPTION value="#F5DEB3" style="color:#F5DEB3">��Wheat</OPTION>
<OPTION value="#FFE4B5" style="color:#FFE4B5">��Moccasin</OPTION>
<OPTION value="#FFDEAD" style="color:#FFDEAD">��NavajoWhite</OPTION>
<OPTION value="#EEE8AA" style="color:#EEE8AA">��PaleGoldenrod</OPTION>
<OPTION value="#D2B48C" style="color:#D2B48C">��Tan</OPTION>
<OPTION value="#DEB887" style="color:#DEB887">��Burlywood</OPTION>
<OPTION value="#E9967A" style="color:#E9967A">��DarkSalmon</OPTION>
<OPTION value="#FA8072" style="color:#FA8072">��Salmon</OPTION>
<OPTION value="#F0E68C" style="color:#F0E68C">��Khaki</OPTION>
<OPTION value="#FFA07A" style="color:#FFA07A">��LightSalmon</OPTION>
<OPTION value="#BDB76B" style="color:#BDB76B">��DarkKhaki</OPTION>
<OPTION value="#F4A460" style="color:#F4A460">��SandyBrown</OPTION>
<OPTION value="#FF7F50" style="color:#FF7F50">��Coral</OPTION>
<OPTION value="#FF6347" style="color:#FF6347">��Tomato</OPTION>
<OPTION value="#CD853F" style="color:#CD853F">��Peru</OPTION>
<OPTION value="#A0522D" style="color:#A0522D">��Sienna</OPTION>
<OPTION value="#D2691E" style="color:#D2691E">��Chocolate</OPTION>
<OPTION value="#8B4513" style="color:#8B4513">��SaddleBrown</OPTION>
<OPTION value="#DAA520" style="color:#DAA520">��Goldenrod</OPTION>
<OPTION value="#B8860B" style="color:#B8860B">��DarkGoldenrod</OPTION>
<OPTION value="#FFD700" style="color:#FFD700">��Gold</OPTION>
<OPTION value="#FFA500" style="color:#FFA500">��Orange</OPTION>
<OPTION value="#FF8C00" style="color:#FF8C00">��DarkOrange</OPTION>
<OPTION value="#FF4500" style="color:#FF4500">��OrangeRed</OPTION>
<OPTION value="#800000" style="color:#800000">��Maroon</OPTION>
<OPTION value="#8B0000" style="color:#8B0000">��DarkRed</OPTION>
<OPTION value="#FF0000" style="color:#FF0000">��Red</OPTION>
<OPTION value="#B22222" style="color:#B22222">��Firebrick</OPTION>
<OPTION value="#A52A2A" style="color:#A52A2A">��Brown</OPTION>
<OPTION value="#CD5C5C" style="color:#CD5C5C">��IndianRed</OPTION>
<OPTION value="#F08080" style="color:#F08080">��LightCoral</OPTION>
<OPTION value="#BC8F8F" style="color:#BC8F8F">��RosyBrown</OPTION>
<OPTION value="#FF1493" style="color:#FF1493">��DeepPink</OPTION>
<OPTION value="#C71585" style="color:#C71585">��MediumVioletRed</OPTION>
<OPTION value="#DC143C" style="color:#DC143C">��Crimson</OPTION>
<OPTION value="#FF69B4" style="color:#FF69B4">��HotPink</OPTION>
<OPTION value="#DA70D6" style="color:#DA70D6">��Orchid</OPTION>
<OPTION value="#DB7093" style="color:#DB7093">��PaleVioletred</OPTION>
<OPTION value="#FFB6C1" style="color:#FFB6C1">��LightPink</OPTION>
<OPTION value="#FFC0CB" style="color:#FFC0CB">��Pink</OPTION>
<OPTION value="#800080" style="color:#800080">��Purple</OPTION>
<OPTION value="#8B008B" style="color:#8B008B">��DarkMagenta</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Fuchsia</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Magenta</OPTION>
<OPTION value="#EE82EE" style="color:#EE82EE">��Violet</OPTION>
<OPTION value="#DDA0DD" style="color:#DDA0DD">��Plum</OPTION>
_HTML_
		if($_[0]&&$list=~s/(value=(["'])$_[0]\2)/$1 selected="selected"/io){
		}elsif($list=~s/value=(["'])$CF{'colway'}\1/value=$1$CF{'colway'}$1 selected="selected"/io){
			$_[0]=$CF{'colway'};
		}elsif($list=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
			$_[0]=$2;
		}
		return<<"_HTML_";
<SELECT name="color" id="color">
$list</SELECT>
_HTML_
	}
}


#-------------------------------------------------
#�����ʥ�HTML
sub artnavi{
=item ����
$ �����ʥӤΥ⡼��
=cut
	return if defined$CF{'artnavi'}&&!$CF{'artnavi'};

	#Netscape4�ϵ����ʥ�̵��
	if($IN{'hua'}=~/^Mozilla\/4.*(?:;\s*|\()[UI](?:;|\))/){
		$CF{'artnavi'}=0;
		return; #�����ʥӤ���Ϥ��ʤ�
	}
	
	unless($_[0]){
		#�����ʥ�����
		#------------------------------------------------------------------------------------
		#�֥饦��Ƚ��
		my$style='display:none;position:absolute;filter:alpha(opacity=60);';
		unless($IN{'hua'}){
			#guess to be WinIE4-6
		}elsif(index($IN{'hua'},'Opera')>-1){
			#guess to be Opera
			$style='display:block;position:fixed;top:-1000;left:-1000;visibility:visible;/*Opera*/';
		}elsif(index($IN{'hua'},'Mac')>-1&& index($IN{'hua'},'MSIE')>-1){
			#guess to be MacIE5
			#�ɤ���MacIE4�ʤ鵭���ʥӤ�ư���ʤ�
			$style='display:none;position:fixed;/*MacIE*/';
		}elsif(index($IN{'hua'},'Mozilla/5')>-1){
			#guess to be Mozilla/Netscape
			$style='display:none;position:fixed;/*Mozilla*/';
		}else{
			#guess to be WinIE4-6
		}
		#iCab�Ȥ��Ϥɤ��ʤΤ�����
		#WinIE�Ϥϥ��֥֥饦������ڤȤδط���HUA������Ǥ��ʤ� => ����¾�Ϥ��٤�WinIE�Ȥ���
		
		print<<"_HTML_";
<DIV id="naviwind" style="$style">
<TABLE id="navihead" cellspacing="1" summary="ArtNavi Header">
<COL span="2">
<TR>
<TH id="navititl" onmousedown="beginDrag(event,'naviwind')">�������ʥ� - Mireille</TH>
<TD id="navibutt" style="width:35px" onmousedown="beginDrag(event,'naviwind')">
<A accesskey="m" onclick="view(event,'navibody')" onkeypress="acskey(event,'navibody')"
 href="#����/�̾�" title="����/�̾�(&amp;M)">��</A>
<A accesskey="c" onclick="view(event,'naviwind')" onkeypress="acskey(event,'naviwind')"
 href="#�Ĥ���" title="�Ĥ���(&amp;C)">��</A></TD>
</TR>
</TABLE>
<DIV id="navibody" style="display:block">
$CK{'navibody'}</DIV>
</DIV>
<SCRIPT type="text/javascript" src="$CF{'navjs'}" defer></SCRIPT>
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
	
	my%DT=%{shift()};
	if('head'eq$_[0]){
		#�����إå�
		$CK{'navibody'}.=<<"_HTML_";
<DIV class="navithre">
<DIV class="navisubj">
<A href="#nav_r$DT{'i'}" title="�ֿ�"><STRONG>$DT{'i'}</STRONG></A>:
<A href="#art$DT{'i'}">$DT{'subject'}</A>
</DIV>
<DIV class="navinums">
_HTML_
		shift;
	}elsif('foot'eq$_[0]){
		#�����եå�
		$CK{'navibody'}.=<<"_HTML_";
<A href="index.cgi?res=$DT{'i'}#Form" title="�ֿ�" style="color:green;">Re</A>
</DIV>
</DIV>
_HTML_
		return;
	}
	
	#����
	if($_[0]){
		#̤��
		$CK{'navibody'}.=<<"_HTML_";
<A class="new" href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A>
_HTML_
		return;
	}else{
		#����
		$CK{'navibody'}.=<<"_HTML_";
<A href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A>
_HTML_
		return;
	}
}

#require��style.cgi��Revision���֤�
$CF{'Style'}=qq$Revision$;
$CF{'Style'}=~/(\d+(?:\.\d+)*)/o;
$CF{'StyleRevision'}=$1;
__END__
