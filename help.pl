#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Help Module -
#
$CF{'Help'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use strict;
use vars qw(%CF %IN %CK);

$CF{'Exte'}.=qq(help:\t$CF{'Help'}\n);

&showHeader(skyline=>'');

print<<'_HTML_';
<H2 class="mode">[ HELP &#38; TIPS ]</H2>

<DIV class="hthread">
<H2 class="list">��Mireille�λȤ���</H2>
<UL>
	<LI><H3 class="list">���ѵ���</H3>
		�����Ԥˤ�äơ����ѼԤ��Ǽ��Ĥ���Ƥ�����������������¤��줿�ꡢ<BR>
		�Ǽ��Ĥ��̤��Ƽ��������Ŀ;�������Ѥ����ꤹ�뤳�Ȥ�����ޤ���<BR>
		������̵�ǤǹԤ����ǽ��������ޤ���<BR>
		����Ū�ˤϡ�<BR>
		<UL>
			<LI>�����Ԥˤ�뵭���κ�����ѹ�<BR>
				���ѼԤ���Ŭ�ڤ����Ƥε�������Ƥ�����硢�����Ԥ�Ƚ�Ǥˤ�äơ��������������ꡢ<BR>
				���������Ƥ��Խ����뤳�Ȥ�����ޤ���</LI>
			<LI>�����Ԥˤ����������<BR>
				�����ԤϷǼ��Ĥˤ������������ѼԤ�̵�Ǥ����Ѥ��뤳�Ȥ��Ǥ��ޤ���<BR>
				��������ʸ�����Ǥʤ������������פ䤽��¾Cookie�Τ褦�ʾ���⤳��˴ޤޤ�ޤ���<BR>
				���ѼԤ������Ϥ�Ȥ��������򤳤ξ��ԻȤǤ��ޤ���</LI>
			<LI>���ѼԤ��Ф�����Ƥ��줿�����ο������ݾ�������Ǥ����<BR>
				�����Ԥϵ��������Ƥο��������Ф�����Ǥ������ޤ���<BR>
				������ʡ���ȿ�������Ƥ���Ƥ��줿�������դ����б��򤹤뤳�Ȥ���«���ޤ���<BR>
				����¾���ηǼ��Ĥ����Ѥˤ�äƲ���»�����ФƤ�����Ԥ���Ǥ���餤�ޤ���</LI>
		</UL>
	</LI>
	<LI><H3 class="list">Mireille��ͭ�λ���</H3>
		<UL>
			<LI>�����κ��<BR>
				�ޤ�������Ͽ侩���ޤ��󡣽�����ǽ��Ȥ����Ȥ򤪴��ᤷ�ޤ���<BR>
				�Ƶ����������褦�Ȥ����硢<BR>
				���Ƶ���������¸�ߤ����ҵ������դ��Ƥ��ʤ���Τϥ���åɤ��Ⱥ������ޤ���<BR>
				���Ƶ��������Ǥʤ����ҵ��������Ǥ�Ĥ��Ƥ��������ʸ�������������ޤ���<BR>
				�������ԤΤߤ��ҵ������դ��Ƥ��륹��åɤ򡢥���åɤ��Ⱥ���Ǥ��ޤ���</LI>
			<LI>��ʸ<BR>
				URL��õ���ơ���ưŪ�˥�󥯤��Ƥ���ޤ��Τǡ����Ҥ����Ѥ���������<BR>
				���˼����Ƥ��붯Ĵ���椫��Ϥޤ�Ԥϡ��񤤤����˲��餫�η��Ǹ�礬��Ĵ����ޤ�<BR>
				����ʳ��ˤ��礬��Ĵ����뤳�Ȥ�����ޤ�
				���ʤߤ�Ⱦ�ѥ������ʤ⤿�֤�Ȥ��ޤ�</LI>
			<LI>���ޥ��<BR>
				���ߤ����ѥ�������Υѥ���ɤ������Τ˻ȤäƤ��ޤ���<BR>
				������&#34;icon=password&#34;�ȤʤäƤ��ޤ���<BR>
				���ѥ��������ߤ������ϡ������ͤ���˸�Ĥ��Ƥߤޤ��礦��</LI>
		</UL>
	</LI>
	<LI><H3 class="list">���ߤ��������</H3>
		<UL>
_HTML_
print<<"_HTML_";
			<LI>��Ƹ�<STRONG>$CF{'newnc'}</STRONG>�ð���ε�����New�ޡ�����Ĥ���</LI>
			<LI>�ɤ�������Ǥ�<STRONG>$CF{'newuc'}</STRONG>�ô֤ϡ�̤�ɡ׾��֤�ݻ�����</LI>
			<LI>�̾�⡼�ɤǤϡ�1�ڡ���������<STRONG>$CF{'page'}</STRONG>����å�ɽ�����ޤ�</LI>
			<LI>����������⡼�ɤǤϡ�1�ڡ���������<STRONG>$CF{'delpg'}</STRONG>����å�ɽ�����ޤ�</LI>
			<LI>��������Τ�����<STRONG>$CF{'logmax'}</STRONG>����åɤ���¸����Ƥ��ޤ�</LI>
			<LI>������@{[($CF{'tags'})?"<STRONG>$CF{'tags'}</STRONG>����ѤǤ��ޤ�":'���ڻ��ѤǤ��ޤ���']}</LI>
			<LI>����<STRONG>@{[('input'eq$CF{'colway'})?'INPUT':'SELECT']}����</STRONG>�����٤ޤ�</LI>
			<LI>������<STRONG>@{[('date'eq$CF{'sort'})?'�������':'�����ֹ�']}</STRONG>���ɽ������ޤ�</LI>
_HTML_
#��綯Ĵ��Ϣ
{
	my%ST=($CF{'strong'}=~/(\S+)\s+(\S+)/go);
	my$line;my$regexp;
	for(keys%ST){
		if(m!^(/.+/)$!o){
			$regexp.=qq(<STRONG>$_</STRONG>,);
		}else{
			$line.=qq(<STRONG class="$ST{$_}">$_</STRONG>,);
		}
	}
	chop$line;chop$regexp;
	if($line&&$regexp){
		print"\t\t\t<LI>$line ����Ϥޤ�Ԥȡ�<BR>����ɽ�� $regexp �˥ޥå�����ʸ����϶�Ĵɽ������ޤ�</LI>\n";
	}elsif($line){
		print"\t\t\t<LI>$line ����Ϥޤ�Ԥ϶�Ĵɽ������ޤ�</LI>\n";
	}elsif($regexp){
		print"\t\t\t<LI>����ɽ�� $regexp �˥ޥå�����ʸ����϶�Ĵɽ������ޤ�</LI>\n";
	}else{
		print"\t\t\t<LI>ʸ����϶�Ĵɽ������ޤ���</LI>\n";
	}
}
#���������Ϣ
{
	&iptico;
	my$group=@{[$CK{'iconlist'}=~/<OPTGROUP.*/gio]};
	my$icons=@{[$CK{'iconlist'}=~/<OPTION.*/gio]};
	my($name,$link,%icon);
	for($CK{'iconlist'}=~/(<!-- %(?:[A-Z0-9]+_)?(?:VENDOR|COPY1)(?:_[A-Z0-9]+)?(?: (?:.*?))?\s*-->)/go){
		$_=~/<!-- %([A-Z0-9]+_)?(VENDOR|COPY1)(_[A-Z0-9]+)?(?: (.*?))?\s*-->/o;
=item
$1: 'BEGIN_','END_'
$2: 'VENDOR','COPY1'
$3: '_NAME','_URL','_LINK'
$4: data
=cut
		if('BEGIN_'eq$1){
			$name=$4;$link='';$icon{$4}=$4;next;
		}elsif('END_'eq$1){
			$name='';$link='';next;
		}elsif($4){
			if('_NAME'eq$3){
				$name=$4;
				$icon{$4}=$4;
			}elsif('_URL'eq$3){
				$icon{$name}=qq(<A href="$4" title="@{['VENDOR'eq$2?'�����':'�켡�����']}">$name</A>);
			}elsif('_LINK'eq$3){
				$icon{$name}=$4;
			}
		}
	}
	print"\t\t\t<LI>$group���롼�ס�$icons�ĤΥ����������Ѳ�ǽ�Ǥ�</LI>\n";
	delete$icon{''};
	(%icon)&&(print"\t\t\t<LI>".join("��\n",values%icon)."\n���������ͭ�����Ǻ����Ѥ��Ƥ��ޤ���</LI>\n");
}
#���å�����Ϣ
{
	my$ascii='[\x0A\x0D\x20-\x7E]'; # 1�Х��� EUC-JPʸ����-\x09
	my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2�Х��� EUC-JPʸ��
	my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3�Х��� EUC-JPʸ��
	my$cookie='';
	my$decoded='';
	for(split('; ',$ENV{'HTTP_COOKIE'})){
		my($i,$j)=split('=',$_,2);
		'Mireille'ne$i&&next;
		$cookie=$j;
		$j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
		$decoded=$j;
	}
	print<<"_HTML_";
			<LI>���å�����Ϣ<BR><FORM action="#" method="get">
			���ʤ��Υ��å�����<INPUT id="yourCookie" name="yourcookie" type="text"
			 size="100" value="$ENV{'HTTP_COOKIE'}" readonly><BR>
			Mireille�Ѥ����ơ�<INPUT id="mirCookie" name="mirCookie" type="text"
			 size="100" value="$decoded" readonly><BR>
			���å����񤭴�����<INPUT id="cookiedata" name="cookiedata" type="text"
			 size="100" value="$cookie"><BR>
				<INPUT type="submit" class="submit" value="OK"
				 onclick="reviseCookie(window.event)" onkeypress="reviseCookie(window.event)">
				<INPUT type="reset" class="reset" value="Reset"
				 onclick="resetCookie(window.event)" onkeypress="resetCookie(window.event)">
			<BR></FORM>
_HTML_
}
		print<<'_HTML_';
<SCRIPT type="text/JavaScript">
<!--
function reviseCookie(e){
	if(e.preventDefault){
		e.preventDefault();
		e.stopPropagation();
	}else if(document.all){
		e.cancelBubble=true;
		e.returnValue=false; 
	}
	var cookie=document.all('cookiedata').value;
	if(cookie){
		if(confirm('�ʲ��Τ褦��Mireille�Υ��å�����񤭴����ޤ���������Ǥ�����'
		 +"�ʻ��;����ܸ줬�����Ƥ��ޤ������ºݤ˽񤭹��ޤ�����Ƥ�����˽񤭹��ޤ�ޤ���\n"+unescape(cookie))){
			document.cookie='Mireille='+cookie+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//��������
			alert("���å��������ꤷ�ޤ���");
		}
	}else{
		if(confirm('Mireille�Υ��å����������ޤ���������Ǥ�����')){
			document.cookie='Mireille=; expires=Thu, 01-Jan-1970 00:00:00 GMT; ';//�Ϥޤ����
			alert("���å����������ޤ���");
		}
	}
	return false;
}
function resetCookie(e){
	if(e.preventDefault){
		e.preventDefault();
		e.stopPropagation();
	}else if(document.all){
		e.cancelBubble=true;
		e.returnValue=false; 
	}
	var date=new Date();
	document.all('cookiedata').value="expire%09"+parseInt(date.getTime()/1000);
	return false;
}
//-->
</SCRIPT>
			�֥��å����񤭴����פˤ�äơ�Mireille�ѤΥ��å�����񤭴����뤳�Ȥ��Ǥ��ޤ�<BR>
			�������褿�Ǽ��Ĥˡ����ޤǹԤäƤ���Ǽ��ĤΥ��å�����ܿ����롢�Ȥ������Ȥ⡢<BR>
			�ܿ����ˤʤ����ܤΥ��å����ϰܿ��Ǥ��ޤ��󤬡�����Ū�ˤϲ�ǽ�Ǥ�<BR>
			<BR>
			��Reset�פ򲡤��ȡ�̤�ɵ������Τ餻��ǽ���������Ǿ��¤Υ��å���������Ϳ�����ޤ�<BR>
			���å������ʤ����֤��顢��Reset�ס�OK�פǥ��å�������¸����ȡ�̤�ɵ������Τ餻��ǽ�ϸ����褦�ˤʤ�ޤ�</LI>
		</UL>
	</LI>
	<LI><H3 class="list">���Τۤ�</H3>
		<UL>
			<LI>��ĤΥ���åɤλȤ��ޤ路��侩���ޤ�<BR>
				���ηǼ��Ĥϰ�İ�ĤΥ���åɤ�������Ĺ���ޤǿ��Ӥ롦����<BR>
				�Ȥ��ä��Ȥ��������ꤷ�ƺ���Ƥ��ޤ���<BR>
				�Ƶ�����3�Ԥ�ʸ�Ϥ����쥹��̵�����ʥ���åɤ��������󡦡���<BR>
				�Ȥ����Ȥ������򤱤��ۤ����������⤷��ޤ���<BR>
				�ʥ���¸�������Թ�ǥ����С��إåɤ������뤫�⡣����</LI>
			<LI>��������κ����<BR>
				�������̵�¤Ǥ���<BR>
				������������䤷�Ƥ⤢�ޤ����®�٤�����ʤ��褦�ˤ��Ƥ���Τ�����פ��ȡ�<BR>
				��������������Υƥ��ȴĶ��Ǥ�700�ĤΥ�������ǻ�ƤߤƤ���ä�ɽ������뤳�Ȥ��ǧ���ޤ�����<BR>
				�ºݤ�HTTP����٤�����ˤʤꡢž���˻��֤�������Τ��񤷤��Ȥϻפ��ޤ���^^;;</LI>
			<LI>�ʤˤ�������<BR>
				���ηǼ��ĤǤ��������Ȥ������ˤʤ�Ȥ����������ɲä����ߤ�����ǽ������С�<BR>
				Airemix <A href="http://www.airemix.com/" title="Airemix" target="_top">http://www.airemix.com/</A>
				�ηǼ��Ĥ˽񤭹��फ��
				�᡼��(<A href="mailto:naruse&#64;airemix.com">naruse&#64;airemix.com</A>)�򤯤�����<BR>
				�����ڤˤ��Ʋ����äƷ빽�Ǥ��ΤǢ�<BR>
				<BR>
				���ʤߤ˥᡼���PGP�Ź沽�������ꤿ�����ϡ�pgp.nic.ad.jp�Τ褦�ʸ����������С��ǡ�<BR>
				"Airemix"�Ǹ�������������θ��������������ޤ��Τǡ������ȤäƤ�������<BR>
				���λ���ϡ�DB DB A4 76 FD BD 94 50 02 CD 0E FC BC E3 C3 88 47 2E C1 EA�פǤ�<BR>
				</LI>
		</UL>
	</LI>
</UL>
</DIV>

<DIV class="hthread">
<H2 class="list">��������������</H2>
<UL>
	<LI>Mireille�ˤϥ�������������夵���뤿��Ρ֥������������פ����ꤷ�Ƥ��ޤ���<BR>
		�����Windows�Ǥ����֥��硼�ȥ��åȥ����פΤ褦�ʤ�ΤǤ�<BR>
		�Ф��ʤ���Ф����ʤ����ǤϤ���ޤ��󤬡��Ȥ�����������⤷��ޤ���</LI>
	<LI><H3 class="list">Index���̤ΤȤ�</H3>
		<DL>
			<DT><KBD>Alt+[1-9]</KBD></DT>
			<DD>���Υڡ�����ξ夫��[1-9]���ܤε����Ρ��ֿ��ؤΥ�󥯤����򤵤�ޤ�</DD>
			<DT><KBD>Alt+Shift+[1-9]</KBD></DT>
			<DD>[1-9]�ڡ����ܤؤΥ�󥯤˰�ư���ޤ�</DD>
			<DT><KBD>Alt+[,.]</KBD></DT>
			<DD><KBD>,</KBD> ���ȸ�Υڡ����ˡ�<KBD>.</KBD> ���ȸŤ��ڡ����ذ�ư���ޤ�<BR>
			JIS�����ܡ��ɤ�ȤäƤ������Ǥ����餳�Υ�������ΰ�̣���狼�뤫�⤷��ޤ���</DD>
		</DL>
	</LI>
	<LI><H3 class="list">��Ʋ��̤ΤȤ�</H3>
		<DL>
			<DT><KBD>Alt+J</KBD></DT><DD>����̾�פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+N</KBD></DT><DD>��̾���פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+K</KBD></DT><DD>��Cookie�פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+I</KBD></DT><DD>�֥�������פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+L</KBD></DT><DD>��E-mail�פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+O</KBD></DT><DD>�֥ۡ���פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+B</KBD></DT><DD>����ʸ�פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+C</KBD></DT><DD>�ֿ��פ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+P</KBD></DT><DD>�֥ѥ���ɡפ˥������뤬�ܤ�ޤ�</DD>
			<DT><KBD>Alt+M</KBD></DT><DD>�֥��ޥ�ɡפ˥������뤬�ܤ�ޤ�</DD>
			
			<DT><KBD>Alt+S</KBD></DT><DD>�ե���������Ƥ��������ޤ�</DD>
		</DL>
	</LI>
	<LI><H3 class="list">����¾�ΤȤ�</H3>
		<DL>
			<DT><KBD>Alt+S</KBD></DT><DD>����/�������ޤ�</DD>
			<DT><KBD>Alt+R</KBD></DT><DD>�ե���������Ƥ�ꥻ�åȤ��ޤ�</DD>
		</DL>
	</LI>
</UL>
</DIV>

<DIV class="hthread" style="text-align:left">
<H2 class="list"><A name="�����äˤʤä��Ȥ���">�������äˤʤä��Ȥ���</A></H2>
<UL>
<LI><H3 class="list"><A href="http://www.tg.rim.or.jp/~hexane/ach/" title="Academic HTML">Academic HTML</A></H3>
HTML,CSS�˴ؤ���Ū�Τʾ��󤬤������󤢤�ޤ�<BR>
HTML,CSS����̤�ؤӤ������Ϥ����򸫤�����ǻ�­��Ƥ��ޤ��ޤ�</LI>
<LI><H3 class="list"><A href="http://openlab.ring.gr.jp/k16/htmllint/" title="Another HTML-lint">Another HTML-lint</A></H3>
HTML�θ��ڤ˺ݤ����Ѥ��ޤ���<BR>
���ƥ����å�����ȡ��ۤȤ�ɤοͤ�����å�������뤳�ȤǤ��礦</LI>
<LI><H3 class="list"><A href="http://www.artemis.ac/arrange/" title="ARTEMIS">ARTEMIS</A></H3>
IconPreview�Ϥ�������Ǥ��������ʤΤ�ĺ���ޤ�����<BR>
��������Ƥ�����ȶ����Ƥ������⤳���Τ򸫤ơ��Ǥ�<BR>
¾�ˤ⤤����Ȼ��ͤˤ��Ƥ��ޤ�<BR>
������ǽ�Ǥ����򸫽������Ͽ�¿������ޤ�</LI>
<LI><H3 class="list"><A href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru" title="HTMLȷ�ݶ����">HTMLȷ�ݶ����</A></H3>
�ĥå��ߥᥤ���HTML���⥵���ȡ��ˤ錄���ϸ����ޤ���<BR>
��HTML 4.01 �Τߤ򡢽��˳���Ū�ʶ�̣���鸦��פ��Ƥ��뤽���Ǥ�<BR>
HTML�ι����˺ݤ��ƻ��ͤˤ��ޤ���</LI>
<LI><H3 class="list"><A href="http://www.srekcah.org/jcode/" title="jcode.pl">jcode.pl</A></H3>
�����������Ѵ��ѤΥ饤�֥��Ǥ�<BR>
Mireille���ΤǤϲ��夷�Ƥ���ΤǻȤäƤ��ޤ���<BR>
����CGI�Ǥϰ������ڤ�Ф��ƻȤäƤ��ޤ�</LI>
<LI><H3 class="list"><A href="http://openlab.ring.gr.jp/Jcode/index-j.html" title="Jcode.pm">Jcode.pm</A></H3>
jcode.pl�θ�Ѥ�Perl5��PerlModule�ȤʤäƤ��ޤ�<BR>
jcode.pl�ε�ǽ��Unicode�򰷤���ǽ���ɲä���Ƥ��ޤ�<BR>
Perl5.8�Ǥ�Encode�⥸�塼����ִ�����Ƥ���褦�Ǥ�</LI>
<LI><H3 class="list"><A href="http://www.kent-web.com/" title="KNET-WEB">KENT-WEB</A></H3>
�ʤˤϤȤ⤢�����ܤ�CGI/Perl����Ϳ�����ƶ��Ͼ��ʤ��Ϥʤ��Ϥ��Ǥ�<BR>
��ĿͤǤ��ä�YYBOARD,YYCHAT�ˤϤ����äˤʤ�ޤ���<BR>
�����ƤȤäĤ��פ�CGI��¿���Ǥ�</LI>
<LI><H3 class="list"><A href="http://www.din.or.jp/~ohzaki/perl.htm" title="Perl���">Perl���</A></H3>
URI��ư��󥯵�ǽ��Ĥ���˺ݤ����ͤˡ������ष��ݼ̤��Ǥ�<BR>
Perl������ɽ���˴ؤ��ƤȤƤ�ͭ�Ѥʾ��󤬤���ޤ�</LI>
<LI><H3 class="list"><A href="http://validator.w3.org/" title="W3C HTML Validation Service">W3C HTML Validation Service</A></H3>
HTML���ʤκ����Ԥ����Ρ�W3C�ˤ��HTML���ڥ����ӥ��Ǥ�<BR>
Another HTML-lint�������å����ܤϾ��ʤ�Ǥ�</LI>
<LI><H3 class="list"><A href="http://tohoho.wakusei.ne.jp/" title="�Ȥۤۤ�WWW����">�Ȥۤۤ�WWW����</A></H3>
HTML����Perl���Ȥ�˻�����ե��������ˤ��ޤ���<BR>
�ʤ��ʤ��ܤäƤ��������Ǥ�</LI>
<LI><H3 class="list"><A href="http://kano.feena.jp/" title="����">����</A></H3>
LastPost�Ϥ�����ealis�ο����Ǥ�<BR>
�ޤ�1.2.2�ε����ʥӤϿ�ǵ����Τ�Υ١����˺��ޤ���<BR>
�Ƕ�Ǥ�PHP�˰ܤäƤ���٤��ѤȤ�����Τ��Ϻ����Ƥ���ä����褦�Ǥ�</LI>
<LI><H3 class="list"><A href="http://www10.plala.or.jp/ryokufuudou/kijindou.html" title="SWORD AND COMMERCE">SWORD AND COMMERCE</A></H3>
retro����ˤ�Mireille�ǤĤޤŤ���No.1�Ȼפ��륢����������β����񤤤Ƥ��������ޤ���<BR>
¾�ˤ�Mireille�β��������������¿�����Ƥ�餤�ޤ���<BR>
���ʤߤˡ�retro����Υ����ȼ��Τ�RagnarkOnline�ϻ��̥����ȤǤ�</LI>
<LI><H3 class="list"><A href="http://snowish.cside8.com/" title="Snowish Hills">Snowish Hills</A></H3>
Mireille���ꤳ��ˤ����äơ�Ⱦ�Х��󥵥��ȸܵҤȤ��ơ�������ͭ�Ѥʥ��ɥХ�����ĺ���ޤ���<BR>
�ä˴���CGI����̾����˸����ʤ���С����ʤ��ϼ�ʤ�ΤˤʤäƤ����Ǥ��礦<BR>
���ߤν�����֤Υǥ��������̾����Υǥ������١����ˤ��Ƥ��ޤ�<BR>
���ʤߤˡ���̾����Υ����ȼ��Τ�Key��CG�����ȤǤ�</LI>
<LI>¾�ˤ�ո��򲼤��ä����������ͤˤ��������ȡ�CGI�κ�Ԥ���˴��դ��ޤ�</LI>
</UL>
</DIV>

<P class="note">���������Ǥ�&trade;��&reg;��&copy;�ޡ����Ͼ�ά���Ƥ��ޤ�<BR>
���줾��Υ�����̾�䥽�եȥ�����̾�ʤɤϳơ��ξ�ɸ����Ͽ��ɸ�ʤɤǤ�</P>
<P align="center" class="note" style="margin-bottom:2em;width:600px">
���ηǼ��Ĥϡ�Microsoft Internet Explorer 5�ʾ���Ȥ����оݤȤ���<BR>
Microsoft Internet Explorer 6�ˤ����ƴ�����ư��򤷤ޤ���<BR>
Netscape 6�ڤ�Mozilla 0.8�ʹߤǤ�ܴۤ����̤��ư��򤹤뤳�Ȥ��ǧ�ѤߤǤ���<BR>
�ʾ�Υ֥饦���ʳ��Ǥ�ư��Ϥ��ޤ��������줷���ʤäƤ��ޤ��ޤ�����λ������������</P>
_HTML_
print<<"_HTML_".&getFooter;
<DIV align="center" class="note" style="width:15em;">
<H4 class="list" style="text-align:center">�����С��������󡡢�</H4>
<UL style="font-family:monospace;font-size:90%">
<LI>Index: $CF{'Index'}</LI>
<LI>Core : $CF{'Core' }</LI>
<LI>Style: $CF{'Style'}</LI>
<LI>Help : $CF{'Help' }</LI>
</UL>
</DIV>
_HTML_
exit;

1;
__END__
