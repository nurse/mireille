#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Administrative Tools -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
#require 5.005;
#use strict;
#use vars qw(%AT %CF %IN %IC);
$|=1;


#------------------------------------------------------------------------------#
#-------------------------------------------------
# Mireille内のHTMLデザイン

#-----------------------------
# MireileのHEADタグの中身
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
<TD class="menu"><A href="index.cgi?new#Form">新規投稿</A></TD>
<TD class="menu"><A href="index.cgi">更新</A></TD>
<TD class="menu"><A href="index.cgi?rvs">修正</A></TD>
<TD class="menu"><A href="index.cgi?del">削除</A></TD>
<TD class="menu"><A href="index.cgi?icct">アイコン</A></TD>
<TD class="menu"><A href="index.cgi?seek">検索</A></TD>
<TD class="menu"><A href="index.cgi?help">ヘルプ</A></TD>
<TD class="menu"><A href="$CF{'home'}" title="$CF{'name'}">ホーム</A></TD>
</TR></TABLE>
_CONFIG_

#-----------------------------
# Page Header
$CF{'pghead'}=<<"_CONFIG_";
<TABLE align="center" border="0" cellspacing="0" class="head" summary="PageHeader" width="90%"><TR>
<TH width="100%"><H1 class="head" align="left">$CF{'pgtitle'}</H1></TH>
<TD nowrap>■■■■■■■</TD>
</TR></TABLE>
_CONFIG_

#-----------------------------
# Page Footer
sub getPageFooter{
	return<<"_HTML_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageFooter" width="90%"><TR>
<TD nowrap>■■■■■■■</TD>
<TH width="100%"><H1 class="head" align="right"><A href="@{[
	$_[0]?qq($CF{'home'}">BACK to HOME):qq(manage.cgi?jump=index.cgi">BACK to INDEX)
]}</A></H1></TH>
</TR></TABLE></DIV>
_HTML_
}
$CF{'pgfoot'}=&getPageFooter;

