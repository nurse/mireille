#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Log Converter to Mir12 -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
use strict;
use vars qw(%CF);

=item �Ȥ���

�ޤ����֤��ޤ��礦
���̥ե��������ष�ơ�convert12.cgi������򤷤ޤ�

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

����ʾ��֤����֤��Ƥ��ꡢ
Mir10�ǥ��쥯�ȥ�ˤ� Mireille1.0 ��
Mir11�ǥ��쥯�ȥ�ˤ� Mireille1.1 ��
MTP164g�ǥ��쥯�ȥ�ˤ�Multi Talk PRIVATE rel 0.1.64g�����äƤ����硢
���줾�졢

#Mir10
$CF{'oldlog'}='../Mir10/log/';
#CF{'from'}='Mir10';

#Mir11
$CF{'oldlog'}='../Mir11/log/';
#CF{'from'}='Mir11';

#MTP164g
$CF{'oldlog'}='../MTP164g/1_data.cgi'
#CF{'from'}='MTP164g';

�����ꤷ�ޤ�

�����ơ�convert12.cgi�Τ����Ƥ��롢Mir12�ǥ��쥯�ȥ��log�ǥ��쥯�ȥ�ˤ����Ѵ���̤���¸���������

$CF{'log'}='./log/';

�Ȥ��ޤ�

���ξ��convert12.cgi�˥֥饦�����饢���������ޤ��礦
�����ԤƤФ��줾��η�������1.2�������Ѵ����졢�Ǽ������Τ���Ȥ���褦�ˤʤ�ޤ�
��Mir12�ǥ��쥯�ȥ�ηǼ��Ĥ�����������ꤵ��Ƥ���С�

���ٹ�!!
���κ�Ȥ�Ԥ����Ѵ���Υǥ��쥯�ȥ�Υ��ե�����ϡ�
�ʾ����Ǥ�Mir12�ǥ��쥯�ȥ����log�ǥ��쥯�ȥ�Υե�����)
�Ѵ���̤Ǿ�񤭤���Ƥ��ޤ����ᡢ�ä��Ƥ��ޤ��ޤ�
ɬ�����������֤�����Τ���ꤷ�Ƥ�������

�����
�Ѵ���Υǥ��쥯�ȥ�Ϥ��餫�����äƤ����ʤ��ȥ��顼���Фޤ�

=item �б�����

