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
<H2 class="heading2">[ HELP &#38; TIPS ]</H2>



<DIV class="section">
<H2 class="h">◇Mireilleの使い方</H2>


<DIV class="section">
<H3 class="h">利用規約</H3>
<P>管理者によって、利用者が掲示板に投稿した記事の著作権が制限されたり、掲示板を通して取得した個人情報を利用したりすることがあります。これらは無断で行われる可能性があります。</P>
<P>具体的には以下の通りになります。（とは言ってもこれ以外のケースも存在しえます。）</P>
<DL class="section">
	<DT>管理者による記事の削除・変更</DT>
	<DD>利用者が不適切な内容の記事を投稿した場合、管理者の判断によって、記事を削除したり、記事の内容を編集することがあります。</DD>
	<DT>管理者による情報の利用</DT>
	<DD>管理者は掲示板における情報を利用者に無断で利用することができます。記事の本文だけでなく、あらゆる統計やその他Cookieのような情報もこれに含まれます。利用者は著作権を始めとした権利をこの場合行使できません。</DD>
	<DT>利用者に対する投稿された記事の信頼性保証等の責任回避</DT>
	<DD>管理者は記事の内容の信憑性に対して責任を持ちません。公共の福祉に反する内容が投稿された場合も誠意ある対応をすることを約束しません。その他この掲示板の利用によって何か損害が出ても管理者は責任を負いません。</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">Mireille特有の仕様</H3>
	<DIV class="section">
	<H4 class="h">記事の削除</H4>
	<P>まず、削除は推奨しません、修正機能を使うことをお勧めします。
	それでも親記事を削除しようとする場合は以下のようになります。</P>
	<UL>
		<LI>親記事だけが存在し、子記事が付いていないものはスレッドごと削除されます。</LI>
		<LI>親記事に子記事が一件でもついている場合は、親記事の本文だけが削除されます。</LI>
		<LI>管理者のみが子記事が付いているスレッドを、スレッドごと削除できます。</LI>
	</UL>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">署名</H4>
	<P>基本的に、署名が同じ人なら同一人物、違えば異なる人物、のはずです。投稿時に使ったパスワードと名前から生成しているので、少しでも名前が変わると違う人物扱いになってしまいます。</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">本文</H4>
	<P>URL系の文字列があると自動的にリンクしてくれます。たとえHTTPなURLでも、httpから書かないようにすれば自動リンクされないようになります。しかし、そうする時は本当に自動リンクされないようにした方がいいのか、良く考えてからにするべきでしょう。</P>
	<P>別項目に示してある強調記号から始まる行や、正規表現にマッチする語句は、書いた時に何らかの形で強調されます。</P>
	<P>ちなみに半角カタカナもたぶん使えます。</P>
	</DIV>
		
	<DIV class="section">
	<H4 class="h">ロック</H4>
	<P>記事が管理者の判断によってロックされることがあります。また、スレッドがそのスレッドの作成者や管理者の判断によりロックされることがあります。ロックされた記事やスレッドは、それ以降変更ができなくなります。</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">NGワード</H4>
	<P>NGワードを含んだ投稿をしてしまうと、エラーが発生します。この場合はNGワードを含まないようにしてから、投稿してください。しかし、これに引っかかってしまうような投稿は、投稿することそのものを考え直したほうがいいかもしれません。</P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">コマンド</H4>
	<P>コマンドは何種類もあるのですが、ここでは良く使われると思われるものだけ取り上げます。</P>
	<DL class="section">
		<DT>icon=<VAR>password</VAR></DT>
		<DD>パスワードを指定して、専用アイコンを使えるようにします。<DD>
		<DT>dnew</DT>
		<DD>修正時に記事の投稿日時を更新します。</DD>
		<DT>znew</DT>
		<DD>修正時にスレッドの最終変更日時を更新します。</DD>
		<DT>renew</DT>
		<DD>修正時に、記事の投稿日時とスレッドの最終変更日時を、共に更新します。</DD>
		<DT>signature=<VAR>seed of signature</VAR></DT>
		<DD>パスワードでなくこれを、署名を生成する際に使う文字列として使うようにします。</DD>
	</DL>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">Quicksave / Quickload</H4>
	<P>本文の内容を一時的に保存することができます。保存できる文字数は使っているブラウザによって異なりますが、日本語を普通に使っている場合だと、InternetExplorerでは数万文字、それ以外では一千文字程度になると思われます。長い文章を投稿する場合は、時々Quicksaveするようにすると、もし送信に失敗したり、ブラウザが急に落ちてしまった時でも、本文の内容が失われずにすみます。同時に保存できるのは一つだけです。<TEXTAREA id="body" style="display:none"></TEXTAREA></P>
	<P><BUTTON class="buttonLoadQuicksave" title="Quicksaveしたデータを削除します" onclick="alert(removeBodyData('MireilleQuicksave'));return false" onkeypress="alert(removeBodyData('MireilleQuicksave'));return false">一時保存したデータを削除</BUTTON></P>
	</DIV>
	
	<DIV class="section">
	<H4 class="h">Autosave</H4>
	<P>本文の内容を自動的に一時保存します。一時保存した内容を読み出すには、投稿フォームのALoadボタンを押してください。いちいち自分でQuicksaveするのが面倒、という人にはとっても便利〜かもしれません。保存可能な文字数など、制限事項はQuicksaveに準じます。ただし、Quicksaveとは別領域に保存しているので、Autosaveによって、Quicksaveした内容が上書きされる、ということはありません。</P>
	<P>この機能について、セキュリティ面から何らかの見解を持つ方の意見を待っています。</P>
	<P><BUTTON class="buttonLoadAutosave" title="Autosaveしたデータを削除します" onclick="alert(removeBodyData('MireilleAutosave'));return false" onkeypress="alert(removeBodyData('MireilleAutosave'));return false">自動保存したデータを削除</BUTTON></P>

	</DIV>
</DIV>


<DIV class="section">
<H3 class="h">現在の設定状況</H3>
	<DIV class="section">
	<H4 class="h">Mireilleの設定</H4>
	<UL>
_HTML_
print<<"_HTML_";
		<LI>投稿後<STRONG>$CF{'newnc'}</STRONG>秒以内の記事に「$CF{'new'}」マークをつける。</LI>
		<LI>読んだ記事でも<STRONG>$CF{'newuc'}</STRONG>秒間は「未読」状態を維持する。</LI>
		<LI>通常モードでは、1ページあたり<STRONG>$CF{'page'}</STRONG>スレッド表示します。</LI>
		<LI>削除・修正モードでは、1ページあたり<STRONG>$CF{'delpg'}</STRONG>スレッド表示します。</LI>
		<LI>新しいものから順に<STRONG>$CF{'logmax'}</STRONG>スレッドが保存されています。</LI>
		<LI>タグは@{[($CF{'tags'})?"<STRONG>$CF{'tags'}</STRONG>を使用できます":'一切使用できません']}。</LI>
		<LI>色は<STRONG>@{[('input'eq$CF{'colway'})?'INPUT':'SELECT']}タグ</STRONG>で選べます。</LI>
		<LI>記事は<STRONG>@{[('date'eq$CF{'sort'})?'投稿日時':'記事番号']}</STRONG>順に表示されます。</LI>
		<LI>相対指定アイコンは<STRONG>使用@{[$CF{'relativeIcon'}?'':'不']}可能</STRONG>です。</LI>
		<LI>絶対指定アイコンは<STRONG>使用@{[$CF{'absoluteIcon'}?'':'不']}可能</STRONG>です。</LI>
		<LI>署名を<STRONG>表示しま@{[$CF{'signature'}?'す':'せん']}</STRONG>。</LI>
_HTML_
#語句強調関連
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
		print"\t\t<LI>$line で始まる行と、<BR>正規表現 $regexp にマッチする語句は強調表示されます。</LI>\n";
	}elsif($line){
		print"\t\t<LI>$line で始まる行は強調表示されます。</LI>\n";
	}elsif($regexp){
		print"\t\t<LI>正規表現 $regexp にマッチする語句は強調表示されます。</LI>\n";
	}else{
		print"\t\t<LI>語句強調はOFFになっています。</LI>\n";
	}
}
#アイコン関連
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
				$icon{$name}=qq(<A href="$4" title="@{['VENDOR'eq$2?'製作者':'一次著作権者']}">$name</A>);
			}elsif('_LINK'eq$3){
				$icon{$name}=$4;
			}
		}
	}
	print"\t\t<LI>$groupグループ、$icons種のアイコンが利用可能です。</LI>\n";
	delete$icon{''};
	(%icon)&&(print"\t\t<LI>".join("、\n",values%icon)."\nが著作権を保有する素材を使用しています。</LI>\n");
}
#クッキー関連
{
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
	<H4 class="h">クッキー関連</H4>
		<FORM action="#" method="get">
		<TABLE cellspacing="2" summary="クッキーの設定" style="margin:0.5em auto 0.5em 1em">
		<TR><TH>あなたのクッキー：</TH>
		<TD><INPUT id="yourCookie" name="yourCookie" type="text" size="100" value="$ENV{'HTTP_COOKIE'}" readonly></TD>
		</TR>
		<TR><TH>Mireille用の内容：</TH>
		<TD><INPUT id="mirCookie" name="mirCookie" type="text" size="100" value="$decoded" readonly></TD>
		</TR>
		<TR><TH>クッキー書き換え：</TH>
		<TD><INPUT id="newCookie" name="newCookie" type="text" size="100" value="$cookie"></TD>
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
	var eNewCookie;
	if(document.all){
		eNewCookie=document.all('newCookie');
		e.returnValue=false;
	}else if(document.getElementById){
		eNewCookie=document.getElementById('newCookie');
		e.preventDefault();
	}else return false;
	e.cancelBubble=true;
	
	if(eNewCookie.value){
		if(confirm('以下のようにMireilleのクッキーを書き換えますがよろしいですか？'
		 +"（仕様上日本語が化けていますが、実際に書き込まれる内容は正常に書き込まれます）\n"
		 +unescape(eNewCookie.value))){
			document.cookie='Mireille='+eNewCookie.value+'; expires=Tue, 19-Jan-2038 03:14:07 GMT; ';//終わりの日
			alert("クッキーを設定しました");
		}
	}else{
		if(confirm('Mireilleのクッキーを削除しますがよろしいですか？')){
			document.cookie='Mireille=; expires=Thu, 01-Jan-1970 00:00:00 GMT; ';//始まりの日
			alert("クッキーを削除しました");
		}
	}
	return true;
}
function resetCookie(e){
	var eNewCookie;
	if(document.all){
		eNewCookie=document.all('newCookie');
		e.returnValue=false;
	}else if(document.getElementById){
		eNewCookie=document.getElementById('newCookie');
		e.preventDefault();
	}else return false;
	e.cancelBubble=true;
	
	var date=new Date();
	eNewCookie.value="time%09"+parseInt(date.getTime()/1000);
	return true;
}


