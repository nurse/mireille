#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Style Sheet -
#
 $CF{'styrev'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;

#-------------------------------------------------
# Mireille内のHTMLデザイン

#-----------------------------
# Mireile Menu
$CF{'menu'}=<<"_CONFIG_";
<table cellspacing="3" class="menu" summary="MireilleMenu">
<tr>
<td class="menu"><a href="$CF{'index'}?new#Form" accesskey="0">新規投稿</a></td>
<td class="menu"><a href="$CF{'index'}">更新</a></td>
<td class="menu"><a href="$CF{'index'}?rvs">修正</a></td>
<td class="menu"><a href="$CF{'index'}?del">削除</a></td>
<td class="menu"><a href="icon.html" target="_blank">アイコン</a></td>
<td class="menu"><a href="$CF{'index'}?seek">検索</a></td>
<td class="menu"><a href="$CF{'help'}">ヘルプ</a></td>
<td class="menu"><a href="$CF{'home'}" title="$CF{'name'}">ホーム</a></td>
</tr>
</table>
_CONFIG_

#-----------------------------
# Page Header
$CF{'head'}=<<'_CONFIG_';
<table cellspacing="3" class="head" summary="Header">
<tr>
<th><h1 class="head" style="text-align:left">Airemix Mireille Board System</h1></th>
<td style="letter-spacing:1em;text-align:right">■■■■■■■</td>
</tr>
</table>
_CONFIG_

#-----------------------------
# Page Footer
$CF{'foot'}=<<'_CONFIG_';
<table cellspacing="3" class="head" summary="Footer">
<tr>
<td style="letter-spacing:1em;text-align:left">■■■■■■■</td>
<th><h1 class="head" style="text-align:right"><a href="./" style="color:#fff;font:normal 17px;">BACK to INDEX</a></h1></th>
</tr>
</table>
_CONFIG_

#-----------------------------
# 注意書き（TOPページのメニューの下に表示されます）
$CF{'note'}=<<'_CONFIG_';
<div class="note" style="width:30em;">
■レスが付いたスレッドは一番上に移動します。<br>
■未読記事は投稿日時が赤く表示されます。<br>
■24時間以内の投稿には<span class="new">New!</span>マークが付きます。<br>
■記事ナンバーをクリックすると、その記事の修正画面になります。<br>
■その他、機能の詳細についてはヘルプをご覧ください。<br>
</div>
_CONFIG_

#-----------------------------
# 親記事
$CF{'artprt'}=<<'_CONFIG_';
<div class="thread">
<table cellspacing="0" class="subject">
<tr>
<th class="subject"><h2 class="subject"><a name="$DT{'i'}" id="$DT{'i'}" title="$DT{'i'}番スレッド">$DT{'subject'}</a></h2></th>
<td class="arrow"><a href="#@{[$DT{'ak'}-1]}" title="上のスレッドへ">▲</a>
<a href="$CF{'index'}?res=$DT{'i'}#Form" accesskey="$DT{'ak'}" title="この記事に返信($DT{'ak'})">■</a>
<a name="$DT{'ak'}" href="#@{[$DT{'ak'}+1]}" title="下のスレッドへ">▼</a></td>
</tr>
</table>
<table cellspacing="0" class="parent" summary="Article$DT{'i'}-0">
<col span="3">
<tr>
<td class="prtnum">
<a name="$DT{'i'}-$DT{'j'}" id="$DT{'i'}-$DT{'j'}" class="number"
 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">【No.$DT{'i'}】</a>
</td>
<td class="info">$DT{'new'}
&#8201;<span class="name">$DT{'name'}</span>
&#8194;<span class="home">$DT{'home'}</span>
</td>
<td class="info" style="text-align:right;">
<span class="date">$DT{'date'}</span>
<a href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">
<span class="revise" title="$DT{'i'}番スレッドの親記事を修正する">【修正】</span></a>
</td>
</tr>
<tr>
<td class="icon"><img src="$CF{'icon'}$DT{'icon'}" alt="icon"></td>
<td colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</td>
</tr>
</table>
_CONFIG_

#-----------------------------
# 子記事
$CF{'artchd'}=<<'_CONFIG_';
<table cellspacing="0" class="child" summary="Article$DT{'i'}-$DT{'j'}">
<col span="3">
<!-- 子記事タイトルを使用する場合、下の1行をコメントアウト -->
<!-- <tr><th colspan="3" class="childsubject"><h3 class="childsubject">$DT{'subject'}</h3></th></tr> -->
<tr>
<td class="chdnum">
<a name="$DT{'i'}-$DT{'j'}" id="$DT{'i'}-$DT{'j'}" class="number"
 href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">【Re:$DT{'j'}】</a>
</td>
<td class="info">$DT{'new'}
&#8201;<span class="name">$DT{'name'}</span>
&#8194;<span class="home">$DT{'home'}</span>
</td>
<td class="info" style="text-align:right;">
<span class="date">$DT{'date'}</span>
<a href="$CF{'index'}?rvs=$DT{'i'}-$DT{'j'}">
<span class="revise" title="$DT{'i'}番スレッド$DT{'j'}番目の子記事を修正する">【修正】</span></a>
</td>
</tr>
<tr>
<!-- アイコンを使用する場合ここから -->
<td class="icon"><img src="$CF{'icon'}$DT{'icon'}" alt="icon"></td>
<td colspan="2" class="body" style="color:$DT{'color'}">$DT{'body'}</td>
<!-- アイコンを使用する場合ここまで -->
<!-- アイコンを使用しない場合ここから -->
<!-- <td colspan="3" class="body" style="color:$DT{'color'}">$DT{'body'}</td> -->
<!-- アイコンを使用しない場合ここまで -->
</tr>
</table>
_CONFIG_

#-----------------------------
# 記事のフッター
$CF{'artfot'}=<<'_CONFIG_';
<h3 class="artfot">
<a href="$CF{'index'}?res=$DT{'i'}#Form" accesskey="$DT{'ak'}">この記事に返信する(<span class="ak">$DT{'ak'}</span>)</a>
</h3>
</div>
_CONFIG_

#-----------------------------
# 新規投稿/編集フォーム
$CF{'wrtfm'}=<<'_CONFIG_';
<div class="note" style="width:26em">
■入力欄において全てのタグは使用できません。<br>
■HTTP, FTP, MAILアドレスのリンクは自動でつきます。<br>
■一般的なブラウザではマウスカーソルを項目の上に置き<br>
&#8195;&#8201;しばらく待つと簡単な説明が出てきます<br>
■その他、機能の詳細についてはヘルプをご覧ください。<br>
</div>

<table class="write" summary="MainForm">
<col><col><col>
<thead><tr><th colspan="3" class="wrttle"><a name="Form" />$DT{'caption'}</th></tr></thead>
<tbody>
<tr title="Name\n名前を入力します（必須）\n最高全角50文字までです">
<th class="item">
<label accesskey="n" for="name">■名前(<span class="ak">N</span>)：</label>
</th>
<td class="input">
<input type="text" name="name" id="name" class="blur" maxlength="50" style="ime-mode:active;width:220px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'name'}">
<label for="cook">Cookie：<input name="cook" id="cook" type="checkbox" checked></label>
</td>
<th class="item" title="Icon\nアイコンを選択します" style="text-align:center">
<label accesskey="i" for="icon">■ <a href="icon.html" title="アイコン一覧" target="_blank">アイコン</a>(<span class="ak">&#8201;I&#8201;</span>) ■</label>
</th>
</tr>
<tr title="e-maiL\nメールアドレスを入力します">
<th class="item">
<label accesskey="l" for="email">■E-mail(<span class="ak">L</span>)：</label>
</th>
<td class="input">
<input type="text" name="email" id="email" class="blur" maxlength="100" style="ime-mode:inactive; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'email'}">
</td>
<td rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<img alt="Preview" name="Preview" src="$CF{'icon'}$CK{'icon'}">
</td>
</tr>
<tr title="hOme\n自分のサイトを入力します">
<th class="item">
<label accesskey="o" for="home">■ホーム(<span class="ak">O</span>)：</label>
</th>
<td class="input">
<input type="text" name="home" id="home" class="blur" maxlength="80" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'home'}">
</td>
</tr>
<tr title="subJect\n記事の題名を入力します\n最高全角100文字までです">
<th class="item">
<label accesskey="j" for="subject">■題名(<span class="ak">J</span>)：</label>
</th>
<td class="input">
<input type="text" name="subject" id="subject" class="blur" maxlength="70" style="ime-mode:active; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'subject'}">
</td>
</tr>
<tr title="Color\n本文の色を入力します\n（#???、#??????、rgb(???,???,???)、WebColor\nのどれでも使用できます">
<th class="item">
<label accesskey="c" for="color">■色(<span class="ak">C</span>)：</label>
</th>
<td class="input">
<!-- input type="text" name="color" id="color" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'color'}" -->
<select name="color" id="color">
@{[&color($DT{'color'})]}</select>
&#8194;
<span title="Password\n削除/修正時に使用するパスワードを入力します（必須）\n最高半角24文字までです">
<span class="item">
<label accesskey="p" for="pass">■パスワード(<span class="ak">P</span>)：</label>
</span>
<span class="input">
<input type="password" name="pass" id="pass" class="blur" maxlength="24" style="ime-mode:disabled;font-size:85%;width:90px" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'pass'}">
</span>
</span>
</td>
</tr>
<tr title="eXcommand\n専用アイコンを始めとする拡張命令を使う場合に使用します\n普通は使いません">
<th class="item">
<label accesskey="x" for="cmd">■E<span class="ak">X</span>コマンド：</label>
</th>
<td class="input">
<input type="text" name="cmd" id="cmd" class="blur" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'command'}">
</td>
<td class="input" title="Icon\nアイコンを選択します">
<select name="icon" id="icon" onchange="IconPreview(this.form['icon'][this.options.selectedIndex].value)">
$main::iconlist</select>
</td>
</tr>
</tbody>
<tbody title="Body\n記事の本文を入力します\n全角約10000文字までです\nタグや文字参照は全てそのまま表示されるようになっており、\n使用することはできません">
<tr>
<td colspan="3" style="text-align:center">
<label accesskey="b" for="body">■ 本文(<span class="ak">B</span>) ■</label><br>
<textarea name="body" id="body" class="blur" cols="80" rows="8" style="ime-mode:active;width:500px;" onFocus="this.className='focus'" onBlur="this.className='blur'">$DT{'body'}</textarea>
</td>
</tr>
</tbody>
<tbody>
<tr><td colspan="3" class="wrtfot" title="Submit\n記事を投稿します">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="投稿する">
<!-- <input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="リセット"> -->
</td></tr>
</tbody>
</table>
<script type="text/javascript"><!--
function IconPreview(arg){document.images["Preview"].src="$CF{'icon'}"+arg;}
//--></script>
_CONFIG_

