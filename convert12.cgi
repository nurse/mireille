#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Log Converter to Mir12 -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
use strict;
use vars qw(%CF);

=item 使い方

まず設置しましょう
圧縮ファイルを解凍して、convert12.cgiの設定をします

/
/Mir10/
/Mir10/log/
/Mir11/
/Mir11/log/
/MTP164g/
/MTP164g/1_data.cgi
/Mir12/
/Mir12/convert12.cgi
/Mir12/log/

こんな状態で設置してあり、
Mir10ディレクトリには Mireille1.0 が
Mir11ディレクトリには Mireille1.1 が
MTP164gディレクトリにはMulti Talk PRIVATE rel 0.1.64gが入っている場合、
それぞれ、

#Mir10
$CF{'oldlog'}='../Mir10/log/';
#CF{'from'}='Mir10';

#Mir11
$CF{'oldlog'}='../Mir11/log/';
#CF{'from'}='Mir11';

#MTP164g
$CF{'oldlog'}='../MTP164g/1_data.cgi'
#CF{'from'}='MTP164g';

と設定します

そして、convert12.cgiのおいてある、Mir12ディレクトリのlogディレクトリにその変換結果を保存したい場合

$CF{'log'}='./log/';

とします

その上でconvert12.cgiにブラウザからアクセスしましょう
少し待てばそれぞれの形式から1.2形式に変換され、掲示板本体から使えるようになります
（Mir12ディレクトリの掲示板がきちんと設定されていれば）

※警告!!
この作業を行うと変換先のディレクトリのログファイルは、
（上の例ではMir12ディレクトリ内のlogディレクトリのファイル)
変換結果で上書きされてしまうため、消えてしまいます
必ず新しく設置したものを指定してください

＊注意
変換先のディレクトリはあらかじめ作っておかないとエラーが出ます

=item 対応形式

Mireille 1.0形式
Mireille 1.1形式
Mireille 1.2形式β（1.2.1.1, 1.2.1.2での暫定形式）
Multi Talk PRIVATE rel 0.1.64g形式
をMireille 1.2形式に変換します

=cut

&main();