/*========================================================*/
// Remove Body Data
function removeBodyData(key){
	if(!bodyObj)return false;
	if(document.cookie.match(/(^|; )MirBody=([^;]+)/))
		document.cookie='MirBody=; expires=Thu, 01-Jan-1970 00:00:00; ';
	document.cookie=key+'=; expires=Thu, 01-Jan-1970 00:00:00; ';
	if(bodyObj.addBehavior){
		//bahavior版（IE依存）
		if(!bodyObj.getAttribute(key))bodyObj.addBehavior('#default#userData');
		var flag=0;
		var expires=new Date();
		expires.setMonth(expires.getMonth()-1);
		
		bodyObj.load('MireilleQuicksave');
		if(bodyObj.getAttribute('MireilleQuicksave')!=null){
			bodyObj.expires=expires.toUTCString();
			bodyObj.save('MireilleQuicksave');
			flag+=1;
		}
		
		bodyObj.load('MireilleAutosave');
		if(bodyObj.getAttribute('MireilleAutosave')!=null){
			bodyObj.expires=expires.toUTCString();
			bodyObj.save('MireilleAutosave');
			flag+=2;
		}
		
		bodyObj.load('MireilleBody');
		bodyObj.removeAttribute('MireilleBody');
		bodyObj.removeAttribute(key);
		expires.setMonth(expires.getMonth()+2);
		bodyObj.expires=expires.toUTCString();
		bodyObj.save('MireilleBody');
		
		if(flag&1)bodyObj.load('MireilleQuicksave');
		if(flag&2)bodyObj.load('MireilleAutosave');
	}
	if(key=='MireilleQuicksave'){
		return'一時保存されていた本文データを削除しました。';
	}else if(key=='MireilleAutosave'){
		return'自動保存されていた本文データを削除しました。';
	}else{
		return'rbd: Something Wicked happened!';
	}
	return true;
}

