#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Style Module -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
#use strict;
#use vars qw(%CF %IN %CK);

#-----------------------------
# デザイン情報
#デザインを大幅に変えたら、適切に変更してください
$CF{'Design'}="Type: Mireille Default 1.2";

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
	$_[0]?qq($CF{'home'}">BACK to HOME):qq(index.cgi">BACK to INDEX)
]}</A></H1></TH>
</TR></TABLE></DIV>
_HTML_
}
$CF{'pgfoot'}=&getPageFooter;

#-----------------------------
# 投稿フォームで使うJavaScript
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
		//絶対指定アイコン
		preview.src=RegExp.$2;
		preview.title=RegExp.$2;
		icon.disabled=true;
	}else if(iconSetting&2&&cmd.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//相対指定アイコン
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
	if(!confirm("新しい本文を保存すると、古い本文データは消えてしまいます\nそれでも保存してよろしいですか？"))
		return false;
	var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
	if(!bodyObj)return false;
	
	var backup='';
	if(document.cookie.match(/(^|; )MirBody=([^;]+)/))backup=unescape(RegExp.$2);
	if(!bodyObj.value.length){
		//valueが空
		document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
		if(bodyObj.addBehavior){
			//bahavior版（IE依存）
			if(!bodyObj.getAttribute('MireilleBody'))bodyObj.addBehavior('#default#userData');
			bodyObj.setAttribute('MireilleBody','');
			bodyObj.save('MireilleBody');
		}
		alert('一時保存されていた本文データを削除しました');
		return;
	}else if(bodyObj.addBehavior){
		//bahavior版（IE依存）（サイズ制限128KB）
		if(!bodyObj.getAttribute('MireilleBody'))bodyObj.addBehavior('#default#userData');
		bodyObj.setAttribute('MireilleBody',bodyObj.value);
		bodyObj.save('MireilleBody');
		alert("今の本文データを一時保存しました\nあくまでIEによる“一時保存”だから過信しないでください");
	}else{
		//Cookie版（サイズ制限3KBほど）
		document.cookie='MirBody='+escape(bodyObj.value)+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';
		if(document.cookie.match(/(^|; )MirBody=([^;]+)/)&&bodyObj.value==unescape(RegExp.$2)){
			alert("今の本文データを一時保存しましたょ\nあくまで“一時保存”だから過信しないでねっ");
		}else{
			//3850byte程度でサイズ制限がかかる。
			document.cookie='MirBody='+backup+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//終末の日
			alert("save失敗\nサイズオーバーかも。");
			return false;
		}
	}
}
function loadBodyCk(){
	if(!confirm("Cookieから本文データを読み出すと、現在の本文は消えてしまいます\nそれでも読み出してよろしいですか？"))
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
		alert('load失敗');
		return false;
	}
}
-->
</SCRIPT>
_CONFIG_


#-----------------------------
# フォーム用属性セレクタ代替JScript
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
# フッターの生成
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
# 注意書き（TOPページのメニューの下に表示されます）
$CF{'note'}=<<"_CONFIG_";
<TABLE align="center" class="note" summary="注意書き"><TR><TD><UL class="note">
<LI>投稿された記事の著作権は管理者の管理下におかれます。</LI>
<LI>未読記事は投稿日時が赤く表示されます。</LI>
<LI>24時間以内の投稿には$CF{'new'}マークが付きます。</LI>
<LI>記事ナンバーをクリックすると、その記事の修正画面になります。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE>

_CONFIG_

#-----------------------------
# 新規投稿/編集フォーム
$CF{'wrtfm'}=<<'_CONFIG_';
<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>本文以外ではタグは一切使用できません。</LI>
<LI>HTTP, FTP, MAILアドレスのリンクは自動でつきます。</LI>
<LI>一般的なブラウザではマウスカーソルを項目の上に置き、<BR>しばらく待つと簡単な説明が出てきます。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE></DIV>

