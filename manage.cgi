#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Administrative Tools -
#
# "This file is written in euc-jp, CRLF." ��
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
    $j=~tr/\r/\n/; # ��̣Ū�ˤ� tr/\x0D\x0A/\n\n/;
    $DT{$i}=$j;
  }
  # Header with G-ZIP etc.
  print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja

_HTML_
  # Password Check
  ($DT{'mode'})||(return undef);
  ($DT{'pass'}eq$AM{'pass'})||(&menu('Password�����פ��ޤ���'));
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
Icon�ꥹ���Խ��ʥ�����(<span class="ak">Y</span>)</label>
<br>
<label accesskey="u" for="icons">
<input name="mode" class="radio" id="icons" type="radio" value="icons">
Icon�ꥹ���Խ�(Sharp��(<span class="ak">U</span>)</label>
<br>
<label accesskey="i" for="iconsmp">
<input name="mode" class="radio" id="iconsmp" type="radio" value="iconsmp" checked>
<span class="ak">I</span>con���ܤ򹹿�</label>
<br>
<label accesskey="g" for="config">
<input name="mode" class="radio" id="config" type="radio" value="config">
<del>Config�Խ�</del>(<span class="ak">G</span>)</label>
<br>
<label accesskey="b" for="css">
<input name="mode" class="radio" id="css" type="radio" value="css">
����CSS�Խ�(<span class="ak">B</span>)</label>
<br>
<label accesskey="l" for="log">
<input name="mode" class="radio" id="log" type="radio" value="log">
<span class="ak">L</span>OG���������</label>
<br>
<label accesskey="z" for="zero">
<input name="mode" class="radio" id="zero" type="radio" value="zero">
<span class="ak">Z</span>ero�ե���������</label>
</fieldset>
<p><label accesskey="p" for="pass"><span class="ak">P</span>assword:
<input name="pass" id="pass" type="password" size="12" value="$IN{'pass'}"></label></p>
<p><input type="submit" accesskey="s" class="submit" value="OK">
<input type="reset" class="reset" value="����󥻥�"></p>
$AM{'foot'}
ASDF
  exit;
}

