#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Help Module -
#
$CF{'Help'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." 空
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
<H2 class="list">◇Mireilleの使い方</H2>
<UL>
	<LI><H3 class="list">利用規約</H3>
		管理者によって、利用者が掲示板に投稿した記事の著作権が制限されたり、<BR>
		掲示板を通して取得した個人情報を利用したりすることがあります。<BR>
		これらは無断で行われる可能性があります。<BR>
		具体的には、<BR>
		<UL>
			<LI>管理者による記事の削除・変更<BR>
				利用者が不適切な内容の記事を投稿した場合、管理者の判断によって、記事を削除したり、<BR>
				記事の内容を編集することがあります。</LI>
			<LI>管理者による情報の利用<BR>
				管理者は掲示板における情報を利用者に無断で利用することができます。<BR>
				記事の本文だけでなく、あらゆる統計やその他Cookieのような情報もこれに含まれます。<BR>
				利用者は著作権を始めとした権利をこの場合行使できません。</LI>
			<LI>利用者に対する投稿された記事の信頼性保証等の責任回避<BR>
				管理者は記事の内容の信憑性に対して責任を持ちません。<BR>
				公共の福祉に反する内容が投稿された場合も誠意ある対応をすることを約束しません。<BR>
				その他この掲示板の利用によって何か損害が出ても管理者は責任を負いません</LI>
		</UL>
	</LI>
	<LI><H3 class="list">Mireille特有の仕様</H3>
		<UL>
			<LI>記事の削除<BR>
				まず、削除は推奨しません。修正機能を使うことをお勧めします。<BR>
				親記事を削除しようとする場合、<BR>
				・親記事だけが存在し、子記事が付いていないものはスレッドごと削除されます。<BR>
				・親記事だけでなく、子記事が一件でもついている場合は本文だけが削除されます。<BR>
				・管理者のみが子記事が付いているスレッドを、スレッドごと削除できます。</LI>
			<LI>本文<BR>
				URLを探して、自動的にリンクしてくれますので、ぜひご活用ください。<BR>
				下に示してある強調記号から始まる行は、書いた時に何らかの形で語句が強調されます<BR>
				それ以外にも語句が強調されることがあります
				ちなみに半角カタカナもたぶん使えます</LI>
			<LI>コマンド<BR>
				現在は専用アイコンのパスワードを入れるのに使っています。<BR>
				形式は&#34;icon=password&#34;となっています。<BR>
				専用アイコンが欲しい方は、管理人さんに交渉してみましょう。</LI>
		</UL>
	</LI>
	<LI><H3 class="list">現在の設定状況</H3>
		<UL>
_HTML_
print<<"_HTML_";
			<LI>投稿後<STRONG>$CF{'newnc'}</STRONG>秒以内の記事にNewマークをつける</LI>
			<LI>読んだ記事でも<STRONG>$CF{'newuc'}</STRONG>秒間は「未読」状態を維持する</LI>
			<LI>通常モードでは、1ページあたり<STRONG>$CF{'page'}</STRONG>スレッド表示します</LI>
			<LI>削除・修正モードでは、1ページあたり<STRONG>$CF{'delpg'}</STRONG>スレッド表示します</LI>
			<LI>新しいものから順に<STRONG>$CF{'logmax'}</STRONG>スレッドが保存されています</LI>
			<LI>タグは@{[($CF{'tags'})?"<STRONG>$CF{'tags'}</STRONG>を使用できます":'一切使用できません']}</LI>
			<LI>色は<STRONG>@{[('input'eq$CF{'colway'})?'INPUT':'SELECT']}タグ</STRONG>で選べます</LI>
			<LI>記事は<STRONG>@{[('date'eq$CF{'sort'})?'投稿日時':'記事番号']}</STRONG>順に表示されます</LI>
_HTML_
#語句強調関連
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
		print"\t\t\t<LI>$line から始まる行と、<BR>正規表現 $regexp にマッチする文字列は強調表示されます</LI>\n";
	}elsif($line){
		print"\t\t\t<LI>$line から始まる行は強調表示されます</LI>\n";
	}elsif($regexp){
		print"\t\t\t<LI>正規表現 $regexp にマッチする文字列は強調表示されます</LI>\n";
	}else{
		print"\t\t\t<LI>文字列は強調表示されません</LI>\n";
	}
}
#アイコン関連
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
				$icon{$name}=qq(<A href="$4" title="@{['VENDOR'eq$2?'製作者':'一次著作権者']}">$name</A>);
			}elsif('_LINK'eq$3){
				$icon{$name}=$4;
			}
		}
	}
	print"\t\t\t<LI>$groupグループ、$icons個のアイコンが利用可能です</LI>\n";
	delete$icon{''};
	(%icon)&&(print"\t\t\t<LI>".join("、\n",values%icon)."\nが著作権を保有する素材を使用しています。</LI>\n");
}
#クッキー関連
{
	my$ascii='[\x0A\x0D\x20-\x7E]'; # 1バイト EUC-JP文字改-\x09
	my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2バイト EUC-JP文字
	my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3バイト EUC-JP文字
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
			<LI>クッキー関連<BR><FORM action="#" method="get">
			あなたのクッキー：<INPUT id="yourCookie" name="yourcookie" type="text"
			 size="100" value="$ENV{'HTTP_COOKIE'}" readonly><BR>
			Mireille用の内容：<INPUT id="mirCookie" name="mirCookie" type="text"
			 size="100" value="$decoded" readonly><BR>
			クッキー書き換え：<INPUT id="cookiedata" name="cookiedata" type="text"
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
		if(confirm('以下のようにMireilleのクッキーを書き換えますがよろしいですか？'
		 +"（仕様上日本語が化けていますが、実際に書き込まれる内容は正常に書き込まれます）\n"+unescape(cookie))){
			document.cookie='Mireille='+cookie+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//終わりの日
			alert("クッキーを設定しました");
		}
	}else{
		if(confirm('Mireilleのクッキーを削除しますがよろしいですか？')){
			document.cookie='Mireille=; expires=Thu, 01-Jan-1970 00:00:00 GMT; ';//始まりの日
			alert("クッキーを削除しました");
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
			「クッキー書き換え」によって、Mireille用のクッキーを書き換えることができます<BR>
			新しく来た掲示板に、今まで行っている掲示板のクッキーを移植する、ということも、<BR>
			移植元にない項目のクッキーは移植できませんが、基本的には可能です<BR>
			<BR>
			「Reset」を押すと、未読記事お知らせ機能が効く、最小限のクッキーだけが与えられます<BR>
			クッキーがない状態から、「Reset」「OK」でクッキーを保存すると、未読記事お知らせ機能は効くようになります</LI>
		</UL>
	</LI>
	<LI><H3 class="list">そのほか</H3>
		<UL>
			<LI>一つのスレッドの使いまわしを推奨します<BR>
				この掲示板は一つ一つのスレッドが恐ろしい長さまで伸びる・・・<BR>
				といった使い方を想定して作られています。<BR>
				親記事は3行の文章だけレスは無し、なスレッドがたくさん・・・<BR>
				という使い方は避けたほうがいいかもしれません<BR>
				（ログ保存方式の都合でオーバーヘッドが増えるかも。。）</LI>
			<LI>アイコンの最大数<BR>
				理論上は無限です。<BR>
				アイコンを増やしてもあまり処理速度は落ちないようにしているので大丈夫かと。<BR>
				いちおうローカルのテスト環境では700個のアイコンで試してみても数秒で表示されることを確認しました。<BR>
				実際はHTTPの負荷が膨大になり、転送に時間がかかるので難しいとは思いますが^^;;</LI>
			<LI>なにか・・・<BR>
				この掲示板でおかしいところ、気になるところ、新しく追加して欲しい機能があれば、<BR>
				Airemix <A href="http://www.airemix.com/" title="Airemix" target="_top">http://www.airemix.com/</A>
				の掲示板に書き込むか、
				メール(<A href="mailto:naruse&#64;airemix.com">naruse&#64;airemix.com</A>)をください<BR>
				お気軽にして下さって結構ですので♪<BR>
				<BR>
				ちなみにメールをPGP暗号化して送りたい方は、pgp.nic.ad.jpのような公開鍵サーバーで、<BR>
				"Airemix"で検索すると成瀬の公開鍵が手に入りますので、それを使ってください<BR>
				鍵の指紋は「DB DB A4 76 FD BD 94 50 02 CD 0E FC BC E3 C3 88 47 2E C1 EA」です<BR>
				</LI>
		</UL>
	</LI>
</UL>
</DIV>

<DIV class="hthread">
<H2 class="list">◇アクセスキー</H2>
<UL>
	<LI>Mireilleにはアクセス性を向上させるための「アクセスキー」を設定しています。<BR>
		これはWindowsでいう「ショートカットキー」のようなものです<BR>
		覚えなければいけない訳ではありませんが、使えると便利かもしれません</LI>
	<LI><H3 class="list">Index画面のとき</H3>
		<DL>
			<DT><KBD>Alt+[1-9]</KBD></DT>
			<DD>そのページ内の上から[1-9]番目の記事の、返信へのリンクが選択されます</DD>
			<DT><KBD>Alt+Shift+[1-9]</KBD></DT>
			<DD>[1-9]ページ目へのリンクに移動します</DD>
			<DT><KBD>Alt+[,.]</KBD></DT>
			<DD><KBD>,</KBD> だと後のページに、<KBD>.</KBD> だと古いページへ移動します<BR>
			JISキーボードを使っている方でしたらこのキー選択の意味がわかるかもしれません</DD>
		</DL>
	</LI>
	<LI><H3 class="list">投稿画面のとき</H3>
		<DL>
			<DT><KBD>Alt+J</KBD></DT><DD>「題名」にカーソルが移ります</DD>
			<DT><KBD>Alt+N</KBD></DT><DD>「名前」にカーソルが移ります</DD>
			<DT><KBD>Alt+K</KBD></DT><DD>「Cookie」にカーソルが移ります</DD>
			<DT><KBD>Alt+I</KBD></DT><DD>「アイコン」にカーソルが移ります</DD>
			<DT><KBD>Alt+L</KBD></DT><DD>「E-mail」にカーソルが移ります</DD>
			<DT><KBD>Alt+O</KBD></DT><DD>「ホーム」にカーソルが移ります</DD>
			<DT><KBD>Alt+B</KBD></DT><DD>「本文」にカーソルが移ります</DD>
			<DT><KBD>Alt+C</KBD></DT><DD>「色」にカーソルが移ります</DD>
			<DT><KBD>Alt+P</KBD></DT><DD>「パスワード」にカーソルが移ります</DD>
			<DT><KBD>Alt+M</KBD></DT><DD>「コマンド」にカーソルが移ります</DD>
			
			<DT><KBD>Alt+S</KBD></DT><DD>フォームの内容を送信します</DD>
		</DL>
	</LI>
	<LI><H3 class="list">その他のとき</H3>
		<DL>
			<DT><KBD>Alt+S</KBD></DT><DD>決定/送信します</DD>
			<DT><KBD>Alt+R</KBD></DT><DD>フォームの内容をリセットします</DD>
		</DL>
	</LI>
</UL>
</DIV>

<DIV class="hthread" style="text-align:left">
<H2 class="list"><A name="お世話になったところ">◇お世話になったところ</A></H2>
<UL>
<LI><H3 class="list"><A href="http://www.tg.rim.or.jp/~hexane/ach/" title="Academic HTML">Academic HTML</A></H3>
HTML,CSSに関する的確な情報がたくさんあります<BR>
HTML,CSSを一通り学びたい場合はここを見るだけで事足りてしまいます</LI>
<LI><H3 class="list"><A href="http://openlab.ring.gr.jp/k16/htmllint/" title="Another HTML-lint">Another HTML-lint</A></H3>
HTMLの検証に際し利用しました<BR>
初めてチェックすると、ほとんどの人がショックを受けることでしょう</LI>
<LI><H3 class="list"><A href="http://www.artemis.ac/arrange/" title="ARTEMIS">ARTEMIS</A></H3>
IconPreviewはここからです、便利なので頂きましたｗ<BR>
新しい投稿があると教えてくれる〜もここのを見て、です<BR>
他にもいろいろと参考にしています<BR>
管理機能でここを見習う点は数多くあります</LI>
<LI><H3 class="list"><A href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru" title="HTML鳩丸倶楽部">HTML鳩丸倶楽部</A></H3>
ツッコミメインなHTML解説サイト、にわたしは見えました<BR>
「HTML 4.01 のみを、純粋に学問的な興味から研究」しているそうです<BR>
HTMLの構成に際して参考にしました</LI>
<LI><H3 class="list"><A href="http://www.srekcah.org/jcode/" title="jcode.pl">jcode.pl</A></H3>
漢字コード変換用のライブラリです<BR>
Mireille本体では横着しているので使っていません<BR>
管理CGIでは一部を切り出して使っています</LI>
<LI><H3 class="list"><A href="http://openlab.ring.gr.jp/Jcode/index-j.html" title="Jcode.pm">Jcode.pm</A></H3>
jcode.plの後継でPerl5用PerlModuleとなっています<BR>
jcode.plの機能にUnicodeを扱う機能が追加されています<BR>
Perl5.8ではEncodeモジュールに置換されているようです</LI>
<LI><H3 class="list"><A href="http://www.kent-web.com/" title="KNET-WEB">KENT-WEB</A></H3>
なにはともあれ日本のCGI/Perl界に与えた影響は少なくはないはずです<BR>
私個人では特にYYBOARD,YYCHATにはお世話になりました<BR>
きわめてとっつき易いCGIが多いです</LI>
<LI><H3 class="list"><A href="http://www.din.or.jp/~ohzaki/perl.htm" title="Perlメモ">Perlメモ</A></H3>
URI自動リンク機能をつけるに際し参考に・・・むしろ丸写しです<BR>
Perlの正規表現に関してとても有用な情報があります</LI>
<LI><H3 class="list"><A href="http://validator.w3.org/" title="W3C HTML Validation Service">W3C HTML Validation Service</A></H3>
HTML規格の策定を行う団体、W3CによるHTML検証サービスです<BR>
Another HTML-lintよりチェック項目は少なめです</LI>
<LI><H3 class="list"><A href="http://tohoho.wakusei.ne.jp/" title="とほほのWWW入門">とほほのWWW入門</A></H3>
HTML部、Perl部ともに時々リファレンス代わりにしました<BR>
なかなか載っていて便利です</LI>
<LI><H3 class="list"><A href="http://kano.feena.jp/" title="彼の野原">彼の野原</A></H3>
LastPostはここのealisの真似です<BR>
また1.2.2の記事ナビは神乃さんのものベースに作りました<BR>
最近ではPHPに移ってあるべき姿というものを模索していらっしゃるようです</LI>
<LI><H3 class="list"><A href="http://www10.plala.or.jp/ryokufuudou/kijindou.html" title="SWORD AND COMMERCE">SWORD AND COMMERCE</A></H3>
retroさんにはMireilleでつまづく所No.1と思われるアイコン設定の解説を書いていただきました<BR>
他にもMireilleの解説の不備な点を多数してもらいました<BR>
ちなみに、retroさんのサイト自体はRagnarkOnline系雑談サイトです</LI>
<LI><H3 class="list"><A href="http://snowish.cside8.com/" title="Snowish Hills">Snowish Hills</A></H3>
Mireilleを作りこむにあたって、半ばオンサイト顧客として、数々の有用なアドバイスを頂きました<BR>
特に管理CGIは西名さんに言われなければ、かなり貧弱なものになっていたでしょう<BR>
現在の初期状態のデザインも西名さんのデザインをベースにしています<BR>
ちなみに、西名さんのサイト自体はKey系CGサイトです</LI>
<LI>他にも意見を下さった方々、参考にしたサイト・CGIの作者さんに感謝します</LI>
</UL>
</DIV>

<P class="note">この説明では&trade;や&reg;や&copy;マークは省略しています<BR>
それぞれのサイト名やソフトウェア名などは各々の商標や登録商標などです</P>
<P align="center" class="note" style="margin-bottom:2em;width:600px">
この掲示板は、Microsoft Internet Explorer 5以上を主とした対象とし、<BR>
Microsoft Internet Explorer 6において完全な動作をします。<BR>
Netscape 6及びMozilla 0.8以降でもほぼ期待通りの動作をすることを確認済みです。<BR>
以上のブラウザ以外では動作はしますが、見苦しくなってしまいます。ご了承ください。</P>
_HTML_
print<<"_HTML_".&getFooter;
<DIV align="center" class="note" style="width:15em;">
<H4 class="list" style="text-align:center">■　バージョン情報　■</H4>
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