<DIV class="center"><TABLE border="2" cellspacing="0" class="write" summary="MainForm">
<COL span="3">
<THEAD><TR><TH colspan="3" class="caption"><A name="Form"></A>$DT{'caption'}</TH></TR></THEAD>

<TBODY>
<TR title="subJect&#10;記事の題名を入力します&#10;最高全角100文字までです">
<TH class="item">
<LABEL accesskey="j" for="subject">■題名(<SPAN class="ak">J</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon&#10;アイコンを選択します" style="text-align:center">
<LABEL accesskey="i" for="icon">■ <A href="index.cgi?icct" title="アイコン見本&#10;新しい窓を開きます" target="_blank">アイコン</A>（<KBD class="ak">Ｉ</KBD>）■</LABEL>
</TH>
</TR>
<TR title="Name&#10;名前を入力します（必須）&#10;最高全角50文字までです">
<TH class="item">
<LABEL accesskey="n" for="name">■名前(<SPAN class="ak">N</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;クッキー保存のON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL&#10;メールアドレスを入力します">
<TH class="item">
<LABEL accesskey="l" for="email">■E-mail(<SPAN class="ak">L</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme&#10;自分のサイトのURLを入力します">
<TH class="item">
<LABEL accesskey="o" for="home">■ホーム(<SPAN class="ak">O</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password&#10;削除/修正時に使用するパスワードを入力します（必須）&#10;最高半角24文字までです">
<TH class="item">
<LABEL accesskey="p" for="pass">■パスワード(<SPAN class="ak">P</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
　
<SPAN title="Color&#10;本文の色を入力します">
<SPAN class="item">
<LABEL accesskey="c" for="color">■色(<SPAN class="ak">C</SPAN>)：</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand&#10;専用アイコンを始めとする拡張命令を使う場合に使用します&#10;'command=value'のように指定します">
<TH class="item">
<LABEL accesskey="m" for="cmd">■コマンド(<SPAN class="ak">M</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()">
</TD>
<TD class="input" title="Icon&#10;アイコンを選択します">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>

<TBODY title="Body&#10;記事の本文を入力します&#10;全角約10000文字までです&#10;使用できるタグはヘルプを参照してください">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">■ 本文(<SPAN class="ak">B</SPAN>) ■</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center">
<TEXTAREA name="body" id="body" cols="80" rows="8">$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY><TR title="Submit&#10;記事を投稿します">
<TD colspan="3" class="foot">
<INPUT type="submit" class="submit" accesskey="s" value="投稿する">
<!-- <INPUT type="reset" class="reset" value="リセット"> -->
<INPUT type="button" class="button" accesskey="," value="一時保存," onclick="saveBodyCk()" onkeypress="saveBodyCk()">
<INPUT type="button" class="button" accesskey="." value="読み込み." onclick="loadBodyCk()" onkeypress="loadBodyCk()">
</TD></TR></TBODY>

</TABLE>
</DIV>

$CF{'jsWritingForms'}
_CONFIG_

#-----------------------------
# 返信フォーム
$CF{'resfm'}=<<'_CONFIG_';
<DIV class="center"><TABLE border="2" cellspacing="0" class="write" summary="ResForm">
<COL span="3">
<THEAD><TR><TH colspan="3" class="caption"><A name="Form"></A>$DT{'caption'}</TH></TR></THEAD>

<TBODY title="Body&#10;記事の本文を入力します&#10;全角約10000文字までです&#10;使用できるタグはヘルプを参照してください">
<TR><TH class="item" colspan="3" style="text-align:center"><LABEL accesskey="b"
 for="body">■ 本文(<SPAN class="ak">B</SPAN>) ■</LABEL></TH></TR>
<TR><TD colspan="3" style="text-align:center">
<TEXTAREA name="body" id="body" cols="80" rows="8">$DT{'body'}</TEXTAREA></TD>
</TR></TBODY>

<TBODY>
<TR title="subJect&#10;記事の題名を入力します&#10;最高全角100文字までです">
<TH class="item"><LABEL accesskey="j" for="subject">■題名(<SPAN class="ak">J</SPAN>)：</LABEL></TH>
<TD class="input">
<INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}">
</TD>
<TH class="item" title="Icon&#10;アイコンを選択します" style="text-align:center">
<LABEL accesskey="i" for="icon">■ <A href="index.cgi?icct" title="アイコン見本&#10;新しい窓を開きます" target="_blank">アイコン</A>（<KBD class="ak">Ｉ</KBD>）■</LABEL>
</TH>
</TR>
<TR title="Name&#10;名前を入力します（必須）&#10;最高全角50文字までです">
<TH class="item">
<LABEL accesskey="n" for="name">■名前(<SPAN class="ak">N</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="name" id="name" maxlength="50" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;クッキー保存のON/OFF">Coo<SPAN class="ak">k</SPAN>ie
<INPUT name="cook" id="cook" type="checkbox" checked></LABEL>
</TD>
<TD rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}">
</TD>
</TR>
<TR title="e-maiL&#10;メールアドレスを入力します">
<TH class="item">
<LABEL accesskey="l" for="email">■E-mail(<SPAN class="ak">L</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}">
</TD>
</TR>
<TR title="hOme&#10;自分のサイトのURLを入力します">
<TH class="item">
<LABEL accesskey="o" for="home">■ホーム(<SPAN class="ak">O</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}">
</TD>
</TR>
<TR title="Password&#10;削除/修正時に使用するパスワードを入力します（必須）&#10;最高半角24文字までです">
<TH class="item">
<LABEL accesskey="p" for="pass">■パスワード(<SPAN class="ak">P</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="password" name="pass" id="pass" maxlength="24" value="$DT{'pass'}">
　
<SPAN title="Color&#10;本文の色を入力します">
<SPAN class="item">
<LABEL accesskey="c" for="color">■色(<SPAN class="ak">C</SPAN>)：</LABEL>
</SPAN>
<SPAN class="input">
@{[&iptcol($DT{'color'})]}
</SPAN>
</SPAN>
</TD>
</TR>
<TR title="coMmand&#10;専用アイコンを始めとする拡張命令を使う場合に使用します&#10;'command=value'のように指定します">
<TH class="item">
<LABEL accesskey="m" for="cmd">■コマンド(<SPAN class="ak">M</SPAN>)：</LABEL>
</TH>
<TD class="input">
<INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()">
</TD>
<TD class="input" title="Icon&#10;アイコンを選択します">
@{[&iptico($DT{'icon'})]}
</TD>
</TR>
</TBODY>
<TBODY>
<TR title="Submit&#10;記事を投稿します">
<TD colspan="3" class="foot">
<INPUT type="submit" class="submit" accesskey="s" value="投稿する">
<!-- <INPUT type="reset" class="reset" value="リセット"> -->
<INPUT type="button" class="button" accesskey="," value="一時保存," onclick="saveBodyCk()" onkeypress="saveBodyCk()">
<INPUT type="button" class="button" accesskey="." value="読み込み." onclick="loadBodyCk()" onkeypress="loadBodyCk()">
</TD></TR>
</TBODY>
</TABLE>
<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>上に表示されているスレッド【No.$DT{'i'}】への返信を行います。</LI>
<LI>本文以外ではタグは一切使用できません。</LI>
<LI>HTTP, FTP, MAILアドレスのリンクは自動でつきます。</LI>
<LI>一般的なブラウザではマウスカーソルを項目の上に置き、<BR>しばらく待つと項目の簡単な説明が出てきます。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE></DIV>

$CF{'jsWritingForms'}
_CONFIG_



#----------------------------------------------------------------------------------------#
#
# ここからStyle処理部
#

#-------------------------------------------------
#親記事
sub artprt{
=item 引数
\% スレッドの記事情報ハッシュのリファレンス
$	この記事の情報
=cut
	#記事情報を受け取って
	my%DT=(new=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
	#削除されたら知らせて
	'del'eq$DT{'Mir12'}&&($DT{'body'}='Mireille: [この記事は削除されました]');
	#記事ナビ
	ArtNavi->addThreadHead(\%DT);
	ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
	#記事項目の調整をして
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">【HOME】</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX秒から日付に
	$DT{'-iconTag'}=&getIconTag(\%DT)||'&nbsp;';
	#未読記事に印
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#いよいよ出力だよ
	print<<"_HTML_";
<DIV class="thread" title="$DT{'i'}番スレッド">
<TABLE cellspacing="0" class="subject" summary="$DT{'i'}番スレッド"><TR>
<TH class="subject"><H2 class="subject"><A name="art$DT{'i'}" id="art$DT{'i'}" title="$DT{'i'}番スレッド">$DT{'subject'}</A></H2></TH>
<TD class="arrow">
<A name="nav_n$DT{'ak'}" href="#nav_n@{[$DT{'ak'}-1]}" title="上のスレッドへ">▲</A>
<A name="nav_r$DT{'i'}" href="index.cgi?res=$DT{'i'}#Form" title="この記事No.$DT{'i'}に返信">■</A>
<A name="nav_s$DT{'ak'}" href="#nav_s@{[$DT{'ak'}+1]}" title="下のスレッドへ">▼</A>
</TD>
</TR></TABLE>

<TABLE cellspacing="0" class="parent" summary="Article$DT{'i'}-0" title="$DT{'i'}-0">
<COL class="number"><COL class="name"><COL class="date">
<TR class="info">
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">【No.$DT{'i'}】</A></TH>
	<TD class="name">$DT{'new'} <SPAN class="name">$DT{'name'}</SPAN>
	<SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}番スレッドの親記事を修正"><A
	 href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">【修正】</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'-iconTag'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
</TABLE>

_HTML_
	return;
}


#-------------------------------------------------
#子記事
sub artchd{
=item 引数
\% スレッドの記事情報ハッシュのリファレンス
$	この記事の情報
=cut
	#記事情報を受け取って
	my%DT=(new=>'',%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));

	#削除されてるときはここの前に飛ばしちゃうの
	#記事ナビ
	ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
	#記事項目の調整をして
	$DT{'email'}&&($DT{'name'}=qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>));
	$DT{'home'}&&=qq(<A href="$DT{'home'}" target="_top">【HOME】</A>);
	$DT{'date'}=&date($DT{'time'}); #UNIX秒から日付に
	$DT{'-iconTag'}=&getIconTag(\%DT)||'&nbsp;';
	#未読記事に印
	$DT{'time'}>$CK{'time'}&&($DT{'date'}=qq(<SPAN class="new">$DT{'date'}</SPAN>));
	$DT{'time'}>$^T-$CF{'newnc'}&&($DT{'new'}=$CF{'new'});
	#いよいよ出力だよ
	print<<"_HTML_";
<TABLE cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}" title="$DT{'i'}-$DT{'j'}">
<COL class="space"><COL class="number"><COL class="name"><COL class="date">
_HTML_

=pod 子記事タイトルを使用する場合
	print<<"_HTML_";
	<TR><TH class="space">&nbsp;</TH>
<TH colspan="3" class="subject"><H3 class="subject">$DT{'subject'}</H3></TH></TR>
_HTML_
=cut

	print<<"_HTML_";
<TR class="info"><TH class="space" rowspan="2">&nbsp;</TH>
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number" href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">【Re:$DT{'j'}】</A></TH>
	<TD class="name">$DT{'new'} <SPAN class="name">$DT{'name'}</SPAN>
	<SPAN class="home">$DT{'home'}</SPAN></TD>
	<TD class="date"><SPAN class="date">$DT{'date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}番スレッドの子記事$DT{'j'}を修正"
	><A href="index.cgi?rvs=$DT{'i'}-$DT{'j'}">【修正】</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'-iconTag'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
</TABLE>

_HTML_
	return;
}


#-------------------------------------------------
#記事フッタ
sub artfot{
=item 引数
\% 記事情報 ハッシュのリファレンス
=cut
	#記事情報を受け取って
	my%DT=%{shift()};
	
	if($DT{'res'}||$CF{'readOnly'}){
		#返信モードのとき
			print<<'_HTML_';
</DIV>


_HTML_
	}else{
		#記事表示
		if($CF{'maxChilds'}&&$DT{'j'}>=$CF{'maxChilds'}){
			#子記事数制限を超えた
			print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}" class="warning"
 href="#res$DT{'i'}">この記事スレッドNo.$DT{'i'}は子記事数制限に達したので返信できません(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
#memo.
#返信モードがないのに「href="#res$DT{'i'}"」とリンクを張っているのは、アクセスキーを使用可能にするため
		}else{
			#この記事スレッドNo.???に返信する(?)
		print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}"
 href="index.cgi?res=$DT{'i'}#art$DT{'i'}-$DT{'j'}">この記事スレッドNo.$DT{'i'}に返信する(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
		}
	}
	#記事ナビ
	ArtNavi->addThreadFoot(\%DT);
}


#-------------------------------------------------
# 親記事フォーム
#
sub prtfrm{
	my%DT=%CK;

	#アイコンの初期設定
	($CF{'prtitm'}=~/\bicon\b/o)&&(&iptico($DT{'icon'}));
	#色の初期設定
#	($CF{'prtitm'}=~/\bcolor\b/o)&&(&iptcol($DT{'color'}));

=item この初期設定の意義

この初期設定部は一見必要なさそうです
しかしプレビュー機能というものがこの掲示板にはあります
通常は<IMG src="$DT{'icon'}">としているわけですが、
$DT{'icon'}が空だったら、もしくは存在しないアイコンだったらどうしましょう
それを前もって設定するためにここでリストと照合しておくわけです
但し、これは初期デザインのようにこのIMGタグがアイコンリストのSELECTタグより、
前にある場合の問題で、プレビュー部分より選択部分が前の場合は、
初期設定をコメントアウトしても問題ありません

=cut

	my$wrtfm=$CF{'wrtfm'};
	chomp$wrtfm;
	if(defined$DT{'body'}){
		$DT{'caption'}='■ 記事修正フォーム ■';
		$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
	}else{
		$DT{'caption'}='■ 新規送信フォーム ■';
		$DT{'home'}||($DT{'home'}='http://');
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="0">\n);
	}
	$DT{'Sys'}&&($wrtfm=~s/<INPUT/$DT{'Sys'}<INPUT/io);
	
	print qq(<FORM accept-charset="euc-jp" id="artform" method="post" action="index.cgi">\n);
	eval qq(print<<"_HTML_";\n$wrtfm\n_HTML_);
	print"</FORM>\n";
}


#-------------------------------------------------
# 子記事フォーム
#
sub chdfrm{
	#返信フォーム準備
	my%DT=%CK;
	
	#アイコンの初期設定
	($CF{'chditm'}=~/\bicon\b/o)&&(&iptico($DT{'icon'}));
	#色の初期設定
#	($CF{'chditm'}=~/\bcolor\b/o)&&(&iptcol($DT{'color'}));
	
	#デザイン読み込み
	my$resfm=$CF{'resfm'};
	chomp$resfm;#最後の改行を切り落とす
	#追加情報を埋め込む
	$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
	if(defined$DT{'j'}){
		$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
		$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
		$DT{'caption'}='■ 修正フォーム ■';
	}else{
		$DT{'caption'}='■ 返信フォーム ■';
	}
	$DT{'Sys'}&&($resfm=~s/<INPUT/$DT{'Sys'}<INPUT/io);

	#項目の初期設定
	$DT{'home'}||($DT{'home'}='http://'); #http://だけ入れておく
	#note01:Resは題名ないことも
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
# 書き込みの前処理を拡張したい時用
sub exprewrt{
	return 0;
}


#-------------------------------------------------
# 投稿日時表示用にフォーマットされた日付取得を返す
sub date{
=item 引数
$ time形式時刻
=cut
	$CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
	my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($_[0]+$CF{'timeOffset'});
	#sprintfの説明は、Perlの解説を見てください^^;;
	return sprintf("%4d年%02d月%02d日(%s) %02d時%02d分%s" #"1970年01月01日(木) 09時00分"の例
	,$year+1900,$mon+1,$day,('日','月','火','水','木','金','土')[$wday],$hour,$min,$ENV{'TZ'});
#	return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"の例
#	,$hour,$min,$sec,$year+1900,$mon+1,$day,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
#記事ナビ
sub artnavi{
=item 引数
$ 記事ナビのモード
=cut
	return if defined$::CF{'artnavi'}&&!$::CF{'artnavi'};

	#Netscape4は記事ナビ無し
	if($::IN{'hua'}=~/^Mozilla\/4.*(?:;\s*|\()[UI](?:;|\))/){
		$::CF{'artnavi'}=0;
		return; #記事ナビを出力しない
	}
	
	unless($_[0]){
		#記事ナビ本体
		#------------------------------------------------------------------------------------
		#ブラウザ判定
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
<TH id="navititl" onmousedown="beginDrag(event,'naviwind')">■記事ナビ - Mireille</TH>
<TD id="navibutt" style="width:35px" onmousedown="beginDrag(event,'naviwind')">
<A accesskey="m" onclick="void(view(event,'navibody'))" onkeydown="acskey(event,'navibody')"
 href="#拡大/縮小" title="拡大/縮小(&amp;M)">□</A>
<A accesskey="c" onclick="void(view(event,'naviwind'))" onkeydown="acskey(event,'naviwind')"
 href="#閉じる" title="閉じる(&amp;C)">×</A></TD>
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
onkeypress="setTimeout(&#34;artnavi('popup')&#34;,500);return false;">記事ナビ(<SPAN class="ak">N</SPAN>)</BUTTON></DIV>
_HTML_
		return;
	}
}

#-------------------------------------------------
# 記事ナビクラス
{package ArtNavi;
	my$ArtNaviBody='';
	#記事ナビの本文 -- クラスメソッド
	sub ArtNavi::body{
		my$class=shift;
		$ArtNaviBody=shift if@_>0;
		$ArtNaviBody
	}
	
	#記事ナビのスレッドヘッダ追加 -- クラスメソッド
	sub ArtNavi::addThreadHead{
		my$class=shift;
		my%DT=%{shift()};
		$ArtNaviBody.=<<"_HTML_";
<DIV class="navithre">
<DIV class="navisubj">
<A href="#nav_r$DT{'i'}" title="返信"><STRONG>$DT{'i'}</STRONG></A>:
<A href="#art$DT{'i'}">$DT{'subject'}</A>
</DIV>
<DIV class="navinums">
_HTML_
	}
	
	#記事ナビのスレッドフッタ追加 -- クラスメソッド
	sub ArtNavi::addThreadFoot{
		my$class=shift;
		my%DT=%{shift()};
		$ArtNaviBody.=<<"_HTML_";
<A href="index.cgi?res=$DT{'i'}#Form" title="返信" style="color:green;">Re</A>
</DIV>
</DIV>
_HTML_
	}
	
	#記事追加 -- クラスメソッド
	sub ArtNavi::addArticle{
		my$class=shift;
		my%DT=%{shift()};
		my$isNew=shift;
		if($isNew){
			#未読
			$ArtNaviBody.=qq(<A class="new" href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A> );
			return;
		}else{
			#既読
			$ArtNaviBody.=qq(<A href="#art$DT{'i'}-$DT{'j'}" title="$DT{'name'}">$DT{'j'}</A> );
			return;
		}
	}
}
package main;

#requireにstyle.cgiのRevisionを返す
($CF{'Style'}=qq$Revision$)=~/(\d+(?:\.\d+)*)/o;
$CF{'StyleRevision'}=$1;
__END__
