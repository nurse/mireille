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
#use strict;
#use vars qw(%CF %IC %IN %CK);
my(%Z0,@zer2,@file);

=pod core.cgiを単体起動させると、locationで跳ばせるCGIに
# この機能を使うには上の行を # で #=item とコメントアウトしてください
if($CF{'program'}eq __FILE__){
	#直接実行だったら動き出す
	&locate($ENV{'QUERY_STRING'});
}
=pod
=cut

#-------------------------------------------------
# MAIN SWITCH
#
sub main{
	#ログファイルちゃんとある？
	defined$CF{'log'}||die q($CF{'log'} is Undefined);
	unless(-e"$CF{'log'}0.cgi"){
		-e"$CF{'log'}0.pl"&&die"旧形式0.plが残っています 不具合の兆し？";
		!-e"$CF{'log'}"&&!mkdir("$CF{'log'}",0777)&&die"Can't read/write/create LogDir($CF{'log'})[$?:$!]";
		open(ZERO,'+>>'."$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$?:$!]";
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
	
	if($CF{'readOnly'}&&$IN{'_isEditing'}){
		#閲覧専用モード
		&showUserError('現在この掲示板は閲覧専用モードに設定されています');
	}else{
		#記事書き込み
		defined$IN{'body'}&&&writeArticle;
		#返信
		$IN{'i'}&&&res;
		#新規書き込み
		defined$IN{'j'}&&(&showHeader,&getCookie,&prtfrm,(print&getFooter),exit);
		#記事修正リストor実行
		defined$IN{'rvs'}&&(index($IN{'rvs'},'-')+1?&rvsArticle:&showRvsMenu);
		#記事削除リストor実行
		defined$IN{'del'}&&(index($IN{'del'},'-')+1?&delArticle:&showRvsMenu);
	}
	#検索
	defined$IN{'seek'}&&&showArtSeek;
	#ヘルプ
	defined$IN{'help'}&&(require($CF{'help'}?$CF{'help'}:'help.pl'))&&exit;
	#アイコン
	defined$IN{'icct'}&&require($CF{'icct'}?$CF{'icct'}:'iconctlg.cgi')&&&iconctlg&&exit;
	#ホーム
	defined$IN{'home'}&&&locate($CF{'home'});
	#記事表示
	&showCover;
	exit;
}


#------------------------------------------------------------------------------#
# MAIN ROUTINS
#
# main直下のサブルーチン群

#-------------------------------------------------
# 表紙表示
#
sub showCover{
	#-----------------------------
	#Cookie取得＆書き込み
	&getCookie?&setCookie(\%CK):($CK{'time'}=$^T-$CF{'newnc'});

	#-----------------------------
	# HTTP,HTML,PAGEヘッダーを表示
	&showHeader;

	#-----------------------------
	#新規投稿フォームを表示する（設定による）
	$CF{'prtwrt'}&&&prtfrm;
	print$CF{'note'};
	#記事ナビボタン
	&artnavi('button');

	#-----------------------------
	#ページ処理
	&logfiles($CF{'sort'});
	!@file&&push(@file,0);
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
	grep{$zer2[$_-$zer2[0]]>$CK{'time'}}grep{$_>$zer2[0]}@file;

	#-----------------------------
	#未読記事のあるスレッド
	my$unread='';
	if(@view){
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
	$#view&&!$view[$#view]&&pop@view;
	for(0..$#view){
		$this.='<A href="#art'.$view[$_].'" title="Alt+'.($_+1).'">'
			.($NEW{"$view[$_]"}?qq(<SPAN class="new">$view[$_]</SPAN>):$view[$_]).'</A> ';
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
		my$unreads=1;
		for(0..$#view){
			$unreads+=&showArticle(i=>$view[$_],ak=>($_+1)
								,-maxChildsShown=>$CF{'maxChildsShown'},-unreads=>$unreads);
		}
	}else{
		#log0のみ つまり設置直後のとき
		&showArticle(i=>0,ak=>1);
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
	print&getFooter;
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
	#コマンドの読み込み
	my%EX;
	for(split(';',$IN{'cmd'})){
		my($i,$j)=split('=',$_,2);
		$i||next;
		$i=~/(\S+(?:\s+\S+)*)/o||next;
		$i=$1;
		$j=defined$j&&$j=~/(\S+(?:\s+\S+)*)/o?$1:'';
		$EX{$i}=$j;
	}
	
	#-----------------------------
	#スレッドのロック
	if($EX{'lockThread'}&&$IN{'i'}){
		open(RW,'+<'."$CF{'log'}$IN{'i'}.cgi")
		||die"Can't read/write log($IN{'i'};.cgi)[$?:$!]";
		eval{flock(RW,2)};
		seek(RW,0,0);
		my@log=map{m/^([^\x0D\x0A]*)/o}<RW>;
		
		my$isLocked=index($log[$#log],"Mir12=\tLocked")>-1;
		my$lockedBy=$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*lockedBy=(\S+)[ ;]/o?$1:'';
		
		#権限をチェック
		if($CF{'admps'}and$IN{'pass'}eq$CF{'admps'}||$IN{'oldps'}eq$CF{'admps'}){
			$lockedBy='Admin';
		}elsif($isLocked&&'ThreadBuilder'ne$lockedBy){
			die'一般ユーザーはこのスレッドのロックを解除できません。';
		}else{
			#親記事のパスワード
			my%DT=$log[0]=~/([^\t]*)=\t([^\t]*);\t/go;
			&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})||die'あなたはこのスレッドをロックできません。';
			$lockedBy='ThreadBuilder';
		}
		
		#ロックオプション
		my$option='';
		my@options=('revise','delete');
		$EX{'lockThread'}=' '.lc($EX{'lockThread'}).' ';
		if(index($EX{'lockThread'},' all ')+1){
			$option=join" ",@options;
		}else{
			$option=join" ",grep{index($EX{'lockThread'}," $_ ")+1}@options;
		}
		$option.=" lockedBy=$lockedBy";
		
		#ロック
		if($isLocked){
			#ロックされている時は解除→pop
			index(pop@log,"Mir12=\tLocked")+1||die'Mireilleのスレッドロック機能にバグがあります。';
		}else{
			#されていない時はロックする→push
			push(@log,"Mir12=\tLocked:$option;\t");
		}
		truncate(RW,0);
		seek(RW,0,0);
		print RW map{"$_\n"}@log;
		close(RW);
		
		#修正モードに移動
		$IN{'page'}=1;
		$IN{'rvs'}='';
		&showRvsMenu(sprintf"第$IN{'i'}番スレッドのロック%s成功",$isLocked?'解除':'');
	}
	
	#-----------------------------
	#コマンドの処理

=pod コマンドで使えるもの

:icon
  「icon = <password>」
  専用アイコン
:iconlist
  「iconlist = (nolist|economy)」
  :nolist
    アイコンリストを読み込まない
  :economy
    アイコンリストを読み込むけれど、表示しない
:absoluteIcon
  「absoluteIcon = <absoluteUrl>」
  絶対指定アイコン
:relativeIcon
  「relativeIcon = <relativeUrl>」
  相対指定アイコン
  （相対指定の基準は$CF{'icon'}です）
:signature
  「signature = <seed of signature>」
  「署名のもと」を指定

:usetag
  !SELECTABLE()で許可してある範囲内で使うタグを選べる
:notag
  タグを使わない
:noautolink
  URI自動リンクを使わない
:noartno
  記事番号リンクを使わない
:nostrong
  語句強調を使わない

:dnew
  記事の投稿日時を更新します
:znew
  スレッドの最終変更日時を更新します
:renew
  dnewとznewを同時に行います

:lockArticle
  記事をロックします
:lockThread
  「lockThread = (all| (revise|delete).. )」
  スレッドをロックします。
  管理パスワードか、親記事のパスワードを使って、
  ロックしたいスレッドに返信するとロックできます
  オプションを指定しない場合は、そのスレッドに対する返信がロックされます。
  :all
    全てのオプションをオン
  :revise
    修正をロック
  :delete
    削除をロック

#未実装
su:	管理パスワードを入れておくと、返信できないスレッドに返信できたりする（ようになる予定）

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

	my@settings=qw(icon iconlist absoluteIcon relativeIcon signature);
	my@writeSettings=qw(usetag notag noautolink noartno nostrong);
	my@oneTimeCommands=qw(dnew znew renew lockArticle);
	
	defined$EX{$_}&&!$EX{$_}&&($EX{$_}=1)for@writeSettings,@oneTimeCommands;
	$IN{'cmd'}=join(';',(map{"$_=$EX{$_}"}grep{$EX{$_}}@settings),(grep{$EX{$_}}@writeSettings));
	
	#専用アイコン機能。index.cgiで設定する。
	#index.cgiで指定したアイコンパスワードに合致すれば。
	$IN{'icon'}=$IC{$EX{'icon'}}if$CF{'exicon'}&&$IC{$EX{'icon'}};
	
	#絶対指定アイコン
	$IN{'icon'}=''if$CF{'absoluteIcon'}&&$EX{'absoluteIcon'};
	#相対指定アイコン
	$IN{'icon'}=$EX{'relativeIcon'}if$CF{'relativeIcon'}&&$EX{'relativeIcon'};
	
	#renewはdnew&&znew
	$EX{'dnew'}=$EX{'znew'}=1if$EX{'renew'};
	
	#-----------------------------
	#エラー表示
	{
		my@error=();
		my@message=();
		$IN{'name'}||push(@error,'名前');
		$IN{'body'}||push(@error,'本文');
		$IN{'pass'}||($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'})
		or push(@error,'パスワード')&&push(@message,'パスワードは8文字以上、128文字以下でなければなりません。');
		if($CF{'ngWords'}&&!@error){
			my$eucpre=qr{(?<!\x8F)};
			my$eucpost=qr{(?=(?:[\xA1-\xFE][\xA1-\xFE])*(?:[\x00-\x7F\x8E\x8F]|\z))};
			my%item=(body=>'本文',subject=>'題名',name=>'名前');
			for(keys%item){
				my$item=$IN{$_};
				my$err=$item{$_};
				study$item;
				for($CF{'ngWords'}=~/\S+/go){
					$item=~/$eucpre$_$eucpost/||next;
					push(@error,$err);
					last;
				}
				@error&&last;
			}
			push(@message,'Something Wicked happend!(不正な文字列)')if@error;
		}
		if(@error){
			&showHeader;
			print<<"_HTML_";
<H2 class="heading2">- Write Error -</H2>
<P>@{[join('と',map{qq(<SPAN style="color:#f00">$_</SPAN>)}@error)]}をちゃんと入力してください</P>
_HTML_
			printf'<P>%s</P>',join'<BR>',@message if@message;
			%CK=%IN;
			&rvsij;
			print&getFooter;
			exit;
		}
	}
	
	#-----------------------------
	#本文の処理
	#form->data変換
	unless(defined$IN{'body'}&&length$IN{'body'}){
		$IN{'body'}='';
	}elsif($CF{'tags'}&&'ALLALL'eq$CF{'tags'}){
		#ALLALLは全面OK。但し強調は無効。URI自動リンクも無効。
		#自前でリンクを張ったり、強調してあるものを、二重にリンク・強調してしまいますから
	}else{
		#本文のみタグを使ってもいい設定にもできる
		my$attrdel=0;#属性を消す/消さない(1/0)
		my$str=$IN{'body'};
		study$str;
		$str=~tr/"'<>/\01-\04/;
		$str=~s/&(#?\w+;)/\05$1/go;
		
		#タグ処理
		if($CF{'tags'}&&!$EX{'notag'}){
			my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
			my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
			my$text_regex='[^\03]*';
			
			my$tags=$CF{'tags'};
			my%tagCom=map{m/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
			if($tagCom{'!SELECTABLE'}){
				$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{m/\w+/}split(/\s+/,$EX{'usetag'}));
			}elsif(defined$tagCom{'!SELECTABLE'}){
				$tags='\w+';
			}
			
			my$result='';
			#もし BRタグや Aタグなど特定のタグだけは削除したくない場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/io;
			my$remain=join('|',grep{m/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
			#逆に FONTタグや IMGタグなど特定のタグだけ削除したい場合には， 
			#$tag_tmp = $2; の後に，次のようにして $tag_tmp を $result に加えるようにすればできます． 
			#$result .= $tag_tmp if $tag_tmp !~ /^<\/?(FONT|IMG)(?![\dA-Za-z])/io;
			my$pos=length$str;
			while($str=~/\G($text_regex)($comment_tag_regex|\03$tag_regex_)?/gso){
				$pos=pos$str;
				($1&&length$1)||($2&&length$2)||last;
				$result.=$1;
				my$tag_tmp=$2;
				if($tag_tmp=~s/^\03((\/?(?:$remain))(?![\dA-Za-z]).*)\04/<$1>/io){
					$tag_tmp=~tr/\01\02/"'/;
					$result.=$attrdel?"<$2>":$tag_tmp;
				}else{
					$result.=$tag_tmp;
				}
				if($tag_tmp=~/^<(XMP|PLAINTEXT|SCRIPT)(?![\dA-Za-z])/io){
					$str=~/(.*?)(?:<\/$1(?![\dA-Za-z])$tag_regex_|$)/gsi;
					(my$tag_tmp=$1)=~tr/\01-\04/"'<>/;
					$result.=$tag_tmp;
				}
			}
			$str=$result.substr($str,$pos);
		}else{
			#許可タグ無しorCommand:notag
		}
		
		#記事番号リンク「>>No.12-6」
		$str=~s{(\04\04No\.(\d+)(-\d+)?)}{<A class="autolink" href="index.cgi?read=$2#art$2$3">$1</A>}go
			if$CF{'noartno'}||!$EX{'noartno'};
		
		#語句強調
		if($CF{'strong'}&&!$EX{'nostrong'}){
			my%ST=map{(my$s=$_)=~tr/"'<>&/\01-\05/;$s}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
			if($CF{'strong'}=~/^ /o){
				#拡張語句強調
				for(sort{length$b<=>length$a}keys%ST){
					if(/^\/(.+)\/$/o){
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
			#実稼動部
			my$href_regex=qr{($http_URL_regex|$ftp_URL_regex|($mail_regex))};
			my@isMail=('<A class="autolink" href="mailto:','<A class="autolink" href="');
			$str=~s{((?:\G|>)[^<]*?)$href_regex}{$1$isMail[!$3]$2" target="_blank">$2</A>}go;
			if($str=~/<(?:XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z])/io){
				#XMP/PLAINTEXT/SCRIPTタグがあるとき
				$str=~s{(<(XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z]).*?(?:<\/$2\s*>|$))}
				{(my$element=$1)=~s/<A class="autolink"[^>]+>(.*?)<\/A>/$1/gos;$element}egios;
			}
		}else{
			#Command:nolink
		}
		
		$str=~s/&/&#38;/go;
		$str=~s/\01/&#34;/go;
		$str=~s/\02/&#39;/go;
		$str=~s/\03/&#60;/go;
		$str=~s/\04/&#62;/go;
		$str=~tr/\05/&/;
		$IN{'body'}=$str;
	}
	$IN{'body'}=~s/\t/&nbsp;&nbsp;/go;
	$IN{'body'}=~s/\n/<BR>/go;
	
	#-----------------------------
	#書き込むデータの前処理
	my$crcOfThisArticle=&getCRC32($IN{'body'});
	$IN{'_Signature'}=&getSignature($EX{'signature'}||$IN{'pass'},$EX{'signature'});
	
	#-----------------------------
	#ZERO情報の取得
	open(ZERO,'+<'."$CF{'log'}0.cgi")||die"Can't read/write log(0.cgi)[$?:$!]";
	eval{flock(ZERO,2)};
	seek(ZERO,0,0);
	my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
	index($zero[0],"Mir12=\t")+1||die"ZEROのログ形式がMir12型以外です";
	%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
	my@zer1=split(/\s+/o,$zero[1]);
	@zer2=$zero[2]?split(/\s/o,$zero[2]):(0);
	
	#-----------------------------
	#@zer1ベース荒らし対策(?)
	#120秒以内に@zer1が全て入れ替わったら危険の兆候
	$zer1[$#zer1]=~/\d+:\w+:\d+\[(\d+)\]/o&&$1+120>$^T&&&showUserError('天文官が凶兆を知らせてきた');
	
	#-----------------------------
	#@zer2のエラー訂正
	for(@file){
		$_>$zer2[0]||next; #既に古くなったもの
		$zer2[$_-$zer2[0]]&&next; #正常
		
		#以下異常なものの復旧
		$zer2[$_-$zer2[0]]=(stat("$CF{'log'}$_.cgi"))[9];
	}
	
	#-----------------------------
	#現在あるログのリストを取得
	&logfiles('number');
	$IN{'i'}=$file[0]+1if$IN{'i'}&&$IN{'i'}>$file[0]+1;
	
	#-----------------------------
	#書き込みの前処理を拡張したい時用
	&exprewrt();
	
	#-----------------------------
	#いよいよ
	unless($IN{'_ArticleType'}&2){
		#新規・返信書き込み
		$IN{'_NewPassword'}=&mircrypt($^T,$IN{'pass'});
		$EX{'znew'}=1;
		if($IN{'i'}&&$zero[1]=~/($IN{'i'}):$crcOfThisArticle:([1-9]\d*)/
			or length$IN{'j'}&&$zero[1]=~/(\d+):$crcOfThisArticle:($IN{'j'})/){
			&showHeader;
			print<<"_HTML_";
<H2 class="heading2">- 多重投稿？ -</H2>
<DIV class="center">
<P style="margin:0.6em">今投稿された記事の内容は<A href="index.cgi?read=$1#art$1-$2" title="該当記事を確認する">第$1番スレッドの$2番目</A>と同一内容だと思われます<BR>
該当記事を確認して、同一内容でない場合は、下のフォームで少し修正してから投稿してみてください。</P>
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="index.cgi?read=$1#art$1-$2" method="get">
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
			print&getFooter;
			exit;
		}elsif(!$IN{'_ArticleType'}){
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
最も記事スレッド番号が小さなものの、記事スレッド番号をあらわす

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
			open(WR,'+>>'."$CF{'log'}$IN{'i'}.cgi")||die"Can't write log($IN{'i'})[$?:$!]";
			eval{flock(WR,2)};
			die"書き込み処理中に割り込まれました($CF{'log'}$IN{'i'}.cgi)"if-s"$CF{'log'}$IN{'i'}.cgi";
			truncate(WR,0);
			seek(WR,0,0);
			print WR "Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$^T;\t"
			."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}($CF{'prtitm'}=~/\+([a-z\d]+)\b/go))."\n";
			close(WR);
		}else{
			#-----------------------------
			#返信書き込み
			open(RW,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
			eval{flock(RW,2)};
			seek(RW,0,0);
			my$line;
			$line=$_ while<RW>;
			
			#スレッドのロック
			index($line,"Mir12=\tLocked")+1&&&showUserError('このスレッドはロックされている');
			
			$IN{'j'}=$.; #$.-1+1
			seek(RW,0,2);
			if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
				#パスワードが管理パスのときは最大子記事数制限がかかっていても投稿出来る
			}elsif($CF{'maxChilds'}&&$IN{'j'}>$CF{'maxChilds'}){
				&showUserError('既に最大子記事数制限を越えている');
			}
			print RW (!chomp$line&&++$IN{'j'}?"\n":'')
			."Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$^T;\t"
			."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}$CF{'chditm'}=~/\+([a-z\d]+)\b/go)."\n";
			close(RW);
		}
		
		#-----------------------------
		#MailNotify
		if($CF{'mailnotify'}){
			#新規/返信があった場合はメールを送る
			require'notify.pl';
			&mailnotify(%IN);
		}
		
	}else{
		#-----------------------------
		#修正書き込み
		open(RW,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
		eval{flock(RW,2)};
		seek(RW,0,0);
		my@log=map{m/^([^\x0D\x0A]*)/o}<RW>;
		$#log<$IN{'j'}&&die'Something Wicked happend!(jが大きすぎ)';
		$log[$IN{'j'}]||die'Something Wicked happend!(修正でないj)';
		my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
		
		#PasswordCheck
		if($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){
			#MasterPassによる
			if($IN{'pass'}){
				#Pass変更
				$IN{'oldps'}=$IN{'pass'};
			}else{
				#Passそのまま
				$IN{'_NewPassword'}=$DT{'pass'};
			}
		}else{
			#UserPassによる
			unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
				&showHeader;
				print qq(<H2 class="heading2">Password Error</H2>\n);
				%CK=%IN;
				&rvsij;
				print&getFooter;
				exit;
			}
			index($log[$IN{'j'}],"Mir12=\tdel")+1&&&showUserError("第$IN{'i'}番の$IN{'j'}は既に削除されている");
			index($log[$IN{'j'}],"Mir12=\tlock")+1&&&showUserError("第$IN{'i'}番の$IN{'j'}はロックされている");
			$log[$#log]=~/Mir12=\tLocked(?:\S+ )*revise[ ;]/o&&&showUserError('このスレッドは固くロックされている');
			#Pass変更
			$IN{'oldps'}=$IN{'pass'};
		}
		
		#記事のロック
		$IN{'Mir12'}='lock:'if$EX{'lockArticle'};
		
		unless($IN{'_NewPassword'}){
			#Pass変更・日時変更
			$EX{'dnew'}&&($DT{'time'}=$^T);
			$IN{'_NewPassword'}=&mircrypt($DT{'time'},$IN{'pass'});
		}
		#書き込み
		$log[$IN{'j'}]=
			"Mir12=\t$IN{'Mir12'};\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$DT{'time'};\t"
			."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
			.join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}
			((!$IN{'j'}?$CF{'prtitm'}:$CF{'chditm'})=~/\+([a-z\d]+)\b/go));
		truncate(RW,0);
		seek(RW,0,0);
		print RW map{"$_\n"}@log;
		close(RW);
	}
	
	if($EX{'znew'}){
		#-----------------------------
		#ログ管理ファイル、0.cgiに書き込み
		#新規・返信の時には投稿情報を保存
		$#zer1=3if$#zer1>3; #(3+2=)5が@zer1の保存件数
		unshift(@zer1,sprintf"%d:%s:%d[%d]",$IN{'i'},$crcOfThisArticle,$IN{'j'},$^T);
		my$No=$IN{'i'}-$zer2[0];
		$No>0||die"ZER2のデータが不正です 'i':$IN{'i'},'zer2':$zer2[0]";
		$zer2[$No]=$^T;
		truncate(ZERO,0);
		seek(ZERO,0,0);
		unless($Z0{'Serial'}){
			srand();
			$Z0{'Serial'}=1+int(rand(-2+2**32));
		}
		print ZERO 
			"Mir12=\t$IN{'i'}-$IN{'j'};\tsubject=\t$IN{'subject'};\tname=\t$IN{'name'};\ttime=\t$^T;\t"
			."Serial=\t$Z0{'Serial'};\t\n@zer1\n@zer2\n";
	}
	close(ZERO); #ここでやっと書き込み終了
	
	#-----------------------------
	#$IN{'cook'}がONならCookieの書き込み
	if($IN{'cook'}){
		unless($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){#管理パスの時はCookie保存しない
			&getCookie;
			&setCookie(\%IN);
		}
	}
	
	#-----------------------------
	#書き込み成功＆「自由に修正をどうぞ」
	&showHeader;
	print<<"_HTML_";
<H2 class="heading2">- 書き込み完了 -</H2>
<DIV class="writingMessage">
<P>以下の内容で第$IN{'i'}番スレッドの$IN{'j'}番目に書き込みました。<BR>
これでよければそのままTOPや掲示板に戻ってください。<BR>
修正したい場合は以下のフォームで修正して投稿してください。</P>

<DIV class="box"><P class="heading3">--- PREVIEW ---</P><P class="body">$IN{'body'}</P></DIV>

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
	print&getFooter;
	exit;
}


#-------------------------------------------------
# 記事返信
#
sub res{
	&getCookie;
	&showHeader;
	print qq(<H2 class="heading2">- 記事返信モード -</H2>\n)
	.qq(<DIV id="threadBox">\n)
	.qq(<H3 class="heading3">このスレッドの今までの内容</H3>\n);
	print"This thread$IN{'i'} is deleted."if&showArticle(i=>$IN{'i'},ak=>1,res=>1)eq'del';
	print<<'_HTML_';
</DIV>
<P id="paragraphThreadBox">
<LABEL for="inpDivHeight">枠の高さ:
<INPUT type="text" id="inpDivHeight" value="400px"></LABEL>
<INPUT type="button" class="button" onclick="setDivHeight();return false" value="高さ設定">
<INPUT type="button" class="button" id="inpDivBorder" onclick="switchDivBorder(this);return false" value="枠を狭める">
</P>
<SCRIPT type="text/javascript">
<!--
/* ========== 枠の高さ設定 ========== */
function setDivHeight(){
	if(!document.getElementById)return false;
	var div=document.getElementById('threadBox');
	var but=document.getElementById('inpDivBorder');
	var inp=document.getElementById('inpDivHeight');
	if(!div.style||!div.style.height)return false;
	but.value='枠を広げる';
	div.style.height=inp.value=inp.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
	div.style.overflow='auto';
}

/* ========== 枠を広げたり狭めたり ========== */
function switchDivBorder(self){
	if(!document.getElementById)return false;
	var div=document.getElementById('threadBox');
	var inp=document.getElementById('inpDivHeight');
	if(!div.style||!div.style.overflow){
		return false;
	}else if(div.style.height=='auto'){
		self.value='枠を広げる';
	div.style.height=inp.value=inp.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
		div.style.overflow='auto';
	}else{
		self.value='枠を狭める';
		div.style.height='auto';
		div.style.overflow='visible';
	}
}

/* ========== 枠を初期化 ========== */
function initDiv(){
	if(!document.getElementById)return false;
	var div=document.getElementById('threadBox');
	var but=document.getElementById('inpDivBorder');
	var inp=document.getElementById('inpDivHeight');
	if(!div.style||!div.style.height)return false;
	but.value='枠を広げる';
	div.style.height=inp.value=inp.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
	div.style.overflow='auto';
}

/* ==========  ========== */
//initDiv();
-->
</SCRIPT>

_HTML_
	$CK{'i'}=$IN{'i'};
	$CK{'ak'}=1;
	&chdfrm;
	print&getFooter;
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
	if(defined$IN{'rvs'}){$mode='rvs';print qq(<H2 class="heading2">- 記事修正モード -</H2>\n);}
	elsif(defined$IN{'del'}){$mode='del';print qq(<H2 class="heading2">- 記事削除モード -</H2>\n);}
	else{print qq(<H2 class="heading2">Something Wicked happend!(modeが不明)</H2>).&getFooter;exit;}
	#処理成功-Coverに戻る
	if($_[0]){
		print<<"_HTML_";
<DIV class="center">
<H3 class="heading3">$_[0]</H3>
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
	}
	#ログ処理
	&logfiles('number');
	my$pgslct=&pgslct($#file,$CF{'delpg'},$mode);
	my@thisPage=@file;
	@thisPage=splice(@thisPage,($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});
	$thisPage[$#thisPage]==0&&pop@thisPage;
	print<<"_HTML_";
<DIV class="center">$pgslct</DIV>

<FORM id="List" method="post" action="index.cgi">
<DIV class="center"><TABLE border="1" cellspacing="0" class="list" summary="List" width="80%">
<COL style="width:5em">
<COL style="width:17em">
<COL>
<TR>
<TD style="text-align:center">[$thisPage[0]-$thisPage[$#thisPage]]</TD>
<TD><SPAN class="ak">P</SPAN>assword: <INPUT name="pass" type="text"
 accesskey="p" size="12" style="ime-mode:inactive" value="$CK{'pass'}"></TD>
<TD>
<INPUT name="$mode" type="hidden" value="">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</TD></TR>
_HTML_
	#ログスレッドごと
	for(@thisPage){
		$_&&-e"$CF{'log'}$_.cgi"||next;
		my$i=$_;
		my$j=-1;
		open(RD,'<'."$CF{'log'}$i.cgi")||die"Can't read log($i.cgi)[$?:$!]";
		eval{flock(RD,1)};
		my$count="<A href=\"index.cgi?read=$i#art$i\">第$i号</A>";
		#記事ごと
		while(<RD>){
			$j++;
			index($_,"Mir12=\tdel;\t")+1&&next;
			if(index($_,"Mir12=\tLocked")+1){
				print<<"_HTML_";
<TR class="child">
<TH align="right">LOCKED</TH>
<TD align="right" colspan="2">このスレッドはロックされています</TD>
</TR>
_HTML_
				last;
			}
			my%DT=/([^\t]*)=\t([^\t]*);\t/go;
			$count="Res $j"if$j;
			my$No="$i-$j";
			my$date=&date($DT{'time'});
			#本文の縮め処理
			$DT{'body'}=~s/<BR\b[^>]*>/↓/go;
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
	print&getFooter;
	exit;
}


#-------------------------------------------------
# 記事を修正
#
sub rvsArticle{
	($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});
	open(RD,'<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read log($IN{'i'}.cgi)[$?:$!]";
	eval{flock(RD,1)};
	my@log=map{m/^([^\x0D\x0A]*)/o}<RD>;
	close(RD);
	my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
	%DT||die"第$IN{'i'}番スレッドには$IN{'j'}なんてありません";
=pod
たとえ$IN{'pass'}が渡されなくても、GetCookieでCookieを参照し、
もしそこで得られた$CK{'pass'}がパスワードと一致すれば修正モードに通す、
というようにして利便性の向上を図っている。
当然パスワードが一致しなければ入力するように要請する。
=cut
	if($IN{'pass'}){
		#INで送られてきた？
		$IN{'oldps'}=$IN{'pass'};
		if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
			#ADMINpassOK
			$IN{'pass'}='';
			#処理へ
		}else{
			index($DT{'Mir12'},'lock')+1&&&showRvsMenu("第$IN{'i'}番の$IN{'j'}はロックされています。");
			#権限をチェック
			if($log[$#log]=~/Mir12=\tLocked:(?:\S+ )*revise[ ;]/o){
				$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*lockedBy=(\S+)[ ;]/o;
				'ThreadBuilder'eq$1||&showRvsMenu('このスレッドは固くロックされています。');
				my%parent=$log[0]=~/([^\t]*)=\t([^\t]*);\t/go;
				&mircrypt($parent{'time'},$IN{'pass'},$parent{'pass'})
					or&showRvsMenu('このスレッドは固くロックされています。');
			}
			&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
				or&showRvsMenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。");
			#INpassOK
			#処理へ
		}
	}else{
		#Cookieを調べる前にロックされているかどうかチェック
		index($DT{'Mir12'},'lock')+1&&&showRvsMenu("第$IN{'i'}番の$IN{'j'}はロックされています。");
		$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*revise[ ;]/o
			and&showRvsMenu('このスレッドは固くロックされています。');
		
		#Cookieにある？
		&getCookie;
		$IN{'oldps'}=$IN{'pass'}=$CK{'pass'};
		#-----------------------------
		unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
			#無いなら入力して
			&showHeader;
			print<<"_HTML_";
<H2 class="heading2">- 第$IN{'i'}番の$IN{'j'}のパスワード認証 -</H2>
<FORM accept-charset="euc-jp" id="Revise" method="post" action="index.cgi">
<TABLE cellspacing="2" summary="Revise" width="550">
<COL width="50">
<COL width="170">
<COL width="330">
<P style="margin:0.6em">パスワードを入力してください</P>
<P style="margin:0.6em"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" type="text" accesskey="p" size="12" style="ime-mode:inactive" value="$CK{'pass'}">
<INPUT name="rvs" type="hidden" value="$IN{'rvs'}"></P>
<P style="margin:0.6em">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</p>
_HTML_
			print&getFooter;
			exit;
		}
		#CKpassOK
		#処理へ
	}
	#Revise Main Routin
	&showHeader;
	print qq(<H2 class="heading2">- 第$IN{'i'}番の$IN{'j'}の修正モード -</H2>\n);
	%CK=%DT;
	@CK{qw(i j pass oldps)}=@IN{qw(i j pass oldps)};
	&rvsij;
	print&getFooter;
	exit;
}


#-------------------------------------------------
# 記事削除
#
sub delArticle{
	($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});
	open(RW,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
	eval{flock(RD,2)};
	seek(RW,0,0);
	my@log=map{m/^([^\x0D\x0A]*)/o}<RW>;
	my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
	#削除分岐
	SWITCH:{
		if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
			#AdminPassOK
			if($IN{'j'}==0&&!$IN{'type'}){
				#削除する方法無いなら入力して
				&showHeader;
				print<<"_HTML_";
<H2 class="heading2">- 第$IN{'i'}番スレッドの削除 -</H2>
<FORM accept-charset="euc-jp" id="Delete" method="post" action="index.cgi">
<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>スレッドの削除方法を選んでください</LEGEND>
<TD>
<LABEL for="mark">親記事の本文のみ削除<INPUT id="mark" name="del" type="radio" value="$IN{'del'}-1" checked></LABEL>
<LABEL for="$CF{'delthr'}">記事スレッドを削除<INPUT id="$CF{'delthr'}" name="del" type="radio" value="$IN{'del'}-2"></LABEL>
</FIELDSET>

<P style="margin:0.6em">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" class="submit" accesskey="s" value="OK">　
<INPUT type="reset" class="reset" value="キャンセル">
</P>
_HTML_
				print&getFooter;
				exit;
			}
			$IN{'j'}==0&&$IN{'type'}==2&&last SWITCH;
		}else{
			#一般Pass
			index($log[$IN{'j'}],"Mir12=\tdel")+1&&&showRvsMenu("第$IN{'i'}番の$IN{'j'}は既に削除されています。");
			index($log[$IN{'j'}],"Mir12=\tlock")+1&&&showRvsMenu("第$IN{'i'}番の$IN{'j'}はロックされています。");
			$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*delete[ ;]/o
				and&showRvsMenu('このスレッドは固くロックされています。');
			&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
				or&showRvsMenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。");
			$IN{'j'}==0&&$#log==0&&last SWITCH;
		}
		
		#mark
		$log[$IN{'j'}]=~s/^Mir12=\t([^\t]*);\t/Mir12=\tdel;\t/go;
		truncate(RW,0);
		seek(RW,0,0);
		print RW map{"$_\n"}@log;
		close(RW);
		&showRvsMenu("第$IN{'i'}番の$IN{'j'}を削除しました。");
	}
	close(RW);
	#親記事削除
	&delThread($CF{'delthr'},$IN{'i'});
	&showRvsMenu("第$IN{'i'}番スレッドを削除しました。($CF{'delthr'})");
	exit;
}


#-------------------------------------------------
# 全文検索機能
#
sub showArtSeek{
	&showHeader;
	print qq(<H2 class="heading2">- 検索モード -</H2>);
	my%SK=split(/\s+/o,$CF{'sekitm'});
	
	if(length$IN{'seek'}){
		#-----------------------------
		#検索＆結果表示
		my$result='';
		my$item='ALL'eq$IN{'item'}?'':";\t$IN{'item'}";
		my$seek=quotemeta$IN{'seek'};
		
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
				open(RD,'<'."$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$?:$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				close(RD);
#				index($thread,$IN{'seek'})>-1||next;
				$thread=~/$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/o||next;
				$result.=qq(<A href="index.cgi?read=$_#art$_">No.$_</A>\n);
			}
		}else{
			#記事ごと検索
			for(@file){
				$_||last;
				open(RD,'<'."$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$?:$!]";
				eval{flock(RD,1)};
				my$thread;
				read(RD,$thread,-s"$CF{'log'}$_.cgi");
				close(RD);
				index($thread,$IN{'seek'})+1||next;
				my$i=$_;
				my$j=0;
				while($thread=~m/$item=\t[^\t]*$eucpre($seek)$eucpost[^\t]*;\t/go){
					$j=substr($thread,0,pos$thread)=~tr/\n//;
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
	$select=~s/(value="$IN{'item'}")/$1 selected/io;
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
	$select=~s/(value="$IN{'every'}")/$1 checked/io;
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
	print&getFooter;
	exit;
}


#-------------------------------------------------
# ユーザー向けエラー
#
sub showUserError{
	my$message=shift();
	&showHeader;
	print<<"_HTML_";
<H2 class="heading2">- エラーが発生しました -</H2>
<P>ご不便をかけて申し訳ございません<BR>
<span class="warning">$message</span>ため、<BR>正常な処理を続行することができませんでした<BR>
以下に念のため今入力されたデータを羅列しておきます<BR>
重要な情報がある場合、保存しておいて、またの機会に投稿してください</P>
<TABLE border="1" summary="ユーザー入力変数を表示しておく">
<CAPTION>今受け取った引数</CAPTION>
_HTML_
	for(grep{m/^[^_]/o&&defined$IN{$_}&&length$IN{$_}}keys%IN){
		$IN{$_}=~s/<BR>/\n/go;
		printf"<TR><TH>%s</TH><TD><XMP>%s</XMP></TD>\n",$_,$IN{$_};
	}
	print'</TABLE>';
	print&getFooter;
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
	$i||die"'Stay here.'";
	if(!index($i,'http:')){
	}elsif($i){
		$i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
		substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
		$i.=$_[0];
	}
	print<<"_HTML_";
Status: 303 See Other
Pragma: no-cache
Cache-Control: no-cache
Location: $i
Content-Language: ja-JP
Content-type: text/html; charset=euc-jp

<DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
<HEAD>
<META http-equiv="Refresh" content="0;URL=$i">
<TITLE>303 See Ohter</TITLE>
</HEAD>
<BODY>
<H1>: Mireille :</H1>
<P>And, please go <A href="$i">here</A>.</P>
<P>Location: $i</P>
<P>Mireille <VAR>$CF{'Version'}</VAR>.<BR>
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
	my$params;
	my@params=();
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){
		@params=@ARGV;
	}elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
		my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
		print"Status: 200 OK\nLast-Modified: $last\n"
		."Content-Type: text/plain\n\nLast-Modified: $last";
		exit;
	}elsif('POST'eq$ENV{'REQUEST_METHOD'}){
		read(STDIN,$params,$ENV{'CONTENT_LENGTH'});
	}elsif('GET'eq$ENV{'REQUEST_METHOD'}){
		$params=$ENV{'QUERY_STRING'};
	}
	
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	
	#引数をハッシュに
	unless($params){
	}elsif(length$params>262114){ # 262114:引数サイズの上限(byte)
		#サイズ制限
		&showHeader;
		print"いくらなんでも量が多すぎます\n$params";
		print&getFooter;
		exit;
	}elsif(length$params>0){
		#入力を展開
		@params=split(/[&;]/o,$params);
	}
	
	#入力を展開してハッシュに入れる
	my%DT;
	while(@params){
		my($i,$j)=split('=',shift(@params),2);
		$i=~/([a-z][-.:\w]*)/o||next;$i=$1;
		defined$j||($DT{$i}='')||next;
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=$j=~/($eucchar*)/o?$1:'';
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		if('body'ne$i){
			#本文以外は全面タグ禁止
			$j=~s/\t/&nbsp;&nbsp;/go;
			$j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
			$j=~s/"/&#34;/go;
			$j=~s/'/&#39;/go;
			$j=~s/</&#60;/go;
			$j=~s/>/&#62;/go;
			$j=~s/\n+$//o;
			$j=~s/\n/<BR>/go;
		}#本文は後でまとめて
		$DT{$i}=$j;
	}
	
	#引数の汚染除去
	$IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?$1:'';
	$IN{'hua'}=($ENV{'HTTP_USER_AGENT'}&&$ENV{'HTTP_USER_AGENT'}=~/($eucchar+)/o)?$1:'';
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
				}elsif($DT{'oldps'}=~/(.{8,128})/o){
					$IN{'oldps'}=$1;
				}
				$IN{'_ArticleType'}=!$IN{'j'}?2:3;
			}else{
				#新規子記事
				$IN{'_ArticleType'}=1;
			}
		}else{
			#新規親記事
			$IN{'j'}=0;
			$IN{'_ArticleType'}=0;
		}

=item 記事種別

0: 新規親記事
1: 新規子記事
2: 修正親記事
3: 修正子記事

=cut

		$IN{'name'}=&getTruncated($DT{'name'},40);
		$IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{8,128})/o){
			$IN{'pass'}=$1;
		}
		
		{ #フォームの内容処理
			for($CF{$IN{'_ArticleType'}&1?'chditm':'prtitm'}=~/\b([a-z\d]+)\b/go){
				if('color'eq$_){
					$IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?$1:'';
				}elsif('email'eq$_){
					$IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?$1:'';
					$IN{'email'}=~s/\@/&#64;/;
				}elsif('home'eq$_){
					$IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?$1:'';
				}elsif('icon'eq$_){
					$IN{'icon'}=($DT{'icon'}=~/(.+)/o)?$1:'';
				}elsif('cmd'eq$_){
					$IN{'cmd'}=$1 if$DT{'cmd'}=~/(.+)/o;
				}elsif('subject'eq$_){
					$IN{'subject'}=&getTruncated($DT{'subject'}?$DT{'subject'}:$DT{'body'},70);
				}elsif('ra'eq$_||'hua'eq$_){
					next;
				}else{
					$IN{"$_"}=($DT{"$_"}=~/(.+)/o)?$1:'';
				}
			}
		}
		#bodyの処理は基本的に&writeArticleで行う
		$IN{'body'}=$DT{'body'}=~/(.*\S)/os?$1:'';
		$IN{'_isEditing'}=1;
	}elsif(defined$DT{'new'}){
		#新規書き込み
		$IN{'j'}=0;
		$IN{'_isEditing'}=1;
	}elsif(defined$DT{'res'}){
		#返信書き込み
		$IN{'i'}=$1 if$DT{'res'}=~/([1-9]\d*)/o;
		$IN{'_isEditing'}=1;
	}elsif(defined$DT{'seek'}){
		#検索
		$IN{'seek'}=($DT{'seek'}=~/(.+)/o)?$1:'';
		my%SK=split(/\s+/o,$CF{'sekitm'});
		$DT{'item'}=($DT{'item'}=~/(.+)/o)?$1:'';
		$IN{'item'}=($SK{$DT{'item'}})?$DT{'item'}:'ALL';
		$IN{'every'}=($DT{'every'}=~/([ij])/o)?$1:'i';
	}elsif(defined$DT{'del'}){
		#記事削除リストor実行
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{8,128})/o){
			$IN{'pass'}=$1;
		}
		$IN{'del'}=($DT{'del'}=~/([1-9]\d*\-\d+(?:\-\d)?)/o)?$1:'';
		$IN{'_isEditing'}=1;
	}elsif(defined$DT{'rvs'}){
		#記事修正リストor実行
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
		unless($DT{'pass'}){
		}elsif($DT{'pass'}eq$CF{'admps'}){
			$IN{'pass'}=$CF{'admps'};
		}elsif($DT{'pass'}=~/(.{8,128})/o){
			$IN{'pass'}=$1;
		}
		$IN{'rvs'}=($DT{'rvs'}=~/([1-9]\d*\-\d+)/o)?$1:'';
		$IN{'_isEditing'}=1;
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
		require'compact.cgi';
		exit;
	}elsif($DT{'read'}){
		#ログ読み
		$IN{'read'}=$1 if$DT{'read'}=~/([1-9]\d*)/o;
		$IN{'page'}=1; #readで指定された値がおかしいときのため
	}else{
		#ページ
		$IN{'read'}=0;
		$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	}
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
		substr($str,0,$length-3)=~/($eucchar*)/o;
		$1=~/([^&]*(?:&#?\w+;[^&]*)*)/o;
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

	my$lastModified;
	if($CF{'use304'}&&$ENV{'HTTP_IF_MODIFIED_SINCE'}){
		my$client=(&parse_rfc1123($ENV{'HTTP_IF_MODIFIED_SINCE'}))[0];
		my$server=(stat("$CF{'log'}0.cgi"))[9];
		if($client&&$server<=$client){
			print<<"_HTML_";
Status: 304 Not Modified
Date: @{[&datef($^T,'rfc1123')]}
Content-Language: ja-JP
Content-type: text/html; charset=euc-jp

_HTML_
			exit;
		}
		$lastModified=&datef($server,'rfc1123');
	}else{
		$lastModified=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
	}
	my%DT=@_;
	
	#-----------------------------
	#準備
	
	#Header
	$DT{'head'}||=$CF{'head'};
	#Skyline
	$DT{'skyline'}||=&getLastpost;
	
	#-----------------------------
	#HTML書き出し
	print<<"_HTML_";
Status: 200 OK
Cache-Control: private
Date: @{[&datef($^T,'rfc1123')]}
Content-Language: ja-JP
Content-type: text/html; charset=euc-jp
_HTML_
	print"Last-Modified: $lastModified\n"if$CF{'useLastModified'};
	#GZIP Switch
	my$status=qq(<META http-equiv="Last-Modified" content="$lastModified">\n);
	$status.=join''
	,map{qq(<META http-equiv="Set-Cookie" content="$_">\n)}split("\n",$CF{'-setCookie'})if$CF{'-setCookie'};
	
	$CF{'conenc'}="|$CF{'gzip'} -cfq9"if!defined$CF{'conenc'}||'|gzip -cfq9'eq$CF{'conenc'}and$CF{'gzip'};
	if($CF{'conenc'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')+1or$CF{'forceGZIP'}){
		#上のif文でgzip決め打ちしているのは“仕様”
		#gzip/compress以外に対応してるブラウザは稀なため、可変への需要が少ないと思われるためと
		#$CF{'conenc'}を設定可能にしているのは、GZIP圧縮転送のON/OFF切り替えのため、だから
		if(!$CF{'forceGZIP'}&&$ENV{'SERVER_NAME'}#広告対策
			and	1+index($ENV{'SERVER_SOFTWARE'},'WhizBanner') #infoseek系
			||	1+index($ENV{'SERVER_NAME'},'tkcity.net')
			||	1+index($ENV{'SERVER_NAME'},'aaacafe.ne.jp')
			||	1+index($ENV{'SERVER_NAME'},'xrea.com')
			||	1+index($ENV{'SERVER_NAME'},'tok2.com')
			||	1+index($ENV{'SERVER_NAME'},'tripod')
			||	1+index($ENV{'SERVER_NAME'},'virtualave.net')
			||	1+index($ENV{'SERVER_NAME'},'hypermart.net')
			||	1+index($ENV{'SERVER_NAME'},'tsukaeru.net')
		){
			print"\n";
			$status.="<!-- can't use gzip on this server because of advertisements -->";
#		}elsif($ENV{'SERVER_SOFTWARE'}&&index($ENV{'SERVER_SOFTWARE'},'mod_gzip')+1){
#			print"\n";
#			$status.="<!-- did't use gzip because this server is using mod_gzip -->";
#memo. cgiだとmod_gzipしてくれないっぽい
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
			print' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')+1; #IEのバグ対策
			$status.="<!-- gzip enable -->";
		}
	}else{
		print"\n";
		$status.="<!-- gzip disable -->";
	}
	print<<"_HTML_",&getHeader(skyline=>$DT{'skyline'});
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
$DT{'head'}
$status
</HEAD>

<BODY>
_HTML_
}


#-------------------------------------------------
# 最新の投稿の情報を取得
#
sub getLastpost{
	unless(%Z0){
		open(ZERO,'<'."$CF{'log'}0.cgi")||die"Can't read log(0.cgi)[$?:$!]";
		eval{flock(ZERO,1)};
		my@zero=map{m/^([^\x0D\x0A]*)/o}<ZERO>;
		close(ZERO);
		$zero[0]&&index($zero[0],"Mir12=\t")+1or die"ZEROのログ形式がMir12型以外です";
		%Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
		@zer2=$zero[2]?split(/\s/o,$zero[2]):(0);
	}
	my$date=&date($Z0{'time'});
	my$dateNow="Date:\t\t".&datef($^T,'dateTime')
	."\nLast-Modified:\t".&datef((stat("$CF{'log'}0.cgi"))[9],'dateTime');
	return sprintf'<P class="lastpost" title="%s"><A href="index.cgi?read=%s#art%s">Lastpost: %s %s</A></P>'
		,$dateNow,$Z0{'Mir12'},$Z0{'Mir12'},$date,$Z0{'name'};
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
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$?:$!]";
	my@list=grep{int$_}map{m/^(\d+)\.cgi$/o}readdir(DIR);
	closedir(DIR);
	if('date'eq$_[0]){
		#日付順 'date'
		my@list=grep{$_>$zer2[0]}@list;
		my@tmp=map{$zer2[$_-$zer2[0]]}@list;
		@file=@list[sort{$tmp[$b]<=>$tmp[$a]or$list[$b]<=>$list[$a]}0..$#list];
	}else{
		#記事番号順 'number'
		@file=sort{$b<=>$a}@list;
	}
	push(@file,0);
	return@file;
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
	$IN{'page'}=$pags if$IN{'page'}>$pags;

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
	$str!=1&&unshift(@page,qq(<A accesskey="&#60;" href="index.cgi?${mode}1">1</A>&#60;&#60;));
	$end!=$pags&&push(@page,qq(&#62;&#62;<A accesskey="&#62;" href="index.cgi?$mode$pags">$pags</A>));

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
	$DT{'-maxChildsShown'}=-1if!defined$DT{'-maxChildsShown'};
	$DT{'-unreads'}||=1;
	
	open(RD,'<'."$CF{'log'}$DT{'i'}.cgi")||die"Can't read log($DT{'i'}.cgi)[$?:$!]";
	eval{flock(RD,1)};
	my@articles=<RD>;
	close(RD);
	
	my$maxChildsShown=$DT{'-maxChildsShown'}>-1?int(abs($DT{'-maxChildsShown'})):$#articles;
	my$horizon=$#articles-$maxChildsShown;
	
	#readモードの時の補正
	$horizon=0if$IN{'read'}&&$IN{'read'}==$DT{'i'};
	
	my$isLocked=0;
	for(@articles){
		unless(++$DT{'j'}){
			#親記事
			$DT{'-unreads'}=&artprt(\%DT,$_);
			print<<"_HTML_"if$horizon>0;
<P class="note" style="text-align:center;width:80%">子記事数が多いため、最新の$maxChildsShown件のみ表示します。
それ以前の記事は<A href="index.cgi?res=$DT{'i'}">返信モード</A>で見ることができます。</P>
_HTML_
		}else{
			#子記事
			$DT{'j'}>$horizon||next;
			index($_,"Mir12=\tdel")+1&&next;
			index($_,"Mir12=\tLocked")+1&&++$isLocked&&last;
			$DT{'-unreads'}=&artchd(\%DT,$_);
		}
	}
	$DT{'j'}<0&&return;#記事がないならフッタを表示せず返す
	#記事フッタ
	$DT{'-isLocked'}=$isLocked;
	&artfot(\%DT);
	return$DT{'-unreads'};
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
	my$expires=$^T+33554432; #33554432=2<<24; #33554432という数字に特に意味はない、ちなみに一年と少し
	if($CF{'ckpath'}){
		my$cook=join('',map{"\t$_\t$DT{$_}"}("time expire lastModified"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		$CF{'-setCookie'}="Mireille=$cook; expires=".&datef($expires,'cookie');
		$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		$CF{'-setCookie'}.="\nMireille=$cook; expires=".&datef($expires,'cookie')."; $CF{'ckpath'}";
	}else{
		my$cook=join('',map{"\t$_\t$DT{$_}"}
		("name pass time expire lastModified $CF{'cokitm'}"=~/\b([a-z\d]+)\b/go));
		$cook=~s/(\W)/'%'.unpack('H2',$1)/ego;
		$CF{'-setCookie'}="Mireille=$cook; expires=".&datef($expires,'cookie');
	}
	$CF{'set_cookie_by_meta_tags'}=1if!defined$CF{'set_cookie_by_meta_tags'}&&index($ENV{'SERVER_NAME'},'tok2.com')+1;
	if($CF{'set_cookie_by_meta_tags'}){
		#tok2対策
	}else{
		print map{qq(Set-Cookie: $_\n)}split("\n",$CF{'-setCookie'});
		undef($CF{'-setCookie'});
	}
}


#-------------------------------------------------
# フォーマットされた日付取得を返す
#
sub datef{
=item 引数
$ time形式の時刻
;
$ 出力形式(cookie|last|dateTime)
=cut
	my$time=shift;
	my$type=shift;
	unless($type){
	}elsif('cookie'eq$type){
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
	my$salt=join('',('a'..'z','.',0..9,'/','A'..'Z')[rand(64),rand(64)]);#「.」が混ざっているのはバグ
	my$pass='';
	for($_[1]=~/.{1,8}/go){
		length$_||next;
		$pass.=substr(crypt($_,$salt),2);
	}
	return defined$_[2]?($_[2]&&$_[2]eq$pass?1:undef):$pass;
}


# ------------------------------------------ #
# getCRC32
# based on 2000/06/26 crc32.pl 1.1.0 digiz
my@crc32;
sub getCRC32{
=item 引数
$ CRC32をとりたい文字列
;
$ 32bitの10進数が欲しい時に真を。
=cut
	@crc32=map{my$a=$_;$a=$a&1?($a>>1&0x7fffffff)^0xedb88320:$a>>1&0x7fffffff for 0..7;$a}0..255unless@crc32;
	my$word=shift;
	my$r=0xffffffff;
	$r=$r>>8&0xffffff^$crc32[$r&255^$_]for unpack"C*",$word;
	$r^=0xffffffff;
	return@_?$r:sprintf("%08X",$r);
}


#-------------------------------------------------
# 署名の生成
#
sub getSignature{
	my$word=shift;
	my$canUseSpecial=shift()&&$CF{'signatureSpecial'};
	my$signature;
	if($canUseSpecial&&$CF{'signatureSpecial'}=~/(?:^|\s+)\Q$word\E\s+(\S+)/o){
		$signature='!'.$1;
	}else{
		my$salt='';
		for(0,1){
			my$n=ord chop$word;
			$n%=76;
			$n+=47;
			$salt.=chr$n;
		}
		$signature=&getCRC32(substr(crypt(&getCRC32($word),$salt),2));
	}
	return$signature;
}


#-------------------------------------------------
# 署名の生成（表示時）
#
my%signatureCacheView;
sub getSignatureView{
	my$data=shift;
	my$signature;
	if($data->{signature}=~/!(.+)/o){
		#特殊署名
		$signature=$1;
	}elsif($signatureCacheView{$data->{signature}.' '.$data->{name}}){
		#キャッシュ
		$signature=$signatureCacheView{$data->{signature}.' '.$data->{name}};
	}else{
		unless($Z0{'Serial'}){
			srand();
			$Z0{'Serial'}=1+int(rand(-2+2**32));
		}
		srand($Z0{'Serial'}^&getCRC32($data->{name},1));
		my$saltForSignatureView=chr(47+rand 76).chr(47+rand 76);
		$signature=substr(crypt($data->{signature},$saltForSignatureView),2);
		$signatureCacheView{$data->{signature}.' '.$data->{name}}=$signature;
	}
	return$signature;
}


#-------------------------------------------------
# アイコン用のIMGタグ
#
sub getIconTag{
=item 引数

$ 記事情報の入ったハッシュへのリファレンス
;
$ どのような形で返すかの設定

=item 返り値設定
「-!keyword!-」のような形式です
具体的には以下のとおり
:-!src!-
  dir+file
:-!dir!-
  dir\
:-!file!-
  file

=cut

	my$data=shift;
	my$text=shift||'<IMG src="-!src!-" alt="" title="-!dir!-+-!file!-">';
	my%DT=(dir=>$CF{'icon'},file=>$data->{'icon'});
	if($CF{'absoluteIcon'}&&$data->{'cmd'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
		#絶対指定アイコン
		$DT{'dir'}='';
		$DT{'file'}||=$1;
	}elsif($CF{'relativeIcon'}&&$data->{'cmd'}=~/(?:^|;)relativeIcon=([^;:.]*(?:\.[^;:.]+)*)/o){
		#相対指定アイコン
		$DT{'file'}||=$1;
	}
	if($DT{'file'}){
		$DT{'src'}=$DT{'dir'}.$DT{'file'};
		$text=~s/(-!(\w+)!-)/defined$DT{$2}?$DT{$2}:$1/ego;
	}else{
		$text=undef;
	}
	return$text;
}


#-------------------------------------------------
# アイコンリスト
#
sub iptico{

=item 引数

$ デフォルト指定にしたいアイコンファイル名を入れた書き換え可能な変数
;
$ SELECTタグに追加したい属性
$ 拡張コマンド

=item 複数アイコンリスト

$CF{'icls'}の最初の一文字が' '（半角空白）だった場合複数リストモードになります
具体的な例を出すと、
・単一とみなされる例
'icon.txt'
'icon1.txt icon2.txt' #"icon1.txt icon2"というテキストファイルだとみなします
'"icon.txt" "exicon.txt"'
・複数とみなされる例
' "icon.txt" "exicon.txt"'
' "icon.txt" exicon.txt'
' icon.txt exicon.txt'

=cut

	my$opt=$_[1]?" $_[1]":'';
	if($CF{'-CacheIconList'}&&('reset'ne$_[2])){
		#キャッシュである$CF{'-CacheIconList'}を返す
		return$CF{'-CacheIconList'};
	}
	
	#アイコンリスト読み込み
	my$iconlist='';
	if($CK{'cmd'}=~/\biconlist=nolist(;|$)/o){
	 #`icon=nolist`でアイコンリストを読み込まない
	}elsif($CF{'icls'}=~/^ /o){
		#複数アイコンリスト読み込み
		for($CF{'icls'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
			$_||next;
			my$tmp;
			open(RD,'<'.$_)||die"Can't open multi-iconlist($_).";
			eval{flock(RD,1)};
			read(RD,$tmp,-s$_);
			close(RD);
			$iconlist.=$tmp;
		}
	}else{
		#単一アイコンリスト読み込み
		open(RD,'<'.$CF{'icls'})||die"Can't open single-iconlist.";
		eval{flock(RD,1)};
		read(RD,$iconlist,-s$CF{'icls'});
		close(RD);
	}
	
	#選択アイコンの決定＋SELECTタグの中身
	my$isEconomy=$CK{'cmd'}=~/(?:^|;)iconlist=economy(?:\s*;|$)/o;
	my$isAbsolute=0;
	my$isDisabled='';
	unless(@_){
	}elsif($CF{'exicon'}&&($CK{'cmd'}=~/(?:^|;)icon=([^;]*)/o)&&$IC{$1}){
		#パスワード型
		$_[0]=$IC{$1};
		if($isEconomy){
			$iconlist=qq(<OPTION value="$_[0]" selected>専用アイコン</OPTION>\n);
		}else{
			$iconlist.=qq(<OPTION value="$_[0]" selected>専用アイコン</OPTION>\n);
		}
	}elsif($CF{'absoluteIcon'}&&$CK{'cmd'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
		#絶対指定アイコン
		$_[0]=$1;
		$isAbsolute=1;
		$isDisabled=1;
		$iconlist=qq(<OPTION value="$_[0]" selected>絶対指定</OPTION>\n)if$isEconomy;
	}elsif($CF{'relativeIcon'}&&$CK{'cmd'}=~/(?:^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/o){
		#相対指定アイコン
		$_[0]=$1;
		$iconlist=qq(<OPTION value="$1" selected>相対指定</OPTION>\n)if$isEconomy;
		$isDisabled=1;
	}elsif($_[0]and$iconlist=~s/^(.*value=(["'])$_[0]\2)(.*)$/$1 selected$3/imo){
		$iconlist="$1 selected$3"if$isEconomy;
	}elsif($iconlist=~s/value=(["'])(.+?)\1/value=$1$2$1 selected/io){
		$_[0]=$2;
	}
	$_[0]=$CF{'icon'}.$_[0]unless$isAbsolute;
	$isDisabled&&=' disabled';
	$CF{'-CacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="document.images['Preview'].src='$CF{'icon'}'+this.value;document.images['Preview'].title=this.value;"$opt$isDisabled>
$iconlist</SELECT>
_HTML_
	return$CF{'-CacheIconList'};
}


#-------------------------------------------------
# カラーリスト読み込み
#
sub iptcol{
=item 引数
$ デフォルト指定にしたい色名
=cut
	if('input'eq$CF{'colway'}){
		return<<"_HTML_";
<INPUT type="text" name="color" id="color" maxlength="20" style="ime-mode:disabled"
 title="Color&#10;本文の色を入力します&#10;（#0f0、#00ff00、rgb(0,255,0)、WebColor(greenとか)&#10;のどの形式でも使えます" value="$_[0]">
_HTML_
	}else{
		my$list=$CF{'colorList'}=~/\S/o?$CF{'colorList'}:<<"_HTML_";#1.2.5以下のindex.cgiとの互換性のため
<OPTION value="#000000" style="color:#000000">■Black</OPTION>
<OPTION value="#696969" style="color:#696969">■DimGray</OPTION>
<OPTION value="#808080" style="color:#808080">■Gray</OPTION>
<OPTION value="#A9A9A9" style="color:#A9A9A9">■DarkGray</OPTION>
<OPTION value="#C0C0C0" style="color:#C0C0C0">■Silver</OPTION>
<OPTION value="#D3D3D3" style="color:#D3D3D3">■LightGrey</OPTION>
<OPTION value="#D8BFD8" style="color:#D8BFD8">■Thistle</OPTION>
<OPTION value="#DCDCDC" style="color:#DCDCDC">■Gainsboro</OPTION>
<OPTION value="#F5F5DC" style="color:#F5F5DC">■Beige</OPTION>
<OPTION value="#F5F5F5" style="color:#F5F5F5">■WhiteSmoke</OPTION>
<OPTION value="#E6E6FA" style="color:#E6E6FA">■Lavender</OPTION>
<OPTION value="#FAF0E6" style="color:#FAF0E6">■Linen</OPTION>
<OPTION value="#FDF5E6" style="color:#FDF5E6">■Oldlace</OPTION>
<OPTION value="#FFE4E1" style="color:#FFE4E1">■Mistyrose</OPTION>
<OPTION value="#F0FFF0" style="color:#F0FFF0">■Honeydew</OPTION>
<OPTION value="#FFF5EE" style="color:#FFF5EE">■Seashell</OPTION>
<OPTION value="#FFF0F5" style="color:#FFF0F5">■LavenderBlush</OPTION>
<OPTION value="#F0F8FF" style="color:#F0F8FF">■AliceBlue</OPTION>
<OPTION value="#F8F8FF" style="color:#F8F8FF">■GhostWhite</OPTION>
<OPTION value="#FFFAF0" style="color:#FFFAF0">■FloralWhite</OPTION>
<OPTION value="#F5FFFA" style="color:#F5FFFA">■Mintcream</OPTION>
<OPTION value="#FFFAFA" style="color:#FFFAFA">■Snow</OPTION>
<OPTION value="#FFFFE0" style="color:#FFFFE0">■LightYellow</OPTION>
<OPTION value="#E0FFFF" style="color:#E0FFFF">■LightCyan</OPTION>
<OPTION value="#FFFFF0" style="color:#FFFFF0">■Ivory</OPTION>
<OPTION value="#F0FFFF" style="color:#F0FFFF">■Azure</OPTION>
<OPTION value="#FFFFFF" style="color:#FFFFFF">■White</OPTION>
<OPTION value="#9370DB" style="color:#9370DB">■MediumPurple</OPTION>
<OPTION value="#6A5ACD" style="color:#6A5ACD">■SlateBlue</OPTION>
<OPTION value="#483D8B" style="color:#483D8B">■DarkSlateBlue</OPTION>
<OPTION value="#7B68EE" style="color:#7B68EE">■MediumSlateBlue</OPTION>
<OPTION value="#BA55D3" style="color:#BA55D3">■MediumOrchid</OPTION>
<OPTION value="#9932CC" style="color:#9932CC">■DarkOrchid</OPTION>
<OPTION value="#8A2BE2" style="color:#8A2BE2">■BlueViolet</OPTION>
<OPTION value="#9400D3" style="color:#9400D3">■DarkViolet</OPTION>
<OPTION value="#4B0082" style="color:#4B0082">■Indigo</OPTION>
<OPTION value="#000080" style="color:#000080">■Navy</OPTION>
<OPTION value="#00008B" style="color:#00008B">■DarkBlue</OPTION>
<OPTION value="#0000CD" style="color:#0000CD">■MediumBlue</OPTION>
<OPTION value="#0000FF" style="color:#0000FF">■Blue</OPTION>
<OPTION value="#191970" style="color:#191970">■MidnightBlue</OPTION>
<OPTION value="#00BFFF" style="color:#00BFFF">■DeepSkyBlue</OPTION>
<OPTION value="#00CED1" style="color:#00CED1">■DarkTurquoise</OPTION>
<OPTION value="#1E90FF" style="color:#1E90FF">■DodgerBlue</OPTION>
<OPTION value="#4169E1" style="color:#4169E1">■RoyalBlue</OPTION>
<OPTION value="#4682B4" style="color:#4682B4">■SteelBlue</OPTION>
<OPTION value="#6495ED" style="color:#6495ED">■CornflowerBlue</OPTION>
<OPTION value="#87CEFA" style="color:#87CEFA">■LightSkyblue</OPTION>
<OPTION value="#5F9EA0" style="color:#5F9EA0">■CadetBlue</OPTION>
<OPTION value="#87CEEB" style="color:#87CEEB">■SkyBlue</OPTION>
<OPTION value="#B0E0E6" style="color:#B0E0E6">■PowderBlue</OPTION>
<OPTION value="#ADD8E6" style="color:#ADD8E6">■LightBlue</OPTION>
<OPTION value="#708090" style="color:#708090">■SlateGray</OPTION>
<OPTION value="#778899" style="color:#778899">■LightSlateGray</OPTION>
<OPTION value="#B0C4DE" style="color:#B0C4DE">■LightSteelBlue</OPTION>
<OPTION value="#008080" style="color:#008080">■Teal</OPTION>
<OPTION value="#008B8B" style="color:#008B8B">■DarkCyan</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">■Aqua</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">■Cyan</OPTION>
<OPTION value="#2F4F4F" style="color:#2F4F4F">■DarkSlateGray</OPTION>
<OPTION value="#AFEEEE" style="color:#AFEEEE">■PaleTurquoise</OPTION>
<OPTION value="#7FFFD4" style="color:#7FFFD4">■Aquamarine</OPTION>
<OPTION value="#66CDAA" style="color:#66CDAA">■MediumAquamarine</OPTION>
<OPTION value="#3CB371" style="color:#3CB371">■MediumSeagreen</OPTION>
<OPTION value="#2E8B57" style="color:#2E8B57">■SeaGreen</OPTION>
<OPTION value="#48D1CC" style="color:#48D1CC">■MediumTurquoise</OPTION>
<OPTION value="#40E0D0" style="color:#40E0D0">■Turquoise</OPTION>
<OPTION value="#20B2AA" style="color:#20B2AA">■LightSeagreen</OPTION>
<OPTION value="#00FA9A" style="color:#00FA9A">■MediumSpringGreen</OPTION>
<OPTION value="#00FF7F" style="color:#00FF7F">■SpringGreen</OPTION>
<OPTION value="#006400" style="color:#006400">■DarkGreen</OPTION>
<OPTION value="#008000" style="color:#008000">■Green</OPTION>
<OPTION value="#00FF00" style="color:#00FF00">■Lime</OPTION>
<OPTION value="#32CD32" style="color:#32CD32">■LimeGreen</OPTION>
<OPTION value="#228B22" style="color:#228B22">■ForestGreen</OPTION>
<OPTION value="#90EE90" style="color:#90EE90">■LightGreen</OPTION>
<OPTION value="#98FB98" style="color:#98FB98">■PaleGreen</OPTION>
<OPTION value="#7CFC00" style="color:#7CFC00">■LawnGreen</OPTION>
<OPTION value="#7FFF00" style="color:#7FFF00">■Chartreuse</OPTION>
<OPTION value="#ADFF2F" style="color:#ADFF2F">■GreenYellow</OPTION>
<OPTION value="#9ACD32" style="color:#9ACD32">■YellowGreen</OPTION>
<OPTION value="#6B8E23" style="color:#6B8E23">■Olivedrab</OPTION>
<OPTION value="#556B2F" style="color:#556B2F">■DarkOlivegreen</OPTION>
<OPTION value="#8FBC8B" style="color:#8FBC8B">■DarkSeaGreen</OPTION>
<OPTION value="#808000" style="color:#808000">■Olive</OPTION>
<OPTION value="#FFFF00" style="color:#FFFF00">■Yellow</OPTION>
<OPTION value="#FAFAD2" style="color:#FAFAD2">■LightGoldenrodYellow</OPTION>
<OPTION value="#FAEBD7" style="color:#FAEBD7">■AntiqueWhite</OPTION>
<OPTION value="#FFF8DC" style="color:#FFF8DC">■Cornsilk</OPTION>
<OPTION value="#FFEFD5" style="color:#FFEFD5">■PapayaWhip</OPTION>
<OPTION value="#FFEBCD" style="color:#FFEBCD">■BlanchedAlmond</OPTION>
<OPTION value="#FFFACD" style="color:#FFFACD">■LemonChiffon</OPTION>
<OPTION value="#FFE4C4" style="color:#FFE4C4">■Bisque</OPTION>
<OPTION value="#FFDAB9" style="color:#FFDAB9">■PeachPuff</OPTION>
<OPTION value="#F5DEB3" style="color:#F5DEB3">■Wheat</OPTION>
<OPTION value="#FFE4B5" style="color:#FFE4B5">■Moccasin</OPTION>
<OPTION value="#FFDEAD" style="color:#FFDEAD">■NavajoWhite</OPTION>
<OPTION value="#EEE8AA" style="color:#EEE8AA">■PaleGoldenrod</OPTION>
<OPTION value="#D2B48C" style="color:#D2B48C">■Tan</OPTION>
<OPTION value="#DEB887" style="color:#DEB887">■Burlywood</OPTION>
<OPTION value="#E9967A" style="color:#E9967A">■DarkSalmon</OPTION>
<OPTION value="#FA8072" style="color:#FA8072">■Salmon</OPTION>
<OPTION value="#F0E68C" style="color:#F0E68C">■Khaki</OPTION>
<OPTION value="#FFA07A" style="color:#FFA07A">■LightSalmon</OPTION>
<OPTION value="#BDB76B" style="color:#BDB76B">■DarkKhaki</OPTION>
<OPTION value="#F4A460" style="color:#F4A460">■SandyBrown</OPTION>
<OPTION value="#FF7F50" style="color:#FF7F50">■Coral</OPTION>
<OPTION value="#FF6347" style="color:#FF6347">■Tomato</OPTION>
<OPTION value="#CD853F" style="color:#CD853F">■Peru</OPTION>
<OPTION value="#A0522D" style="color:#A0522D">■Sienna</OPTION>
<OPTION value="#D2691E" style="color:#D2691E">■Chocolate</OPTION>
<OPTION value="#8B4513" style="color:#8B4513">■SaddleBrown</OPTION>
<OPTION value="#DAA520" style="color:#DAA520">■Goldenrod</OPTION>
<OPTION value="#B8860B" style="color:#B8860B">■DarkGoldenrod</OPTION>
<OPTION value="#FFD700" style="color:#FFD700">■Gold</OPTION>
<OPTION value="#FFA500" style="color:#FFA500">■Orange</OPTION>
<OPTION value="#FF8C00" style="color:#FF8C00">■DarkOrange</OPTION>
<OPTION value="#FF4500" style="color:#FF4500">■OrangeRed</OPTION>
<OPTION value="#800000" style="color:#800000">■Maroon</OPTION>
<OPTION value="#8B0000" style="color:#8B0000">■DarkRed</OPTION>
<OPTION value="#FF0000" style="color:#FF0000">■Red</OPTION>
<OPTION value="#B22222" style="color:#B22222">■Firebrick</OPTION>
<OPTION value="#A52A2A" style="color:#A52A2A">■Brown</OPTION>
<OPTION value="#CD5C5C" style="color:#CD5C5C">■IndianRed</OPTION>
<OPTION value="#F08080" style="color:#F08080">■LightCoral</OPTION>
<OPTION value="#BC8F8F" style="color:#BC8F8F">■RosyBrown</OPTION>
<OPTION value="#FF1493" style="color:#FF1493">■DeepPink</OPTION>
<OPTION value="#C71585" style="color:#C71585">■MediumVioletRed</OPTION>
<OPTION value="#DC143C" style="color:#DC143C">■Crimson</OPTION>
<OPTION value="#FF69B4" style="color:#FF69B4">■HotPink</OPTION>
<OPTION value="#DA70D6" style="color:#DA70D6">■Orchid</OPTION>
<OPTION value="#DB7093" style="color:#DB7093">■PaleVioletred</OPTION>
<OPTION value="#FFB6C1" style="color:#FFB6C1">■LightPink</OPTION>
<OPTION value="#FFC0CB" style="color:#FFC0CB">■Pink</OPTION>
<OPTION value="#800080" style="color:#800080">■Purple</OPTION>
<OPTION value="#8B008B" style="color:#8B008B">■DarkMagenta</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">■Fuchsia</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">■Magenta</OPTION>
<OPTION value="#EE82EE" style="color:#EE82EE">■Violet</OPTION>
<OPTION value="#DDA0DD" style="color:#DDA0DD">■Plum</OPTION>
_HTML_
		if($_[0]&&$list=~s/(value=(["'])$_[0]\2)/$1 selected="selected"/io){
		}elsif($list=~s/value=(["'])$CF{'colway'}\1/value=$1$CF{'colway'}$1 selected="selected"/io){
			$_[0]=$CF{'colway'};
		}elsif($list=~s/value=(["'])(.+?)\1/value=$1$2$1 selected="selected"/io){
			$_[0]=$2;
		}
		return<<"_HTML_";
<SELECT name="color" id="color">
$list</SELECT>
_HTML_
	}
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
	my$file=0;
	if('gzip'eq$type&&$CF{'gzip'}){
		#GZIP圧縮
		for(@del){
			$_||next;
			`$CF{'gzip'} -fq9 "$CF{'log'}$_.cgi"`;
			($?==0)||die"$?:Can't use gzip($CF{'gzip'}) oldlog($_.cgi)[$?:$!]";
			$file++;
		}
	}elsif('unlink'eq$type){
		#削除
		for(@del){
			$_||next;
			unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog($_.cgi)[$?:$!]";
			$file++;
		}
	}elsif('rename'eq$type){
		#ファイル名変更
		for(@del){
			$_||next;
			if(-e"$CF{'log'}$_.bak.cgi"){
				#しょうがないから古いのは削除しちゃう
				unlink"$CF{'log'}$_.bak.cgi"||die"Can't unlink old-old log($CF{'log'}$_.bak.cgi)[$?:$!]";
			}
			rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")||die"Can't rename oldlog($_.cgi)[$?:$!]";
			$file++;
		}
	}elsif($type=~/!(.*)/o){
		#特殊
		for(@del){
			$_||next;
			`$1 "$CF{'log'}$_.cgi"`;
			$?==0||die"$?:Invalid delete type($1) oldlog($_.cgi)[$?:$!]";
			$file++;
		}
	}else{
		die"Invalid delete type:'$type'";
	}
	return($file);
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

また2と3については削除に際して以下を仮定します
・Aタグの内容には[<>]が来ない
・自動リンク1セットは必ず/<A class="autolink" [^>]*>([^<]+)<\/A>/にマッチする
・リンクする対象の「&」をエスケープした際は「&#38;」でエスケープした
何らかの形でこの仮定が崩れた場合、削除しきれないことや、きちんと復元できない可能性があります

=cut

		my$str=$CK{'body'};
		#記事番号リンク「>>No.12-6」
		$str=~s{<A class="autolink"[^>]*>&#38;#62;&#38;#62;(No\.(\d+)(-\d+)?)</A>}{&#62;&#62;$1}go;
		#Aタグ
		$str=~s{<A class="autolink" [^>]*>([^<]+)</A>}{my$tmp=$1;$tmp=~s/&#38;#38;/&#38;/g;$tmp}ego;
		
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
	my($day,$mon,$year,$hour,$min,$sec)=(split(/[\s:]/o,$date))[1..6];
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
		$SIG{'__DIE__'}=$ENV{'REQUEST_METHOD'}?sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/o){return}
			print"Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/plain; charset=euc-jp"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Index Style Core Exte))
			."\n".join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(log icon icls style));
			print"\n".join('',map{"$$_[0]\t: $$_[1]\n"}
			([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]))
			."\n\t= = = ENV = = =\n".join('',map{sprintf"%-20.20s : %s\n",$_,$ENV{$_}}grep{$ENV{"$_"}}
			qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD
			SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE PROCESSOR_IDENTIFIER))
			."\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+";
			exit;
		}:sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/o){return}
			print@_?"ERROR: $_[0]":'ERROR';
			exit;
		};
	}
	# Version
	$CF{'Version'}=join('.',q$Mireille: 1_2_11 $=~/\d+[a-z]?/go);
	($CF{'Core'}=q$Revision$)=~/(\d+((?:\.\d+)*))/o;
	$CF{'CoreRevision'}=$1;
	$CF{'Version'}.=$2.'β' if index(q$State$,'Exp')+1;
}
1;
__END__
