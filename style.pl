#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Style Sheet -
#
 $CF{'styrev'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;

#-------------------------------------------------
# Mireille���HTML�ǥ�����

#-----------------------------
# Mireile Menu
$CF{'menu'}=<<"_CONFIG_";
<table cellspacing="3" class="menu" summary="MireilleMenu">
<tr>
<td class="menu"><a href="$CF{'index'}?new#Form" accesskey="0">�������</a></td>
<td class="menu"><a href="$CF{'index'}">����</a></td>
<td class="menu"><a href="$CF{'index'}?rvs">����</a></td>
<td class="menu"><a href="$CF{'index'}?del">���</a></td>
<td class="menu"><a href="icon.html" target="_blank">��������</a></td>
<td class="menu"><a href="$CF{'index'}?seek">����</a></td>
<td class="menu"><a href="$CF{'help'}">�إ��</a></td>
<td class="menu"><a href="$CF{'home'}" title="$CF{'name'}">�ۡ���</a></td>
</tr>
</table>
_CONFIG_

#-----------------------------
# Page Header
$CF{'head'}=<<'_CONFIG_';
<table cellspacing="3" class="head" summary="Header">
<tr>
<th><h1 class="head" style="text-align:left">Airemix Mireille Board System</h1></th>
<td style="letter-spacing:1em;text-align:right">��������������</td>
</tr>
</table>
_CONFIG_

#-----------------------------
# Page Footer
$CF{'foot'}=<<'_CONFIG_';
<table cellspacing="3" class="head" summary="Footer">
<tr>
<td style="letter-spacing:1em;text-align:left">��������������</td>
<th><h1 class="head" style="text-align:right"><a href="./" style="color:#fff;font:normal 17px;">BACK to INDEX</a></h1></th>
</tr>
</table>
_CONFIG_

#-----------------------------
# ��ս񤭡�TOP�ڡ����Υ�˥塼�β���ɽ������ޤ���
$CF{'note'}=<<'_CONFIG_';
<div class="note" style="width:30em;">
���쥹���դ�������åɤϰ��־�˰�ư���ޤ���<br>
��̤�ɵ���������������֤�ɽ������ޤ���<br>
��24���ְ������Ƥˤ�<span class="new">New!</span>�ޡ������դ��ޤ���<br>
�������ʥ�С��򥯥�å�����ȡ����ε����ν������̤ˤʤ�ޤ���<br>
������¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������<br>
</div>
_CONFIG_

#-----------------------------
# �Ƶ���
$CF{'artprt'}=<<'_CONFIG_';
<div class="thread">
<table cellspacing="0" class="subject">
<tr>
<th class="subject"><h2 class="subject"><a name="$DT{'i'}" id="$DT{'i'}" title="$DT{'i'}�֥���å�">$DT{'subject'}</a></h2></th>
<td class="arrow"><a href="#@{[$DT{'ak'}-1]}" title="��Υ���åɤ�">��</a>
<a href="$CF{'index'}?res=$DT{'i'}#Form" accesskey="$DT{'ak'}" title="���ε������ֿ�($DT{'ak'})">��</a>
<a name="$DT{'ak'}" href="#@{[$DT{'ak'}+1]}" title="���Υ���åɤ�">��</a></td>
</tr>
</table>
<table cellspacing="0" class="parent" summary="Article$DT{'i'}-0">
<col span="3">
<tr>
<td class="prtnum">
<a name="$DT{'i'}-$DT{'j'}" id="$DT{'i'}-$DT{'j'}" class="number"
 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">��No.$DT{'i'}��</a>
</td>
<td class="info">$DT{'new'}
&#8201;<span class="name">$DT{'name'}</span>
&#8194;<span class="home">$DT{'home'}</span>
</td>
<td class="info" style="text-align:right;">
<span class="date">$DT{'date'}</span>
<a href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">
<span class="revise" title="$DT{'i'}�֥���åɤοƵ�����������">�ڽ�����</span></a>
</td>
</tr>
<tr>
<td class="icon"><img src="$CF{'icon'}$DT{'icon'}" alt="icon"></td>
<td colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</td>
</tr>
</table>
_CONFIG_

#-----------------------------
# �ҵ���
$CF{'artchd'}=<<'_CONFIG_';
<table cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}">
<col span="3">
<!-- �ҵ��������ȥ����Ѥ����硢����1�Ԥ򥳥��ȥ����� -->
<!-- <tr><th colspan="3" class="childsubject"><h3 class="childsubject">$DT{'subject'}</h3></th></tr> -->
<tr>
<td class="chdnum">
<a name="$DT{'i'}-$DT{'j'}" id="$DT{'i'}-$DT{'j'}" class="number"
 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">��Re:$DT{'j'}��</a>