var bodyObj=document.all?document.all('body'):document.getElementById?document.getElementById('body'):null;
//-->
</SCRIPT>
		<P>「クッキー書き換え」によって、Mireille用のクッキーを書き換えることができます。新しく来た掲示板に、今まで行っている掲示板のクッキーを移植する、ということも、移植元にない項目のクッキーは移植できませんが、基本的には可能です。</P>
		<P>「Reset」を押すと、未読記事お知らせ機能が効く、最小限のクッキーだけが与えられます。クッキーがない状態から、「Reset」ボタンを押した上で、「OK」を押してクッキーを保存すると、未読記事お知らせ機能は効くようになります。</P>
	</DIV>
</DIV>

<DIV class="section">
<H3 class="h">そのほか</H3>
		<DIV class="section">
		<H4 class="h">一つのスレッドの使いまわしを推奨します</H4>
		<P>この掲示板は一つ一つのスレッドが恐ろしい長さまで伸びる・・・といった使い方を想定して作られています。親記事は3行の文章だけレスは無し、なスレッドがたくさん・・・という使い方は避けたほうがいいかもしれません。（ログ保存方式の都合でオーバーヘッドが増えるかも。。）</P>
		</DIV>
		
		<DIV class="section">
		<H4 class="h">アイコンの最大数</H4>
		<P>理論上は無限です。アイコンを増やしてもあまり処理速度は落ちないようにしているので大丈夫かと。いちおうローカルのテスト環境では700個のアイコンで試してみても数秒で表示されることを確認しました。実際はHTTPの負荷が膨大になり、転送に時間がかかるので難しいとは思いますが^^;;</P>
		</DIV>
		
		<DIV class="section">
		<H4 class="h">なにか・・・</H4>
		<P>この掲示板でおかしいところ、気になるところ、新しく追加して欲しい機能があれば、Airemix <A href="http://www.airemix.com/" title="Airemix" target="_top">http://www.airemix.com/</A> の掲示板に書き込むか、メール(<A href="mailto:naruse&#64;airemix.com">naruse&#64;airemix.com</A>)をください。お気軽にして下さって結構ですので♪</P>
		<P>ちなみにメールをPGP暗号化して送りたい方は、pgp.nic.ad.jpのような公開鍵サーバーで、"Airemix"で検索すると成瀬の公開鍵が手に入りますので、それを使ってください。</P>
		<P>鍵の指紋は「DB DB A4 76 FD BD 94 50 02 CD 0E FC BC E3 C3 88 47 2E C1 EA」です。</P>
		</DIV>
	</DIV>
