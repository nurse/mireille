#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Core File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
use strict;
use vars qw(%CF %IC %IN %CK %Z0 @zer2 @file);

=item core.cgiを単体起動させると、locationで跳ばせるCGIに

# この機能を使うには上の行を # で #=item とコメントアウトしてください

INIT:{
	if($CF{'program'}eq __FILE__){
		#直接実行だったら動き出す
		&locate($ENV{'QUERY_STRING'});
	}
}

=pod

=cut

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
	#ログファイルちゃんとある？
	defined$CF{'log'}||die"\$CF{'log'} is Undefined";
	unless(-e"$CF{'log'}0.cgi"){
		(-e"$CF{'log'}0.pl")&&(die"旧形式0.plが残っています 不具合の兆し？");
		DIR:{
			(-e"$CF{'log'}")&&(last DIR);
			mkdir("$CF{'log'}",0777)&&(last DIR);
			die"Can't read/write/create LogDir($CF{'log'})[$!]";
		}
		open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
		eval{flock(ZERO,2)};
		if(!-s"$CF{'log'}0.cgi"){
			print ZERO "Mir12=\t0-0;\tsubject=\tWelcome to Mireille;\tname=\tMireilleSystem;\ttime=\t$^T;\t"
			."body=\tLOGディレクトリ及び0.cgiが、正常に設置されていなかった為、設置しなおしました<BR>"
			."このメッセージが表示されている場合、すでにMireilleにより正常に自動設置されています<BR>"
			."なお、このメッセージは新規投稿があると、自動的に消滅します;\t";
		}
		close(ZERO);
	}

	#モードごとの振り分け
	&getParam;
	
	if($CF{'readOnly'}&&$IN{'isEditing'}){
		#閲覧専用モード
		&showUserError('現在この掲示板は閲覧専用モードに設定されています');
	}else{
		#記事書き込み
		defined$IN{'body'}&&&writeArticle;
		#返信
		$IN{'i'}&&&res;
		#新規書き込み
		defined$IN{'j'}&&(&showHeader,&getCookie,&prtfrm,&footer);
		#記事修正リストor実行
		defined$IN{'rvs'}&&(index($IN{'rvs'},'-')<0?&showRvsMenu:&rvsArticle);
		#記事削除リストor実行
		defined$IN{'del'}&&(index($IN{'del'},'-')<0?&showRvsMenu:&delArticle);
	}
	#検索
	defined$IN{'seek'}&&&showArtSeek;
	#ヘルプ
	defined$IN{'help'}&&(require($CF{'help'}?$CF{'help'}:'help.pl'));
	#アイコン
	defined$IN{'icct'}&&(require($CF{'icct'}?$CF{'icct'}:'iconctlg.cgi'));
	#ホーム
	defined$IN{'home'}&&&locate($CF{'home'});
	#記事表示
	&showIndex;
	exit;
}


#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# main直下のサブルーチン群

