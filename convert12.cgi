#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille 1.1 to 1.2 Converter -
#
 $CF{'cnvrev'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF);

require 'index.cgi';

my@zero;

#ログ拡張子
if(-e"$CF{'log'}0.cgi"){
  $CF{'logext'}='.cgi';
  sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_RDWR)||die"Can't write log$_!";
  flock(ZERO,LOCK_EX);
  (<ZERO>=~m/\tsubject=\t/)&&(die"Already 1.2!");
  while(<ZERO>){
    chomp$_;push(@zero,$_);
  }
}elsif(-e"$CF{'log'}0.pl"){
  $CF{'logext'}='.pl';
  sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write log$_!";
  flock(ZERO,LOCK_EX);

  sysopen(OLD,"$CF{'log'}0.pl",O_CREAT|O_WRONLY)||die"Can't write log$_!";
  flock(OLD,LOCK_EX);
  while(<ZERO>){
    chomp$_;push(@zero,$_);
  }
  close(OLD);
}else{
  #最初から
  sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write log$_!";
  flock(ZERO,LOCK_EX);
}

#バックアップディレクトリ
my$bckdir=$^T;
$bckdir=~s/^(.*)(\d{4})$/$2/o;
$bckdir='back'.$bckdir;
(mkdir"$CF{'log'}$bckdir",0777)||(die"Can't make Dir:$bckdir");

#ファイル一覧
my@file;
opendir(DIR,$CF{'log'});
for(readdir(DIR)){
  ('0.cgi'eq$_)&&(next);
  (($_=~/^(\d+)$CF{'logext'}$/io)&&($1))&&(push(@file,"$1"));
  rename("$CF{'log'}$_","$CF{'log'}$bckdir/$_");#Backup
}
closedir(DIR);

#変換
my@convert=();
my$convert=0;

for(@file){
  sysopen(RD,"$CF{'log'}$bckdir/$_$CF{'logext'}",O_RDONLY)||die"Can't open $_.pl.";
  flock(RD,LOCK_EX);
  my$log=join('',<RD>);
  close(RD);

  $log=~s/\ttitle=\t/\tsubject=\t/go;
  $log=~s/\tmes=\t/\tbody=\t/go;

  sysopen(WR,"$CF{'log'}$_.cgi",O_CREAT|O_WRONLY)||die"Can't write log$_!";
  flock(WR,LOCK_EX);
  print WR $log;
  close(WR);
  
  push(@convert,"$_.cgi");
  next;
}

truncate(ZERO,0);
seek(ZERO,0,0);
print<<"_DATA_";
$zero[0]
$zero[1]
$zero[2]
_DATA_
close(ZERO);


    print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<link rel="start" href="$CF{'home'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>: Mireille LogFileConverter :</title>
</head>
<body>
<h1>Mireille LogFileConverter $CF{'cnvrev'}</h1>

<h2>ログファイルの変換は完了しました</h2>


<pre style="text-align:left;width:60%">
◇今回行った処理
Mireilleのログを1.1形式から1.2形式への変換

◇処理の結果
@{[$#convert+1]}個のファイルを1.2形式に変換しました

◇変換したファイル
@convert

</pre>
</html>
_HTML_
exit;


#-------------------------------------------------
# 初期設定
BEGIN{
  # Revision Number
  $CF{'cnvrev'}=qq$Revision$;
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
$CF{'cnvrev'}
Index : $CF{'idxrev'}

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
