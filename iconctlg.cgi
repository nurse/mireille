#!/usr/local/bin/perl
#------------------------------------------------------------------------------#
# 'IconCatalog' IconCatalog for MireilleIconList0.x
# - Icon Catalog Module -
#
$CF{'iconCatalog'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $rcsid = q$Id$;
require 5.005;
use strict;
use vars qw(%CF %IN %CK);

=head1 NAME

iconCatalog - Show Icon Catalog with MireilleIconList0.x

=head1 SYNOPSIS

Ŭ�������ꤷ�����֤��ƥ�󥯤�ĥ��Ф褤

C< E<lt>A href="iconctlg.cgi"E<gt>�����������E<lt>/AE<gt> >
iconctlg.cgi��Ŭ�ڤ����ꤵ��Ƥ���С��������������ɽ�������ϥ���

=head1 DESCRIPTION

Mireille�δ���CGI��Υ���������������ʬ���ڤ�Ф�����Τǡ�
Mireille���饤��ݡ��Ȥ��Ƥ�Ȥ��뤷��ñ�ȤǤ�Ȥ��ޤ���

�����icon.html�����ƤΥ�����������̤�ɽ�����뤿�ᡢ
���̤Υ����������Ͽ�������֤Ǥ�˽��Ū��¸�ߤȤʤäƤ��ޤ�������
�ڡ���ʬ�䵡ǽ����ܤ������ᡢ����ʤ��Ȥ�ʤ��ʤ�ޤ�����

=head1 CODES

=cut

&main;

sub main{
	if($CF{'program'}eq __FILE__){
		#ľ�ܼ¹ԤΤȤ�
		$CF{'iconList'}='icon.txt';
		$CF{'iconDir'}=	'/icon/full/';
		$CF{'name'}=	'Airemix';
		$CF{'home'}=	'http://airemix.com/';
		$CF{'index'}=	'index.cgi';
		$CF{'pgtitle'}=	'Airemix Icon Catalog System';
		$CF{'style'}=	'style.css';
		$CF{'menu'}='';

#-----------------------------
# Page Header
$CF{'pghead'}=<<"_CONFIG_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageHeader" width="90%"><TR>
<TH width="100%"><H1 class="head" align="left">$CF{'pgtitle'}</H1></TH>
<TD nowrap>��������������</TD>
</TR></TABLE></DIV>
_CONFIG_

#-----------------------------
# Page Footer
$CF{'pgfoot'}=<<"_CONFIG_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="PageFooter" width="90%"><TR>
<TD nowrap>��������������</TD>
<TH width="100%"><DIV class="head" align="right"><A href="$CF{'index'}">BACK to INDEX</A></DIV></TH>
</TR></TABLE></DIV>
_CONFIG_

		$CF{'bodyHead'}='';
		$CF{'bodyFoot'}='';
		$CF{'iched'}='';
		$CF{'icfot'}='';
		&getParam;
		if(!$IN{'mode'}){
		}elsif('convert'eq$IN{'mode'}){
			my$iconlist;
			#ñ�쥢������ꥹ���ɤ߹���
			open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist($CF{'iconList'})[$?:$!]";
			eval{flock(RD,1)};
			read(RD,$iconlist,-s$CF{'iconList'});
			close(RD);
			print scalar&generateEalis3qw(&parseMir0x($iconlist));
			exit;
		}
		&iconctlg;
	}else{
		#�ץ���ऴ�Ȥ��ɤ餮��Ĵ��
		$CF{'menu'}||='';
		$CF{'bodyHead'}||='';
		$CF{'bodyFoot'}||='';
		$CF{'iconList'}||=$CF{'icls'}||'';
		$CF{'iconDir'}||=$CF{'icon'}||$CF{'icondir'}||'';
		defined$IN{'page'}||($IN{'page'}=1);
		
		$CF{'bodyHead'}='<DIV style="margin:1em 0 0 0">'.$CF{'bodyHead'}.'</DIV>'unless$CF{'noAddDivToBodyHead'};

	}
}


#-------------------------------------------------
# ����������
#
sub iconctlg{

=head2 iconctlg

���������ܤ�������Ԥ�HTML�Ȥ���CGI��ͳ�ǽ��Ϥ���

=over 4

=cut

	my@others=();
	my%CR;
	my@icon=();

	#��������ꥹ���ɤ߹���
	my$iconlist='';
	if($CF{'iconList'}=~/^ /o){
		#ʣ����������ꥹ���ɤ߹���
		for($CF{'iconList'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
			$_||next;
			my$tmp;
			open(RD,'<'.$_)||die"Can't open multi-iconlist($_)[$?:$!]";
			eval{flock(RD,1)};
			read(RD,$tmp,-s$_);
			close(RD);
			$iconlist.=$tmp;
		}
	}else{
		#ñ�쥢������ꥹ���ɤ߹���
		open(RD,'<'.$CF{'iconList'})||die"Can't open single-iconlist($CF{'iconList'})[$?:$!]";
		eval{flock(RD,1)};
		read(RD,$iconlist,-s$CF{'iconList'});
		close(RD);
	}
	
	my@pages=$iconlist=~/<!--\s*(%PAGE-BREAK(?:\s+.*?)?)\s*-->/go;
	my$pages=@pages+1;
	
	#$IN{'page'}�����Ķ��������Ǥ���ɽ������
	$IN{'page'}>$pages&&($IN{'page'}=0);
	
	my$page=1; #�����ڡ����ܡ�
	my$j=0; #�������ܡ�
	my$cols=6; #6��ǲ���
	my$aGroup=''; #optgroup��Ĥ򤳤�˰��Ū�˳�Ǽ����
	for(&parseMir0x($iconlist)){
		my%DT=%{$_};
		#���ޥ��ʬ��
		if('TAG'eq$DT{'cmd'}){
			$IN{'page'}&&$page!=$IN{'page'}&& next;
			#$IN{'page'}==0��$page==$IN{'page'}�λ��Τߤ����겼��¹�
			if('OPTION'eq$DT{'swt'}){
				if(!$j){
					#others
					push(@others,qq(<TD><IMG src="$CF{'iconDir'}$DT{'value'}")
					.qq( alt="" title="$CF{'iconDir'}$DT{'value'}"><BR>$DT{'label'}</TD>\n));
				}else{
					$aGroup.="<TR>\n"if$j==1;
					$aGroup.=qq(<TD><IMG src="$CF{'iconDir'}$DT{'value'}")
					.qq( alt="" title="$CF{'iconDir'}$DT{'value'}"><BR>$DT{'label'}</TD>\n);
					if(++$j>$cols){
						$aGroup.="</TR>\n";
						$j=1;
					}
				}
			}elsif('OPTGROUP'eq$DT{'swt'}){
				$aGroup=<<"_HTML_";
<DIV class="box">
<P class="h">$DT{'label'}</P>
<TABLE cellspacing="0" summary="$DT{'label'}">
<COL span="$cols" width="110">
_HTML_
				$j=1;
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				for(keys%CR){
					if($CR{$_}{'LINK'}){
					}elsif($CR{$_}{'NAME'}&&$CR{$_}{'URL'}){
						$CR{$_}{'LINK'}=qq(<A href="$CR{$_}{'URL'}" title=")
						.(('VENDOR'eq$_)?'�����':'�켡�����').qq(">$CR{$_}{'NAME'}</A>);
					}elsif($CR{$_}{'NAME'}){
						$CR{$_}{'LINK'}=$CR{$_}{'NAME'};
					}elsif($CR{$_}{'URL'}){
						$CR{$_}{'LINK'}=qq(<A href="$CR{$_}{'URL'}" title=")
						.(('VENDOR'eq$_)?'�����':'�켡�����').qq(">$CR{$_}{'URL'}</A>);
					}
				}
				
				my$copy='';
				if($CR{'VENDOR'}{'LINK'}&&$CR{'COPY1'}{'LINK'}){
					$copy="&#169;$CR{'COPY1'}{'LINK'} &gt;&gt; by $CR{'VENDOR'}{'LINK'}";
				}elsif($CR{'VENDOR'}{'LINK'}){
					$copy="by $CR{'VENDOR'}{'LINK'}";
				}elsif($CR{'COPY1'}{'LINK'}){
					$copy="&#169;$CR{'COPY1'}{'LINK'}";
				}
				$aGroup.="</TR>\n"if$j>1;
				$aGroup.=<<"_HTML_";
</TABLE>
<P class="footer">$copy</P>
</DIV>

_HTML_
				$j=0;
				push(@icon,$aGroup);
			}
		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
			#���ڡ���������
			$page++==$IN{'page'}&& last;
		}elsif('COPY'eq$DT{'cmd'}){
			if('BEGIN'eq$DT{'swt'}){
				undef$CR{$DT{'type'}};
			}elsif('END'eq$DT{'swt'}){
				undef$CR{$DT{'type'}};
			}elsif('SET'eq$DT{'swt'}){
				$CR{$DT{'type'}}{$DT{'key'}}=$DT{'value'};
			}
		}
		#next;
	}

=item �Ǹ��optgroup���Ĥ����Ƥ��ʤ����

��������Ĥ��Ƥ�����

=cut

	if($j){
		my$copy='';
		if($CR{'VENDOR'}{'LINK'}&&$CR{'COPY1'}{'LINK'}){
			$copy="&#169;$CR{'COPY1'}{'LINK'} &gt;&gt; by$CR{'VENDOR'}{'LINK'}";
		}elsif($CR{'VENDOR'}{'LINK'}){
			$copy="by$CR{'VENDOR'}{'LINK'}";
		}elsif($CR{'COPY1'}{'LINK'}){
			$copy="&#169;$CR{'COPY1'}{'LINK'}";
		}
				$aGroup.="</TR>\n"if$j>1;
				$aGroup.=<<"_HTML_";
</TABLE>
<P class="footer">$copy</P>
</DIV>

_HTML_
		push(@icon,$aGroup);
	}

=item ʬ�ࡧ����¾���ν���

OPTGROUP�λ����ǤǤʤ�OPTION�����ơ�ʬ�ࡧ����¾(Others)�Ȥ���

=cut

	if($#others>-1){
		$aGroup=<<"_HTML_";
<DIV class="box">
<P class="h">����¾</P>
<TABLE cellspacing="0" summary="����¾">
<COL span="$cols" width="110">
<TR>
_HTML_
		my$j=0;
		for(@others){
			$aGroup.="<TR>\n"if$j==1;
			$aGroup.=$_;
			if(++$j==$cols){
				$aGroup.="</TR>\n";
				$j=1;
			}
		}
		$aGroup.="</TR>\n"if$j>1;
		$aGroup.=<<"_HTML_";
</TABLE>
</DIV>

_HTML_
		push(@icon,$aGroup);
	}
	undef$aGroup;
	
	#-----------------------------
	# HTML����

=item HTML����

$encoding�ǽ��Ϥ���HTML�δ��������ɤ����Ǥ���
����Ͼ���Airemix�ʳ���CGI���Ȥ߹��ޤ줿�Ȥ��ˡ�
Shift_JIS�Τۤ����Թ礬�����Ȥ�������Ȼפ��뤿��

HTML-META-Last-Modified����Ϥ��Ƥ���
WWWC�ǥ����å����褦�ʿͤ����ʤ��Ȥϸ¤�ʤ��Τ�

=cut

	my$encoding='euc-jp';
	my$status=sprintf(qq(<META http-equiv="Last-Modified" content="%s, %02d %s %s %s GMT">\n)
	,(split(/\s+/o,gmtime((stat$CF{'iconList'})[9])))[0,2,1,4,3]);
	my$pageSelector=$pages<=1?'':&pageSelector($pages,undef,'icct',undef,
							['[����]',qq(<A accesskey="," href="$CF{'index'}?%s=%d">&#60; ����</A>)
								,'[�Ǹ�]',qq(<A accesskey="." href="$CF{'index'}?%s=%d">���� &#62;</A>)]);
	my$html=<<"_HTML_";
Content-Language: ja-JP
Content-type: text/html; charset=$encoding

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=$encoding">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<LINK rel="start" href="$CF{'home'}">
<LINK rel="index" href="$CF{'index'}">
<TITLE>: Icon Catalog :</TITLE>
</HEAD>
<BODY>
$CF{'bodyHead'}
$CF{'pghead'}
$CF{'menu'}
<H2 class="heading2">�������󥫥���</H2>
$CF{'iched'}
$pageSelector
<DIV class="iconCatalog">
@icon
</DIV>
$pageSelector
$CF{'icfot'}
$CF{'menu'}
$CF{'pgfoot'}
<DIV class="AiremixCopy">- <A href="http://airemix.com/" target="_blank"
 title=": Airemix :">Airemix iconCatalog</A>
<VAR title="times:@{[times]}">$CF{'iconCatalog'}</VAR> -</DIV>
$CF{'bodyFoot'}
</BODY>
</HTML>
_HTML_
	print('euc-jp'eq$encoding?$html
	:('shift_jis'eq$encoding?euc2sjis($html):die"̤�ΤΥ��󥳡��ǥ���($encoding)�����ꤵ��ޤ���"));
	exit;

=back

=cut

}


#-------------------------------------------------
# �ڡ�������TABLE
#
sub pageSelector{
=item ����
$ �����ǲ�����åɤ���Ρ�
$ 1�ڡ���������Υ���åɿ�
;
$ �⡼�ɤ��ݻ�(rvs,del)
$ ľ�����٤�ڡ�����
$ following / preceding�ǻȤ�ʸ�����arrayRef
=cut
	my$thds=shift||1;
	my$page=shift||1;
	my$mode=$_[0]?"$_[0];page":'page';@_&&shift;
	my$max=$_[0]||20;@_&&shift; #ľ�����٤�ڡ�����
	my$pageText=$_[0]?shift: #�ڡ������쥯���Ѥ�ʸ��
		['[�ǿ�]',qq(<A accesskey="," href="$CF{'index'}?%s=%d">&#60; ���</A>)
		,'[�Ǹ�]',qq(<A accesskey="." href="$CF{'index'}?%s=%d">�Τ� &#62;</A>)];@_&&shift;

	
	#pageɽ��Ĵ��
	my$half=int($max/2);
	my$str; #$str�ڡ����ܤ���
	my$end; #$end�ڡ����ܤޤ�Ϣ³����ľ�����٤�褦��ɽ��
	my$pags=int(($thds-1)/$page)+1;
	my@key=map{qq( accesskey="$_")}('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9�ڡ�����AccessKey
	
	#�ɤ�����ɤ��ޤ�
	if($pags<=$max){
		$str=1;
		$end=$pags;
	}elsif($IN{'page'}-$half<=1){
		#1-10
		$str=1;
		$end=$pags-$max;
	}elsif($IN{'page'}+$half>=$pags){
		#(max-10)-max
		$str=$pags-$max+1;
		$end=$pags;
	}else{
		$str=$IN{'page'}-$half+1;
		$end=$IN{'page'}+$half-1;
	}
	
	#�����
	my@page=map{$_==$IN{'page'}?qq(<STRONG class="current">$_</STRONG>)
	:sprintf qq(<A href="$CF{'index'}?%s=%d"%s>%d</A>),$mode,$_,$key[$_]?$key[$_]:'',$_}$str..$end;
	
	#����ȺǸ�
	unshift(@page,qq(<A accesskey="&#60;" href="$CF{'index'}?$mode=1">1</A> ..))		if$str!=1;
	push(@page,qq(.. <A accesskey="&#62;" href="$CF{'index'}?$mode=$pags">$pags</A>))	if$end!=$pags;
	
	#following / preceding
	my$following=$IN{'page'}==$str?
		$pageText->[0]:sprintf$pageText->[1],$mode,$IN{'page'}-1;
	my$preceding=$IN{'page'}==$end?
		$pageText->[2]:sprintf$pageText->[3],$mode,$IN{'page'}+1;
	
	#��������
	return &getPageSelectorSkin($following,join("\n",@page),$preceding,$str,$end,$pags,$mode);
}


#-------------------------------------------------
# �ڡ�������BOX
sub getPageSelectorSkin{
	my$following=shift;
	my$pageList =shift;
	my$preceding=shift;
#	my($str,$end,$pags,$mode)=@_; #���Ϥ��Ȥ�Ω�Ƥ�������
	return<<"_HTML_";
<TABLE align="center" border="1" cellspacing="0" class="pageSelector">
<TR>
<TD class="following">$following</TD>
<TD class="pageList">[ $pageList ]</TD>
<TD class="preceding">$preceding</TD>
</TR>
</TABLE>
_HTML_
}


#-------------------------------------------------
# ������������Ʊ�������
#
sub getParam{
	my$modifiedFile=$CF{'iconList'};
	my@param=();
	
	#��������
	unless($ENV{'REQUEST_METHOD'}){
		@param=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
		#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
		#�Ǹ�ι���������Τ餻��
		print 'Last-Modified: '
		.sprintf("%s, %02d %s %s %s GMT",(split(/\s+/o,gmtime((stat$modifiedFile)[9])))[0,2,1,4,3])
		."\nContent-Type: text/plain\n\n";
		exit;
	}else{
		my$i='';
		if('POST'eq$ENV{'REQUEST_METHOD'}){
			read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
		}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
			$i=$ENV{'QUERY_STRING'};
		}
		
		if(length$i>262114){ # 262114:�����������ξ��(byte)
			die"������ʤ�Ǥ��̤�¿�����ޤ�\n$i";
		}elsif(length$i>0){
			@param=split(/[&;]/o,$i); #���Ϥ�Ÿ�����ƥϥå����
		}
	}
	
	# EUC-JPʸ��
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
		|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
	))x;
	
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/(\w+)/o)?"$1":'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		$DT{$i}=$j;
	}
	%IN=%{&filteringParams(\%DT)}
}
sub filteringParams{
	my%OLD=%{shift()};
	my%NEW;
	$NEW{'page'}=($OLD{'page'}&&(int$OLD{'page'})=~/([1-9]\d*)/o)?$1:1;
	$NEW{'mode'}=$1 if($OLD{'mode'}&&$OLD{'mode'}=~/(\w*)/o);
	return\%NEW
}

#------------------------------------------------------------------------------#
# List Parsers and Generators
#

#-------------------------------------------------
# Mireille0.x Parser and Generator
#

=head2 Mireille0.x������������ꥹ�Ȥβ��Ϥ�����

Mireille0.x�����ϼ��Mireille��Marldia���Ѥ����륢������ꥹ�ȷ����ǡ�
���ʤ�������HTML�˽񤭽Ф�����ˡ���Ȥ���HTML�����ҤȤ��ƺ��줿�ꥹ�ȷ����Ǥ��롣
HTML���ҤȤ������ʤ�����������ĥ������Ĥ����Ȥ⤹����ѻ��ˤʤ�䤹����
���Τ��ᡢ����ɽ������������Ƥ��ʤ�����Ǥ��Υꥹ�ȷ����򰷤��Τ��񤷤��Ȼפ��롣

=over 4

=cut

sub parseMir0x{
	my$iconlist=shift;
	my@events;
	while($iconlist=~/(.+)/go){
		$_=$1;
		if(/<!--\s*%(\S+)\s+(.*)-->/o){
			#��������Υ��ޥ��
			my$command=$1;
			my$param=$2;$param=~s/\s+$//o;
			if('PAGE-BREAK'eq$command){
				#���ڡ�������
				push(@events,{cmd=>'PAGE-BREAK'});
			}elsif($command=~/([A-Z]+)(_[A-Z]+)*/o){
				#���ɽ������

=item MireilleIconListCommand

 ���٥�ȡ���������ꥹ�Ȥ�̿���ȯ������
 ����¸�ߤ���̿��η����ϰʲ��Τ褦
cmd:    : 'COPY'
swt:  $1: 'BEGIN','END','SET'
type: $2: 'VENDOR','COPY1'
key:  $3: 'NAME','URL','LINK'
value:$4: ̿��ΰ���

=cut

				my@cmds=split('_',$command);
				if('SET'eq$cmds[0]||'VENDOR'eq$cmds[0]||'COPY1'eq$cmds[0]){
					'SET'eq$cmds[0]&& shift@cmds;
					push(@events,{cmd=>'COPY',swt=>'SET',type=>$cmds[0],key=>$cmds[1],value=>$param});
				}elsif('BEGIN'eq$cmds[0]){
					push(@events,{cmd=>'COPY',swt=>'BEGIN',type=>$cmds[1]});
					push(@events,{cmd=>'COPY',swt=>'SET',type=>$cmds[1],key=>'NAME',value=>$param})if$param;
				}elsif('END'eq$cmds[0]){
					push(@events,{cmd=>'COPY',swt=>'END',type=>$cmds[1]});
				}
			}
			next
		}
		
		if(/^\s*<OPTION ([^>]*)\bvalue=(["'])(.+?)\2([^>]*)>([^<]*)(<\/OPTION>)?$/io){

=item OPTION����

 /^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(<\/OPTION>)?$/io
 <TD><IMG $1src="$CF{'iconDir'}$3" alt="$5"$4><BR>$5</TD>\n
 ���٥�ȡ���ĤΥ��������ȯ��
cmd: TAG
swt: OPTION
label: $3: OPTION���Ǥ����� �ޤ��� label°������
value: $5: value°������

=cut

			push(@events,{cmd=>'TAG',swt=>'OPTION',value=>$3,label=>$5});
		}elsif(/^<OPTGROUP ([^>]*)\blabel=(["'])(.+?)\2(.*)>$/io){

=item OPTGOUP���ǻ�

 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 ���٥�ȡ�OPTGROUP������ä�
cmd: TAG
swt: OPTGROUP
label: $3: label°������

=cut

			push(@events,{cmd=>'TAG',swt=>'OPTGROUP',label=>$3});
		}elsif(/<\/OPTGROUP>/io){#</OPTGROUP>

=item OPTGOUP���ǽ�

 /OPTGROUP/io
 ���٥�ȡ�OPTGROUP���˽Ф�
cmd: TAG
swt: /OPTGROUP

=cut

			push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
		}
		next;
	}

=back

=cut

	return@events;
}
sub generateMir0x{
	my@list;
	for(@_){
		my%DT=%{$_};
		if(!$DT{'cmd'}||'TAG'eq$DT{'cmd'}){
			if('OPTION'eq$DT{'swt'}){
				push(@list,qq(<OPTION value="$DT{'value'}">$DT{'label'}</OPTION>));
			}elsif('OPTGROUP'eq$DT{'swt'}){
				push(@list,qq(<OPTGROUP label="$DT{'label'}">));
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				push(@list,qq(</OPTGROUP>));
			}
		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
			push(@list,qq(<!-- %PAGE-BREAK -->));
		}elsif('COPY'eq$DT{'cmd'}){
			if('BEGIN'eq$DT{'swt'}){
				push(@list,qq(<!-- %BEGIN_$DT{'type'} $DT{'value'} -->));
			}elsif('END'eq$DT{'swt'}){
				push(@list,qq(<!-- %SET_$DT{'type'}_$DT{'key'} $DT{'value'} -->));
			}elsif('SET'eq$DT{'swt'}){
				push(@list,qq(<!-- %END_$DT{'type'} -->));
			}
		}
		#next;
	}
	return wantarray?@list:join("\n",map{m/^<OPTION/?"\t$_":$_}@list);
}

#-------------------------------------------------
# ealis3qw[] Parser and Generator
#

=head2 ealis3qw[]������������ꥹ�Ȥβ��Ϥ�����

ealis3���Ѥ�����qw[]������������ꥹ�Ȥβ��Ϥ�������Ԥ���
URL���Ѥ��뤳�Ȥ��Ǥ��ʤ�ʸ���Ǥ���`*'�ȶ�������Ū���Ѥ����ꥹ�ȷ�����
ñ���ʬ��ǽ񤯤Ȥ��˳ڡ�
Perl�Υ����������黻��qw�˰�¸���Ƥ��뤬��¾�θ���Ǥ�split(/\s+/)�����OK���⡣

=cut

sub parseEalis3qw{
	my@icons=$#_?@_:shift=~/(\S+)\s+(\S[^\x0a\x0d]*)/go;
	my@events;
	my$isGroup=0;
	for(0..($#icons-1)/2){
		my$value=$icons[$_*2];
		my$label=$icons[$_*2+1];
		if('**'eq$value){
			$isGroup&& push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
			if($value){
				push(@events,{cmd=>'TAG',swt=>'OPTGROUP',label=>$label});
				$isGroup=1;
			}else{
				$isGroup=0;
			}
		}else{
			push(@events,{cmd=>'TAG',swt=>'OPTION',label=>,$label,value=>$value});
		}
		next;
	}
	
	$isGroup&& push(@events,{cmd=>'TAG',swt=>'/OPTGROUP'});
	return@events;
}
sub generateEalis3qw{
	my@list;
	my$max=1;
	my$isGroup=-1;
	for(@_){
		my%DT=%{$_};
		if(!$DT{'cmd'}||'TAG'eq$DT{'cmd'}){
			if('OPTION'eq$DT{'swt'}){
				$max=length$DT{'value'}if$max<length$DT{'value'};
				if(!$isGroup){push(@list,'**','');$isGroup=1;}#̵̾���롼��
				push(@list,$DT{'value'},$DT{'label'});
			}elsif('OPTGROUP'eq$DT{'swt'}){
				push(@list,'**',$DT{'label'});
				$isGroup=1;#���롼����
			}elsif('/OPTGROUP'eq$DT{'swt'}){
				$isGroup=0;#���롼�פϤǤ������
			}
#		}elsif('PAGE-BREAK'eq$DT{'cmd'}){
#			
#		}elsif('COPY'eq$DT{'cmd'}){
#			if('BEGIN'eq$DT{'swt'}){
#				
#			}elsif('END'eq$DT{'swt'}){
#				
#			}elsif('SET'eq$DT{'swt'}){
#				
#			}
		}
		#next;
	}
	return wantarray?@list:join('',
	map{sprintf("\t%-${max}s\t%s\n",$list[$_*2],$list[$_*2+1])}(0..($#list-1)/2));
}


#------------------------------------------------------------------------------#
# jcode.pl: Perl library for Japanese character code conversion
# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
# http://www.srekcah.org/jcode/
sub euc2sjis{
	my$s=$_[0];
	$s=~s<([\xa1-\xfe]{2}|\x8e[\xa1-\xdf]|\x8f[\xa1-\xfe]{2})>
	[
		my($c1,$c2)=unpack('CC',$1);
		if($c1==0x8e){#SS2
			substr($1,1,1);
		}elsif($c1==0x8f){#SS3
			"\x81\xac";
		}elsif($c1 % 2){
			pack('CC',($c1>>1)+($c1<0xdf?0x31:0x71),$c2-0x60-($c2<0xe0));
		}else{
			pack('CC',($c1>>1)+($c1<0xdf?0x30:0x70),$c2-2);
		}
	]ego;
	return$s;
}



#-------------------------------------------------
# �������
#
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=$ENV{'REQUEST_METHOD'}?sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/o){return}
			print"Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/plain; charset=euc-jp"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Icon))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(icon icls style));
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://airemix.com/  #+";
			exit;
		}:sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/o){return}
			print@_?"ERROR: $_[0]":'ERROR';
			exit;
		};
	}
	# Revision Number
	$CF{'iconCatalog'}=qq$Revision$;
	$CF{'Exte'}.=qq(icon:\t$CF{'iconCatalog'}\n);
}

1;
__END__

=head1 BUGS

��ǧ���Ƥ���Х������ä���Ȥä���ľ���Ƥ��ޤ�

=head1 RESTRICTIONS

¸�ߤ��ޤ���
�����줢�ä��Ȥ���Ф���ϥХ��Ǥ�

=head1 NOTES

=over 4


=item Comments

����Υ����ȤϻȤ�����������᥽�åɤ��������ȸ������⡢
��¤����ݤλؿˤΤ���ˤĤ����Ƥ��ޤ���
�⤷���ʤ��δĶ���B<UNIX>��B<Perl>�����äƤ���Τʤ顢
S<pod2text iconctlg.cgi>
�ޤ���B<Windows>��B<Perl>��B<Jcode.pm>�����äƤ���Τʤ顢
S<perl -e"use Jcode;print Jcode::convert(scalar`pod2text iconctlg.cgi`,'sjis','euc')">
�⤷���ϡ�B<Perl>��B<nkf32.exe>�����äƤ���Τʤ顢
S<pod2text iconctlg.cgi|nkf32 -sE>
�ʤɤȤ����Windows�Ǥ�ʸ���������뤳�Ȥʤ�POD�ɥ�����Ȥ��ɤᡢ
����CGI��������¤���ݤ狼��á��Υϥ��ʣ�

=item Commands of MireilleIconlist

I<%PAGE-BREAK>̿��ϼ¸�Ū�ʼ����Ǥ���
�����ǤޤǤ˳μ¤ˡ������̤�̿��˼�ä�������Ȼפ��ޤ�

��Ȥ��I<PAGE-BREAK>�ϡ�
CSS��I<page-break-after>��ռ����ƤĤ����ΤǤ�����
����Ǥ��������ڡ����Ȥ������Ϥ��뤳�Ȥˤʤ�ޤ�
���������ڡ������Ȥ˰ۤʤ�ڡ���̾��Ĥ��褦�Ȼפ��ȡ�
���Υڡ���̾����ꤹ�뤿��Υ�����ɤȤ��ơ�
I<PAGE-BREAK>��Ȥ��Τϰ��´�������ޤ���
�ष��I<PAGE-START>�Ȥ��ǤϤʤ������ȡ�
���Τ褦����ͳ��I<PAGE-BREAK>̿��ϼ¸�Ū�ʤ�ΤȤ��Ƥ��ޤ���

��äȤ���̿��̾���פ��Ĥ����餽������Ѥ���ͽ��Ǥ���

=back

=head1 COPYRIGHT

��ʬ��B<Mireille>�ΰ����Ȥ������ۤ���B<MireilleLicense>�˽示���ΤȤ��ޤ���
����Ū�˽���BSD�饤���󥹤�GPL�Τ褦�ʡ�
������Ū�ʥ饤���󥹤�Ƴ�����뤳�Ȥ�Ƥ���Ƥ��ޤ���

B<ealis3qw>�����Ͽ�ǵ����ˤ��B<ealis>���Ѥ���������Ǥ�
http://kano.feena.jp/erial/

=head1 AVAILABILITY

B<Airemix> http://airemix.com/

=head1 SEE ALSO

B<Mireille>�Υإ�פ⸫�Ƥ�������

=head1 AUTHOR

NARUSE, Yui naruse@airemix.com

=head1 HISTORY

$Log$
Revision 1.5  2003/06/04 15:23:18  naruse
ɽ����ʬ�Υ���������ľ����

Revision 1.4  2003/03/11 15:57:29  naruse
�٤����Х�����

Revision 1.3  2003/01/24 05:16:39  naruse
�Х�����������Ū��Ĵ��

Revision 1.2  2002/10/21 07:13:52  naruse
ealis3�Υ�������ꥹ�Ȥ��������뵡ǽ���ɲ�
Mireille�Υ�������ꥹ�Ȥ���Ϥ���ؿ���ʬΥ
���Τۤ�Ĵ��

Revision 1.1  2002/09/27 08:19:40  naruse
Initial revision


=cut