#-----------------------------
# 返信フォーム
$CF{'resfm'}=<<'_CONFIG_';
<table class="write" summary="ResForm">
<col><col><col>
<thead>
<tr><th colspan="3" class="wrttle">
<a name="Form" />$DT{'caption'}
</th></tr>
</thead>
<tbody title="Body\n記事の本文を入力します\n全角約10000文字までです\nタグや文字参照は全てそのまま表示されるようになっており、\n使用することはできません">
<tr>
<td colspan="3" style="text-align:center">
<label accesskey="b" for="body">■ 本文(<span class="ak">B</span>) ■</label><br>
<textarea name="body" id="body" class="blur" cols="80" rows="8" style="ime-mode:active;width:500px;" onFocus="this.className='focus'" onBlur="this.className='blur'">$DT{'body'}</textarea>
</td>
</tr>
</tbody>
<tbody>
<tr title="Name\n名前を入力します（必須）\n最高全角50文字までです">
<th class="item">
<label accesskey="n" for="name">■名前(<span class="ak">N</span>)：</label>
</th>
<td class="input">
<input type="text" name="name" id="name" class="blur" maxlength="50" style="ime-mode:active;width:220px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'name'}">
<label for="cook">Cookie：<input name="cook" id="cook" type="checkbox" checked></label>
</td>
<th class="item" title="Icon\nアイコンを選択します" style="text-align:center">
<label accesskey="i" for="icon">■ <a href="icon.html" title="アイコン一覧" target="_blank">アイコン</a>(<span class="ak">&#8201;I&#8201;</span>) ■</label>
</th>
</tr>
<tr title="e-maiL\nメールアドレスを入力します">
<th class="item">
<label accesskey="l" for="email">■E-mail(<span class="ak">L</span>)：</label>
</th>
<td class="input">
<input type="text" name="email" id="email" class="blur" maxlength="100" style="ime-mode:inactive; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'email'}">
</td>
<td rowspan="4" style="margin:0;text-align:center;vertical-align:middle" title="Icon Preview">
<img alt="Preview" name="Preview" src="$CF{'icon'}$CK{'icon'}">
</td>
</tr>
<tr title="hOme\n自分のサイトを入力します">
<th class="item">
<label accesskey="o" for="home">■ホーム(<span class="ak">O</span>)：</label>
</th>
<td class="input">
<input type="text" name="home" id="home" class="blur" maxlength="80" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'home'}">
</td>
</tr>
<tr title="subJect\n記事の題名を入力します\n最高全角100文字までです">
<th class="item">
<label accesskey="j" for="subject">■題名(<span class="ak">J</span>)：</label>
</th>
<td class="input">
<input type="text" name="subject" id="subject" class="blur" maxlength="70" style="ime-mode:active; width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'subject'}" disabled="disabled">
</td>
</tr>
<tr title="Color\n本文の色を入力します\n（#???、#??????、rgb(???,???,???)、WebColor\nのどれでも使用できます">
<th class="item">
<label accesskey="c" for="color">■色(<span class="ak">C</span>)：</label>
</th>
<td class="input">
<!-- input type="text" name="color" id="color" class="blur" maxlength="20" style="ime-mode:disabled; width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'color'}" -->
<select name="color" id="color">
@{[&color($DT{'color'})]}</select>
&#8194;
<span title="Password\n削除/修正時に使用するパスワードを入力します（必須）\n最高半角24文字までです">
<span class="item">
<label accesskey="p" for="pass">■パスワード(<span class="ak">P</span>)：</label>
</span>
<span class="input">
<input type="password" name="pass" id="pass" class="blur" maxlength="24" style="ime-mode:disabled; font-size:85%;width:90px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'pass'}">
</span>
</span>
</td>
</tr>
<tr title="eXcommand\n専用アイコンを始めとする拡張命令を使う場合に使用します\n普通は使いません">
<th class="item">
<label accesskey="x" for="cmd">■E<span class="ak">X</span>コマンド：</label>
</th>
<td class="input">
<input type="text" name="cmd" id="cmd" class="blur" style="ime-mode:inactive;width:300px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$DT{'command'}">
</td>
<td class="input" title="Icon\nアイコンを選択します">
<select name="icon" id="icon" onchange="IconPreview(this.form['icon'][this.options.selectedIndex].value)">
$main::iconlist</select>
</td>
</tr>
</tbody>
<tbody>
<tr title="Submit\n記事を投稿します"><td colspan="3" class="wrtfot">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="投稿する">
<!-- <input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="リセット"> -->
</td></tr>
</tbody>
</table>
<div class="note" style="width:28em">
■上に表示されているスレッド【No.$DT{'i'}】への返信を行います。<br>
■入力欄において全てのタグは使用できません。<br>
■HTTP, FTP, MAILアドレスのリンクは自動でつきます。<br>
■レスが付いたスレッドは一番上に移動します。<br>
■一般的なブラウザではマウスカーソルを項目の上に置き、<br>
&#8195;&#8201;しばらく待つと項目の簡単な説明が出てきます<br>
■その他、機能の詳細についてはヘルプをご覧ください。<br>
</div>
<script type="text/javascript"><!--
function IconPreview(arg){document.images["Preview"].src="$CF{'icon'}"+arg;}
//--></script>
_CONFIG_