</td>
<td class="info">$DT{'new'}
&#8201;<span class="name">$DT{'name'}</span>
&#8194;<span class="home">$DT{'home'}</span>
</td>
<td class="info" style="text-align:right;">
<span class="date">$DT{'date'}</span>
<a href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">
<span class="revise" title="$DT{'i'}�֥���å�$DT{'j'}���ܤλҵ�����������">�ڽ�����</span></a>
</td>
</tr>
<tr>
<!-- �����������Ѥ����礳������ -->
<td class="icon"><img src="$CF{'icon'}$DT{'icon'}" alt="icon"></td>
<td colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</td>
<!-- �����������Ѥ����礳���ޤ� -->
<!-- �����������Ѥ��ʤ���礳������ -->
<!-- <td colspan="3" class="body" style="color:$DT{'color'}">$DT{'body'}</td> -->
<!-- �����������Ѥ��ʤ���礳���ޤ� -->
</tr>
</table>
_CONFIG_

#-----------------------------
# �����Υեå���
$CF{'artfot'}=<<'_CONFIG_';
<h3 class="artfot">
<a href="$CF{'index'}?res=$DT{'i'}#Form" accesskey="$DT{'ak'}">���ε������ֿ�����(<span class="ak">$DT{'ak'}</span>)</a>
</h3>
</div>
_CONFIG_

#-----------------------------
# �������/�Խ��ե�����
$CF{'wrtfm'}=<<'_CONFIG_';
<div class="note" style="width:26em">
��������ˤ��������ƤΥ����ϻ��ѤǤ��ޤ���<br>
��HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���<br>
������Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤�<br>
&#8195;&#8201;���Ф餯�ԤĤȴ�ñ���������ФƤ��ޤ�<br>
������¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������<br>
</div>