#-------------------------------------------------
# Index 記事表示
#
sub showIndex{
	&xmlmode if 'xml'eq$IN{'viewstyle'};

	#-----------------------------
	#Cookie取得＆書き込み
	&getCookie?&setCookie(\%CK):($CK{'time'}=$^T-$CF{'newnc'});

	#-----------------------------
	# HTTP,HTML,PAGEヘッダーを表示
	&showHeader;

	#-----------------------------
	#新規投稿フォームを表示する（設定による）
	$CF{'prtwrt'}&&&prtfrm;
	print"$CF{'note'}";
	#記事ナビボタン
	&artnavi('button');

	#-----------------------------
	#ページ処理
	&logfiles($CF{'sort'});
	if($IN{'read'}){
		my$page=1;my$thread=1;
		for(@file){
			$_==$IN{'read'}&&($IN{'page'}=$page,last);
			++$thread>$CF{'page'}|| next;
			$page++;$thread=1;
		}
	}

	#-----------------------------
	#記事情報
	my%NEW;
	my@view=map{$NEW{"$_"}=qq(<A href="index.cgi?read=$_#art$_" class="new">$_</A>)}
	grep{$zer2[$_-$zer2[0]]>$CK{'time'}}@file;

	#-----------------------------
	#未読記事のあるスレッド
	my$unread='';
	if($#view>-1){
		# 20 : 未読記事のあるスレッドがある時に表示するスレッド数の上限
		$unread='<P>未読記事のあるスレッド[ '.($#view>20?"@view[0..20] ..":"@view[0..$#view]")." ]</P>";
	}

	#-----------------------------
	#ページ選択TABLEを表示
	my$pgslct=&pgslct($#file,$CF{'page'});

	#-----------------------------
	#このページのスレッド
	my$this='';
	@view=splice(@file,($IN{'page'}-1)*$CF{'page'},$CF{'page'});
	$#view!=0&&!$view[$#view]&&pop@view;
	for(0..$#view){
		$this.=qq(<A href="#art$view[$_]" title="Alt+$_">)
		.($NEW{"$view[$_]"}?qq(<SPAN class="new">$view[$_]</SPAN>):$view[$_])."</A> ";
	}

	#-----------------------------
	#記事情報表示上
	print<<"_HTML_";
<DIV class="artinfo">
$unread
$pgslct
<P class="artinfo">このページのスレッド<BR>\n[ $this]<BR>
<A name="nav_n0" href="#nav_s1" title="下のスレッドへ" accesskey="0">▼</A></P>
</DIV>
_HTML_
	#-----------------------------
	#記事表示
	if(0 ne$view[0]){
		#既に稼動中のとき
		#Threads Body
		for(0..$#view){
			&showArticle('i'=>$view[$_],'ak'=>($_+1));
		}
	}else{
		#log0のみ つまり設置直後のとき
		&showArticle('i'=>0,'ak'=>1);
	}
	#-----------------------------
	#記事情報表示下
	print<<"_HTML_";
<DIV class="artinfo">
<P class="artinfo"><A name="nav_s@{[$#view+2]}" href="#nav_n@{[$#view+1]}" title="上のスレッドへ" accesskey="&#@{[$#view+50]};">▲</A><BR>
このページのスレッド<BR>\n[ $this]</P>

$pgslct
</DIV>
_HTML_

	#-----------------------------
	#記事ナビ
	&artnavi;

	#-----------------------------
	#フッタ
	&footer;
	exit;
}


#-------------------------------------------------
# 記事書き込み
#
sub writeArticle{

=item 書き込みの情報

(length$IN{'j'}xor$IN{'i'})			新規
(!defined$IN{'i'}&&$IN{'j'}eq 0)	新規親記事
($IN{'i'}&&!defined$IN{'j'})		新規子記事
($IN{'i'}&&defined$IN{'j'})			修正
($IN{'i'}&&$IN{'j'}eq 0)			修正親記事
($IN{'i'}&&$IN{'j'}ne 0)			修正子記事

=cut

	#-----------------------------
	#コマンドとその調整
	my%EX;
	for(split(/;/o,$IN{'cmd'})){
		my($i,$j)=split('=',$_,2);
		$i||next;
		defined$j||($j=1);
		$EX{$i}=$j;
	}

=item コマンドで使えるもの

icon : 専用アイコン
bring: 持ち込みアイコン

dnew : 記事日時更新
znew : スレッド日時更新
renew: dnew&&znew

usetag:		!SELECTABLE()で許可してあるアイコンの範囲内で使うアイコンを選べる
notag:		タグを使わない
noautolink:	URI自動リンクを使わない
noartno:	記事番号リンクを使わない
nostrong:	語句強調を使わない

su: 管理パスワードを入れておくと、返信できないスレッドに返信できたりする（ようになる予定）

"key=value;key=value"の形式でコマンド欄に入力する
key及びvalueは[=;]を含んではならない
（Q:アイコンのurlに[=;]が含まれることってある？）
（A:cgiで中継してる場合はあるかもね。。）

・備考
key1="value1;value1";key2=value2;
はMireille1.2.2.16では期待通りに解釈してくれないわけです
1.2.2.16現在ではおそらく今の適当な処理でもいいけれど、
本格的にコマンドを拡充させるならMarldiaのコマンド周りをもって来るべき
まぁ、これら以外にコマンドのネタが思いつかないので・・・^^;;
Marldiaはデータの保持などは適当でもいいこともあって、結構管理コマンドをつけていたりするので、
上記のようなものを使う必要性があるかもしれないため、念のため対応させているのですけどね

=cut

	#renewはdnew&&znew
	$EX{'dnew'}=$EX{'znew'}=1if$EX{'renew'};
	
	#専用アイコン機能。index.cgiで設定する。
	if($CF{'exicon'}){
		#index.cgiで指定したアイコンパスワードに合致すれば。
		$IN{'icon'}=$IC{"$EX{'icon'}"}if$IC{"$EX{'icon'}"};

=item 持ち込みアイコン 標準では無効

持ち込みアイコンを真に稼動させるためには$CF{'icon'}=''としないと意味がありません
しかし、画像持込は、大きな画像を貼られるというわかりやすい手法の他にも、
使い方によっては利用者の情報を収集することができるという危険があるので、
信用の置ける人しか来ない場所で無い限り、使わないほうがいいです

PerlモジュールのImage::sizeを用いることによって、サイズ制限をかけることが出来るかもしれません
これなら少し安全性は増しますが、CGI経由で投稿者の情報が流出する、、
という可能性が依然残っているため、無制限にすることは出来ないでしょう

=cut

#		$IN{'icon'}=$EX{'bring'}if$EX{'bring'};
	}
	
	
	#-----------------------------
	#本文の処理
	#form->data変換
	if($CF{'tags'}&& 'ALLALL'eq$CF{'tags'}){
		#ALLALLは全面OK。但し強調は無効。URI自動リンクも無効。
		#自前でリンクを張ったり、強調してあるものを、二重にリンク・強調してしまいますから
	}else{
		#本文のみタグを使ってもいい設定にもできる
		my$attrdel=0;#属性を消す/消さない(1/0)
		my$str=$IN{'body'};
		study$str;
		$str=~tr/"'<>/\01-\04/;
		
		#タグ処理
		if($CF{'tags'}&&!$EX{'notag'}){
			my$tags=$CF{'tags'};
			my%tagCom=map{m/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
			if($tagCom{'!SELECTABLE'}){
				$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{m/\w+/}split(/\s+/,$EX{'usetag'}));
			}elsif(defined$tagCom{'!SELECTABLE'}){
				$tags='\w+';
			}
			
			my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
			my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
			my$text_regex = '[^\03]*';
			my$result='';
			#もし BRタグや Aタグなど特定のタグだけは削除したくない場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/i;
			my$remain=join('|',grep{m/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
			#逆に FONTタグや IMGタグなど特定のタグだけ削除したい場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/i;
			my$pos=length$str;
			while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
				$pos=pos$str;
				length$1||length$2||last;
				$result.=$1;
				my$tag_tmp=$2;
				if($tag_tmp=~s/^\03((\/?(?:$remain))(?![\dA-Za-z]).*)\04/<$1>/io){
					$tag_tmp=~tr/\01\02/"'/;
					$result.=$attrdel?"<$2>":$tag_tmp;
				}else{
					$result.=$tag_tmp;
				}
				if($tag_tmp=~/^\03(XMP|PLAINTEXT|SCRIPT)(?![\dA-Za-z])/i){
					$str=~/(.*?)(?:\03\/$1(?![\dA-Za-z])$tag_regex_|$)/gsi;
					(my$tag_tmp=$1)=~tr/\01\02/"'/;
					$result.=$tag_tmp;
				}
			}
			$str=$result.substr($str,$pos);
		}else{
			#許可タグ無しorCommand:notag
		}
		
		#語句強調
		if($CF{'strong'}&&!$EX{'nostrong'}){
			my%ST=map{(my$str=$_)=~tr/"'<>/\01-\04/;$str}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
			if($CF{'strong'}=~/^ /o){
				#拡張語句強調
				for(keys%ST){
					if($_=~/^\/(.+)\/$/o){
						my$regexp=$1;
						($ST{$_}=~s/^\/(.+)\/$/$1/o)?($str=~s[$regexp][$ST{$_}]gm)
						:($str=~s[$regexp][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm);
					}elsif($ST{$_}=~s/^\/(.+)\/$/$1/o){
						$str=~s[^(\Q$_\E.*)$][$ST{$_}]gm;
					}else{
						$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;
					}
				}
			}else{
				#基本語句強調
				for(keys%ST){$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;}
			}
		}
		
		#URI自動リンク
		if($CF{'noautolink'}||!$EX{'noautolink'}){
			#[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
			#[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
			#[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
			#[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
			#http URL の正規表現
			my$http_URL_regex =
		q{\b(?:https?|shttp)://(?:(?:[!$&-.\w:;=~]|%[\dA-Fa-f}.
		q{][\dA-Fa-f])*@)?(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)}.
		q{*[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.}.
		q{\d+)(?::\d*)?(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f]}.
		q{[\dA-Fa-f])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-}.
		q{Fa-f])*)*(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f}.
		q{])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*)}.
		q{*)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])}.
		q{*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{)?};
			#ftp URL の正規表現
			my$ftp_URL_regex =
		q{\bftp://(?:(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*}.
		q{(?::(?:[!$&-.\w;=~]|%[\dA-Fa-f][\dA-Fa-f])*)?@)?(?}.
		q{:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)*[a-zA-Z](?:[-a-zA-}.
		q{Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.\d+)(?::\d*)?}.
		q{(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*(?:/(?}.
		q{:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*(?:;type=[}.
		q{AIDaid])?)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\d}.
		q{A-Fa-f])*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA}.
		q{-Fa-f])*)?};
			#メールアドレスの正規表現改
			#"aaa@localhost"などを掲示板で「メールアドレス」として使うとは思えないので。
			my$mail_regex=
		q{(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
		.q{\[\]\00-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
		.q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x}
		.q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff])|"[^\\\\\x80-}
		.q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
		.q{\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
		.q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
		.q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,}
		.q{;:".\\\\\[\]\00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
		.q{^\x80-\xff])*\]))+};
		
			$str=~s{(?<!["'])($http_URL_regex|$ftp_URL_regex|($mail_regex))(?!["'])}
			{<A class="autolink" href="@{[$2?'mailto:':'']}$1" target="_blank">$1<\x2fA>}go;
		}else{
			#Command:nolink
		}
		
		#記事番号リンク「>>No.12-6」
		if($CF{'noartno'}||!$EX{'noartno'}){
			$str=~s{(\04\04No\.(\d+)(\-\d+)?)}{<A class="autolink" href="index.cgi?read=$2#art$2$3">$1</A>}go;
		}
		
		$str=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
		$str=~s/\01/&#34;/go;
		$str=~s/\02/&#39;/go;
		$str=~s/\03/&#60;/go;
		$str=~s/\04/&#62;/go;
		$IN{'body'}=$str;
	}
	$IN{'body'}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
	$IN{'body'}=~s/\n+$//o;
	$IN{'body'}=~s/\n/<BR>/go;
	
	
	#-----------------------------
	#$IN{'cook'}がONならCookieの書き込み
	COOKIE:{
		$IN{'cook'}||last COOKIE;
		$CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}&& last COOKIE; #管理パスの時はCookie保存しない
		&getCookie;
		&setCookie(\%IN);
	}

	#-----------------------------
	#エラー表示
	my@error;
	$IN{'name'}||push(@error,'名前');
	$IN{'body'}||push(@error,'本文');
	$IN{'pass'}||($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'})or push(@error,'パスワード');
	if(@error){
		&showHeader;
		print<<"_HTML_";
<H2 class="mode">- Write Error -</H2>
<P>@{[join('と',map{qq(<SPAN style="color:#f00">$_</SPAN>)}@error)]}をちゃんと入力してください</P>
_HTML_
		%CK=%IN;
		&rvsij;
		&footer;
	}

	#-----------------------------
	#書き込みデータ準備
	open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't read/write log(0.cgi)[$!]";
	eval{flock(ZERO,2)};
	seek(ZERO,0,0);
	my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
	index($zero[0],"Mir12=\t")&&die"ログ形式がMir12型以外です($zero[0])";
	%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
	my@zer1=split(/\s+/o,$zero[1]);
	@zer2=split(/\s/o,$zero[2]);
	$zer2[0]||($zer2[0]=0);

	#-----------------------------
	&logfiles('number');
	$IN{'i'}=$file[0]+1if$IN{'i'}&&$IN{'i'}>$file[0]+1;

	#-----------------------------
	#書き込みの前処理を拡張したい時用
	&exprewrt();

	#-----------------------------
	#いよいよ
	unless($IN{'ArtType'}&2){
		#新規・返信書き込み
		$IN{'newps'}=&mircrypt($^T,$IN{'pass'});
		$EX{'znew'}=1;
		if($IN{'i'}&&$zero[1]=~/($IN{'i'}):$ENV{'CONTENT_LENGTH'}:([1-9]\d*)/
			or length$IN{'j'}&&$zero[1]=~/(\d+):$ENV{'CONTENT_LENGTH'}:($IN{'j'})/){
			&showHeader;
	print<<"_HTML_";
<H2 class="mode">- 多重投稿？ -</H2>
<DIV class="center">
<P style="margin:0.6em">今投稿された記事の内容は<A href="index.cgi?read=$1#art$1-$2" title="該当記事を確認する">第$1番スレッドの$2番目</A>と同一内容だと思われます<BR>
該当記事を確認して、同一内容でない場合は、下のフォームで少し修正してから投稿してみてください。</P>
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="掲示板に戻る(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}に戻る(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
			%CK=%IN;
			&rvsij;
			&footer;
		}elsif(!$IN{'ArtType'}){
			#-----------------------------
			#新規書き込み
			if($CF{'logmax'}>0&&@file>$CF{'logmax'}){
				#古い記事スレッドファイルを ファイル名変更/削除 する

=pod この部分はこんがらがりやすいのでメモ。

@fileは (101,100,99,95,91,・・・,3,2,1,0) といった配列
この順番は常に降順
最後に必ず記事情報ファイルを表す 0 が来る

@zer2は (1 1000000 10000001 ・・・ 1200000) といった配列
最初の数字は記事番号と@zer2での添え字との対応を表す
このOffsetが100なら記事番号159の情報は$zer2[59]にある

ファイルが増えすぎたときに記事スレッドファイルを削除する際には、
上記の二つの配列を同時に正しく処理しなければならない
この時、記事スレッドファイルが削除されたことによって、
@fileが所々数字が飛んでいる可能性があることに注意
@zer2は記事が削除されていても連番になっている

ちなみに、
$file[$#file-1] はこの時削除される記事のうちで記事スレッド番号が最も小さいものの、記事スレッド番号を、
$file[$CF{'logmax'}-1] は記事スレッド番号が最も大きいものの、記事スレッド番号をあらわす
$file[$CF{'logmax'}-2] は削除された後に残った記事スレッドのうち、
記事スレッド番号が小さなものの、記事スレッド番号をあらわす

よって、$file[$CF{'logmax'}-2]-$file[$#file-1] はこの時削除される延べ記事数をあらわす
#途中記事スレッドが削除されている場合、実際に削除される記事スレッド数とは異なる

注：
 @fileには0.cgiが含まれているので一つ多い、
 また@fileにはこれから追加する新スレッドがないので一つ少ない

=cut

				splice(@zer2,1,$file[$CF{'logmax'}-2]-$file[$#file-1]);
				&delThread($CF{'delold'},splice(@file,$CF{'logmax'}-1,@file-$CF{'logmax'}))
				#($#file-1)-($CF{'logmax'}-1)+1=@file-$CF{'logmax'}、ということ
				||die"\$CF{'delold'}の設定が異常です($CF{'delold'})";
				$zer2[0]=$file[$CF{'logmax'}-2]-1;
			}
			$IN{'i'}=$file[0]+1;
			open(WR,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't write log($IN{'i'})[$!]";
			eval{flock(WR,2)};
			truncate(WR,0);
			seek(WR,0,0);
			print WR "Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}($CF{'prtitm'}=~/\+([a-z\d]+)\b/go))."\n";
			close(WR);
		}else{
			#-----------------------------
			#返信書き込み
			open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
			eval{flock(RW,2)};
			seek(RW,0,0);
			my$line;
			while(<RW>){$line=$_;}
			$IN{'j'}=$.; #$.-1+1
			seek(RW,0,2);
			my$prefix='';
			if(!chomp$line){
				++$IN{'j'};
				$prefix="\n";
			}
			if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
				#パスワードが管理パスのときは最大子記事数制限がかかっていても投稿出来る
			}elsif($CF{'maxChilds'}&&$IN{'j'}>$CF{'maxChilds'}){
				&showUserError('既に最大子記事数制限を越えている');
			}
			print RW $prefix
			."Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}($CF{'chditm'}=~/\+([a-z\d]+)\b/go))."\n";
			close(RW);
		}
		
		#-----------------------------
		#MailNotify
		if($CF{'mailnotify'}){
			#新規/返信があった場合はメールを送る
			require 'notify.pl';
			&mailnotify(%IN);
		}
		
	}else{
		#-----------------------------
		#修正書き込み
		open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
		eval{flock(RW,2)};
		seek(RW,0,0);
		my@log=map{m/^([^\x0D\x0A]*)/o}<RW>;
		$#log<$IN{'j'} and die"Something Wicked happend!(jが大きすぎ)";
		$log[$IN{'j'}] or  die"Something Wicked happend!(修正でないj)";
		my%DT=($log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go);
		#PasswordCheck
		if($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){
			#MasterPassによる
			if($IN{'pass'}){
				#Pass変更
				$IN{'oldps'}=$IN{'pass'};
			}else{
				#Passそのまま
				$IN{'newps'}=$DT{'pass'};
			}
		}else{
			#UserPassによる
			unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
				&showHeader;
				print qq(<H2 class="mode">Password Error</H2>\n);
				%CK=%IN;
				&rvsij;
				&footer;
				exit;
			}
			#Pass変更
			$IN{'oldps'}=$IN{'pass'};
		}
		unless($IN{'newps'}){
			#Pass変更・日時変更
			$EX{'dnew'}&&($DT{'time'}=$^T);
			$IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
		}
		#書き込み
		$log[$IN{'j'}]=
			"Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$DT{'time'};\tbody=\t$IN{'body'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}((!$IN{'j'}?$CF{'prtitm'}:$CF{'chditm'})=~/\b([a-z\d]+)\b/go))."\n";
		truncate(RW,0);
		seek(RW,0,0);
		print RW @log;
		close(RW);
	}
	
	if($EX{'znew'}){
		#-----------------------------
		#ログ管理ファイル、0.plに書き込み
		#新規・返信の時には投稿情報を保存
		$#zer1>2&&($#zer1=2);
		unshift(@zer1,"$IN{'i'}:$ENV{'CONTENT_LENGTH'}:$IN{'j'}");
		my$No=$IN{'i'}-$zer2[0];
		$No>0||die"ZER2のデータが不正です 'i':$IN{'i'},'zer2':$zer2[0]";
		$zer2[$No]=$^T;
		truncate(ZERO,0);
		seek(ZERO,0,0);
		print ZERO 
			"Mir12=\t$IN{'i'}-$IN{'j'};\tsubject=\t$IN{'subject'};\tname=\t$IN{'name'};\ttime=\t$^T;\t"
			."\n@zer1\n@zer2\n";
	}
	close(ZERO); #ここでやっと書き込み終了

	#-----------------------------
	#書き込み成功＆「自由に修正をどうぞ」
	&showHeader;
	print<<"_HTML_";
<H2 class="mode">- 書き込み完了 -</H2>
<DIV class="center">
<P style="margin:0.6em">以下の内容で第$IN{'i'}番スレッドの$IN{'j'}番目に書き込みました。<BR>
これでよければそのままTOPや掲示板に戻ってください。<BR>
修正したい場合は以下のフォームで修正して投稿してください。</P>
<DIV align="center" class="note" style="width:600px"><P align="left">
<STRONG>--- PREVIEW ---</STRONG><BR>$IN{'body'}</P></DIV>
<TABLE border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="掲示板に戻る(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}に戻る(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
	%CK=%IN;
	$CK{'oldps'}||($CK{'oldps'}=$CK{'pass'});
	&rvsij;
	&footer;

	exit;
}


#-------------------------------------------------
# 記事返信
#
sub res{
	&getCookie;
	&showHeader;
	print qq(<H2 class="mode">- 記事返信モード -</H2>\n);
	print q(<DIV style="border:dashed 1px #333;height:400px;overflow:auto;width:99%">)
	.q(<H3>このスレッドの今までの内容</H3>);
	print"This thread$IN{'i'} is deleted."if"del"eq&showArticle('i'=>$IN{'i'},'ak'=>1,'res'=>1);
	print q(</DIV>);
	$CK{'i'}=$IN{'i'};
	$CK{'ak'}=1;
	&chdfrm;
	&footer;
	exit;
}


#-------------------------------------------------
# 記事修正・削除メニュー
#
sub showRvsMenu{
=item 引数
$ 前回の処理の結果
=cut
	&getCookie;
	&showHeader;
	my$mode='';
	#モード分岐
	if(defined$IN{'rvs'}){$mode='rvs';print qq(<H2 class="mode">- 記事修正モード -</H2>\n);}
	elsif(defined$IN{'del'}){$mode='del';print qq(<H2 class="mode">- 記事削除モード -</H2>\n);}
	else{print qq(<H2 class="mode">Something Wicked happend!(modeが不明)</H2>);&footer;}
	#処理成功-Indexに戻る
	if($_[0]){
		print<<"_HTML_";
<DIV class="center">
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<CAPTION>$_[0]</CAPTION>
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="掲示板に戻る(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}に戻る(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
	}
	#ログ処理
	&logfiles('number');
	my$pgslct=&pgslct($#file,$CF{'delpg'},$mode);
	my@i=@file;
	@i=splice(@i,($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});
	$i[$#i]==0&& pop@i;
	print<<"_HTML_";
<DIV class="center">$pgslct</DIV>

<FORM id="List" method="post" action="index.cgi">
<DIV class="center"><TABLE border="1" cellspacing="0" class="list" summary="List" width="80%">
<COL style="width:5em">
<COL style="width:15em">
<COL>
<TR>
<TD style="text-align:center">[$i[0]-$i[$#i]]</TD>
<TD><SPAN class="ak">P</SPAN>assword: <INPUT name="pass" type="password"
 accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}"></TD>
<TD>
<INPUT name="$mode" type="hidden" value="">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</TD></TR>
_HTML_
	#ログスレッドごと
	for(@i){
		$_||next;
		-e"$CF{'log'}$_.cgi"||next;
		my$i=$_;
		my$j=-1;
		open(RD,"<$CF{'log'}$i.cgi")||die"Can't read log($i.cgi)[$!]";
		eval{flock(RD,1)};
#		print"<TR><TD colspan=\"6\"><HR></TD></TR>";
		my$count="<A href=\"index.cgi?read=$i#art$i\">第$i号</A>";
		#記事ごと
		while(<RD>){
			$j++;
			index($_,"Mir12=\tdel;\t")||next;
			my%DT=($_=~/([^\t]*)=\t([^\t]*);\t/go);
			$j&&($count="Res $j");
			my$No="$i-$j";
			my$date=&date($DT{'time'});
			#本文の縮め処理
			$DT{'body'}=~s/<br\b[^>]*>/↓/go;
			$DT{'body'}=&getTruncated($DT{'body'},100);
			my$level=!$j?'parent':'child';
			print<<"_HTML_";
<TR class="$level">
<TH align="right">$count</TH>
<TH align="left">$DT{'subject'}</TH>
<TD align="right">by $DT{'name'}</TD>
</TR>
<TR>
<TD><INPUT type="radio" name="$mode" value="$No"></TD>
<TD align="right">$date</TD>
<TD align="right">$DT{'body'}</TD>
</TR>
_HTML_
		}
		close(RD);
	}
	print"</TABLE></DIV></FORM>\n";
	print qq(<DIV class="center">$pgslct</DIV>);
	&footer;
	exit;
}


#-------------------------------------------------
# 記事を修正
#
sub rvsArticle{
	($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});
	open(RD,"<$CF{'log'}$IN{'i'}.cgi")||die"Can't read log($IN{'i'}.cgi)[$!]";
	eval{flock(RD,1)};
	my$i=0;
	my%DT;
	while(<RD>){
		$i++==$IN{'j'}||next;
		%DT=($_=~/([^\t]*)=\t([^\t]*);\t/go);
	}
	close(RD);
=pod
たとえ$IN{'pass'}が渡されなくても、GetCookieでCookieを参照し、
もしそこで得られた$CK{'pass'}がパスワードと一致すれば修正モードに通す、
というようにして利便性の向上を図っている。
当然パスワードが一致しなければ入力するように要請する。
=cut
	if($IN{'pass'}){
		#INで送られてきた？
		$IN{'oldps'}=$IN{'pass'};
		if(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
			#INpassOK
			#処理へ
		}elsif($CF{'admps'}&&($IN{'pass'}eq$CF{'admps'})){
			#ADMINpassOK
			$IN{'pass'}='';
			#処理へ
		}else{
			&showRvsMenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。");
		}
	}else{
		#Cookieにある？
		&getCookie;
		$IN{'pass'}=$CK{'pass'};
		$IN{'oldps'}=$CK{'pass'};
		#-----------------------------
		unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
			#無いなら入力して
			&showHeader;
			print<<"_HTML_";
<H2 class="mode">- 第$IN{'i'}番の$IN{'j'}のパスワード認証 -</H2>
<FORM accept-charset="euc-jp" id="Revise" method="post" action="index.cgi">
<TABLE cellspacing="2" summary="Revise" width="550">
<COL width="50">
<COL width="170">
<COL width="330">
<P style="margin:0.6em">パスワードを入力してください</P>
<P style="margin:0.6em"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
<INPUT name="rvs" type="hidden" value="$IN{'rvs'}"></P>
<P style="margin:0.6em">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</p>
_HTML_
			&footer;
			exit;
		}
		#CKpassOK
		#処理へ
	}
	#Revise Main Routin
	&showHeader;
	print qq(<H2 class="mode">- 第$IN{'i'}番の$IN{'j'}の修正モード -</H2>\n);
	%CK=%DT;
	@CK{qw(i j pass oldps)}=@IN{qw(i j pass oldps)};
	&rvsij;
	&footer;
	exit;
}


#-------------------------------------------------
# 記事削除
#
sub delArticle{
	my$delEvenIfMarkMode=0;
	
	($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});
	open(RW,"+>>$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$!]";
	eval{flock(RD,2)};
	seek(RW,0,0);
	my@log=<RW>;
	my%DT=($log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go);
	#削除分岐
	SWITCH:{
		if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
			#AdminPassOK
			if($IN{'j'}==0&&!$IN{'type'}){
				#削除する方法無いなら入力して
				&showHeader;
				print<<"_HTML_";
<H2 class="mode">- 第$IN{'i'}番スレッドの削除 -</H2>
<FORM accept-charset="euc-jp" id="Delete" method="post" action="index.cgi">
<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>スレッドの削除方法を選んでください</LEGEND>
_HTML_
				my$i=<<"_HTML_";
<TD>
<LABEL for="mark">親記事の本文のみ削除<INPUT id="mark" name="del" type="radio" value="$IN{'del'}-1"></LABEL>
<LABEL for="$CF{'delthr'}">記事スレッドを削除<INPUT id="$CF{'delthr'}" name="del" type="radio" value="$IN{'del'}-2"></LABEL>
_HTML_
				$i=~s/id="$CF{'delthr'}"/id="$CF{'delthr'}" checked="checked"/o;
				print<<"_HTML_";
$i
</FIELDSET>

<P style="margin:0.6em">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</P>
_HTML_
				&footer;
				exit;
			}
			$IN{'j'}==0&&$IN{'type'}==2&& last SWITCH;
		}else{
			#一般Pass
			&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
			 or &showRvsMenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。");
			$IN{'j'}==0&&$#log==0&& last SWITCH;
		}
		
		#mark
		if($delEvenIfMarkMode){
			$log[$IN{'j'}]=~s/\tbody=\t([^\t]*);\t/\tbody=\tdel;\t/go;
		}
		$log[$IN{'j'}]=~s/^Mir12=\t([^\t]*);\t/Mir12=\tdel;\t/go;
		truncate(RW,0);
		seek(RW,0,0);
		print RW @log;
		close(RW);
		&showRvsMenu("第$IN{'i'}番の$IN{'j'}を削除しました。");
	}
	close(RW);
	#親記事削除
	&showRvsMenu("第$IN{'i'}番スレッドを削除しました。(".&delThread($CF{'delthr'},$IN{'i'}).")");
	exit;
}


#-------------------------------------------------
# 全文検索機能
#
sub showArtSeek{
	&showHeader;
	print qq(<H2 class="mode">- 検索モード -</H2>);
	my%SK=split(/ /o,$CF{'sekitm'});
	
	if(length$IN{'seek'}){
		#-----------------------------
		#検索＆結果表示
		my$result='';
		my$item='';
		my$seek=quotemeta$IN{'seek'};
		'ALL'eq$IN{'item'}||($item="\t$IN{'item'}");
		&logfiles('number');
		
		#正しくパターンマッチさせる
		my$eucpre=qr{(?<!\x8F)};
		my$eucpost=qr{(?=
			(?:[\xA1-\xFE][\xA1-\xFE])*	# JIS X 0208 が 0文字以上続いて
			(?:[\x00-\x7F\x8E\x8F]|\z)	# ASCII, SS2, SS3 または終端
		)}x;
		
		if('i'eq$IN{'every'}){
			#スレッドごと検索
			for(@file){
				$_||last;
				open(RD,"<$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				index($thread,$IN{'seek'})>-1||next;
				$thread=~/$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/o||next;
				$result.=qq(<A href="index.cgi?read=$_#art$_">No.$_</A>\n);
			}
		}else{
			#記事ごと検索
			for(@file){
				$_||last;
				open(RD,"<$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				close(RD);
				index($thread,$IN{'seek'})>-1||next;
				my$i=$_;
				my$j=0;
				for($thread=~/([\w\W]*?)$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/go){
					$j+=@{[/[\x0A\x0D]+/go]};
					$result.=qq(<A href="index.cgi?read=$i#art$i-$j">No.$i-$j</A>\n);
				}
			}
		}
		print<<"_HTML_";
<P>「<STRONG>$IN{'seek'}</STRONG>」で<STRONG>$SK{$IN{'item'}}</STRONG>を<STRONG>@{[
'i'eq$IN{'every'}?'スレッド':'各記事']}ごと</STRONG>に検索した結果、<BR>
@{[$result?"以下のスレッドで検索単語を発見しました♪<BR>$result":"検索単語は発見できませんでした"]}<BR>
かかった時間：@{[join'+',(times)[0,1]]}秒</P>
_HTML_
	}
	
	print<<"_HTML_";
<FORM accept-charset="euc-jp" id="seek" method="post" action="index.cgi">
<DIV class="center"><TABLE cellspacing="2" summary="検索フォーム" style="margin: 1em auto">
<TR>
<TH class="item">
<LABEL accesskey="m" for="item">検索する項目(<SPAN class="ak">M</SPAN>)</LABEL></TH>
<TD><SELECT name="item" id="item">
_HTML_
	my$select=join('',map{qq(<OPTION value="$_">$SK{$_}</OPTION>)}($CF{'sekitm'}=~/(\w+) \S+/go));
	$select=~s/(value="$IN{'item'}")/$1 selected="selected"/io;
	print<<"_HTML_";
$select</SELECT>
</TD>
</TR>
<TR>
<TH class="item"><LABEL accesskey="k" for="seek">検索する単語(<SPAN class="ak">K</SPAN>)</LABEL></TH>
<TD><INPUT type="text" name="seek" id="seek" style="ime-mode:active;width:200px;" value="$IN{'seek'}"></TD>
</TR>
<TR>
<TH class="item">検索する単位</TH>
<TD>
_HTML_
	my%DT=qw(i スレッドごと j 各記事ごと);
	$select=join('',map{qq(<LABEL accesskey="$_" for="every$_"><INPUT type="radio" name="every" id="every$_")
	.qq( value="$_">$DT{$_}(<SPAN class="ak">\u$_</SPAN>)</LABEL>\n)}('i','j'));
	$select=~s/(value="$IN{'every'}")/$1 checked="checked"/io;
	print<<"_HTML_";
$select
</TD>
</TR>
<TR>
<TD colspan="2">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" accesskey="r" value="キャンセル">
</TD>
</TR>
</TABLE>
</DIV>
<DIV class="center"><TABLE class="note"><TR><TD>
<UL class="note">
<LI>現行では検索文字列に正規表現を使うことは出来ません</LI>
<LI>ブラウザの「このページの内検索」を使えば、<BR>どこに探したい単語があるのかもわかりますね。</LI>
</UL></TD></TR></TABLE></DIV>
</FORM>
_HTML_
	&footer;
	exit;
}


#-------------------------------------------------
# ユーザー向けエラー
#
sub showUserError{
	my$message=shift();
	&showHeader;
	print<<"_HTML_";
<H2 class="mode">- エラーが発生しました -</H2>
<P>ご不便をかけて申し訳ございません<BR>
<span class="warning">$message</span>ため、<BR>正常な処理を続行することができませんでした<BR>
以下に念のため今入力されたデータを羅列しておきます<BR>
重要な情報がある場合、保存しておいて、またの機会に投稿してください</P>
<TABLE border="1" summary="ユーザー入力変数を表示しておく">
<CAPTION>今受け取った引数</CAPTION>
_HTML_
	print map{"<TR><TH>$_</TH><TD><XMP>$IN{$_}</XMP></TD>\n"}keys%IN;
	print '</TABLE>';
	&footer;
	exit;
}


#-------------------------------------------------
# Locationで転送
#
sub locate{
=item 引数
;
$ 飛ぶ先のURL（絶対でも相対でも）
=cut
	my$i=$_[0];
	($i)||(die"'Stay here.'");
	if(index($i,'http:')==0){
	}elsif($i=~/\?/o){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=sprintf('%s?%s',$_[0]);
	}elsif($i){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=$_[0];
	}
	print<<"_HTML_";
Status: 303 See Other
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Pragma: no-cache
Cache-Control: no-cache
Location: $i
X-Moe: Mireille

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"> 
<HTML>
<HEAD>
<META http-equiv="Refresh" content="0;URL=$i">
<TITLE>303 See Ohter</TITLE>
</HEAD>
<BODY>
<H1>: Mireille :</H1>
<P>And, please go <A href="$i">here</A>.</P>
<P>Location: $i</P>
<P>Mireille <VAR>$CF{'Core'}</VAR>.<BR>
Copyright &#169;2001,2002 <A href="http://www.airemix.com/" target="_blank" title="Airemix">Airemix</A>. All rights reserved.</P>
</BODY>
</HTML>
_HTML_
	exit;
}



#------------------------------------------------------------------------------#
# Sub Routins
#
# main直下のサブルーチン群の補助

#-------------------------------------------------
# Form内容取得
#
sub getParam{
	my$param;
	my@param;
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){
		@param=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
		my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
		print"Status: 200 OK\nLast-Modified: $last\n"
		."Content-Type: text/plain\n\nLast-Modified: $last";
		exit;
	}elsif('POST'eq$ENV{'REQUEST_METHOD'}){
		read(STDIN,$param,$ENV{'CONTENT_LENGTH'});
	}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
		$param=$ENV{'QUERY_STRING'};
	}
	
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	
	#引数をハッシュに
	if(length$param>262114){ # 262114:引数サイズの上限(byte)
		#サイズ制限
		&showHeader;
		print"いくらなんでも量が多すぎます\n$param";
		&footer;
		exit;
	}elsif(length$param>0){
		#入力を展開
		@param=split(/[&;]/o,$param);
	}
	undef$param;
	
	#入力を展開してハッシュに入れる
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/(\w+)/o)?$1:'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		if('body'ne$i){
			#本文以外は全面タグ禁止
			$j=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;/go;
			$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
			$j=~s/"/&#34;/go;
			$j=~s/'/&#39;/go;
			$j=~s/</&#60;/go;
			$j=~s/>/&#62;/go;
			$j=~s/\n/<BR>/go;
			$j=~s/(<BR>)+$//o;
		}#本文は後でまとめて
		$DT{$i}=$j;
	}
	
	#引数の汚染除去
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?"$1":'';
	$IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	if(defined$DT{'body'}){
		#記事書き込み
		#http URL の正規表現
		my$http_URL_regex =
	q{\b(?:https?|shttp)://(?:(?:[!$&-.\w:;=~]|%[\dA-Fa-f}.
	q{][\dA-Fa-f])*@)?(?:(?:[a-zA-Z\d](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.)}.
	q{*[a-zA-Z](?:[-a-zA-Z\d]*[a-zA-Z\d])?\.?|\d+\.\d+\.\d+\.}.
	q{\d+)(?::\d*)?(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f]}.
	q{[\dA-Fa-f])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-}.
	q{Fa-f])*)*(?:/(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f}.
	q{])*(?:;(?:[!$&-.\w:=@~]|%[\dA-Fa-f][\dA-Fa-f])*)*)}.
	q{*)?(?:\?(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])}.
	q{*)?(?:#(?:[!$&-/\w:;=?@~]|%[\dA-Fa-f][\dA-Fa-f])*}.
	q{)?};
		#メールアドレスの正規表現改
		#"aaa@localhost"などはWWW上で「メールアドレス」として使うとは思えないので。
		my$mail_regex=
	q{(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
	.q{\[\]\00-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
	.q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x}
	.q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff])|"[^\\\\\x80-}
	.q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
	.q{\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
	.q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
	.q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\00-\037\x80-\xff]+(?![^(\040)<>@,}
	.q{;:".\\\\\[\]\00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
	.q{^\x80-\xff])*\]))*};
		
		#bodyを除いた必須項目の処理
		if($DT{'i'}&&$DT{'i'}=~/([1-9]\d*)/o){
			$IN{'i'}=$1;
			if(defined$DT{'j'}&&$DT{'j'}=~/(0$|[1-9]\d*)/o){
				#修正[親子]記事
				$IN{'j'}=$1;
				unless($DT{'oldps'}){
				}elsif($DT{'oldps'}eq$CF{'admps'}){
					$IN{'oldps'}=$CF{'admps'};
				}elsif($DT{'oldps'}=~/(.{1,24})/o){
					$IN{'oldps'}=$1;
				}
				$IN{'ArtType'}=!$IN{'j'}?2:3;
			}else{
				#新規子記事
				$IN{'ArtType'}=1;
			}
		}else{
			#新規親記事
			$IN{'j'}=0;
			$IN{'ArtType'}=0;
		}

