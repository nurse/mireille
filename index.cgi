#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw{%CF %IC};

#-------------------------------------------------
# 稼動させる前に確認すること

#サイトの名前
$CF{'name'} = 'Airemix';
#サイトトップページのURL
$CF{'home'} = 'http://airemix.site.ne.jp/';
#この掲示板のタイトル
$CF{'title'} = ': Mireille  :';
#GZIPのPATH
$CF{'gzip'} = '/usr/bin/gzip';
#アイコンのディレクトリのURL
$CF{'icon'} = '/icon/full/';
#スタイルシート
$CF{'style'} = 'style.css';

#-------------------------------------------------
# 必要に応じて変更

#マスターパスワード（全ての記事を編集・削除できます 25文字以上推奨）
$CF{'maspas'} = '';
#使用を許可するタグ（半角スペース区切り）
$CF{'tags'} = 'DEL EM SMALL STRONG RUBY RB RB RT RP';
#＊＊秒以内の記事にNewマークをつける
$CF{'newnc'} = '86400';
#読んだ記事でも＊＊秒間は「未読」状態を維持する（投稿日時にclass="new"をつける）
$CF{'newuc'} = '600';
#一定期間内の記事につけるマーク（＊＊秒以内の記事にNewマークをつける）
$CF{'new'} = '<span class="new">New!</span>';
#通常モードの1ページあたりのスレッド数
$CF{'page'} = '5';
#削除・修正モードでの1ページあたりのスレッド数
$CF{'delpg'} = '10';
#最大スレッド数
$CF{'logmax'} = '100';
#親記事の項目(+color +email +home +icon +ra +hua cmd +subject)
$CF{'prtitm'} = '+color +email +home +icon +ra +hua cmd +subject';
#子記事の項目(+color +email +home +icon +ra +hua cmd)
$CF{'chditm'} = '+color +email +home +icon +ra +hua cmd';
#Cookieの項目(color email home icon)
$CF{'cokitm'} = 'color email home icon';
#記事スレッドの削除方法
$CF{'del'} = 'rename';
#記事の並び順
$CF{'sort'} = 'date';
#新規/返信 があったときに指定アドレスにメールする
$CF{'mailnotify'} = '0';
#新規投稿フォームをIndexに表示
$CF{'prtres'} = '';
#専用アイコン機能ON(1),OFF(0)
$CF{'exicon'}='0';
#専用アイコン列挙
#$IC{'PASSWORD'}='FILENAME'; #NAME
#"icon=moe" -> moe.png

#-------------------------------------------------
# 変更しないほうがいい

#タイムゾーン
$ENV{'TZ'}  = 'JST-9';
#システムファイル
$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = './log/'; #LOG PATH


#-------------------------------------------------
# その他

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

if($0=~m{index.cgi$}o){
  #直接実行だったら動き出す
  require './style.pl';
  require './core.cgi';
}

#-------------------------------------------------
# 初期設定
BEGIN{
  # Revision Number
  $CF{'idxrev'}=qq$Revision$;
  #エラーが出たらエラー画面を表示するように
  if($0=~m{index.cgi$}o){
    $SIG{'__DIE__'}=sub{
    print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
: Mireille :
Mireille Error Screen...

ERROR: $_[0]
Index : $CF{'idxrev'}
Style : $CF{'styrev'}
Core  : $CF{'correv'}

PerlVer  : $]
PerlPath : $^X
BaseTime : $^T
OS Name  : $^O
FileName : $0

ENV
CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}
QUERY_STRING: $ENV{'QUERY_STRING'}
REQUEST_METHOD: $ENV{'REQUEST_METHOD'}

SERVER_NAME: $ENV{'SERVER_NAME'}
HTTP: $ENV{'HTTP_HOST'} $ENV{'SCRIPT_NAME'}
OS: $ENV{'OS'}
PROCESSOR_IDENTIFIER: $ENV{'PROCESSOR_IDENTIFIER'}
SERVER_SOFTWARE: $ENV{'SERVER_SOFTWARE'}

Airemix Mireille
http://airemix.site.ne.jp/
_HTML_
    exit;
    };
  }
}
1;
__END__
