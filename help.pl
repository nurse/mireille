#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Help File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IN %CK);

$CF{'Help'}=qq$Revision$;
&header(skyline=>'none');

print<<'_HTML_';
<h2 class="mode">[ HELP &#38; TIPS ]</h2>

<div class="hthread" style="text-align:left">
<h2 class="ul">��Mireille�λȤ���</h2>
<ul style="margin-top:0px">
 <li><h3 class="ul">�񤭹���Ȥ�</h3>
  <ul class="list">
   <li>��ʸ<br>
    ������ʸ�����Ȥ��Ѵ�����ơ����Ƥ��Τޤ�ɽ������ޤ���<br>
    URL�ˤĤ��Ƥ�õ���ơ���ưŪ�˥�󥯤��Ƥ���ޤ��Τǡ����Ҥ����Ѥ���������<br>
    ���ʤߤ�Ⱦ�ѥ������ʤ⤿�֤�Ȥ��ޤ�</li>
   <li>EX���ޥ��<br>
    ���ߤ����ѥ�������Υѥ���ɤ������Τ˻ȤäƤ��ޤ���<br>
    ������&#34;icon=password&#34;�ȤʤäƤ��ޤ���<br>
    ���ѥ��������ߤ������ϡ������ͤ���˸�Ĥ��Ƥߤޤ��礦��</li>
  </ul>
 </li>
 <li><h3 class="ul">���ߤ��������</h3>
  <ul class="list">
_HTML_

    my@info=(
 'tags'  =>'���Ѥ���Ĥ��륿��'
,'newnc' =>'��Ƹ�*****�ð���ε�����New�ޡ�����Ĥ���'
,'newuc' =>'�ɤ�������Ǥ�???�ô֤ϡ�̤�ɡ׾��֤�ݻ�����'
,'page'  =>'�̾�⡼�ɤǤ�1�ڡ���������Υ���åɿ�'
,'delpg' =>'����������⡼�ɤǤ�1�ڡ���������Υ���åɿ�'
,'logmax'=>'���祹��åɿ�'
,'colway'=>'����������ˡ'
,'sort'  =>'�������¤ӽ�'
);

#    my($key=>$val)=('','');
    #��ư���������˳�ǧ���뤳��
    while(my($key=>$val)=(shift@info,shift@info)){
      $key||last;
      print qq(    <li><span style="width:350px">$val��</span>$CF{$key}</li>);
    }

print<<'_HTML_';
  </ul>
 </li>
 <li><h3 class="ul">���Τۤ�</h3>
  <ul class="list">
   <li>��ĤΥ���åɤλȤ��ޤ路��侩���ޤ�<br>
    ���ηǼ��Ĥϰ�İ�ĤΥ���åɤ�������Ĺ���ޤǿ��Ӥ롦����<br>
    �Ȥ��ä��Ȥ��������ꤷ�ƺ���Ƥ��ޤ���<br>
    3�Ԥ�ʸ�Ϥ����Υ���åɤ��������󡦡���<br>
    �Ȥ����Ȥ������򤱤��ۤ����������⤷��ޤ���</li>
   <li>��������κ����<br>
    �������̵�¤Ǥ���<br>
    ������������䤷�Ƥ⤢�ޤ����®�٤�����ʤ��褦�ˤ��Ƥ���Τ�����פ��ȡ�<br>
    ��������700�ĤΥ�������ǻ�ƤߤƤ���ä�ɽ������뤳�Ȥ��ǧ���ޤ�����
    �ºݤ�HTTP����٤�����ˤʤ�Τ��񤷤��Ȥϻפ��ޤ���^^;;</li>
   <li>�ʤˤ�������<br>
    ���ηǼ��ĤǤ��������Ȥ������ˤʤ�Ȥ����������ɲä����ߤ�����ǽ������С�<br>
    Airemix <a href="http://airemix.site.ne.jp/" title="Airemix">http://airemix.site.ne.jp/</a>
    �ηǼ��Ĥ˽񤭹��फ��<br>
    �᡼��(<a href="mailto:naruse@airemix.site.ne.jp">naruse@airemix.site.ne.jp</a>)�򤯤�����<br>
    �����ڤˤ��Ʋ����äƷ빽�Ǥ��ΤǢ�</li>
  </ul>
 </li>
</ul>
</div>

<div class="hthread" style="text-align:left">
<h2 class="ul">��������������</h2>
<ul style="margin-top:0px">
 <li>Mireille�ˤϥ�������������夵���뤿��Ρ֥������������פ����ꤷ�Ƥ��ޤ���<br>
 �����Widnows�Ǥ����֥��硼�ȥ��åȥ����פΤ褦�ʤ�ΤǤ�<br>
 �Ф���ʤ���Ф����ʤ����ǤϤ���ޤ��󤬡��Ȥ�����������⤷��ޤ���</li>
 <li><h3 class="ul">Index���̤ΤȤ�</h3>
  <ul class="list">
   <li>Alt+[1-9]<br>
   ���Υڡ�����ξ夫��[1-9]���ܤε����Ρ��ֿ��ؤΥ�󥯤����򤵤�ޤ�</li>
   <li>Alt+Shift+[1-9]<br>
   [1-9]�ڡ����ܤؤΥ�󥯤˰�ư���ޤ�</li>
   <li>Alt+[,.]<br>
   &#34;,&#34;���ȸ�Υڡ����ˡ�&#34;.&#34;���ȸŤ��ڡ����ذ�ư���ޤ�<br>
   JIS�����ܡ��ɤ�ȤäƤ������Ǥ����餳�Υ�������ΰ�̣���狼�뤫�⤷��ޤ���</li>
  </ul>
 </li>
 <li><h3 class="ul">��Ʋ��̤ΤȤ�</h3>
  <ul class="list">
   <li>Alt+J<br>����̾�ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+N<br>��̾���ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+I<br>�֥�������ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+L<br>��E-mail�ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+O<br>�֥ۡ���ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+B<br>����ʸ�ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+C<br>�ֿ��ץե�����˥������뤬�ܤ�ޤ�</li>
   <li>Alt+P<br>�֥ѥ���ɡץե�����˥������뤬�ܤ�ޤ�</li>

   <li>Alt+S<br>�ե���������Ƥ��������ޤ�</li>
  </ul>
 </li>
 <li><h3 class="ul">����¾�ΤȤ�</h3>
  <ul class="list">
   <li>Alt+S<br>����/�������ޤ�</li>
   <li>Alt+R<br>�ե���������Ƥ�ꥻ�åȤ��ޤ�</li>
  </ul>
 </li>
</ul>
</div>

<div class="hthread" style="text-align:left">
<h2 class="ul">�������äˤʤä��Ȥ���</h2>
<ul>
<li><h3 class="ul"><a href="http://www.tg.rim.or.jp/~hexane/ach/" title="Academic HTML">Academic HTML</a></h3>
HTML,CSS�˴ؤ���Ū�Τʾ��󤬤������󤢤�ޤ�<br>
HTML,CSS����̤�ؤӤ������Ϥ����򸫤�����ǻ�­��Ƥ��ޤ��ޤ�</li>
<li><h3 class="ul"><a href="http://openlab.ring.gr.jp/k16/htmllint/" title="Another HTML-lint">Another HTML-lint</a></h3>
HTML�θ��ڤ˺ݤ����Ѥ��ޤ���<br>
���ƥ����å�����ȡ��ۤȤ�ɤοͤ�����å�������뤳�ȤǤ��礦</li>
<li><h3 class="ul"><a href="http://www.artemis.ac/arrange/" title="ARTEMIS">ARTEMIS</a></h3>
IconPreview�Ϥ�������Ǥ��������ʤΤ�ĺ���ޤ�����<br>
��������Ƥ�����ȶ����Ƥ������⤳���Τ򸫤ơ��Ǥ�<br>
¾�ˤ⤤����Ȼ��ͤˤ��Ƥ��ޤ�<br>
������ǽ�Ǥ����򸫽������Ͽ�¿������ޤ�</li>
<li><h3 class="ul"><a href="http://kano.vis.ne.jp/erial/" title="elialarts.">erialarts.</a></h3>
LastPost�Ϥ�����ealis�ο����Ǥ�<br>
1.2.2�ε����ʥӤϿ�ǵ����Τ�Υ١����˺��ޤ���<br>
DHTML����ǤϤ��ʤ��ޤ���^^;;<br>
table��Ȥ鷺��ɽ�������褦�Ȥ��Ƥ���Τ�º�ɤ��ޤ�</li>
<li><h3 class="ul"><a href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru" title="HTMLȷ�ݶ����">HTMLȷ�ݶ����</a></h3>
�ĥå��ߥᥤ���HTML���⥵���ȡ��ˤ錄���ϸ����ޤ���<br>
��HTML 4.01 �Τߤ򡢽��˳���Ū�ʶ�̣���鸦��פ��Ƥ��뤽���Ǥ�<br>
HTML�ι����˺ݤ��ƻ��ͤˤ��ޤ���</li>
<li><h3 class="ul"><a href="http://www.srekcah.org/jcode/" title="jcode.pl">jcode.pl</a></h3>
�����������Ѵ��ѤΥ饤�֥��Ǥ�<br>
Mireille���ΤǤϲ��夷�Ƥ���ΤǻȤäƤ��ޤ���<br>
����CGI�Ǥϰ������ڤ�Ф��ƻȤäƤ��ޤ�</li>
<li><h3 class="ul"><a href="http://openlab.ring.gr.jp/Jcode/index-j.html" title="Jcode.pm">Jcode.pm</a></h3>
jcode.pl�θ�Ѥ�Perl5��PerlModule�ȤʤäƤ��ޤ�<br>
jcode.pl�ε�ǽ��Unicode�򰷤���ǽ���ɲä���Ƥ��ޤ�</li>
<li><h3 class="ul"><a href="http://www.kent-web.com/" title="KNET-WEB">KENT-WEB</a></h3>
�ʤˤϤȤ⤢�����ܤ�CGI/Perl����Ϳ�����ƶ��Ͼ��ʤ��Ϥʤ��Ϥ��Ǥ�<br>
��ĿͤǤ��ä�YYBOARD,YYCHAT�ˤϤ����äˤʤ�ޤ���<br>
�����ƤȤäĤ��פ�CGI��¿���Ǥ�</li>
<li><h3 class="ul"><a href="http://www.din.or.jp/~ohzaki/perl.htm" title="Perl���">Perl���</a></h3>
URI��ư��󥯵�ǽ��Ĥ���˺ݤ����ͤˡ������ष��ݼ̤��Ǥ�<br>
Perl������ɽ���˴ؤ��ƤȤƤ�ͭ�Ѥʾ��󤬤���ޤ�</li>
<li><h3 class="ul"><a href="http://validator.w3.org/" title="W3C HTML Validation Service">W3C HTML Validation Service</a></h3>
HTML���ʤκ����Ԥ����Ρ�W3C�ˤ��HTML���ڥ����ӥ��Ǥ�<br>
Another HTML-lint�������å����ܤϾ��ʤ�Ǥ�</li>
<li><h3 class="ul"><a href="http://wakusei.cplaza.ne.jp/twn/www.htm" title="�Ȥۤۤ�WWW����">�Ȥۤۤ�WWW����</a></h3>
HTML����Perl���Ȥ�˻�����ե��������ˤ��ޤ���<br>
�ʤ��ʤ��ܤäƤ��������Ǥ�<br>
����Ǥ������ά����Ƥ���Τ���ǰ�Ǥ�������</li>
<li><h3 class="ul"><a href="http://snowish.cside8.com/" title="Snowish Hills">Snowish Hills</a></h3>
Mireille���ꤳ��ˤ����äơ�ͭ�Ѥʥ��ɥХ�����¿��ĺ���ޤ���<br>
�ä˴�����ǽ����̾����˸����ʤ���Ф��ʤ��ϼ�ʤ�ΤˤʤäƤ����Ǥ��礦<br>
������֤Υǥ��������̾����Υǥ������١����ˤ��Ƥ��ޤ�<br>
���ʤߤˡ���̾����Υ����ȼ��Τ�Key��CG�����ȤǤ�</li>
<li>¾�ˤ�ո��򲼤��ä����������ͤˤ��������ȡ�CGI�κ�Ԥ���˴��դ��ޤ�</li>
</ul>
</div>

<pre style="margin:1em auto;text-align:center;width:600px">
���ηǼ��Ĥϡ�Microsoft Internet Explorer 5�ʾ���Ȥ����оݤȤ���
Microsoft Internet Explorer 6�ˤ����ƴ�����ư��򤷤ޤ���
Netscape 6�ڤ�Mozilla 0.8�ʹߤǤ�ܴۤ����̤��ư��򤹤뤳�Ȥ��ǧ�ѤߤǤ���
�ʾ�Υ֥饦���ʳ��Ǥ�ư��Ϥ��ޤ��������줷���ʤäƤ��ޤ��ޤ�����λ������������</pre>
_HTML_
print<<"_HTML_";
<div class="note" style="width:15em;">
<pre>
�������С��������󡡢�
��Index: $CF{'Index'}
��Core: $CF{'Core'}
��Style: $CF{'Style'}
��Help : $CF{'Help'}
</pre>
</div>
_HTML_
&footer;

1;
__END__