=item 記事種別

0: 新規親記事
1: 新規子記事
2: 修正親記事
3: 修正子記事

=cut

		$IN{'name'}=substr($DT{'name'},0,200);
		$IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}=$1;
		}
		
		{ #フォームの内容処理
			for($CF{$IN{'ArtType'}&1?'chditm':'prtitm'}=~/\b([a-z\d]+)\b/go){
				if('color'eq$_){
					$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
				}elsif('email'eq$_){
					$IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
				}elsif('home'eq$_){
					$IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
				}elsif('icon'eq$_){
					$IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
				}elsif('cmd'eq$_){
					$IN{'cmd'}=$1 if$DT{'cmd'}=~/(.+)/o;
				}elsif('subject'eq$_){
					$IN{'subject'}=&getTruncated($DT{'subject'}?$DT{'subject'}:$DT{'body'},80);
				}elsif('ra'eq$_||'hua'eq$_){
					next;
				}else{
					$IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
				}
			}
		}
		#bodyの処理は&writeArticleで行う
		$IN{'body'}=$DT{'body'};
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'new'}){
		#新規書き込み
		$IN{'j'}=0;
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'res'}){
		#返信書き込み
		$IN{'i'}=$1 if$DT{'res'}=~/([1-9]\d*)/o;
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'seek'}){
		#検索
		$IN{'seek'}=($DT{'seek'}=~/(.+)/o)?"$1":'';
		my%SK=split(/ /o,$CF{'sekitm'});
		$DT{'item'}=($DT{'item'}=~/(.+)/o)?"$1":'';
		$IN{'item'}=($SK{$DT{'item'}})?$DT{'item'}:'ALL';
		$IN{'every'}=($DT{'every'}=~/([ij])/o)?$1:'i';
	}elsif(defined$DT{'del'}){
		#記事削除リストor実行
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}="$1";
		}
		$IN{'del'}=($DT{'del'}=~/(\d+\-\d+(\-\d)?)/o)?"$1":'';
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'rvs'}){
		#記事修正リストor実行
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{1,24})/o){
			$IN{'pass'}="$1";
		}
		$IN{'rvs'}=($DT{'rvs'}=~/(\d+\-\d+)/o)?"$1":'';
		$IN{'isEditing'}=1;
	}elsif(defined$DT{'icct'}){
		#アイコンカタログ
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		return($IN{'icct'}=1);
	}elsif(defined$DT{'help'}){
		#ヘルプ
		return($IN{'help'}=1);
	}elsif(defined$DT{'home'}){
		#ホーム
		return($IN{'home'}=1);
	}elsif(defined$DT{'compact'}){
		#携帯端末モード
		require 'compact.cgi';
		exit;
	}elsif($DT{'read'}){
		#ログ読み
		$IN{'read'}=$1 if$DT{'read'}=~/([1-9]\d*)/o;
		$IN{'page'}=1; #readで指定された値がおかしいときのため
	}else{
		#ページ
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	}
	$IN{'viewstyle'}="$1"if$DT{'viewstyle'}=~/(\w+)/o;
	$IN{'xslurl'}="$1"if$DT{'xslurl'}=~/(.+)/o;
	return%IN;
}