<table class="write" summary="MainForm">
<col><col><col>
<thead><tr><th colspan="3" class="wrttle"><a name="Form" />$DT{'caption'}</th></tr></thead>
<tbody>
<tr title="Name\n̾�������Ϥ��ޤ���ɬ�ܡ�\n�ǹ�����50ʸ���ޤǤǤ�">
<th class="item">
<label accesskey="n" for="name">��̾��(<span class="ak">N</span>)��</label>
</th>
<td class="input">
<input type="text" name="name" id="name" class="blur" maxlength="50" style="ime-mode:active;width:220px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'name'}">
<label for="cook">Cookie��<input name="cook" id="cook" type="checkbox" checked></label>
</td>
<th class="item" title="Icon\n������������򤷤ޤ�" style="text-align:center">
<label accesskey="i" for="icon">�� <a href="icon.html" title="�����������" target="_blank">��������</a>(<span class="ak">&#8201;I&#8201;</span>) ��</label>
</th>
</tr>
<tr title="e-maiL\n�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<th class="item">
<label accesskey="l" for="email">��E-mail(<span class="ak">L</span>)��</label>
</th>
<td class="input">
<input type="text" name="email" id="email" class="blur" maxlength="100" style="ime-mode:inactive; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'email'}">
</td>
<td rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<img alt="Preview" name="Preview" src="$CF{'icon'}$CK{'icon'}">
</td>
</tr>
<tr title="hOme\n��ʬ�Υ����Ȥ����Ϥ��ޤ�">
<th class="item">
<label accesskey="o" for="home">���ۡ���(<span class="ak">O</span>)��</label>
</th>
<td class="input">
<input type="text" name="home" id="home" class="blur" maxlength="80" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'home'}">
</td>
</tr>
<tr title="subJect\n��������̾�����Ϥ��ޤ�\n�ǹ�����100ʸ���ޤǤǤ�">
<th class="item">
<label accesskey="j" for="subject">����̾(<span class="ak">J</span>)��</label>
</th>
<td class="input">
<input type="text" name="subject" id="subject" class="blur" maxlength="70" style="ime-mode:active; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'subject'}">
</td>
</tr>
<tr title="Color\n��ʸ�ο������Ϥ��ޤ�\n��#???��#??????��rgb(???,???,???)��WebColor\n�Τɤ�Ǥ���ѤǤ��ޤ�">
<th class="item">
<label accesskey="c" for="color">����(<span class="ak">C</span>)��</label>
</th>
<td class="input">
<!-- input type="text" name="color" id="color" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'color'}" -->
<select name="color" id="color">
@{[&color($DT{'color'})]}</select>
&#8194;
<span title="Password\n���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�\n�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<span class="item">
<label accesskey="p" for="pass">���ѥ����(<span class="ak">P</span>)��</label>
</span>
<span class="input">
<input type="password" name="pass" id="pass" class="blur" maxlength="24" style="ime-mode:disabled;font-size:85%;width:90px" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'pass'}">
</span>
</span>
</td>
</tr>
<tr title="eXcommand\n���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�\n���̤ϻȤ��ޤ���">
<th class="item">
<label accesskey="x" for="cmd">��E<span class="ak">X</span>���ޥ�ɡ�</label>
</th>
<td class="input">
<input type="text" name="cmd" id="cmd" class="blur" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'command'}">
</td>
<td class="input" title="Icon\n������������򤷤ޤ�">
<select name="icon" id="icon" onchange="IconPreview(this.form['icon'][this.options.selectedIndex].value)">
$main::iconlist</select>
</td>
</tr>
</tbody>
<tbody title="Body\n��������ʸ�����Ϥ��ޤ�\n������10000ʸ���ޤǤǤ�\n������ʸ�����Ȥ����Ƥ��Τޤ�ɽ�������褦�ˤʤäƤ��ꡢ\n���Ѥ��뤳�ȤϤǤ��ޤ���">
<tr>
<td colspan="3" style="text-align:center">
<label accesskey="b" for="body">�� ��ʸ(<span class="ak">B</span>) ��</label><br>
<textarea name="body" id="body" class="blur" cols="80" rows="8" style="ime-mode:active;width:500px;" onFocus="this.className='focus'" onBlur="this.className='blur'">$DT{'body'}</textarea>
</td>
</tr>
</tbody>
<tbody>
<tr><td colspan="3" class="wrtfot" title="Submit\n��������Ƥ��ޤ�">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="��Ƥ���">
<!-- <input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="�ꥻ�å�"> -->
</td></tr>
</tbody>
</table>
<script type="text/javascript"><!--
function IconPreview(arg){document.images["Preview"].src="$CF{'icon'}"+arg;}
//--></script>
_CONFIG_

