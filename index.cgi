#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw{%CF %IC};

#-------------------------------------------------
# ��ư���������˳�ǧ���뤳��

#�����Ȥ�̾��
$CF{'name'} = 'Airemix';
#�����ȥȥåץڡ�����URL
$CF{'home'} = 'http://airemix.site.ne.jp/';
#���ηǼ��ĤΥ����ȥ�
$CF{'title'} = ': Mireille  :';
#GZIP��PATH
$CF{'gzip'} = '/usr/bin/gzip';
#��������Υǥ��쥯�ȥ��URL
$CF{'icon'} = '/icon/full/';
#�������륷����
$CF{'style'} = 'style.css';

#-------------------------------------------------
# ɬ�פ˱������ѹ�

#�ޥ������ѥ���ɡ����Ƥε������Խ�������Ǥ��ޤ� 25ʸ���ʾ�侩��
$CF{'maspas'} = '';
#���Ѥ���Ĥ��륿����Ⱦ�ѥ��ڡ������ڤ��
$CF{'tags'} = 'DEL EM SMALL STRONG RUBY RB RB RT RP';
#�����ð���ε�����New�ޡ�����Ĥ���
$CF{'newnc'} = '86400';
#�ɤ�������Ǥ�����ô֤ϡ�̤�ɡ׾��֤�ݻ���������������class="new"��Ĥ����
$CF{'newuc'} = '600';
#���������ε����ˤĤ���ޡ����ʡ����ð���ε�����New�ޡ�����Ĥ����
$CF{'new'} = '<span class="new">New!</span>';
#�̾�⡼�ɤ�1�ڡ���������Υ���åɿ�
$CF{'page'} = '5';
#����������⡼�ɤǤ�1�ڡ���������Υ���åɿ�
$CF{'delpg'} = '10';
#���祹��åɿ�
$CF{'logmax'} = '100';
#�Ƶ����ι���(+color +email +home +icon +ra +hua cmd +subject)
$CF{'prtitm'} = '+color +email +home +icon +ra +hua cmd +subject';
#�ҵ����ι���(+color +email +home +icon +ra +hua cmd)
$CF{'chditm'} = '+color +email +home +icon +ra +hua cmd';
#Cookie�ι���(color email home icon)
$CF{'cokitm'} = 'color email home icon';
#��������åɤκ����ˡ
$CF{'del'} = 'rename';
#�������¤ӽ�
$CF{'sort'} = 'date';
#����/�ֿ� �����ä��Ȥ��˻��ꥢ�ɥ쥹�˥᡼�뤹��
$CF{'mailnotify'} = '0';
#������ƥե������Index��ɽ��
$CF{'prtres'} = '';
#���ѥ�������ǽON(1),OFF(0)
$CF{'exicon'}='0';
#���ѥ����������
#$IC{'PASSWORD'}='FILENAME'; #NAME
#"icon=moe" -> moe.png

#-------------------------------------------------
# �ѹ����ʤ��ۤ�������

#�����ॾ����
$ENV{'TZ'}  = 'JST-9';
#�����ƥ�ե�����
$CF{'index'}= 'index.cgi'; #MIREILLE MAIN CGI
$CF{'help'} = 'help.html'; #HELP FILE
$CF{'log'}  = './log/'; #LOG PATH


#-------------------------------------------------
# ����¾

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

if($0=~m{index.cgi$}o){
  #ľ�ܼ¹Ԥ��ä���ư���Ф�
  require './style.pl';
  require './core.cgi';
}

#-------------------------------------------------
# �������
BEGIN{
  # Revision Number
  $CF{'idxrev'}=qq$Revision$;
  #���顼���Ф��饨�顼���̤�ɽ������褦��
  if($0=~m{index.cgi$}o){
    $SIG{'__DIE__'}=sub{
    print<<"_HTML_";
Content-Language: ja
Content-type: text/plain; charset=euc-jp

<pre>
: Mireille :
Mireille Error Screen...

ERROR: $_[0]
Index : $CF{'idxrev'}
Style : $CF{'styrev'}
Core  : $CF{'correv'}

PerlVer  : $]
PerlPath : $^X
BaseTime : $^T
OS Name  : $^O
FileName : $0

ENV
CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}
QUERY_STRING: $ENV{'QUERY_STRING'}
REQUEST_METHOD: $ENV{'REQUEST_METHOD'}

SERVER_NAME: $ENV{'SERVER_NAME'}
HTTP: $ENV{'HTTP_HOST'} $ENV{'SCRIPT_NAME'}
OS: $ENV{'OS'}
PROCESSOR_IDENTIFIER: $ENV{'PROCESSOR_IDENTIFIER'}
SERVER_SOFTWARE: $ENV{'SERVER_SOFTWARE'}

Airemix Mireille
http://airemix.site.ne.jp/
_HTML_
    exit;
    };
  }
}
1;
__END__
