#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Administrative Tools -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
#require 5.005;
#use strict;
#use vars qw(%AT %CF %IN %IC);
$|=1;


#------------------------------------------------------------------------------#
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
	$_[0]?qq($CF{'home'}">BACK to HOME):qq(manage.cgi?jump=index.cgi">BACK to INDEX)
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
#------------------------------------------------------------------------------#

#����CGI�Υѥ����
$AT{'pass'}='';

#-------------------------------------------------
# Switch

__FILE__=~/\bmanage.cgi$/o&&$ENV{'SERVER_NAME'}&&$ENV{'SERVER_NAME'}ne"localhost"&& die<<"_HTML_";
<STRONG>����¤Υ������ƥ�����ݤ��뤿��ηٹ�</STRONG>
����CGI��ư����Τ˺����ɬ�פʥ������ƥ��ռ��������Ԥ���­���Ƥ��ޤ�
�����������ϰ��̤��ܤ��̤��Ƥ�������
_HTML_

&getParam;
unless($IN{'mode'}){
	&menu('Ready...');
}elsif('icong'eq$IN{'mode'}){
	&icong;
}elsif('icont'eq$IN{'mode'}){
	&icont;
}elsif('icons'eq$IN{'mode'}){
	&icons;
}elsif('iconsmp'eq$IN{'mode'}){
	&iconsmp;
}elsif('config'eq$IN{'mode'}){
	&config;
}elsif('css'eq$IN{'mode'}){
	&css;
}elsif('log'eq$IN{'mode'}){
	&log;
}elsif('zero'eq$IN{'mode'}){
	&zero;
}elsif('manage'eq$IN{'mode'}){
	&manage;
}else{
	&menu('NG');
}
exit;