#-----------------------------
# フォーム用JavaScript
$CF{'form_jscript'}=<<'_CONFIG_';
<SCRIPT type="text/javascript" defer>
<!--
// Save/Load BodyData from Cookie
function saveBodyCk(){
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	if(confirm("新しい本文を保存すると、古い本文データは消えてしまいます\nそれでも保存しちゃってよいですか？")){
		var backup='';
		if(document.cookie.match(/(^|; )MirBody=([^;]+)/))backup=unescape(RegExp.$2);
		if(bodyObj.value.length){
			document.cookie='MirBody='+escape(bodyObj.value)+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';
		}else{
			document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
			alert('一時保存されていた本文データを削除しましたょ');
			return;
		}
		if(!document.cookie.match(/(^|; )MirBody=([^;]+)/)){
			//3850byte程度でサイズ制限がかかる。
			document.cookie='MirBody='+backup+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//終わりの日
			alert("save失敗\nサイズオーバーかも。");
			return false;
		}
		alert("今の本文データを一時保存しましたょ\nあくまで“一時保存”だから過信しないでねっ");
	}
}
function loadBodyCk(){
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	if(!confirm('Cookieから本文データをロードしますよ？？'))return;
	if(!document.cookie.match(/(^|; )MirBody=([^;]+)/)){
		alert('load失敗');
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
# フッターの生成
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

#管理CGIのパスワード
$AT{'pass'}='';

#-------------------------------------------------
# Switch

__FILE__=~/\bmanage.cgi$/o&&$ENV{'SERVER_NAME'}&&$ENV{'SERVER_NAME'}ne"localhost"&& die<<"_HTML_";
<STRONG>最低限のセキュリティを確保するための警告</STRONG>
管理CGIを起動するのに最低限必要なセキュリティ意識が管理者に不足しています
せめて説明書は一通り目を通してください
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
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){@param=@ARGV;}
	elsif('POST'eq$ENV{'REQUEST_METHOD'}){read(STDIN,$i,$ENV{'CONTENT_LENGTH'});}
	elsif('GET'eq$ENV{'REQUEST_METHOD'}){$i=$ENV{'QUERY_STRING'};}
	#入力を展開
	@param=split(/[&;]/o,$i)if$i;
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
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
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		$DT{$i}=$j;
	}
	# Password Check
	$DT{'mode'}||return undef;
	$DT{'pass'}eq$AT{'pass'}||&menu('Passwordが一致しません');
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
	print"おそらくはフィルタの設定ミス\n管理CGI".__LINE__."行目でのエラー";
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
Iconリスト編集（タグ）(<SPAN class="ak">Y</SPAN>)</LABEL>
<BR>
<LABEL accesskey="u" for="icons">
<INPUT name="mode" class="radio" id="icons" type="radio" value="icons">
Iconリスト編集(Sharp）(<SPAN class="ak">U</SPAN>)</LABEL>
<BR>
<LABEL accesskey="i" for="iconsmp">
<INPUT name="mode" class="radio" id="iconsmp" type="radio" value="iconsmp" checked>
<SPAN class="ak">I</SPAN>con見本を更新</LABEL>
<BR>
<LABEL accesskey="c" for="config">
<INPUT name="mode" class="radio" id="config" type="radio" value="config">
index.cgi編集(<SPAN class="ak">C</SPAN>)</LABEL>
<BR>
<LABEL accesskey="b" for="css">
<INPUT name="mode" class="radio" id="css" type="radio" value="css">
外部CSS編集(<SPAN class="ak">B</SPAN>)</LABEL>
<BR>
<LABEL accesskey="l" for="log">
<INPUT name="mode" class="radio" id="log" type="radio" value="log">
<SPAN class="ak">L</SPAN>OG管理・削除</LABEL>
<BR>
<LABEL accesskey="z" for="zero">
<INPUT name="mode" class="radio" id="zero" type="radio" value="zero">
記事情報ファイル回復(<SPAN class="ak">Z</SPAN>)</LABEL>
<BR>
<LABEL accesskey="m" for="manage">
<INPUT name="mode" class="radio" id="manage" type="radio" value="manage">
管理CGIの管理(<SPAN class="ak">M</SPAN>)</LABEL>
</FIELDSET>
<P style="margin:0.5em"><LABEL accesskey="p" for="pass"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" id="pass" type="password" size="12" value="$pass"></LABEL></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK">
<INPUT type="reset" class="reset" value="キャンセル"></P>
ASDF
	exit;
}


#-------------------------------------------------
# アイコン（タグ）
sub icont{
	&loadcfg;
	unless($IN{'icon'}){#アイコンリスト編集
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my$icon;
		read(RD,$icon,-s$CF{'icls'});
		close(RD);
		$icon=~s/\t/\ \ /go;
		$icon=~s/[\x0D\x0A]*$//o;
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">アイコンリスト編集モード</H2>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<P><TEXTAREA name="icon" cols="100" rows="15">$icon</TEXTAREA></P>
<P><LABEL accesskey="r" for="renew">アイコン見本更新(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icont">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
	exit;
	}else{#アイコンリスト書き込み Tag
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
			&menu('アイコンリスト書き込み完了');
		}else{
			&iconsmp;
			&menu('アイコンリスト・見本書き込み完了');
		}
	}
	exit;
}

