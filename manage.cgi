#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Administrative Tools -
#
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw{%AM %CF %IN %IC @file @zer2};
$|=1;

#Password
$AM{'pass'}='hoehoe';
#-------------------------------------------------
# Switch
unless(&getfm){
  &menu('NULL');
}elsif($IN{'mode'}eq'icont'){
  &icont(%IN);
}elsif($IN{'mode'}eq'icons'){
  &icons(%IN);
}elsif($IN{'mode'}eq'iconsmp'){
  &iconsmp;
}elsif($IN{'mode'}eq'config'){
  &config(%IN);
}elsif($IN{'mode'}eq'css'){
  &css(%IN);
}elsif($IN{'mode'}eq'log'){
  &log(%IN);
}elsif($IN{'mode'}eq'zero'){
  &zero(%IN);
}else{
  &menu('NG');
}
exit;

#-------------------------------------------------
# Get Form
sub getfm{
  my$i;my%DT;
  if($ENV{'REQUEST_METHOD'}eq'POST'){read(STDIN,$i,$ENV{'CONTENT_LENGTH'});}
  elsif($ENV{'REQUEST_METHOD'}eq'GET'){$i=$ENV{'QUERY_STRING'};}
  foreach(split('&',$i)){
    my($i,$j)=split('=',$_,2);
    (defined$j)||($IN{$i}="",next);
    study$j;
    $j=~tr/+/ /;
    $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    $j=~s/\x0D\x0A/\n/go;
    $j=~tr/\r/\n/; # 意味的には tr/\x0D\x0A/\n\n/;
    $DT{$i}=$j;
  }
  # Header with G-ZIP etc.
  print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja

_HTML_
  # Password Check
  ($DT{'mode'})||(return undef);
  ($DT{'pass'}eq$AM{'pass'})||(&menu('Passwordが一致しません'));
  if($DT{'mode'}eq'icont'){
    $IN{'mode'}='icont';
    $IN{'icon'}=($DT{'icon'}=~/(.+)/os)?"$1":undef;
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    $IN{'renew'}=($DT{'renew'}=~/(.)/o)?'1':undef;
    return%IN;
  }elsif($DT{'mode'}eq'icons'){
    $IN{'mode'}='icons';
    $IN{'icon'}=($DT{'icon'}=~/(.+)/os)?"$1":undef;
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    $IN{'renew'}=($DT{'renew'}=~/(.)/o)?'1':undef;
    return%IN;
  }elsif($DT{'mode'}eq'iconsmp'){
    $IN{'mode'}='iconsmp';
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    return%IN;
  }elsif($DT{'mode'}eq'config'){
    while(my($i,$j)=each%DT){
      $IN{"$i"}=($j=~/(.*)/os)?"$1":undef;
    }
    $IN{'mode'}='config';
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    return%IN;
  }elsif($DT{'mode'}eq'css'){
    $IN{'mode'}='css';
    $IN{'css'}=($DT{'css'}=~/(.+)/os)?"$1":undef;
    $IN{'file'}=($DT{'file'}=~/(\w+)/o)?"$1":undef;
    $IN{'code'}=($DT{'code'}=~/(\w+)/o)?"$1":undef;
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    return%IN;
  }elsif($DT{'mode'}eq'log'){#LOG
    $IN{'mode'}='log';
    $IN{'str'}=($DT{'str'}=~/(\d+)/o)?$1:0;
    $IN{'end'}=($DT{'end'}=~/(\d+)/o)?$1:0;
    $IN{'del'}=($DT{'del'}=~/(\w)/o)?"$1":undef;
    $IN{'save'}=($DT{'save'}=~/(\d+)/o)?$1:0;
    $IN{'push'}=($DT{'push'}=~/(\d)/o)?"$1":'';
    $IN{'type'}=($DT{'type'}=~/(\w)/o)?"$1":undef;
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    return%IN;
  }elsif($DT{'mode'}eq'zero'){#Zero
    $IN{'mode'}='zero';
    $IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":undef;
    $IN{'recover'}=($DT{'recover'}=~/(.)/o)?'1':undef;
    return%IN;
  }
  exit;
}