#-------------------------------------------------
# Get Parameters
sub getParam{
	my$i='';
	my@param;
	#��������
	unless($ENV{'REQUEST_METHOD'}){@param=@ARGV;}
	elsif('POST'eq$ENV{'REQUEST_METHOD'}){read(STDIN,$i,$ENV{'CONTENT_LENGTH'});}
	elsif('GET'eq$ENV{'REQUEST_METHOD'}){$i=$ENV{'QUERY_STRING'};}
	#���Ϥ�Ÿ��
	@param=split(/[&;]/o,$i)if$i;
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
	))x;
	
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/([-\w]+)/o)?"$1":'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		$DT{$i}=$j;
	}
	# Password Check
	$DT{'mode'}||return undef;
	$DT{'pass'}eq$AT{'pass'}||&menu('Password�����פ��ޤ���');
	$IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":'';
	$IN{'mode'}=$1 if($DT{'mode'}=~/(\w+)/o);
	$IN{'phase'}=$1 if($DT{'phase'}=~/(\d+)/o);
	if('icong'eq$DT{'mode'}){
		for(keys%DT){
			$IN{$_}=$DT{$_} if($_=~/^\d+-\w*/o);
		}
		return%IN;
	}elsif('icont'eq$DT{'mode'}){
		$IN{'icon'}=$1 if($DT{'icon'}=~/(.+)/os);
		$IN{'renew'}=1 if($DT{'renew'}=~/(.)/o);
		return%IN;
	}elsif('icons'eq$DT{'mode'}){
		$IN{'icon'}=$1 if($DT{'icon'}=~/(.+)/os);
		$IN{'renew'}=1 if($DT{'renew'}=~/(.)/o);
		return%IN;
	}elsif('iconsmp'eq$DT{'mode'}){
		return%IN;
	}elsif('config'eq$DT{'mode'}){
		while(my($i,$j)=each%DT){
			$IN{"$i"}=$1 if($j=~/(.*)/os);
		}
		return%IN;
	}elsif('css'eq$DT{'mode'}){
		$IN{'css'}=$1 if($DT{'css'}=~/(.+)/os);
		$IN{'file'}=$1 if($DT{'file'}=~/(\w+)/o);
		$IN{'code'}=$1 if($DT{'code'}=~/(\w+)/o);
		return%IN;
	}elsif('log'eq$DT{'mode'}){#LOG
		$IN{'str'}=($DT{'str'}=~/(\d+)/o)?$1:0;
		$IN{'end'}=($DT{'end'}=~/(\d+)/o)?$1:0;
		$IN{'del'}=$1 if($DT{'del'}=~/(\w)/o);
		$IN{'save'}=($DT{'save'}=~/(\d+)/o)?$1:0;
		$IN{'push'}=($DT{'push'}=~/(\d)/o)?"$1":'';
		$IN{'type'}=$1 if($DT{'type'}=~/(\w)/o);
		return%IN;
	}elsif('zero'eq$DT{'mode'}){#Zero
		$IN{'recover'}=1 if($DT{'recover'}=~/(.)/o);
		return%IN;
	}elsif('manage'eq$DT{'mode'}){#Manage
		$IN{'manage'}=$1 if($DT{'manage'}=~/(\w+)/o);
		$IN{'filename'}=$1 if($DT{'filename'}=~/([^\\\/:*?"<>|]+)/o);
		return%IN;
	}
	print"<PRE>something wicked happend!\n";
	print"�����餯�ϥե��륿������ߥ�\n����CGI".__LINE__."���ܤǤΥ��顼";
	exit;
}

#-------------------------------------------------
# Menu
sub menu{
	my$status=@_?shift():'';
	my$pass=defined$IN{'pass'}?$IN{'pass'}:'';
	print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode" style="margin:1em auto">[ $status ]</H2>
<FORM accept-charset="euc-jp" name="menu" method="post" action="$AT{'manage'}">
<FIELDSET style="text-align:left;padding:0.5em;margin:auto;width:15em">
<LEGEND>Mode</LEGEND>
<LABEL accesskey="y" for="icont">
<INPUT name="mode" class="radio" id="icont" type="radio" value="icont">
Icon�ꥹ���Խ��ʥ�����(<SPAN class="ak">Y</SPAN>)</LABEL>
<BR>
<LABEL accesskey="u" for="icons">
<INPUT name="mode" class="radio" id="icons" type="radio" value="icons">
Icon�ꥹ���Խ�(Sharp��(<SPAN class="ak">U</SPAN>)</LABEL>
<BR>
<LABEL accesskey="i" for="iconsmp">
<INPUT name="mode" class="radio" id="iconsmp" type="radio" value="iconsmp" checked>
<SPAN class="ak">I</SPAN>con���ܤ򹹿�</LABEL>
<BR>
<LABEL accesskey="c" for="config">
<INPUT name="mode" class="radio" id="config" type="radio" value="config">
index.cgi�Խ�(<SPAN class="ak">C</SPAN>)</LABEL>
<BR>
<LABEL accesskey="b" for="css">
<INPUT name="mode" class="radio" id="css" type="radio" value="css">
����CSS�Խ�(<SPAN class="ak">B</SPAN>)</LABEL>
<BR>
<LABEL accesskey="l" for="log">
<INPUT name="mode" class="radio" id="log" type="radio" value="log">
<SPAN class="ak">L</SPAN>OG���������</LABEL>
<BR>
<LABEL accesskey="z" for="zero">
<INPUT name="mode" class="radio" id="zero" type="radio" value="zero">
��������ե��������(<SPAN class="ak">Z</SPAN>)</LABEL>
<BR>
<LABEL accesskey="m" for="manage">
<INPUT name="mode" class="radio" id="manage" type="radio" value="manage">
����CGI�δ���(<SPAN class="ak">M</SPAN>)</LABEL>
</FIELDSET>
<P style="margin:0.5em"><LABEL accesskey="p" for="pass"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" id="pass" type="password" size="12" value="$pass"></LABEL></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK">
<INPUT type="reset" class="reset" value="����󥻥�"></P>
ASDF
	exit;
}


#-------------------------------------------------
# ��������ʥ�����
sub icont{
	&loadcfg;
	unless($IN{'icon'}){#��������ꥹ���Խ�
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my$icon;
		read(RD,$icon,-s$CF{'icls'});
		close(RD);
		$icon=~s/\t/\ \ /go;
		$icon=~s/[\x0D\x0A]*$//o;
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">��������ꥹ���Խ��⡼��</H2>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<P><TEXTAREA name="icon" cols="100" rows="15">$icon</TEXTAREA></P>
<P><LABEL accesskey="r" for="renew">���������ܹ���(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icont">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
	exit;
	}else{#��������ꥹ�Ƚ񤭹��� Tag
		study$IN{'icon'};
		$IN{'icon'}=~tr/\n//s;
		$IN{'icon'}=~s/(\n)*$/\n/;

		open(WR,"+>>$CF{'icls'}")||die"Can't write iconlist($CF{'icls'})[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $IN{'icon'};
		close(WR);

		unless($IN{'renew'}){
			&menu('��������ꥹ�Ƚ񤭹��ߴ�λ');
		}else{
			&iconsmp;
			&menu('��������ꥹ�ȡ����ܽ񤭹��ߴ�λ');
		}
	}
	exit;
}

#-------------------------------------------------
# ��������ʡ���
sub icons{
	&loadcfg;
	unless($IN{'icon'}){
		#��������ꥹ��Sharp�Խ�����
		print&getManageHeader.<<"ASDF";
<H2 class="mode">��������ꥹ���Խ��⡼��</H2>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<P><TEXTAREA name="icon" cols="100" rows="15">
ASDF
		
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my@icon=<RD>;
		close(RD);
		
		my$optg=0;
		
		for(@icon){
			
			if($_=~m{^\s*<OPTION .*?\bvalue=(["'])(.+?)\1.*?>([^<]*)(</OPTION>)?$}io){
				if($optg==1){print"\ \ ";}
				elsif($optg==2){print"#\n";$optg=0;}
				print"$2#$3\n";
				next;
			}elsif($_=~m{<OPTGROUP .*\blabel=(["'])(.+?)\1.*>}io){
				($2)||($optg=0);
				$optg=1;
				print"#$2\n";
				next;
			}elsif($_=~m{</OPTGROUP>}io){
				print"#\n";
				$optg=2;
				next;
			}else{
				print"$_";
			}
		}
		
		print<<"ASDF".&getManageFooter;
</TEXTAREA></P>
<P><LABEL accesskey="r" for="renew">���������ܹ���(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icons">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
		exit;
	}else{
		#��������ꥹ�Ƚ񤭹���
#		study$IN{'icon'};
		$IN{'icon'}=~tr/\n//s;
#		$IN{'icon'}=~s/&/&#38;/go;
#		$IN{'icon'}=~s/"/&#34;/go;
#		$IN{'icon'}=~s/'/&#39;/go;
#		$IN{'icon'}=~s/</&#60;/go;
#		$IN{'icon'}=~s/>/&#62;/go;
		my@icon=split("\n","$IN{'icon'}");
		
=icon Sharp
 GroupName
^\s*\#\s*(.*)$
 IconName
^\s*([^#])\s*#\s*(.*)$
=cut
		
		open(WR,"+>>$CF{'icls'}")||die"Can't write iconlist($CF{'icls'})[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		my$optg=0;
		for(@icon){
			if($_=~/^\s*\#\s*(.*)$/o){
				#�������󥰥롼��
				($optg==1)&&(print WR "</OPTGROUP>\n");
				($1)||($optg=0,next);
				print WR qq[<OPTGROUP label="$1">\n];
				$optg=1;
				next;
			}elsif($_=~/^\s*([^#]+(?:#\d+)?)\s*\#\s*(.+)$/o){
				#�����������
				($optg==1)&&(print WR "\ \ ");
				print WR qq[<OPTION value="$1">$2</OPTION>\n];
				next;
			}else{
				print WR "$_\n";
			}
		}
		($optg==1)&&(print WR "</OPTGROUP>\n");
		close(WR);
		
		unless($IN{'renew'}){
			&menu('��������ꥹ�Ƚ񤭹��ߴ�λ');
		}else{
			&iconsmp;
			&menu('��������ꥹ�ȡ����ܽ񤭹��ߴ�λ');
		}
		exit;
	}
}

#-------------------------------------------------
# ���������ܹ���
sub iconsmp{
	&loadcfg;

=item

OPTION
 ^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$
 <TD><IMG $1src="$CF{'icon'}$2" title=\"$1\"$3><BR>$1</TD>

#OPTGOUP
 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 OPTGROUP������ä�

#/OPTGOUP
 {^</OPTGROUP>$}{</TR></TABLE>}
 OPTGROUP���˽Ф�

=cut

	open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
	eval{flock(RD,1)};
	
	my$j=0;
	my@others=();
	$AT{'x'}=6;
	my%CR;
	my@icon=();
	my$table=''; #optgroup��Ĥ򤳤�˰��Ū�˳�Ǽ����
	
	for(<RD>){
		if($_=~m{^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$}io){
			#��������
			if(!$j){
				#others
				push(@others,(@others%$AT{'x'}?'':"</TR>\n<TR>\n")
				.qq(<TD><IMG $1src="$CF{'icon'}$3" title="$5"$4><BR>$5</TD>\n));
				next;
			}
			$table.=qq(<TD><IMG $1src="$CF{'icon'}$3" title="$5"$4><BR>$5</TD>\n);
			if($j<$AT{'x'}){
				#���롼����1-5��
				$j++;
			}else{
				#���롼����6���ܡ�����
				$table.="</TR>\n<TR>\n";
				$j=1;
			}
			next;
		}elsif($_=~m{^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$}io){
			#�������󥰥롼�׻�
			$table=<<"_HTML_";
<TABLE $1cellspacing="0" class="icon" summary="$3"$4>
<CAPTION>$3</CAPTION>
<COL span="$AT{'x'}" width="110">
<TR>
_HTML_
			$j=1;
		}elsif($_=~/OPTGROUP/io){#</OPTGROUP>
			#�������󥰥롼�׽�
			my$copy='';
			if($CR{'VENDOR_LINK'}&&$CR{'COPY1_LINK'}){
				$copy="&#169;$CR{'COPY1_LINK'} &gt;&gt; by$CR{'VENDOR_LINK'}";
			}elsif($CR{'VENDOR_LINK'}){
				$copy="by$CR{'VENDOR_LINK'}";
			}elsif($CR{'COPY1_LINK'}){
				$copy="&#169;$CR{'COPY1_LINK'}";
			}
			$table.=($j>1?"</TR>\n<TR>\n":'').<<"_HTML_";
<TH colspan="$AT{'x'}" class="foot">$copy</TH>
</TR>
</TABLE>

_HTML_
			$j=0;
			push(@icon,$table);
			next;
		}elsif($_=~/<!--\s*%([A-Z0-9]+_)?(VENDOR|COPY1)(_[A-Z0-9]+)?(?:\s+(.*?))?\s*-->/o){

=item

$1: 'BEGIN_','END_'
$2: 'VENDOR','COPY1'
$3: '_NAME','_URL','_LINK'
$4: 

=cut

			if('BEGIN_'eq$1){
				$CR{$2.'_NAME'}='';$CR{$2.'_URL'}='';$CR{$2.'_LINK'}='';
				if($4){$CR{$2.'_NAME'}=$4;}else{next;}
			}elsif('END_'eq$1){
				$CR{$2.'_NAME'}='';$CR{$2.'_URL'}='';$CR{$2.'_LINK'}='';next;
			}elsif($3){
				if('_NAME'eq$3){
					$CR{$2.'_NAME'}=$4;
					($CR{$2.'_LINK'})&&(next);
				}elsif('_URL'eq$3){
					$CR{$2.'_URL'}=$4;
				}elsif('_LINK'eq$3){
					$CR{$2.'_LINK'}=$4;
					next;
				}
			}else{next;}
			if($CR{$2.'_NAME'}&&$CR{$2.'_URL'}){
				$CR{$2.'_LINK'}=qq(<A href="$CR{$2.'_URL'}" title=")
				.(('VENDOR'eq$2)?'�����':'�켡�����').qq(">$CR{$2.'_NAME'}</A>);
			}elsif($CR{$2.'_NAME'}){
				$CR{$2.'_LINK'}=$CR{$2.'_NAME'};
			}
			next;
		}
	}
	close(RD);
	
	($j)&&(print WR "</TR></TABLE>\n");
	
	#����¾�ν���
	if($#others>-1){
		$table=<<"_HTML_";
<TABLE cellspacing="0" class="icon" summary="Others">
<CAPTION>����¾</CAPTION>
<COL span="$AT{'x'}" width="110">
@others
</TR>
</TABLE>

_HTML_
		push(@icon,$table);
	}
	undef$table;
	
	open(WR,'+>>icon.html')||die"Can't write iconsample(icon.html)[$!]";
	eval{flock(WR,2)};
	truncate(WR,0);
	seek(WR,0,0);
	print WR <<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<LINK rel="start" href="$CF{'home'}">
<LINK rel="index" href="index.cgi">
<TITLE>: Mireille Icon List :</TITLE>
</HEAD>
<BODY style="margin-top:1em">
$CF{'pghead'}
$CF{'menu'}
<H2 class="mode">����������</H2>\n$CF{'iched'}
@icon
$CF{'icfot'}
@{[&getPageFooter]}
<DIV class="AiremixCopy">
- <A href="http://www.airemix.com/" target="_top" title="Airemix - Mireille -">Airemix Mireille</A>
<VAR title="times:@{[times]}">$CF{'Manage'}</VAR> -</DIV>
</BODY>
</HTML>
_HTML_
	close(WR);

	&menu("���������ܹ�����λ");
}

#-------------------------------------------------
# index.cgi������
sub config{
my@required=(
 'name'		=>'�����Ȥ�̾��'
,'home'		=>'�����ȥȥåץڡ�����URL'
,'title'	=>'���ηǼ��ĤΥ����ȥ��TITLE���ǡ�'
,'pgtitle'	=>'���ηǼ��ĤΥ����ȥ�ʥڡ����Υإå�����ɽ����'
,'icls'		=>'��������ꥹ��'
,'style'	=>'�������륷����'
,'icon'		=>'��������Υǥ��쥯�ȥ�'
,'icct'		=>'�������󥫥���CGI'
,'help'		=>'�إ�ץե�����'
,'navjs'	=>'�����ʥ�JavaScript'
,'log'		=>'���ǥ��쥯�ȥ�'
,'gzip'		=>'gzip�ξ��'
);
		my@implied=(
 'admps'	=>'�����ԥѥ���ɡ����Ƥε������Խ�������Ǥ��ޤ� 25ʸ���ʾ�侩��'
,'tags'		=>'���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��'
,'strong'	=>'��Ĵ���뵭����б�����CSS�Υ��饹��Ⱦ�ѥ��ڡ������ڤ�ǡֵ��� ���饹 ���桦�����ס�'
,'newnc'	=>'��Ƹ�*****�ð���ε�����New�ޡ�����Ĥ���'
,'newuc'	=>'�ɤ�������Ǥ�???�ô֤ϡ�̤�ɡ׾��֤�ݻ�����'
,'new'		=>'��Ƹ�*****�ð���ε����ˤĤ���New�ޡ���'
,'page'		=>'�̾�⡼�ɤǤ�1�ڡ���������Υ���åɿ�'
,'delpg'	=>'����������⡼�ɤǤ�1�ڡ���������Υ���åɿ�'
,'logmax'	=>'���祹��åɿ�'
,'maxChilds'=>'�쥹��åɤ�����κ���ҵ����������¤���'
,'sekitm'	=>'�����Ǥ�����ܡ�"���ܤ�name �������̾�� "�򤯤꤫������'
,'prtitm'	=>'�Ƶ����ι���(+color +email +home +icon +ra +hua +cmd +subject)'
,'chditm'	=>'�ҵ����ι���(+color +email +home +icon +ra +hua +cmd)'
,'cokitm'	=>'Cookie�ι���(color email home icon cmd)'
,'conenc'	=>'����ž���Τ����(Content-Encoding����ˡ)'
,'ckpath'	=>'Cookie����Ͽ����PATH(path=/ �Ȥ��ä�����)'
);
		my@select=(
 'colway'	=>'����������ˡ','input INPUT���� select SELECT����'
,'delold'	=>'�Ť���������åɤκ����ˡ','gzip GZIP���� rename �ե�����̾�ѹ� unlink �ե�������'
,'delthr'	=>'��������åɤκ����ˡ','gzip GZIP���� rename �ե�����̾�ѹ� unlink �ե�������'
,'sort'		=>'�������¤ӽ�','number ����å��ֹ�� date ���������'
,'prtwrt'	=>'������ƥե������Index��ɽ��','0 ɽ�����ʤ� 1 ɽ������'
,'mailnotify'=>'����/�ֿ� �����ä��Ȥ��˻��ꥢ�ɥ쥹�˥᡼�뤹��','0 �Ȥ�ʤ� 1 �Ȥ�'
,'readOnly'	=>'�Ǽ��Ĥ�������Ѥˤ���','0 �ɤ߽�OK 1 ��������'
,'use304'	=>'�������ʤ��Ȥ��ˡ�304 Not Modified�פ��Ϥ����ݤ�','0 �Ϥ��ʤ� 1 �Ϥ�'
,'useLastModified'=>'��ˡ�Last-Modified�פ��Ϥ����ݤ�','0 �Ϥ��ʤ� 1 �Ϥ�'
);
		my@design=(
 'colorList'=>'���ꥹ��'
,'bodyHead'	=>'HTML-BODY�Υإå����ʥڡ����Ǿ����ΥХʡ�����Ϥ����ˡ�'
,'bodyFoot'	=>'HTML-BODY�Υեå����ʥڡ����ǲ����ΥХʡ�����Ϥ����ˡ�'
,'iched'	=>'�������󥫥����Υإå���'
,'icfot'	=>'�������󥫥����Υեå���'
);
	unless($IN{'name'}){
		my$message='';
		unless(&loadcfg){
			$message=<<'_HTML_';
<H2>index.cgi���ɤ߹��ߤǥ��顼��ȯ�����ޤ���</H2>
<P>index.cgi����»���Ƥ����ǽ��������ޤ�<BR>
���Τޤ޼¹Ԥ���С�config���񤭤������ꤷ�ʤ����ޤ�</P>
_HTML_
		}
		my%config=%CF;
		for(%config){
			$config{"$_"}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
			$config{"$_"}=~s/&/&#38;/go;
			$config{"$_"}=~s/"/&#34;/go;
			$config{"$_"}=~s/'/&#39;/go;
			$config{"$_"}=~s/</&#60;/go;
			$config{"$_"}=~s/>/&#62;/go;
		}
		print&getManageHeader.<<"ASDF";
<H2 class="mode">index.cgi�Խ��⡼��</H2>
$message
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<TABLE style="margin:1em">
<COL style="text-align:left;width:600px"><COL style="text-align:left;width:200px">

<TBODY>
<TR><TH colspan="2"><H3 class="list">��ư���������˳�ǧ���뤳��</H2></TH></TR>
ASDF
		my$i=0;
		#��ư���������˳�ǧ���뤳��
		for($i=0;$i<$#required;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$required[$i+1]��</TH>
<TD><INPUT name="$required[$i]" type="text" style="ime-mode:inactive;width:200px" value="$config{"$required[$i]"}"></TD>
</TR>
ASDF
		}

		print<<"ASDF";
<TR>
<TH class="item">�����ॾ����ʡ�JST-9�פΤ褦�ˡˡ�</TD>
<TD><INPUT name="TZ" type="text" style="ime-mode:disabled" value="$ENV{'TZ'}"></TD>
</TR>
</TBODY>

<TBODY>
<TR><TH colspan="2"><H3 class="list">ɬ�פ˱������ѹ�</H2></TH></TR>
ASDF
		#ɬ�פ˱������ѹ�
		for($i=0;$i<$#implied;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$implied[$i+1]��</TH>
<TD><INPUT name="$implied[$i]" type="text" style="ime-mode:inactive;width:200px" value="$config{"$implied[$i]"}"></TD>
</TR>
ASDF
		}

		#����
		for($i=0;$i<$#select;$i+=3){
			print<<"ASDF";
<TR>
<TH class="item">$select[$i+1]��</TH>
<TD>
<SELECT name="$select[$i]">
ASDF
			my$name=$select[$i+2];
			my@label=split(/ /o,$select[$i+2]);
			for(my$j=0;$j<$#label;$j+=2){
				if($label[$j]eq$config{$select[$i]}){
					print<<"ASDF";
<OPTION value="$label[$j]" selected="selected">$label[$j+1]</OPTION>
ASDF
				}else{
					print<<"ASDF";
<OPTION value="$label[$j]">$label[$j+1]</OPTION>
ASDF
				}
			}
		print<<"ASDF";
</SELECT>
</TD>
</TR>
ASDF
		}
		print<<"ASDF";
</TBODY>

<TBODY>
<TR><TH colspan="2"><H3 class="list">���ѥ�������</H2></TH></TR>
<TR>
<TH class="item">���ѥ�������ǽ��</TD>
ASDF
		$i=<<"ASDF";
<TD>
<LABEL for="exiconon">�Ȥ�<INPUT id="exiconon" name="exicon" type="radio" value="1" checked></LABEL>
<LABEL for="exiconof">�Ȥ�ʤ�<INPUT id="exiconof" name="exicon" type="radio" value="0"></LABEL>
</TD>
</TR>
<TR>
ASDF
		$i=~s/(value=\"$config{'exicon'}\")/$1 checked="checked"/o;
		print$i;
		my@IC=keys%IC;
		for(0..($#IC+5)){
			my$key='';my$val='';
			if($_<=$#IC){
				$key=$IC[$_];
				$val=$IC{$IC[$_]}
			}
			print<<"ASDF";
<TR>
<TH class="item">�ѥ���ɡ�<INPUT name="ICN$_" type="text" style="ime-mode:disabled" value="$key"></TD>
<TD>�ե�����̾��<INPUT name="ICV$_" type="text" style="ime-mode:disabled" value="$val"></TD>
</TR>
ASDF
		}
		print<<"ASDF";
<TR><TH colspan="2"><H3 class="list">Mireille���HTML�ǥ�����</H2></TH></TR>
ASDF
		#Mireille���HTML�ǥ�����
		for($i=0;$i<$#design;$i+=2){
			print<<"ASDF";
<TR><TH class="item" colspan="2">$design[$i+1]��</TH></TR>
<TR><TD colspan="2"><TEXTAREA name="$design[$i]" cols="130" rows="7" style="ime-mode:inactive;width:800px">$config{$design[$i]}</TEXTAREA></TD></TR>
ASDF
		}
		print<<"ASDF".&getManageFooter;
</TABLE>
<P>
<INPUT name="mode" type="hidden" value="config">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
	}else{
		for(keys%IN){
			$IN{"$_"}=~s/(\n)*$//o;
			$IN{"$_"}=~s/'/\\'/go;
			$IN{"$_"}=~s/^_CONFIG_$/(_CONFIG_)/gmo;
		}
		
		open(RD,"<$AT{'manage'}")||die"Can't read manage($AT{'manage'})[$!]";
		eval{flock(RD,1)};
		my$config=<RD>;
		close(RD);

		$config.=<<"ASDF";

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# \$$CF{'Manage'}\$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
#require 5.005;
#use strict;
#use vars qw(\%CF \%IC);
\$|=1;

#-------------------------------------------------
# ��ư���������˳�ǧ���뤳��

ASDF
		my$i=0;
		for($i=0;$i<$#required;$i+=2){
			$config.=<<"ASDF";
#$required[$i+1]
\$CF{\'$required[$i]\'}=\'$IN{"$required[$i]"}\';
ASDF
		}
		$config.=<<"ASDF";
#�����ॾ����ʡ�JST-9�פΤ褦�ˡ�
\$ENV{'TZ'}=\'$IN{'TZ'}\';

#-------------------------------------------------
# ɬ�פ˱������ѹ�

ASDF
		for($i=0;$i<$#implied;$i+=2){
			$config.=<<"ASDF";
#$implied[$i+1]
\$CF{\'$implied[$i]\'}=\'$IN{"$implied[$i]"}\';
ASDF
		}
		for($i=0;$i<$#select;$i+=3){
			$config.=<<"ASDF";
#$select[$i+1] ($select[$i+2])
\$CF{\'$select[$i]\'}=\'$IN{"$select[$i]"}\';
ASDF
		}
		$config.=<<"ASDF";
#�ե�����̾���ꥢ������Υ��ޥ��̾
#\$CF{'exicfi'}='iconfile';
#���ѥ�������ǽ (ON 1 OFF 0)
\$CF{'exicon'}=\'$IN{'exicon'}\';
#���ѥ����������
#\$IC{'PASSWORD'}='FILENAME'; #NAME
#\$IC{'hae'}='mae.png'; #��
#\$IC{'hie'}='mie.png'; #��
#\$IC{'hue'}='mue.png'; #�
#\$IC{'hee'}='mee.png'; #��
#\$IC{'hoe'}='moe.png'; #ǵ��
#�㡧���ޥ�ɤ�"icon=hoe"��������ǵ���������Ѥ�'moe.png'���Ȥ��ޤ�
#�����Ϥ���Ȥ��ϡ�\$IC{'hoe'}='moe.png'; #ǵ���פΤ褦�ˡ��ǽ�Ρ�#�פ���Τ�˺�줺��
ASDF
		for(my$i=0;defined$IN{"ICN$i"};$i++){
			($IN{"ICN$i"}&&$IN{"ICV$i"})||(next);
			$config.=qq{\$IC{\'$IN{"ICN$i"}\'}=\'$IN{"ICV$i"}\';\n};
		}
		$config.=<<"ASDF";

#-------------------------------------------------
# Mireille���HTML�ǥ�����

ASDF
		for($i=0;$i<$#design;$i+=2){
			$config.=<<"ASDF";
#-----------------------------
# $design[$i+1]
\$CF{\'$design[$i]\'}=<<'_CONFIG_';
$IN{$design[$i]}
_CONFIG_

ASDF
		}
		$config.=<<'ASDF';
#-------------------------------------------------
# �¹� or �ɤ߹��ߡ�

if($CF{'program'}eq __FILE__){
	#ľ�ܼ¹Ԥ��ä���ư���Ф�
	require 'core.cgi';
	require 'style.pl';
	&main;
}

#-------------------------------------------------
# �������
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\nX-Moe: Mireille\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		};
	}
	# Version
ASDF
		$config.=q(	$CF{'Index'}=q$)."$CF{'Manage'}".'$;'.<<'ASDF';

	$CF{'Index'}=~/(\d+((?:\.\d+)*))/o;
	$CF{'IndexRevision'}=$1;
}

1;
__END__
ASDF
		open(WR,'+>>index.cgi')||die"Can't write index.cgi[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $config;
		close(WR);
		
		&menu('index.cgi�˽񤭹��ߴ�λ');
	}
	exit;
}

#-------------------------------------------------
# CSS���Խ�
sub css{
	unless($IN{'file'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">�������륷���ȥե���������</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSS�ե�����̾<INPUT name="file" type="text" style="ime-mode:disabled" value="$IN{'file'}">�ʳ�ĥ�Ҥ����Ϥ��ʤ���<BR>
�㡧$CF{'style'}�ʤ顢style�Ȥ������Ϥ���<BR>
������Υ������ƥ����ݤΤ���Ǥ��Τǡ��������餺</P>
<P>
<INPUT name="mode" type="hidden" value="css">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
	}elsif(!$IN{'css'}){
		open(RD,"<$IN{'file'}.css")||die"Can't read css($IN{'file'}.css)[$!]";
		eval{flock(RD,1)};
		my$css=join('',<RD>);
		close(RD);
		
		study$css;
		$css=~/\@charset\s*[\"\']([\-\w]*)[\"\']/io;
		$IN{'code'}=$1;
		($IN{'code'}=~/Shift_JIS/io)&&($css=sjis2euc($css));
		$css=~s/\t/\ \ /go;
		$css=~s/&/&#38;/go;
		$css=~s/"/&#34;/go;
		$css=~s/'/&#39;/go;
		$css=~s/</&#60;/go;
		$css=~s/>/&#62;/go;
		
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">�������륷�����Խ��⡼��</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSS�ե�����̾:$IN{'file'}.css<INPUT name="file" type="hidden" value="$IN{'file'}"><P>
<P><TEXTAREA name="css" cols="100" rows="15">$css</TEXTAREA><P>
<P>
<INPUT name="code" type="hidden" value="$IN{'code'}">
<INPUT name="mode" type="hidden" value="css">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
	}else{
		$IN{'css'}=~s/(\n)*$/\n/o;
		if($IN{'code'}=~/Shift_JIS/i){
			$IN{'css'}=euc2sjis($IN{'css'});
		}
		open(WR,"+>>$IN{'file'}\.css")||die"Can't write css($IN{'file'}.css)[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $IN{'css'};
		close(WR);
		
		&menu('css�񤭹��ߴ�λ');
	}
	exit;
}

#-------------------------------------------------
# ������
sub log{
	unless($IN{'type'}){
		#�����������˥塼
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">�������⡼��</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>�Хå����å׺��</LEGEND>
<LABEL for="back"><INPUT name="type" id="back" type="radio" value="3" accesskey="y" checked="checked"
>�Хå����åץե������������(<SPAN class="ak">Y</SPAN>)</LABEL>
<PRE style="text-align:center">�ե�����̾�ѹ���������������ΤȤ��ˤǤ����Хå����åץե��������ݤ��ޤ�</PRE>
</FIELDSET>

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>��������åɤ���</LEGEND>
<FIELDSET style="padding:0.5em;width:90%">
<LEGEND>�������ե�����λ���</LEGEND>

<P style="text-align:left"><INPUT name="type" type="radio" value="1" accesskey="y"
>����å��ֹ�<INPUT name="str" type="text" size="3" style="ime-mode:disabled" value=""
>����<INPUT name="end" type="text" size="3" style="ime-mode:disabled" value=""
>�ޤǺ������(<SPAN class="ak">Y</SPAN>)<BR>
���΢��˲�������ʤ��ä����ϡ�1������������<BR>
��΢��˲�������ʤ��ä����ϡ�������ǿ���Ĥ��Ƥ������ΤΤ�Τ�������ޤ�<BR>
���ʤ���ʥ��ޥ�ɤǤ⤢��Τǡ�ɬ���¹����˥Хå����åפ�Ȥ�褦�ˤ��ޤ��礦</P>

<P style="text-align:left"><INPUT name="type" type="radio" value="2" accesskey="y"
>�ǿ�����<INPUT name="save" type="text" size="3" style="ime-mode:disabled" value=""
>�ĻĤ��ơ�����ʳ���������(<SPAN class="ak">Y</SPAN>)<BR>
�����Ǥ����ֺǿ��פȤϥ���å��ֹ�κǤ��礭��ʪ���Τ��ȤǤ�<BR>
ɬ���¹����˥Хå����åפ�Ȥ�褦�ˤ��ޤ��礦</P>
</FIELDSET>


<FIELDSET style="padding:0.5em;width:50%">
<LEGEND accesskey="c">�������</LEGEND>
<LABEL for="rename">�ե�����̾�ѹ���<INPUT name="del" id="rename" type="radio" value="rename" checked></LABEL>
<LABEL for="unlink">�ե���������<INPUT name="del" id="unlink" type="radio" value="unlink"></LABEL>
</FIELDSET>

<P><LABEL for="push"><INPUT id="push" name="push" type="checkbox" value="1">����å��ֹ��Ĥ��</LABEL>
<BR>����å��ֹ�򣱤�����֤��ѹ����ޤ�</P>
</FIELDSET>

<P><INPUT name="mode" type="hidden" value="log">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
ASDF
	}elsif($IN{'type'}=~/^\d$/){
		#����������ʳ�
		print&getManageHeader.<<"_HTML_";
<H2 class="mode">�������⡼��</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">
_HTML_
		if($IN{'type'}==1){
			#������������
			if(!$IN{'str'}&&!$IN{'end'}){
				print<<"_HTML_";
<P>���ϥ���å��ֹ�Ƚ�λ����å��ֹ椬�������Ϥ���Ƥ��ޤ���<BR>
��äƻ��ꤷ�ʤ����Ƥ�������</P>
_HTML_
			}else{
				my$delete;
				if($IN{'str'}&&$IN{'end'}){
					$delete="$IN{'str'}����$IN{'end'}�ޤ�";
				}elsif(!$IN{'str'}){
					$delete="�ǽ餫��$IN{'end'}�ޤ�";
				}elsif(!$IN{'end'}){
					$delete="$IN{'str'}����ǿ��ޤ�";
				}
				print<<"_HTML_";
<P>�����ˡ�$delete��@{[('unlink'eq$IN{'del'})?'�ե�������':'�ե�����̾�ѹ�']}�Ǻ�����Ƥ�����Ǥ�����
<INPUT name="str" type="hidden" size="3" value="$IN{'str'}" readonly>
<INPUT name="end" type="hidden" size="3" value="$IN{'end'}" readonly>
<INPUT name="type" type="hidden" value="a">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
_HTML_
			}
		}elsif($IN{'type'}==2){
			#1��(�ǿ�-��)������
			&loadcfg;
			my@file=&logfiles;
			my$i=$#file-$IN{'save'}+1;
			print<<"ASDF";
<P>�����ˡ��ǿ�����<INPUT name="save" type="text" size="3" value="$IN{'save'}" readonly
>�ĻĤ���@{[('unlink'eq$IN{'del'})?'�ե�������':'�ե�����̾�ѹ�']}�Ǻ�����Ƥ�����Ǥ�����<BR>
����å��ֹ�$file[$#file]����$file[$IN{'save'}]�ޤǤΡ�$i��������ޤ�
<INPUT name="type" type="hidden" value="b">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
ASDF
		}elsif($IN{'type'}==3){
				#�Хå����å׺��
				print<<"ASDF";
<P>�����ˡ��Хå����åץե��������ݤ��Ƥ�����Ǥ�����</P>
<INPUT name="type" type="hidden" value="c">
ASDF
		}else{
			exit;
		}
		
		print<<"ASDF".&getManageFooter;
<BR>
<P>
<INPUT name="mode" type="hidden" value="log">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT name="push" type="hidden" value="$IN{'push'}">
���ͤ�: @{[$IN{'push'}?'����':'���ʤ�']}</P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
<P><A href="$AT{'manage'}" title="����">�ְ㤨���ΤǺǽ餫����ľ��</A></P>
ASDF
	}elsif($IN{'type'}=~/^\w$/){
		&loadcfg;
		if('c'eq$IN{'type'}){
			my$file=unlink<$CF{'log'}*.bak>;
			$file.=unlink<$CF{'log'}*.bak.cgi>;
			$file.=unlink<$CF{'log'}*.bak.pl>;
			$file.=unlink<$CF{'log'}*.gz>;
			$file.=unlink<$CF{'log'}*.gz.cgi>;
			$file.=unlink<$CF{'log'}*.bz2.cgi>;
			&menu("$file�ĤΥХå����åץե�����������ޤ���");
		}
		my@file=&logfiles;#(4,3,2,1)
		if($IN{'type'}eq'a'){
			if($IN{'str'}&&$IN{'end'}){
			}elsif(!$IN{'str'}){
				$IN{'str'}=1;
			}elsif(!$IN{'end'}){
				$IN{'end'}=$file[0];
			}
		}elsif($IN{'type'}eq'b'){
			$IN{'str'}=$file[$#file];
			$IN{'end'}=$file[$IN{'save'}];
		}else{
			exit;
		}

		my$file=0;
		if('unlink'eq$IN{'del'}){
			for($IN{'str'}..$IN{'end'}){
				(unlink"$CF{'log'}$_.cgi")||(next);
				$file++;
			}
		}else{
			for($IN{'str'}..$IN{'end'}){
				(rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi"))||(next);
				$file++;
			}
		}
		
		if($IN{'push'}){
			open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
			eval{flock(ZERO,2)};
			truncate(ZERO,0);
			seek(ZERO,0,0);
			my@zero=();
			while(<ZERO>){
				chomp$_;push(@zero,$_);
			}
			my@zer0=split("\t",$zero[0]);
			my@zer1=split(/ /,$zero[1]);
			my@zer2=split(/ /,$zero[2]);
			my@zerC=();
			my$zerD='';
			my$i=1;
			for(@file){
				rename("$CF{'log'}$_.cgi","$CF{'log'}$i.cgi")||die"Can't rename log($_.cgi->$i)[$!]";
				$zerC["$i"]=$zer2["$_"];
				$zerD.="$_=$i;";
				$i++;
			}
			$zerC[0]=0;
			chop$zerD;#�Ǹ��' '���
			
			truncate(ZERO,0);
			seek(ZERO,0,0);
			print ZERO "@zer0\n";
			print ZERO "@zer1\n";
			print ZERO "@zerC\n";
			print ZERO "$zerD\n";#�ե�����̾�ѹ��Υ�
			close(ZERO);
			
			&menu("��$IN{'str'}��$IN{'end'}�Υե�����$file�Ĥ�����λ<BR>���ͤ�����");
		}
		
		&menu("��$IN{'str'}��$IN{'end'}�Υե�����$file�Ĥ�����λ");
	}
	
	exit;
}

#-------------------------------------------------
# 0.cgi�ʵ�����������ե�����ˤβ���
sub zero{
	unless($IN{'recover'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">��������ե���������⡼��</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">
<P>��������ե������ꥫ�Хꤹ��ȡ���¸�ξ���ϼ����ޤ�<BR>
����Ǥ������Ǥ�����
<INPUT name="mode" type="hidden" value="zero">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><LABEL accesskey="r" for="recover">��������
<INPUT name="recover" id="recover" type="checkbox" value="1"></LABEL></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
		exit;
	}else{
		&loadcfg;
		my@file=&logfiles;
		my@zer2=();	
		for(@file){
			$zer2[$_-$file[$#file]]=(stat("$CF{'log'}$_.cgi"))[9];
		}
		unshift(@zer2,$file[$#file]-1);
		
		open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
		eval{flock(ZERO,2)};
		truncate(ZERO,0);
		seek(ZERO,0,0);
		print ZERO <<"ASDF";
Mir12=\t;\ttitle=\t��������ե������������ޤ���;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

@zer2
ASDF
		close(ZERO);
		&menu("��������ե����������λ");
	}
	exit;
}


#-------------------------------------------------
# ����CGI���Τδ���
sub manage{
	unless($IN{'manage'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">����CGI�δ���</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:25em;text-align:left">
<LEGEND accesskey="m">��뤳��(<SPAN class="ak">M</SPAN>)</LEGEND>
<LABEL accesskey="r" for="rename"><INPUT name="manage" type="radio" id="rename" value="rename"
 checked>����CGI�ե�����̾�ѹ�(<SPAN class="ak">R</SPAN>)</LABEL>
<BR>
��
<LABEL accesskey="n" for="filename">�ѹ���Υե�����̾(<SPAN class="ak">N</SPAN>)��
&#34;<INPUT name="filename" type="text" id="filename" value="">.cgi&#34;</LABEL>
<BR>
<LABEL accesskey="u" for="unlink"><INPUT name="manage" type="radio" id="unlink" value="unlink"
>����CGI�ե��������(<SPAN class="ak">U</SPAN>)</LABEL>
</FIELDSET>

<INPUT name="mode" type="hidden" value="manage">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
		exit;
	}else{
		if('rename'eq$IN{'manage'}){
			($IN{'filename'})||(&menu('�ѹ���Υե�����̾�����Ϥ���Ƥ��ޤ���Ǥ���'));
			(rename(__FILE__,"$IN{'filename'}.cgi"))||(die"�ѹ�����\n$!\n�Ǥ��ʤ��Τ��⤷��ʤ�");
			&menu(qq(�ե�����̾��<A href="$IN{'filename'}.cgi">$IN{'filename'}.cgi</A>���ѹ����ޤ���));
		}elsif('unlink'eq$IN{'manage'}){
			(unlink(__FILE__))||(die"�������\n$!\n�Ǥ��ʤ��Τ��⤷��ʤ�");
			&menu("����CGI�������ޤ���");
		}
	}
	exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# mainľ���Υ��֥롼���󷲤����

#-------------------------------------------------
# config�ɤ߹���
#
sub loadcfg{
	require 'index.cgi';
}

#-------------------------------------------------
# ���ե�����̾����μ���
#
sub logfiles{
	$CF{'Index'}||&loadcfg;
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	my@file=sort{$b<=>$a}map{m/^(?!0)(\d+)\.cgi$/o}readdir(DIR);
	closedir(DIR);
	return@file;
}

#-----------------------------
# �إå���������
sub getManageHeader{
	return<<"_HTML_";# Header without G-ZIP etc.
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
$CF{'head'}</HEAD>

<BODY>

<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="Header" width="90%"><TR>
<TH width="100%"><H1 class="head">Mireille Administrative Tools</H1></TH>
<TD nowrap>��������������</TD>
</TR></TABLE></DIV>
_HTML_
}

#-----------------------------
# �եå���������
sub getManageFooter{
	my$AiremixCopy=<<"_HTML_";
<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</A>
<VAR title="times:@{[times]}">$CF{'Manage'}</VAR> -</DIV>
_HTML_
	return&getPageFooter(defined$IN{'read'}).$AiremixCopy
	.$CF{'form_jscript'}."</BODY>\n</HTML>\n";
}


#------------------------------------------------------------------------------#
# jcode.pl: Perl library for Japanese character code conversion
# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
#  ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/
sub sjis2euc{
	my$s=$_[0];
	$s=~s<([\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc]|[\xa1-\xdf])>
	[
		my($c1,$c2)=unpack('CC',$1);
		if(0xa1<=$c1&&$c1<=0xdf){
			$c2=$c1;$c1=0x8e;
		}elsif(0x9f<=$c2){
			$c1=$c1*2-($c1>=0xe0?0xe0:0x60);$c2+=2;
		}else{
			$c1=$c1*2-($c1>=0xe0?0xe1:0x61);$c2+=0x60+($c2<0x7f);
		}
		pack('CC',$c1,$c2);
	]ego;
	return$s;
}

sub euc2sjis{
	my$s=$_[0];
	$s=~s<([\xa1-\xfe]{2}|\x8e[\xa1-\xdf]|\x8f[\xa1-\xfe]{2})>
	[
		my($c1,$c2)=unpack('CC',$1);
		if($c1==0x8e){#SS2
			substr($1,1,1);
		}elsif($c1==0x8f){#SS3
			"\x81\xac";
		}elsif($c1 % 2){
			pack('CC',($c1>>1)+($c1<0xdf?0x31:0x71),$c2-0x60-($c2<0xe0));
		}else{
			pack('CC',($c1>>1)+($c1<0xdf?0x30:0x70),$c2-2);
		}
	]ego;
	return$s;
}

#------------------------------------------------------------------------------#
# BEGIN

BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Manage Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		};
	}
	# Revision Number
	$CF{'Manage'}=q$Revision$;

	__FILE__=~/([^\/\\:]+)$/o;
	$AT{'manage'}=$1;

	#-------------------------------------------------
	# Mireille���HTML�ǥ�����
	$CF{'title'}='Mireille Administrative Tools';
	$CF{'pgtitle'}='Mireille Administrative Tools';
	$CF{'style'}='style.css';
	$CF{'home'}='';
	$CF{'name'}='';
	$CF{'bodyHead'}='';
	$CF{'bodyFoot'}='';
}

1;
__END__
