#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Help File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
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
<h2 class="ul">◇Mireilleの使い方</h2>
<ul style="margin-top:0px">
 <li><h3 class="ul">書き込むとき</h3>
  <ul class="list">
   <li>本文<br>
    タグや文字参照は変換されて、全てそのまま表示されます。<br>
    URLについてを探して、自動的にリンクしてくれますので、ぜひご活用ください。<br>
    ちなみに半角カタカナもたぶん使えます</li>
   <li>EXコマンド<br>
    現在は専用アイコンのパスワードを入れるのに使っています。<br>
    形式は&#34;icon=password&#34;となっています。<br>
    専用アイコンが欲しい方は、管理人さんに交渉してみましょう。</li>
  </ul>
 </li>
 <li><h3 class="ul">現在の設定状況</h3>
  <ul class="list">
_HTML_

    my@info=(
 'tags'  =>'使用を許可するタグ'
,'newnc' =>'投稿後*****秒以内の記事にNewマークをつける'
,'newuc' =>'読んだ記事でも???秒間は「未読」状態を維持する'
,'page'  =>'通常モードでの1ページあたりのスレッド数'
,'delpg' =>'削除・修正モードでの1ページあたりのスレッド数'
,'logmax'=>'最大スレッド数'
,'colway'=>'色の選択方法'
,'sort'  =>'記事の並び順'
);

#    my($key=>$val)=('','');
    #稼動させる前に確認すること
    while(my($key=>$val)=(shift@info,shift@info)){
      $key||last;
      print qq(    <li><span style="width:350px">$val：</span>$CF{$key}</li>);
    }

print<<'_HTML_';
  </ul>
 </li>
 <li><h3 class="ul">そのほか</h3>
  <ul class="list">
   <li>一つのスレッドの使いまわしを推奨します<br>
    この掲示板は一つ一つのスレッドが恐ろしい長さまで伸びる・・・<br>
    といった使い方を想定して作られています。<br>
    3行の文章だけのスレッドがたくさん・・・<br>
    という使い方は避けたほうがいいかもしれません</li>
   <li>アイコンの最大数<br>
    理論上は無限です。<br>
    アイコンを増やしてもあまり処理速度は落ちないようにしているので大丈夫かと。<br>
    いちおう700個のアイコンで試してみても数秒で表示されることを確認しました。
    実際はHTTPの負荷が膨大になるので難しいとは思いますが^^;;</li>
   <li>なにか・・・<br>
    この掲示板でおかしいところ、気になるところ、新しく追加して欲しい機能があれば、<br>
    Airemix <a href="http://airemix.site.ne.jp/" title="Airemix">http://airemix.site.ne.jp/</a>
    の掲示板に書き込むか、<br>
    メール(<a href="mailto:naruse@airemix.site.ne.jp">naruse@airemix.site.ne.jp</a>)をください<br>
    お気軽にして下さって結構ですので♪</li>
  </ul>
 </li>
</ul>
</div>

<div class="hthread" style="text-align:left">
<h2 class="ul">◇アクセスキー</h2>
<ul style="margin-top:0px">
 <li>Mireilleにはアクセス性を向上させるための「アクセスキー」を設定しています。<br>
 これはWidnowsでいう「ショートカットキー」のようなものです<br>
 覚えるなければいけない訳ではありませんが、使えると便利かもしれません</li>
 <li><h3 class="ul">Index画面のとき</h3>
  <ul class="list">
   <li>Alt+[1-9]<br>
   そのページ内の上から[1-9]番目の記事の、返信へのリンクが選択されます</li>
   <li>Alt+Shift+[1-9]<br>
   [1-9]ページ目へのリンクに移動します</li>
   <li>Alt+[,.]<br>
   &#34;,&#34;だと後のページに、&#34;.&#34;だと古いページへ移動します<br>
   JISキーボードを使っている方でしたらこのキー選択の意味がわかるかもしれません</li>
  </ul>
 </li>
 <li><h3 class="ul">投稿画面のとき</h3>
  <ul class="list">
   <li>Alt+J<br>「題名」フォームにカーソルが移ります</li>
   <li>Alt+N<br>「名前」フォームにカーソルが移ります</li>
   <li>Alt+I<br>「アイコン」フォームにカーソルが移ります</li>
   <li>Alt+L<br>「E-mail」フォームにカーソルが移ります</li>
   <li>Alt+O<br>「ホーム」フォームにカーソルが移ります</li>
   <li>Alt+B<br>「本文」フォームにカーソルが移ります</li>
   <li>Alt+C<br>「色」フォームにカーソルが移ります</li>
   <li>Alt+P<br>「パスワード」フォームにカーソルが移ります</li>

   <li>Alt+S<br>フォームの内容を送信します</li>
  </ul>
 </li>
 <li><h3 class="ul">その他のとき</h3>
  <ul class="list">
   <li>Alt+S<br>決定/送信します</li>
   <li>Alt+R<br>フォームの内容をリセットします</li>
  </ul>
 </li>
