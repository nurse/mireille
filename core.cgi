#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Core File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
use strict;
use vars qw(%CF %IC %IN %CK %Z0 @zer2 @file);

=item core.cgi��ñ�ε�ư������ȡ�location��ķ�Ф���CGI��

# ���ε�ǽ��Ȥ��ˤϾ�ιԤ� # �� #=item �ȥ����ȥ����Ȥ��Ƥ�������

INIT:{
	if($CF{'program'}eq __FILE__){
		#ľ�ܼ¹Ԥ��ä���ư���Ф�
		&locate($ENV{'QUERY_STRING'});
	}
}

=pod

=cut

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
	#���ե���������Ȥ��롩
	defined$CF{'log'}||die"\$CF{'log'} is Undefined";
	unless(-e"$CF{'log'}0.cgi"){
		(-e"$CF{'log'}0.pl")&&(die"�����0.pl���ĤäƤ��ޤ� �Զ���������");
		DIR:{
			(-e"$CF{'log'}")&&(last DIR);
			mkdir("$CF{'log'}",0777)&&(last DIR);
			die"Can't read/write/create LogDir($CF{'log'})[$!]";
		}
		open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
		eval{flock(ZERO,2)};
		if(!-s"$CF{'log'}0.cgi"){
			print ZERO "Mir12=\t0-0;\tsubject=\tWelcome to Mireille;\tname=\tMireilleSystem;\ttime=\t$^T;\t"
			."body=\tLOG�ǥ��쥯�ȥ�ڤ�0.cgi������������֤���Ƥ��ʤ��ä��١����֤��ʤ����ޤ���<BR>"
			."���Υ�å�������ɽ������Ƥ����硢���Ǥ�Mireille�ˤ������˼�ư���֤���Ƥ��ޤ�<BR>"
			."�ʤ������Υ�å������Ͽ�����Ƥ�����ȡ���ưŪ�˾��Ǥ��ޤ�;\t";
		}
		close(ZERO);
	}

	#�⡼�ɤ��Ȥο���ʬ��
	&getParam;
	
	if($CF{'readOnly'}&&$IN{'isEditing'}){
		#�������ѥ⡼��
		&showUserError('���ߤ��ηǼ��Ĥϱ������ѥ⡼�ɤ����ꤵ��Ƥ��ޤ�');
	}else{
		#�����񤭹���
		defined$IN{'body'}&&&writeArticle;
		#�ֿ�
		$IN{'i'}&&&res;
		#�����񤭹���
		defined$IN{'j'}&&(&showHeader,&getCookie,&prtfrm,&footer);
		#���������ꥹ��or�¹�
		defined$IN{'rvs'}&&(index($IN{'rvs'},'-')<0?&showRvsMenu:&rvsArticle);
		#��������ꥹ��or�¹�
		defined$IN{'del'}&&(index($IN{'del'},'-')<0?&showRvsMenu:&delArticle);
	}
	#����
	defined$IN{'seek'}&&&showArtSeek;
	#�إ��
	defined$IN{'help'}&&(require($CF{'help'}?$CF{'help'}:'help.pl'));
	#��������
	defined$IN{'icct'}&&(require($CF{'icct'}?$CF{'icct'}:'iconctlg.cgi'));
	#�ۡ���
	defined$IN{'home'}&&&locate($CF{'home'});
	#����ɽ��
	&showIndex;
	exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# mainľ���Υ��֥롼����

#-------------------------------------------------
# Index ����ɽ��
#
sub showIndex{
	&xmlmode if 'xml'eq$IN{'viewstyle'};

	#-----------------------------
	#Cookie�������񤭹���
	&getCookie?&setCookie(\%CK):($CK{'time'}=$^T-$CF{'newnc'});

	#-----------------------------
	# HTTP,HTML,PAGE�إå�����ɽ��
	&showHeader;

	#-----------------------------
	#������ƥե������ɽ�����������ˤ���
	$CF{'prtwrt'}&&&prtfrm;
	print"$CF{'note'}";
	#�����ʥӥܥ���
	&artnavi('button');

	#-----------------------------
	#�ڡ�������
	&logfiles($CF{'sort'});
	if($IN{'read'}){
		my$page=1;my$thread=1;
		for(@file){
			$_==$IN{'read'}&&($IN{'page'}=$page,last);
			++$thread>$CF{'page'}|| next;
			$page++;$thread=1;
		}
	}

	#-----------------------------
	#��������
	my%NEW;
	my@view=map{$NEW{"$_"}=qq(<A href="index.cgi?read=$_#art$_" class="new">$_</A>)}
	grep{$zer2[$_-$zer2[0]]>$CK{'time'}}@file;

	#-----------------------------
	#̤�ɵ����Τ��륹��å�
	my$unread='';
	if($#view>-1){
		# 20 : ̤�ɵ����Τ��륹��åɤ��������ɽ�����륹��åɿ��ξ��
		$unread='<P>̤�ɵ����Τ��륹��å�[ '.($#view>20?"@view[0..20] ..":"@view[0..$#view]")." ]</P>";
	}

	#-----------------------------
	#�ڡ�������TABLE��ɽ��
	my$pgslct=&pgslct($#file,$CF{'page'});

	#-----------------------------
	#���Υڡ����Υ���å�
	my$this='';
	@view=splice(@file,($IN{'page'}-1)*$CF{'page'},$CF{'page'});
	$#view!=0&&!$view[$#view]&&pop@view;
	for(0..$#view){
		$this.=qq(<A href="#art$view[$_]" title="Alt+$_">)
		.($NEW{"$view[$_]"}?qq(<SPAN class="new">$view[$_]</SPAN>):$view[$_])."</A> ";
	}

	#-----------------------------
	#��������ɽ����
	print<<"_HTML_";
<DIV class="artinfo">
$unread
$pgslct
<P class="artinfo">���Υڡ����Υ���å�<BR>\n[ $this]<BR>
<A name="nav_n0" href="#nav_s1" title="���Υ���åɤ�" accesskey="0">��</A></P>
</DIV>
_HTML_
	#-----------------------------
	#����ɽ��
	if(0 ne$view[0]){
		#���˲�ư��ΤȤ�
		#Threads Body
		for(0..$#view){
			&showArticle('i'=>$view[$_],'ak'=>($_+1));
		}
	}else{
		#log0�Τ� �Ĥޤ�����ľ��ΤȤ�
		&showArticle('i'=>0,'ak'=>1);
	}
	#-----------------------------
	#��������ɽ����
	print<<"_HTML_";
<DIV class="artinfo">
<P class="artinfo"><A name="nav_s@{[$#view+2]}" href="#nav_n@{[$#view+1]}" title="��Υ���åɤ�" accesskey="&#@{[$#view+50]};">��</A><BR>
���Υڡ����Υ���å�<BR>\n[ $this]</P>

$pgslct
</DIV>
_HTML_

	#-----------------------------
	#�����ʥ�
	&artnavi;

	#-----------------------------
	#�եå�
	&footer;
	exit;
}


#-------------------------------------------------
# �����񤭹���
#
sub writeArticle{

=item �񤭹��ߤξ���

(length$IN{'j'}xor$IN{'i'})			����
(!defined$IN{'i'}&&$IN{'j'}eq 0)	�����Ƶ���
($IN{'i'}&&!defined$IN{'j'})		�����ҵ���
($IN{'i'}&&defined$IN{'j'})			����
($IN{'i'}&&$IN{'j'}eq 0)			�����Ƶ���
($IN{'i'}&&$IN{'j'}ne 0)			�����ҵ���

=cut

	#-----------------------------
	#���ޥ�ɤȤ���Ĵ��
	my%EX;
	for(split(/;/o,$IN{'cmd'})){
		my($i,$j)=split('=',$_,2);
		$i||next;
		defined$j||($j=1);
		$EX{$i}=$j;
	}

=item ���ޥ�ɤǻȤ�����

icon : ���ѥ�������
bring: �������ߥ�������

dnew : ������������
znew : ����å���������
renew: dnew&&znew

usetag:		!SELECTABLE()�ǵ��Ĥ��Ƥ��륢��������ϰ���ǻȤ�������������٤�
notag:		������Ȥ�ʤ�
noautolink:	URI��ư��󥯤�Ȥ�ʤ�
noartno:	�����ֹ��󥯤�Ȥ�ʤ�
nostrong:	��綯Ĵ��Ȥ�ʤ�

su: �����ѥ���ɤ�����Ƥ����ȡ��ֿ��Ǥ��ʤ�����åɤ��ֿ��Ǥ����ꤹ��ʤ褦�ˤʤ�ͽ���

"key=value;key=value"�η����ǥ��ޥ��������Ϥ���
key�ڤ�value��[=;]��ޤ�ǤϤʤ�ʤ�
��Q:���������url��[=;]���ޤޤ�뤳�ȤäƤ��롩��
��A:cgi����Ѥ��Ƥ���Ϥ��뤫��͡�����

������
key1="value1;value1";key2=value2;
��Mireille1.2.2.16�Ǥϴ����̤�˲�ᤷ�Ƥ���ʤ��櫓�Ǥ�
1.2.2.16���ߤǤϤ����餯����Ŭ���ʽ����Ǥ⤤������ɡ�
�ܳ�Ū�˥��ޥ�ɤ�Ƚ�������ʤ�Marldia�Υ��ޥ�ɼ�����ä����٤�
�ޤ��������ʳ��˥��ޥ�ɤΥͥ����פ��Ĥ��ʤ��Τǡ�����^^;;
Marldia�ϥǡ������ݻ��ʤɤ�Ŭ���Ǥ⤤�����Ȥ⤢�äơ��빽�������ޥ�ɤ�Ĥ��Ƥ����ꤹ��Τǡ�
�嵭�Τ褦�ʤ�Τ�Ȥ�ɬ���������뤫�⤷��ʤ����ᡢǰ�Τ����б������Ƥ���ΤǤ����ɤ�

=cut

	#renew��dnew&&znew
	$EX{'dnew'}=$EX{'znew'}=1if$EX{'renew'};
	
	#���ѥ�������ǽ��index.cgi�����ꤹ�롣
	if($CF{'exicon'}){
		#index.cgi�ǻ��ꤷ����������ѥ���ɤ˹��פ���С�
		$IN{'icon'}=$IC{"$EX{'icon'}"}if$IC{"$EX{'icon'}"};

=item �������ߥ������� ɸ��Ǥ�̵��

�������ߥ�������򿿤˲�ư�����뤿��ˤ�$CF{'icon'}=''�Ȥ��ʤ��Ȱ�̣������ޤ���
�����������������ϡ��礭�ʲ�����Ž����Ȥ����狼��䤹����ˡ��¾�ˤ⡢
�Ȥ����ˤ�äƤ����ѼԤξ����������뤳�Ȥ��Ǥ���Ȥ�����������Τǡ�
���Ѥ��֤���ͤ�����ʤ�����̵���¤ꡢ�Ȥ�ʤ��ۤ��������Ǥ�

Perl�⥸�塼���Image::size���Ѥ��뤳�Ȥˤ�äơ����������¤򤫤��뤳�Ȥ�����뤫�⤷��ޤ���
����ʤ龯���������������ޤ�����CGI��ͳ����ƼԤξ���ή�Ф��롢��
�Ȥ�����ǽ���������ĤäƤ��뤿�ᡢ̵���¤ˤ��뤳�ȤϽ���ʤ��Ǥ��礦

=cut

#		$IN{'icon'}=$EX{'bring'}if$EX{'bring'};
	}
	
	
	#-----------------------------
	#��ʸ�ν���
	#form->data�Ѵ�
	if($CF{'tags'}&& 'ALLALL'eq$CF{'tags'}){
		#ALLALL������OK��â����Ĵ��̵����URI��ư��󥯤�̵����
		#�����ǥ�󥯤�ĥ�ä��ꡢ��Ĵ���Ƥ����Τ���Ť˥�󥯡���Ĵ���Ƥ��ޤ��ޤ�����
	}else{
		#��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
		my$attrdel=0;#°����ä�/�ä��ʤ�(1/0)
		my$str=$IN{'body'};
		study$str;
		$str=~tr/"'<>/\01-\04/;
		
		#��������
		if($CF{'tags'}&&!$EX{'notag'}){
			my$tags=$CF{'tags'};
			my%tagCom=map{m/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
			if($tagCom{'!SELECTABLE'}){
				$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{m/\w+/}split(/\s+/,$EX{'usetag'}));
			}elsif(defined$tagCom{'!SELECTABLE'}){
				$tags='\w+';
			}
			
			my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
			my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
			my$text_regex = '[^\03]*';
			my$result='';
			#�⤷ BR������ A�����ʤ�����Υ��������Ϻ���������ʤ����ˤϡ� 
			#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
			#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/i;
			my$remain=join('|',grep{m/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
			#�դ� FONT������ IMG�����ʤ�����Υ�������������������ˤϡ� 
			#$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
			#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/i;
			my$pos=length$str;
			while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
				$pos=pos$str;
				length$1||length$2||last;
				$result.=$1;
				my$tag_tmp=$2;
				if($tag_tmp=~s/^\03((\/?(?:$remain))(?![\dA-Za-z]).*)\04/<$1>/io){
					$tag_tmp=~tr/\01\02/"'/;
					$result.=$attrdel?"<$2>":$tag_tmp;
				}else{
					$result.=$tag_tmp;
				}
				if($tag_tmp=~/^\03(XMP|PLAINTEXT|SCRIPT)(?![\dA-Za-z])/i){
					$str=~/(.*?)(?:\03\/$1(?![\dA-Za-z])$tag_regex_|$)/gsi;
					(my$tag_tmp=$1)=~tr/\01\02/"'/;
					$result.=$tag_tmp;
				}
			}
			$str=$result.substr($str,$pos);
		}else{
			#���ĥ���̵��orCommand:notag
		}
		
		#��綯Ĵ
		if($CF{'strong'}&&!$EX{'nostrong'}){
			my%ST=map{(my$str=$_)=~tr/"'<>/\01-\04/;$str}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
			if($CF{'strong'}=~/^ /o){
				#��ĥ��綯Ĵ
				for(keys%ST){
					if($_=~/^\/(.+)\/$/o){
						my$regexp=$1;
						($ST{$_}=~s/^\/(.+)\/$/$1/o)?($str=~s[$regexp][$ST{$_}]gm)
						:($str=~s[$regexp][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm);
					}elsif($ST{$_}=~s/^\/(.+)\/$/$1/o){
						$str=~s[^(\Q$_\E.*)$][$ST{$_}]gm;
					}else{
						$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;
					}
				}
			}else{
				#���ܸ�綯Ĵ
				for(keys%ST){$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;}
			}
		}
		
		#URI��ư���
		if($CF{'noautolink'}||!$EX{'noautolink'}){
			#[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
			#[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
			#[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
			#[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
			#http URL ������ɽ��
			my$http_URL_regex =
		q{\b(?:https?|shttp)://(?:(?:[!$&-.\w:;=~]|%[\dA-Fa-f}.
		q{][\dA-Fa-f])*@)?(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)}.
		q{*[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.}.
		q{\d+)(?::\d*)?(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f]}.
		q{[\dA-Fa-f])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-}.
		q{Fa-f])*)*(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f}.
		q{])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*)}.
		q{*)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])}.
		q{*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{)?};
			#ftp URL ������ɽ��
			my$ftp_URL_regex =
		q{\bftp://(?:(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{(?::(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*)?@)?(?}.
		q{:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)*[a-zA-Z](?:[-a-zA-}.
		q{Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.\d+)(?::\d*)?}.
		q{(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*(?:/(?}.
		q{:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*(?:;type=[}.
		q{AIDaid])?)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\d}.
		q{A-Fa-f])*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA}.
		q{-Fa-f])*)?};
			#�᡼�륢�ɥ쥹������ɽ����
			#"aaa@localhost"�ʤɤ�Ǽ��Ĥǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τǡ�
			my$mail_regex=
		q{(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
		.q{\[\]\00-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
		.q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x}
		.q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff])|"[^\\\\\x80-}
		.q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
		.q{\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
		.q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
		.q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,}
		.q{;:".\\\\\[\]\00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
		.q{^\x80-\xff])*\]))+};
		
			$str=~s{(?<!["'])($http_URL_regex|$ftp_URL_regex|($mail_regex))(?!["'])}
			{<A class="autolink" href="@{[$2?'mailto:':'']}$1" target="_blank">$1<\x2fA>}go;
		}else{
			#Command:nolink
		}
		
		#�����ֹ��󥯡�>>No.12-6��
		if($CF{'noartno'}||!$EX{'noartno'}){
			$str=~s{(\04\04No\.(\d+)(\-\d+)?)}{<A class="autolink" href="index.cgi?read=$2#art$2$3">$1</A>}go;
		}
		
		$str=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$str=~s/\01/&#34;/go;
		$str=~s/\02/&#39;/go;
		$str=~s/\03/&#60;/go;
		$str=~s/\04/&#62;/go;
		$IN{'body'}=$str;
	}
	$IN{'body'}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
	$IN{'body'}=~s/\n+$//o;
	$IN{'body'}=~s/\n/<BR>/go;
	
	
	#-----------------------------
	#$IN{'cook'}��ON�ʤ�Cookie�ν񤭹���
	COOKIE:{
		$IN{'cook'}||last COOKIE;
		$CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}&& last COOKIE; #�����ѥ��λ���Cookie��¸���ʤ�
		&getCookie;
		&setCookie(\%IN);
	}

	#-----------------------------
	#���顼ɽ��
	my@error;
	$IN{'name'}||push(@error,'̾��');
	$IN{'body'}||push(@error,'��ʸ');
	$IN{'pass'}||($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'})or push(@error,'�ѥ����');
	if(@error){
		&showHeader;
		print<<"_HTML_";
<H2 class="mode">- Write Error -</H2>
<P>@{[join('��',map{qq(<SPAN style="color:#f00">$_</SPAN>)}@error)]}����������Ϥ��Ƥ�������</P>
_HTML_
		%CK=%IN;
		&rvsij;
		&footer;
	}

	#-----------------------------
	#�񤭹��ߥǡ�������
	open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't read/write log(0.cgi)[$!]";
	eval{flock(ZERO,2)};
	seek(ZERO,0,0);
	my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
	index($zero[0],"Mir12=\t")&&die"��������Mir12���ʳ��Ǥ�($zero[0])";
	%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
	my@zer1=split(/\s+/o,$zero[1]);
	@zer2=split(/\s/o,$zero[2]);
	$zer2[0]||($zer2[0]=0);

	#-----------------------------
	&logfiles('number');
	$IN{'i'}=$file[0]+1if$IN{'i'}&&$IN{'i'}>$file[0]+1;

	#-----------------------------
	#�񤭹��ߤ����������ĥ����������
	&exprewrt();

	#-----------------------------
	#���褤��
	unless($IN{'ArtType'}&2){
		#�������ֿ��񤭹���
		$IN{'newps'}=&mircrypt($^T,$IN{'pass'});
		$EX{'znew'}=1;
		if($IN{'i'}&&$zero[1]=~/($IN{'i'}):$ENV{'CONTENT_LENGTH'}:([1-9]\d*)/
			or length$IN{'j'}&&$zero[1]=~/(\d+):$ENV{'CONTENT_LENGTH'}:($IN{'j'})/){
			&showHeader;
	print<<"_HTML_";
<H2 class="mode">- ¿����ơ� -</H2>
<DIV class="center">
<P style="margin:0.6em">����Ƥ��줿���������Ƥ�<A href="index.cgi?read=$1#art$1-$2" title="�����������ǧ����">��$1�֥���åɤ�$2����</A>��Ʊ�����Ƥ��Ȼפ��ޤ�<BR>
�����������ǧ���ơ�Ʊ�����ƤǤʤ����ϡ����Υե�����Ǿ����������Ƥ�����Ƥ��ƤߤƤ���������</P>
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
			%CK=%IN;
			&rvsij;
			&footer;
		}elsif(!$IN{'ArtType'}){
			#-----------------------------
			#�����񤭹���
			if($CF{'logmax'}>0&&@file>$CF{'logmax'}){
				#�Ť���������åɥե������ �ե�����̾�ѹ�/��� ����

=pod ������ʬ�Ϥ��󤬤餬��䤹���Τǥ�⡣

@file�� (101,100,99,95,91,������,3,2,1,0) �Ȥ��ä�����
���ν��֤Ͼ�˹߽�
�Ǹ��ɬ����������ե������ɽ�� 0 �����

@zer2�� (1 1000000 10000001 ������ 1200000) �Ȥ��ä�����
�ǽ�ο����ϵ����ֹ��@zer2�Ǥ�ź�����Ȥ��б���ɽ��
����Offset��100�ʤ鵭���ֹ�159�ξ����$zer2[59]�ˤ���

�ե����뤬�����������Ȥ��˵�������åɥե������������ݤˤϡ�
�嵭����Ĥ������Ʊ�����������������ʤ���Фʤ�ʤ�
���λ�����������åɥե����뤬������줿���Ȥˤ�äơ�
@file���꡹����������Ǥ����ǽ�������뤳�Ȥ����
@zer2�ϵ������������Ƥ��Ƥ�Ϣ�֤ˤʤäƤ���

���ʤߤˡ�
$file[$#file-1] �Ϥ��λ��������뵭���Τ����ǵ�������å��ֹ椬�Ǥ⾮������ΤΡ���������å��ֹ��
$file[$CF{'logmax'}-1] �ϵ�������å��ֹ椬�Ǥ��礭����ΤΡ���������å��ֹ�򤢤�魯
$file[$CF{'logmax'}-2] �Ϻ�����줿��˻Ĥä���������åɤΤ�����
��������å��ֹ椬�����ʤ�ΤΡ���������å��ֹ�򤢤�魯

��äơ�$file[$CF{'logmax'}-2]-$file[$#file-1] �Ϥ��λ����������ٵ������򤢤�魯
#���浭������åɤ��������Ƥ����硢�ºݤ˺������뵭������åɿ��Ȥϰۤʤ�

��
 @file�ˤ�0.cgi���ޤޤ�Ƥ���Τǰ��¿����
 �ޤ�@file�ˤϤ��줫���ɲä��뿷����åɤ��ʤ��Τǰ�ľ��ʤ�

=cut

				splice(@zer2,1,$file[$CF{'logmax'}-2]-$file[$#file-1]);
				&delThread($CF{'delold'},splice(@file,$CF{'logmax'}-1,@file-$CF{'logmax'}))
				#($#file-1)-($CF{'logmax'}-1)+1=@file-$CF{'logmax'}���Ȥ�������
				||die"\$CF{'delold'}�����꤬�۾�Ǥ�($CF{'delold'})";
				$zer2[0]=$file[$CF{'logmax'}-2]-1;
			}
			$IN{'i'}=$file[0]+1;
			open(WR,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't write log($IN{'i'})[$!]";
			eval{flock(WR,2)};
			truncate(WR,0);
			seek(WR,0,0);
			print WR "Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}($CF{'prtitm'}=~/\+([a-z\d]+)\b/go))."\n";
			close(WR);
		}else{
			#-----------------------------
			#�ֿ��񤭹���
			open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
			eval{flock(RW,2)};
			seek(RW,0,0);
			my$line;
			while(<RW>){$line=$_;}
			$IN{'j'}=$.; #$.-1+1
			seek(RW,0,2);
			my$prefix='';
			if(!chomp$line){
				++$IN{'j'};
				$prefix="\n";
			}
			if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
				#�ѥ���ɤ������ѥ��ΤȤ��Ϻ���ҵ��������¤������äƤ��Ƥ���ƽ����
			}elsif($CF{'maxChilds'}&&$IN{'j'}>$CF{'maxChilds'}){
				&showUserError('���˺���ҵ��������¤�ۤ��Ƥ���');
			}
			print RW $prefix
			."Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}($CF{'chditm'}=~/\+([a-z\d]+)\b/go))."\n";
			close(RW);
		}
		
		#-----------------------------
		#MailNotify
		if($CF{'mailnotify'}){
			#����/�ֿ������ä����ϥ᡼�������
			require 'notify.pl';
			&mailnotify(%IN);
		}
		
	}else{
		#-----------------------------
		#�����񤭹���
		open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
		eval{flock(RW,2)};
		seek(RW,0,0);
		my@log=map{m/^([^\x0D\x0A]*)/o}<RW>;
		$#log<$IN{'j'} and die"Something Wicked happend!(j���礭����)";
		$log[$IN{'j'}] or  die"Something Wicked happend!(�����Ǥʤ�j)";
		my%DT=($log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go);
		#PasswordCheck
		if($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){
			#MasterPass�ˤ��
			if($IN{'pass'}){
				#Pass�ѹ�
				$IN{'oldps'}=$IN{'pass'};
			}else{
				#Pass���Τޤ�
				$IN{'newps'}=$DT{'pass'};
			}
		}else{
			#UserPass�ˤ��
			unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
				&showHeader;
				print qq(<H2 class="mode">Password Error</H2>\n);
				%CK=%IN;
				&rvsij;
				&footer;
				exit;
			}
			#Pass�ѹ�
			$IN{'oldps'}=$IN{'pass'};
		}
		unless($IN{'newps'}){
			#Pass�ѹ��������ѹ�
			$EX{'dnew'}&&($DT{'time'}=$^T);
			$IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
		}
		#�񤭹���
		$log[$IN{'j'}]=
			"Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$DT{'time'};\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}((!$IN{'j'}?$CF{'prtitm'}:$CF{'chditm'})=~/\b([a-z\d]+)\b/go))."\n";
		truncate(RW,0);
		seek(RW,0,0);
		print RW @log;
		close(RW);
	}
	
	if($EX{'znew'}){
		#-----------------------------
		#�������ե����롢0.pl�˽񤭹���
		#�������ֿ��λ��ˤ���ƾ������¸
		$#zer1>2&&($#zer1=2);
		unshift(@zer1,"$IN{'i'}:$ENV{'CONTENT_LENGTH'}:$IN{'j'}");
		my$No=$IN{'i'}-$zer2[0];
		$No>0||die"ZER2�Υǡ����������Ǥ� 'i':$IN{'i'},'zer2':$zer2[0]";
		$zer2[$No]=$^T;
		truncate(ZERO,0);
		seek(ZERO,0,0);
		print ZERO 
			"Mir12=\t$IN{'i'}-$IN{'j'};\tsubject=\t$IN{'subject'};\tname=\t$IN{'name'};\ttime=\t$^T;\t"
			."\n@zer1\n@zer2\n";
	}
	close(ZERO); #�����Ǥ�äȽ񤭹��߽�λ

	#-----------------------------
	#�񤭹����������ּ�ͳ�˽�����ɤ�����
	&showHeader;
	print<<"_HTML_";
<H2 class="mode">- �񤭹��ߴ�λ -</H2>
<DIV class="center">
<P style="margin:0.6em">�ʲ������Ƥ���$IN{'i'}�֥���åɤ�$IN{'j'}���ܤ˽񤭹��ߤޤ�����<BR>
����Ǥ褱��Ф��Τޤ�TOP��Ǽ��Ĥ���äƤ���������<BR>
�������������ϰʲ��Υե�����ǽ���������Ƥ��Ƥ���������</P>
<DIV align="center" class="note" style="width:600px"><P align="left">
<STRONG>--- PREVIEW ---</STRONG><BR>$IN{'body'}</P></DIV>
<TABLE border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
	%CK=%IN;
	$CK{'oldps'}||($CK{'oldps'}=$CK{'pass'});
	&rvsij;
	&footer;

	exit;
}


#-------------------------------------------------
# �����ֿ�
#
sub res{
	&getCookie;
	&showHeader;
	print qq(<H2 class="mode">- �����ֿ��⡼�� -</H2>\n);
	print q(<DIV style="border:dashed 1px #333;height:400px;overflow:auto;width:99%">)
	.q(<H3>���Υ���åɤκ��ޤǤ�����</H3>);
	print"This thread$IN{'i'} is deleted."if"del"eq&showArticle('i'=>$IN{'i'},'ak'=>1,'res'=>1);
	print q(</DIV>);
	$CK{'i'}=$IN{'i'};
	$CK{'ak'}=1;
	&chdfrm;
	&footer;
	exit;
}


#-------------------------------------------------
# ���������������˥塼
#
sub showRvsMenu{
=item ����
$ ����ν����η��
=cut
	&getCookie;
	&showHeader;
	my$mode='';
	#�⡼��ʬ��
	if(defined$IN{'rvs'}){$mode='rvs';print qq(<H2 class="mode">- ���������⡼�� -</H2>\n);}
	elsif(defined$IN{'del'}){$mode='del';print qq(<H2 class="mode">- ��������⡼�� -</H2>\n);}
	else{print qq(<H2 class="mode">Something Wicked happend!(mode������)</H2>);&footer;}
	#��������-Index�����
	if($_[0]){
		print<<"_HTML_";
<DIV class="center">
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<CAPTION>$_[0]</CAPTION>
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
	}
	#������
	&logfiles('number');
	my$pgslct=&pgslct($#file,$CF{'delpg'},$mode);
	my@i=@file;
	@i=splice(@i,($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});
	$i[$#i]==0&& pop@i;
	print<<"_HTML_";
<DIV class="center">$pgslct</DIV>

<FORM id="List" method="post" action="index.cgi">
<DIV class="center"><TABLE border="1" cellspacing="0" class="list" summary="List" width="80%">
<COL style="width:5em">
<COL style="width:15em">
<COL>
<TR>
<TD style="text-align:center">[$i[0]-$i[$#i]]</TD>
<TD><SPAN class="ak">P</SPAN>assword: <INPUT name="pass" type="password"
 accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}"></TD>
<TD>
<INPUT name="$mode" type="hidden" value="">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</TD></TR>
_HTML_
	#������åɤ���
	for(@i){
		$_||next;
		-e"$CF{'log'}$_.cgi"||next;
		my$i=$_;
		my$j=-1;
		open(RD,"<$CF{'log'}$i.cgi")||die"Can't read log($i.cgi)[$!]";
		eval{flock(RD,1)};
#		print"<TR><TD colspan=\"6\"><HR></TD></TR>";
		my$count="<A href=\"index.cgi?read=$i#art$i\">��$i��</A>";
		#��������
		while(<RD>){
			$j++;
			index($_,"Mir12=\tdel;\t")||next;
			my%DT=($_=~/([^\t]*)=\t([^\t]*);\t/go);
			$j&&($count="Res $j");
			my$No="$i-$j";
			my$date=&date($DT{'time'});
			#��ʸ�ν̤����
			$DT{'body'}=~s/<br\b[^>]*>/��/go;
			$DT{'body'}=&getTruncated($DT{'body'},100);
			my$level=!$j?'parent':'child';
			print<<"_HTML_";
<TR class="$level">
<TH align="right">$count</TH>
<TH align="left">$DT{'subject'}</TH>
<TD align="right">by $DT{'name'}</TD>
</TR>
<TR>
<TD><INPUT type="radio" name="$mode" value="$No"></TD>
<TD align="right">$date</TD>
<TD align="right">$DT{'body'}</TD>
</TR>
_HTML_
		}
		close(RD);
	}
	print"</TABLE></DIV></FORM>\n";
	print qq(<DIV class="center">$pgslct</DIV>);
	&footer;
	exit;
}


#-------------------------------------------------
# ��������
#
sub rvsArticle{
	($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});
	open(RD,"<$CF{'log'}$IN{'i'}.cgi")||die"Can't read log($IN{'i'}.cgi)[$!]";
	eval{flock(RD,1)};
	my$i=0;
	my%DT;
	while(<RD>){
		$i++==$IN{'j'}||next;
		%DT=($_=~/([^\t]*)=\t([^\t]*);\t/go);
	}
	close(RD);
=pod
���Ȥ�$IN{'pass'}���Ϥ���ʤ��Ƥ⡢GetCookie��Cookie�򻲾Ȥ���
�⤷����������줿$CK{'pass'}���ѥ���ɤȰ��פ���н����⡼�ɤ��̤���
�Ȥ����褦�ˤ����������θ����ޤäƤ��롣
�����ѥ���ɤ����פ��ʤ�������Ϥ���褦���������롣
=cut
	if($IN{'pass'}){
		#IN�������Ƥ�����
		$IN{'oldps'}=$IN{'pass'};
		if(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
			#INpassOK
			#������
		}elsif($CF{'admps'}&&($IN{'pass'}eq$CF{'admps'})){
			#ADMINpassOK
			$IN{'pass'}='';
			#������
		}else{
			&showRvsMenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���");
		}
	}else{
		#Cookie�ˤ��롩
		&getCookie;
		$IN{'pass'}=$CK{'pass'};
		$IN{'oldps'}=$CK{'pass'};
		#-----------------------------
		unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
			#̵���ʤ����Ϥ���
			&showHeader;
			print<<"_HTML_";
<H2 class="mode">- ��$IN{'i'}�֤�$IN{'j'}�Υѥ����ǧ�� -</H2>
<FORM accept-charset="euc-jp" id="Revise" method="post" action="index.cgi">
<TABLE cellspacing="2" summary="Revise" width="550">
<COL width="50">
<COL width="170">
<COL width="330">
<P style="margin:0.6em">�ѥ���ɤ����Ϥ��Ƥ�������</P>
<P style="margin:0.6em"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
<INPUT name="rvs" type="hidden" value="$IN{'rvs'}"></P>
<P style="margin:0.6em">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</p>
_HTML_
			&footer;
			exit;
		}
		#CKpassOK
		#������
	}
	#Revise Main Routin
	&showHeader;
	print qq(<H2 class="mode">- ��$IN{'i'}�֤�$IN{'j'}�ν����⡼�� -</H2>\n);
	%CK=%DT;
	@CK{qw(i j pass oldps)}=@IN{qw(i j pass oldps)};
	&rvsij;
	&footer;
	exit;
}


#-------------------------------------------------
# �������
#
sub delArticle{
	my$delEvenIfMarkMode=0;
	
	($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});
	open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
	eval{flock(RD,2)};
	seek(RW,0,0);
	my@log=<RW>;
	my%DT=($log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go);
	#���ʬ��
	SWITCH:{
		if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
			#AdminPassOK
			if($IN{'j'}==0&&!$IN{'type'}){
				#���������ˡ̵���ʤ����Ϥ���
				&showHeader;
				print<<"_HTML_";
<H2 class="mode">- ��$IN{'i'}�֥���åɤκ�� -</H2>
<FORM accept-charset="euc-jp" id="Delete" method="post" action="index.cgi">
<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>����åɤκ����ˡ������Ǥ�������</LEGEND>
_HTML_
				my$i=<<"_HTML_";
<TD>
<LABEL for="mark">�Ƶ�������ʸ�Τߺ��<INPUT id="mark" name="del" type="radio" value="$IN{'del'}-1"></LABEL>
<LABEL for="$CF{'delthr'}">��������åɤ���<INPUT id="$CF{'delthr'}" name="del" type="radio" value="$IN{'del'}-2"></LABEL>
_HTML_
				$i=~s/id="$CF{'delthr'}"/id="$CF{'delthr'}" checked="checked"/o;
				print<<"_HTML_";
$i
</FIELDSET>

<P style="margin:0.6em">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</P>
_HTML_
				&footer;
				exit;
			}
			$IN{'j'}==0&&$IN{'type'}==2&& last SWITCH;
		}else{
			#����Pass
			&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
			 or &showRvsMenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���");
			$IN{'j'}==0&&$#log==0&& last SWITCH;
		}
		
		#mark
		if($delEvenIfMarkMode){
			$log[$IN{'j'}]=~s/\tbody=\t([^\t]*);\t/\tbody=\tdel;\t/go;
		}
		$log[$IN{'j'}]=~s/^Mir12=\t([^\t]*);\t/Mir12=\tdel;\t/go;
		truncate(RW,0);
		seek(RW,0,0);
		print RW @log;
		close(RW);
		&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�������ޤ�����");
	}
	close(RW);
	#�Ƶ������
	&showRvsMenu("��$IN{'i'}�֥���åɤ������ޤ�����(".&delThread($CF{'delthr'},$IN{'i'}).")");
	exit;
}


#-------------------------------------------------
# ��ʸ������ǽ
#
sub showArtSeek{
	&showHeader;
	print qq(<H2 class="mode">- �����⡼�� -</H2>);
	my%SK=split(/ /o,$CF{'sekitm'});
	
	if(length$IN{'seek'}){
		#-----------------------------
		#���������ɽ��
		my$result='';
		my$item='';
		my$seek=quotemeta$IN{'seek'};
		'ALL'eq$IN{'item'}||($item="\t$IN{'item'}");
		&logfiles('number');
		
		#�������ѥ�����ޥå�������
		my$eucpre=qr{(?<!\x8F)};
		my$eucpost=qr{(?=
			(?:[\xA1-\xFE][\xA1-\xFE])*	# JIS X 0208 �� 0ʸ���ʾ�³����
			(?:[\x00-\x7F\x8E\x8F]|\z)	# ASCII, SS2, SS3 �ޤ��Ͻ�ü
		)}x;
		
		if('i'eq$IN{'every'}){
			#����åɤ��ȸ���
			for(@file){
				$_||last;
				open(RD,"<$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				index($thread,$IN{'seek'})>-1||next;
				$thread=~/$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/o||next;
				$result.=qq(<A href="index.cgi?read=$_#art$_">No.$_</A>\n);
			}
		}else{
			#�������ȸ���
			for(@file){
				$_||last;
				open(RD,"<$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				close(RD);
				index($thread,$IN{'seek'})>-1||next;
				my$i=$_;
				my$j=0;
				for($thread=~/([\w\W]*?)$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/go){
					$j+=@{[/[\x0A\x0D]+/go]};
					$result.=qq(<A href="index.cgi?read=$i#art$i-$j">No.$i-$j</A>\n);
				}
			}
		}
		print<<"_HTML_";
<P>��<STRONG>$IN{'seek'}</STRONG>�פ�<STRONG>$SK{$IN{'item'}}</STRONG>��<STRONG>@{[
'i'eq$IN{'every'}?'����å�':'�Ƶ���']}����</STRONG>�˸���������̡�<BR>
@{[$result?"�ʲ��Υ���åɤǸ���ñ���ȯ�����ޤ�����<BR>$result":"����ñ���ȯ���Ǥ��ޤ���Ǥ���"]}<BR>
�����ä����֡�@{[join'+',(times)[0,1]]}��</P>
_HTML_
	}
	
	print<<"_HTML_";
<FORM accept-charset="euc-jp" id="seek" method="post" action="index.cgi">
<DIV class="center"><TABLE cellspacing="2" summary="�����ե�����" style="margin: 1em auto">
<TR>
<TH class="item">
<LABEL accesskey="m" for="item">�����������(<SPAN class="ak">M</SPAN>)</LABEL></TH>
<TD><SELECT name="item" id="item">
_HTML_
	my$select=join('',map{qq(<OPTION value="$_">$SK{$_}</OPTION>)}($CF{'sekitm'}=~/(\w+) \S+/go));
	$select=~s/(value="$IN{'item'}")/$1 selected="selected"/io;
	print<<"_HTML_";
$select</SELECT>
</TD>
</TR>
<TR>
<TH class="item"><LABEL accesskey="k" for="seek">��������ñ��(<SPAN class="ak">K</SPAN>)</LABEL></TH>
<TD><INPUT type="text" name="seek" id="seek" style="ime-mode:active;width:200px;" value="$IN{'seek'}"></TD>
</TR>
<TR>
<TH class="item">��������ñ��</TH>
<TD>
_HTML_
	my%DT=qw(i ����åɤ��� j �Ƶ�������);
	$select=join('',map{qq(<LABEL accesskey="$_" for="every$_"><INPUT type="radio" name="every" id="every$_")
	.qq( value="$_">$DT{$_}(<SPAN class="ak">\u$_</SPAN>)</LABEL>\n)}('i','j'));
	$select=~s/(value="$IN{'every'}")/$1 checked="checked"/io;
	print<<"_HTML_";
$select
</TD>
</TR>
<TR>
<TD colspan="2">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" accesskey="r" value="����󥻥�">
</TD>
</TR>
</TABLE>
</DIV>
<DIV class="center"><TABLE class="note"><TR><TD>
<UL class="note">
<LI>���ԤǤϸ���ʸ���������ɽ����Ȥ����ȤϽ���ޤ���</LI>
<LI>�֥饦���Ρ֤��Υڡ������⸡���פ�Ȥ��С�<BR>�ɤ���õ������ñ�줬����Τ���狼��ޤ��͡�</LI>
</UL></TD></TR></TABLE></DIV>
</FORM>
_HTML_
	&footer;
	exit;
}


#-------------------------------------------------
# �桼�����������顼
#
sub showUserError{
	my$message=shift();
	&showHeader;
	print<<"_HTML_";
<H2 class="mode">- ���顼��ȯ�����ޤ��� -</H2>
<P>�����ؤ򤫤��ƿ������������ޤ���<BR>
<span class="warning">$message</span>���ᡢ<BR>����ʽ�����³�Ԥ��뤳�Ȥ��Ǥ��ޤ���Ǥ���<BR>
�ʲ���ǰ�Τ��ả���Ϥ��줿�ǡ��������󤷤Ƥ����ޤ�<BR>
���פʾ��󤬤����硢��¸���Ƥ����ơ��ޤ��ε������Ƥ��Ƥ�������</P>
<TABLE border="1" summary="�桼���������ѿ���ɽ�����Ƥ���">
<CAPTION>��������ä�����</CAPTION>
_HTML_
	print map{"<TR><TH>$_</TH><TD><XMP>$IN{$_}</XMP></TD>\n"}keys%IN;
	print '</TABLE>';
	&footer;
	exit;
}


#-------------------------------------------------
# Location��ž��
#
sub locate{
=item ����
;
$ �������URL�����ФǤ����ФǤ��
=cut
	my$i=$_[0];
	($i)||(die"'Stay here.'");
	if(index($i,'http:')==0){
	}elsif($i=~/\?/o){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=sprintf('%s?%s',$_[0]);
	}elsif($i){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=$_[0];
	}
	print<<"_HTML_";
Status: 303 See Other
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
Location: $i
X-Moe: Mireille

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> 
<HTML>
<HEAD>
<META http-equiv="Refresh" content="0;URL=$i">
<TITLE>303 See Ohter</TITLE>
</HEAD>
<BODY>
<H1>: Mireille :</H1>
<P>And, please go <A href="$i">here</A>.</P>
<P>Location: $i</P>
<P>Mireille <VAR>$CF{'Core'}</VAR>.<BR>
Copyright &#169;2001,2002 <A href="http://www.airemix.com/" target="_blank" title="Airemix">Airemix</A>. All rights reserved.</P>
</BODY>
</HTML>
_HTML_
	exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# mainľ���Υ��֥롼���󷲤����

#-------------------------------------------------
# Form���Ƽ���
#
sub getParam{
	my$param;
	my@param;
	#��������
	unless($ENV{'REQUEST_METHOD'}){
		@param=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
#�Ǹ����ƻ�����Τ餻��
		my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
		print"Status: 200 OK\nLast-Modified: $last\n"
		."Content-Type: text/plain\n\nLast-Modified: $last";
		exit;
	}elsif('POST'eq$ENV{'REQUEST_METHOD'}){
		read(STDIN,$param,$ENV{'CONTENT_LENGTH'});
	}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
		$param=$ENV{'QUERY_STRING'};
	}
	
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
	))x;
	
	#������ϥå����
	if(length$param>262114){ # 262114:�����������ξ��(byte)
		#����������
		&showHeader;
		print"������ʤ�Ǥ��̤�¿�����ޤ�\n$param";
		&footer;
		exit;
	}elsif(length$param>0){
		#���Ϥ�Ÿ��
		@param=split(/[&;]/o,$param);
	}
	undef$param;
	
	#���Ϥ�Ÿ�����ƥϥå���������
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/(\w+)/o)?$1:'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		if('body'ne$i){
			#��ʸ�ʳ������̥����ػ�
			$j=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
			$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
			$j=~s/"/&#34;/go;
			$j=~s/'/&#39;/go;
			$j=~s/</&#60;/go;
			$j=~s/>/&#62;/go;
			$j=~s/\n/<BR>/go;
			$j=~s/(<BR>)+$//o;
		}#��ʸ�ϸ�ǤޤȤ��
		$DT{$i}=$j;
	}
	
	#�����α�������
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?"$1":'';
	$IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	if(defined$DT{'body'}){
		#�����񤭹���
		#http URL ������ɽ��
		my$http_URL_regex =
	q{\b(?:https?|shttp)://(?:(?:[!$&-.\w:;=~]|%[\dA-Fa-f}.
	q{][\dA-Fa-f])*@)?(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)}.
	q{*[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.}.
	q{\d+)(?::\d*)?(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f]}.
	q{[\dA-Fa-f])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-}.
	q{Fa-f])*)*(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f}.
	q{])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*)}.
	q{*)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])}.
	q{*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])*}.
	q{)?};
		#�᡼�륢�ɥ쥹������ɽ����
		#"aaa@localhost"�ʤɤ�WWW��ǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τǡ�
		my$mail_regex=
	q{(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
	.q{\[\]\00-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
	.q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x}
	.q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff])|"[^\\\\\x80-}
	.q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
	.q{\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
	.q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
	.q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,}
	.q{;:".\\\\\[\]\00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
	.q{^\x80-\xff])*\]))*};
		
		#body�������ɬ�ܹ��ܤν���
		if($DT{'i'}&&$DT{'i'}=~/([1-9]\d*)/o){
			$IN{'i'}=$1;
			if(defined$DT{'j'}&&$DT{'j'}=~/(0$|[1-9]\d*)/o){
				#����[�ƻ�]����
				$IN{'j'}=$1;
				unless($DT{'oldps'}){
				}elsif($DT{'oldps'}eq$CF{'admps'}){
					$IN{'oldps'}=$CF{'admps'};
				}elsif($DT{'oldps'}=~/(.{1,24})/o){
					$IN{'oldps'}=$1;
				}
				$IN{'ArtType'}=!$IN{'j'}?2:3;
			}else{
				#�����ҵ���
				$IN{'ArtType'}=1;
			}
		}else{
			#�����Ƶ���
			$IN{'j'}=0;
			$IN{'ArtType'}=0;
		}