#-----------------------------
# �ֿ��ե�����
$CF{'resfm'}=<<'_CONFIG_';
<table class="write" summary="ResForm">
<col><col><col>
<thead>
<tr><th colspan="3" class="wrttle">
<a name="Form" />$DT{'caption'}
</th></tr>
</thead>
<tbody title="Body\n��������ʸ�����Ϥ��ޤ�\n������10000ʸ���ޤǤǤ�\n������ʸ�����Ȥ����Ƥ��Τޤ�ɽ�������褦�ˤʤäƤ��ꡢ\n���Ѥ��뤳�ȤϤǤ��ޤ���">
<tr>
<td colspan="3" style="text-align:center">
<label accesskey="b" for="body">�� ��ʸ(<span class="ak">B</span>) ��</label><br>
<textarea name="body" id="body" class="blur" cols="80" rows="8" style="ime-mode:active;width:500px;" onFocus="this.className='focus'" onBlur="this.className='blur'">$DT{'body'}</textarea>
</td>
</tr>
</tbody>
<tbody>
<tr title="Name\n̾�������Ϥ��ޤ���ɬ�ܡ�\n�ǹ�����50ʸ���ޤǤǤ�">
<th class="item">
<label accesskey="n" for="name">��̾��(<span class="ak">N</span>)��</label>
</th>
<td class="input">
<input type="text" name="name" id="name" class="blur" maxlength="50" style="ime-mode:active;width:220px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'name'}">
<label for="cook">Cookie��<input name="cook" id="cook" type="checkbox" checked></label>
</td>
<th class="item" title="Icon\n������������򤷤ޤ�" style="text-align:center">
<label accesskey="i" for="icon">�� <a href="icon.html" title="�����������" target="_blank">��������</a>(<span class="ak">&#8201;I&#8201;</span>) ��</label>
</th>
</tr>
<tr title="e-maiL\n�᡼�륢�ɥ쥹�����Ϥ��ޤ�">
<th class="item">
<label accesskey="l" for="email">��E-mail(<span class="ak">L</span>)��</label>
</th>
<td class="input">
<input type="text" name="email" id="email" class="blur" maxlength="100" style="ime-mode:inactive; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'email'}">
</td>
<td rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<img alt="Preview" name="Preview" src="$CF{'icon'}$CK{'icon'}">
</td>
</tr>
<tr title="hOme\n��ʬ�Υ����Ȥ����Ϥ��ޤ�">
<th class="item">
<label accesskey="o" for="home">���ۡ���(<span class="ak">O</span>)��</label>
</th>
<td class="input">
<input type="text" name="home" id="home" class="blur" maxlength="80" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'home'}">
</td>
</tr>
<tr title="subJect\n��������̾�����Ϥ��ޤ�\n�ǹ�����100ʸ���ޤǤǤ�">
<th class="item">
<label accesskey="j" for="subject">����̾(<span class="ak">J</span>)��</label>
</th>
<td class="input">
<input type="text" name="subject" id="subject" class="blur" maxlength="70" style="ime-mode:active; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'subject'}" disabled="disabled">
</td>
</tr>
<tr title="Color\n��ʸ�ο������Ϥ��ޤ�\n��#???��#??????��rgb(???,???,???)��WebColor\n�Τɤ�Ǥ���ѤǤ��ޤ�">
<th class="item">
<label accesskey="c" for="color">����(<span class="ak">C</span>)��</label>
</th>
<td class="input">
<!-- input type="text" name="color" id="color" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'color'}" -->
<select name="color" id="color">
@{[&color($DT{'color'})]}</select>
&#8194;
<span title="Password\n���/�������˻��Ѥ���ѥ���ɤ����Ϥ��ޤ���ɬ�ܡ�\n�ǹ�Ⱦ��24ʸ���ޤǤǤ�">
<span class="item">
<label accesskey="p" for="pass">���ѥ����(<span class="ak">P</span>)��</label>
</span>
<span class="input">
<input type="password" name="pass" id="pass" class="blur" maxlength="24" style="ime-mode:disabled; font-size:85%;width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'pass'}">
</span>
</span>
</td>
</tr>
<tr title="eXcommand\n���ѥ��������Ϥ�Ȥ����ĥ̿���Ȥ����˻��Ѥ��ޤ�\n���̤ϻȤ��ޤ���">
<th class="item">
<label accesskey="x" for="cmd">��E<span class="ak">X</span>���ޥ�ɡ�</label>
</th>
<td class="input">
<input type="text" name="cmd" id="cmd" class="blur" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'command'}">
</td>
<td class="input" title="Icon\n������������򤷤ޤ�">
<select name="icon" id="icon" onchange="IconPreview(this.form['icon'][this.options.selectedIndex].value)">
$main::iconlist</select>
</td>
</tr>
</tbody>
<tbody>
<tr title="Submit\n��������Ƥ��ޤ�"><td colspan="3" class="wrtfot">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="��Ƥ���">
<!-- <input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="�ꥻ�å�"> -->
</td></tr>
</tbody>
</table>
<div class="note" style="width:28em">
�����ɽ������Ƥ��륹��åɡ�No.$DT{'i'}�ۤؤ��ֿ���Ԥ��ޤ���<br>
��������ˤ��������ƤΥ����ϻ��ѤǤ��ޤ���<br>
��HTTP, FTP, MAIL���ɥ쥹�Υ�󥯤ϼ�ư�ǤĤ��ޤ���<br>
���쥹���դ�������åɤϰ��־�˰�ư���ޤ���<br>
������Ū�ʥ֥饦���Ǥϥޥ��������������ܤξ���֤���<br>
&#8195;&#8201;���Ф餯�ԤĤȹ��ܤδ�ñ���������ФƤ��ޤ�<br>
������¾����ǽ�ξܺ٤ˤĤ��Ƥϥإ�פ�������������<br>
</div>
<script type="text/javascript"><!--
function IconPreview(arg){document.images["Preview"].src="$CF{'icon'}"+arg;}
//--></script>
_CONFIG_