Mireille 1.0����
Mireille 1.1����
Mireille 1.2�����¡�1.2.1.1, 1.2.1.2�Ǥλ��������
Multi Talk PRIVATE rel 0.1.64g����
��Mireille 1.2�������Ѵ����ޤ�

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
/* �̾�Υ��ʸ�� */
a:link		{color:#44f;text-decoration:none;}
a:visited	{color:#44f;text-decoration:none;}
a:hover		{color:#fa8;text-decoration:underline;}
a:active	{color:#f00;text-decoration:underline;}
body{
	background-color: #fff;
	border-style: none;
	color: #355;
	font-family: '�ͣ� �Х����å�',Osaka,sans-serif;
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
	font-family: '�ͣ� �����å�',Osaka,monospace;
	font-size: 85%;
	font-weight: normal;
	margin: 0.2em 1em;
	text-align: left;
	white-space: pre;
	word-break: break-all;
}
/* ---------- �ڡ����إå����ơ��֥� ---------- */
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
	font-family: 'Comic Sans MS','�ͣ� �Х����å�',Osaka,sans-serif;
	font-size: 19px;
	font-weight: normal;
}
h1.head{margin: 0;}
h1.head a:visited{color: #fff;}
/* ---------- ���Ф���Modeɽ���Ǽ�˻��ѡ� ---------- */
h2.mode{
	background-color: #ace;
	color: #fff;
	font-family: 'Comic Sans MS','�ͣ� �Х����å�',Osaka,sans-serif;
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
<td nowrap>��������������</td>
</tr></table></div>

_HTML_
	if(!$ENV{'REQUEST_METHOD'}||'GET'eq$ENV{'REQUEST_METHOD'}){
		print<<"_HTML_";
<h2 class="mode">���ե�������Ѵ��򤷤ޤ��衩</h2>
<pre style="text-align:left;width:60%">
Mireille Log Converter to Mireille'Mir12'�����Ѥ��������ɤ��⤢�꤬�Ȥ��������ޤ�
���줫�餳��CGI��"$CF{'oldlog'}"����¸����Ƥ��롢"$CF{'from'}"�����Υ���
Mir12�������Ѵ�������ǡ�"$CF{'log'}"����¸���ޤ�

���ν����ϤǤ��ޤ����Ǥ��礦��
�Хå����åפϤȤ�ޤ�������
���ե�������Ѵ��˺ݤ������ǡ�������»�����Ȥ��Ƥ⡢
Airemix�Ϥ�����Ǥ�ϰ��ڼ��ޤ����Ʊ��Ϥ��ޤ����ɡ�
���ν������Ǥ��ޤ����顢�����Ρֳ��ϡפ򲡤��Ƥ�������
�����򤪵��ꤤ�����ޤ�


</pre>
<form method="post" action="convert12.cgi">
<p><input type="hidden" name="mode" value="exec">
<input type="submit" value="����" style="height:30px;width:100px"></p>
</form>
_HTML_
	}elsif('POST'eq $ENV{'REQUEST_METHOD'}){
		($CF{'oldlog'}&&$CF{'from'}&&$CF{'log'})||die"����������Ǥ��Ƥʤ��ߤ����Ǥ�";

		my($from,@convert)=&convert();
		my$convert=@convert;
		print<<"_HTML_";
<h2>���ե�������Ѵ��ϴ�λ���ޤ���</h2>


<pre style="text-align:left;width:60%">
������Ԥä�����
���� $from���� ���� Mireille'Mir12'���� �ؤ��Ѵ�

�������η��
$convert�ĤΥե������ Mir12���� ���Ѵ����ޤ���

������ե�����"0.cgi"��Mir12�����ؤ��Ѵ�
���Ѵ��������ե�����
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
		print qq(<h2 class="mode">���餫�Υ��顼�������ޤ���[$ENV{'REQUEST_METHOD'}]</h2>);
	}
	print<<"_HTML_";
<div class="center"><table align="center" border="0" cellspacing="0" class="head" summary="Footer" width="90%"><tr>
<td nowrap>��������������</td>
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
	return('���顼',('���顼'));
}


#-------------------------------------------------
# From Mireille 1.0.x
sub fromMir10{
	#ZeroFile�ξ���õ��
	my$logext; #����ĥ��
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
	
	#�ե��������
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
		
		$log[0]=~/^Mir12=\t/o&& next;#�Ѵ��Ѥ߽���
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
	#ZeroFile�ξ���õ��
	my$logext; #����ĥ��
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
	
	($zero[0]=~/^Mir12=\t/o)&&(die"�����������Ǥ�Mir12���Ǥ�");
	$zero[0]=~s/\bMir1=\t/Mir12=\t/go;
	
	open(ZERO,">$CF{'log'}0.cgi")||die"Can't write log($CF{'log'}0.cgi)[$?:$!]";
	eval{flock(ZERO,2)};
	print ZERO join("\n",@zero[0,1,2])."\n";
	close(ZERO);
	
	#�ե��������
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
	
	#MTP���ɤ߹���
	open(MTP,$CF{'oldlog'})||die"Can't read log($CF{'oldlog'})[$?:$!]";
	eval{flock(MTP,1)};
	my%DT;
	my@log;
	while(<MTP>){
		chomp$_;
		unless($_){
			#����å��Ѥ�
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
		#SJIS����EUC�˴��������ɤ��Ѵ����褦
		$_=sjis2euc($_);
		unless(defined$DT{'subject'}){
			#0����
			@DT{qw(i mtp subject)}=split('<>',$_);
			next;
		}
		#����
		@DT{qw(mtp mtp email time name icon body home ra mtp hua)}=split('<>',$_);
		$DT{'icon'}.='.gif'; #MTP��Ԥä�UNISYS�����ʤΡ�
		my$data="Mir12=\t;\tname=\t$DT{'name'};\tpass=\t;\ttime=\t$DT{'time'};\tbody=\t$DT{'body'};\t";
		#�Ƶ���:�ҵ���
		for(!@log?qw(color email home icon ra hua cmd subject):qw(color email home icon ra hua cmd)){
			$data.=qq($_=\t$DT{"$_"};\t);
		}
		push(@log,$data);
	}
	close(MTP);
	if(%DT){
		#����å��Ѥ�
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
Mir12=\t;\tsubject=\tMTP164g���饳��С�������;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

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
# �������
BEGIN{
	getlogin||umask(0); #'nobody'�ä�''����͡�
	# Revision Number
	$CF{'Conv'}=qq$Revision$;
	#���顼���Ф��饨�顼���̤�ɽ������褦��
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