#----------------------------------------------------------------------------------------#
#
# ここからStyle設定部
#

#-------------------------------------------------
#親記事
sub artprt{
  #記事情報を受け取って
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #削除されたら知らせて
  ($DT{'Mir1'}eq'del')&&($DT{'body'}='Mireille: [この記事は削除されました]');
  #記事項目の調整をして
  ($DT{'email'})&&($DT{'name'}=qq{<a href="mailto:$DT{'email'}">$DT{'name'}</a>});
  ($DT{'home'})&&($DT{'home'}=qq{<a href="$DT{'home'}" target="_blank">【HOME】</a>});
  $DT{'date'}=&date($DT{'time'}); #UNIX秒から日付に
  #未読記事に印
  $DT{'new'}='';
  ($DT{'time'}>$CK{'time'})&&($DT{'date'}="<span class=\"new\">$DT{'date'}</span>",$new++);
  ($DT{'time'}>$^T-$CF{'newnc'})&&($DT{'new'}=$CF{'new'});
  #いよいよ出力だよ
  eval qq{print<<"_HTML_";\n$CF{'artprt'}\n_HTML_}; #OLDSTYLE
  #親記事いっちょ上がり
}


#-------------------------------------------------
#子記事
sub artchd{
  #記事情報を受け取って
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #削除されてるときはここの前に飛ばしちゃうの
  #記事項目の調整をして
  ($DT{'email'})&&($DT{'name'}=qq{<a href="mailto:$DT{'email'}">$DT{'name'}</a>});
  ($DT{'home'})&&($DT{'home'}=qq{<a href="$DT{'home'}" target="_blank">【HOME】</a>});
  $DT{'date'}=&date($DT{'time'}); #UNIX秒から日付に
  #未読記事に印
  $DT{'new'}='';
  ($DT{'time'}>$CK{'time'})&&($DT{'date'}="<span class=\"new\">$DT{'date'}</span>",$new++);
  ($DT{'time'}>$^T-$CF{'newnc'})&&($DT{'new'}=$CF{'new'});
  #いよいよ出力だよ
  eval qq{print<<"_HTML_";\n$CF{'artchd'}\n_HTML_}; #OLDSTYLE
  #子記事いっちょ上がり
}