#----------------------------------------------------------------------------------------#
#
# ��������Style������
#

#-------------------------------------------------
#�Ƶ���
sub artprt{
  #��������������ä�
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #������줿���Τ餻��
  ($DT{'Mir1'}eq'del')&&($DT{'body'}='Mireille: [���ε����Ϻ������ޤ���]');
  #�������ܤ�Ĵ���򤷤�
  ($DT{'email'})&&($DT{'name'}=qq{<a href="mailto:$DT{'email'}">$DT{'name'}</a>});
  ($DT{'home'})&&($DT{'home'}=qq{<a href="$DT{'home'}" target="_blank">��HOME��</a>});
  $DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
  #̤�ɵ����˰�
  $DT{'new'}='';
  ($DT{'time'}>$CK{'time'})&&($DT{'date'}="<span class=\"new\">$DT{'date'}</span>",$new++);
  ($DT{'time'}>$^T-$CF{'newnc'})&&($DT{'new'}=$CF{'new'});
  #���褤����Ϥ���
  eval qq{print<<"_HTML_";\n$CF{'artprt'}\n_HTML_}; #OLDSTYLE
  #�Ƶ������ä���夬��
}


#-------------------------------------------------
#�ҵ���
sub artchd{
  #��������������ä�
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #�������Ƥ�Ȥ��Ϥ������������Ф����㤦��
  #�������ܤ�Ĵ���򤷤�
  ($DT{'email'})&&($DT{'name'}=qq{<a href="mailto:$DT{'email'}">$DT{'name'}</a>});
  ($DT{'home'})&&($DT{'home'}=qq{<a href="$DT{'home'}" target="_blank">��HOME��</a>});
  $DT{'date'}=&date($DT{'time'}); #UNIX�ä������դ�
  #̤�ɵ����˰�
  $DT{'new'}='';
  ($DT{'time'}>$CK{'time'})&&($DT{'date'}="<span class=\"new\">$DT{'date'}</span>",$new++);
  ($DT{'time'}>$^T-$CF{'newnc'})&&($DT{'new'}=$CF{'new'});
  #���褤����Ϥ���
  eval qq{print<<"_HTML_";\n$CF{'artchd'}\n_HTML_}; #OLDSTYLE
  #�ҵ������ä���夬��
}


#-------------------------------------------------
#�����եå�
sub artfot{
  #��������������ä�
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #����ɽ�����ֿ��⡼�ɡ�
  unless($DT{'res'}){
    #����ɽ���⡼�ɤΤȤ�
    eval qq{print<<"_HTML_";\n$CF{'artfot'}\n_HTML_};
  }else{
    #�ֿ��⡼�ɤΤȤ�
    print<<"_HTML_";
</div>
_HTML_
  }
}


#-------------------------------------------------
# �Ƶ����ե�����
#
sub prtfrm{
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}
  
  ($CF{'prtitm'}=~m/\bicon\b/o)&&(&icon($DT{'icon'}));
  
  my$wrtfm=$CF{'wrtfm'};
  chomp$wrtfm;
  if(defined$DT{'body'}){
    $DT{'caption'}='�� ���������ե����� ��';
    $DT{'Sys'}.=qq{<input name="i" type="hidden" value="$DT{'i'}">\n};
    $DT{'Sys'}.=qq{<input name="j" type="hidden" value="$DT{'j'}">\n};
    $DT{'Sys'}.=qq{<input name="oldps" type="hidden" value="$DT{'oldps'}">\n};
  }else{
    $DT{'caption'}='�� ���������ե����� ��';
    ($DT{'home'})||($DT{'home'}='http://');
    $DT{'subject'}='';
    $DT{'body'}='';
    $DT{'Sys'}.=qq{<input name="j" type="hidden" value="0">\n};
  }
  ($DT{'Sys'})&&($wrtfm=~s{<input}{$DT{'Sys'}<input}io);

  print qq{<form accept-charset="euc-jp" id="newpost" method="post" action="$CF{'index'}">\n};
  eval qq{print<<"_HTML_";\n$wrtfm\n_HTML_};
  print"</form>\n";
}


