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
<H2 class="heading2">[ HELP &#38; TIPS ]</H2>



<DIV class="section">
<H2 class="h">��Mireille�λȤ���</H2>


<DIV class="section">
<H3 class="h">���ѵ���</H3>
<P>�����Ԥˤ�äơ����ѼԤ��Ǽ��Ĥ���Ƥ�����������������¤��줿�ꡢ<BR>
�Ǽ��Ĥ��̤��Ƽ��������Ŀ;�������Ѥ����ꤹ�뤳�Ȥ�����ޤ���<BR>
������̵�ǤǹԤ����ǽ��������ޤ���</P>
<P>����Ū�ˤϰʲ����̤�ˤʤ�ޤ����ʤȤϸ��äƤ⤳��ʳ��Υ�������¸�ߤ����ޤ�����</P>
<DL class="section">
	<DT>�����Ԥˤ�뵭���κ�����ѹ�</DT>
	<DD>���ѼԤ���Ŭ�ڤ����Ƥε�������Ƥ�����硢�����Ԥ�Ƚ�Ǥˤ�äơ��������������ꡢ<BR>
		���������Ƥ��Խ����뤳�Ȥ�����ޤ���</DD>
	<DT>�����Ԥˤ����������</DT>
	<DD>�����ԤϷǼ��Ĥˤ������������ѼԤ�̵�Ǥ����Ѥ��뤳�Ȥ��Ǥ��ޤ���<BR>
		��������ʸ�����Ǥʤ������������פ䤽��¾Cookie�Τ褦�ʾ���⤳��˴ޤޤ�ޤ���<BR>
		���ѼԤ������Ϥ�Ȥ��������򤳤ξ��ԻȤǤ��ޤ���</DD>
	<DT>���ѼԤ��Ф�����Ƥ��줿�����ο������ݾ�������Ǥ����</DT>
	<DD>�����Ԥϵ��������Ƥο��������Ф�����Ǥ������ޤ���<BR>
		������ʡ���ȿ�������Ƥ���Ƥ��줿�������դ����б��򤹤뤳�Ȥ���«���ޤ���<BR>
		����¾���ηǼ��Ĥ����Ѥˤ�äƲ���»�����ФƤ�����Ԥ���Ǥ���餤�ޤ���</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">Mireille��ͭ�λ���</H3>
	<DIV class="section">
	<H4 class="h">�����κ��</H4>
	<P>�ޤ�������Ͽ侩���ޤ��󡢽�����ǽ��Ȥ����Ȥ򤪴��ᤷ�ޤ���
	����Ǥ�Ƶ����������褦�Ȥ�����ϰʲ��Τ褦�ˤʤ�ޤ���</P>
	<UL>
		<LI>�Ƶ���������¸�ߤ����ҵ������դ��Ƥ��ʤ���Τϥ���åɤ��Ⱥ������ޤ���</LI>
		<LI>�Ƶ����˻ҵ��������Ǥ�Ĥ��Ƥ�����ϡ��Ƶ�������ʸ�������������ޤ���</LI>
		<LI>�����ԤΤߤ��ҵ������դ��Ƥ��륹��åɤ򡢥���åɤ��Ⱥ���Ǥ��ޤ���</LI>
	</UL>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">��̾</H4>
	<P>����Ū�ˡ���̾��Ʊ���ͤʤ�Ʊ���ʪ���㤨�аۤʤ��ʪ���ΤϤ��Ǥ���
	��ƻ��˻Ȥä��ѥ���ɤ�̾�������������Ƥ���Τǡ������Ǥ�̾�����Ѥ��Ȱ㤦��ʪ�����ˤʤäƤ��ޤ��ޤ���</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">��ʸ</H4>
	<P>URLʸ���󤬤���ȼ�ưŪ�˥�󥯤��Ƥ���ޤ���
	���Ȥ�URL�Ǥ⡢http����񤫤ʤ��褦�ˤ���м�ư��󥯤���ʤ��褦�ˤʤ�ޤ���������������������˼�ư��󥯤���ʤ��褦�ˤ������������Τ����ɤ��ͤ��Ƥ���ˤ��Ƥ���������</P>
	<P>�̹��ܤ˼����Ƥ��붯Ĵ���椫��Ϥޤ�Ԥ䡢����ɽ���˥ޥå�������ϡ��񤤤����˲��餫�η��Ƕ�Ĵ����ޤ���</P>
	<P>���ʤߤ�Ⱦ�ѥ������ʤ⤿�֤�Ȥ��ޤ���</P>
	</DIV>
		
	<DIV class="section">
	<H4 class="h">��å�</H4>
	<P>�����������Ԥ�Ƚ�Ǥˤ�äƥ�å����줿�ꡢ����åɤ����Υ���åɤκ����Ԥ�����Ԥ�Ƚ�Ǥˤ���å�����뤳�Ȥ�����ޤ���
	��å����줿�����䥹��åɤϡ�����ʹ��ѹ����Ǥ��ʤ��ʤ�ޤ���</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">NG���</H4>
	<P>NG��ɤ�ޤ����Ƥ򤷤Ƥ��ޤ��ȡ����顼��ȯ�����ޤ���
	NG��ɤ�ޤޤʤ��褦�ˤ��ʤ�����ƤǤ��ޤ��󤬡�����˰��ä����äƤ��ޤ��褦����Ƥϡ���Ƥ��뤳�Ȥ��Τ�Τ�ľ�����ۤ����������⤷��ޤ���</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">���ޥ��</H4>
	<P>���ޥ�ɤϲ�����⤢��ΤǤ����������Ǥ��ɤ��Ȥ���Ȼפ����Τ������夲�ޤ���</P>
	<DL class="section">
		<DT>icon=<VAR>password</VAR></DT>
		<DD>�ѥ���ɤ���ꤷ�ơ����ѥ��������Ȥ���褦�ˤ��ޤ���<DD>
		<DT>dnew</DT>
		<DD>�������˵�������������򹹿����ޤ���</DD>
		<DT>znew</DT>
		<DD>�������˥���åɤκǽ��ѹ������򹹿����ޤ���</DD>
		<DT>renew</DT>
		<DD>�������ˡ���������������ȥ���åɤκǽ��ѹ������򡢤Ȥ�˹������ޤ���</DD>
		<DT>signature=<VAR>seed of signature</VAR></DT>
		<DD>��̾����������ݤ˻Ȥ�ʸ����򡢥ѥ���ɤǤʤ��������Ȥ��褦�ˤ��ޤ���</DD>
	</DL>
	</DIV>
</DIV>


<DIV class="section">
<H3 class="h">���ߤ��������</H3>
	<DIV class="section">
	<H4 class="h">Mireille������</H4>
	<UL>
_HTML_
print<<"_HTML_";
		<LI>��Ƹ�<STRONG>$CF{'newnc'}</STRONG>�ð���ε����ˡ�$CF{'new'}�ץޡ�����Ĥ��롣</LI>
		<LI>�ɤ�������Ǥ�<STRONG>$CF{'newuc'}</STRONG>�ô֤ϡ�̤�ɡ׾��֤�ݻ����롣</LI>
		<LI>�̾�⡼�ɤǤϡ�1�ڡ���������<STRONG>$CF{'page'}</STRONG>����å�ɽ�����ޤ���</LI>
		<LI>����������⡼�ɤǤϡ�1�ڡ���������<STRONG>$CF{'delpg'}</STRONG>����å�ɽ�����ޤ���</LI>
		<LI>��������Τ�����<STRONG>$CF{'logmax'}</STRONG>����åɤ���¸����Ƥ��ޤ���</LI>
		<LI>������@{[($CF{'tags'})?"<STRONG>$CF{'tags'}</STRONG>����ѤǤ��ޤ�":'���ڻ��ѤǤ��ޤ���']}��</LI>
		<LI>����<STRONG>@{[('input'eq$CF{'colway'})?'INPUT':'SELECT']}����</STRONG>�����٤ޤ���</LI>
		<LI>������<STRONG>@{[('date'eq$CF{'sort'})?'�������':'�����ֹ�']}</STRONG>���ɽ������ޤ���</LI>
		<LI>���л��ꥢ�������<STRONG>����@{[$CF{'relativeIcon'}?'':'��']}��ǽ</STRONG>�Ǥ���</LI>
		<LI>���л��ꥢ�������<STRONG>����@{[$CF{'absoluteIcon'}?'':'��']}��ǽ</STRONG>�Ǥ���</LI>
		<LI>��̾��<STRONG>ɽ������@{[$CF{'signature'}?'��':'����']}</STRONG>��</LI>
_HTML_
#��綯Ĵ��Ϣ
{
	my%ST=($CF{'strong'}=~/(\S+)\s+(\S+)/go);
	my$line;my$regexp;
	for(keys%ST){
		my$str=$_;
		$str=~s/&/&#38;/go;
		$str=~s/"/&#34;/go;
		$str=~s/'/&#39;/go;
		$str=~s/</&#60;/go;
		$str=~s/>/&#62;/go;
		if($ST{$_}=~m{^(/.+/)$}o){
			$regexp.=qq(<STRONG style="color:#f77;font-weight:normal">$str</STRONG>, );
		}elsif(m!^(/.+/)$!o){
			$regexp.=qq(<STRONG class="$ST{$_}">$str</STRONG>, );
		}else{
			$line.=qq(<STRONG class="$ST{$_}">$str</STRONG>, );
		}
	}
	chop$line;chop$line;
	chop$regexp;chop$regexp;
	if($line&&$regexp){
		print"\t\t<LI>$line �ǻϤޤ�Ԥȡ�<BR>����ɽ�� $regexp �˥ޥå�������϶�Ĵɽ������ޤ���</LI>\n";
	}elsif($line){
		print"\t\t<LI>$line �ǻϤޤ�Ԥ϶�Ĵɽ������ޤ���</LI>\n";
	}elsif($regexp){
		print"\t\t<LI>����ɽ�� $regexp �˥ޥå�������϶�Ĵɽ������ޤ���</LI>\n";
	}else{
		print"\t\t<LI>��綯Ĵ��OFF�ˤʤäƤ��ޤ���</LI>\n";
	}
}
#���������Ϣ
{
	my$iconlist=&iptico;
	my$group=@{[$iconlist=~/<OPTGROUP.*/gio]};
	my$icons=@{[$iconlist=~/<OPTION.*/gio]};
	my($name,$link,%icon);
	for($iconlist=~/(<!-- %(?:[A-Z0-9]+_)?(?:VENDOR|COPY1)(?:_[A-Z0-9]+)?(?: (?:.*?))?\s*-->)/go){
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
	print"\t\t<LI>$group���롼�ס�$icons��Υ����������Ѳ�ǽ�Ǥ���</LI>\n";
	delete$icon{''};
	(%icon)&&(print"\t\t<LI>".join("��\n",values%icon)."\n���������ͭ�����Ǻ����Ѥ��Ƥ��ޤ���</LI>\n");
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
	</UL>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">���å�����Ϣ</H4>
		<FORM action="#" method="get">
		<TABLE cellspacing="2" summary="���å���������" style="margin:0.5em auto 0.5em 1em">
		<TR><TH>���ʤ��Υ��å�����</TH>
		<TD><INPUT id="yourCookie" name="yourCookie" type="text" size="100" value="$ENV{'HTTP_COOKIE'}" readonly></TD>
		</TR>
		<TR><TH>Mireille�Ѥ����ơ�</TH>
		<TD><INPUT id="mirCookie" name="mirCookie" type="text" size="100" value="$decoded" readonly></TD>
		</TR>
		<TR><TH>���å����񤭴�����</TH>
		<TD><INPUT id="cookiedata" name="cookiedata" type="text" size="100" value="$cookie"></TD>
		</TR>
		<TR><TD colspan="2">
		<INPUT type="submit" class="submit" value="OK"
		 onclick="reviseCookie(event);return false" onkeypress="reviseCookie(event);return false">
		<INPUT type="reset" class="reset" value="Reset"
		 onclick="resetCookie(event);return false" onkeypress="resetCookie(event);return false">
		</TD></TR></TABLE>
		</FORM>
_HTML_
}
		print<<'_HTML_';
<SCRIPT type="text/JavaScript">
<!--
function reviseCookie(e){
	var cookie;
	if(document.all)cookiedata=document.all('cookiedata').value;
	else if(document.getElementById)cookie=document.getElementById('cookiedata').value;
	else return false;
	
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
}
function resetCookie(e){
	var cookiedata;
	if(document.all)cookiedata=document.all('cookiedata');
	else if(document.getElementById)cookiedata=document.getElementById('cookiedata');
	else return false;
	
	var date=new Date();
	cookiedata.value="expire%09"+parseInt(date.getTime()/1000);
}
//-->
</SCRIPT>
		<P>�֥��å����񤭴����פˤ�äơ�Mireille�ѤΥ��å�����񤭴����뤳�Ȥ��Ǥ��ޤ���<BR>
		�������褿�Ǽ��Ĥˡ����ޤǹԤäƤ���Ǽ��ĤΥ��å�����ܿ����롢�Ȥ������Ȥ⡢<BR>
		�ܿ����ˤʤ����ܤΥ��å����ϰܿ��Ǥ��ޤ��󤬡�����Ū�ˤϲ�ǽ�Ǥ���</P>
		<P>��Reset�פ򲡤��ȡ�̤�ɵ������Τ餻��ǽ���������Ǿ��¤Υ��å���������Ϳ�����ޤ���<BR>
		���å������ʤ����֤��顢��Reset�ץܥ���򲡤�����ǡ���OK�פ򲡤��ƥ��å�������¸����ȡ�<BR>
		̤�ɵ������Τ餻��ǽ�ϸ����褦�ˤʤ�ޤ���</P>
	</DIV>
</DIV>

<DIV class="section">
<H3 class="h">���Τۤ�</H3>
		<DIV class="section">
		<H4 class="h">��ĤΥ���åɤλȤ��ޤ路��侩���ޤ�</H4>
		<P>���ηǼ��Ĥϰ�İ�ĤΥ���åɤ�������Ĺ���ޤǿ��Ӥ롦����<BR>
		�Ȥ��ä��Ȥ��������ꤷ�ƺ���Ƥ��ޤ���<BR>
		�Ƶ�����3�Ԥ�ʸ�Ϥ����쥹��̵�����ʥ���åɤ��������󡦡���<BR>
		�Ȥ����Ȥ������򤱤��ۤ����������⤷��ޤ���<BR>
		�ʥ���¸�������Թ�ǥ����С��إåɤ������뤫�⡣����</P>
		</DIV>
		
		<DIV class="section">
		<H4 class="h">��������κ����</H4>
		<P>�������̵�¤Ǥ���<BR>
		������������䤷�Ƥ⤢�ޤ����®�٤�����ʤ��褦�ˤ��Ƥ���Τ�����פ��ȡ�<BR>
		��������������Υƥ��ȴĶ��Ǥ�700�ĤΥ�������ǻ�ƤߤƤ���ä�ɽ������뤳�Ȥ��ǧ���ޤ�����<BR>
		�ºݤ�HTTP����٤�����ˤʤꡢž���˻��֤�������Τ��񤷤��Ȥϻפ��ޤ���^^;;</P>
		</DIV>
		
		<DIV class="section">
		<H4 class="h">�ʤˤ�������</H4>
		<P>���ηǼ��ĤǤ��������Ȥ������ˤʤ�Ȥ����������ɲä����ߤ�����ǽ������С�<BR>
		Airemix <A href="http://www.airemix.com/" title="Airemix" target="_top">http://www.airemix.com/</A> �ηǼ��Ĥ˽񤭹��फ���᡼��(<A href="mailto:naruse&#64;airemix.com">naruse&#64;airemix.com</A>)�򤯤�������<BR>
		�����ڤˤ��Ʋ����äƷ빽�Ǥ��ΤǢ�</P>
		<P>���ʤߤ˥᡼���PGP�Ź沽�������ꤿ�����ϡ�pgp.nic.ad.jp�Τ褦�ʸ����������С��ǡ�<BR>
		"Airemix"�Ǹ�������������θ��������������ޤ��Τǡ������ȤäƤ���������<BR>
		���λ���ϡ�DB DB A4 76 FD BD 94 50 02 CD 0E FC BC E3 C3 88 47 2E C1 EA�פǤ���</P>
		</DIV>
	</DIV>
</DIV>



<DIV class="section">
<H2 class="h">��������������</H2>
<P>Mireille�ˤϥ�������������夵���뤿��Ρ֥������������פ����ꤵ��Ƥ��ޤ���<BR>
�����Windows�Ǥ����֥��硼�ȥ��åȥ����פΤ褦�ʤ�Τǡ�<BR>
�Ф��ʤ���Ф����ʤ����ǤϤ���ޤ��󤬡��Ȥ�����������⤷��ޤ���</P>
<P>�ɤΤ褦�ʤ�Τ����ꤵ��Ƥ��뤫�Τꤿ���Ȥ������˿͡�����<BR>
��Ȥ����ä����Τ���˰ʲ��˼�ʤ�Τ�󤲤Ƥ����ޤ���</P>


<DIV class="section">
<H3 class="h">Index���̤ΤȤ�</H3>
<DL>
	<DT><KBD>Alt+[1-9]</KBD></DT>
	<DD>���Υڡ�����ξ夫��[1-9]���ܤε����Ρ��ֿ��ؤΥ�󥯤����򤵤�ޤ���<BR>
	�֥饦���ˤ�äƤϡ����ε������Ф����ֿ����̤˰�ư���ޤ���</DD>
	<DT><KBD>Alt+Shift+[1-9]</KBD></DT>
	<DD>[1-9]�ڡ����ܤؤΥ�󥯤����򤵤�ޤ���<BR>
	�֥饦���ˤ�äƤϡ����Τޤ�����ڡ����ذ�ư���ޤ���</DD>
	<DT><KBD>Alt+[,.]</KBD></DT>
	<DD><KBD>,</KBD> �ǿ����������Τ���ڡ�����<KBD>.</KBD> ���Τε����Τ���ڡ����Υ�󥯤����򤵤�ޤ���<BR>
	�֥饦���ˤ�äƤϡ����Τޤޥڡ������ư���ޤ���<BR>
	JIS�����ܡ��ɤ�ȤäƤ������Ǥ����餳�Υ�������ΰ�̣���狼�뤫�⤷��ޤ���</DD>
	<DT><KBD>Alt+M</KBD></DT>
	<DD>�����ʥӤ� ���粽/�����ȥ벽 ���ޤ���</DD>
	<DT><KBD>Alt+C</KBD></DT>
	<DD>�����ʥӤ��Ĥ��ޤ���</DD>
	<DT><KBD>Alt+N</KBD></DT>
	<DD>�����ʥӤ򳫤��ޤ���</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">��Ʋ��̤ΤȤ�</H3>
<DL>
	<DT><KBD>Alt+J</KBD></DT><DD>����̾�פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+N</KBD></DT><DD>��̾���פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+K</KBD></DT><DD>��Cookie�פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+I</KBD></DT><DD>�֥�������פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+L</KBD></DT><DD>��E-mail�פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+O</KBD></DT><DD>�֥ۡ���פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+B</KBD></DT><DD>����ʸ�פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+C</KBD></DT><DD>�ֿ��פ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+P</KBD></DT><DD>�֥ѥ���ɡפ˥������뤬�ܤ�ޤ���</DD>
	<DT><KBD>Alt+M</KBD></DT><DD>�֥��ޥ�ɡפ˥������뤬�ܤ�ޤ���</DD>
	
	<DT><KBD>Alt+S</KBD></DT><DD>�ե���������Ƥ��������ޤ���</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">����¾�ΤȤ�</H3>
<DL>
	<DT><KBD>Alt+S</KBD></DT><DD>����/�������ޤ���</DD>
	<DT><KBD>Alt+R</KBD></DT><DD>�ե���������Ƥ�ꥻ�åȤ��ޤ���</DD>
</DL>
</DIV>
</DIV>



<DIV class="section">
<H2 class="h">��<A name="�����äˤʤä��Ȥ���">�����äˤʤä��Ȥ���</A></H2>
<DL>
<DT>Academic HTML &lt;<a href="http://www.tg.rim.or.jp/~hexane/ach/">http://www.tg.rim.or.jp/~hexane/ach/</A>&gt;</DT>
<DD>HTML/CSS�˴ؤ���Ū�Τʾ��󤬤������󤢤�ޤ���<BR>
HTML/CSS����̤�ؤӤ������Ϥ����򸫤�����ǻ�­��Ƥ��ޤ��ޤ���</DD>
<DT>Another HTML-lint &lt;<a href="http://openlab.ring.gr.jp/k16/htmllint/">http://openlab.ring.gr.jp/k16/htmllint/</A>&gt;</DT>
<DD>HTML�θ��ڤ˺ݤ����Ѥ��ޤ�����<BR>
���ƥ����å�����ȡ��ۤȤ�ɤοͤ�����å�������뤳�ȤǤ��礦��</DD>
<DT>ARTEMIS &lt;<a href="http://www.artemis.ac/arrange/">http://www.artemis.ac/arrange/</A>&gt;</DT>
<DD>IconPreview�Ϥ�������Ǥ��������ʤΤ�ĺ���ޤ�����<BR>
��������Ƥ�����ȶ����Ƥ������⤳���Τ򸫤ơ��Ǥ���<BR>
¾�ˤ⤤����Ȼ��ͤˤ��Ƥ��ޤ���<BR>
������ǽ�Ǥ����򸫽������Ͽ�¿������ޤ���</DD>
<DT>HTMLȷ�ݶ���� &lt;<a href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru">http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru</A>&gt;</DT>
<DD>�ĥå��ߥᥤ���HTML���⥵���ȡ��ˤ錄���ϸ����ޤ�����<BR>
��HTML 4.01 �Τߤ򡢽��˳���Ū�ʶ�̣���鸦��פ��Ƥ��뤽���Ǥ���<BR>
HTML�ι����˺ݤ��ƻ��ͤˤ��ޤ�����</DD>
<DT>jcode.pl &lt;<a href="http://www.srekcah.org/jcode/">http://www.srekcah.org/jcode/</A>&gt;</DT>
<DD>�����������Ѵ��ѤΥ饤�֥��Ǥ���<BR>
Mireille���ΤǤϲ��夷�Ƥ���ΤǻȤäƤ��ޤ���<BR>
����CGI�Ǥϰ������ڤ�Ф��ƻȤäƤ��ޤ���</DD>
<DT>Jcode.pm &lt;<a href="http://openlab.ring.gr.jp/Jcode/index-j.html">http://openlab.ring.gr.jp/Jcode/index-j.html</A>&gt;</DT>
<DD>jcode.pl�θ�Ѥ�Perl5��PerlModule�ȤʤäƤ��ޤ���<BR>
jcode.pl�ε�ǽ��Unicode�򰷤���ǽ���ɲä���Ƥ��ޤ���<BR>
Perl5.8�Ǥ�Encode�⥸�塼����ִ�����Ƥ���褦�Ǥ���</DD>
<DT>KNET-WEB &lt;<a href="http://www.kent-web.com/">http://www.kent-web.com/</A>&gt;</DT>
<DD>�ʤˤϤȤ⤢�����ܤ�CGI/Perl����Ϳ�����ƶ��Ͼ��ʤ��Ϥʤ��Ϥ��Ǥ���<BR>
��ĿͤǤ��ä�YYBOARD,YYCHAT�ˤϤ����äˤʤ�ޤ�����<BR>
�����ƤȤäĤ��פ�CGI��¿���Ǥ���</DD>
<DT>Perl��� &lt;<a href="http://www.din.or.jp/~ohzaki/perl.htm">http://www.din.or.jp/~ohzaki/perl.htm</A>&gt;</DT>
<DD>URI��ư��󥯵�ǽ��Ĥ���˺ݤ����ͤˡ������ष��ݼ̤��Ǥ���<BR>
Perl������ɽ���˴ؤ��ƤȤƤ�ͭ�Ѥʾ��󤬤���ޤ���</DD>
<DT>W3C HTML Validation Service &lt;<a href="http://validator.w3.org/">http://validator.w3.org/</A>&gt;</DT>
<DD>HTML���ʤκ����Ԥ����Ρ�W3C�ˤ��HTML���ڥ����ӥ��Ǥ���<BR>
Another HTML-lint�������å����ܤϾ��ʤ�Ǥ���</DD>
<DT>�Ȥۤۤ�WWW���� &lt;<a href="http://tohoho.wakusei.ne.jp/">http://tohoho.wakusei.ne.jp/</A>&gt;</DT>
<DD>HTML����Perl���Ȥ�˻�����ե��������ˤ��ޤ�����<BR>
�ʤ��ʤ��ܤäƤ��������Ǥ���</DD>
<DT>���� &lt;<a href="http://kano.feena.jp/">http://kano.feena.jp/</A>&gt;</DT>
<DD>LastPost�Ϥ�����ealis�ο����Ǥ���<BR>
�ޤ�1.2.2�ε����ʥӤϿ�ǵ����Τ�Υ١����˺��ޤ�����<BR>
�Ƕ�Ǥ�PHP�˰ܤäƤ���٤��ѤȤ�����Τ��Ϻ����Ƥ���ä����褦�Ǥ���</DD>
<DT>SWORD AND COMMERCE &lt;<a href="http://www10.plala.or.jp/ryokufuudou/kijindou.html">http://www10.plala.or.jp/ryokufuudou/kijindou.html</A>&gt;</DT>
<DD>retro����ˤ�Mireille�ǤĤޤŤ���No.1�Ȼפ��륢����������β����񤤤Ƥ��������ޤ�����<BR>
¾�ˤ�Mireille�β��������������¿�����Ƥ�餤�ޤ�����<BR>
���ʤߤˡ�retro����Υ����ȼ��Τ�RagnarkOnline�ϻ��̥����ȤǤ���</DD>
<DT>Snowish Hills &lt;<DEL>http://snowish.cside8.com/</DEL>&gt;</DT>
<DD>Mireille���ꤳ��ˤ����äơ�Ⱦ�Х��󥵥��ȸܵҤȤ��ơ�������ͭ�Ѥʥ��ɥХ�����ĺ���ޤ�����<BR>
�ä˴���CGI����̾����˸����ʤ���С����ʤ��ϼ�ʤ�ΤˤʤäƤ����Ǥ��礦��<BR>
���ߤν�����֤Υǥ��������̾����Υǥ������١����ˤ��Ƥ��ޤ���<BR>
���ʤߤˡ���̾����Υ����ȼ��Τ�Key��CG�����ȤǤ���</DD>
</DL>
<P>¾�ˤ�ո��򲼤��ä����������ͤˤ��������ȡ�CGI�κ�Ԥ���˴��դ��ޤ���</P>
</DIV>

<P class="note">���������Ǥ�&trade;��&reg;��&copy;�ޡ����Ͼ�ά���Ƥ��ޤ���<BR>
���줾��Υ�����̾�䥽�եȥ�����̾�ʤɤϳơ��ξ�ɸ����Ͽ��ɸ�ʤɤǤ���</P>

<P class="note">���ηǼ��Ĥϡ�Microsoft Internet Explorer for Windows �С������5�ʾ���Ȥ����оݤȤ���<BR>
Windows��InternetExplorer6�ȡ�Netscape��Chimera�ʤɤ�Mozilla�Ϥǡ��ܴۤ�����ư��򤷤ޤ���<BR>
�ޤ�Opera7��Microsoft Internet Explorer 5 for Macintosh�Ǥ⳵�ʹ����̤��ư��򤹤�Ϥ��Ǥ���<BR>
�嵭�Υ֥饦���ʳ��Ǥ�ư��Ϥ���Ϥ��Ǥ��������ɤ��ʤäƤ��ޤ���ǽ��������ޤ���<BR>
��λ�����������ޤ��� ��â�����ɤ߽񤭤��Ǥ��ʤ�����Mireille�ΥХ��Ǥ���</P>
_HTML_
print<<"_HTML_".&getFooter;
<DIV align="center" class="note" style="width:15em">
<P class="heading4" style="text-align:center">�����С��������󡡢�</P>
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