</DIV>



<DIV class="section">
<H2 class="h">◇アクセスキー</H2>
<P>Mireilleにはアクセス性を向上させるための「アクセスキー」が設定されています。</P>
<P>これはWindowsでいう「ショートカットキー」のようなもので、覚えなければいけない訳ではありませんが、使えると便利かもしれません。</P>
<P>どのようなものが設定されているか知りたいという、暇人・・・もとい奇特な方のために以下に主なものを挙げておきます。</P>


<DIV class="section">
<H3 class="h">Index画面のとき</H3>
<DL>
	<DT><KBD>Alt+[1-9]</KBD></DT>
	<DD>そのページ内の上から[1-9]番目の記事の、返信へのリンクが選択されます。ブラウザによっては、その記事に対する返信画面に移動します。</DD>
	<DT><KBD>Alt+Shift+[1-9]</KBD></DT>
	<DD>[1-9]ページ目へのリンクが選択されます。ブラウザによっては、そのまま選択ページへ移動します。</DD>
	<DT><KBD>Alt+[,.]</KBD></DT>
	<DD><KBD>,</KBD> で新しい記事のあるページ、<KBD>.</KBD> で昔の記事のあるページのリンクが選択されます。ブラウザによっては、そのままページを移動します。JISキーボードを使っている方でしたらこのキー選択の意味がわかるかもしれません。</DD>
	<DT><KBD>Alt+M</KBD></DT>
	<DD>記事ナビを 最大化/タイトル化 します。</DD>
	<DT><KBD>Alt+C</KBD></DT>
	<DD>記事ナビを閉じます。</DD>
	<DT><KBD>Alt+N</KBD></DT>
	<DD>記事ナビを開きます。</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">投稿画面のとき</H3>
