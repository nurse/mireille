#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
require 5.005;
#use strict;
#use vars qw(%CF %IC);

#-------------------------------------------------
# ��ư���������˳�ǧ������

#�����Ȥ�̾��
$CF{'name'}='Airemix';
#�����ȥȥåץڡ�����URL
$CF{'home'}='/';
#���ηǼ��ĤΥ����ȥ��TITLE���ǡ�
$CF{'title'}=': Mireille :';
#���ηǼ��ĤΥ����ȥ�ʥڡ����Υإå�����ɽ����
$CF{'pgtitle'}='Airemix Mireille Board System';
#��������Υǥ��쥯�ȥ�
$CF{'icon'}='/icon/full/';
#��������ꥹ��
$CF{'icls'}='icon.txt';
#�������󥫥���CGI
$CF{'icct'}='iconctlg.cgi';
#�������륷����
$CF{'style'}='style.css';
#�����ʥ�JavaScript
$CF{'navjs'}='artnavi.js';
#�إ�ץե�����
$CF{'help'}='help.pl';
#���ǥ��쥯�ȥ�
$CF{'log'}='./log/';
#gzip�ξ��
$CF{'gzip'}='gzip';
#�����ॾ����ʡ�JST-9�פΤ褦�ˡ�
$ENV{'TZ'}='JST-9';

#-------------------------------------------------
# ɬ�פ˱������ѹ�������

#�����ԥѥ���ɡ����Ƥε������Խ�������Ǥ��ޤ� 25ʸ���ʾ�侩��
$CF{'admps'}='';
#�ü��̾�ꥹ�ȡʡ֥ѥ���� ɽ����̾ �ѥ���� ɽ����̾ �������ס�
$CF{'signatureSpecial'}='mir *MIREILLE* airemix *Airemix*';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'}='ACRONYM CODE DEL DFN EM Q SMALL STRONG RUBY RB RB RT RP SPAN';
#��Ĵ���뵭����б�����CSS�Υ��饹�ʡֵ��� ���饹 ���� ���饹 �������ס�
$CF{'strong'}=' // s2f2f /(/\*[^*]*\*+(?:[^/*][^*]*\*+)*/)/ s2f2f /((?:^|[\x09\x20]+)(?:\/\/|#|��).*)/ s2f2f /^((?:>|&#62;|&gt;|&#x3E;).*)/ s8184 �� s8184 �� s8198 �� s819e �� s819e �� s819e �� s81a0 �� s81a0 �� s81a6 = s8198 == s819e === s81a0';
#NG��ɡ�Ⱦ�ѥ��ڡ������ڤ��
$CF{'ngWords'}='';
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
#�쥹��åɤ�����κ���ɽ���ҵ����������¤���
$CF{'maxChildsShown'}='10';
#�����Ǥ�����ܡʡֹ��ܤ�name ɽ��̾ ���ܤ�name ɽ��̾ �������ס�
$CF{'sekitm'}='ALL ���� name ̾�� email E-mail home �ۡ��� subject ��̾ body ��ʸ';
#�Ƶ����ι���(+color +email +home +icon +ra +hua +cmd +subject)
$CF{'prtitm'}='+color +email +home +icon +ra +hua +cmd +subject';
#�ҵ����ι���(+color +email +home +icon +ra +hua +cmd)
$CF{'chditm'}='+color +email +home +icon +ra +hua +cmd';
#Cookie�ι���(color email home icon cmd)
$CF{'cokitm'}='color email home icon cmd';
#����ž��������(Content-Encoding����ˡ)
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
#�������ʤ��Ȥ��ˡ�304 Not Modified�פ��Ϥ����ݤ� (0 �Ϥ��ʤ� 1 �Ϥ�)
$CF{'use304'}='0';
#��ˡ�Last-Modified�פ��Ϥ����ݤ� (0 �Ϥ��ʤ� 1 �Ϥ�)
$CF{'useLastModified'}='0';
#��̾��ɽ�����뤫�ݤ� (0 ɽ�����ʤ� 1 ɽ������)
$CF{'signature'}='1';
#���л��ꥢ������ (0 �Ȥ�ʤ� 1 �Ȥ�)
$CF{'absoluteIcon'}='1';
#���л��ꥢ������ (0 �Ȥ�ʤ� 1 �Ȥ�)
$CF{'relativeIcon'}='1';
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
<OPTION value="#000000" style="color:#000000">��Black</OPTION>
<OPTION value="#696969" style="color:#696969">��DimGray</OPTION>
<OPTION value="#808080" style="color:#808080">��Gray</OPTION>
<OPTION value="#A9A9A9" style="color:#A9A9A9">��DarkGray</OPTION>
<OPTION value="#C0C0C0" style="color:#C0C0C0">��Silver</OPTION>
<OPTION value="#D3D3D3" style="color:#D3D3D3">��LightGrey</OPTION>
<OPTION value="#D8BFD8" style="color:#D8BFD8">��Thistle</OPTION>
<OPTION value="#DCDCDC" style="color:#DCDCDC">��Gainsboro</OPTION>
<OPTION value="#F5F5DC" style="color:#F5F5DC">��Beige</OPTION>
<OPTION value="#F5F5F5" style="color:#F5F5F5">��WhiteSmoke</OPTION>
<OPTION value="#E6E6FA" style="color:#E6E6FA">��Lavender</OPTION>
<OPTION value="#FAF0E6" style="color:#FAF0E6">��Linen</OPTION>
<OPTION value="#FDF5E6" style="color:#FDF5E6">��Oldlace</OPTION>
<OPTION value="#FFE4E1" style="color:#FFE4E1">��Mistyrose</OPTION>
<OPTION value="#F0FFF0" style="color:#F0FFF0">��Honeydew</OPTION>
<OPTION value="#FFF5EE" style="color:#FFF5EE">��Seashell</OPTION>
<OPTION value="#FFF0F5" style="color:#FFF0F5">��LavenderBlush</OPTION>
<OPTION value="#F0F8FF" style="color:#F0F8FF">��AliceBlue</OPTION>
<OPTION value="#F8F8FF" style="color:#F8F8FF">��GhostWhite</OPTION>
<OPTION value="#FFFAF0" style="color:#FFFAF0">��FloralWhite</OPTION>
<OPTION value="#F5FFFA" style="color:#F5FFFA">��Mintcream</OPTION>
<OPTION value="#FFFAFA" style="color:#FFFAFA">��Snow</OPTION>
<OPTION value="#FFFFE0" style="color:#FFFFE0">��LightYellow</OPTION>
<OPTION value="#E0FFFF" style="color:#E0FFFF">��LightCyan</OPTION>
<OPTION value="#FFFFF0" style="color:#FFFFF0">��Ivory</OPTION>
<OPTION value="#F0FFFF" style="color:#F0FFFF">��Azure</OPTION>
<OPTION value="#FFFFFF" style="color:#FFFFFF">��White</OPTION>
<OPTION value="#9370DB" style="color:#9370DB">��MediumPurple</OPTION>
<OPTION value="#6A5ACD" style="color:#6A5ACD">��SlateBlue</OPTION>
<OPTION value="#483D8B" style="color:#483D8B">��DarkSlateBlue</OPTION>
<OPTION value="#7B68EE" style="color:#7B68EE">��MediumSlateBlue</OPTION>
<OPTION value="#BA55D3" style="color:#BA55D3">��MediumOrchid</OPTION>
<OPTION value="#9932CC" style="color:#9932CC">��DarkOrchid</OPTION>
<OPTION value="#8A2BE2" style="color:#8A2BE2">��BlueViolet</OPTION>
<OPTION value="#9400D3" style="color:#9400D3">��DarkViolet</OPTION>
<OPTION value="#4B0082" style="color:#4B0082">��Indigo</OPTION>
<OPTION value="#000080" style="color:#000080">��Navy</OPTION>
<OPTION value="#00008B" style="color:#00008B">��DarkBlue</OPTION>
<OPTION value="#0000CD" style="color:#0000CD">��MediumBlue</OPTION>
<OPTION value="#0000FF" style="color:#0000FF">��Blue</OPTION>
<OPTION value="#191970" style="color:#191970">��MidnightBlue</OPTION>
<OPTION value="#00BFFF" style="color:#00BFFF">��DeepSkyBlue</OPTION>
<OPTION value="#00CED1" style="color:#00CED1">��DarkTurquoise</OPTION>
<OPTION value="#1E90FF" style="color:#1E90FF">��DodgerBlue</OPTION>
<OPTION value="#4169E1" style="color:#4169E1">��RoyalBlue</OPTION>
<OPTION value="#4682B4" style="color:#4682B4">��SteelBlue</OPTION>
<OPTION value="#6495ED" style="color:#6495ED">��CornflowerBlue</OPTION>
<OPTION value="#87CEFA" style="color:#87CEFA">��LightSkyblue</OPTION>
<OPTION value="#5F9EA0" style="color:#5F9EA0">��CadetBlue</OPTION>
<OPTION value="#87CEEB" style="color:#87CEEB">��SkyBlue</OPTION>
<OPTION value="#B0E0E6" style="color:#B0E0E6">��PowderBlue</OPTION>
<OPTION value="#ADD8E6" style="color:#ADD8E6">��LightBlue</OPTION>
<OPTION value="#708090" style="color:#708090">��SlateGray</OPTION>
<OPTION value="#778899" style="color:#778899">��LightSlateGray</OPTION>
<OPTION value="#B0C4DE" style="color:#B0C4DE">��LightSteelBlue</OPTION>
<OPTION value="#008080" style="color:#008080">��Teal</OPTION>
<OPTION value="#008B8B" style="color:#008B8B">��DarkCyan</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Aqua</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Cyan</OPTION>
<OPTION value="#2F4F4F" style="color:#2F4F4F">��DarkSlateGray</OPTION>
<OPTION value="#AFEEEE" style="color:#AFEEEE">��PaleTurquoise</OPTION>
<OPTION value="#7FFFD4" style="color:#7FFFD4">��Aquamarine</OPTION>
<OPTION value="#66CDAA" style="color:#66CDAA">��MediumAquamarine</OPTION>
<OPTION value="#3CB371" style="color:#3CB371">��MediumSeagreen</OPTION>
<OPTION value="#2E8B57" style="color:#2E8B57">��SeaGreen</OPTION>
<OPTION value="#48D1CC" style="color:#48D1CC">��MediumTurquoise</OPTION>
<OPTION value="#40E0D0" style="color:#40E0D0">��Turquoise</OPTION>
<OPTION value="#20B2AA" style="color:#20B2AA">��LightSeagreen</OPTION>
<OPTION value="#00FA9A" style="color:#00FA9A">��MediumSpringGreen</OPTION>
<OPTION value="#00FF7F" style="color:#00FF7F">��SpringGreen</OPTION>
<OPTION value="#006400" style="color:#006400">��DarkGreen</OPTION>
<OPTION value="#008000" style="color:#008000">��Green</OPTION>
<OPTION value="#00FF00" style="color:#00FF00">��Lime</OPTION>
<OPTION value="#32CD32" style="color:#32CD32">��LimeGreen</OPTION>
<OPTION value="#228B22" style="color:#228B22">��ForestGreen</OPTION>
<OPTION value="#90EE90" style="color:#90EE90">��LightGreen</OPTION>
<OPTION value="#98FB98" style="color:#98FB98">��PaleGreen</OPTION>
<OPTION value="#7CFC00" style="color:#7CFC00">��LawnGreen</OPTION>
<OPTION value="#7FFF00" style="color:#7FFF00">��Chartreuse</OPTION>
<OPTION value="#ADFF2F" style="color:#ADFF2F">��GreenYellow</OPTION>
<OPTION value="#9ACD32" style="color:#9ACD32">��YellowGreen</OPTION>
<OPTION value="#6B8E23" style="color:#6B8E23">��Olivedrab</OPTION>
<OPTION value="#556B2F" style="color:#556B2F">��DarkOlivegreen</OPTION>
<OPTION value="#8FBC8B" style="color:#8FBC8B">��DarkSeaGreen</OPTION>
<OPTION value="#808000" style="color:#808000">��Olive</OPTION>
<OPTION value="#FFFF00" style="color:#FFFF00">��Yellow</OPTION>
<OPTION value="#FAFAD2" style="color:#FAFAD2">��LightGoldenrodYellow</OPTION>
<OPTION value="#FAEBD7" style="color:#FAEBD7">��AntiqueWhite</OPTION>
<OPTION value="#FFF8DC" style="color:#FFF8DC">��Cornsilk</OPTION>
<OPTION value="#FFEFD5" style="color:#FFEFD5">��PapayaWhip</OPTION>
<OPTION value="#FFEBCD" style="color:#FFEBCD">��BlanchedAlmond</OPTION>
<OPTION value="#FFFACD" style="color:#FFFACD">��LemonChiffon</OPTION>
<OPTION value="#FFE4C4" style="color:#FFE4C4">��Bisque</OPTION>
<OPTION value="#FFDAB9" style="color:#FFDAB9">��PeachPuff</OPTION>
<OPTION value="#F5DEB3" style="color:#F5DEB3">��Wheat</OPTION>
<OPTION value="#FFE4B5" style="color:#FFE4B5">��Moccasin</OPTION>
<OPTION value="#FFDEAD" style="color:#FFDEAD">��NavajoWhite</OPTION>
<OPTION value="#EEE8AA" style="color:#EEE8AA">��PaleGoldenrod</OPTION>
<OPTION value="#D2B48C" style="color:#D2B48C">��Tan</OPTION>
<OPTION value="#DEB887" style="color:#DEB887">��Burlywood</OPTION>
<OPTION value="#E9967A" style="color:#E9967A">��DarkSalmon</OPTION>
<OPTION value="#FA8072" style="color:#FA8072">��Salmon</OPTION>
<OPTION value="#F0E68C" style="color:#F0E68C">��Khaki</OPTION>
<OPTION value="#FFA07A" style="color:#FFA07A">��LightSalmon</OPTION>
<OPTION value="#BDB76B" style="color:#BDB76B">��DarkKhaki</OPTION>
<OPTION value="#F4A460" style="color:#F4A460">��SandyBrown</OPTION>
<OPTION value="#FF7F50" style="color:#FF7F50">��Coral</OPTION>
<OPTION value="#FF6347" style="color:#FF6347">��Tomato</OPTION>
<OPTION value="#CD853F" style="color:#CD853F">��Peru</OPTION>
<OPTION value="#A0522D" style="color:#A0522D">��Sienna</OPTION>
<OPTION value="#D2691E" style="color:#D2691E">��Chocolate</OPTION>
<OPTION value="#8B4513" style="color:#8B4513">��SaddleBrown</OPTION>
<OPTION value="#DAA520" style="color:#DAA520">��Goldenrod</OPTION>
<OPTION value="#B8860B" style="color:#B8860B">��DarkGoldenrod</OPTION>
<OPTION value="#FFD700" style="color:#FFD700">��Gold</OPTION>
<OPTION value="#FFA500" style="color:#FFA500">��Orange</OPTION>
<OPTION value="#FF8C00" style="color:#FF8C00">��DarkOrange</OPTION>
<OPTION value="#FF4500" style="color:#FF4500">��OrangeRed</OPTION>
<OPTION value="#800000" style="color:#800000">��Maroon</OPTION>
<OPTION value="#8B0000" style="color:#8B0000">��DarkRed</OPTION>
<OPTION value="#FF0000" style="color:#FF0000">��Red</OPTION>
<OPTION value="#B22222" style="color:#B22222">��Firebrick</OPTION>
<OPTION value="#A52A2A" style="color:#A52A2A">��Brown</OPTION>
<OPTION value="#CD5C5C" style="color:#CD5C5C">��IndianRed</OPTION>
<OPTION value="#F08080" style="color:#F08080">��LightCoral</OPTION>
<OPTION value="#BC8F8F" style="color:#BC8F8F">��RosyBrown</OPTION>
<OPTION value="#FF1493" style="color:#FF1493">��DeepPink</OPTION>
<OPTION value="#C71585" style="color:#C71585">��MediumVioletRed</OPTION>
<OPTION value="#DC143C" style="color:#DC143C">��Crimson</OPTION>
<OPTION value="#FF69B4" style="color:#FF69B4">��HotPink</OPTION>
<OPTION value="#DA70D6" style="color:#DA70D6">��Orchid</OPTION>
<OPTION value="#DB7093" style="color:#DB7093">��PaleVioletred</OPTION>
<OPTION value="#FFB6C1" style="color:#FFB6C1">��LightPink</OPTION>
<OPTION value="#FFC0CB" style="color:#FFC0CB">��Pink</OPTION>
<OPTION value="#800080" style="color:#800080">��Purple</OPTION>
<OPTION value="#8B008B" style="color:#8B008B">��DarkMagenta</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Fuchsia</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Magenta</OPTION>
<OPTION value="#EE82EE" style="color:#EE82EE">��Violet</OPTION>
<OPTION value="#DDA0DD" style="color:#DDA0DD">��Plum</OPTION>
_CONFIG_

#-----------------------------
# HTML-BODY�Υإå����ʥڡ����Ǿ����ΥХʡ�����Ϥ����ˡ�
$CF{'bodyHead'}=<<'_CONFIG_';

_CONFIG_

#-----------------------------
# HTML-BODY�Υեå����ʥڡ����ǲ����ΥХʡ�����Ϥ����ˡ�
$CF{'bodyFoot'}=<<'_CONFIG_';

_CONFIG_

#-----------------------------
# �������󥫥����Υإå���
$CF{'iched'}=<<'_CONFIG_';

_CONFIG_

#-----------------------------
# �������󥫥����Υեå���
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
	# Mireille Error Screen 1.2.1
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			$_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/&&return;
			print"Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/plain; charset=euc-jp"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.2.1 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		};
	}
	$CF{'_HiraganaLetterA'}->{'Index'}='��';
	# Version
	$CF{'Index'}=q$Revision$;
	$CF{'Index'}=~/(\d+((?:\.\d+)*))/o;
	$CF{'IndexRevision'}=$1;
}

1;
__END__