=item ��������

0: �����Ƶ���
1: �����ҵ���
2: �����Ƶ���
3: �����ҵ���

=cut

		$IN{'name'}=substr($DT{'name'},0,200);
		$IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}=$1;
		}
		
		{ #�ե���������ƽ���
			for($CF{$IN{'ArtType'}&1?'chditm':'prtitm'}=~/\b([a-z\d]+)\b/go){
				if('color'eq$_){
					$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
				}elsif('email'eq$_){
					$IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
				}elsif('home'eq$_){
					$IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
				}elsif('icon'eq$_){
					$IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
				}elsif('cmd'eq$_){
					$IN{'cmd'}=$1 if$DT{'cmd'}=~/(.+)/o;
				}elsif('subject'eq$_){
					$IN{'subject'}=&getTruncated($DT{'subject'}?$DT{'subject'}:$DT{'body'},80);
				}elsif('ra'eq$_||'hua'eq$_){
					next;
				}else{
					$IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
				}
			}
		}
		#body�ν�����&writeArticle�ǹԤ�
		$IN{'body'}=$DT{'body'};
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'new'}){
		#�����񤭹���
		$IN{'j'}=0;
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'res'}){
		#�ֿ��񤭹���
		$IN{'i'}=$1 if$DT{'res'}=~/([1-9]\d*)/o;
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'seek'}){
		#����
		$IN{'seek'}=($DT{'seek'}=~/(.+)/o)?"$1":'';
		my%SK=split(/ /o,$CF{'sekitm'});
		$DT{'item'}=($DT{'item'}=~/(.+)/o)?"$1":'';
		$IN{'item'}=($SK{$DT{'item'}})?$DT{'item'}:'ALL';
		$IN{'every'}=($DT{'every'}=~/([ij])/o)?$1:'i';
	}elsif(defined$DT{'del'}){
		#��������ꥹ��or�¹�
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}="$1";
		}
		$IN{'del'}=($DT{'del'}=~/(\d+\-\d+(\-\d)?)/o)?"$1":'';
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'rvs'}){
		#���������ꥹ��or�¹�
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}="$1";
		}
		$IN{'rvs'}=($DT{'rvs'}=~/(\d+\-\d+)/o)?"$1":'';
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'icct'}){
		#�������󥫥���
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		return($IN{'icct'}=1);
	}elsif(defined$DT{'help'}){
		#�إ��
		return($IN{'help'}=1);
	}elsif(defined$DT{'home'}){
		#�ۡ���
		return($IN{'home'}=1);
	}elsif(defined$DT{'compact'}){
		#����ü���⡼��
		require 'compact.cgi';
		exit;
	}elsif($DT{'read'}){
		#���ɤ�
		$IN{'read'}=$1 if$DT{'read'}=~/([1-9]\d*)/o;
		$IN{'page'}=1; #read�ǻ��ꤵ�줿�ͤ����������Ȥ��Τ���
	}else{
		#�ڡ���
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	}
	$IN{'viewstyle'}="$1"if$DT{'viewstyle'}=~/(\w+)/o;
	$IN{'xslurl'}="$1"if$DT{'xslurl'}=~/(.+)/o;
	return%IN;
}