sub main{
	$CF{'oldlog'}='../../test/Mirei1133/log/';
	$CF{'from'}='Mir11';
	$CF{'log'}='./log/';
	$ENV{'REQUEST_METHOD'}='POST';#test.
	
	print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<title>: Mireille LogFileConverter :</title>
<style type="text/css">
<!--
/* 通常のリンク文字 */
a:link		{color:#44f;text-decoration:none;}
a:visited	{color:#44f;text-decoration:none;}
a:hover		{color:#fa8;text-decoration:underline;}
a:active	{color:#f00;text-decoration:underline;}
body{
	background-color: #fff;
	border-style: none;
	color: #355;
	font-family: 'ＭＳ Ｐゴシック',Osaka,sans-serif;
	font-size: 15px;
	margin: 3px 0;
	padding: 0;
	text-align: center;
	width: 100%;
}
form{
	margin: 0;
}
pre{
	font-family: 'ＭＳ ゴシック',Osaka,monospace;
	font-size: 85%;
	font-weight: normal;
	margin: 0.2em 1em;
	text-align: left;
	white-space: pre;
	word-break: break-all;
}
/* ---------- ページヘッダーテーブル ---------- */
table.head{
	background: #6ac;
	color: #fff;
	margin: auto;
}
table.head td{
	color: #fff;
	letter-spacing: 1em;
	padding: 3px 5px;
}
table.head th{padding: 3px 5px;}
h1.head,h1.head a:link{
	color: #fff;
	font-family: 'Comic Sans MS','ＭＳ Ｐゴシック',Osaka,sans-serif;
	font-size: 19px;
	font-weight: normal;
}
h1.head{margin: 0;}
h1.head a:visited{color: #fff;}
/* ---------- 見出し（Mode表示で主に使用） ---------- */
h2.mode{
	background-color: #ace;
	color: #fff;
	font-family: 'Comic Sans MS','ＭＳ Ｐゴシック',Osaka,sans-serif;
	font-size: 17px;
	font-weight: bold;
	margin: 10px auto;
	padding: 3px;
	text-align: center;
	width: 80%;
	margin-top:10px;margin-bottom:10px;
}
-->
</style>
</head>
<body>
<div class="center"><table align="center" border="0" cellspacing="0" class="head" summary="Header" width="90%"><tr>
<th width="100%"><h1 class="head" align="left">Mireille LogFileConverter</h1></th>
<td nowrap>■■■■■■■</td>
</tr></table></div>

_HTML_
	if(!$ENV{'REQUEST_METHOD'}||'GET'eq$ENV{'REQUEST_METHOD'}){
		print<<"_HTML_";
<h2 class="mode">ログファイルの変換をしますよ？</h2>
<pre style="text-align:left;width:60%">
Mireille Log Converter to Mireille'Mir12'をご利用いただきどうもありがとうございます
これからこのCGIは"$CF{'oldlog'}"に保存されている、"$CF{'from'}"形式のログを、
Mir12形式に変換した上で、"$CF{'log'}"に保存します

心の準備はできましたでしょうか
バックアップはとりましたか？
ログファイルの変換に際し、ログデータが破損したとしても、
Airemixはその責任は一切取りません（同情はしますけど）
心の準備ができましたら、したの「開始」を押してください
幸運をお祈りいたします


</pre>
<form method="post" action="convert12.cgi">
<p><input type="hidden" name="mode" value="exec">
<input type="submit" value="開始" style="height:30px;width:100px"></p>
</form>
_HTML_
	}elsif('POST'eq $ENV{'REQUEST_METHOD'}){
		($CF{'oldlog'}&&$CF{'from'}&&$CF{'log'})||die"ちゃんと設定できてないみたいです";

		my($from,@convert)=&convert();
		my$convert=@convert;
		print<<"_HTML_";
<h2>ログファイルの変換は完了しました</h2>


<pre style="text-align:left;width:60%">
◇今回行った処理
ログを $from形式 から Mireille'Mir12'形式 への変換

◇処理の結果
$convert個のファイルを Mir12形式 に変換しました

・情報ファイル"0.cgi"のMir12形式への変換
・変換したログファイル
_HTML_
		my$i=0;
		for(@convert){
			print$_;
			if(++$i>=10){print"\n";$i=0;}
			else{print" ";}
		}
		print<<"_HTML_";

</pre>
_HTML_
	}else{
		print qq(<h2 class="mode">何らかのエラーが起きました[$ENV{'REQUEST_METHOD'}]</h2>);
	}
	print<<"_HTML_";
<div class="center"><table align="center" border="0" cellspacing="0" class="head" summary="Footer" width="90%"><tr>
<td nowrap>■■■■■■■</td>
<th width="100%"><h1 class="head" align="right"><a href="$CF{'log'}../">BACK to INDEX</a></h1></th>
</tr></table></div>

<div class="AiremixCopy">- <a href="http://www.airemix.com/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</a>
<var>$CF{'Conv'}</var> -</div>
</body>
</html>
_HTML_
	exit;
}


#-------------------------------------------------
# Converter Switch
sub convert{
	unless($CF{'from'}){
	}elsif('Mir10'eq$CF{'from'}){
		return&fromMir10();
	}elsif('Mir11'eq$CF{'from'}){
		return&fromMir11();
	}elsif('MTP164g'eq$CF{'from'}){
		return&fromMTP164g();
	}
	return('エラー',('エラー'));
}


#-------------------------------------------------
# From Mireille 1.0.x
sub fromMir10{
	#ZeroFileの場所を探す
	my$logext; #ログ拡張子
	my$old0; #PATH of OldZeroFile
	if(-e"$CF{'oldlog'}0.cgi"){
		$logext='.cgi';
		$old0="$CF{'oldlog'}0.cgi";
	}elsif(-e"$CF{'oldlog'}0.pl"){
		$logext='.pl';
		$old0="$CF{'oldlog'}0.pl";
	}else{
		die"ZeroFile couldn't be found.";
	}
	
	#ZeroConvert
	open(OLD,$old0)||die"Can't read oldlog($old0)[$?:$!]";
	eval{flock(OLD,1)};
	my@zero=map{m/(.*)/o}<OLD>;
	close(OLD);
	
	my%DT;
	my@key=qw(Mir12 subject name email home icon color body blank pass time ra hua);
	@DT{@key}=split("\t",$zero[0]);
	$DT{'Mir12'}='1-1'unless$DT{'Mir12'};
	$zero[0]=join('',map{"$_=\t$DT{$_};\t"}qw(Mir12 subject name color time));
	open(ZERO,">$CF{'log'}0.cgi")||die"Can't write log($CF{'log'}0.cgi)[$?:$!]";
	eval{flock(ZERO,2)};
	print ZERO join("\n",@zero[0,1,2])."\n";
	close(ZERO);
	
	#ファイル一覧
	opendir(DIR,$CF{'oldlog'});
	my@file=sort{$a<=>$b}map{m/^(\d+)$logext$/o;$1}grep{m/^[1-9]\d*$logext$/o}readdir(DIR);
	closedir(DIR);
	
	#LogConvert
	my@convert=();
	for(@file){
		open(OLD,"$CF{'oldlog'}$_$logext")||die"Can't read oldlog($CF{'oldlog'}$_$logext)[$?:$!]";
		eval{flock(OLD,1)};
		my@log=map{m/(.*)/o}<OLD>;
		close(OLD);
		
		$log[0]=~/^Mir12=\t/o&& next;#変換済み除外
		for(@log){
			$_||next;
			my%DT;
			@DT{@key}=split("\t",$_);
			$_=join('',map{"$_=\t$DT{$_};\t"}@key);
		}
		
		open(NEW,">$CF{'log'}$_.cgi")||die"Can't write log($CF{'log'}$_.cgi)[$?:$!]";
		eval{flock(NEW,2)};
		print NEW join("\n",@log)."\n";
		close(NEW);
		
		push(@convert,"$_$logext");
		next;
	}
	my$from="Mireille'Mir10'";
	return($from,@convert);
}


#-------------------------------------------------
# From Mireille 1.1.x & 1.2.1.[1-2]
sub fromMir11{
	#ZeroFileの場所を探す
	my$logext; #ログ拡張子
	my$old0; #PATH of OldZeroFile
	if(-e"$CF{'oldlog'}0.cgi"){
		$logext='.cgi';
		$old0="$CF{'oldlog'}0.cgi";
	}elsif(-e"$CF{'oldlog'}0.pl"){
		$logext='.pl';
		$old0="$CF{'oldlog'}0.pl";
	}else{
		die"ZeroFile couldn't be found.";
	}
	
	#ZeroConvert
	open(OLD,$old0)||die"Can't read oldlog($old0)[$?:$!]";
	eval{flock(OLD,1)};
	my@zero=map{m/(.*)/o}<OLD>;
	close(OLD);
	
	($zero[0]=~/^Mir12=\t/o)&&(die"ログ形式がすでにMir12型です");
	$zero[0]=~s/\bMir1=\t/Mir12=\t/go;
	
	open(ZERO,">$CF{'log'}0.cgi")||die"Can't write log($CF{'log'}0.cgi)[$?:$!]";
	eval{flock(ZERO,2)};
	print ZERO join("\n",@zero[0,1,2])."\n";
	close(ZERO);
	
	#ファイル一覧
	opendir(DIR,$CF{'oldlog'});
	my@file=sort{$a<=>$b}map{m/^(\d+)$logext$/o;$1}grep{m/^[1-9]\d*$logext$/o}readdir(DIR);
	closedir(DIR);
	
	#LogConvert
	my@convert=();
	for(@file){
		my$log;
		open(OLD,"$CF{'oldlog'}$_$logext")||die"Can't read oldlog($CF{'oldlog'}$_$logext)[$?:$!]";
		eval{flock(OLD,1)};
		read(OLD,$log,-s"$CF{'oldlog'}$_$logext");
		close(OLD);
		print$log;
		
		$log=~s/\bMir1=\t/Mir12=\t/go;
		$log=~s/\ttitle=\t/\tsubject=\t/go;
		$log=~s/\tmes=\t/\tbody=\t/go;
		
		open(NEW,">$CF{'log'}$_.cgi")||die"Can't write log($CF{'log'}$_.cgi)[$?:$!]";
		eval{flock(NEW,2)};
		print NEW $log;
		close(NEW);
		push(@convert,"$_$logext");
	}
	my$from="Mireille'Mir11'";
	return($from,@convert);
}


#-------------------------------------------------
# From Multi Talk PRIVATE rel 0.1.64g
sub fromMTP164g{
	my@error=();
	my@zer2=(0);
	my@convert;
	
	#MTPログ読み込み
	open(MTP,$CF{'oldlog'})||die"Can't read log($CF{'oldlog'})[$?:$!]";
	eval{flock(MTP,1)};
	my%DT;
	my@log;
	while(<MTP>){
		chomp$_;
		unless($_){
			#スレッド変え
			$zer2[$DT{'i'}]=$DT{'time'};
			push(@convert,$DT{'i'});
			if(-s"$CF{'log'}$DT{'i'}.cgi"){
				push(@error,"$CF{'log'}$DT{'i'}.cgi");
			}else{
				open(LOG,">$CF{'log'}$DT{'i'}.cgi")||die"Can't write log($CF{'log'}$DT{'i'}.cgi)[$?:$!]";
				eval{flock(LOG,2)};
				print LOG join("\n",@log)."\n";
				close(LOG);
			}
			%DT=();
			@log=();
		}
		#SJISからEUCに漢字コードを変換しよう
		$_=sjis2euc($_);
		unless(defined$DT{'subject'}){
			#0行目
			@DT{qw(i mtp subject)}=split('<>',$_);
			next;
		}
		#記事
		@DT{qw(mtp mtp email time name icon body home ra mtp hua)}=split('<>',$_);
		$DT{'icon'}.='.gif'; #MTP作者ってUNISYS好きなの？
		my$data="Mir12=\t;\tname=\t$DT{'name'};\tpass=\t;\ttime=\t$DT{'time'};\tbody=\t$DT{'body'};\t";
		#親記事:子記事
		for(!@log?qw(color email home icon ra hua cmd subject):qw(color email home icon ra hua cmd)){
			$data.=qq($_=\t$DT{"$_"};\t);
		}
		push(@log,$data);
	}
	close(MTP);
	if(%DT){
		#スレッド変え
		$zer2[$DT{'i'}]=$DT{'time'};
		push(@convert,$DT{'i'});
		if(-s"$CF{'log'}$DT{'i'}.cgi"){
			push(@error,"$CF{'log'}$DT{'i'}.cgi");
		}else{
			open(LOG,">$CF{'log'}$DT{'i'}.cgi")||die"Can't write log($CF{'log'}$DT{'i'}.cgi)[$?:$!]";
			eval{flock(LOG,2)};
			print LOG join("\n",@log)."\n";
			close(LOG);
		}
		%DT=();
		@log=();
	}
	
	open(ZERO,"$CF{'log'}0.cgi")||die"Can't write log($CF{'log'}0.cgi)[$?:$!]";
	eval{flock(ZERO,1)};
	print ZERO<<"ASDF".join(' ',@zer2);;
Mir12=\t;\tsubject=\tMTP164gからコンバート成功;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

ASDF
	close(ZERO);
	
	my$from="Multi Talk PRIVATE rel 0.1.64g";
	return($from,@convert);
}


#-------------------------------------------------
# jcode.pl: Perl library for Japanese character code conversion
# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
#	ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/
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


#-------------------------------------------------
# 初期設定
BEGIN{
	getlogin||umask(0); #'nobody'って''だよね？
	# Revision Number
	$CF{'Conv'}=qq$Revision$;
	#エラーが出たらエラー画面を表示するように
	$SIG{'__DIE__'}=sub{
		print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
       :: Mireille ::
   * Error Screen 1.0 (T_T;) *

ERROR: $_[0]
$CF{'Conv'}

PerlVer	: $]
PerlPath : $^X
BaseTime : $^T
OS Name	: $^O
FileName : $0

 = = ENV = =
CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}
QUERY_STRING	: $ENV{'QUERY_STRING'}
REQUEST_METHOD: $ENV{'REQUEST_METHOD'}

SERVER_NAME: $ENV{'SERVER_NAME'}
HTTP_PATH	: $ENV{'HTTP_HOST'} $ENV{'SCRIPT_NAME'}
ENV_OS		 : $ENV{'OS'}
SERVER_SOFTWARE			: $ENV{'SERVER_SOFTWARE'}
PROCESSOR_IDENTIFIER : $ENV{'PROCESSOR_IDENTIFIER'}

+#     Airemix Mireille      #+
+#  http://www.airemix.com/  #+
_HTML_
		exit;
	};
}
1;
__END__