#-------------------------------------------------
#記事フッタ
sub artfot{
  #記事情報を受け取って
  my%DT=(%{shift()},($_=~m/([^\t]*)=\t([^\t]*);\t/go));
  #記事表示？返信モード？
  unless($DT{'res'}){
    #記事表示モードのとき
    eval qq{print<<"_HTML_";\n$CF{'artfot'}\n_HTML_};
  }else{
    #返信モードのとき
    print<<"_HTML_";
</div>
_HTML_
  }
}


#-------------------------------------------------
# 親記事フォーム
#
sub prtfrm{
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}
  
  ($CF{'prtitm'}=~m/\bicon\b/o)&&(&icon($DT{'icon'}));
  
  my$wrtfm=$CF{'wrtfm'};
  chomp$wrtfm;
  if(defined$DT{'body'}){
    $DT{'caption'}='■ 記事修正フォーム ■';
    $DT{'Sys'}.=qq{<input name="i" type="hidden" value="$DT{'i'}">\n};
    $DT{'Sys'}.=qq{<input name="j" type="hidden" value="$DT{'j'}">\n};
    $DT{'Sys'}.=qq{<input name="oldps" type="hidden" value="$DT{'oldps'}">\n};
  }else{
    $DT{'caption'}='■ 新規送信フォーム ■';
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
# 子記事フォーム
#
sub chdfrm{
  #返信フォーム準備
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}

  ($CF{'chditm'}=~m/\bicon\b/o)&&(&icon($DT{'icon'}));

  #デザイン読み込み
  my$resfm=$CF{'resfm'};
  chomp$resfm;#最後の改行を切り落とす
  #追加情報を埋め込む
  $DT{'Sys'}.=qq{<input name="i" type="hidden" value="$DT{'i'}">\n};
  if(defined$DT{'j'}){
    $DT{'Sys'}.=qq{<input name="j" type="hidden" value="$DT{'j'}">\n};
    $DT{'Sys'}.=qq{<input name="oldps" type="hidden" value="$DT{'oldps'}">\n};
    $DT{'caption'}='■ 修正フォーム ■';
    #データを戻す
    $DT{'body'}=~s/<br>/\n/go;#"<br>"2"\n"
    $DT{'body'}=~s/<\/?a[^>]*>//go;#ClearAnchors
    $DT{'body'}=~s/</&#60;/go;
    $DT{'body'}=~s/>/&#62;/go;
  }else{
    $DT{'caption'}='■ 返信フォーム ■';
    $DT{'body'}='';
  }
  ($DT{'Sys'})&&($resfm=~s{<input}{$DT{'Sys'}<input}io);

  #項目の初期設定
  ($DT{'home'})||($DT{'home'}='http://'); #http://だけ入れておく
  #note01:Resは題名ないことも
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
# 投稿日時表示用にフォーマットされた日付取得を返す
sub date{
  my($sec,$min,$hour,$mday,$mon,$year,$wday)=localtime($_[0]);
  #sprintfの説明は、Perlの解説を見てください^^;;
 return sprintf("%4d年%02d月%02d日(%s) %02d時%02d分" #"1970年01月01日(木) 09時00分"の例
 ,$year+1900,$mon+1,$mday,('日','月','火','水','木','金','土')[$wday],$hour,$min);
#  return sprintf("%1d:%01d:%2d %4d/%02d/%02d(%s)" #"9:0: 0 1970/01/01(Thu)"の例
#  ,$hour,$min,$sec,$year+1900,$mon+1,$mday,('Sun','Mon','Tue','Wed','Thu','Fri','Sat')[$wday]);
}


#-------------------------------------------------
# アイコンリスト
#
sub icon{
  #リスト読み込み
  unless(defined$main::iconlist){
    sysopen(RD,'icon.txt',O_RDONLY);#||die"Can't open iconlist." #わざわざエラー返さなくてもいいでしょ
    flock(RD,LOCK_SH);
    $main::iconlist=join('',<RD>);
    close(RD);
  }
  
  #初期設定
  if($_[0]){
    #note02
#    #見つからなければ最後にCookieのものを追加
#    ($icon=~s["$CK{'icon'}"]["$CK{'icon'}" selected="selected"]io)
#     ||($icon.=qq{<option value="$CK{'icon'}" selected="selected">$CK{'icon'}</option>\n});
    #見つからなけければそのまま（普通はブラウザが一番上のアイコンをを選ぶ）
    $main::iconlist=~s{value="$_[0]"}{value="$_[0]" selected="selected"}io;
  }elsif(defined$_[0]){
    ($main::iconlist=~s/value="([^"]*)"/value="([^"]*)" selected="selected"/imo)&&($CK{'icon'}=$2);
  }
}


#-------------------------------------------------
# カラーリスト読み込み
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
# フッター出力
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
