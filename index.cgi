#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
require 5.004;
use strict;
use vars qw(%CF %IC);
$|=1;

#-------------------------------------------------
# 稼動させる前に確認すること

#サイトの名前
$CF{'name'}='Airemix';
#サイトトップページのURL
$CF{'home'}='/';
#この掲示板のタイトル（TITLE要素）
$CF{'title'}=': Mireille :';
#この掲示板のタイトル（ページのヘッダーで表示）
$CF{'pgtitle'}='Airemix Mireille Board System';
#アイコンリスト
$CF{'icls'}='icon.txt';
#スタイルシート
$CF{'style'}='style.css';
#アイコンのディレクトリ
$CF{'icon'}='/icon/full/';
#アイコンカタログCGI
$CF{'icct'}='iconctlg.cgi';
#ヘルプファイル
$CF{'help'}='help.pl';
#記事ナビJavaScript
$CF{'navjs'}='artnavi.js';
#ログディレクトリ
$CF{'log'}='./log/';
#gzipの場所
$CF{'gzip'}='gzip';
#タイムゾーン（「JST-9」のように）
$ENV{'TZ'}='JST-9';

#-------------------------------------------------
# 必要に応じて変更

#管理者パスワード（全ての記事を編集・削除できます 25文字以上推奨）
$CF{'admps'}='';
#使用を許可するタグ（半角スペース区切り）
$CF{'tags'}='ACRONYM CODE DEL DFN EM Q SMALL STRONG RUBY RB RB RT RP';
#強調する記号と対応するCSSのクラス（半角スペース区切りで「記号 クラス 記号・・・」）
$CF{'strong'}=' // s2f2f /(/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)/ s2f2f # s2f2f ＃ s2f2f /(\s+(?:\/\/|#|＃).*)/ s2f2f /^((?:>|&#62;|&gt;|&#x3E;).*)/ s8184 ＞ s8184 ◇ s819e ◆ s819e □ s81a0 ■ s81a0 ※ s81a6';
#投稿後*****秒以内の記事にNewマークをつける
$CF{'newnc'}='86400';
#読んだ記事でも???秒間は「未読」状態を維持する
$CF{'newuc'}='600';
#投稿後*****秒以内の記事につけるNewマーク
$CF{'new'}='<SPAN class="new">New!</SPAN>';
#通常モードでの1ページあたりのスレッド数
$CF{'page'}='5';
#削除・修正モードでの1ページあたりのスレッド数
$CF{'delpg'}='10';
#最大スレッド数
$CF{'logmax'}='100';
#一スレッドあたりの最大子記事数を制限する
$CF{'maxChilds'}='100';
#検索できる項目（"項目のname 選択字の名前 "をくりかえす）
$CF{'sekitm'}='ALL 全て name 名前 email E-mail home ホーム subject 題名 body 本文';
#親記事の項目(+color +email +home +icon +ra +hua cmd +subject)
$CF{'prtitm'}='+color +email +home +icon +ra +hua cmd +subject';
#子記事の項目(+color +email +home +icon +ra +hua cmd)
$CF{'chditm'}='+color +email +home +icon +ra +hua cmd';
#Cookieの項目(color email home icon)
$CF{'cokitm'}='color email home icon';
#圧縮転送のやり方(Content-Encodingの方法)
$CF{'conenc'}='|gzip -cfq9';
#Cookieを登録するPATH(path=/ といった形で)
$CF{'ckpath'}='';
#色の選択方法 (input INPUTタグ select SELECTタグ)
$CF{'colway'}='select';
#古い記事スレッドの削除方法 (gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除)
$CF{'delold'}='gzip';
#記事スレッドの削除方法 (gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除)
$CF{'delthr'}='gzip';
#記事の並び順 (number スレッド番号順 date 投稿日時順)
$CF{'sort'}='date';
#新規投稿フォームをIndexに表示 (0 表示しない 1 表示する)
$CF{'prtwrt'}='0';
#新規/返信 があったときに指定アドレスにメールする (0 使わない 1 使う)
$CF{'mailnotify'}='0';
#掲示板を閲覧専用にする (0 読み書きOK 1 閲覧専用)
$CF{'readOnly'}='0';
#更新がないときに「304 Not Modified」を渡すか否か
$CF{'use304'}='0';
#常に「Last-Modified」を渡すか否か
$CF{'useLastModified'}='0';
#専用アイコン機能 (ON 1 OFF 0)
$CF{'exicon'}='0';
#専用アイコン列挙
#$IC{'PASSWORD'}='FILENAME'; #NAME
#$IC{'hae'}='mae.png'; #苗
#$IC{'hie'}='mie.png'; #贄
#$IC{'hue'}='mue.png'; #鵺
#$IC{'hee'}='mee.png'; #姐
#$IC{'hoe'}='moe.png'; #乃絵
#例：コマンドに"icon=hoe"と入れると乃絵さん専用の'moe.png'が使えます
#手入力するときは「$IC{'hoe'}='moe.png'; #乃絵」のように、最初の「#」を取るのを忘れずに