<DL>
	<DT><KBD>Alt+J</KBD></DT><DD>「題名」にカーソルが移ります。</DD>
	<DT><KBD>Alt+N</KBD></DT><DD>「名前」にカーソルが移ります。</DD>
	<DT><KBD>Alt+K</KBD></DT><DD>「Cookie」にカーソルが移ります。</DD>
	<DT><KBD>Alt+I</KBD></DT><DD>「アイコン」にカーソルが移ります。</DD>
	<DT><KBD>Alt+L</KBD></DT><DD>「E-mail」にカーソルが移ります。</DD>
	<DT><KBD>Alt+O</KBD></DT><DD>「ホーム」にカーソルが移ります。</DD>
	<DT><KBD>Alt+B</KBD></DT><DD>「本文」にカーソルが移ります。</DD>
	<DT><KBD>Alt+C</KBD></DT><DD>「色」にカーソルが移ります。</DD>
	<DT><KBD>Alt+P</KBD></DT><DD>「パスワード」にカーソルが移ります。</DD>
	<DT><KBD>Alt+M</KBD></DT><DD>「コマンド」にカーソルが移ります。</DD>
	
	<DT><KBD>Alt+,</KBD></DT><DD>Quicksaveします。</DD>
	<DT><KBD>Alt+.</KBD></DT><DD>Quickloadします。</DD>
	<DT><KBD>Alt+/</KBD></DT><DD>Autosaveした内容を読み出します。</DD>
	
	<DT><KBD>Alt+S</KBD></DT><DD>フォームの内容を送信します。</DD>
</DL>
</DIV>


<DIV class="section">
<H3 class="h">その他のとき</H3>
<DL>
	<DT><KBD>Alt+S</KBD></DT><DD>決定/送信します。</DD>
	<DT><KBD>Alt+R</KBD></DT><DD>フォームの内容をリセットします。</DD>
</DL>
</DIV>
</DIV>



