#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - MireilleNotify -
#
#BEGIN{$main::version=q$Revision$;}
# "This file is written in euc-jp, LF." ��
# Scripted by NaRuSe.
#------------------------------------------------------------------------------#
use strict;
use vars qw(%CF);
sub mailnotify{
  #���Τ餻��������
  $CF{'mailto'}='me@mysite.jp';
  #�����᡼�륢�ɥ쥹
  $CF{'myself'}='me@mysite.jp myself@mysite.jp';
  #sendmail�Υѥ�
  $CF{'sendmail'}='/usr/sbin/sendmail';

  #��Ƥ��줿�����Υ᡼�륢�ɥ쥹�ȡ������襢�ɥ쥹��Ʊ���ʤ顢�᡼�������ʤ�
  my%DT=('time'=>$^T,@_);
  (" $CF{'myself'} "=~m/ $DT{'email'} /o)&&(return 2);
  # �����β��ԡ�����������
  for(keys%DT){
    $DT{"$_"}=~s/<br>/\x0A/go;
    $DT{"$_"}=~s/&#38;/&/go;
    $DT{"$_"}=~s/&#34;/"/go;
    $DT{"$_"}=~s/&#39;/'/go;
    $DT{"$_"}=~s/&#60;/</go;
    $DT{"$_"}=~s/&#62;/>/go;
  }
  #�������ɽ����
  my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($DT{'time'});
#  my@wdays=qw(Sun Mon Tue Wed Thu Fri Sat);
  my@wdays=qw(�� �� �� �� �� �� ��);
  $wday="($wdays[$wday])";
  ($year<1900)&&($year+=1900);
#  return sprintf("%4d/%02d/%02d%s %02d:%02d",$year,$mon+1,$mday,$wday,$hour,$min);
  $DT{'time'}=sprintf("%4dǯ%02d��%02d��%s %02d��%02dʬ",$year,$mon+1,$mday,$wday,$hour,$min);

  #��̾��2�Х���ʸ���ϻȤ��ޤ����
  my$Subject = "Mireille Notify $DT{'i'}-$DT{'j'}";
  #��ʸ
  my$Body=<<"_HTML_";
��������$DT{'i'}-$DT{'j'}
����̾��$DT{'subject'}
��̾����$DT{'name'}
�����$DT{'time'}
��Icon��$DT{'icon'}
��Mail��$DT{'email'}
��Home��$DT{'home'}
��������$DT{'color'}
��REMOTE_ADDR��$DT{'ra'}
��HTTP_USER_AGENT��$DT{'hua'}
����ʸ��
$DT{'body'}
_HTML_

  # JIS�������Ѵ�
#  $Subject=jcode::e2j($Subject);
  $Body=jcode::e2j($Body);

  open(MAIL,"| $CF{'sendmail'} -t")||die"Can't use sendmail.";
  print MAIL <<"_HTML_";
To: $CF{'mailto'}
From: Mireille\@$ENV{'SERVER_NAME'}
Subject: $Subject
MIME-Version: 1.0
Content-type: text/plain; charset=iso-2022-jp
Content-Transfer-Encoding: 7bit
X-Mailer: Mireille $main::version
X-Moe: Undefined

$Body
_HTML_
  close(MAIL);
  return 1;
}

#�ʲ������������Ѵ�
package jcode;
;# jcode.pl: Perl library for Japanese character code conversion
;# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
;#  ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/

;# EUC to JIS
sub e2j{
  my$s=$_[0];
  $s=~s/(([\241-\376]{2}|\216[\241-\337]|\217[\241-\376]{2})+)/&_e2j($1)."\e(B"/geo;
  return$s;
}
sub _e2j{
  my($s)=shift;
  $s=~s/(([\241-\376]{2})+|(\216[\241-\337])+|(\217[\241-\376]{2})+)/&__e2j($1)/geo;
  return$s;
}
sub __e2j{
  my($s)=shift;
  my$esc;
  if($s=~tr/\216//d){
	$esc="\e(I";
  }elsif($s=~tr/\217//d){
	$esc="\e\$(D";
  }else{
	$esc="\e\$B";
  }
  $s=~tr/\241-\376/\041-\176/;
  $esc.$s;
}

1;
__END__