#-------------------------------------------------
# Mireille内のHTMLデザイン

#-----------------------------
# 色リスト
$CF{'colorList'}=<<'_CONFIG_';
<OPTION value="#FBDADE" style="color:#FBDADE">■桜色</OPTION>
<OPTION value="#D53E62" style="color:#D53E62">■薔薇色</OPTION>
<OPTION value="#FF7F8F" style="color:#FF7F8F">■珊瑚色</OPTION>
<OPTION value="#AD3140" style="color:#AD3140">■臙脂色</OPTION>
<OPTION value="#9E2236" style="color:#9E2236">■茜色</OPTION>
<OPTION value="#905D54" style="color:#905D54">■小豆色</OPTION>
<OPTION value="#EF454A" style="color:#EF454A">■朱色</OPTION>
<OPTION value="#F1BB93" style="color:#F1BB93">■肌色</OPTION>
<OPTION value="#564539" style="color:#564539">■焦茶色</OPTION>
<OPTION value="#6B3E08" style="color:#6B3E08">■褐色</OPTION>
<OPTION value="#AA7A40" style="color:#AA7A40">■琥珀色</OPTION>
<OPTION value="#F8A900" style="color:#F8A900">■山吹色</OPTION>
<OPTION value="#EDAE00" style="color:#EDAE00">■鬱金色</OPTION>
<OPTION value="#C8A65D" style="color:#C8A65D">■芥子色</OPTION>
<OPTION value="#C2BD3D" style="color:#C2BD3D">■鶸色</OPTION>
<OPTION value="#AAB300" style="color:#AAB300">■若草色</OPTION>
<OPTION value="#97A61E" style="color:#97A61E">■萌黄色</OPTION>
<OPTION value="#6DA895" style="color:#6DA895">■青磁色</OPTION>
<OPTION value="#89BDDE" style="color:#89BDDE">■空色</OPTION>
<OPTION value="#007BC3" style="color:#007BC3">■露草色</OPTION>
<OPTION value="#00519A" style="color:#00519A">■瑠璃色</OPTION>
<OPTION value="#384D98" style="color:#384D98">■群青色</OPTION>
<OPTION value="#4347A2" style="color:#4347A2">■桔梗色</OPTION>
<OPTION value="#A294C8" style="color:#A294C8">■藤色</OPTION>
<OPTION value="#714C99" style="color:#714C99">■菫色</OPTION>
<OPTION value="#744B98" style="color:#744B98">■菖蒲色</OPTION>
<OPTION value="#C573B2" style="color:#C573B2">■菖蒲色</OPTION>
<OPTION value="#EAE0D5" style="color:#EAE0D5">■香色</OPTION>
<OPTION value="#DED2BF" style="color:#DED2BF">■象牙色</OPTION>
<OPTION value="#343434" style="color:#343434">■墨</OPTION>
_CONFIG_
undef$CF{'colorList'}; #とりあえず消しとく。。
#消していることに特に意味はないので、色リストを設定したい人は上の行を削除してください

#-----------------------------
# アイコンリストのヘッダー
$CF{'iched'}=<<'_CONFIG_';

_CONFIG_

#-----------------------------
# アイコンリストのフッター
$CF{'icfot'}=<<'_CONFIG_';

_CONFIG_

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
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\n"
			."\n\n<PLAINTEXT>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\ngetlogin\t: ".getlogin;
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
	$CF{'Index'}=qq$Revision$;
	getlogin||umask(0); #nobody権限で作ったファイルをユーザが消せるように
}

1;
__END__