<DIV class="section">
<H2 class="h">◇<A name="お世話になったところ">お世話になったところ</A></H2>
<DL>
<DT>Academic HTML &lt;<a href="http://www.tg.rim.or.jp/~hexane/ach/">http://www.tg.rim.or.jp/~hexane/ach/</A>&gt;</DT>
<DD>HTML/CSSに関する的確な情報がたくさんあります。HTML/CSSを一通り学びたい場合はここを見るだけで事足りてしまいます。</DD>
<DT>Another HTML-lint &lt;<a href="http://openlab.ring.gr.jp/k16/htmllint/">http://openlab.ring.gr.jp/k16/htmllint/</A>&gt;</DT>
<DD>HTMLの検証に際し利用しました。初めてチェックすると、ほとんどの人がショックを受けることでしょう。</DD>
<DT>ARTEMIS &lt;<a href="http://www.artemis.ac/arrange/">http://www.artemis.ac/arrange/</A>&gt;</DT>
<DD>IconPreviewはここからです、便利なので頂きました。新しい投稿があると教えてくれる〜もここのを見て、です。他にもいろいろと参考にしています。管理機能でここを見習う点は数多くあります。</DD>
<DT>HTML鳩丸倶楽部 &lt;<a href="http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru">http://www.ne.jp/asahi/minazuki/bakera/html/hatomaru</A>&gt;</DT>
<DD>ツッコミメインなHTML解説サイト、にわたしは見えました。「HTML 4.01 のみを、純粋に学問的な興味から研究」しているそうです。HTMLの構成に際して参考にしました。</DD>
<DT>jcode.pl &lt;<a href="http://www.srekcah.org/jcode/">http://www.srekcah.org/jcode/</A>&gt;</DT>
<DD>漢字コード変換用のライブラリです。Mireille本体では横着しているので使っていません。管理CGIでは一部を切り出して使っています。</DD>
<DT>KNET-WEB &lt;<a href="http://www.kent-web.com/">http://www.kent-web.com/</A>&gt;</DT>
<DD>なにはともあれ日本のCGI/Perl界に与えた影響は少なくはないはずです。私個人では特にYYBOARDとYYCHATにはお世話になりました。きわめてとっつき易いCGIが多いです。</DD>
<DT>Perlメモ &lt;<a href="http://www.din.or.jp/~ohzaki/perl.htm">http://www.din.or.jp/~ohzaki/perl.htm</A>&gt;</DT>
<DD>URI自動リンク機能をつけるに際し参考に・・・むしろ丸写しです。Perlの正規表現に関してとても有用な情報があります。</DD>
<DT>W3C HTML Validation Service &lt;<a href="http://validator.w3.org/">http://validator.w3.org/</A>&gt;</DT>
<DD>HTML規格の策定を行う団体、W3CによるHTML検証サービスです。Another HTML-lintよりチェック項目は少なめです。</DD>
<DT>とほほのWWW入門 &lt;<a href="http://tohoho.wakusei.ne.jp/">http://tohoho.wakusei.ne.jp/</A>&gt;</DT>
<DD>HTML部、Perl部ともに時々リファレンス代わりにしました。なかなか載っていて便利です。</DD>
<DT>彼の野原 &lt;<a href="http://kano.feena.jp/">http://kano.feena.jp/</A>&gt;</DT>
<DD>LastPostはここのealisの真似です。また1.2.2の記事ナビは神乃さんのものベースに作りました。今はPerlからPHPに力点を移した模様。ヰキはじめました？</DD>
<DT>SWORD AND COMMERCE &lt;<a href="http://www10.plala.or.jp/ryokufuudou/kijindou.html">http://www10.plala.or.jp/ryokufuudou/kijindou.html</A>&gt;</DT>
<DD>retroさんにはMireilleでつまづく所No.1と思われるアイコン設定の解説を書いていただきました。他にもMireilleの解説の不備な点を多数してもらいました。ちなみに、retroさんのサイト自体はRagnarkOnline系雑談サイトです。</DD>
<DT>Snowish Hills &lt;<DEL>http://snowish.cside8.com/</DEL>&gt;</DT>
<DD>Mireilleを作りこむにあたって、半ばオンサイト顧客として、数々の有用なアドバイスを頂きました。特に管理CGIは西名さんに言われなければ、かなり貧弱なものになっていたでしょう。現在の初期状態のデザインも西名さんのデザインをベースにしています。ちなみに、西名さんのサイト自体はKey系CGサイトでした。</DD>
</DL>
<P>他にも意見を下さった方々、参考にしたサイト・CGIの作者さんに感謝します。</P>
</DIV>

<P class="note">この説明では&trade;や&reg;や&copy;マークは省略しています。<BR>
それぞれのサイト名やソフトウェア名などは各々の商標や登録商標などです。</P>

<P class="note">この掲示板は、Microsoft Internet Explorer for Windows バージョン5以上を主とした対象とし、<BR>
Windows版InternetExplorer6と、NetscapeやMozilla FirebirdなどのMozilla系で、ほぼ完全な動作をします。<BR>
またOpera7やMicrosoft Internet Explorer 5 for Macintoshでも概ね期待通りの動作をするはずです。<BR>
上記のブラウザ以外では動作はするはずですが、見辛くなってしまう可能性があります。<BR>
ご了承くださいまし。 （但し、読み書きができない場合はMireilleのバグです）</P>
_HTML_
print<<"_HTML_".&getFooter;
<DIV align="center" class="note" style="width:15em">
<P class="heading4" style="text-align:center">■　バージョン情報　■</P>
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