#-------------------------------------------------
# アイコン（＃）
sub icons{
	&loadcfg;
	unless($IN{'icon'}){
		#アイコンリストSharp編集画面
		print&getManageHeader.<<"ASDF";
<H2 class="mode">アイコンリスト編集モード</H2>
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
<P><LABEL accesskey="r" for="renew">アイコン見本更新(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icons">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
		exit;
	}else{
		#アイコンリスト書き込み
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
				#アイコングループ
				($optg==1)&&(print WR "</OPTGROUP>\n");
				($1)||($optg=0,next);
				print WR qq[<OPTGROUP label="$1">\n];
				$optg=1;
				next;
			}elsif($_=~/^\s*([^#]+(?:#\d+)?)\s*\#\s*(.+)$/o){
				#アイコン項目
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
			&menu('アイコンリスト書き込み完了');
		}else{
			&iconsmp;
			&menu('アイコンリスト・見本書き込み完了');
		}
		exit;
	}
}

#-------------------------------------------------
# アイコン見本更新
sub iconsmp{
	&loadcfg;

=item

OPTION
 ^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$
 <TD><IMG $1src="$CF{'icon'}$2" title=\"$1\"$3><BR>$1</TD>

#OPTGOUP
 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 OPTGROUP内に入った

#/OPTGOUP
 {^</OPTGROUP>$}{</TR></TABLE>}
 OPTGROUP外に出た

=cut

	open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
	eval{flock(RD,1)};
	
	my$j=0;
	my@others=();
	$AT{'x'}=6;
	my%CR;
	my@icon=();
	my$table=''; #optgroup一つをこれに一時的に格納する
	
	for(<RD>){
		if($_=~m{^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$}io){
			#アイコン
			if(!$j){
				#others
				push(@others,(@others%$AT{'x'}?'':"</TR>\n<TR>\n")
				.qq(<TD><IMG $1src="$CF{'icon'}$3" title="$5"$4><BR>$5</TD>\n));
				next;
			}
			$table.=qq(<TD><IMG $1src="$CF{'icon'}$3" title="$5"$4><BR>$5</TD>\n);
			if($j<$AT{'x'}){
				#グループ内1-5桁
				$j++;
			}else{
				#グループ内6桁目：改行
				$table.="</TR>\n<TR>\n";
				$j=1;
			}
			next;
		}elsif($_=~m{^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$}io){
			#アイコングループ始
			$table=<<"_HTML_";
<TABLE $1cellspacing="0" class="icon" summary="$3"$4>
<CAPTION>$3</CAPTION>
<COL span="$AT{'x'}" width="110">
<TR>
_HTML_
			$j=1;
		}elsif($_=~/OPTGROUP/io){#</OPTGROUP>
			#アイコングループ終
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
				.(('VENDOR'eq$2)?'製作者':'一次著作権者').qq(">$CR{$2.'_NAME'}</A>);
			}elsif($CR{$2.'_NAME'}){
				$CR{$2.'_LINK'}=$CR{$2.'_NAME'};
			}
			next;
		}
	}
	close(RD);
	
	($j)&&(print WR "</TR></TABLE>\n");
	
	#その他の処理
	if($#others>-1){
		$table=<<"_HTML_";
<TABLE cellspacing="0" class="icon" summary="Others">
<CAPTION>その他</CAPTION>
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
<H2 class="mode">アイコン見本</H2>\n$CF{'iched'}
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

	&menu("アイコン見本更新完了");
}

#-------------------------------------------------
# index.cgiの設定
sub config{
my@required=(
 'name'		=>'サイトの名前'
,'home'		=>'サイトトップページのURL'
,'title'	=>'この掲示板のタイトル（TITLE要素）'
,'pgtitle'	=>'この掲示板のタイトル（ページのヘッダーで表示）'
,'icls'		=>'アイコンリスト'
,'style'	=>'スタイルシート'
,'icon'		=>'アイコンのディレクトリ'
,'icct'		=>'アイコンカタログCGI'
,'help'		=>'ヘルプファイル'
,'navjs'	=>'記事ナビJavaScript'
,'log'		=>'ログディレクトリ'
,'gzip'		=>'gzipの場所'
);
		my@implied=(
 'admps'	=>'管理者パスワード（全ての記事を編集・削除できます 25文字以上推奨）'
,'tags'		=>'使用を許可するタグ（半角スペース区切り）'
,'strong'	=>'強調する記号と対応するCSSのクラス（半角スペース区切りで「記号 クラス 記号・・・」）'
,'newnc'	=>'投稿後*****秒以内の記事にNewマークをつける'
,'newuc'	=>'読んだ記事でも???秒間は「未読」状態を維持する'
,'new'		=>'投稿後*****秒以内の記事につけるNewマーク'
,'page'		=>'通常モードでの1ページあたりのスレッド数'
,'delpg'	=>'削除・修正モードでの1ページあたりのスレッド数'
,'logmax'	=>'最大スレッド数'
,'maxChilds'=>'一スレッドあたりの最大子記事数を制限する'
,'sekitm'	=>'検索できる項目（"項目のname 選択字の名前 "をくりかえす）'
,'prtitm'	=>'親記事の項目(+color +email +home +icon +ra +hua +cmd +subject)'
,'chditm'	=>'子記事の項目(+color +email +home +icon +ra +hua +cmd)'
,'cokitm'	=>'Cookieの項目(color email home icon cmd)'
,'conenc'	=>'圧縮転送のやり方(Content-Encodingの方法)'
,'ckpath'	=>'Cookieを登録するPATH(path=/ といった形で)'
);
		my@select=(
 'colway'	=>'色の選択方法','input INPUTタグ select SELECTタグ'
,'delold'	=>'古い記事スレッドの削除方法','gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除'
,'delthr'	=>'記事スレッドの削除方法','gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除'
,'sort'		=>'記事の並び順','number スレッド番号順 date 投稿日時順'
,'prtwrt'	=>'新規投稿フォームをIndexに表示','0 表示しない 1 表示する'
,'mailnotify'=>'新規/返信 があったときに指定アドレスにメールする','0 使わない 1 使う'
,'readOnly'	=>'掲示板を閲覧専用にする','0 読み書きOK 1 閲覧専用'
,'use304'	=>'更新がないときに「304 Not Modified」を渡すか否か','0 渡さない 1 渡す'
,'useLastModified'=>'常に「Last-Modified」を渡すか否か','0 渡さない 1 渡す'
);
		my@design=(
 'colorList'=>'色リスト'
,'bodyHead'	=>'HTML-BODYのヘッダー（ページ最上部のバナー広告はここに）'
,'bodyFoot'	=>'HTML-BODYのフッター（ページ最下部のバナー広告はここに）'
,'iched'	=>'アイコンカタログのヘッダー'
,'icfot'	=>'アイコンカタログのフッター'
);
	unless($IN{'name'}){
		my$message='';
		unless(&loadcfg){
			$message=<<'_HTML_';
<H2>index.cgiの読み込みでエラーが発生しました</H2>
<P>index.cgiが破損している可能性があります<BR>
このまま実行すれば、configを上書きして設定しなおせます</P>
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
<H2 class="mode">index.cgi編集モード</H2>
$message
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<TABLE style="margin:1em">
<COL style="text-align:left;width:600px"><COL style="text-align:left;width:200px">

<TBODY>
<TR><TH colspan="2"><H3 class="list">稼動させる前に確認すること</H2></TH></TR>
ASDF
		my$i=0;
		#稼動させる前に確認すること
		for($i=0;$i<$#required;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$required[$i+1]：</TH>
<TD><INPUT name="$required[$i]" type="text" style="ime-mode:inactive;width:200px" value="$config{"$required[$i]"}"></TD>
</TR>
ASDF
		}

		print<<"ASDF";
<TR>
<TH class="item">タイムゾーン（「JST-9」のように）：</TD>
<TD><INPUT name="TZ" type="text" style="ime-mode:disabled" value="$ENV{'TZ'}"></TD>
</TR>
</TBODY>

<TBODY>
<TR><TH colspan="2"><H3 class="list">必要に応じて変更</H2></TH></TR>
ASDF
		#必要に応じて変更
		for($i=0;$i<$#implied;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$implied[$i+1]：</TH>
<TD><INPUT name="$implied[$i]" type="text" style="ime-mode:inactive;width:200px" value="$config{"$implied[$i]"}"></TD>
</TR>
ASDF
		}

		#選択型
		for($i=0;$i<$#select;$i+=3){
			print<<"ASDF";
<TR>
<TH class="item">$select[$i+1]：</TH>
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
<TR><TH colspan="2"><H3 class="list">専用アイコン</H2></TH></TR>
<TR>
<TH class="item">専用アイコン機能：</TD>
ASDF
		$i=<<"ASDF";
<TD>
<LABEL for="exiconon">使う<INPUT id="exiconon" name="exicon" type="radio" value="1" checked></LABEL>
<LABEL for="exiconof">使わない<INPUT id="exiconof" name="exicon" type="radio" value="0"></LABEL>
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
<TH class="item">パスワード：<INPUT name="ICN$_" type="text" style="ime-mode:disabled" value="$key"></TD>
<TD>ファイル名：<INPUT name="ICV$_" type="text" style="ime-mode:disabled" value="$val"></TD>
</TR>
ASDF
		}
		print<<"ASDF";
<TR><TH colspan="2"><H3 class="list">Mireille内のHTMLデザイン</H2></TH></TR>
ASDF
		#Mireille内のHTMLデザイン
		for($i=0;$i<$#design;$i+=2){
			print<<"ASDF";
<TR><TH class="item" colspan="2">$design[$i+1]：</TH></TR>
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
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
#require 5.005;
#use strict;
#use vars qw(\%CF \%IC);
\$|=1;

#-------------------------------------------------
# 稼動させる前に確認すること

ASDF
		my$i=0;
		for($i=0;$i<$#required;$i+=2){
			$config.=<<"ASDF";
#$required[$i+1]
\$CF{\'$required[$i]\'}=\'$IN{"$required[$i]"}\';
ASDF
		}
		$config.=<<"ASDF";
#タイムゾーン（「JST-9」のように）
\$ENV{'TZ'}=\'$IN{'TZ'}\';

#-------------------------------------------------
# 必要に応じて変更

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
#ファイル名指定アイコンのコマンド名
#\$CF{'exicfi'}='iconfile';
#専用アイコン機能 (ON 1 OFF 0)
\$CF{'exicon'}=\'$IN{'exicon'}\';
#専用アイコン列挙
#\$IC{'PASSWORD'}='FILENAME'; #NAME
#\$IC{'hae'}='mae.png'; #苗
#\$IC{'hie'}='mie.png'; #贄
#\$IC{'hue'}='mue.png'; #鵺
#\$IC{'hee'}='mee.png'; #姐
#\$IC{'hoe'}='moe.png'; #乃絵
#例：コマンドに"icon=hoe"と入れると乃絵さん専用の'moe.png'が使えます
#手入力するときは「\$IC{'hoe'}='moe.png'; #乃絵」のように、最初の「#」を取るのを忘れずに
ASDF
		for(my$i=0;defined$IN{"ICN$i"};$i++){
			($IN{"ICN$i"}&&$IN{"ICV$i"})||(next);
			$config.=qq{\$IC{\'$IN{"ICN$i"}\'}=\'$IN{"ICV$i"}\';\n};
		}
		$config.=<<"ASDF";

#-------------------------------------------------
# Mireille内のHTMLデザイン

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
# 実行 or 読み込み？

if($CF{'program'}eq __FILE__){
	#直接実行だったら動き出す
	require 'core.cgi';
	require 'style.pl';
	&main;
}

#-------------------------------------------------
# 初期設定
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
		
		&menu('index.cgiに書き込み完了');
	}
	exit;
}

#-------------------------------------------------
# CSSの編集
sub css{
	unless($IN{'file'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">スタイルシートファイル選択</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSSファイル名<INPUT name="file" type="text" style="ime-mode:disabled" value="$IN{'file'}">（拡張子は入力しない）<BR>
例：$CF{'style'}なら、styleとだけ入力する<BR>
万が一のセキュリティ確保のためですので、あしからず</P>
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
<H2 class="mode">スタイルシート編集モード</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSSファイル名:$IN{'file'}.css<INPUT name="file" type="hidden" value="$IN{'file'}"><P>
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
		
		&menu('css書き込み完了');
	}
	exit;
}

#-------------------------------------------------
# ログ管理
sub log{
	unless($IN{'type'}){
		#ログ管理初期メニュー
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">ログ管理モード</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>バックアップ削除</LEGEND>
<LABEL for="back"><INPUT name="type" id="back" type="radio" value="3" accesskey="y" checked="checked"
>バックアップファイルを削除する(<SPAN class="ak">Y</SPAN>)</LABEL>
<PRE style="text-align:center">ファイル名変更型削除やログの増大のときにできたバックアップファイルを一掃します</PRE>
</FIELDSET>

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>記事スレッドを削除</LEGEND>
<FIELDSET style="padding:0.5em;width:90%">
<LEGEND>削除するファイルの指定</LEGEND>

<P style="text-align:left"><INPUT name="type" type="radio" value="1" accesskey="y"
>スレッド番号<INPUT name="str" type="text" size="3" style="ime-mode:disabled" value=""
>から<INPUT name="end" type="text" size="3" style="ime-mode:disabled" value=""
>まで削除する(<SPAN class="ak">Y</SPAN>)<BR>
前の□に何も入れなかった場合は、1〜□を削除し、<BR>
後の□に何も入れなかった場合は、□から最新を残してそれより昔のものをを削除します<BR>
かなり危険なコマンドでもあるので、必ず実行前にバックアップをとるようにしましょう</P>

<P style="text-align:left"><INPUT name="type" type="radio" value="2" accesskey="y"
>最新から<INPUT name="save" type="text" size="3" style="ime-mode:disabled" value=""
>個残して、それ以外を削除する(<SPAN class="ak">Y</SPAN>)<BR>
ここでいう「最新」とはスレッド番号の最も大きい物、のことです<BR>
必ず実行前にバックアップをとるようにしましょう</P>
</FIELDSET>


<FIELDSET style="padding:0.5em;width:50%">
<LEGEND accesskey="c">削除方式</LEGEND>
<LABEL for="rename">ファイル名変更：<INPUT name="del" id="rename" type="radio" value="rename" checked></LABEL>
<LABEL for="unlink">ファイル削除：<INPUT name="del" id="unlink" type="radio" value="unlink"></LABEL>
</FIELDSET>

<P><LABEL for="push"><INPUT id="push" name="push" type="checkbox" value="1">スレッド番号をつめる</LABEL>
<BR>スレッド番号を１から順番に変更します</P>
</FIELDSET>

<P><INPUT name="mode" type="hidden" value="log">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
ASDF
	}elsif($IN{'type'}=~/^\d$/){
		#ログ管理第一段階
		print&getManageHeader.<<"_HTML_";
<H2 class="mode">ログ管理モード</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">
_HTML_
		if($IN{'type'}==1){
			#□〜□型指定
			if(!$IN{'str'}&&!$IN{'end'}){
				print<<"_HTML_";
<P>開始スレッド番号と終了スレッド番号が共に入力されていません<BR>
戻って指定しなおしてください</P>
_HTML_
			}else{
				my$delete;
				if($IN{'str'}&&$IN{'end'}){
					$delete="$IN{'str'}から$IN{'end'}まで";
				}elsif(!$IN{'str'}){
					$delete="最初から$IN{'end'}まで";
				}elsif(!$IN{'end'}){
					$delete="$IN{'str'}から最新まで";
				}
				print<<"_HTML_";
<P>本当に、$deleteを@{[('unlink'eq$IN{'del'})?'ファイル削除':'ファイル名変更']}で削除してよろしいですか？
<INPUT name="str" type="hidden" size="3" value="$IN{'str'}" readonly>
<INPUT name="end" type="hidden" size="3" value="$IN{'end'}" readonly>
<INPUT name="type" type="hidden" value="a">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
_HTML_
			}
		}elsif($IN{'type'}==2){
			#1〜(最新-□)型指定
			&loadcfg;
			my@file=&logfiles;
			my$i=$#file-$IN{'save'}+1;
			print<<"ASDF";
<P>本当に、最新から<INPUT name="save" type="text" size="3" value="$IN{'save'}" readonly
>個残して@{[('unlink'eq$IN{'del'})?'ファイル削除':'ファイル名変更']}で削除してよろしいですか？<BR>
スレッド番号$file[$#file]から$file[$IN{'save'}]までの、$i件を削除します
<INPUT name="type" type="hidden" value="b">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
ASDF
		}elsif($IN{'type'}==3){
				#バックアップ削除
				print<<"ASDF";
<P>本当に、バックアップファイルを一掃してよろしいですか？</P>
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
ログ詰め: @{[$IN{'push'}?'する':'しない']}</P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
<P><A href="$AT{'manage'}" title="管理">間違えたので最初からやり直す</A></P>
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
			&menu("$file個のバックアップファイルを削除しました");
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
			chop$zerD;#最後の' '削り
			
			truncate(ZERO,0);
			seek(ZERO,0,0);
			print ZERO "@zer0\n";
			print ZERO "@zer1\n";
			print ZERO "@zerC\n";
			print ZERO "$zerD\n";#ファイル名変更のログ
			close(ZERO);
			
			&menu("ログ$IN{'str'}〜$IN{'end'}のファイル$file個を削除完了<BR>ログ詰め成功");
		}
		
		&menu("ログ$IN{'str'}〜$IN{'end'}のファイル$file個を削除完了");
	}
	
	exit;
}

#-------------------------------------------------
# 0.cgi（記事情報管理ファイル）の回復
sub zero{
	unless($IN{'recover'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">記事情報ファイル回復モード</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">
<P>記事情報ファイルをリカバリすると、既存の情報は失われます<BR>
それでもよろしいですか？
<INPUT name="mode" type="hidden" value="zero">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><LABEL accesskey="r" for="recover">回復する
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
Mir12=\t;\ttitle=\t記事情報ファイルを回復しました;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

@zer2
ASDF
		close(ZERO);
		&menu("記事情報ファイル回復完了");
	}
	exit;
}


#-------------------------------------------------
# 管理CGI自体の管理
sub manage{
	unless($IN{'manage'}){
		print&getManageHeader.<<"ASDF".&getManageFooter;
<H2 class="mode">管理CGIの管理</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:25em;text-align:left">
<LEGEND accesskey="m">やること(<SPAN class="ak">M</SPAN>)</LEGEND>
<LABEL accesskey="r" for="rename"><INPUT name="manage" type="radio" id="rename" value="rename"
 checked>管理CGIファイル名変更(<SPAN class="ak">R</SPAN>)</LABEL>
<BR>
　
<LABEL accesskey="n" for="filename">変更後のファイル名(<SPAN class="ak">N</SPAN>)：
&#34;<INPUT name="filename" type="text" id="filename" value="">.cgi&#34;</LABEL>
<BR>
<LABEL accesskey="u" for="unlink"><INPUT name="manage" type="radio" id="unlink" value="unlink"
>管理CGIファイルを削除(<SPAN class="ak">U</SPAN>)</LABEL>
</FIELDSET>

<INPUT name="mode" type="hidden" value="manage">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
ASDF
		exit;
	}else{
		if('rename'eq$IN{'manage'}){
			($IN{'filename'})||(&menu('変更後のファイル名が入力されていませんでした'));
			(rename(__FILE__,"$IN{'filename'}.cgi"))||(die"変更失敗\n$!\nできないのかもしれない");
			&menu(qq(ファイル名を<A href="$IN{'filename'}.cgi">$IN{'filename'}.cgi</A>に変更しました));
		}elsif('unlink'eq$IN{'manage'}){
			(unlink(__FILE__))||(die"削除失敗\n$!\nできないのかもしれない");
			&menu("管理CGIを削除しました");
		}
	}
	exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# main直下のサブルーチン群の補助

#-------------------------------------------------
# config読み込み
#
sub loadcfg{
	require 'index.cgi';
}

#-------------------------------------------------
# ログファイル名配列の取得
#
sub logfiles{
	$CF{'Index'}||&loadcfg;
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	my@file=sort{$b<=>$a}map{m/^(?!0)(\d+)\.cgi$/o}readdir(DIR);
	closedir(DIR);
	return@file;
}

#-----------------------------
# ヘッダーの生成
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
<TD nowrap>■■■■■■■</TD>
</TR></TABLE></DIV>
_HTML_
}

#-----------------------------
# フッターの生成
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
	# Mireille内のHTMLデザイン
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
