#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Core File -
#
 $CF{'correv'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IC %IN %CK %Z0 @zer2 @file);

INIT:{
  if($0=~m{core.cgi$}o){
    #ľ�ܼ¹Ԥ��ä���ư���Ф�
    &locate($ENV{'CONTENT_LENGTH'});
  }
  DIR:{
    ($CF{'log'})||die"Undefined LogDir!";
    (-e"$CF{'log'}")&&(last DIR);
    (mkdir"$CF{'log'}",0777)&&(last DIR);
    die"Can't read/write/create LogDir!";
  }
  sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write log0!";
  print ZERO <<"ASDF";
Mir1=	0-0;	subject=	Welcome to Mireille;	name=	System;	time=	999499209;	body=	LOG�ǥ��쥯�ȥ�ڤ�0.cgi����������֤���Ƥ��ʤ��ä��褦�Ǥ���ưŪ�����֤��ʤ����ޤ���;	
ASDF
  close(ZERO);
}

#-------------------------------------------------
# MARD SWITCH
#
#�⡼�ɤ��Ȥο���ʬ��
MAIN:{
  #����ɽ��
  (&getfm)||(last MAIN);
  #�����񤭹���
  (defined$IN{'body'})&&(&write);
  #�ֿ�
  ($IN{'i'})&&(&res);
  #�����񤭹���
  if(defined$IN{'j'}){&getck;&header;&prtfrm(\%CK,'j'=>0);&footer;}
  #����
  (defined$IN{'seek'})&&(&seek);
  #���������ꥹ��or�¹�
  if(defined$IN{'rvs'}){($IN{'rvs'})||(&rvsmenu);&revise;}
  #��������ꥹ��or�¹�
  if(defined$IN{'del'}){($IN{'del'})||(&rvsmenu);&delete;}
  #�إ��
  (defined$IN{'help'})&&(&locate($CF{'help'}));
  #�ۡ���
  (defined$IN{'home'})&&(&locate($CF{'home'}));
  #����ɽ��
  last MAIN;
  exit;
}

#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# MAIN:ľ���Υ��֥롼����

#-------------------------------------------------
# Index ����ɽ��
#
#sub index{
  my$new=0;
  #-----------------------------
  #Cookie�������񤭹���
  if(&getck){
    &wrtcook(\%CK);
  }else{
    $CK{'time'}=$^T-$CF{'newnc'};
  }

  #-----------------------------
  # HTTP,HTML,PAGE�إå�����ɽ��
  &header;

  #-----------------------------
  #�ڡ�������
  &logfiles($CF{'sort'});
  if($IN{'read'}){
    my%FILE;my$i=1;my$j=1;
    for(@file){
      $FILE{"$_"}="$i";
      (++$j>$CF{'page'})||(next);
      $i++;$j=1;
    }
    $IN{'page'}=$FILE{"$IN{'read'}"};
  }
  my$max=int(($#file-1)/$CF{'page'})+1;
  ($max<$IN{'page'})&&($IN{'page'}=$max);
  ($IN{'page'})||($IN{'page'}=1);

  #-----------------------------
  #������ƥե������ɽ�����������ˤ���
  if($CF{'prtwrt'}){
    &prtfrm(\%CK,'j'=>0);
  }
  print"$CF{'note'}";

  #-----------------------------
  #��������
  my@new=();my%NEW;
  for(1..$#zer2){
    my$No=$_+$zer2[0];
    ($zer2[$_]>$CK{'time'})||(next);
    unshift(@new,qq{<a href="$CF{'index'}?read=$No#$No" class="new">$No</a>});
    $NEW{"$No"}=1;
  }
  my$info="<p>";
  #20��ޤ�
  if($#new>19){
    $info.=qq{̤�ɵ����Τ��륹��å�[ @new[0..20] .. ]<br>\n};
  }elsif($#new>-1){
    $info.=qq{̤�ɵ����Τ��륹��å�[ @new[0..$#new] ]<br>\n};
  }

  my@i=@file;@i=splice(@i,($IN{'page'}-1)*$CF{'page'},$CF{'page'});
  (($i[0]!=0)&&(!$i[$#i]))&&(pop@i);

  $info.="���Υڡ����Υ���å�<br>\n[ ";
  $new=0;
  for(@i){
    $new++;
    if($NEW{"$_"}){
      $info.=qq{<a href="#$_" title="Alt+$new"><span class="new">$_</span></a> };
    }else{
      $info.=qq{<a href="#$_" title="Alt+$new">$_</a> };
    }
  }
  $info.="]</p>\n";
  print$info;

  #-----------------------------
  #�ڡ�������TABLE��ɽ��
  my$pgslct=&pgslct($max);
  print"$pgslct";

  #-----------------------------
  #����ɽ��
  $new=0;
  if($#file){
    #���˲�ư��ΤȤ�
    my$i=1;
#    if($CF{'prtres'}){
#      for(@i){
#        $new+=&article('i'=>$_,'ak'=>$i++,%CK);
#      }
#    }else{
      for(@i){
        $new+=&article('i'=>$_,'ak'=>$i++);
      }
#    }
  }else{
    #log0�Τ� �Ĥޤ�����ľ��ΤȤ�
#    if($CF{'prtres'}){
#      &article('i'=>0,'ak'=>1,%CK);
#    }else{
      &article('i'=>0,'ak'=>1);
#    }
  }

  #-----------------------------
  #̤�ɵ������Τ餻��ǽ
  ($new)&&(print"<p><span class=\"new\">���Υڡ�����̤�ɵ�����$new�濫��ޤ�����</span></p>\n");
  print$info;

  #-----------------------------
  #�ڡ�������TALBE�ȥեå���
  print"$pgslct";
  &footer;

  exit;
#}


#-------------------------------------------------
# �����񤭹���
#
sub write{
  #-----------------------------
  #���顼ɽ��
  my@error;
  ($IN{'name'})||(push(@error,"<span style=\"color:#f00\">̾��</span>"));
  ($IN{'body'})||(push(@error,"<span style=\"color:#f00\">��ʸ</span>"));
  ($IN{'pass'}||($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'})))
   ||(push(@error,'<span style="color:#f00">�ѥ����</span>'));

  if($#error>-1){
    my$error=join('��',@error);
    &header;
    print<<"_HTML_";
<h2 class="mode">- Write Error -</h2>
<p>$error����������Ϥ��Ƥ�������</p>
_HTML_
    &rvsij(\%IN);
    &footer;
  }
  
  SUBJECT:{
    #subject����ν���
    if($IN{'j'}){
      ($CF{'chditm'}=~m/\bsubject\b/o)||(last SUBJECT);
    }else{
      ($CF{'prtitm'}=~m/\bsubject\b/o)||(last SUBJECT);
    }
    unless($IN{'subject'}){
      $IN{'subject'}=$IN{'body'};
      $IN{'subject'}=~s/<br>/\n/o;
    }
    my$i=substr($IN{'subject'},0,80);
    $i=~m/(.{0,80})/o;
    $i=$1;
    if($i=~/\x8F$/o){
      chop$i;
    }elsif($i=~tr/\x8E\xA1-\xFE//%2){
      $i.=substr($IN{'subject'},80,1);
    }
    $IN{'subject'}=$i;
  }
  
  #-----------------------------
  #���ѥ�������ǽ��config.pl�����ꤹ�롣
  if($CF{'exicon'}&&$IN{'cmd'}){
    my%EX=split(/[=&;]/o,$IN{'cmd'});
    #custom.pl�ǻ��ꤷ����������ѥ��˹��פ���С�
    ($IC{"$EX{'icon'}"})&&($IN{'icon'}=$IC{"$EX{'icon'}"});

=item �������ߥ�������

#    ($EX{'bring'})&&($IN{'icon'}=$EX{'bring'});
�������ߥ�������򿿤˲�ư�����뤿��ˤ�$CF{'icon'}=''�Ȥ��ʤ��ȡ�
��̣������ޤ���
�������������������礭�ʲ�����Ž����Ȥ����狼��䤹����ΤΤۤ��ˤ⡢
�Ȥ����ˤ�äƤ����ѼԤξ����������뤳�Ȥ��Ǥ���Ȥ�����������Τǡ�[
���Ѥ��֤���ͤ�����ʤ�����̵���¤�Ȥ�ʤ��ۤ��������Ǥ�

�⥸�塼��Image::size���Ѥ��뤳�Ȥˤ�äơ����������¤򤫤��뤳�Ȥ�����뤫�⤷��ޤ���
����ʤ�Ȥꤢ�����������������ޤ�����CGI��Ȥ������ƼԤξ���ή�Ф��롢��
�Ȥ�����ǽ���������ĤäƤ��뤿�ᡢ̵���¤ˤ��뤳�ȤϽ���ʤ��Ǥ��礦

=cut

  }

  #-----------------------------
  #$IN{'cook'}��ON�ʤ�Cookie�ν񤭹���
  COOKIE:{
    ($IN{'cook'})||(last COOKIE);
    ($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'}))&&(last COOKIE);
    &getck;
    &wrtcook(\%IN);
  }


  #-----------------------------
  #�񤭹��ߥǡ�������
  sysopen(ZERO,"$CF{'log'}0.cgi",O_RDWR)||die"Can't write log0!";
  flock(ZERO,LOCK_EX);
  my@zero=();
  while(<ZERO>){
    chomp$_;push(@zero,$_);
  }
  ($zero[0]=~/^Mir1=\t/o)||(die"��������Mir1���ʳ��Ǥ�");
  %Z0=($zero[0]=~m/([^\t]*)=\t([^\t]*);\t/go);
  my@zer1=split(/ /,$zero[1]);
  @zer2=split(/ /,$zero[2]);
  $IN{'newps'}=&mircrypt($^T,$IN{'pass'});
  
  #-----------------------------
  &logfiles('number');
  if($IN{'i'}){
    (($IN{'i'}>$file[0]+1)||($IN{'i'}<1))&&($IN{'i'}=$file[0]+1);
  }
  
  if((length$IN{'j'})xor($IN{'i'})){
    #�������ֿ��񤭹���
    my$i=$IN{'i'};
    my$j=$IN{'j'};
    ($i)||($i='\\d+');
    (length$j)||($j='\\d+');
    if($zero[1]=~/($i):$ENV{'CONTENT_LENGTH'}:($j)/){
      
      &header;
  print<<"_HTML_";
<h2 class="mode">- ¿������ӽ� -</h2>
<p style="margin:0.6em">�ʲ������Ƥ���$1�֥���åɤ�$2���ܤ�Ʊ�����Ƥ��Ȼפ��ޤ�<br>
Ʊ�����ƤǤʤ����ϡ����Υե�����Ǿ����������Ƥ�����Ƥ��Ƥ���������</p>
<table summary="BackMenu" width="300"><tr>
<colgroup span="2" width="150">
<td><form action="$CF{'index'}" method="get">
<input type="submit" class="button" accesskey="b" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="�Ǽ��Ĥ����(B)">
</form></td>
<td><form action="$CF{'home'}" method="get">
<input type="submit" class="button" accesskey="h" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="$CF{'name'}�����(H)">
</form></td>
</tr></table>
_HTML_
      &rvsij(\%IN,'i'=>$1,'j'=>$2);
      &footer;
    }elsif(!defined$IN{'i'}){ #((!defined$IN{'i'})&&($IN{'j'}eq'0'))
      #-----------------------------
      #�����񤭹���
      if($CF{'logmax'}>0){
        #�Ť���������åɥե������ �ե�����̾�ѹ�/��� ����
        if($#file>=$CF{'logmax'}){
          my$del=0;
          if($CF{'autodel'}eq'unlink'){
            #���
            for($file[$#file-1]..$file[$CF{'logmax'}-1]){
              $del++;
              unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog!";
            }
          }else{
            #�ե�����̾�ѹ�
            for($file[$#file-1]..$file[$CF{'logmax'}-1]){
              $del++;
              rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")
               ||die"Can't rename oldlog!";
            }
          }
          splice(@zer2,1,$del);
          $zer2[0]=$file[$CF{'logmax'}-1];
        }
      }

      $IN{'i'}=$file[0]+1;
      $IN{'j'}=0;
      sysopen(WR,"$CF{'log'}$IN{'i'}.cgi",O_CREAT|O_WRONLY)||die"Can't write log$IN{'i'}!";
      flock(WR,LOCK_EX);
    print WR "Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t";
      for($CF{'prtitm'}=~m/\+([a-z\d]+)\b/go){
        print WR qq($_=\t$IN{"$_"};\t);
      }
      print WR "\n";
      close(WR);
    }elsif($IN{'i'}){ #($IN{'i'})&&(!defined$IN{'j'})
      #-----------------------------
      #�ֿ��񤭹���
      sysopen(RW,"$CF{'log'}$IN{'i'}.cgi",O_CREAT|O_RDWR)||die"Can't write log$IN{'i'}!";
      flock(RW,LOCK_EX);
      seek(RW,0,0);
      my@log=<RW>;
      $IN{'j'}=$#log+1;
      seek(RW,0,2);
    print RW "Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t";
      for($CF{'chditm'}=~m/\+([a-z\d]+)\b/go){
        print RW qq($_=\t$IN{"$_"};\t);
      }
      print RW "\n";
      close(RW);
    }
    
    #-----------------------------
    #�������ե����롢0.pl�˽񤭹���
    #�������ֿ��λ��ˤ���ƾ������¸
    ($#zer1>2)&&(splice(@zer1,2));
    unshift(@zer1,"$IN{'i'}:$ENV{'CONTENT_LENGTH'}:$IN{'j'}");
    my$No=$IN{'i'}-$zer2[0];
    ($No>0)||(die"ZER2�Υǡ����������Ǥ� 'i':$IN{'i'},'zer2':$zer2[0]");
    $zer2[$No]=$^T;
    truncate(ZERO,0);
    seek(ZERO,0,0);
    print ZERO <<"_HTML_";
Mir1=\t$IN{'i'}-$IN{'j'};\tsubject=\t$IN{'subject'};\tname=\t$IN{'name'};\ttime=\t$^T;\t
@zer1
@zer2
_HTML_
    
    #-----------------------------
    #MailNotify
    
    #����/�ֿ������ä����ϥ᡼�������
    if($CF{'mailnotify'}){
      require'notify.pl';
      (&mailnotify(%IN))||(print ZERO 'MailNotify Failed.\n');
    }
  }elsif(($IN{'i'})&&(defined$IN{'j'})){
    #-----------------------------
    #�����񤭹���
    sysopen(RW,"$CF{'log'}$IN{'i'}.cgi",O_RDWR)||die"Can't write log$IN{'i'}!";
    flock(RW,LOCK_EX);
    my@log=<RW>;
    chomp$log[$IN{'j'}];
    my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

    if($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'})){
      #MasterPass�ˤ��
      if($IN{'pass'}){
        #Pass�ѹ�
        $IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
      }else{
        $IN{'newps'}=$DT{'pass'};
      }
      $IN{'pass'}='';
    }else{
      #UserPass�ˤ��
      unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
        &header;
        print qq[<h2 class="mode">Password Error</h2>\n];
        &rvsij(\%IN);
        &footer;
        exit;
      }
      $IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
    }

    #�񤭹���
    $log[$IN{'j'}]
    ="Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$DT{'time'};\tbody=\t$IN{'body'};\t";
    if($IN{'j'}eq'0'){
      #�Ƶ���
      for($CF{'prtitm'}=~m/\+([a-z\d]+)\b/go){
        $log[$IN{'j'}].=qq($_=\t$IN{"$_"};\t);
      }
    }else{
      #�ҵ���
      for($CF{'chditm'}=~m/\+([a-z\d]+)\b/go){
        $log[$IN{'j'}].=qq($_=\t$IN{"$_"};\t);
      }
    }
    $log[$IN{'j'}].="\n";
    
    truncate(RW,0);
    seek(RW,0,0);
    print RW join('',@log);
    close(RW);
  }else{
    #-----------------------------
    #Something Wicked happened!
    &header;
    print<<'_HTML_';
<h2 class="mode">Something Wicked happened!</h2>
<pre>�����ٰ��ʤ��Ȥ������ޤ���
�Ǽ��Ĥ�̤�ΤΥХ���¸�ߤ��뤫��
���֤����꤬���뤫��
��������ƤǤ����ǽ��������ޤ���
�����ͤˤ��Υ��顼��ȯ���������Ȥ������Ƥ���������
ErrorCode:"WriteSwitch'ELSE'"
_HTML_
    for(keys%IN){
      print"$_\t$IN{$_}\n";
    }
    print'</pre>';
    &footer;
  }
  close(ZERO); #�����Ǥ�äȽ񤭹��߽�λ

  #-----------------------------
  #�񤭹����������ּ�ͳ�˽�����ɤ�����
  &header;
  print<<"_HTML_";
<h2 class="mode">- �񤭹��ߴ�λ -</h2>
<p style="margin:0.6em">�ʲ������Ƥ���$IN{'i'}�֥���åɤ�$IN{'j'}���ܤ˽񤭹��ߤޤ�����<br>
����Ǥ褱��Ф��Τޤ�TOP��Ǽ��Ĥ���äƤ���������<br>
�������������ϰʲ��Υե�����ǽ���������Ƥ��Ƥ���������</p>
<table summary="BackMenu" width="300"><tr>
<colgroup span="2" width="150">
<td><form action="$CF{'index'}" method="get">
<input type="submit" class="button" accesskey="b" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="�Ǽ��Ĥ����(B)">
</form></td>
<td><form action="$CF{'home'}" method="get">
<input type="submit" class="button" accesskey="h" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="$CF{'name'}�����(H)">
</form></td>
</tr></table>
_HTML_
  &rvsij(\%IN);
  &footer;

  exit;
}


#-------------------------------------------------
# ���������������˥塼
#
sub rvsmenu{
  &getck;
  &header;
  my$mode='';
  if(defined$IN{'rvs'}){$mode='rvs';print qq[<h2 class="mode">- �����Խ��⡼�� -</h2>\n];}
  elsif(defined$IN{'del'}){$mode='del';print qq[<h2 class="mode">- ��������⡼�� -</h2>\n];}
  else{print qq[<h2 class="mode">Something Wicked happend!</h2>];&footer;}
  ($_[0])&&(print"<p>$_[0]</p>\n");

  &logfiles('number');
  my$max=int(($#file-1)/$CF{'delpg'})+1;
  ($max<$IN{'page'})&&($IN{'page'}=$max);
  my@i=@file;
  @i=splice(@i,($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});

  my$pgslct=&pgslct($max,"$mode");
  print<<"_HTML_";
$pgslct

<form id="List" method="post" action="$CF{'index'}">
<table cellspacing="0" class="list" summary="List" width="550">
<col width="50">
<col width="170">
<col width="330">
<tr><td colspan="2"><span class="ak">P</span>assword: <input name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
</td>
<td>
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">��
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="����󥻥�">
</td></tr>
_HTML_

  for(@i){
    my$i=$_;
    my$j=-1;
    (-e"$CF{'log'}$i.cgi")||(next);
    ($i)||(next);
    sysopen(RD,"$CF{'log'}$i.cgi",O_RDONLY)||die"Can't open log$i!";
    flock(RD,LOCK_SH);
    print'<tr><td colspan="6"><hr></td></tr>';
    my$count="<a href=\"$CF{'index'}?read=$i#$i\">��$i��</a>";
    while(<RD>){
      $j++;
      ($_=~/^Mir1=\tdel;\t/o)&&(next);
      my%DT=($_=~m/([^\t]*)=\t([^\t]*);\t/go);
      ($j)&&($count="Res $j");
      my$No="$i-$j";
      my$date=&date($DT{'time'});
      $DT{'body'}=($DT{'body'}=~/(.*)<br>/o)?$1:'';
      $DT{'body'}=~s/<[^>]*>//go;
      my$i=substr($DT{'body'},0,100);
      if($i=~/\x8F$/o){
        chop$i;
      }elsif($i=~tr/\x8E\xA1-\xFE//%2){
       $i.=substr($DT{'body'},100,1);
      }
      $DT{'body'}=$i;
      print<<"_HTML_";
<tr>
<td align="right">$count</td>
<td align="left">$DT{'titke'}</td>
<td align="right">by $DT{'name'}</td>
</tr>
<tr>
<td><input type="radio" name="$mode" value="$No"></td>
<td align="right">$date</td>
<td align="right">$DT{'body'}</td>
</tr>
_HTML_
    }
    close(RD);
  }
  print"</table></form>\n";

  print"$pgslct";
  &footer;

  exit;
}


#-------------------------------------------------
# ��������
#

#���Ȥ�$IN{'pass'}���Ϥ���ʤ��Ƥ⡢GetCookie��Cookie�򻲾Ȥ���
#�⤷����������줿$CK{'pass'}���ѥ���ɤȰ��פ���н����⡼�ɤ��̤���
#�Ȥ����褦�ˤ����������θ����ޤäƤ��롣
#�����ѥ���ɤ����פ��ʤ�������Ϥ���褦���������롣
sub revise{
  ($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});

  sysopen(RD,"$CF{'log'}$IN{'i'}.cgi",O_RDONLY)||die"Can't open log$IN{'i'}!";
  flock(RD,LOCK_SH);
  my@log=<RD>;
  close(RD);
    my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

  if($IN{'pass'}){
    #IN�������Ƥ�����
    if(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
      #��äƤ���н�����
    }elsif($CF{'maspas'}&&($IN{'pass'}eq$CF{'maspas'})){
      #Revise Main Routin
      &header;
      print qq[<h2 class="mode">- ��$IN{'i'}�֤�$IN{'j'}�ν����⡼�� -</h2>\n];
      $DT{'i'}="$IN{'i'}";
      $DT{'j'}="$IN{'j'}";
      $DT{'pass'}='';
      $DT{'oldps'}="$IN{'pass'}";
      &rvsij(\%DT);
      &footer;
      exit;
    }else{
      &rvsmenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���");
    }
  }else{
    #Cookie�ˤ��롩
    &getck;
    $IN{'pass'}=$CK{'pass'};

    #-----------------------------
    unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
      #̵���ʤ����Ϥ���
      &header;
      print<<"_HTML_";
<h2 class="mode">- ��$IN{'i'}�֤�$IN{'j'}�Υѥ����ǧ�� -</h2>
<form accept-charset="euc-jp" id="Revise" method="post" action="$CF{'index'}">
<table cellspacing="2" summary="Revise" width="550">
<col width="50">
<col width="170">
<col width="330">
<p style="margin:0.6em">�ѥ���ɤ����Ϥ��Ƥ�������</p>
<p style="margin:0.6em"><span class="ak">P</span>assword:
<input name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
<input type="hidden" name="rvs" value="$IN{'rvs'}"></p>
<p style="margin:0.6em">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">��
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="����󥻥�">
</p>
_HTML_
      &footer;
      exit;
    }
  }
  #Revise Main Routin
  &header;
  print qq[<h2 class="mode">- ��$IN{'i'}�֤�$IN{'j'}�ν����⡼�� -</h2>\n];
  $DT{'i'}="$IN{'i'}";
  $DT{'j'}="$IN{'j'}";
  $DT{'pass'}="$IN{'pass'}";
  $DT{'oldps'}="$IN{'pass'}";
  &rvsij(\%DT);
  &footer;

  exit;
}


#-------------------------------------------------
# �������

sub delete{
  ($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});

  sysopen(RD,"$CF{'log'}$IN{'i'}.cgi",O_RDONLY)||die"Can't open log$IN{'i'}!";
  flock(RD,LOCK_SH);
  my@log=<RD>;
  close(RD);
  my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

  SWITCH:{
    if($CF{'maspas'}&&($IN{'pass'}eq$CF{'maspas'})){
      if(($IN{'j'}eq'0')&&(!$IN{'type'})){
        #̵���ʤ����Ϥ���
        &header;
        print<<"_HTML_";
<h2 class="mode">- ��$IN{'i'}�֥���åɤκ�� -</h2>
<form accept-charset="euc-jp" id="Delete" method="post" action="$CF{'index'}">
<fieldset style="padding:0.5em;width:60%">
<legend>����åɤκ����ˡ������Ǥ�������</legend>
_HTML_
        my$i=<<"_HTML_";
<td>
<label for="mark">�Ƶ�������ʸ�Τߺ��<input id="mark" name="del" type="radio" value="$IN{'del'}-1"></label>
<label for="$CF{'del'}">��������åɤ���<input id="$CF{'del'}" name="del" type="radio" value="$IN{'del'}-2"></label>
_HTML_
        $i=~s/(id=\"$CF{'del'}\")/$1 checked="checked"/o;
        print<<"_HTML_";
$i
</fieldset>

<p style="margin:0.6em">
<input name="pass" type="hidden"  value="$IN{'pass'}">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">��
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="����󥻥�">
</p>
_HTML_
        &footer;
        exit;
      }
      (($IN{'j'}eq'0')&&($IN{'type'}==2))&&(last SWITCH);
    }else{
      (&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'}))
       ||(&rvsmenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���"));
      (($IN{'j'}eq'0')&&($#log==0))&&(last SWITCH);
    }
    
    #mark
    $log[$IN{'j'}]=~s/^Mir1=\t([^\t]*);\t/Mir1=\tdel;\t/go;
    my$data=join('',@log);
    
    sysopen(WR,"$CF{'log'}$IN{'i'}.cgi",O_WRONLY|O_TRUNC)||die"Can't write log$IN{'i'}!";
    flock(WR,LOCK_EX);
    print WR $data;
    close(WR);
    &rvsmenu("��$IN{'i'}�֤�$IN{'j'}�������ޤ�����('mark')");
  }
  #�Ƶ������
  if($CF{'del'}eq'unlink'){
    #���
    unlink"$CF{'log'}$IN{'i'}.cgi"||die"Can't delete log$IN{'i'}!";
    &rvsmenu("��$IN{'i'}�֥���åɤ������ޤ�����('unlink')");
  }elsif($CF{'del'}eq'rename'){
    #�ե�����̾�ѹ�
    rename("$CF{'log'}$IN{'i'}.cgi","$CF{'log'}$IN{'i'}.cgi.bak")||die"Can't rename log$IN{'i'}!";
    &rvsmenu("��$IN{'i'}�֥���åɤ������ޤ�����('rename')");
  }
  exit;
}


#-------------------------------------------------
# ��ʸ������ǽ
#

#�ޤ�AND,OR�����Τ褦�ʹ��٤ʵ�ǽ�ϼ������Ƥ��ʤ�
#���ʤߤˡ���ʸ�פȤ����Τϵ���Ǥʤ���ʸ���̤����ʸ����פǤ���
#index�ؿ���Ȥ����Ȥˤ���®����ޤäƤ��롢���Ĥ�ꡣ
sub seek{
  &header;
  print qq[<h2 class="mode">- �����⡼�� -</h2>];
  if(length$IN{'seek'}){
    #-----------------------------
    #�������ɽ��
    my$j='';
    &logfiles('number');
    for(@file){
      ($_)||(last);
      sysopen(RD,"$CF{'log'}$_.cgi",O_RDONLY)||die"Can't open log$_!";
      flock(RD,LOCK_SH);
      my$log=join('',<RD>);
      close(RD);
      (index($log,$IN{'seek'})>-1)&&($j.=qq{<a href="$CF{'index'}?read=$_#$_">No.$_</a>\n});
    }
    print"<p>��$IN{'seek'}�פǸ���������̡�<br>";
    if($j){print"�ʲ��Υ���åɤǸ���ñ���ȯ�����ޤ�����</p>$j";
    }else{print'<p>����ñ���ȯ���Ǥ��ޤ���Ǥ���</p>';}
  }
  print<<"_HTML_";
<form accept-charset="euc-jp" id="seek" method="post" action="$CF{'index'}">
<p>��������ñ��(<span class="ak">W</span>)
<input type="text" name="seek" id="seek" class="blur" accesskey="w" style="ime-mode:active;width:200px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$IN{'seek'}">
</p>
<p>
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">��
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="����󥻥�">
</p>
</form>
<h2 class="mode">���</h2>
<pre style="text-align:center">
���θ��������ƥ��ϫ�Ϸڸ��Τ��ᡢ
�������Ƥι��ܤ��Ф���礷��Ƚ���ԤäƤ��ޤ���
��ä�̾���˥ҥåȤ����Τ��������Ȥ˥ҥåȤ����Τ��ϸ��ߤ狼��ޤ���

�ޤ�������ñ�줬����å���Τɤ��˽ФƤ������Ϲͤ��Ƥ��ޤ���
�֥饦���Υڡ����⸡����ǽ�ʤɤ�ȤäƤ�������^^;;
</pre>
_HTML_
  &footer;

  exit;
}


#------------------------------------------------------------------------------#
# HTTP,HTML,Page�إå�����ޤȤ�ƽ��Ϥ���
#
sub header{
  print<<"_HTML_";
Content-type: text/html; charset=euc-jp
Content-Language: ja
_HTML_

#GZIP����ž���⤫������Ȥ��Ϥ�����
#CSS���б���IE3�ʲ���NN4�ϳ���CSS���ɤ߹��ޤ��ʤ�
  #GZIP Switch
  if((-x$CF{'gzip'})&&($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/io)){
    print"Content-encoding: gzip\n\n";
    open(STDOUT,"| $CF{'gzip'} -1 -c")||die"Can't use GZIP!";
    print"<!-- gzip enable -->\n";
  }else{print"\n<!-- gzip disable -->\n";}

  print<<'_HTML_';
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
_HTML_
  #CSS Switch
  CSS:{
    if($ENV{'HTTP_USER_AGENT'}=~m/MSIE 3/o){
      #IE3��NG
      last CSS;
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4.*compatible}o){
      #Mozilla/4�ߴ����̤�
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4}o){
      #Netscape4�ϥ���
      last CSS;
    }
    #����ʳ��ˤϰ���Ϥ��Ƥ���
    print qq{<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">\n};
  }
  #LastPost
  unless(%Z0){
    sysopen(ZERO,"$CF{'log'}0.cgi",O_RDONLY)||die"Can't write log0!";
    flock(ZERO,LOCK_SH);
    my@zero=<ZERO>;
    close(ZERO);
    ($zero[0]=~/^Mir1=\t/o)||(die"��������Mir1���ʳ��Ǥ�");
    %Z0=($zero[0]=~m/([^\t]*)=\t([^\t]*);\t/go);
    @zer2=split(/ /,$zero[2]);
  }
  my$date=&date($Z0{'time'});
  print<<"_HTML_";
<link rel="start" href="$CF{'home'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>$CF{'title'}</title>
</head>
<body>
<p class="lastpost">
<a href="index.cgi?read=$Z0{'Mir1'}#$Z0{'Mir1'}">Lastpost: $date $Z0{'name'}</a></p>
$CF{'head'}
$CF{'menu'}
_HTML_
#  eval qq{print<<"_HTML_";\n$CF{'menu'}\n_HTML_};
}


#-------------------------------------------------
# �����Խ����
#
sub rvsij{
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}

  #�ǡ������᤹
  $DT{'body'}=~s/<br>/\n/go;#"<br>"2"\n"
  $DT{'body'}=~s/<\/?a[^>]*>//go;#ClearAnchors
  $DT{'body'}=~s/</&#60;/go;
  $DT{'body'}=~s/>/&#62;/go;

  if($DT{'j'}){
    #�ҵ���
    &chdfrm(\%DT);
  }else{
    #�Ƶ���
    &prtfrm(\%DT);
  }
}


#-------------------------------------------------
# �����ֿ�
#
sub res{
  &getck;
  &header;

  print qq[<h2 class="mode">- Response Mode -</h2>\n];
  (&article('i'=>$IN{'i'},'ak'=>1,'res'=>1)eq'del')&&(print"This thread$IN{'i'} is deleted.");

  &chdfrm(\%CK,'i'=>$IN{'i'},'ak'=>1);
  &footer;
  exit;
}


#-------------------------------------------------
# ����ɽ��
#

#���Υ��֥롼�������1����åɤ���Ϥ���
#RES�ե��������°�����뤫�����꼡�衢��
#�ΤϤ����ä�������������ꥹ�Ȥ����粽��ȼ�ʤ���
#JavaScript�ˤ���ǳ�������ޤ�����档��
sub article{
  #���Υ���åɶ��̤ξ���
  my%DT=@_;
  my$new=0;
  $DT{'j'}=-1;
  
  sysopen(RD,"$CF{'log'}$DT{'i'}.cgi",O_RDONLY)||die"Can't open log$DT{'i'}!";
  flock(RD,LOCK_SH);
  while(<RD>){
    $DT{'j'}++;
    if($DT{'j'}eq'0'){
      #�Ƶ���
      &artprt(\%DT);
    }else{
      #�ҵ���
      ($_=~/^Mir1=\tdel;\t/o)&&(next);#�����������
      &artchd(\%DT);
    }
  }
  close(RD);
  ($DT{'j'}<0)&&(return);
  #�����եå�
  &artfot(\%DT);
  return$new;#̤�ɵ����η�����֤�
}


#-------------------------------------------------
# �ڡ�������TABLE
#
sub pgslct{
  my$i=$IN{'page'}-1;
  my$j=$IN{'page'}+1;
  my$k='';
  my@page=();
  my@key=('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9�ڡ�����AccessKey
  ($_[1])&&($k=";$_[1]");

  #pageɽ��Ĵ��
  my$per=20;
  my$hal=int($per/2);
  my$str=0;
  my$end=0;

  #�ɤ�����ɤ��ޤ�
  if($_[0]<=$per){
    $str=1;
    $end=$_[0];
  }elsif($IN{'page'}-$hal<1){
    #1-10
    $str=1;
    $end=$per;
    ($end>$_[0])&&($end=$_[0]);
  }elsif($IN{'page'}+$hal>=$_[0]){
    #(max-10)-max
    $str=$_[0]-$per+1;
    $end=$_[0];
  }else{
    $str=$IN{'page'}-$hal+1;
    $end=$IN{'page'}+$hal;
  }

  #�����
  for($str..$end){
    ($_==$IN{'page'})&&(push(@page,qq(<strong class="pgsl">$_</strong>)),next);
    if($key[$_]){
      push(@page,qq(<a accesskey="$key[$_]" href="$CF{'index'}?page=$_$k">$_</a>));
    }else{
      push(@page,qq(<a href="$CF{'index'}?page=$_$k">$_</a>));
    }
  }

  #�ǽ�ȺǸ�
  ($str!=1)&&(unshift(@page,qq(<a accesskey="&#60;" href="$CF{'index'}?page=1$k">1</a>&lt;&lt;)));
  ($end!=$_[0])&&(push(@page,qq(&gt;&gt;<a accesskey="&#62;" href="$CF{'index'}?page=$_[0]$k">$_[0]</a>)));

  #�ҤȤ�����
  $i=($IN{'page'}==1)?'[�ǿ�]':qq[<a accesskey="," href="$CF{'index'}?page=$i$k">&#60; ���</a>];
  $j=($_[0]-$IN{'page'})?qq[<a accesskey="." href="$CF{'index'}?page=$j$k">�Τ� &#62;</a>]:'[�Ǹ�]';

  #��������
  return<<"_HTML_";
<table cellspacing="0" class="pgsl" summary="PageSelect">
<col style="width:3.5em">
<col>
<col style="width:3.5em">
<tr><td>$i</td>
<td>[ @page ]</td>
<td>$j</td>
</tr>
</table>
_HTML_
}


#-------------------------------------------------
# Location��ž��
#
sub locate{
  my$i;
  if($_[0]=~/^http:/o){
    $i=$_[0];
  }elsif($_[0]=~/\?/o){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=sprintf('%s?%s',$_[0]);
  }elsif($_[0]){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=$_[0];
  }
  print<<"_HTML_";
Location: $i
Content-Type: text/html
Pragma: no-cache
Cache-Control: no-cache

<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<meta http-equiv="Refresh" content="0;URL=$i">
<title>301 Moved Permanently</title>
</head>
<body>
<h1>: Mireille :</h1>
<p>And, please go <a href="$i">here</A>.</p>
<p>Location: $i</p>
<p>Mireille <var>$CF{'corver'}</var>.<br>
Copyright &#169;2001 <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix">Airemix</a>. All rights reserved.</p>
</body>
</html>
_HTML_
  exit;
}

#------------------------------------------------------------------------------#
# Sub Routins
#

#-------------------------------------------------
# Form���Ƽ���
#

#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
#�Ǹ����ƻ�����Τ餻��
sub getfm{
  my$i='';
  my%DT;
  if($ENV{'REQUEST_METHOD'}eq'HEAD'){ #forWWWD
    my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'last');
    print"Last-Modified: $last\n";
    print"Content-Type: text/plain\n\n";
    exit;
  }elsif($ENV{'REQUEST_METHOD'}eq'POST'){
    read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
  }elsif($ENV{'REQUEST_METHOD'}eq'GET'){
    $i=$ENV{'QUERY_STRING'};
  }

  if(length$i>262114){
    #����������
    &header;
    print"������ʤ�Ǥ��̤�¿�����ޤ�\n$i";
    &footer;
    exit;
  }elsif(length$i>0){
    # EUC-JPʸ��
#   $ascii='[\x00-\x7F]'; # 1�Х��� EUC-JPʸ��
    my$ascii='[\x09\x0A\x0D\x20-\x7E]'; # 1�Х��� EUC-JPʸ����
    my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2�Х��� EUC-JPʸ��
    my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3�Х��� EUC-JPʸ��
    my$character="(?:$ascii|$twoBytes|$threeBytes)"; # EUC-JPʸ��
    
    #���Ϥ�Ÿ�����ƥϥå���������
    for(split(/[&;]/o,$i)){
      my($i,$j)=split('=',$_,2);
      (defined$j)||($DT{$i}='',next);
      study$j;
      $j=~tr/+/\ /;
      $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
      $j=($j=~m/($character*)/o)?"$1":'';
      $j=~s/\t/\ \ /go;
      $j=~s/"/&#34;/go;
      $j=~s/&(#?\w+;)?/($1)?"&$1":'&#38;'/ego;
      $j=~s/'/&#39;/go;
  
      if($CF{'tags'}&&('body'eq$i)){
        #��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
        my$tags=$CF{'tags'};
        $j=~s/</&#60;\t/go;
        $j=~s/>/&#62;\t/go;
        $j=~s{&#60;\t(/?)(\w+)([^\t]*)&#62;\t}
         {my($a,$b,$c)=($1,$2,$3);($tags=~m/\b$2\b/io)?"<$a$b>":"&#60;$a$b$c&#62;"}ego;
        $j=~tr/\00\t//d;
      }else{
        $j=~s/</&#60;/go;
        $j=~s/>/&#62;/go;
      }
  
      $j=~s/\x0D\x0A/<br>/go;$j=~s/\x0D/<br>/go;$j=~s/\x0A/<br>/go;
      $j=~s/(<br>)+$//o;
      $DT{$i}=$j;
    }
  }

  #�������Ϥα�������
  if(defined$DT{'body'}){#�����񤭹���
    #HTTP URL ����ɽ��
    my$http_URL_regex =
   q{\b(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f}.
   q{][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)}.
   q{*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.}.
   q{[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]}.
   q{[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-}.
   q{Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f}.
   q{])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)}.
   q{*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])}.
   q{*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{)?};
    #FTP URL ����ɽ��
    my$ftp_URL_regex =
   q{\bftp://(?:(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*} .
   q{(?::(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?} .
   q{:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z](?:[-a-zA-} .
   q{Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)?} .
   q{(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?} .
   q{:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(?:;type=[} .
   q{AIDaid])?)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9} .
   q{A-Fa-f])*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A} .
   q{-Fa-f])*)?};
    #MAIL ����ɽ��
    my$mail_regex=
   q{(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
   .q{\[\]\000-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
   .q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x}
   .q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff])|"[^\\\\\x80-}
   .q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
   .q{\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
   .q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
   .q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,}
   .q{;:".\\\\\[\]\000-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
   .q{^\x80-\xff])*\]))*};

    #ɬ��
    $DT{'body'}=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
    {my($org,$mail)=($1,$2);(my$tmp=$org)=~s/"/&#34;/go;
    '<a class="user" href="'.($mail ne''?'mailto:':'')."$tmp\" target=\"_blank\">$org</a>"}ego;
    $IN{'body'}=($DT{'body'}=~/(.+)/o)?"$1":'';
    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?"$1":'';
    $IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
    if($DT{'pass'}eq$CF{'maspas'}){
      $IN{'pass'}=$CF{'maspas'};
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    if($DT{'oldps'}eq$CF{'maspas'}){
      $IN{'oldps'}=$CF{'maspas'};
    }else{
      $IN{'oldps'}=($DT{'oldps'}=~/(.{1,24})/o)?"$1":'';
    }
    (($DT{'i'}=~/(\d+)/o)&&$1)&&($IN{'i'}=$1);
    ($DT{'j'}=~/(\d+)/o)&&($IN{'j'}=$1);

    if($IN{'j'}eq'0'){
      #�Ƶ���
      for($CF{'prtitm'}=~m/\b([a-z\d]+)\b/go){
        if('color'eq$_){
          $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
        }elsif('email'eq$_){
          $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
          $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
        }elsif('home'eq$_){
          $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
          $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
        }elsif('icon'eq$_){
          $IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
        }elsif('cmd'eq$_){
          ($DT{'cmd'}=~/(.+)/o)&&($IN{'cmd'}="$1");
        }elsif(('ra'eq$_)||('hua'eq$_)){
          next;
        }else{
          $IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
        }
      }
      
    }elsif($IN{'i'}){
      #�ҵ���
      for($CF{'chditm'}=~m/\b([a-z\d]+)\b/go){
        if('color'eq$_){
          $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
        }elsif('email'eq$_){
          $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
          $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
        }elsif('home'eq$_){
          $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
          $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
        }elsif('icon'eq$_){
          $IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
        }elsif('cmd'eq$_){
          ($DT{'cmd'}=~/(.+)/o)&&($IN{'cmd'}="$1");
        }elsif(('ra'eq$_)||('hua'eq$_)){
          next;
        }else{
          $IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
        }
      }
    }else{
      die"Something Wicked happened!";
    }
  }elsif($DT{'i'}){
  #�ֿ�
    $IN{'i'}=($DT{'i'}=~/(\d+)/o)?$1:undef;
  }elsif(defined$DT{'j'}){
  #�����񤭹���
    $IN{'j'}=($DT{'j'}=~/(\d+)/o)?$1:0;
  }elsif(defined$DT{'seek'}){
  #����
    $IN{'seek'}=($DT{'seek'}=~/(.+)/o)?"$1":'';
  }elsif(defined$DT{'del'}){
  #��������ꥹ��or�¹�
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
    if($DT{'pass'}eq$CF{'maspas'}){
      $IN{'pass'}=$CF{'maspas'};
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    $IN{'del'}=($DT{'del'}=~/(\d+\-\d+(-\d)?)/o)?"$1":'';
  }elsif(defined$DT{'rvs'}){
  #���������ꥹ��or�¹�
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
    if("$DT{'pass'}"eq"$CF{'maspas'}"){
      $IN{'pass'}="$CF{'maspas'}";
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    $IN{'rvs'}=($DT{'rvs'}=~/(\d+\-\d+)/o)?"$1":'';
  }elsif(defined$DT{'help'}){
  #����
    return($IN{'help'}=1);
  }elsif(defined$DT{'home'}){
  #�ۡ���
    return($IN{'home'}=1);
  }elsif(defined$DT{'new'}){
  #�����񤭹���
    $IN{'j'}=0;
  }elsif(defined$DT{'res'}){
  #�ֿ��񤭹���
    (($DT{'res'}=~/(\d+)/o)&&$1)&&($IN{'i'}=$1);
  }elsif(defined$DT{'compact'}){
    #����ü���⡼��
    require './compact.cgi';
  }elsif($DT{'read'}){
  #���ɤ�
      (($DT{'read'}=~/(\d+)/o)&&$1)&&($IN{'read'}=$1);
  }else{
  #�ڡ���
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
  }
  $IN{'ra'}=($ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
  $IN{'hua'}=($ENV{'HTTP_USER_AGENT'}=~/([^\t]+)/o)?"$1":'';
  return%IN;
}

#-------------------------------------------------
# Cookie���������
#
sub getck{
  ($ENV{'HTTP_COOKIE'}=~/(.+)/o)||(return undef);
  my$cookie="$1";
  for(split('; ',$cookie)){
    my($i,$j)=split('=',$_,2);
    ('Mireille'ne$i)&&(next);
    $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    %CK=split("\t",$j);
    last;
  }
  return%CK;
}

#-------------------------------------------------
# Cookie�񤭹���
#
sub wrtcook{
  my%DT=%{shift()};
  for(keys%CK){
    (length$DT{"$_"})||($DT{"$_"}=$CK{"$_"});
  }
  my$cook='';
  my$time=0;
  my$expire=0;
  if($CK{'expire'}>$^T){
    #������
    $time=$CK{'time'};
    $expire=$CK{'expire'};
  }elsif($CK{'expire'}>0){
    #�����ڤ�
    $time=$CK{'expire'}-$CF{'newuc'};
    $expire=$^T+$CF{'newuc'};
    $CK{'time'}=$time;
  }else{
    #����
    $time=$^T;
    $expire=$^T+$CF{'newuc'};
    $CK{'time'}=$^T-$CF{'newnc'};
  }
    $cook="name\t$DT{'name'}\tpass\t$DT{'pass'}\ttime\t$time\texpire\t$expire";
  for($CF{'cokitm'}=~m/\b([a-z\d]+)\b/go){
    $cook.=qq(\t$_\t$DT{$_});
  }
  $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
  my$gmt=&datef(($^T+20000000),'gmt');
  print"Set-Cookie: Mireille=$cook; expires=$gmt\n";
}

#-------------------------------------------------
# �ե����ޥåȤ��줿���ռ������֤�
sub datef{
  unless($_[1]){
  }elsif($_[1]eq'gmt'){
   # Cookie��
    return sprintf("%s, %02d-%s-%d %s GMT",(split/\s+/o,gmtime($_[0]))[0,2,1,4,3]);
  }elsif($_[1]eq'last'){
   # LastModified��
    return sprintf("%s, %02d %s %s %s GMT",(split/\s+/o,gmtime($_[0]))[0,2,1,4,3]);
  }
  return&date;
}

#-------------------------------------------------
# ��������åɥե�����Υꥹ�Ȥ����
#

#���ե�����̾���������
#�����ֹ����Ϲ��������˴�Ť����¤��ؤ���
#�ե�����̾�ֹ�Υꥹ�Ȥ��֤�
sub logfiles{
  undef@file;
  opendir(DIR,$CF{'log'});
  for(readdir(DIR)){
    (($_=~/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
  }
  closedir(DIR);
  
  if($_[0]eq'date'){
    #���ս� 'date'
    @file=sort{$zer2[$b-$zer2[0]]<=>$zer2[$a-$zer2[0]] or $b<=>$a}@file;
  }else{
    #�����ֹ�� 'number'
    @file=sort{$b<=>$a}@file;
  }
  push(@file,0);
  return@file;
}

#-------------------------------------------------
# �ѥ���ɰŹ沽
sub mircrypt{
  srand($_[0]);
  my$m='abcdefghijklmnopqrstuvwxyz.0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  my$n=substr($m,int(rand(64)),1);
  $n.=substr($m,int(rand(64)),1);
  my$pass='';
  for($_[1]=~m/(.{1,8})/go){
    (length$_)||(next);
    $_=crypt($_,$n);
    substr($_,0,2,'');
    $pass.=$_;
  }
  ($_[2])||(return$pass);
  $IN{'newps'}=$pass;
  ($IN{'newps'}eq$_[2])&&(return 1);#OK
  return undef;#NG
}


1;
__END__