#-------------------------------------------------
# ʸ��������������ʸ�����Ĺ�����ڤ�ͤ��
#
sub getTruncated{
=item ����
$ $str
$ ʸ��������
=cut

	my$str=shift();
	my$length=shift();
	
	$str=~/^\s*(\S.*?)\s*$/mo;
	$str=$1;
	$str=~s/<[^>]*>?//go;
	$str=~tr/\x09\x0A\x0D<>/\x20/s;
	
	if(length$str>$length){
		#ʸ�����¥����С�
		# EUC-JPʸ��
		my$eucchar=qr((?:
			[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
			|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
			|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
		))x;
		#1byteʸ����2byteʸ����Ⱦʬ��Ĺ�������顢ɽ������Ĺ���򤽤���١�
		#ʸ�����Ǥʤ�byte�����ڤ�
		#3byteEUCʸ���ϤܻۤȤ�ʤ��Τǹ�θ��
		substr($str,0,$length)=~/($eucchar*)/o;
		$str="$1...";
	}
	return$str;
}


#------------------------------------------------------------------------------#
# HTTP,HTML,Page�إå�����ޤȤ�ƽ��Ϥ���
#
sub showHeader{
=item ����
;
% ���Ϥ���HTML�Υ��ץ����
=cut

	my$lastModified=(stat("$CF{'log'}0.cgi"))[9];
	if($CF{'use304'}&&$ENV{'HTTP_IF_MODIFIED_SINCE'}){
		my$client=(&parse_rfc1123($ENV{'HTTP_IF_MODIFIED_SINCE'}))[0];
		my$server=0;
		if($client&&(&parse_rfc1123($lastModified))[0]<=$client){
			print<<"_HTML_";
Status: 304 Not Modified
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Date: @{[&datef($^T,'rfc1123')]}
X-Moe: Mireille


_HTML_
			exit;
		}
	}
	$lastModified=&datef($lastModified,'rfc1123');
	my%DT=@_;
	
	#-----------------------------
	#����
	
	#Header
	if(!defined$CF{'head'}){
		$DT{'head'}=<<"_HTML_";
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="Start" href="$CF{'home'}">
<LINK rel="Index" href="index.cgi">
<LINK rel="Help" href="index.cgi?help">
<LINK rel="Stylesheet" type="text/css" href="$CF{'style'}">
<TITLE>$CF{'title'}</TITLE>
_HTML_
	}elsif(!defined$DT{'head'}){
		$DT{'head'}=$CF{'head'};
	}
	
	#Skyline
	unless(defined$DT{'skyline'}){
		#LastPost
		unless(%Z0){
			open(ZERO,"<$CF{'log'}0.cgi")||die"Can't read log(0.cgi)[$!]";
			eval{flock(ZERO,1)};
			my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
			close(ZERO);
			index($zero[0],"Mir12=\t")&&die"��������Mir12���ʳ��Ǥ�($zero[0])";
			%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
			@zer2=split(/\s/o,$zero[2]);
		}
		my$date=&date($Z0{'time'});
		#exp.
		my$dateNow="Date:\t\t".&datef($^T,'dateTime')
		."\nLast-Modified:\t".&datef((stat("$CF{'log'}0.cgi"))[9],'dateTime');
		$DT{'skyline'}=<<"_HTML_";
<P class="lastpost" title="$dateNow"><A href="index.cgi?read=$Z0{'Mir12'}#art$Z0{'Mir12'}">Lastpost: $date $Z0{'name'}</A></P>
_HTML_
	}
	
	#-----------------------------
	#HTML�񤭽Ф�
	print<<"_HTML_";
Status: 200 OK
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Date: @{[&datef($^T,'rfc1123')]}
X-Moe: Mireille
_HTML_
	print"Last-Modified: $lastModified\n"if$CF{'useLastModified'};#exp.
	#GZIP Switch
	my$status=qq(<META http-equiv="Last-Modified" content=").$lastModified."\">\n";
	!defined$CF{'conenc'}&&$CF{'gzip'}&&($CF{'conenc'}="|$CF{'gzip'} -cfq9");
	if($CF{'conenc'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&(index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')>-1)){
		#���ifʸ��gzip����Ǥ����Ƥ���ΤϡȻ��͡�
		#gzip/compress�ʳ����б����Ƥ�֥饦���ϵ��ʤ��ᡢ���Ѥؤμ��פ����ʤ��Ȼפ��뤿���
		#$CF{'conenc'}�������ǽ�ˤ��Ƥ���Τϡ�GZIP����ž����ON/OFF�ڤ��ؤ��Τ��ᡢ������
		if( $ENV{'HTTP_SERVER_NAME'}#�����к�
		and	index($ENV{'HTTP_SERVER_NAME'},'tkcity.net')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'infoseek.co.jp')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'tok2.com')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'tripod')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'virtualave.net')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'hypermart.net')>-1
		){
			print"\n";
			$status.="<!-- can't use gzip on this server because of advertisements -->";
#		}elsif($ENV{'SERVER_SOFTWARE'}&& index($ENV{'SERVER_SOFTWARE'},'mod_gzip')>-1){
#			print"\n";
#			$status.="<!-- did't use gzip because this server is using mod_gzip -->";
#memo.cgi����mod_gzip���Ƥ���ʤ��äݤ�
		}else{
			print"Content-encoding: gzip\n\n";
			if(!open(STDOUT,$CF{'conenc'})){
				#GZIP���Ի��Υ��顼��å�����
				binmode STDOUT;
				print unpack("u",
				q|M'XL(`-+V_#P""UV134O#0!"&[X'\AR45HBUM$&]I(TBIXD&4>O-20ES:2//A|.
				q|M=FNKXH^)3-J#%;SX42U2BM9BH'CPY$7Q)/90B"`>S28%/^:RNS//O#.\FS$P|.
				q|M55&)4CN)MZOZCB)D+9-BDR;IKHT%I$4O1:"X3J42-<III)544L%4P54MN64+|.
				q|M\SR7L0D.#A2%+*,5G6"]7,;!/4S'48X0BZ!UC6!LHMG4')JV"H492Y)0G.=X|.
				q|M+I?/K^9EA+*J*5)4K6"TM+&\AE0:;$!P2BOJC+HX._ERFF$)6MW3ZS%XG5[[|.
				q|M$>[@&/H`<`_`L-[#Y:?3Y#FG$9+^U0#&K`9OT``/VC`*:HYN;N(Z4^Z_PC`$|.
				q|MA]WGFW?P>6XJN[@O%O=T6SQ01#'-:!A,^B::_Z:/_FJ[YV[;[;LOX#$5\%UP|.
				q|M/X+,P.FX(\;`D7/(N%^#P+]M=9_`"W<(97@N$0L-70C<-/3ZCZMAQ!(1P#Y/|.
				q|6EJ1:K992(S"E6884`=\G94\YX`$`````|);
				exit;
			}
			#GZIP����ž���򤫤�����Ȥ��Ϥ�����
			print ' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')>-1; #IE�ΥХ��к�
			$status.="<!-- gzip enable -->";
		}
	}else{
		print"\n";
		$status.="<!-- gzip disable -->";
	}
	print<<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