#-------------------------------------------------
# 文字化けさせずに文字列の長さを切り詰める
#
sub getTruncated{
=item 引数
$ $str
$ 文字数制限
=cut

	my$str=shift();
	my$length=shift();
	
	$str=~/^\s*(\S.*?)\s*$/mo;
	$str=$1;
	$str=~s/<[^>]*>?//go;
	$str=~tr/\x09\x0A\x0D<>/\x20/s;
	
	if(length$str>$length){
		#文字制限オーバー
		# EUC-JP文字
		my$eucchar=qr((?:
			[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
			|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
			|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
		))x;
		#1byte文字は2byte文字の半分の長さだから、表示時の長さをそろえる為、
		#文字数でなくbyte数で切る
		#3byteEUC文字はほぼ使わないので考慮外
		substr($str,0,$length)=~/($eucchar*)/o;
		$str="$1...";
	}
	return$str;
}


#------------------------------------------------------------------------------#
# HTTP,HTML,Pageヘッダーをまとめて出力する
#
sub showHeader{
=item 引数
;
% 出力するHTMLのオプション
=cut

	my$lastModified=(stat("$CF{'log'}0.cgi"))[9];
	if($CF{'use304'}&&$ENV{'HTTP_IF_MODIFIED_SINCE'}){
		my$client=(&parse_rfc1123($ENV{'HTTP_IF_MODIFIED_SINCE'}))[0];
		my$server=0;
		if($client&&(&parse_rfc1123($lastModified))[0]<=$client){
			print<<"_HTML_";
Status: 304 Not Modified
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Date: @{[&datef($^T,'rfc1123')]}
X-Moe: Mireille


_HTML_
			exit;
		}
	}
	$lastModified=&datef($lastModified,'rfc1123');
	my%DT=@_;
	
	#-----------------------------
	#準備
	
	#Header
	if(!defined$CF{'head'}){
		$DT{'head'}=<<"_HTML_";
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="Start" href="$CF{'home'}">
<LINK rel="Index" href="index.cgi">
<LINK rel="Help" href="index.cgi?help">
<LINK rel="Stylesheet" type="text/css" href="$CF{'style'}">
<TITLE>$CF{'title'}</TITLE>
_HTML_
	}elsif(!defined$DT{'head'}){
		$DT{'head'}=$CF{'head'};
	}
	
	#Skyline
	unless(defined$DT{'skyline'}){
		#LastPost
		unless(%Z0){
			open(ZERO,"<$CF{'log'}0.cgi")||die"Can't read log(0.cgi)[$!]";
			eval{flock(ZERO,1)};
			my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
			close(ZERO);
			index($zero[0],"Mir12=\t")&&die"ログ形式がMir12型以外です($zero[0])";
			%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
			@zer2=split(/\s/o,$zero[2]);
		}
		my$date=&date($Z0{'time'});
		#exp.
		my$dateNow="Date:\t\t".&datef($^T,'dateTime')
		."\nLast-Modified:\t".&datef((stat("$CF{'log'}0.cgi"))[9],'dateTime');
		$DT{'skyline'}=<<"_HTML_";
<P class="lastpost" title="$dateNow"><A href="index.cgi?read=$Z0{'Mir12'}#art$Z0{'Mir12'}">Lastpost: $date $Z0{'name'}</A></P>
_HTML_
	}
	
	#-----------------------------
	#HTML書き出し
	print<<"_HTML_";
Status: 200 OK
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP
Date: @{[&datef($^T,'rfc1123')]}
X-Moe: Mireille
_HTML_
	print"Last-Modified: $lastModified\n"if$CF{'useLastModified'};#exp.
	#GZIP Switch
	my$status=qq(<META http-equiv="Last-Modified" content=").$lastModified."\">\n";
	!defined$CF{'conenc'}&&$CF{'gzip'}&&($CF{'conenc'}="|$CF{'gzip'} -cfq9");
	if($CF{'conenc'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&(index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')>-1)){
		#上のif文でgzip決め打ちしているのは“仕様”
		#gzip/compress以外に対応してるブラウザは稀なため、可変への需要が少ないと思われるためと
		#$CF{'conenc'}を設定可能にしているのは、GZIP圧縮転送のON/OFF切り替えのため、だから
		if( $ENV{'HTTP_SERVER_NAME'}#広告対策
		and	index($ENV{'HTTP_SERVER_NAME'},'tkcity.net')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'infoseek.co.jp')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'tok2.com')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'tripod')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'virtualave.net')>-1
		||	index($ENV{'HTTP_SERVER_NAME'},'hypermart.net')>-1
		){
			print"\n";
			$status.="<!-- can't use gzip on this server because of advertisements -->";
#		}elsif($ENV{'SERVER_SOFTWARE'}&& index($ENV{'SERVER_SOFTWARE'},'mod_gzip')>-1){
#			print"\n";
#			$status.="<!-- did't use gzip because this server is using mod_gzip -->";
#memo.cgiだとmod_gzipしてくれないっぽい
		}else{
			print"Content-encoding: gzip\n\n";
			if(!open(STDOUT,$CF{'conenc'})){
				#GZIP失敗時のエラーメッセージ
				binmode STDOUT;
				print unpack("u",
				q|M'XL(`-+V_#P""UV134O#0!"&[X'\AR45HBUM$&]I(TBIXD&4>O-20ES:2//A|.
				q|M=FNKXH^)3-J#%;SX42U2BM9BH'CPY$7Q)/90B"`>S28%/^:RNS//O#.\FS$P|.
				q|M55&)4CN)MZOZCB)D+9-BDR;IKHT%I$4O1:"X3J42-<III)544L%4P54MN64+|.
				q|M\SR7L0D.#A2%+*,5G6"]7,;!/4S'48X0BZ!UC6!LHMG4')JV"H492Y)0G.=X|.
				q|M+I?/K^9EA+*J*5)4K6"TM+&\AE0:;$!P2BOJC+HX._ERFF$)6MW3ZS%XG5[[|.
				q|M$>[@&/H`<`_`L-[#Y:?3Y#FG$9+^U0#&K`9OT``/VC`*:HYN;N(Z4^Z_PC`$|.
				q|MA]WGFW?P>6XJN[@O%O=T6SQ01#'-:!A,^B::_Z:/_FJ[YV[;[;LOX#$5\%UP|.
				q|M/X+,P.FX(\;`D7/(N%^#P+]M=9_`"W<(97@N$0L-70C<-/3ZCZMAQ!(1P#Y/|.
				q|6EJ1:K992(S"E6884`=\G94\YX`$`````|);
				exit;
			}
			#GZIP圧縮転送をかけられるときはかける
			print ' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')>-1; #IEのバグ対策
			$status.="<!-- gzip enable -->";
		}
	}else{
		print"\n";
		$status.="<!-- gzip disable -->";
	}
	print<<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
