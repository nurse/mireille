#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
require 5.004;
use strict;
use vars qw(%CF %IC);
$|=1;

#-------------------------------------------------
# ��ư���������˳�ǧ���뤳��

#�����Ȥ�̾��
$CF{'name'}='Airemix';
#�����ȥȥåץڡ�����URL
$CF{'home'}='/';
#���ηǼ��ĤΥ����ȥ��TITLE���ǡ�
$CF{'title'}=': Mireille :';
#���ηǼ��ĤΥ����ȥ�ʥڡ����Υإå�����ɽ����
$CF{'pgtitle'}='Airemix Mireille Board System';
#��������ꥹ��
$CF{'icls'}='icon.txt';
#�������륷����
$CF{'style'}='style.css';
#��������Υǥ��쥯�ȥ�
$CF{'icon'}='/icon/full/';
#�������󥫥���CGI
$CF{'icct'}='iconctlg.cgi';
#�إ�ץե�����
$CF{'help'}='help.pl';
#�����ʥ�JavaScript
$CF{'navjs'}='artnavi.js';
#���ǥ��쥯�ȥ�
$CF{'log'}='./log/';
#gzip�ξ��
$CF{'gzip'}='gzip';
#�����ॾ����ʡ�JST-9�פΤ褦�ˡ�
$ENV{'TZ'}='JST-9';

#-------------------------------------------------
# ɬ�פ˱������ѹ�

#�����ԥѥ���ɡ����Ƥε������Խ�������Ǥ��ޤ� 25ʸ���ʾ�侩��
$CF{'admps'}='';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'}='ACRONYM CODE DEL DFN EM Q SMALL STRONG RUBY RB RB RT RP';
#��Ĵ���뵭����б�����CSS�Υ��饹��Ⱦ�ѥ��ڡ������ڤ�ǡֵ��� ���饹 ���桦�����ס�
$CF{'strong'}=' // s2f2f /(/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)/ s2f2f # s2f2f �� s2f2f /(\s+(?:\/\/|#|��).*)/ s2f2f /^((?:>|&#62;|&gt;|&#x3E;).*)/ s8184 �� s8184 �� s819e �� s819e �� s81a0 �� s81a0 �� s81a6';
#��Ƹ�*****�ð���ε�����New�ޡ�����Ĥ���
$CF{'newnc'}='86400';
#�ɤ�������Ǥ�???�ô֤ϡ�̤�ɡ׾��֤�ݻ�����
$CF{'newuc'}='600';
#��Ƹ�*****�ð���ε����ˤĤ���New�ޡ���
$CF{'new'}='<SPAN class="new">New!</SPAN>';
#�̾�⡼�ɤǤ�1�ڡ���������Υ���åɿ�
$CF{'page'}='5';
#����������⡼�ɤǤ�1�ڡ���������Υ���åɿ�
$CF{'delpg'}='10';
#���祹��åɿ�
$CF{'logmax'}='100';
#�쥹��åɤ�����κ���ҵ����������¤���
$CF{'maxChilds'}='100';
#�����Ǥ�����ܡ�"���ܤ�name �������̾�� "�򤯤꤫������
$CF{'sekitm'}='ALL ���� name ̾�� email E-mail home �ۡ��� subject ��̾ body ��ʸ';
#�Ƶ����ι���(+color +email +home +icon +ra +hua cmd +subject)
$CF{'prtitm'}='+color +email +home +icon +ra +hua cmd +subject';
#�ҵ����ι���(+color +email +home +icon +ra +hua cmd)
$CF{'chditm'}='+color +email +home +icon +ra +hua cmd';
#Cookie�ι���(color email home icon)
$CF{'cokitm'}='color email home icon';
#����ž���Τ����(Content-Encoding����ˡ)
$CF{'conenc'}='|gzip -cfq9';
#Cookie����Ͽ����PATH(path=/ �Ȥ��ä�����)
$CF{'ckpath'}='';
#����������ˡ (input INPUT���� select SELECT����)
$CF{'colway'}='select';
#�Ť���������åɤκ����ˡ (gzip GZIP���� rename �ե�����̾�ѹ� unlink �ե�������)
$CF{'delold'}='gzip';
#��������åɤκ����ˡ (gzip GZIP���� rename �ե�����̾�ѹ� unlink �ե�������)
$CF{'delthr'}='gzip';
#�������¤ӽ� (number ����å��ֹ�� date ���������)
$CF{'sort'}='date';
#������ƥե������Index��ɽ�� (0 ɽ�����ʤ� 1 ɽ������)
$CF{'prtwrt'}='0';
#����/�ֿ� �����ä��Ȥ��˻��ꥢ�ɥ쥹�˥᡼�뤹�� (0 �Ȥ�ʤ� 1 �Ȥ�)
$CF{'mailnotify'}='0';
#�Ǽ��Ĥ�������Ѥˤ��� (0 �ɤ߽�OK 1 ��������)
$CF{'readOnly'}='0';
#�������ʤ��Ȥ��ˡ�304 Not Modified�פ��Ϥ����ݤ�
$CF{'use304'}='0';
#��ˡ�Last-Modified�פ��Ϥ����ݤ�
$CF{'useLastModified'}='0';
#���ѥ�������ǽ (ON 1 OFF 0)
$CF{'exicon'}='0';
#���ѥ����������
#$IC{'PASSWORD'}='FILENAME'; #NAME
#$IC{'hae'}='mae.png'; #��
#$IC{'hie'}='mie.png'; #��
#$IC{'hue'}='mue.png'; #�
#$IC{'hee'}='mee.png'; #��
#$IC{'hoe'}='moe.png'; #ǵ��
#�㡧���ޥ�ɤ�"icon=hoe"��������ǵ���������Ѥ�'moe.png'���Ȥ��ޤ�
#�����Ϥ���Ȥ��ϡ�$IC{'hoe'}='moe.png'; #ǵ���פΤ褦�ˡ��ǽ�Ρ�#�פ���Τ�˺�줺��

#-------------------------------------------------
# Mireille���HTML�ǥ�����

#-----------------------------
# ���ꥹ��
$CF{'colorList'}=<<'_CONFIG_';
<OPTION value="#FBDADE" style="color:#FBDADE">������</OPTION>
<OPTION value="#D53E62" style="color:#D53E62">���鯿�</OPTION>
<OPTION value="#FF7F8F" style="color:#FF7F8F">�����꿧</OPTION>
<OPTION value="#AD3140" style="color:#AD3140">���û鿧</OPTION>
<OPTION value="#9E2236" style="color:#9E2236">������</OPTION>
<OPTION value="#905D54" style="color:#905D54">����Ʀ��</OPTION>
<OPTION value="#EF454A" style="color:#EF454A">���뿧</OPTION>
<OPTION value="#F1BB93" style="color:#F1BB93">��ȩ��</OPTION>
<OPTION value="#564539" style="color:#564539">�����㿧</OPTION>
<OPTION value="#6B3E08" style="color:#6B3E08">���쿧</OPTION>
<OPTION value="#AA7A40" style="color:#AA7A40">�����ῧ</OPTION>
<OPTION value="#F8A900" style="color:#F8A900">�����ῧ</OPTION>
<OPTION value="#EDAE00" style="color:#EDAE00">��ݵ�⿧</OPTION>
<OPTION value="#C8A65D" style="color:#C8A65D">�����ҿ�</OPTION>
<OPTION value="#C2BD3D" style="color:#C2BD3D">��󴿧</OPTION>
<OPTION value="#AAB300" style="color:#AAB300">������</OPTION>
<OPTION value="#97A61E" style="color:#97A61E">��˨����</OPTION>
<OPTION value="#6DA895" style="color:#6DA895">���ļ���</OPTION>
<OPTION value="#89BDDE" style="color:#89BDDE">������</OPTION>
<OPTION value="#007BC3" style="color:#007BC3">��Ϫ��</OPTION>
<OPTION value="#00519A" style="color:#00519A">��������</OPTION>
<OPTION value="#384D98" style="color:#384D98">�����Ŀ�</OPTION>
<OPTION value="#4347A2" style="color:#4347A2">���˹���</OPTION>
<OPTION value="#A294C8" style="color:#A294C8">��ƣ��</OPTION>
<OPTION value="#714C99" style="color:#714C99">������</OPTION>
<OPTION value="#744B98" style="color:#744B98">���Գ���</OPTION>
<OPTION value="#C573B2" style="color:#C573B2">���Գ���</OPTION>
<OPTION value="#EAE0D5" style="color:#EAE0D5">���ῧ</OPTION>
<OPTION value="#DED2BF" style="color:#DED2BF">���ݲ翧</OPTION>
<OPTION value="#343434" style="color:#343434">����</OPTION>
_CONFIG_
undef$CF{'colorList'}; #�Ȥꤢ�����ä��Ȥ�����
#�ä��Ƥ��뤳�Ȥ��ä˰�̣�Ϥʤ��Τǡ����ꥹ�Ȥ����ꤷ�����ͤϾ�ιԤ������Ƥ�������

#-----------------------------
# ��������ꥹ�ȤΥإå���
$CF{'iched'}=<<'_CONFIG_';

_CONFIG_

#-----------------------------
# ��������ꥹ�ȤΥեå���
$CF{'icfot'}=<<'_CONFIG_';

_CONFIG_

#-------------------------------------------------
# �¹� or �ɤ߹��ߡ�

if($CF{'program'}eq __FILE__){
	#ľ�ܼ¹Ԥ��ä���ư���Ф�
	require 'core.cgi';
	require 'style.pl';
	&main;
}

#-------------------------------------------------
# �������
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\n"
			."\n\n<PLAINTEXT>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
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
	$CF{'Index'}=qq$Revision$;
	getlogin||umask(0); #nobody���¤Ǻ�ä��ե������桼�����ä���褦��
}

1;
__END__