#-------------------------------------------------
# �ҵ����ե�����
#
sub chdfrm{
  #�ֿ��ե��������
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}

  ($CF{'chditm'}=~m/\bicon\b/o)&&(&icon($DT{'icon'}));

  #�ǥ������ɤ߹���
  my$resfm=$CF{'resfm'};
  chomp$resfm;#�Ǹ�β��Ԥ��ڤ���Ȥ�
  #�ɲþ����������
  $DT{'Sys'}.=qq{<input name="i" type="hidden" value="$DT{'i'}">\n};
  if(defined$DT{'j'}){
    $DT{'Sys'}.=qq{<input name="j" type="hidden" value="$DT{'j'}">\n};
    $DT{'Sys'}.=qq{<input name="oldps" type="hidden" value="$DT{'oldps'}">\n};
    $DT{'caption'}='�� �����ե����� ��';
    #�ǡ������᤹
    $DT{'body'}=~s/<br>/\n/go;#"<br>"2"\n"
    $DT{'body'}=~s/<\/?a[^>]*>//go;#ClearAnchors
    $DT{'body'}=~s/</&#60;/go;
    $DT{'body'}=~s/>/&#62;/go;
  }else{
    $DT{'caption'}='�� �ֿ��ե����� ��';
    $DT{'body'}='';
  }
  ($DT{'Sys'})&&($resfm=~s{<input}{$DT{'Sys'}<input}io);

  #���ܤν������
  ($DT{'home'})||($DT{'home'}='http://'); #http://��������Ƥ���
  #note01:Res����̾�ʤ����Ȥ�
  if($CF{'chditm'}!~m/\bsubject\b/o){
    $DT{'subject'}='disabled';
    $resfm=~s{name="subject"}{name="subject" disabled="disabled"}io;
  }
  
  print<<"_HTML_";
<form accept-charset="euc-jp" id="newpost" method="post" action="$CF{'index'}">
_HTML_
  eval qq{print<<"_HTML_";\n$resfm\n_HTML_};
  print"</form>\n";
}