#-------------------------------------------------
# Menu
sub menu{
  print<<"ASDF";
$AM{'head'}<h2 class="mode" style="margin:1em">[ $_[0] ]</h2>
<form accept-charset="euc-jp" name="menu" method="post" action="$AM{'manage'}">
<fieldset style="text-align:left;padding:0.5em;width:15em">
<legend>Mode</legend>
<label accesskey="y" for="icont">
<input name="mode" class="radio" id="icont" type="radio" value="icont">
Iconリスト編集（タグ）(<span class="ak">Y</span>)</label>
<br>
<label accesskey="u" for="icons">
<input name="mode" class="radio" id="icons" type="radio" value="icons">
Iconリスト編集(Sharp）(<span class="ak">U</span>)</label>
<br>
<label accesskey="i" for="iconsmp">
<input name="mode" class="radio" id="iconsmp" type="radio" value="iconsmp" checked>
<span class="ak">I</span>con見本を更新</label>
<br>
<label accesskey="g" for="config">
<input name="mode" class="radio" id="config" type="radio" value="config">
<del>Config編集</del>(<span class="ak">G</span>)</label>
<br>
<label accesskey="b" for="css">
<input name="mode" class="radio" id="css" type="radio" value="css">
外部CSS編集(<span class="ak">B</span>)</label>
<br>
<label accesskey="l" for="log">
<input name="mode" class="radio" id="log" type="radio" value="log">
<span class="ak">L</span>OG管理・削除</label>
<br>
<label accesskey="z" for="zero">
<input name="mode" class="radio" id="zero" type="radio" value="zero">
<span class="ak">Z</span>eroファイル復旧</label>
</fieldset>
<p><label accesskey="p" for="pass"><span class="ak">P</span>assword:
<input name="pass" id="pass" type="password" size="12" value="$IN{'pass'}"></label></p>
<p><input type="submit" accesskey="s" class="submit" value="OK">
<input type="reset" class="reset" value="キャンセル"></p>
$AM{'foot'}
ASDF
  exit;
}

#-------------------------------------------------
# IconTag
sub icont{
  my(%DT)=@_;
  &loadcfg;
  unless($DT{'icon'}){#アイコンリスト編集
    sysopen(RD,"$CF{'icls'}",O_RDONLY)||die"Can't open iconlist.";
    flock(RD,LOCK_SH);
    my$icon=join('',<RD>);
    close(RD);
    $icon=~s/\t/\ \ /go;
    $icon=~s/[\x0D\x0A]*$//o;
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">アイコンリスト編集モード</h2>
<form accept-charset="euc-jp" name="iconedit" method="post" action="$AM{'manage'}">
<p><textarea name="icon" cols="100" rows="15">$icon</textarea></p>
<p><label accesskey="r" for="renew">アイコン見本更新(<span class="ak">R</span>):
<input name="renew" id="renew" type="checkbox" value="renew" checked></label></p>
<input name="mode" type="hidden" value="icont">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
  exit;
  }else{#アイコンリスト書き込み Tag
    study$DT{'icon'};
    $DT{'icon'}=~tr/\n//s;
    $DT{'icon'}=~s/(\n)*$/\n/;

    sysopen(WR,"$CF{'icls'}",O_CREAT|O_WRONLY|O_TRUNC)||die"Can't write icli.";
    flock(WR,LOCK_EX);
    print WR $DT{'icon'};
    close(WR);

    unless($DT{'renew'}){
      &menu('アイコンリスト書き込み完了');
    }else{
      &iconsmp;
      &menu('アイコンリスト・見本書き込み完了');
    }
  }
  exit;
}

#-------------------------------------------------
# IconSharp
sub icons{
  my(%DT)=@_;
  &loadcfg;
  unless($DT{'icon'}){
    #アイコンリストSharp編集画面
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">アイコンリスト編集モード</h2>
<form accept-charset="euc-jp" name="iconedit" method="post" action="$AM{'manage'}">
<p><textarea name="icon" cols="100" rows="15">
ASDF
    
    sysopen(RD,"$CF{'icls'}",O_RDONLY)||die"Can't open iconlist.";
    flock(RD,LOCK_SH);
    my@icon=<RD>;
    close(RD);
    
    my$optg=0;
    
    for(@icon){
      
      if($_=~m{^\s*<option ([^>]*)value=([\"\'])([^\2]*)\2([^>]*)>([^<]*)(</option>)?$}io){
        if($optg==1){print"  ";}
        elsif($optg==2){print"#\n";$optg=0;}
        print"$3#$5\n";
        next;
      }elsif($_=~m{^<optgroup (.*)label=[\"\']([^\"\']*)[\"\'](.*)>$}io){
        ($2)||($optg=0);
        $optg=1;
        print"#$2\n";
        next;
      }elsif($_=~m{^</optgroup>}io){
        print"#\n";
        $optg=2;
        next;
      }else{
        print"$_";
      }
    }
    
    print<<"ASDF";
</textarea></p>
<p><label accesskey="r" for="renew">アイコン見本更新(<span class="ak">R</span>):
<input name="renew" id="renew" type="checkbox" value="renew" checked></label></p>
<input name="mode" type="hidden" value="icons">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
    
    exit;
  }else{
    #アイコンリスト書き込み
#    study$DT{'icon'};
    $DT{'icon'}=~tr/\n//s;
#    $DT{'icon'}=~s/&/&#38;/go;
#    $DT{'icon'}=~s/"/&#34;/go;
#    $DT{'icon'}=~s/'/&#39;/go;
#    $DT{'icon'}=~s/</&#60;/go;
#    $DT{'icon'}=~s/>/&#62;/go;
    my@icon=split("\n","$DT{'icon'}");
    
=icon Sharp
 GroupName
^\s*\#\s*(.*)$
 IconName
^\s*([^#])\s*#\s*(.*)$
=cut
    
    sysopen(OUT,"$CF{'icls'}",O_CREAT|O_WRONLY|O_TRUNC)||die"Can't write icli.";
    flock(OUT,LOCK_EX);
    my$optg=0;
    for(@icon){
      if($_=~m/^\s*\#\s*(.*)$/o){
        #アイコングループ
        ($optg==1)&&(print OUT "</optgroup>\n");
        ($1)||($optg=0,next);
        print OUT qq[<optgroup label="$1">\n];
        $optg=1;
        next;
      }elsif($_=~m/^\s*([^#]*)\s*\#\s*(.*)$/o){
        #アイコン項目
        ($optg==1)&&(print OUT "  ");
        print OUT qq[<option value="$1">$2</option>\n];
        next;
      }else{
        print OUT "$_\n";
      }
    }
    ($optg==1)&&(print OUT "</optgroup>\n");
    close(OUT);
    
    unless($DT{'renew'}){
      &menu('アイコンリスト書き込み完了');
    }else{
      &iconsmp;
      &menu('アイコンリスト・見本書き込み完了');
    }
    exit;
  }
}

#-------------------------------------------------
# Icon見本更新
sub iconsmp{
  &loadcfg;
  sysopen(RD,"$CF{'icls'}",O_RDONLY)||die"Can't open iconlist.";
  flock(RD,LOCK_SH);
  my@icon=<RD>;
  close(RD);
  
  #OPTGROUP要素
  #^<optgroup (.*)label=[\"\']([^\"\']*)[\"\'](.*)>$
  #<table $1summary="$2"$3>
  #{^</optgroup>$}{</tr></table>}
  #OPTION要素
  #^\s*<option (.*)value=[\"\']([^\"\']*)[\"\'](.*)>(.*)(</option>)?$
  #<td><img $1src="$CF{'icon'}$2" alt=\"$1\"$3><br>$1</td>
  sysopen(OUT,'icon.html',O_CREAT|O_WRONLY|O_TRUNC)||die"Can't write samp.";
  flock(OUT,2);
  print OUT <<"_HTML_";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<link rel="start" href="$CF{'home'}">
<link rel="index" href="index.cgi">
<link rel="help" href="help.html">
<title>: Mireille Icon List :</title>
</head>
<body style="margin-top:1em">
_HTML_
  print OUT $CF{'pghead'};
  eval qq{print OUT <<"_HTML_";\n$CF{'menu'}\n_HTML_};
  print OUT qq[<h2 class="mode">アイコン見本</h2>\n$CF{'iched'}];

  my$i='0';
  my$j='0';
  my@others=();
  $AM{'x'}='6';
  my%CR;
  for(@icon){
    if($_=~/option/io){#<option value=".*">.*</option>
      $j++;
      if($i){
        if($j){#<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
          {<td><img $1src="$CF{'icon'}$3" alt=\"$5\"$4><br>$5</td>}imo;
          ($j>($AM{'x'}-2))&&($j='-1');
        }elsif($i=='2'){#</tr>+<tr>+<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
          {</tr><tr>\n<td><img $1src="$CF{'icon'}$3" alt=\"$5\"$4><br>$5</td>}io;
        }elsif($i=='1'){#<tr>+<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
           {<tr>\n<td><img $1src="$CF{'icon'}$3" alt=\"$5\"$4><br>$5</td>}io;
          $i='2';
        }
      }else{#<option>
        push(@others,$_);
        next;
      }
      print OUT $_;next;
    }elsif($_=~/<optgroup/io){#<optgroup label=".*">
      $_=~s{^<optgroup (.*)label=[\"\']([^\"\']*)[\"\'](.*)>$}
      {<table $1cellspacing="0" class="icon" summary="$2"$3>\n<caption>$2</caption>}io;
      $_.=qq{<col span="$AM{'x'}" width="110">};
      $i='1';$j='-1';print OUT $_;next;
    }elsif($_=~/optgroup/io){#</optgroup>
      if($CR{'VENDOR_Link'}&&$CR{'COPY1_Link'}){
        $_=<<"_HTML_";
</tr>
<tr><th colspan="$AM{'x'}">&#169;$CR{'COPY1_Link'} &gt;&gt; by$CR{'VENDOR_Link'}</th></tr>
</table>

_HTML_
      }elsif($CR{'VENDOR_Link'}){
        $_=<<"_HTML_";
</tr>
<tr><th colspan="$AM{'x'}" class="foot">by$CR{'VENDOR_Link'}</th></tr>
</table>

_HTML_
      }elsif($CR{'COPY1_Link'}){
        $_=<<"_HTML_";
</tr>
<tr><th colspan="$AM{'x'}" class="foot">&#169;$CR{'COPY1_Link'}</th></tr>
</table>

_HTML_
      }
      $i='0';print OUT $_;next;
    }elsif($_=~m/<!-- %([^>]+) -->/o){
      if('BEGIN_VENDOR'eq$1){
        $CR{'VENDOR'}='';$CR{'VENDOR_URL'}='';$CR{'VENDOR_Link'}='';
        next;
      }elsif($1=~m/^VENDOR(\w*) (.+)/o){
        if(''eq$1){
          $CR{'VENDOR'}="$2";
        }elsif('_URL'eq$1){
          $CR{'VENDOR_URL'}="$2";
        }elsif('_Link'eq$1){
          $CR{'VENDOR_Link'}="$2";
          next;
        }
        $CR{'VENDOR_Link'}=qq[<a href="$CR{'VENDOR_URL'}" title="製作者">$CR{'VENDOR'}</a>];
        next;
      }elsif('END_VENDOR'eq$1){
        $CR{'VENDOR'}='';$CR{'VENDOR_URL'}='';$CR{'VENDOR_Link'}='';
        next;
      }elsif('BEGIN_COPY1'eq$1){
        $CR{'COPY1'}='';$CR{'COPY1_URL'}='';$CR{'COPY1_Link'}='';
        next;
      }elsif($1=~m/^COPY1(\w*) (.+)/o){
        if(''eq$1){
          $CR{'COPY1'}="$2";
        }elsif('_URL'eq$1){
          $CR{'COPY1_URL'}="$2";
        }elsif('_Link'eq$1){
          $CR{'COPY1_Link'}="$2";
          next;
        }
        $CR{'COPY1_Link'}=qq[<a href="$CR{'COPY1_URL'}" title="一次著作権者">$CR{'COPY1'}</a>];
        next;
      }elsif('END_COPY1'eq$1){
        $CR{'COPY1'}='';$CR{'COPY1_URL'}='';$CR{'COPY1_Link'}='';
        next;
      }
    }
  }
  ($i)&&(print OUT qq{</tr></table>\n});
  if($#others>-1){
    print OUT <<"_HTML_";
<table cellspacing="0" class="icon" summary="Others">
<caption>その他</caption>
<col span="$AM{'x'}" width="110">
_HTML_
    
    my$i='1';
    my$j='-1';
    for(@others){
      $j++;
        if($j){#<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
          {<td><img $1src="$CF{'icon'}$3" alt="$5"$4><br>$5</td>}imo;
          ($j>($AM{'x'}-2))&&($j='-1');
        }elsif($i=='2'){#</tr>+<tr>+<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
          {</tr><tr>\n<td><img $1src="$CF{'icon'}$3" alt="$5"$4><br>$5</td>}io;
        }elsif($i=='1'){#<tr>+<td>
          $_=~s{^\s*<option (.*)value=([\"\'])([^\"\']*)\2([^>]*)>([^<]*)(</option>)?$}
           {<tr>\n<td><img $1src="$CF{'icon'}$3" alt="$5"$4><br>$5</td>}io;
          $i='2';
        }
      print OUT $_;next;
    }
    print OUT qq{</tr></table>\n\n};
  }
  print OUT $CF{'icfot'};
  print OUT $CF{'pgfoot'};
  print OUT <<"_HTML_";
<div class="AiremixCopy">- <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</a>
<var>$main::version</var> -</div>
</body>
</html>
_HTML_
  close(OUT);

  &menu('アイコン見本更新完了');
}

#-------------------------------------------------
# Config Editor
sub config{
  my(%DT)=@_;
my@required=(
 'name'  =>'サイトの名前'
,'home'  =>'サイトトップページのURL'
,'title' =>'この掲示板のタイトル'
,'gzip'  =>'GZIPのPATH'
,'icon'  =>'アイコンのディレクトリのURL'
,'style' =>'スタイルシート'
);
    my@implied=(
 'admps'=>'管理者パスワード（全ての記事を編集・削除できます 15-30文字推奨）'
,'tags'  =>'使用を許可するタグ（半角スペース区切り）'
,'newnc' =>'＊＊秒以内の記事にNewマークをつける'
,'newuc' =>'読んだ記事でも＊＊秒間は「未読」状態を維持する（投稿日時にclass="new"をつける）'
,'new'   =>'一定期間内の記事につけるマーク（＊＊秒以内の記事にNewマークをつける）'
,'page'  =>'通常モードの1ページあたりのスレッド数'
,'delpg' =>'削除・修正モードでの1ページあたりのスレッド数'
,'logmax'=>'最大スレッド数'
,'prtitm'=>'親記事の項目(+color +email +home +icon +ra +hua cmd +title)'
,'chditm'=>'子記事の項目(+color +email +home +icon +ra +hua cmd)'
,'cokitm'=>'Cookieの項目(color email home icon)'
);
    my@select=(
 'del'   =>'記事スレッドの削除方法','rename ファイル名変更 unlink ファイル削除'
,'sort'  =>'記事の並び順','number 記事番号順 date 投稿日時順'
,'mailnotify'=>'新規/返信 があったときに指定アドレスにメールする','0 使わない 1 使う'
,'prtwrt'=>'新規投稿フォームをIndexに表示','0 表示しない 1 表示する'
);
    my@design=(
 'menu'  =>'Mireile Menu'
,'head'  =>'Page Header'
,'note'  =>'注意書き（TOPページのメニューの下に表示されます）'
,'foot'  =>'Page Footer'
,'artprt'=>'親記事'
,'artchd'=>'子記事'
,'artfot'=>'記事のフッター'
,'wrtfm' =>'新規投稿/編集フォーム'
,'resfm' =>'返信フォーム'
,'iched' =>'アイコンリストのヘッダー'
,'icfot' =>'アイコンリストのフッター'
);
  unless($DT{'name'}){
    my$message='';
    unless(&loadcfg){
      $message=<<'_HTML_';
<h2>configの読み込みでエラーが発生しました</h2>
<p>configが破損している可能性があります<br>
このまま実行すれば、configを上書きして設定しなおせます</p>
_HTML_
    }
    for(%CF){
      $CF{"$_"}=~s/\t/  /go;
      $CF{"$_"}=~s/&/&#38;/go;
      $CF{"$_"}=~s/"/&#34;/go;
      $CF{"$_"}=~s/'/&#39;/go;
      $CF{"$_"}=~s/</&#60;/go;
      $CF{"$_"}=~s/>/&#62;/go;
    }
    (defined$CF{'prtitm'})||($CF{'prtitm'}='+color +email +home +icon +ra +hua cmd +title');
    (defined$CF{'chditm'})||($CF{'chditm'}='+color +email +home +icon +ra +hua cmd');
    (defined$CF{'cokitm'})||($CF{'cokitm'}='color email home icon');



    print<<"ASDF";
$AM{'head'}

$message<form accept-charset="euc-jp" name="cssedit" method="post" action="$AM{'manage'}">
<table style="margin:1em">
<caption>CONFIG編集</caption>
<col style="text-align:left;width:600px"><col style="text-align:left;width:200px">

<tbody>
<tr><th class="cfghead" colspan="2">稼動させる前に確認すること</th></tr>
ASDF

    my$i=0;
    #稼動させる前に確認すること
    for($i=0;$i<$#required;$i+=2){
      print<<"ASDF";
<tr>
<th class="item">$required[$i+1]：</th>
<td><input name="$required[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$required[$i]"}"></td>
</tr>
ASDF
    }

    print<<"ASDF";
</tbody>

<tbody>
<tr><th class="cfghead" colspan="2">必要に応じて変更</th></tr>
ASDF
    #必要に応じて変更
    for($i=0;$i<$#implied;$i+=2){
      print<<"ASDF";
<tr>
<th class="item">$implied[$i+1]：</th>
<td><input name="$implied[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$implied[$i]"}"></td>
</tr>
ASDF
    }

    #選択型
    for($i=0;$i<$#select;$i+=3){
      print<<"ASDF";
<tr>
<th class="item">$select[$i+1]：</th>
<td>
<select name="$select[$i]">
ASDF
      my$name=$select[$i+2];
      my@label=split(/ /o,$select[$i+2]);
      for(my$j=0;$j<$#label;$j+=2){
        if($label[$j]eq$CF{$select[$i]}){
          print<<"ASDF";
<option value="$label[$j]" selected="selected">$label[$j+1]</option>
ASDF
        }else{
          print<<"ASDF";
<option value="$label[$j]">$label[$j+1]</option>
ASDF
        }
      }
    print<<"ASDF";
</select>
</td>
</tr>
ASDF
    }
    print<<"ASDF";
</tbody>

<tbody>
<tr><th class="cfghead" colspan="2">専用アイコン</th></tr>
<tr>
<th class="item">専用アイコン機能：</td>
ASDF
    $i=<<"ASDF";
<td>
<label for="exiconon">使う<input id="exiconon" name="exicon" type="radio" value="1"
checked></label>
<label for="exiconof">使わない<input id="exiconof" name="exicon" type="radio" value="0"></label>
</td>
</tr>
<tr>
ASDF
    $i=~s/(value=\"$CF{'exicon'}\")/$1 checked="checked"/o;
    print$i;
    my@IC=keys%IC;
    for(0..$#IC){
      print<<"ASDF";
<tr>
<th class="item">パスワード：<input name="ICN$_" type="text" style="ime-mode:disabled" value="$IC[$_]"></td>
<td>ファイル名：<input name="ICV$_" type="text" style="ime-mode:disabled" value="$IC{$IC[$_]}"></td>
</tr>
ASDF
    }

    for(($#IC+1)..($#IC+5)){
      print<<"ASDF";
<tr>
<th class="item">パスワード：<input name="ICN$_" type="text" style="ime-mode:disabled" value=""></td>
<td>ファイル名：<input name="ICV$_" type="text" style="ime-mode:disabled" value=""></td>
</tr>
ASDF
    }
  
    print<<"ASDF";
<tr><th class="cfghead" colspan="2">変更しないほうがいい</td></tr>
<tr>
<th class="item">タイムゾーン：</td>
<td><input name="TZ" type="text" style="ime-mode:disabled" value="$ENV{'TZ'}"></td>
</tr>
<tr>
<th class="item">index：</td>
<td><input name="index" type="text" style="ime-mode:disabled" value="index.cgi"></td>
</tr>
</tr>
<tr>
<th class="item">help：</td>
<td><input name="help" type="text" style="ime-mode:disabled" value="help.html"></td>
</tr>
</tr>
<tr>
<th class="item">log：</td>
<td><input name="log" type="text" style="ime-mode:disabled" value="$CF{'log'}"></td>
</tr>

<tr><th class="cfghead" colspan="2">Mireille内のHTMLデザイン</td></tr>
ASDF
    #Mireille内のHTMLデザイン
    for($i=0;$i<$#design;$i+=2){
      print<<"ASDF";
<tr><th class="item" colspan="2">$design[$i+1]：</th></tr>
<tr><td colspan="2"><textarea name="$design[$i]" cols="130" rows="7" style="ime-mode:inactive;width:800px">$CF{$design[$i]}</textarea></td></tr>
ASDF
    }
    print<<"ASDF";
</table>
<p>
<input name="mode" type="hidden" value="config">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
  }else{
    for(keys%DT){
      $DT{"$_"}=~s/(\n)*$//;
    }
    
    #危険な文字を回避
    $DT{'menu'}  =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'head'}  =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'note'}  =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'foot'}  =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'artprt'}=~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'artchd'}=~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'artfot'}=~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'wrtfm'} =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    $DT{'resfm'} =~s/^_CONFIG_$/(_CONFIG_)/gmo;
    
    my$config=<<"ASDF";
#------------------------------------------------------------------------------#
# 'Mireille' Config
#
\$CF{'cfgver'}=\'$main::version\';
# "This Script is written in euc-jp." 空
#------------------------------------------------------------------------------#
use strict;
use vars qw{\%CF \%IC};
#-------------------------------------------------
# 稼動させる前に確認すること

ASDF
    my$i=0;
    for($i=0;$i<$#required;$i+=2){
      $config.=<<"ASDF";
#$required[$i+1]
\$CF{\'$required[$i]\'} = \'$DT{"$required[$i]"}\';
ASDF
    }
    $config.=<<"ASDF";

#-------------------------------------------------
# 必要に応じて変更

ASDF
    for($i=0;$i<$#implied;$i+=2){
      $config.=<<"ASDF";
#$implied[$i+1]
\$CF{\'$implied[$i]\'} = \'$DT{"$implied[$i]"}\';
ASDF
    }
    for($i=0;$i<$#select;$i+=3){
      $config.=<<"ASDF";
#$select[$i+1]
\$CF{\'$select[$i]\'} = \'$DT{"$select[$i]"}\';
ASDF
    }
    $config.=<<"ASDF";
#専用アイコン機能ON(1),OFF(0)
\$CF{'exicon'}=\'$DT{'exicon'}\';
#専用アイコン列挙
#\$IC{'PASSWORD'}='FILENAME'; #NAME
#"icon=moe" -> moe.png
ASDF
    for(my$i=0;defined$DT{"ICN$i"};$i++){
      ($DT{"ICN$i"}&&$DT{"ICV$i"})||(next);
      $config.=qq{\$IC{\'$DT{"ICN$i"}\'}=\'$DT{"ICV$i"}\';\n};
    }
    $config.=<<"ASDF";

#-------------------------------------------------
# 変更しないほうがいい

#タイムゾーン
\$ENV{'TZ'}  = \'$DT{'TZ'}\';
#システムファイル
\$CF{'log'}  = \'$DT{'log'}\'; #LOG PATH

#-------------------------------------------------
# Mireille内のHTMLデザイン

ASDF
    for($i=0;$i<$#design;$i+=2){
      $config.=<<"ASDF";
#-----------------------------
# $design[$i+1]
\$CF{\'$design[$i]\'}=<<'_CONFIG_';
$DT{$design[$i]}
_CONFIG_

ASDF
    }
    $config.=<<"ASDF";
1;
__END__
ASDF
    sysopen(OUT,"config$CF{'cfgext'}",O_CREAT|O_WRONLY|O_TRUNC)||die"Can't write config.";
    flock(OUT,2);
    print OUT $config;
    close(OUT);
    
    &menu('configに書き込み完了');
  }
  exit;
}

#-------------------------------------------------
# CSS Editor
sub css{
  my(%DT)=@_;
  unless($DT{'file'}){
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">スタイルシートファイル選択</h2>
<form accept-charset="euc-jp" name="cssedit" method="post" action="$AM{'manage'}">
<p>CSSファイル名<input name="file" type="text" style="ime-mode:disabled" value="$IN{'file'}">（拡張子は入力しない）<br>
例：$CF{'style'}なら、styleとだけ入力する<br>
万が一のセキュリティ確保のためですので、あしからず</p>
<p>
<input name="mode" type="hidden" value="css">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
  }elsif(!$DT{'css'}){
    open(IN,"$DT{'file'}\.css")||die qq{Can not open "$DT{'file'}.css".};
    flock(IN,1);
    my$css=join('',<IN>);
    close(IN);
    
    study$css;
    $css=~/\@charset\s*[\"\']([\-\w]*)[\"\']/io;
    $DT{'code'}=$1;
    ($DT{'code'}=~/Shift_JIS/io)&&($css=jcode::euc($css));
    $css=~s/\t/  /go;
    $css=~s/&/&#38;/go;
    $css=~s/"/&#34;/go;
    $css=~s/'/&#39;/go;
    $css=~s/</&#60;/go;
    $css=~s/>/&#62;/go;
    
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">スタイルシート編集モード</h2>
<form accept-charset="euc-jp" name="cssedit" method="post" action="$AM{'manage'}">
<p>CSSファイル名:$IN{'file'}.css<input name="file" type="hidden" value="$IN{'file'}"><p>
<p><textarea name="css" cols="100" rows="15">$css</textarea><p>
<p>
<input name="code" type="hidden" value="$DT{'code'}">
<input name="mode" type="hidden" value="css">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
  }else{
    $DT{'css'}=~s/(\n)*$/\n/o;
    if($DT{'code'}=~/Shift_JIS/i){
      $DT{'css'}=jcode::sjis($DT{'css'});
    }
    sysopen(OUT,"$DT{'file'}\.css",O_CREAT|O_WRONLY|O_TRUNC)||die qq{Can not write "$DT{'file'}.css".};
    flock(OUT,2);
    print OUT $DT{'css'};
    close(OUT);
    
    &menu('css書き込み完了');
  }
  exit;
}

#-------------------------------------------------
# LOG Editor
sub log{
  my(%DT)=@_;
  unless($DT{'type'}){
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">ログ管理モード</h2>
<form accept-charset="euc-jp" name="logedit" method="post" action="$AM{'manage'}">


<fieldset style="padding:0.5em;width:60%">
<legend>バックアップ削除</legend>
<label for="back"><input name="type" id="back" type="radio" value="3" checked="checked">
バックアップファイルを削除する</label>
<pre style="text-align:center">ファイル名変更型削除のときにできたバックアップファイルを一掃します
具体的にはログディレクトリ内のすべての拡張子.bakのファイルを削除します
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:60%">
<legend>記事スレッドを削除</legend>
<fieldset style="padding:0.5em;width:90%">
<legend>□〜□型指定</legend>
<input name="type" type="radio" value="1">
<input name="str" type="text" size="3" style="ime-mode:disabled" value="">
〜
<input name="end" type="text" size="3" style="ime-mode:disabled" value="">
<pre style="text-align:center">記事番号□〜□まで削除します
前の□に何も入れなかった場合は、0〜□を削除し、
後の□に何も入れなかった場合は、□から最新を残してそれより昔のものをを削除します
かなり危険なコマンドでもあるので、必ず実行前にバックアップをとるようにしましょう
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:90%">
<legend>1〜(最新-□)型指定</legend>
<input name="type" type="radio" value="2">
<input name="save" type="text" size="3" style="ime-mode:disabled" value="">
<pre style="text-align:center">最新から□個残して、それ以外を削除します
ここでいう「最新」とは記事番号の最も大きい物、のことです
必ず実行前にバックアップをとるようにしましょう
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:50%">
<legend>削除方式</legend>
<label for="rename">ファイル名変更：<input name="del" id="rename" type="radio" value="rename" checked></label>
<label for="unlink">ファイル削除：<input name="del" id="unlink" type="radio" value="unlink"></label>
</fieldset>

<p><label for="push"><input id="push" name="push" type="checkbox" value="1">記事番号をつめる</label>
<br>記事番号を１から順番に変更します</p>
</fieldset>

<p><input name="mode" type="hidden" value="log">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
</form>
$AM{'foot'}
ASDF
  }elsif($DT{'type'}=~/^\d$/){
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">ログ管理モード</h2>
<form accept-charset="euc-jp" name="logedit" method="post" action="$AM{'manage'}">
ASDF
    if($DT{'type'}==1){
      ($DT{'str'})||($DT{'str'}=1);
      ($DT{'end'})||($DT{'end'}=$DT{'str'},$DT{'str'}=1);
      print<<"ASDF";
<p>本当に、
<input name="str" type="text" size="3" value="$DT{'str'}" readonly>から
<input name="end" type="text" size="3" value="$DT{'end'}" readonly>を削除してよろしいですか？
<input name="type" type="hidden" value="a">
<input name="del" type="hidden" value="$DT{'del'}">
</p>
ASDF
      if($DT{'del'}eq'unlink'){
        print"<p>ファイル削除</p>";
      }else{
        print"<p>ファイル名変更/p>";
      }
    }elsif($DT{'type'}==2){
      &loadcfg;
      my@file;
      opendir(DIR,$CF{'log'});
      for(readdir(DIR)){
        (($_=~/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
      }
      closedir(DIR);
      @file=sort{$b<=>$a}@file;
      my$i=$#file-$DT{'save'}+1;
      print<<"ASDF";
<p>本当に、最新から
<input name="save" type="text" size="3" value="$DT{'save'}" readonly>個残して
削除してよろしいですか？<input name="type" type="hidden" value="b"><br>
記事番号$file[$#file]から$file[$DT{'save'}]までの、$i件を削除します
<input name="del" type="hidden" value="$DT{'del'}">
</p>
ASDF
      if($DT{'del'}eq'unlink'){
        print"<p>ファイル削除</p>";
      }else{
        print"<p>ファイル名変更/p>";
      }
    }elsif($DT{'type'}==3){
        print<<"ASDF";
<p>本当に、バックアップファイルを一掃してよろしいですか？</p>
<input name="type" type="hidden" value="c">
ASDF
    }else{
      exit;
    }
    
    print<<"ASDF";
<br>
<p><a href="$AM{'manage'}" title="管理">間違えたので最初からやり直す</a></p>
<br>
<p>
<input name="mode" type="hidden" value="log">
<input name="pass" type="hidden" value="$IN{'pass'}">
ログ詰め: <input name="push" type="text" size="3" value="$DT{'push'}" readonly></p>
<p><input type="submit" accesskey="s" class="submit" value="OK"></p>
</form>
$AM{'foot'}
ASDF
  }elsif($DT{'type'}=~/^\w$/){
    &loadcfg;
    if($DT{'type'}eq'a'){
      ($DT{'str'})||($DT{'str'}=1);
      ($DT{'end'})||($DT{'end'}=$DT{'str'},$DT{'str'}=1);
    }elsif($DT{'type'}eq'b'){
      my@file;
      opendir(DIR,$CF{'log'});
      for(readdir(DIR)){
        (($_=~/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
      }
      closedir(DIR);
      @file=sort{$b<=>$a}@file;#(4,3,2,1)
      $DT{'str'}=$file[$#file];
      $DT{'end'}=$file[$DT{'save'}];
    }elsif($DT{'type'}eq'c'){
      my$file=unlink<$CF{'log'}*.bak>;
      $file.=unlink<$CF{'log'}*.bak.cgi>;
      $file.=unlink<$CF{'log'}*.bak.pl>;
      &menu("$file個のバックアップファイルを削除しました");
    }else{
      exit;
    }

    my$file=0;
    if($DT{'del'}eq'unlink'){
      for($DT{'str'}..$DT{'end'}){
        (unlink"$CF{'log'}$_.cgi")||(next);
        $file++;
      }
    }else{
      for($DT{'str'}..$DT{'end'}){
        (rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi"))||(next);
        $file++;
      }
    }
    
    if($DT{'push'}){
      my@file;
      opendir(DIR,$CF{'log'});
      for(readdir(DIR)){
        (($_=~m/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
      }
      closedir(DIR);
      @file=sort{$a<=>$b}@file;#(1,2,3,4)
      
      sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_RDWR)||die"Can't write log0";
      flock(ZERO,LOCK_EX);
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
        rename("$CF{'log'}$_.cgi","$CF{'log'}$i.cgi");
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
      
      &menu("ログ$DT{'str'}〜$DT{'end'}のファイル$file個を削除完了<br>ログ詰め成功");
    }
    
    &menu("ログ$DT{'str'}〜$DT{'end'}のファイル$file個を削除完了");
  }
  
  exit;
}

#-------------------------------------------------
# ZeroFileRecovery
sub zero{
  my(%DT)=@_;
  unless($DT{'recover'}){
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">ZeroFile回復モード</h2>
<form accept-charset="euc-jp" name="zero" method="post" action="$AM{'manage'}">
<p>ZeroFileをリカバリすると、既存の情報は失われます<br>
それでもよろしいですか？
<input name="mode" type="hidden" value="zero">
<input name="pass" type="hidden" value="$IN{'pass'}"></p>
<p><label accesskey="r" for="recover">回復する
<input name="recover" id="recover" type="checkbox" value="1"></label></p>
<p><input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
    exit;
  }else{
    &loadcfg;

    my@file=();
    my@zer2=();	
    
    opendir(DIR,$CF{'log'});
    for(readdir(DIR)){
      (($_=~/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
    }
    closedir(DIR);
    #記事番号順 'number'
    @file=sort{$b<=>$a}@file;
    
    for(@file){
      $zer2[$_-$file[$#file]]=(stat("$CF{'log'}$_.cgi"))[9];
    }
    
    unshift(@zer2,$file[$#file]-1);
    
    sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write 0.cgi.";
    print ZERO <<"ASDF";
Mir1=\t;\ttitle=\tZeroFileを回復しました;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

@zer2
ASDF
    close(ZERO);
    &menu("ZeroFile回復完了");
  }
  exit;
}


#-------------------------------------------------
# config読み込み
#
sub loadcfg{
#  if(-e'./config.cgi'){
#    $CF{'cfgext'}='.cgi';
#    eval"do'./config.cgi'";
#  }elsif(-e'./config.pl'){
#    $CF{'cfgext'}='.pl';
#    eval"do'./config.pl'";
#  }else{
     eval"do'./index.cgi'";
     eval"do'./style.pl'";
#  }
}

#------------------------------------------------------------------------------#
# BEGIN

BEGIN{
  $CF{'mngrev'}=q$Revision$;
  $CF{'style'} = 'style.css';
  $ENV{'SCRIPT_NAME'}=~m{/([^/]+)$}o;
  $AM{'manage'}=$1;
  $AM{'head'}=<<"_HTML_";
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
<link rel="stylesheet" href="$CF{'style'}" media="screen" type="text/css">
<style type="text/css" media="screen">
<!--
th.cfghead{
  background-color:#cdf;
  color:#05a;
}
-->
</style>
<title>Mireille Administrative Tools</title>
</head>

<body>

<table cellspacing="3" class="head" summary="Header">
<tr>
<th><h1 class="head" style="text-align:left;margin-left:0.5em">Mireille Administrative Tools</h1></th>
<td style="font-size:15px;text-align:right;letter-spacing:1em">■■■■■■■</td>
</tr>
</table>
_HTML_

  $AM{'foot'}=<<"_HTML_";
<table cellspacing="3" class="head">
<tr>
<td style="font-size:15px;text-align:left;letter-spacing:1em">■■■■■■■</td>
<th><h1 class="head" style="text-align:right;margin-right:0.5em">
<a href="./" style="color:#fff;font-size:17px;font-weight:normal">BACK to INDEX</a></h2></td>
</tr>
</table>

<div class="AiremixCopy">- <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</a>
<var>$main::version</var> -</div>
</body>
</html>
</body>
</html>
_HTML_

  # Mireille Error Screen 1.1
  if($0 eq __FILE__){
    $SIG{'__DIE__'}=sub{
      print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
       :: Mireille ::
   * Error Screen 1.0 (T_T;) *

ERROR: $_[0]
Manage: $CF{'mngrev'}
Index : $CF{'idxrev'}
Style : $CF{'styrev'}
Core  : $CF{'correv'}

PerlVer  : $]
PerlPath : $^X
BaseTime : $^T
OS Name  : $^O
FileName : $0

 = = ENV = =
CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}
QUERY_STRING  : $ENV{'QUERY_STRING'}
REQUEST_METHOD: $ENV{'REQUEST_METHOD'}

SERVER_NAME: $ENV{'SERVER_NAME'}
HTTP_PATH  : $ENV{'HTTP_HOST'} $ENV{'SCRIPT_NAME'}
ENV_OS     : $ENV{'OS'}
SERVER_SOFTWARE      : $ENV{'SERVER_SOFTWARE'}
PROCESSOR_IDENTIFIER : $ENV{'PROCESSOR_IDENTIFIER'}

+#       Airemix Mireille       #+
+#  http://airemix.site.ne.jp/  #+
_HTML_
      exit;
    };
  }
}


package jcode;
;# jcode.pl: Perl library for Japanese character code conversion
;# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
;#  ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/
sub euc{
  my($s,$icode)=($_[0],'');
#外部からのデータはSJISであると信じます
#  if ($s!~/[\e\200-\377]/){#notJapanese
#    $icode=undef;
#  }elsif($s=~/\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I/o){#'jis'
#    $icode='jis';
#  }elsif($s=~/[\000-\006\177\377]/o){#'binary'
#    $icode='binary';
#  }else{#'euc'or'sjis'
#    my($sjis,$euc)=(0,0);
#    while($s=~/(([\201-\237\340-\374][\100-\176\200-\374])+)/go){$sjis+=length($1);}
#    while($s=~/(([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])+)/go)
#    {$euc+=length($1);}
#    $icode=('euc',undef,'sjis')[($sjis<=>$euc)+$[+1];
#  }
#  if('jis'eq$icode){
#    $s=~s/(\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I)([^\e]*)/&_jis2euc($1,$2)/geo;
#  }elsif('sjis'eq$icode){
    $s=~s/([\201-\237\340-\374][\100-\176\200-\374]|[\241-\337])/$jcode::s2e{$1}||&s2e($1)/geo;
#  }
  return$s;
}
=jis2euc
#JISは使わない
;# JIS to EUC
sub _jis2euc{
  my($esc,$s)=@_;
  if($esc!~/^\e\([BJ]/o){
    $s=~tr/\041-\176/\241-\376/;
    if($esc=~/^\e\(I/o){
      $s=~s/([\241-\337])/\216$1/g;
    }elsif($esc=~/^\e\$\(D/o){
      $s=~s/([\241-\376][\241-\376])/\217$1/g;
    }
  }
  $s;
}
=cut
;# SJIS to EUC
sub s2e{
  my($c1,$c2,$code);
  ($c1,$c2)=unpack('CC',$code=shift);
  if(0xa1<=$c1&& $c1<=0xdf){
    $c2=$c1;$c1=0x8e;
  }elsif(0x9f<=$c2){
    $c1=$c1*2-($c1>=0xe0?0xe0:0x60);$c2+=2;
  }else{
    $c1=$c1*2-($c1>=0xe0?0xe1:0x61);$c2+=0x60+($c2<0x7f);
  }
#  if($cache){$s2e{$code}=pack('CC',$c1,$c2);}else{pack('CC',$c1,$c2);}
  $jcode::s2e{$code}=pack('CC',$c1,$c2);
}

sub sjis{
#内部データなのだから漢字コードはEUCに決まってますｗ
  my($s,$icode)=($_[0],'');
#  if ($s!~/[\e\200-\377]/){#notJapanese
#    $icode=undef;
#  }elsif($s=~/\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I/o){#'jis'
#    $icode='jis';
#  }elsif($s=~/[\000-\006\177\377]/o){#'binary'
#    $icode='binary';
#  }else{#'euc'or'sjis'
#    my($sjis, $euc)=(0,0);
#    while($s=~/(([\201-\237\340-\374][\100-\176\200-\374])+)/go){$sjis+=length($1);}
#    while($s=~/(([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])+)/go)
#    {$euc+=length($1);}
#    $icode=('euc',undef,'sjis')[($sjis<=>$euc)+$[+1];
#  }
#  if('jis'eq$icode){#jis2sjis
#    $s=~s/(\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D|\e\([BJ]|\e\(I)([^\e]*)/&_jis2sjis($1,$2)/geo;
#  }elsif('euc'eq$icode){#euc2sjis
    $s=~s/([\241-\376][\241-\376]|\216[\241-\337]|\217[\241-\376][\241-\376])/$jcode::e2s{$1}||&e2s($1)/geo;
#  }
  return$s;
}
=jis2sjis
#JISは使いません
;# JIS to SJIS
sub _jis2sjis{
  my($esc,$s)=@_;
  if($esc=~/^\e\$\(D/o){
    $s=~s/../\x81\xac/g;
  }elsif($esc!~/^\e\([BJ]/o){
    $s=~tr/\041-\176/\241-\376/;
    ($esc=~/^\e\$\@|\e\$B|\e&\@\e\$B|\e\$\(D/o)
    &&($s=~s/([\241-\376][\241-\376])/$jcode::e2s{$1}||&e2s($1)/geo);
  }
  $s;
}
=cut
;# EUC to SJIS
sub e2s{
  my($c1,$c2,$code);
  ($c1,$c2)=unpack('CC',$code=shift);
  if($c1==0x8e){#SS2
    return substr($code,1,1);
  }elsif($c1==0x8f){#SS3
    return"\x81\xac";
  }elsif($c1 % 2){
    $c1=($c1>>1)+($c1<0xdf?0x31:0x71);
    $c2-=0x60+($c2<0xe0);
  }else{
    $c1=($c1>>1)+($c1<0xdf?0x30:0x70);
    $c2-=2;
  }
#  if($cache){$e2s{$code}=pack('CC',$c1,$c2);}else{pack('CC',$c1,$c2);}
  $jcode::e2s{$code}=pack('CC',$c1,$c2);
}

__END__