</ul>
</div>

<div class="hthread" style="text-align:left">
<h2 class="ul">◇お世話になったところ</h2>
<ul>
<li><h3 class="ul"><a href="http://www.tg.rim.or.jp/~hexane/ach/" title="Academic HTML">Academic HTML</a></h3>
HTML,CSSに関する的確な情報がたくさんあります<br>
HTML,CSSを一通り学びたい場合はここを見るだけで事足りてしまいます</li>
<li><h3 class="ul"><a href="http://openlab.ring.gr.jp/k16/htmllint/" title="Another HTML-lint">Another HTML-lint</a></h3>
HTMLの検証に際し利用しました<br>
初めてチェックすると、ほとんどの人がショックを受けることでしょう</li>
<li><h3 class="ul"><a href="http://www.artemis.ac/arrange/" title="ARTEMIS">ARTEMIS</a></h3>
IconPreviewはここからです、便利なので頂きましたｗ<br>
新しい投稿があると教えてくれる〜もここのを見て、です<br>
他にもいろいろと参考にしています<br>
管理機能でここを見習う点は数多くあります</li>
<li><h3 class="ul"><a href="http://kano.vis.ne.jp/erial/" title="elialarts.">erialarts.</a></h3>
LastPostはここのealisの真似です<br>
1.2.2の記事ナビは神乃さんのものベースに作りました<br>
DHTML周りではかないません^^;;<br>
tableを使わずに表示させようとしているのも尊敬します</li>
<li><h3 class="ul"><a href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru" title="HTML鳩丸倶楽部">HTML鳩丸倶楽部</a></h3>
ツッコミメインなHTML解説サイト、にわたしは見えました<br>
「HTML 4.01 のみを、純粋に学問的な興味から研究」しているそうです<br>
HTMLの構成に際して参考にしました</li>
<li><h3 class="ul"><a href="http://www.srekcah.org/jcode/" title="jcode.pl">jcode.pl</a></h3>
漢字コード変換用のライブラリです<br>
Mireille本体では横着しているので使っていません<br>
管理CGIでは一部を切り出して使っています</li>
<li><h3 class="ul"><a href="http://openlab.ring.gr.jp/Jcode/index-j.html" title="Jcode.pm">Jcode.pm</a></h3>
jcode.plの後継でPerl5用PerlModuleとなっています<br>
jcode.plの機能にUnicodeを扱う機能が追加されています</li>
<li><h3 class="ul"><a href="http://www.kent-web.com/" title="KNET-WEB">KENT-WEB</a></h3>
なにはともあれ日本のCGI/Perl界に与えた影響は少なくはないはずです<br>
私個人では特にYYBOARD,YYCHATにはお世話になりました<br>
きわめてとっつき易いCGIが多いです</li>
<li><h3 class="ul"><a href="http://www.din.or.jp/~ohzaki/perl.htm" title="Perlメモ">Perlメモ</a></h3>
URI自動リンク機能をつけるに際し参考に・・・むしろ丸写しです<br>
Perlの正規表現に関してとても有用な情報があります</li>
<li><h3 class="ul"><a href="http://validator.w3.org/" title="W3C HTML Validation Service">W3C HTML Validation Service</a></h3>
HTML規格の策定を行う団体、W3CによるHTML検証サービスです<br>
Another HTML-lintよりチェック項目は少なめです</li>
<li><h3 class="ul"><a href="http://wakusei.cplaza.ne.jp/twn/www.htm" title="とほほのWWW入門">とほほのWWW入門</a></h3>
HTML部、Perl部ともに時々リファレンス代わりにしました<br>
なかなか載っていて便利です<br>
それでも一部省略されているのが残念ですが、、</li>
<li><h3 class="ul"><a href="http://snowish.cside8.com/" title="Snowish Hills">Snowish Hills</a></h3>
Mireilleを作りこむにあたって、有用なアドバイスを多数頂きました<br>
特に管理機能は西名さんに言われなければかなり貧弱なものになっていたでしょう<br>
初期状態のデザインも西名さんのデザインをベースにしています<br>
ちなみに、西名さんのサイト自体はKey系CGサイトです</li>
<li>他にも意見を下さった方々、参考にしたサイト・CGIの作者さんに感謝します</li>
</ul>
</div>

<pre style="margin:1em auto;text-align:center;width:600px">
この掲示板は、Microsoft Internet Explorer 5以上を主とした対象とし、
Microsoft Internet Explorer 6において完全な動作をします。
Netscape 6及びMozilla 0.8以降でもほぼ期待通りの動作をすることを確認済みです。
以上のブラウザ以外では動作はしますが、見苦しくなってしまいます。ご了承ください。</pre>
_HTML_
print<<"_HTML_";
<div class="note" style="width:15em;">
<pre>
　■　バージョン情報　■
■Index: $CF{'Index'}
■Core: $CF{'Core'}
■Style: $CF{'Style'}
■Help : $CF{'Help'}
</pre>
</div>
_HTML_
&footer;

1;
__END__