#-------------------------------------------------
# IconTag
sub icont{
  my(%DT)=@_;
  &loadcfg;
  unless($DT{'icon'}){#��������ꥹ���Խ�
    sysopen(RD,"$CF{'icls'}",O_RDONLY)||die"Can't open iconlist.";
    flock(RD,LOCK_SH);
    my$icon=join('',<RD>);
    close(RD);
    $icon=~s/\t/\ \ /go;
    $icon=~s/[\x0D\x0A]*$//o;
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">��������ꥹ���Խ��⡼��</h2>
<form accept-charset="euc-jp" name="iconedit" method="post" action="$AM{'manage'}">
<p><textarea name="icon" cols="100" rows="15">$icon</textarea></p>
<p><label accesskey="r" for="renew">���������ܹ���(<span class="ak">R</span>):
<input name="renew" id="renew" type="checkbox" value="renew" checked></label></p>
<input name="mode" type="hidden" value="icont">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
  exit;
  }else{#��������ꥹ�Ƚ񤭹��� Tag
    study$DT{'icon'};
    $DT{'icon'}=~tr/\n//s;
    $DT{'icon'}=~s/(\n)*$/\n/;

    sysopen(WR,"$CF{'icls'}",O_CREAT|O_WRONLY|O_TRUNC)||die"Can't write icli.";
    flock(WR,LOCK_EX);
    print WR $DT{'icon'};
    close(WR);

    unless($DT{'renew'}){
      &menu('��������ꥹ�Ƚ񤭹��ߴ�λ');
    }else{
      &iconsmp;
      &menu('��������ꥹ�ȡ����ܽ񤭹��ߴ�λ');
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
    #��������ꥹ��Sharp�Խ�����
    print<<"ASDF";
$AM{'head'}
<h2 class="mode">��������ꥹ���Խ��⡼��</h2>
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
<p><label accesskey="r" for="renew">���������ܹ���(<span class="ak">R</span>):
<input name="renew" id="renew" type="checkbox" value="renew" checked></label></p>
<input name="mode" type="hidden" value="icons">
<input name="pass" type="hidden" value="$IN{'pass'}">
<input type="submit" accesskey="s" class="submit" value="OK"></p>
$AM{'foot'}
ASDF
    
    exit;
  }else{
    #��������ꥹ�Ƚ񤭹���
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
        #�������󥰥롼��
        ($optg==1)&&(print OUT "</optgroup>\n");
        ($1)||($optg=0,next);
        print OUT qq[<optgroup label="$1">\n];
        $optg=1;
        next;
      }elsif($_=~m/^\s*([^#]*)\s*\#\s*(.*)$/o){
        #�����������
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
      &menu('��������ꥹ�Ƚ񤭹��ߴ�λ');
    }else{
      &iconsmp;
      &menu('��������ꥹ�ȡ����ܽ񤭹��ߴ�λ');
    }
    exit;
  }
}

#-------------------------------------------------
# Icon���ܹ���
sub iconsmp{
  &loadcfg;
  sysopen(RD,"$CF{'icls'}",O_RDONLY)||die"Can't open iconlist.";
  flock(RD,LOCK_SH);
  my@icon=<RD>;
  close(RD);
  
  #OPTGROUP����
  #^<optgroup (.*)label=[\"\']([^\"\']*)[\"\'](.*)>$
  #<table $1summary="$2"$3>
  #{^</optgroup>$}{</tr></table>}
  #OPTION����
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
  print OUT qq[<h2 class="mode">����������</h2>\n$CF{'iched'}];

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
        $CR{'VENDOR_Link'}=qq[<a href="$CR{'VENDOR_URL'}" title="�����">$CR{'VENDOR'}</a>];
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
        $CR{'COPY1_Link'}=qq[<a href="$CR{'COPY1_URL'}" title="�켡�����">$CR{'COPY1'}</a>];
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
<caption>����¾</caption>
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

  &menu('���������ܹ�����λ');
}

#-------------------------------------------------
# Config Editor
sub config{
  my(%DT)=@_;
my@required=(
 'name'  =>'�����Ȥ�̾��'
,'home'  =>'�����ȥȥåץڡ�����URL'
,'title' =>'���ηǼ��ĤΥ����ȥ�'
,'gzip'  =>'GZIP��PATH'
,'icon'  =>'��������Υǥ��쥯�ȥ��URL'
,'style' =>'�������륷����'
);
    my@implied=(
 'admps'=>'�����ԥѥ���ɡ����Ƥε������Խ�������Ǥ��ޤ� 15-30ʸ���侩��'
,'tags'  =>'���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��'
,'newnc' =>'�����ð���ε�����New�ޡ�����Ĥ���'
,'newuc' =>'�ɤ�������Ǥ�����ô֤ϡ�̤�ɡ׾��֤�ݻ���������������class="new"��Ĥ����'
,'new'   =>'���������ε����ˤĤ���ޡ����ʡ����ð���ε�����New�ޡ�����Ĥ����'
,'page'  =>'�̾�⡼�ɤ�1�ڡ���������Υ���åɿ�'
,'delpg' =>'����������⡼�ɤǤ�1�ڡ���������Υ���åɿ�'
,'logmax'=>'���祹��åɿ�'
,'prtitm'=>'�Ƶ����ι���(+color +email +home +icon +ra +hua cmd +title)'
,'chditm'=>'�ҵ����ι���(+color +email +home +icon +ra +hua cmd)'
,'cokitm'=>'Cookie�ι���(color email home icon)'
);
    my@select=(
 'del'   =>'��������åɤκ����ˡ','rename �ե�����̾�ѹ� unlink �ե�������'
,'sort'  =>'�������¤ӽ�','number �����ֹ�� date ���������'
,'mailnotify'=>'����/�ֿ� �����ä��Ȥ��˻��ꥢ�ɥ쥹�˥᡼�뤹��','0 �Ȥ�ʤ� 1 �Ȥ�'
,'prtwrt'=>'������ƥե������Index��ɽ��','0 ɽ�����ʤ� 1 ɽ������'
);
    my@design=(
 'menu'  =>'Mireile Menu'
,'head'  =>'Page Header'
,'note'  =>'��ս񤭡�TOP�ڡ����Υ�˥塼�β���ɽ������ޤ���'
,'foot'  =>'Page Footer'
,'artprt'=>'�Ƶ���'
,'artchd'=>'�ҵ���'
,'artfot'=>'�����Υեå���'
,'wrtfm' =>'�������/�Խ��ե�����'
,'resfm' =>'�ֿ��ե�����'
,'iched' =>'��������ꥹ�ȤΥإå���'
,'icfot' =>'��������ꥹ�ȤΥեå���'
);
  unless($DT{'name'}){
    my$message='';
    unless(&loadcfg){
      $message=<<'_HTML_';
<h2>config���ɤ߹��ߤǥ��顼��ȯ�����ޤ���</h2>
<p>config����»���Ƥ����ǽ��������ޤ�<br>
���Τޤ޼¹Ԥ���С�config���񤭤������ꤷ�ʤ����ޤ�</p>
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
<caption>CONFIG�Խ�</caption>
<col style="text-align:left;width:600px"><col style="text-align:left;width:200px">

<tbody>
<tr><th class="cfghead" colspan="2">��ư���������˳�ǧ���뤳��</th></tr>
ASDF

    my$i=0;
    #��ư���������˳�ǧ���뤳��
    for($i=0;$i<$#required;$i+=2){
      print<<"ASDF";
<tr>
<th class="item">$required[$i+1]��</th>
<td><input name="$required[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$required[$i]"}"></td>
</tr>
ASDF
    }

    print<<"ASDF";
</tbody>

<tbody>
<tr><th class="cfghead" colspan="2">ɬ�פ˱������ѹ�</th></tr>
ASDF
    #ɬ�פ˱������ѹ�
    for($i=0;$i<$#implied;$i+=2){
      print<<"ASDF";
<tr>
<th class="item">$implied[$i+1]��</th>
<td><input name="$implied[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$implied[$i]"}"></td>
</tr>
ASDF
    }

    #����
    for($i=0;$i<$#select;$i+=3){
      print<<"ASDF";
<tr>
<th class="item">$select[$i+1]��</th>
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
<tr><th class="cfghead" colspan="2">���ѥ�������</th></tr>
<tr>
<th class="item">���ѥ�������ǽ��</td>
ASDF
    $i=<<"ASDF";
<td>
<label for="exiconon">�Ȥ�<input id="exiconon" name="exicon" type="radio" value="1"
checked></label>
<label for="exiconof">�Ȥ�ʤ�<input id="exiconof" name="exicon" type="radio" value="0"></label>
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
<th class="item">�ѥ���ɡ�<input name="ICN$_" type="text" style="ime-mode:disabled" value="$IC[$_]"></td>
<td>�ե�����̾��<input name="ICV$_" type="text" style="ime-mode:disabled" value="$IC{$IC[$_]}"></td>
</tr>
ASDF
    }

    for(($#IC+1)..($#IC+5)){
      print<<"ASDF";
<tr>
<th class="item">�ѥ���ɡ�<input name="ICN$_" type="text" style="ime-mode:disabled" value=""></td>
<td>�ե�����̾��<input name="ICV$_" type="text" style="ime-mode:disabled" value=""></td>
</tr>
ASDF
    }
  
    print<<"ASDF";
<tr><th class="cfghead" colspan="2">�ѹ����ʤ��ۤ�������</td></tr>
<tr>
<th class="item">�����ॾ����</td>
<td><input name="TZ" type="text" style="ime-mode:disabled" value="$ENV{'TZ'}"></td>
</tr>
<tr>
<th class="item">index��</td>
<td><input name="index" type="text" style="ime-mode:disabled" value="index.cgi"></td>
</tr>
</tr>
<tr>
<th class="item">help��</td>
<td><input name="help" type="text" style="ime-mode:disabled" value="help.html"></td>
</tr>
</tr>
<tr>
<th class="item">log��</td>
<td><input name="log" type="text" style="ime-mode:disabled" value="$CF{'log'}"></td>
</tr>

<tr><th class="cfghead" colspan="2">Mireille���HTML�ǥ�����</td></tr>
ASDF
    #Mireille���HTML�ǥ�����
    for($i=0;$i<$#design;$i+=2){
      print<<"ASDF";
<tr><th class="item" colspan="2">$design[$i+1]��</th></tr>
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
    
    #����ʸ�������
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
# "This Script is written in euc-jp." ��
#------------------------------------------------------------------------------#
use strict;
use vars qw{\%CF \%IC};
#-------------------------------------------------
# ��ư���������˳�ǧ���뤳��

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
# ɬ�פ˱������ѹ�

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
#���ѥ�������ǽON(1),OFF(0)
\$CF{'exicon'}=\'$DT{'exicon'}\';
#���ѥ����������
#\$IC{'PASSWORD'}='FILENAME'; #NAME
#"icon=moe" -> moe.png
ASDF
    for(my$i=0;defined$DT{"ICN$i"};$i++){
      ($DT{"ICN$i"}&&$DT{"ICV$i"})||(next);
      $config.=qq{\$IC{\'$DT{"ICN$i"}\'}=\'$DT{"ICV$i"}\';\n};
    }
    $config.=<<"ASDF";

#-------------------------------------------------
# �ѹ����ʤ��ۤ�������

#�����ॾ����
\$ENV{'TZ'}  = \'$DT{'TZ'}\';
#�����ƥ�ե�����
\$CF{'log'}  = \'$DT{'log'}\'; #LOG PATH

#-------------------------------------------------
# Mireille���HTML�ǥ�����

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
    
    &menu('config�˽񤭹��ߴ�λ');
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
<h2 class="mode">�������륷���ȥե���������</h2>
<form accept-charset="euc-jp" name="cssedit" method="post" action="$AM{'manage'}">
<p>CSS�ե�����̾<input name="file" type="text" style="ime-mode:disabled" value="$IN{'file'}">�ʳ�ĥ�Ҥ����Ϥ��ʤ���<br>
�㡧$CF{'style'}�ʤ顢style�Ȥ������Ϥ���<br>
������Υ������ƥ����ݤΤ���Ǥ��Τǡ��������餺</p>
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
<h2 class="mode">�������륷�����Խ��⡼��</h2>
<form accept-charset="euc-jp" name="cssedit" method="post" action="$AM{'manage'}">
<p>CSS�ե�����̾:$IN{'file'}.css<input name="file" type="hidden" value="$IN{'file'}"><p>
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
    
    &menu('css�񤭹��ߴ�λ');
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
<h2 class="mode">�������⡼��</h2>
<form accept-charset="euc-jp" name="logedit" method="post" action="$AM{'manage'}">


<fieldset style="padding:0.5em;width:60%">
<legend>�Хå����å׺��</legend>
<label for="back"><input name="type" id="back" type="radio" value="3" checked="checked">
�Хå����åץե������������</label>
<pre style="text-align:center">�ե�����̾�ѹ�������ΤȤ��ˤǤ����Хå����åץե��������ݤ��ޤ�
����Ū�ˤϥ��ǥ��쥯�ȥ���Τ��٤Ƥγ�ĥ��.bak�Υե�����������ޤ�
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:60%">
<legend>��������åɤ���</legend>
<fieldset style="padding:0.5em;width:90%">
<legend>������������</legend>
<input name="type" type="radio" value="1">
<input name="str" type="text" size="3" style="ime-mode:disabled" value="">
��
<input name="end" type="text" size="3" style="ime-mode:disabled" value="">
<pre style="text-align:center">�����ֹ梢�����ޤǺ�����ޤ�
���΢��˲�������ʤ��ä����ϡ�0������������
��΢��˲�������ʤ��ä����ϡ�������ǿ���Ĥ��Ƥ������ΤΤ�Τ�������ޤ�
���ʤ���ʥ��ޥ�ɤǤ⤢��Τǡ�ɬ���¹����˥Хå����åפ�Ȥ�褦�ˤ��ޤ��礦
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:90%">
<legend>1��(�ǿ�-��)������</legend>
<input name="type" type="radio" value="2">
<input name="save" type="text" size="3" style="ime-mode:disabled" value="">
<pre style="text-align:center">�ǿ����颢�ĻĤ��ơ�����ʳ��������ޤ�
�����Ǥ����ֺǿ��פȤϵ����ֹ�κǤ��礭��ʪ���Τ��ȤǤ�
ɬ���¹����˥Хå����åפ�Ȥ�褦�ˤ��ޤ��礦
</pre>
</fieldset>

<fieldset style="padding:0.5em;width:50%">
<legend>�������</legend>
<label for="rename">�ե�����̾�ѹ���<input name="del" id="rename" type="radio" value="rename" checked></label>
<label for="unlink">�ե���������<input name="del" id="unlink" type="radio" value="unlink"></label>
</fieldset>

<p><label for="push"><input id="push" name="push" type="checkbox" value="1">�����ֹ��Ĥ��</label>
<br>�����ֹ�򣱤�����֤��ѹ����ޤ�</p>
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
<h2 class="mode">�������⡼��</h2>
<form accept-charset="euc-jp" name="logedit" method="post" action="$AM{'manage'}">
ASDF
    if($DT{'type'}==1){
      ($DT{'str'})||($DT{'str'}=1);
      ($DT{'end'})||($DT{'end'}=$DT{'str'},$DT{'str'}=1);
      print<<"ASDF";
<p>�����ˡ�
<input name="str" type="text" size="3" value="$DT{'str'}" readonly>����
<input name="end" type="text" size="3" value="$DT{'end'}" readonly>�������Ƥ�����Ǥ�����
<input name="type" type="hidden" value="a">
<input name="del" type="hidden" value="$DT{'del'}">
</p>
ASDF
      if($DT{'del'}eq'unlink'){
        print"<p>�ե�������</p>";
      }else{
        print"<p>�ե�����̾�ѹ�/p>";
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
<p>�����ˡ��ǿ�����
<input name="save" type="text" size="3" value="$DT{'save'}" readonly>�ĻĤ���
������Ƥ�����Ǥ�����<input name="type" type="hidden" value="b"><br>
�����ֹ�$file[$#file]����$file[$DT{'save'}]�ޤǤΡ�$i��������ޤ�
<input name="del" type="hidden" value="$DT{'del'}">
</p>
ASDF
      if($DT{'del'}eq'unlink'){
        print"<p>�ե�������</p>";
      }else{
        print"<p>�ե�����̾�ѹ�/p>";
      }
    }elsif($DT{'type'}==3){
        print<<"ASDF";
<p>�����ˡ��Хå����åץե��������ݤ��Ƥ�����Ǥ�����</p>
<input name="type" type="hidden" value="c">
ASDF
    }else{
      exit;
    }
    
    print<<"ASDF";
<br>
<p><a href="$AM{'manage'}" title="����">�ְ㤨���ΤǺǽ餫����ľ��</a></p>
<br>
<p>
<input name="mode" type="hidden" value="log">
<input name="pass" type="hidden" value="$IN{'pass'}">
���ͤ�: <input name="push" type="text" size="3" value="$DT{'push'}" readonly></p>
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
      &menu("$file�ĤΥХå����åץե�����������ޤ���");
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
      chop$zerD;#�Ǹ��' '���
      
      truncate(ZERO,0);
      seek(ZERO,0,0);
      print ZERO "@zer0\n";
      print ZERO "@zer1\n";
      print ZERO "@zerC\n";
      print ZERO "$zerD\n";#�ե�����̾�ѹ��Υ�
      close(ZERO);
      
      &menu("��$DT{'str'}��$DT{'end'}�Υե�����$file�Ĥ�����λ<br>���ͤ�����");
    }
    
    &menu("��$DT{'str'}��$DT{'end'}�Υե�����$file�Ĥ�����λ");
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
<h2 class="mode">ZeroFile�����⡼��</h2>
<form accept-charset="euc-jp" name="zero" method="post" action="$AM{'manage'}">
<p>ZeroFile��ꥫ�Хꤹ��ȡ���¸�ξ���ϼ����ޤ�<br>
����Ǥ������Ǥ�����
<input name="mode" type="hidden" value="zero">
<input name="pass" type="hidden" value="$IN{'pass'}"></p>
<p><label accesskey="r" for="recover">��������
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
    #�����ֹ�� 'number'
    @file=sort{$b<=>$a}@file;
    
    for(@file){
      $zer2[$_-$file[$#file]]=(stat("$CF{'log'}$_.cgi"))[9];
    }
    
    unshift(@zer2,$file[$#file]-1);
    
    sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write 0.cgi.";
    print ZERO <<"ASDF";
Mir1=\t;\ttitle=\tZeroFile��������ޤ���;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

@zer2
ASDF
    close(ZERO);
    &menu("ZeroFile������λ");
  }
  exit;
}


#-------------------------------------------------
# config�ɤ߹���
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
<td style="font-size:15px;text-align:right;letter-spacing:1em">��������������</td>
</tr>
</table>
_HTML_

  $AM{'foot'}=<<"_HTML_";
<table cellspacing="3" class="head">
<tr>
<td style="font-size:15px;text-align:left;letter-spacing:1em">��������������</td>
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
#��������Υǡ�����SJIS�Ǥ���ȿ����ޤ�
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
#JIS�ϻȤ�ʤ�
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
#�����ǡ����ʤΤ�������������ɤ�EUC�˷�ޤäƤޤ���
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
#JIS�ϻȤ��ޤ���
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