#-------------------------------------------------
# �������ɽ���Ѥ˥ե����ޥåȤ��줿���ռ������֤�
sub date{
  my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
  #sprintf�������ϡ�Perl�β���򸫤Ƥ�������^^;;
 return sprintf("%4dǯ%02d��%02d��(%s) %02d��%02dʬ" #"1970ǯ01��01��(��) 09��00ʬ"����
 ,$year+1900,$mon+1,$mday,('��','��','��','��','��','��','��')[$wday],$hour,$min);
#  return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"����
#  ,$hour,$min,$sec,$year+1900,$mon+1,$mday,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# ��������ꥹ��
#
sub icon{
  #�ꥹ���ɤ߹���
  unless(defined$main::iconlist){
    sysopen(RD,'icon.txt',O_RDONLY);#||die"Can't open iconlist." #�虜�虜���顼�֤��ʤ��Ƥ⤤���Ǥ���
    flock(RD,LOCK_SH);
    $main::iconlist=join('',<RD>);
    close(RD);
  }
  
  #�������
  if($_[0]){
    #note02
#    #���Ĥ���ʤ���кǸ��Cookie�Τ�Τ��ɲ�
#    ($icon=~s["$CK{'icon'}"]["$CK{'icon'}" selected="selected"]io)
#     ||($icon.=qq{<option value="$CK{'icon'}" selected="selected">$CK{'icon'}</option>\n});
    #���Ĥ���ʤ�����Ф��Τޤޡ����̤ϥ֥饦�������־�Υ������������֡�
    $main::iconlist=~s{value="$_[0]"}{value="$_[0]" selected="selected"}io;
  }elsif(defined$_[0]){
    ($main::iconlist=~s/value="([^"]*)"/value="([^"]*)" selected="selected"/imo)&&($CK{'icon'}=$2);
  }
}


#-------------------------------------------------
# ���顼�ꥹ���ɤ߹���
#
sub color{
  my$list=<<"_HTML_";
<option value="#000000" style="background-color: #000000;">Black</option>
<option value="#2f4f4f" style="background-color: #2f4f4f;">DarkSlateGray</option>
<option value="#696969" style="background-color: #696969;">DimGray</option>
<option value="#808080" style="background-color: #808080;">Gray</option>
<option value="#708090" style="background-color: #708090;">SlateGray</option>
<option value="#778899" style="background-color: #778899;">LightSlateGray</option>
<option value="#8b4513" style="background-color: #8b4513;">SaddleBrown</option>
<option value="#a0522d" style="background-color: #a0522d;">Sienna</option>
<option value="#d2691e" style="background-color: #d2691e;">Chocolate</option>
<option value="#cd5c5c" style="background-color: #cd5c5c;">IndianRed</option>
<option value="#a52a2a" style="background-color: #a52a2a;">Brown</option>
<option value="#8b0000" style="background-color: #8b0000;">DarkRed</option>
<option value="#800000" style="background-color: #800000;">Maroon</option>
<option value="#b22222" style="background-color: #b22222;">FireBrick</option>
<option value="#ff6347" style="background-color: #ff6347;">Tomato</option>
<option value="#ff4500" style="background-color: #ff4500;">OrangeRed</option>
<option value="#dc143c" style="background-color: #dc143c;">Crimson</option>
<option value="#c71585" style="background-color: #c71585;">MediumVioletRed</option>
<option value="#ff1493" style="background-color: #bb1493;">DeepPink</option>
<option value="#8b008b" style="background-color: #8b008b;">DarkMagenta</option>
<option value="#800080" style="background-color: #800080;">Purple</option>
<option value="#9932cc" style="background-color: #9932cc;">DarkOrchid</option>
<option value="#9400d3" style="background-color: #9400d3;">DarkViolet</option>
<option value="#8a2be2" style="background-color: #8a2be2;">BlueViolet</option>
<option value="#6a5acd" style="background-color: #6a5acd;">SlateBlue</option>
<option value="#4b0082" style="background-color: #4b0082;">Indigo</option>
<option value="#00008e" style="background-color: #00008e;">DarkBlue</option>
<option value="#000080" style="background-color: #000080;">Navy</option>
<option value="#191970" style="background-color: #191970;">MidnightBlue</option>
<option value="#483d8b" style="background-color: #483d8b;">DarkSlateBlue</option>
<option value="#0000cd" style="background-color: #0000cd;">MediumBlue</option>
<option value="#4169e1" style="background-color: #4169e1;">RoyalBlue</option>
<option value="#5f9ea0" style="background-color: #5f9ae0;">CadetBlue</option>
<option value="#4682b4" style="background-color: #4682b4;">SteelBlue</option>
<option value="#008080" style="background-color: #008080;">Teal</option>
<option value="#008b8b" style="background-color: #008b8b;">Darkcyan</option>
<option value="#2e8b57" style="background-color: #2e8b57;">SeaGreen</option>
<option value="#228b22" style="background-color: #228b22;">ForestGreen</option>
<option value="#006400" style="background-color: #006400;">DarkGreen</option>
<option value="#556b2f" style="background-color: #556b2f;">DarkOliveGreen</option>
<option value="#6b8e23" style="background-color: #6b8e23;">OliveDrab</option>
<option value="#808000" style="background-color: #808000;">Olive</option>
_HTML_
  ($_[0])&&($list=~s{value="$_[0]"}{value="$_[0]" selected="selected"}io);
  return$list;
}


#-------------------------------------------------
# �եå�������
#
sub footer{
  eval qq{print<<"_HTML_";\n$CF{'menu'}\n_HTML_};
  $CF{'correv'}=~s{ision: }{:}o;#"Revision: 1.2.0.1"->"Rev:1.2.0.1"
  print<<"_HTML_";
$CF{'foot'}
<div class="AiremixCopy">- <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</a>
<var>$CF{'correv'}</var> -</div>
</body>
</html>
_HTML_
  exit;
}


1;
__END__