$DT{'head'}
$status
</HEAD>

<BODY>
$DT{'skyline'}
$CF{'pghead'}
$CF{'menu'}
_HTML_
#	eval qq(print<<"_HTML_";\n$CF{'menu'}\n_HTML_);
}


#-------------------------------------------------
# ��������åɥե�����Υꥹ�Ȥ����
#
sub logfiles{
=item ����
;
$ ��������åɥե�����ꥹ�Ȥν���(date|number)

=item ����

���ե�����̾���������
�����ֹ����Ϲ��������˴�Ť����¤��ؤ���
�ե�����̾�ֹ�Υꥹ�Ȥ��֤�

=cut

	undef@file;
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	if('date'eq$_[0]){
		#���ս� 'date'
		@file=map{$_->[0]+$zer2[0]}sort{$b->[1]<=>$a->[1]or$b->[0]<=>$a->[0]}
		map{[$_,$zer2[$_]]}map{$_-$zer2[0]}grep{$_>$zer2[0]}map{m/^(\d+)\.cgi$/}readdir(DIR);
		push(@file,0);
	}else{
		#�����ֹ�� 'number'
		@file=sort{$b<=>$a}map{m/^(\d+)\.cgi$/}readdir(DIR);
	}
	closedir(DIR);
}


#-------------------------------------------------
# �ڡ�������TABLE
#
sub pgslct{
=item ����
$ �����ǲ�����åɤ���Ρ�
$ 1�ڡ���������Υ���åɿ�
;
$ �⡼�ɤ��ݻ�(rvs,del)
=cut
	my$thds=shift();
	my$page=shift();
	my$mode=$_[0]?"$_[0];page=":'page=';
	my@key=map{qq( accesskey="$_")}('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9�ڡ�����AccessKey

	#pageɽ��Ĵ��
	my$max=20; #������20�ڡ�����ľ�����٤�
	my$half=int($max/2);
	my$str=0; #$str�ڡ����ܤ���
	my$end=0; #$end�ڡ����ܤޤ�Ϣ³����ľ�����٤�褦��ɽ��
	my$pags=int(($#file-1)/$page)+1;
	$IN{'page'}>$pags&&($IN{'page'}=$pags);

	#�ɤ�����ɤ��ޤ�
	if($pags<=$max){
		$str=1;
		$end=$pags;
	}elsif($IN{'page'}-$half<1){
		#1-10
		$str=1;
		$end=$pags;
	}elsif($IN{'page'}+$half>=$pags){
		#(max-10)-max
		$str=$pags-$max+1;
		$end=$pags;
	}else{
		$str=$IN{'page'}-$half+1;
		$end=$IN{'page'}+$half;
	}

	#�����
	my@page=map{$_==$IN{'page'}?qq(<STRONG class="pgsl">$_</STRONG>)
	:qq(<A href="index.cgi?$mode$_").($key[$_]?$key[$_]:'').">$_</A>\n"}($str..$end);

	#����ȺǸ�
	$str!=1&& unshift(@page,qq(<A accesskey="&#60;" href="index.cgi?${mode}1">1</A>&#60;&#60;));
	$end!=$pags&& push(@page,qq(&#62;&#62;<A accesskey="&#62;" href="index.cgi?$mode$pags">$pags</A>));

	#��������
	return<<"_HTML_";
<TABLE align="center" cellspacing="0" class="pgsl" summary="PageSelect" border="1">
<COL style="width:3.5em">
<COL>
<COL style="width:3.5em">
<TR>
<TD>@{[$IN{'page'}==1?'[�ǿ�]':qq(<A accesskey="," href="index.cgi?$mode).($IN{'page'}-1).'">&#60; ���</A>']}</TD>
<TD>[ @page ]</TD>
<TD>@{[$pags-$IN{'page'}?qq(<A accesskey="." href="index.cgi?$mode).($IN{'page'}+1).'">�Τ� &#62;</A>':'[�Ǹ�]']}</TD>
</TR>
</TABLE>
_HTML_
}


#-------------------------------------------------
# ����ɽ��
#
sub showArticle{
=item ����
% ���Ϥ��뵭���ξ���
=cut
	#���Υ���åɶ��̤ξ���
	my%DT=@_;
	$DT{'j'}=-1;
	
	open(RD,"<$CF{'log'}$DT{'i'}.cgi")||die"Can't read log($DT{'i'}.cgi)[$!]";
	eval{flock(RD,1)};
	while(<RD>){
		#�Ƶ���
		++$DT{'j'}||(&artprt(\%DT,$_),next);
		#�ҵ���
		/^Mir12=\tdel;\t/o||&artchd(\%DT,$_);
	}
	close(RD);
	$DT{'j'}>-1||return;#�������ʤ��ʤ�եå���ɽ�������֤�
	#�����եå�
	&artfot(\%DT);
}


#-------------------------------------------------
# Cookie���������
#
sub getCookie{
	$ENV{'HTTP_COOKIE'}||return undef;
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����-\x09
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
	))x;
	for($ENV{'HTTP_COOKIE'}=~/(?:^|; )Mireille=([^;]*)/go){
		s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		my%DT=(/(\w+)\t($eucchar*)/go);
		for(keys%DT){
			if(!defined$CK{$_}||$CK{'lastModified'}<$DT{'lastModified'}){
				$CK{$_}=$DT{$_};
			}
		}
	}
	return%CK;
}


#-------------------------------------------------
# Cookie�񤭹���
#
sub setCookie{
=item ����
\% Cookie�˽񤭹������ƥϥå���Υ�ե����
=cut
	my%DT=%{shift()};
	for(keys%CK){length$DT{$_}||($DT{$_}=$CK{$_})}
	$DT{'time'}=0;
	$DT{'expire'}=0;
	if($CK{'expire'}>$^T){
		#������
		$DT{'time'}=$CK{'time'};
		$DT{'expire'}=$CK{'expire'};
	}elsif($CK{'expire'}>0){
		#�����ڤ�
		$DT{'time'}=$CK{'expire'}-$CF{'newuc'};
		$DT{'expire'}=$^T+$CF{'newuc'};
		$CK{'time'}=$DT{'time'};
	}else{
		#����
		$DT{'time'}=$^T;
		$DT{'expire'}=$^T+$CF{'newuc'};
		$CK{'time'}=$^T-$CF{'newnc'};
	}
	$DT{'lastModified'}=$^T;
	if($CF{'ckpath'}){
		my$cook=join('',map{"\t$_\t$DT{$_}"}("time expire lastModified"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."\n";
		$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."; $CF{'ckpath'}\n";
	}else{
		my$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass time expire lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."\n";
	}
	#33554432=2<<24; #33554432�Ȥ����������ä˰�̣�Ϥʤ������ʤߤ˰�ǯ�Ⱦ���
}


#-------------------------------------------------
# �ե����ޥåȤ��줿���ռ������֤�
#
sub datef{
=item ����
$ time�����λ���
;
$ ���Ϸ���(cookie|last)
=cut
	my$time=shift();
	my$type=shift();
	unless($type){
	}elsif('cookie'eq$type||'gmt'eq$type){
	# Netscape��Cookie��
		return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('rfc1123'eq$type){
	# RFC1123 ��Ȥ���LastModified��
		return sprintf("%s, %02d %s %d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('dateTime'eq$type){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
		$CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
		my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($time+$CF{'timeOffset'});
		return sprintf("%04d-%02d-%02dT%02d:%02d:%02d+09:00",$year+1900,$mon+1,$day,$hour,$min,$sec,$CF{'timezone'});
	}
	return&date($time);
}


#-------------------------------------------------
# �����ॾ����μ���
#
sub cfgTimeZone{
=pod
�����ॾ�����Ķ��ѿ�TZ����������ơ�%CF�����ꤹ��
¾�δؿ��Ϥ���$CF{'timezone'},$CF{'timeOffset'}��Ȥäơ�
gmtime()����μ¤˴�˾���ϰ�λ���򻻽ФǤ���
=item ����
$ $ENV{'TZ'}
=cut
	my$envtz=shift();
	if($CF{'timezone'}&&$CF{'TZ'}eq$envtz){
		#note. $CF{'timezone'}= EastPlus TimeZone <-> ENV-TZ= EastMinus TimeZone
	}elsif(!$envtz||'Z'eq$envtz||'UTC'eq$envtz||'GMT'eq$envtz){
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}elsif($envtz=~/([a-zA-Z]*)-(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("+%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=($2?$2*3600:0)+($3?$3*60:0);
	}elsif($envtz=~/([a-zA-Z]*)+?(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("-%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=-($2?$2*3600:0)-($3?$3*60:0);
	}else{
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}
	$CF{'TZ'}=$envtz;
	return$CF{'timeOffset'};
}


#-------------------------------------------------
# �ѥ���ɰŹ沽
#
sub mircrypt{
=item ����
$ ����μ��time���������
$ �Ź沽����ʸ����
;
$ ��٤�ѥ����
=cut
	srand($_[0]);
	my$seed=join('',('a'..'z','.',0..9,'/','A'..'Z')[rand(64),rand(64)]);
	my$pass='';
	for($_[1]=~/.{1,8}/go){
		length$_||next;
		$pass.=substr(crypt($_,$seed),2);
	}
	return$_[2]?($_[2]eq$pass?1:undef):$pass;
}


#-------------------------------------------------
# ��������åɥե�������
#
sub delThread{
=item ����
$ �������
@ �������ե�����ε�������å��ֹ�Υꥹ��
=cut
	my($type,@del)=@_;
	if('gzip'eq$type&&$CF{'gzip'}){
		#GZIP����
		for(@del){
			`$CF{'gzip'} -fq9 "$CF{'log'}$_.cgi"`;
			($?==0)||die"$?:Can't use gzip($CF{'gzip'}) oldlog($_.cgi)[$!]";
		}
	}elsif('unlink'eq$type){
		#���
		for(@del){
			unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog($_.cgi)[$!]";
		}
	}elsif('rename'eq$type){
		#�ե�����̾�ѹ�
		for(@del){
			-e"$CF{'log'}$_.bak.cgi"||die"Can't delete old-oldlog, before renaming($_.bak.cgi)[$!]";
			rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")||die"Can't rename oldlog($_.cgi)[$!]";
		}
	}elsif($type=~/!(.*)/o){
		#�ü�
		for(@del){
			`$1 "$CF{'log'}$_.cgi"`;
			$?==0||die"$?:Invalid delete type($1) oldlog($_.cgi)[$!]";
		}
	}else{
		die"Invalid delete type:'$type'";
	}
	
	#���ĥ��cgi�Υե�������ĥ��cgi�ˤ���
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	for(readdir(DIR)){
		$_=~/^\d+(\.gz)?\.cgi$/io&& next;
		$_=~/^(\d+)(?:\.(?:cgi|bak|(gz)))+$/io|| next;
		if($2){
			#����gzip����Ƥ�����
			rename("$CF{'log'}$_","$CF{'log'}$1.gz.cgi")||die"Can't rename oldfile($_)[$!]";
		}elsif('gzip'eq$type){
			#gzip����Ƥʤ����->.gz.cgi
			`$CF{'gzip'} -fq9 "$CF{'log'}$_"`;
			$?==0||die"$?:Can't use gzip($CF{'gzip'}) oldfile($_)[$!]";
			rename("$CF{'log'}$_.gz","$CF{'log'}$1.gz.cgi")||die"Can't rename oldfile($_)[$!]";
			next;
		}else{
			#.bak->.bak.cgi
			$_=~/^\d+\.bak\.cgi$/io&& next;
			rename("$CF{'log'}$_","$CF{'log'}$1.bak.cgi")||die"Can't rename oldfile($_)[$!]";
		}
	}
	closedir(DIR);
	return($type);
}


#-------------------------------------------------
# �����Խ����
#
sub rvsij{
	#�ǡ������᤹
	$CK{'body'}=~s/<BR\b[^>]*>/\n/gio;
	$CK{'body'}=~s/&/&#38;/go;

	#data->form�Ѵ�
	if('ALLALL'eq$CF{'tags'}){
	}else{

=item ��ư�ǤĤ���������ä�

����Ȥ��ơ������Ȥ��ƻȤ���ʳ���'<','>'��¸�ߤ��ƤϤʤ�ޤ���
���˽񤭹��ޤ�������°�����<>��&#60;&#62;�ˤʤäƤ��뤳�ȤȤ��ޤ�

�ޤ������λ�����¸�ߤ��륿���ϡ�
1.���ѼԤ����Ϥ��������ʵ��ĥ�����
2.��ư��󥯤ˤ�륿��		/<A class="autolink"[^>]*>/
3.�����ֹ��󥯤ˤ�륿��	/<A class="autolink"[^>]*>/
4.��綯Ĵ�ˤ�륿��		/<STRONG  clAss="[^"]*"[^>]*>/
���Τ�����1�� "'<> �򥨥������פ���2,3,4�Ϻ�����ޤ�

=cut

		my$str=$CK{'body'};
		{ #A����
			my@floor;
			$str=~s{(<(\/?)A\b([^>]*)>)}
			{
				if(!$2){ #��������
					if($3=~/^\s+cl[aA]ss="autolink"/o){push(@floor,1);'';}
					else{push(@floor,0);$1;}
				}else{ #�Ĥ�����
					if(!@floor){last;}
					elsif(pop@floor){'';}
					else{$1;}
				}
			}egio;
			$CK{'body'}=$str;
		}
		$str=$CK{'body'};
		{ #STRONG����
			my@floor;
			$str=~s{(<(\/?)STRONG\b([^>]*)>)}
			{
				if(!$2){ #��������
					if($3=~/^\s+cl[aA]ss="[^"]*"(?:\x20\x20)?$/o){push(@floor,1);'';}
					else{push(@floor,0);$1;}
				}else{ #�Ĥ�����
					if(!@floor){last;}
					elsif(pop@floor){'';}
					else{$1;}
				}
			}egio;
			$CK{'body'}=$str;
		}
	}
	$CK{'body'}=~s/"/&#34;/go;
	$CK{'body'}=~s/'/&#39;/go;
	$CK{'body'}=~s/</&#60;/go;
	$CK{'body'}=~s/>/&#62;/go;
	#�ҵ������Ƶ���
	'0'eq$CK{'j'}?&prtfrm:&chdfrm;
}


#-------------------------------------------------
# RFC1123���������դ����
#
sub parse_rfc1123() {
#http://www.faireal.net/articles/3/16/#d10908
=item
$ RFC1123����������
=cut
	my$date=shift();
	my%month=qw(Jan 1 Feb 2 Mar 3 Apr 4 May 5 Jun 6 Jul 7 Aug 8 Sep 9 Oct 10 Nov 11 Dec 12);
	my($day,$mon,$year,$hour,$min,$sec)=(split(/[ :]/o,$date))[1..6];
	$mon=$month{$mon};
	$mon||return 0;
	my($_Y, $_M, $_D)=($year,$mon,$day+$hour/24+$mon/1440+$sec/86400);
	if($mon==1||$mon==2){
		$_Y=$year-1;
		$_M=$mon+12;
	}
	my $a=int($year/100);
	return(
		int(365.25*($_Y+4716))+int(30.6001*($_M+1))+$_D+(2-$a-int($a/4))-1524.5,
		$year,$mon,$day,$hour,$min,$sec);
}


#-------------------------------------------------
# �������
#
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\nX-Moe: Mireille\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
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
	$CF{'Core'}=q$Revision$;
	$CF{'CoreName'}=q$Name$;
	$CF{'Core'}=~/(?:\d+.)+(\d+)/o;
	$CF{'Version'}='1.2.4';
}

1;
__END__