$DT{'head'}
$status
</HEAD>

<BODY>
$DT{'skyline'}
$CF{'pghead'}
$CF{'menu'}
_HTML_
#	eval qq(print<<"_HTML_";\n$CF{'menu'}\n_HTML_);
}


#-------------------------------------------------
# 記事スレッドファイルのリストを取得
#
sub logfiles{
=item 引数
;
$ 記事スレッドファイルリストの順番(date|number)

=item 説明

ログファイル名を取得し、
その番号又は更新日時に基づいて並び替えて
ファイル名番号のリストを返す

=cut

	undef@file;
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	if('date'eq$_[0]){
		#日付順 'date'
		@file=map{$_->[0]+$zer2[0]}sort{$b->[1]<=>$a->[1]or$b->[0]<=>$a->[0]}
		map{[$_,$zer2[$_]]}map{$_-$zer2[0]}grep{$_>$zer2[0]}map{m/^(\d+)\.cgi$/}readdir(DIR);
		push(@file,0);
	}else{
		#記事番号順 'number'
		@file=sort{$b<=>$a}map{m/^(\d+)\.cgi$/}readdir(DIR);
	}
	closedir(DIR);
}


#-------------------------------------------------
# ページ選択TABLE
#
sub pgslct{
=item 引数
$ 全部で何スレッドあるの？
$ 1ページあたりのスレッド数
;
$ モードの保持(rvs,del)
=cut
	my$thds=shift();
	my$page=shift();
	my$mode=$_[0]?"$_[0];page=":'page=';
	my@key=map{qq( accesskey="$_")}('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9ページのAccessKey

	#page表示調節
	my$max=20; #全部で20ページは直接飛べる
	my$half=int($max/2);
	my$str=0; #$strページ目から
	my$end=0; #$endページ目まで連続して直接飛べるように表示
	my$pags=int(($#file-1)/$page)+1;
	$IN{'page'}>$pags&&($IN{'page'}=$pags);

	#どこからどこまで
	if($pags<=$max){
		$str=1;
		$end=$pags;
	}elsif($IN{'page'}-$half<1){
		#1-10
		$str=1;
		$end=$pags;
	}elsif($IN{'page'}+$half>=$pags){
		#(max-10)-max
		$str=$pags-$max+1;
		$end=$pags;
	}else{
		$str=$IN{'page'}-$half+1;
		$end=$IN{'page'}+$half;
	}

	#配列へ
	my@page=map{$_==$IN{'page'}?qq(<STRONG class="pgsl">$_</STRONG>)
	:qq(<A href="index.cgi?$mode$_").($key[$_]?$key[$_]:'').">$_</A>\n"}($str..$end);

	#最先と最後
	$str!=1&& unshift(@page,qq(<A accesskey="&#60;" href="index.cgi?${mode}1">1</A>&#60;&#60;));
	$end!=$pags&& push(@page,qq(&#62;&#62;<A accesskey="&#62;" href="index.cgi?$mode$pags">$pags</A>));

	#いざ出力
	return<<"_HTML_";
<TABLE align="center" cellspacing="0" class="pgsl" summary="PageSelect" border="1">
<COL style="width:3.5em">
<COL>
<COL style="width:3.5em">
<TR>
<TD>@{[$IN{'page'}==1?'[最新]':qq(<A accesskey="," href="index.cgi?$mode).($IN{'page'}-1).'">&#60; 後の</A>']}</TD>
<TD>[ @page ]</TD>
<TD>@{[$pags-$IN{'page'}?qq(<A accesskey="." href="index.cgi?$mode).($IN{'page'}+1).'">昔の &#62;</A>':'[最古]']}</TD>
</TR>
</TABLE>
_HTML_
}


#-------------------------------------------------
# 記事表示
#
sub showArticle{
=item 引数
% 出力する記事の情報
=cut
	#このスレッド共通の情報
	my%DT=@_;
	$DT{'j'}=-1;
	
	open(RD,"<$CF{'log'}$DT{'i'}.cgi")||die"Can't read log($DT{'i'}.cgi)[$!]";
	eval{flock(RD,1)};
	while(<RD>){
		#親記事
		++$DT{'j'}||(&artprt(\%DT,$_),next);
		#子記事
		/^Mir12=\tdel;\t/o||&artchd(\%DT,$_);
	}
	close(RD);
	$DT{'j'}>-1||return;#記事がないならフッタを表示せず返す
	#記事フッタ
	&artfot(\%DT);
}


#-------------------------------------------------
# Cookieを取得する
#
sub getCookie{
	$ENV{'HTTP_COOKIE'}||return undef;
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改-\x09
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	for($ENV{'HTTP_COOKIE'}=~/(?:^|; )Mireille=([^;]*)/go){
		s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		my%DT=(/(\w+)\t($eucchar*)/go);
		for(keys%DT){
			if(!defined$CK{$_}||$CK{'lastModified'}<$DT{'lastModified'}){
				$CK{$_}=$DT{$_};
			}
		}
	}
	return%CK;
}


#-------------------------------------------------
# Cookie書き込み
#
sub setCookie{
=item 引数
\% Cookieに書き込む内容ハッシュのリファレンス
=cut
	my%DT=%{shift()};
	for(keys%CK){length$DT{$_}||($DT{$_}=$CK{$_})}
	$DT{'time'}=0;
	$DT{'expire'}=0;
	if($CK{'expire'}>$^T){
		#期限内
		$DT{'time'}=$CK{'time'};
		$DT{'expire'}=$CK{'expire'};
	}elsif($CK{'expire'}>0){
		#期限切れ
		$DT{'time'}=$CK{'expire'}-$CF{'newuc'};
		$DT{'expire'}=$^T+$CF{'newuc'};
		$CK{'time'}=$DT{'time'};
	}else{
		#新規
		$DT{'time'}=$^T;
		$DT{'expire'}=$^T+$CF{'newuc'};
		$CK{'time'}=$^T-$CF{'newnc'};
	}
	$DT{'lastModified'}=$^T;
	if($CF{'ckpath'}){
		my$cook=join('',map{"\t$_\t$DT{$_}"}("time expire lastModified"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."\n";
		$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."; $CF{'ckpath'}\n";
	}else{
		my$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass time expire lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		print"Set-Cookie: Mireille=$cook; expires=".&datef($^T+33554432,'cookie')."\n";
	}
	#33554432=2<<24; #33554432という数字に特に意味はない、ちなみに一年と少し
}


#-------------------------------------------------
# フォーマットされた日付取得を返す
#
sub datef{
=item 引数
$ time形式の時刻
;
$ 出力形式(cookie|last)
=cut
	my$time=shift();
	my$type=shift();
	unless($type){
	}elsif('cookie'eq$type||'gmt'eq$type){
	# Netscape風Cookie用
		return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('rfc1123'eq$type){
	# RFC1123 主としてLastModified用
		return sprintf("%s, %02d %s %d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
	}elsif('dateTime'eq$type){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
		$CF{'timezone'}||&cfgTimeZone($ENV{'TZ'});
		my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($time+$CF{'timeOffset'});
		return sprintf("%04d-%02d-%02dT%02d:%02d:%02d+09:00",$year+1900,$mon+1,$day,$hour,$min,$sec,$CF{'timezone'});
	}
	return&date($time);
}


#-------------------------------------------------
# タイムゾーンの取得
#
sub cfgTimeZone{
=pod
タイムゾーンを環境変数TZから取得して、%CFに設定する
他の関数はこの$CF{'timezone'},$CF{'timeOffset'}を使って、
gmtime()から確実に希望の地域の時刻を算出できる
=item 引数
$ $ENV{'TZ'}
=cut
	my$envtz=shift();
	if($CF{'timezone'}&&$CF{'TZ'}eq$envtz){
		#note. $CF{'timezone'}= EastPlus TimeZone <-> ENV-TZ= EastMinus TimeZone
	}elsif(!$envtz||'Z'eq$envtz||'UTC'eq$envtz||'GMT'eq$envtz){
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}elsif($envtz=~/([a-zA-Z]*)-(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("+%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=($2?$2*3600:0)+($3?$3*60:0);
	}elsif($envtz=~/([a-zA-Z]*)+?(\d+)(:\d+)?/o){
		$CF{'timezone'}=sprintf("-%02d:%02d",$2?$2:0,$3?$3:0);
		$CF{'timeOffset'}=-($2?$2*3600:0)-($3?$3*60:0);
	}else{
		$CF{'timezone'}='Z';$CF{'timeOffset'}=0;
	}
	$CF{'TZ'}=$envtz;
	return$CF{'timeOffset'};
}


#-------------------------------------------------
# パスワード暗号化
#
sub mircrypt{
=item 引数
$ 乱数の種（time形式時刻）
$ 暗号化する文字列
;
$ 比べるパスワード
=cut
	srand($_[0]);
	my$seed=join('',('a'..'z','.',0..9,'/','A'..'Z')[rand(64),rand(64)]);
	my$pass='';
	for($_[1]=~/.{1,8}/go){
		length$_||next;
		$pass.=substr(crypt($_,$seed),2);
	}
	return$_[2]?($_[2]eq$pass?1:undef):$pass;
}


#-------------------------------------------------
# 記事スレッドファイル削除
#
sub delThread{
=item 引数
$ 削除方式
@ 削除するファイルの記事スレッド番号のリスト
=cut
	my($type,@del)=@_;
	if('gzip'eq$type&&$CF{'gzip'}){
		#GZIP圧縮
		for(@del){
			`$CF{'gzip'} -fq9 "$CF{'log'}$_.cgi"`;
			($?==0)||die"$?:Can't use gzip($CF{'gzip'}) oldlog($_.cgi)[$!]";
		}
	}elsif('unlink'eq$type){
		#削除
		for(@del){
			unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog($_.cgi)[$!]";
		}
	}elsif('rename'eq$type){
		#ファイル名変更
		for(@del){
			-e"$CF{'log'}$_.bak.cgi"||die"Can't delete old-oldlog, before renaming($_.bak.cgi)[$!]";
			rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")||die"Can't rename oldlog($_.cgi)[$!]";
		}
	}elsif($type=~/!(.*)/o){
		#特殊
		for(@del){
			`$1 "$CF{'log'}$_.cgi"`;
			$?==0||die"$?:Invalid delete type($1) oldlog($_.cgi)[$!]";
		}
	}else{
		die"Invalid delete type:'$type'";
	}
	
	#非拡張子cgiのファイルを拡張子cgiにする
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	for(readdir(DIR)){
		$_=~/^\d+(\.gz)?\.cgi$/io&& next;
		$_=~/^(\d+)(?:\.(?:cgi|bak|(gz)))+$/io|| next;
		if($2){
			#既にgzipされているもの
			rename("$CF{'log'}$_","$CF{'log'}$1.gz.cgi")||die"Can't rename oldfile($_)[$!]";
		}elsif('gzip'eq$type){
			#gzipされてないもの->.gz.cgi
			`$CF{'gzip'} -fq9 "$CF{'log'}$_"`;
			$?==0||die"$?:Can't use gzip($CF{'gzip'}) oldfile($_)[$!]";
			rename("$CF{'log'}$_.gz","$CF{'log'}$1.gz.cgi")||die"Can't rename oldfile($_)[$!]";
			next;
		}else{
			#.bak->.bak.cgi
			$_=~/^\d+\.bak\.cgi$/io&& next;
			rename("$CF{'log'}$_","$CF{'log'}$1.bak.cgi")||die"Can't rename oldfile($_)[$!]";
		}
	}
	closedir(DIR);
	return($type);
}


#-------------------------------------------------
# 記事編集中継
#
sub rvsij{
	#データを戻す
	$CK{'body'}=~s/<BR\b[^>]*>/\n/gio;
	$CK{'body'}=~s/&/&#38;/go;

	#data->form変換
	if('ALLALL'eq$CF{'tags'}){
	}else{

=item 自動でつけたタグを消す

前提として、タグとして使われる以外の'<','>'は存在してはなりません
ログに書き込まれる時点で属性中の<>は&#60;&#62;になっていることとします

また、この時点で存在するタグは、
1.利用者が入力したタグ（許可タグ）
2.自動リンクによるタグ		/<A class="autolink"[^>]*>/
3.記事番号リンクによるタグ	/<A class="autolink"[^>]*>/
4.語句強調によるタグ		/<STRONG  clAss="[^"]*"[^>]*>/
このうち、1は "'<> をエスケープし、2,3,4は削除します

=cut

		my$str=$CK{'body'};
		{ #Aタグ
			my@floor;
			$str=~s{(<(\/?)A\b([^>]*)>)}
			{
				if(!$2){ #開きタグ
					if($3=~/^\s+cl[aA]ss="autolink"/o){push(@floor,1);'';}
					else{push(@floor,0);$1;}
				}else{ #閉じタグ
					if(!@floor){last;}
					elsif(pop@floor){'';}
					else{$1;}
				}
			}egio;
			$CK{'body'}=$str;
		}
		$str=$CK{'body'};
		{ #STRONGタグ
			my@floor;
			$str=~s{(<(\/?)STRONG\b([^>]*)>)}
			{
				if(!$2){ #開きタグ
					if($3=~/^\s+cl[aA]ss="[^"]*"(?:\x20\x20)?$/o){push(@floor,1);'';}
					else{push(@floor,0);$1;}
				}else{ #閉じタグ
					if(!@floor){last;}
					elsif(pop@floor){'';}
					else{$1;}
				}
			}egio;
			$CK{'body'}=$str;
		}
	}
	$CK{'body'}=~s/"/&#34;/go;
	$CK{'body'}=~s/'/&#39;/go;
	$CK{'body'}=~s/</&#60;/go;
	$CK{'body'}=~s/>/&#62;/go;
	#子記事：親記事
	'0'eq$CK{'j'}?&prtfrm:&chdfrm;
}


#-------------------------------------------------
# RFC1123形式の日付を解析
#
sub parse_rfc1123() {
#http://www.faireal.net/articles/3/16/#d10908
=item
$ RFC1123形式の日付
=cut
	my$date=shift();
	my%month=qw(Jan 1 Feb 2 Mar 3 Apr 4 May 5 Jun 6 Jul 7 Aug 8 Sep 9 Oct 10 Nov 11 Dec 12);
	my($day,$mon,$year,$hour,$min,$sec)=(split(/[ :]/o,$date))[1..6];
	$mon=$month{$mon};
	$mon||return 0;
	my($_Y, $_M, $_D)=($year,$mon,$day+$hour/24+$mon/1440+$sec/86400);
	if($mon==1||$mon==2){
		$_Y=$year-1;
		$_M=$mon+12;
	}
	my $a=int($year/100);
	return(
		int(365.25*($_Y+4716))+int(30.6001*($_M+1))+$_D+(2-$a-int($a/4))-1524.5,
		$year,$mon,$day,$hour,$min,$sec);
}


#-------------------------------------------------
# 初期設定
#
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\nX-Moe: Mireille\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\ngetlogin\t: ".getlogin;
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		};
	}
	# Revision Number
	$CF{'Core'}=q$Revision$;
	$CF{'CoreName'}=q$Name$;
	$CF{'Core'}=~/(?:\d+.)+(\d+)/o;
	$CF{'Version'}='1.2.4';
}

1;
__END__
