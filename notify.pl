#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Notify Module-
#
$CF{'Notify'}=q$Revision$;
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use strict;
use vars qw(%CF);

$CF{'Exte'}.=qq(notify: $CF{'Notify'}\n);

sub mailnotify{
	#お知らせの送り先
	$CF{'mailto'}='me@mysite.jp';
	#除外メールアドレス
	$CF{'myself'}='me@mysite.jp myself@mysite.jp';
	#sendmailのパス
	$CF{'sendmail'}='sendmail';
	#親記事のとき知らせる項目
	$CF{'prtntf'}='subject name time icon email home color ra hua body';
	#子記事のとき知らせる項目
	$CF{'chdntf'}='name time icon email home color ra hua body';
#ra:REMOTE_ADDR			例「127.0.0.1」
#hua:HTTP_USER_AGENT	例「Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)」


	#投稿された記事のメールアドレスと、送り先アドレスが同じなら、メールを送らない
	my%DT=('time'=>$^T,@_);
	(" $CF{'myself'} "=~m/ $DT{'email'} /o)&&(return 2);
	# 記事の改行・タグを復元
	for(keys%DT){
		$DT{"$_"}=~s/<BR[^>]*>/\x0A/gio;
		$DT{"$_"}=~s/&#38;/&/go;
		$DT{"$_"}=~s/&#34;/"/go;
		$DT{"$_"}=~s/&#39;/'/go;
		$DT{"$_"}=~s/&#60;/</go;
		$DT{"$_"}=~s/&#62;/>/go;
	}
	#投稿日時表示用
	my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($DT{'time'});
	$DT{'time'}=sprintf("%4d年%02d月%02d日(%s) %02d時%02d分" #"1970年01月01日(木) 09時00分"の例
	,$year+1900,$mon+1,$mday,('日','月','火','水','木','金','土')[$wday],$hour,$min);

	#題名（2バイト文字はたぶん使えません）
	my$Subject = "Mireille Notify $DT{'i'}-$DT{'j'}";
	#本文
	my$Body='';
	if($DT{'j'}eq 0){
		for(split(/\s/,$CF{'prtntf'})){
			(length$DT{$_})&&($Body.=qq($_:$DT{$_}\n));
		}
	}elsif($DT{'j'}){
		for(split(/\s/,$CF{'prtntf'})){
			(length$DT{$_})&&($Body.=qq($_:$DT{$_}\n));
		}
	}else{die"Something Wicked happend";}

	# JISコード変換
	$Subject=jcode::e2j($Subject);
	$Body=jcode::e2j($Body);

	open(MAIL,"| $CF{'sendmail'} -t")||die"Can't use sendmail.";
	print MAIL <<"_HTML_";
To: $CF{'mailto'}
From: Mireille\@$ENV{'SERVER_NAME'}
Subject: $Subject
MIME-Version: 1.0
Content-type: text/plain; charset=iso-2022-jp
Content-Transfer-Encoding: 7bit
X-Mailer: Mireille $CF{'Notify'}

$Body
_HTML_
	close(MAIL);
	return 1;
}

#以下漢字コード変換
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
