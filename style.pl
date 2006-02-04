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
<TD class="menu"><A href="$CF{'index'}?new#Form">新規投稿</A></TD>
<TD class="menu"><A href="$CF{'index'}">更新</A></TD>
<TD class="menu"><A href="$CF{'index'}?rvs">修正</A></TD>
<TD class="menu"><A href="$CF{'index'}?del">削除</A></TD>
<TD class="menu"><A href="$CF{'index'}?icct">アイコン</A></TD>
<TD class="menu"><A href="$CF{'index'}?seek">検索</A></TD>
<TD class="menu"><A href="$CF{'index'}?help">ヘルプ</A></TD>
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
<TH width="100%"><DIV class="head"><A href="@{[
	$_[0]?qq($CF{'home'}">BACK to HOME):qq($CF{'index'}">BACK to INDEX)
]}</A></DIV></TH>
</TR></TABLE></DIV>
_HTML_
}
$CF{'pgfoot'}=&getPageFooter;

#-----------------------------
# 投稿フォームで使うJavaScript
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
		//絶対指定アイコン
		oPreview.src=RegExp.$2;
		oPreview.title='+'+RegExp.$2;
		oIcon.disabled=true;
	}else if(iconSetting&2&&oCommand.value.match(/(^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/)){
		//相対指定アイコン
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
			status="現在の本文データをIE式で自動保存しました。";
			break;
		case'SavedBodyDataCookie':
			status="現在の本文データを自動保存しました。";
			break;
		case'FailedToSave':
			status="自動保存に失敗しました。Cookieに保存可能な最大文字数(約4KB)を超えたからかもしれません。";
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
	if(!confirm("新しい本文を保存すると、古い本文データは消えてしまいます\nそれでも保存してよろしいですか？"))
		return false;
	
	switch(saveBodyData('MireilleQuicksave')){
	case'DeleteBodyData':
		alert('一時保存されていた本文データを削除しました。');
			break;
	case'SavedBodyDataIE':
		alert("現在の本文データを一時保存しました。\nあくまでIEによる“一時保存”なので過信しないでください。");
			break;
	case'SavedBodyDataCookie':
		alert("現在の本文データを一時保存しました。\nあくまで“一時保存”なので過信しないでください。");
			break;
	case'FailedToSave':
		alert("一時保存に失敗しました。\n保存可能な最大文字数を超えたからかもしれません。\n"
				+'本文をファイルに保存しながら書いた方がよいかと思われます。');
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
		//bahavior版（IE依存）（サイズ制限:escape無しで128KB）
		if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
		if(!oBody.value.length){
			//valueが空→削除
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
			//保存
			expires.setMonth(expires.getMonth()+1);
			oBody.expires=expires.toUTCString();
			oBody.setAttribute(key,oBody.value);
			oBody.setAttribute('MireilleBody',new Date().toUTCString());
			oBody.save('MireilleBody');
			return'SavedBodyDataIE';
		}
	}else{
		//Cookie版（サイズ制限:escapeした後で3KBほど）
		if(!oBody.value.length){
			//valueが空→削除
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
			//3850byte程度でサイズ制限がかかる。
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
	if(!confirm("Cookieから本文データを読み出すと、現在の本文は消えてしまいます\nそれでも読み出してよろしいですか？"))
		return false;
	
	if(key=='MireilleQuicksave'||key=='MireilleAutosave');
	else if(confirm("QuicksaveのデータとAutosaveのデータ、どちらを読み出しますか？\n"
				+"Quicksaveの場合は「OK」、Autosaveの場合は「キャンセル」を選んでください"))
		key='MireilleQuicksave';
	else key='MireilleAutosave';
	
	if(oBody.addBehavior){
		if(!oBody.getAttribute('MireilleBody'))oBody.load('MireilleBody');
		var temp=oBody.getAttribute(key);
		if(temp){
			oBody.value=temp;
		}else{
			alert('読み込みに失敗しました');
		}
	}else if(document.cookie.match(new RegExp('(^|; )'+key+'=([^;]+)'))){
		oBody.value=unescape(RegExp.$2);
	}else{
		alert('読み込みに失敗しました');
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
		//bahavior版（IE依存）
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
		return'一時保存されていた本文データを削除しました。';
	}else if(key=='MireilleAutosave'){
		return'自動保存されていた本文データを削除しました。';
	}else{
		return'rbd: Something Wicked happened!';
	}
	return true;
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
# ヘッダーの生成
sub getHeader{
    my%DT=@_;
    return join"\n",$CF{'bodyHead'},($DT{'skyline'}||''),$CF{'pghead'},$CF{'menu'};
}

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
<DIV class="center">
<TABLE align="center" class="note" summary="注意書き"><TR><TD><UL class="note">
<LI>投稿された記事の著作権は管理者の管理下におかれます。</LI>
<LI>未読記事は投稿日時が赤く表示されます。</LI>
<LI>24時間以内の投稿には$CF{'new'}マークが付きます。</LI>
<LI>記事ナンバーをクリックすると、その記事の修正画面になります。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE>
</DIV>
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
    my%DT=(%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
    my@temp=qw(Name Home Date Icon Signature New accessUnread);
    @DT{map{'_'.$_}@temp}=map{''}@temp;
    #削除されたら知らせて
    'del'eq$DT{'Mir12'}&&($DT{'body'}='Mireille: [この記事は削除されました]');
    #記事ナビ
    ArtNavi->addThreadHead(\%DT);
    ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
    #記事項目の調整をして
    $DT{'_Name'}=sprintf'<SPAN class="name">%s</SPAN>'
	,$DT{'email'}?qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>):$DT{'name'};
    $DT{'_Home'}=qq(<SPAN class="home"><A href="$DT{'home'}" target="_top">【HOME】</A></SPAN>)if$DT{'home'};
    $DT{'_Date'}=sprintf$DT{'time'}>$CK{'time'}?'<SPAN class="new">%s</SPAN>':'%s',&date($DT{'time'});
    $DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
    $DT{'_Signature'}=sprintf'<SPAN class="signature">[&nbsp;%s&nbsp;]</SPAN><BR>'
	,&getSignatureView(\%DT)if$CF{'signature'}&&$DT{'signature'};
    if($DT{'time'}>$^T-$CF{'newnc'}){
	$DT{'_New'}=$CF{'new'};
	$DT{'_tabUnread'}=sprintf' tabindex="%d"',$DT{'-unreads'};
	++$DT{'-unreads'};
    }
    
    #ファイル添付
    my $attachments = getAttachedFiles(\%DT) if $DT{'attach'};
    
    #いよいよ出力だよ
    print<<"_HTML_";
<DIV class="thread" title="$DT{'i'}番スレッド" align="center" width="99%">
<TABLE border="0" cellspacing="0" class="subject" summary="$DT{'i'}番スレッド" width="100%"><TR>
<TH class="subject"><H2 class="subject"><A name="art$DT{'i'}" id="art$DT{'i'}" title="$DT{'i'}番スレッド">$DT{'subject'}</A></H2></TH>
<TD class="arrow">
<A name="nav_n$DT{'ak'}" href="#nav_n@{[$DT{'ak'}-1]}" title="上のスレッドへ">▲</A>
<A name="nav_r$DT{'i'}" href="$CF{'index'}?res=$DT{'i'}#Form" title="この記事No.$DT{'i'}に返信">■</A>
<A name="nav_s$DT{'ak'}" href="#nav_s@{[$DT{'ak'}+1]}" title="下のスレッドへ">▼</A>
</TD>
</TR></TABLE>

<TABLE border="0" cellspacing="0" class="parent" summary="Article$DT{'i'}-0" title="$DT{'i'}-0" width="100%">
<COL class="number"><COL class="name"><COL class="date">
<TR class="info">
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number"
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}"$DT{'_tabUnread'}>【No.$DT{'i'}】</A></TH>
	<TD class="name">$DT{'_New'} $DT{'_Name'} $DT{'_Home'}</TD>
	<TD class="date"><SPAN class="date">$DT{'_Date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}番スレッドの親記事を修正"><A
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">【修正】</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'_Signature'} $DT{'_Icon'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
$attachments</TABLE>

_HTML_
    return$DT{'-unreads'};
}


#-------------------------------------------------
#子記事
sub artchd{
=item 引数
\% スレッドの記事情報ハッシュのリファレンス
$	この記事の情報
=cut
    #記事情報を受け取って
    my%DT=(%{shift()},(shift()=~/([^\t]*)=\t([^\t]*);\t/go));
    my@temp=qw(Name Home Date Icon Signature New accessUnread);
    @DT{map{'_'.$_}@temp}=map{''}@temp;
    #削除されてるときはここの前に飛ばしちゃうの
    #記事ナビ
    ArtNavi->addArticle(\%DT,($DT{'time'}>$CK{'time'}));
    #記事項目の調整をして
    $DT{'_Name'}=sprintf'<SPAN class="name">%s</SPAN>'
	,$DT{'email'}?qq(<A href="mailto:$DT{'email'}">$DT{'name'}</A>):$DT{'name'};
    $DT{'_Home'}=qq(<SPAN class="home"><A href="$DT{'home'}" target="_top">【HOME】</A></SPAN>)if$DT{'home'};
    $DT{'_Date'}=sprintf$DT{'time'}>$CK{'time'}?'<SPAN class="new">%s</SPAN>':'%s',&date($DT{'time'});
    $DT{'_Icon'}=&getIconTag(\%DT)||'&nbsp;';
    $DT{'_Signature'}=sprintf'<SPAN class="signature">[&nbsp;%s&nbsp;]</SPAN><BR>'
	,&getSignatureView(\%DT)if$CF{'signature'}&&$DT{'signature'};
    if($DT{'time'}>$^T-$CF{'newnc'}){
	$DT{'_New'}=$CF{'new'};
	$DT{'_tabUnread'}=sprintf' tabindex="%d"',$DT{'-unreads'};
	++$DT{'-unreads'};
    }
    
    #ファイル添付
    my $attachments = getAttachedFiles(\%DT) if $DT{'attach'};
    
    #いよいよ出力だよ
    print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}" title="$DT{'i'}-$DT{'j'}" width="100%">
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
	<TH class="number"><A name="art$DT{'i'}-$DT{'j'}" class="number"
	 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}"$DT{'_tabUnread'}>【Re:$DT{'j'}】</A></TH>
	<TD class="name">$DT{'_New'} $DT{'_Name'} $DT{'_Home'}</TD>
	<TD class="date"><SPAN class="date">$DT{'_Date'}</SPAN>
	<SPAN class="revise" title="$DT{'i'}番スレッドの子記事$DT{'j'}を修正"
	><A href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">【修正】</A></SPAN></TD>
</TR>
<TR><TD class="icon">$DT{'_Signature'} $DT{'_Icon'}</TD>
	<TD colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</TD></TR>
$attachments</TABLE>

_HTML_
    return$DT{'-unreads'};
}


#-------------------------------------------------
#記事フッタ
sub artfot{
=item 引数
\% 記事情報 ハッシュのリファレンス
=cut
    #記事情報を受け取って
    my%DT=%{shift()};
	
    if($DT{'res'}){
	#返信モードのとき
	print<<'_HTML_';
</DIV>


_HTML_
    }elsif($CF{'readOnly'}||$DT{'-isLocked'}||$DT{'-isOverflowed'}){
	#何らかの理由で閲覧専用
	my$message=sprintf
	    +($CF{'readOnly'}?'読み込み専用モードなのでこの記事スレッドNo.%dの閲覧専用です'
	      :$DT{'-isLocked'}?'この記事スレッドNo.%dはロックされているので閲覧専用です'
	      :$DT{'-isOverflowed'}?'この記事スレッドNo.%dは子記事数制限に達したので閲覧専用です'
	      :'なにはともあれとりあえずこの記事スレッドNo.%dは閲覧専用です'),$DT{'i'};
	print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}" class="warning"
 href="$CF{'index'}?res=$DT{'i'}">$message(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
    }else{
	#この記事スレッドNo.???に返信する(?)
	print<<"_HTML_";
<TABLE border="0" cellspacing="0" class="foot" summary="ArticleFooter" width="100%"><TR>
<TH align="right" width="100%"><P align="right"><A accesskey="$DT{'ak'}" name="res$DT{'i'}"
 href="$CF{'index'}?res=$DT{'i'}#Form">この記事スレッドNo.$DT{'i'}に返信する(<SPAN
 class="ak">$DT{'ak'}</SPAN>)</A></P></TH>
</TR></TABLE>
</DIV>


_HTML_
    }
    #記事ナビ
    ArtNavi->addThreadFoot(\%DT);
}


#-------------------------------------------------
# 記事ファイル添付欄
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
# 親記事投稿フォーム
#
sub prtfrm{
    my%DT=%CK;
    $DT{'_type'} = 'Parent';
    
    #アイコンの初期設定
    &iptico($DT{'icon'})if$CF{'prtitm'}=~/\bicon\b/o;
    #色の初期設定
    #	&iptcol($DT{'color'})if$CF{'prtitm'}=~/\bcolor\b/o;
	
    #追加情報
    $DT{'Sys'}=qq(<INPUT name="j" type="hidden" value="0">\n);
    if(defined$DT{'i'}){
	$DT{'caption'}='■ 親記事修正フォーム ■';
	$DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
	$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
    }else{
	$DT{'caption'}='■ 新規投稿フォーム ■';
    }
	
    #項目の初期設定
    $DT{'home'}='http://'unless$DT{'home'}; #http://だけ入れておく
    $DT{'cook'}=$DT{'cook'}||!exists$DT{'cook'}?' checked':'';
	
    #ファイル添付
    my $attachForm = getAttachForm(\%DT);
    
    print<<"_HTML_";
<FORM accept-charset="euc-jp" id="artform" method="post" action="$CF{'index'}" enctype="multipart/form-data">
<DIV class="center"><TABLE align="center" class="note"><TR><TD><UL class="note">
<LI>本文以外ではタグは一切使用できません。</LI>
<LI>HTTP, FTP, MAILアドレスのリンクは自動でつきます。</LI>
<LI>一般的なブラウザではマウスカーソルを項目の上に置き、<BR>しばらく待つと簡単な説明が出てきます。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE></DIV>



<DIV id="writingForm" class="box">
<H2 class="h"><A name="Form">$DT{'caption'}</A></H2>


<TABLE class="inputOthers">
<TR title="subJect&#10;記事の題名を入力します&#10;最高半角70文字までです">
<TH class="item"><LABEL accesskey="j" for="subject">■題名(<SPAN class="ak">J</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}"></TD>
<TH class="iconInputLabel" title="Icon&#10;アイコンを選択します">
<LABEL accesskey="i" for="icon">■ <A href="$CF{'index'}?icct" title="アイコンカタログ&#10;新しい窓を開きます"
 target="_blank">アイコン</A>（<KBD class="ak">I</KBD>）■</LABEL></TH>
</TR>

<TR title="Name&#10;名前を入力します（必須）&#10;最高半角40文字までです">
<TH class="item"><LABEL accesskey="n" for="name">■名前(<SPAN class="ak">N</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="name" id="name" maxlength="40" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;クッキー保存のON/OFF"
 >クッキ保存<INPUT name="cook" id="cook" type="checkbox"$DT{'cook'}></LABEL></TD>
<TD rowspan="4" class="iconPreview" title="Icon Preview"
 ><IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
</TR>

<TR title="e-maiL&#10;メールアドレスを入力します">
<TH class="item"><LABEL accesskey="l" for="email">■E-mail(<SPAN class="ak">L</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}"></TD>
</TR>

<TR title="hOme&#10;自分のサイトのURLを入力します">
<TH class="item"><LABEL accesskey="o" for="home">■ホーム(<SPAN class="ak">O</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}"></TD>
</TR>

<TR title="Password&#10;削除/修正時に使用するパスワードを入力します（必須）&#10;最低8文字・最高128文字です">
<TH class="item"><LABEL accesskey="p" for="pass">■パスワード(<SPAN class="ak">P</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="pass" id="pass" maxlength="128" value="$DT{'pass'}">
　
<SPAN title="Color&#10;本文の色を入力します">
	<SPAN class="item"><LABEL accesskey="c" for="color">■色(<SPAN class="ak">C</SPAN>)：</LABEL></SPAN>
	<SPAN class="input">@{[&iptcol($DT{'color'})]}</SPAN>
</SPAN>
</TD>
</TR>

<TR title="coMmand&#10;専用アイコンを始めとする拡張命令を使う場合に使用します&#10;'command=value'のように指定します">
<TH class="item"><LABEL accesskey="m" for="cmd">■コマンド(<SPAN class="ak">M</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()"></TD>
<TD class="input" title="Icon&#10;アイコンを選択します">@{[&iptico($DT{'icon'})]}</TD>


$attachForm

</TABLE>


<TABLE class="inputBody">
<TR><TD class="leftColumn">&nbsp;</TD>
<TH class="item"
 title="Body:記事の本文を入力します&#10;全角約10000文字までです&#10;使用できるタグはヘルプを参照"
><LABEL accesskey="b" for="body">■ 本文(<SPAN class="ak">B</SPAN>) ■</LABEL></TH>
<TD class="rightColumn">
<BUTTON accesskey="," class="buttonQuicksave"  title="本文データをQuickSaveします"
 onclick="quicksaveBodyData();return false" onkeypress="quicksaveBodyData();return false"
 >QSave(<KBD class="ak">,</KBD>)</BUTTON>
<BUTTON accesskey="." class="buttonLoadQuicksave" title="Quicksaveしたデータを読み込みます"
 onclick="loadBodyData('MireilleQuicksave');return false" onkeypress="loadBodyData('MireilleQuicksave');return false"
 >QLoad(<KBD class="ak">.</KBD>)</BUTTON>
<BUTTON accesskey="/" class="buttonLoadAutosave" title="Autosaveしたデータを読み込みます"
 onclick="loadBodyData('MireilleAutosave');return false" onkeypress="loadBodyData('MireilleAutosave');return false"
 >ALoad(<KBD class="ak">/</KBD>)</BUTTON>
</TD></TR>
<TR><TD colspan="3"><TEXTAREA name="body" id="body" cols="80" rows="8" onchange="if(!isLoaded)initialization()">$DT{'body'}</TEXTAREA></TD></TR>
</TABLE>


<P class="footer">$DT{'Sys'}
<INPUT type="submit" class="submit" accesskey="s" value="投稿する">
<!-- <INPUT type="reset" class="reset" value="リセット"> --></P>


</DIV>



$CF{'jsWritingForms'}
</FORM>

_HTML_
    return 1;
}


#-------------------------------------------------
# 子記事フォーム
#
sub chdfrm{
    #返信フォーム準備
    my%DT=%CK;
    $DT{'_type'} = 'Child';
    
    #アイコンの初期設定
    &iptico($DT{'icon'})if$CF{'chditm'}=~/\bicon\b/o;
    #色の初期設定
    #	&iptcol($DT{'color'})if$CF{'chditm'}=~/\bcolor\b/o;
	
    #追加情報
    $DT{'Sys'}.=qq(<INPUT name="i" type="hidden" value="$DT{'i'}">\n);
    if(defined$DT{'j'}){
	$DT{'Sys'}.=qq(<INPUT name="j" type="hidden" value="$DT{'j'}">\n);
	$DT{'Sys'}.=qq(<INPUT name="oldps" type="hidden" value="$DT{'oldps'}">\n);
	$DT{'caption'}='■ 子記事修正フォーム ■';
    }else{
	$DT{'caption'}='■ 返信投稿フォーム ■';
    }
	
    #項目の初期設定
    $DT{'home'}='http://'unless$DT{'home'}; #http://だけ入れておく
    $DT{'cook'}=$DT{'cook'}||!exists$DT{'cook'}?' checked':'';
    #note01:Resは題名ないことも
    if($CF{'chditm'}!~/\bsubject\b/o){
	$DT{'subject'}='disabled';
	$DT{'_isSubjectDisabled'}=' disabled';
    }else{
	$DT{'_isSubjectDisabled'}='';
    }
    
    #ファイル添付
    my $attachForm = getAttachForm(\%DT);
    
    
    print<<"_HTML_";
<FORM accept-charset="euc-jp" id="artform" method="post" action="$CF{'index'}" enctype="multipart/form-data">



<DIV id="writingForm" class="box">
<H2 class="h"><A name="Form">$DT{'caption'}</A></H2>


<TABLE class="inputBody">
<TR><TD class="leftColumn">&nbsp;</TD>
<TH class="item"
 title="Body:記事の本文を入力します&#10;全角約10000文字までです&#10;使用できるタグはヘルプを参照"
><LABEL accesskey="b" for="body">■ 本文(<SPAN class="ak">B</SPAN>) ■</LABEL></TH>
<TD class="rightColumn">
<BUTTON accesskey="," class="buttonQuicksave"  title="本文データをQuickSaveします"
  onclick="quicksaveBodyData();return false" onkeypress="quicksaveBodyData();return false"
 >QSave(<KBD class="ak">,</KBD>)</BUTTON>
<BUTTON accesskey="." class="buttonLoadQuicksave" title="Quicksaveしたデータを読み込みます"
 onclick="loadBodyData('MireilleQuicksave');return false" onkeypress="loadBodyData('MireilleQuicksave');return false"
 >QLoad(<KBD class="ak">.</KBD>)</BUTTON>
<BUTTON accesskey="/" class="buttonLoadAutosave" title="Autosaveしたデータを読み込みます"
 onclick="loadBodyData('MireilleAutosave');return false" onkeypress="loadBodyData('MireilleAutosave');return false"
>ALoad(<KBD class="ak">/</KBD>)</BUTTON>
</TD></TR>
<TR><TD colspan="3"><TEXTAREA name="body" id="body" cols="80" rows="8" onchange="if(!isLoaded)initialization()">$DT{'body'}</TEXTAREA></TD></TR>
</TABLE>


<TABLE class="inputOthers">
<TR title="subJect&#10;記事の題名を入力します&#10;最高半角70文字までです">
<TH class="item"><LABEL accesskey="j" for="subject">■題名(<SPAN class="ak">J</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="subject" id="subject" maxlength="70" value="$DT{'subject'}"$DT{'_isSubjectDisabled'}></TD>
<TH class="iconInputLabel" title="Icon&#10;アイコンを選択します">
<LABEL accesskey="i" for="icon">■ <A href="$CF{'index'}?icct" title="アイコンカタログ&#10;新しい窓を開きます"
 target="_blank">アイコン</A>（<KBD class="ak">I</KBD>）■</LABEL></TH>
</TR>

<TR title="Name&#10;名前を入力します（必須）&#10;最高半角40文字までです">
<TH class="item"><LABEL accesskey="n" for="name">■名前(<SPAN class="ak">N</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="name" id="name" maxlength="40" value="$DT{'name'}">
<LABEL accesskey="k" for="cook" title="cooKie&#10;クッキー保存のON/OFF"
 >クッキ保存<INPUT name="cook" id="cook" type="checkbox"$DT{'cook'}></LABEL></TD>
<TD rowspan="4" class="iconPreview" title="Icon Preview"
 ><IMG name="Preview" id="Preview" src="$DT{'icon'}" alt="" title="$DT{'icon'}"></TD>
</TR>

<TR title="e-maiL&#10;メールアドレスを入力します">
<TH class="item"><LABEL accesskey="l" for="email">■E-mail(<SPAN class="ak">L</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="email" id="email" maxlength="100" value="$DT{'email'}"></TD>
</TR>

<TR title="hOme&#10;自分のサイトのURLを入力します">
<TH class="item"><LABEL accesskey="o" for="home">■ホーム(<SPAN class="ak">O</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="home" id="home" maxlength="80" value="$DT{'home'}"></TD>
</TR>

<TR title="Password&#10;削除/修正時に使用するパスワードを入力します（必須）&#10;最低8文字・最高128文字です">
<TH class="item"><LABEL accesskey="p" for="pass">■パスワード(<SPAN class="ak">P</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="pass" id="pass" maxlength="128" value="$DT{'pass'}">
　
<SPAN title="Color&#10;本文の色を入力します">
	<SPAN class="item"><LABEL accesskey="c" for="color">■色(<SPAN class="ak">C</SPAN>)：</LABEL></SPAN>
	<SPAN class="input">@{[&iptcol($DT{'color'})]}</SPAN>
</SPAN>
</TD>
</TR>

<TR title="coMmand&#10;専用アイコンを始めとする拡張命令を使う場合に使用します&#10;'command=value'のように指定します">
<TH class="item"><LABEL accesskey="m" for="cmd">■コマンド(<SPAN class="ak">M</SPAN>)：</LABEL></TH>
<TD class="input"><INPUT type="text" name="cmd" id="cmd" value="$DT{'cmd'}" onchange="changePreviewIcon()"></TD>
<TD class="input" title="Icon&#10;アイコンを選択します">@{[&iptico($DT{'icon'})]}</TD>
</TR>

$attachForm

</TABLE>


<P class="footer">$DT{'Sys'}
<INPUT type="submit" class="submit" accesskey="s" value="投稿する">
<!-- <INPUT type="reset" class="reset" value="リセット"> --></P>


</DIV>



<DIV class="center"><TABLE class="note"><TR><TD><UL class="note">
<LI>上に表示されているスレッド【No.$DT{'i'}】への返信を行います。</LI>
<LI>本文以外ではタグは一切使用できません。</LI>
<LI>HTTP, FTP, MAILアドレスのリンクは自動でつきます。</LI>
<LI>一般的なブラウザではマウスカーソルを項目の上に置き、<BR>しばらく待つと項目の簡単な説明が出てきます。</LI>
<LI>その他、機能の詳細についてはヘルプをご覧ください。</LI>
</UL></TD></TR></TABLE></DIV>

$CF{'jsWritingForms'}
</FORM>
_HTML_
    return 1;
}


#-------------------------------------------------
# ファイル添付フォーム
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
[<LABEL for="remove_attach__$item->{'hash'}"><INPUT type="checkbox" id="remove_attach__$item->{'hash'}" name="remove_attach__$item->{'hash'}" value="$item->{'hash'}">削除</LABEL>]
_HTML_
	}
    }
    for( my $i = 0; $i < $length - @array; $i++ ){
	$html .= qq{<INPUT id="attach__$i" name="attach__$i" type="file">\n};
    }
    
    return <<"_HTML_";
<TR title="attach&#10;ファイルを添付します">
<TH class="item"><LABEL>■ファイル添付：</LABEL></TH>
<TD class="input" colspan="2">$html</TD>
</TR>
_HTML_
}


#-------------------------------------------------
# ページ選択BOX
sub getPageSelectorSkin{
    my$following=shift;
    my$pageList =shift;
    my$preceding=shift;
    #	my($str,$end,$pags,$mode)=@_; #自力で組み立てたい時用
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
# 表紙の記事情報表示上
sub getArticoleInfomationA{
    my%data=@_;
    return<<"_HTML_";
<DIV class="artinfo">
$data{'unread'}
$data{'pageSelector'}
<P class="artinfo">このページのスレッド<BR>\n[ $data{'this'}]<BR>
<A name="nav_n0" href="#nav_s1" title="下のスレッドへ" accesskey="0">▼</A></P>
</DIV>
_HTML_
}


#-------------------------------------------------
# 表紙の記事情報表示下
sub getArticoleInfomationB{
    my%data=@_;
    return<<"_HTML_";
<DIV class="artinfo">
<P class="artinfo"><A name="nav_s@{[$data{'view'}+2]}" href="#nav_n@{[$data{'view'}+1]}" title="上のスレッドへ" accesskey="&#@{[$data{'view'}+50]};">▲</A><BR>
このページのスレッド<BR>\n[ $data{'this'}]</P>

$data{'pageSelector'}
</DIV>
_HTML_
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
    return($::CF{'artnavi'}=0)if$::IN{'hua'}=~/^Mozilla\/4.*(?:;\s*|\()[UI](?:;|\))/;
	
    unless(@_){
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
    }elsif('button'eq$_[0]){
	print<<"_HTML_";
<DIV><BUTTON onclick="setTimeout(&#34;artnavi('popup')&#34;,500);return false;" accesskey="n"
onkeypress="setTimeout(&#34;artnavi('popup')&#34;,500);return false;">記事ナビ(<SPAN class="ak">N</SPAN>)</BUTTON></DIV>
_HTML_
    }
    return;
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
	my$subject=$DT{'subject'}; #MirString->getTruncated($DT{'subject'},45);
	$ArtNaviBody.=<<"_HTML_";
<DIV class="navithre">
<DIV class="navisubj">
<A href="#nav_r$DT{'i'}" title="返信"><STRONG>$DT{'i'}</STRONG></A>:
<A href="#art$DT{'i'}">$subject</A>
</DIV>
<DIV class="navinums">
_HTML_
    }
	
    #記事ナビのスレッドフッタ追加 -- クラスメソッド
    sub ArtNavi::addThreadFoot{
	my$class=shift;
	my%DT=%{shift()};
	$ArtNaviBody.=<<"_HTML_";
<A href="$CF{'index'}?res=$DT{'i'}#Form" title="返信" style="color:green;">Re</A>
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

$CF{'_HiraganaLetterA'}->{'Style'}='あ';
#requireにstyle.cgiのRevisionを返す
($CF{'Style'}=qq$Revision$)=~/(\d+(?:\.\d+)*)/o;
$CF{'StyleRevision'}=$1;
__END__
