#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Administrative Tools -
#
# $Revision$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use strict;
use vars qw(%AT %CF %IN %IC @file @zer2);
$|=1;


# Header without G-ZIP etc.
print<<'_HTML_';
Content-type: text/html; charset=euc-jp
Content-Language: ja-JP

_HTML_

=pod TEST
&icong;
exit;
=pod
=cut


#管理CGIのパスワード
$AT{'pass'}='';

#-------------------------------------------------
# Switch

__FILE__=~/\bmanage.cgi$/o&&$ENV{'SERVER_NAME'}&&$ENV{'SERVER_NAME'}ne"localhost"&& die<<"_HTML_";
<STRONG>最低限のセキュリティを確保するための警告</STRONG>
管理CGIを起動するのに最低限必要なセキュリティ意識が管理者に不足しています
せめて説明書は一通り目を通してください
_HTML_

&getParam;
unless($IN{'mode'}){
	&menu('NULL');
}elsif('icong'eq$IN{'mode'}){
	&icong;
}elsif('icont'eq$IN{'mode'}){
	&icont;
}elsif('icons'eq$IN{'mode'}){
	&icons;
}elsif('iconsmp'eq$IN{'mode'}){
	&iconsmp;
}elsif('config'eq$IN{'mode'}){
	&config;
}elsif('css'eq$IN{'mode'}){
	&css;
}elsif('log'eq$IN{'mode'}){
	&log;
}elsif('zero'eq$IN{'mode'}){
	&zero;
}elsif('manage'eq$IN{'mode'}){
	&manage;
}else{
	&menu('NG');
}
exit;

#-------------------------------------------------
# Get Parameters
sub getParam{
	my$i='';
	my@param;
	#引数取得
	unless($ENV{'REQUEST_METHOD'}){@param=@ARGV;}
	elsif('POST'eq$ENV{'REQUEST_METHOD'}){read(STDIN,$i,$ENV{'CONTENT_LENGTH'});}
	elsif('GET'eq$ENV{'REQUEST_METHOD'}){$i=$ENV{'QUERY_STRING'};}
	#入力を展開
	@param=split(/[&;]/o,$i)if$i;
	# EUC-JP文字
	my$eucchar=qr((?:
		[\x09\x0A\x0D\x20-\x7E]			# 1バイト EUC-JP文字改
		|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2バイト EUC-JP文字
		|(?:\x8F[\xA1-\xFE]{2})			# 3バイト EUC-JP文字
	))x;
	
	my%DT;
	while(@param){
		my($i,$j)=split('=',shift(@param),2);
		defined$j||($DT{$i}='',next);
		$i=($i=~/([-\w]+)/o)?"$1":'';
		study$j;
		$j=~tr/+/\ /;
		$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
		$j=($j=~/($eucchar*)/o)?"$1":'';
		#メインフレームの改行は\x85らしいけど、対応する必要ないよね？
		$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
		$DT{$i}=$j;
	}
	# Password Check
	($DT{'mode'})||(return undef);
	($DT{'pass'}eq$AT{'pass'})||(&menu('Passwordが一致しません'));
	$IN{'pass'}=($DT{'pass'}=~/(.+)/o)?"$1":'';
	$IN{'mode'}=$1 if($DT{'mode'}=~/(\w+)/o);
	$IN{'phase'}=$1 if($DT{'phase'}=~/(\d+)/o);
	if('icong'eq$DT{'mode'}){
		for(keys%DT){
			$IN{$_}=$DT{$_} if($_=~/^\d+-\w*/o);
		}
		return%IN;
	}elsif('icont'eq$DT{'mode'}){
		$IN{'icon'}=($DT{'icon'}=~/(.+)/os)?"$1":undef;
		$IN{'renew'}=($DT{'renew'}=~/(.)/o)?'1':undef;
		return%IN;
	}elsif('icons'eq$DT{'mode'}){
		$IN{'icon'}=($DT{'icon'}=~/(.+)/os)?"$1":undef;
		$IN{'renew'}=($DT{'renew'}=~/(.)/o)?'1':undef;
		return%IN;
	}elsif('iconsmp'eq$DT{'mode'}){
		return%IN;
	}elsif('config'eq$DT{'mode'}){
		while(my($i,$j)=each%DT){
			$IN{"$i"}=($j=~/(.*)/os)?"$1":undef;
		}
		return%IN;
	}elsif('css'eq$DT{'mode'}){
		$IN{'css'}=($DT{'css'}=~/(.+)/os)?"$1":undef;
		$IN{'file'}=($DT{'file'}=~/(\w+)/o)?"$1":undef;
		$IN{'code'}=($DT{'code'}=~/(\w+)/o)?"$1":undef;
		return%IN;
	}elsif('log'eq$DT{'mode'}){#LOG
		$IN{'str'}=($DT{'str'}=~/(\d+)/o)?$1:0;
		$IN{'end'}=($DT{'end'}=~/(\d+)/o)?$1:0;
		$IN{'del'}=($DT{'del'}=~/(\w)/o)?"$1":undef;
		$IN{'save'}=($DT{'save'}=~/(\d+)/o)?$1:0;
		$IN{'push'}=($DT{'push'}=~/(\d)/o)?"$1":'';
		$IN{'type'}=($DT{'type'}=~/(\w)/o)?"$1":undef;
		return%IN;
	}elsif('zero'eq$DT{'mode'}){#Zero
		$IN{'recover'}=($DT{'recover'}=~/(.)/o)?'1':undef;
		return%IN;
	}elsif('manage'eq$DT{'mode'}){#Manage
		$IN{'manage'}=($DT{'manage'}=~/(\w+)/o)?$1:undef;
		$IN{'filename'}=($DT{'filename'}=~/([^\\\/:*?"<>|]+)/o)?$1:undef;
		return%IN;
	}
	print"<PRE>something wicked happend!\n";
	print"おそらくはフィルタの設定ミス\n管理CGI".__LINE__."行目でのエラー";
	exit;
}

#-------------------------------------------------
# Menu
sub menu{
	my$status=@_?shift():'';
	my$pass=defined$IN{'pass'}?$IN{'pass'}:'';
	print<<"ASDF";
$AT{'head'}<H2 class="mode" style="margin:1em auto">[ $status ]</H2>
<FORM accept-charset="euc-jp" name="menu" method="post" action="$AT{'manage'}">
<FIELDSET style="text-align:left;padding:0.5em;margin:auto;width:15em">
<LEGEND>Mode</LEGEND>
<LABEL accesskey="y" for="icont">
<INPUT name="mode" class="radio" id="icont" type="radio" value="icont">
Iconリスト編集（タグ）(<SPAN class="ak">Y</SPAN>)</LABEL>
<BR>
<LABEL accesskey="u" for="icons">
<INPUT name="mode" class="radio" id="icons" type="radio" value="icons">
Iconリスト編集(Sharp）(<SPAN class="ak">U</SPAN>)</LABEL>
<BR>
<LABEL accesskey="g" for="icong">
<INPUT name="mode" class="radio" id="icong" type="radio" value="icong">
IconGUI編集(<SPAN class="ak">G</SPAN>)</LABEL>
<BR>
<LABEL accesskey="i" for="iconsmp">
<INPUT name="mode" class="radio" id="iconsmp" type="radio" value="iconsmp" checked>
<SPAN class="ak">I</SPAN>con見本を更新</LABEL>
<BR>
<LABEL accesskey="c" for="config">
<INPUT name="mode" class="radio" id="config" type="radio" value="config">
index.cgi編集(<SPAN class="ak">C</SPAN>)</LABEL>
<BR>
<LABEL accesskey="b" for="css">
<INPUT name="mode" class="radio" id="css" type="radio" value="css">
外部CSS編集(<SPAN class="ak">B</SPAN>)</LABEL>
<BR>
<LABEL accesskey="l" for="log">
<INPUT name="mode" class="radio" id="log" type="radio" value="log">
<SPAN class="ak">L</SPAN>OG管理・削除</LABEL>
<BR>
<LABEL accesskey="z" for="zero">
<INPUT name="mode" class="radio" id="zero" type="radio" value="zero">
記事情報ファイル回復(<SPAN class="ak">Z</SPAN>)</LABEL>
<BR>
<LABEL accesskey="m" for="manage">
<INPUT name="mode" class="radio" id="manage" type="radio" value="manage">
管理CGIの管理(<SPAN class="ak">M</SPAN>)</LABEL>
</FIELDSET>
<P style="margin:0.5em"><LABEL accesskey="p" for="pass"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" id="pass" type="password" size="12" value="$pass"></LABEL></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK">
<INPUT type="reset" class="reset" value="キャンセル"></P>
@{[&getFooter]}
ASDF
	exit;
}

#-------------------------------------------------
# アイコン（GUI）
#
sub icong{
	&loadcfg;
	$CF{'icls'}='iconLite.txt';
	if(!$IN{'phase'}||1==$IN{'phase'}){#アイコンリスト編集
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my$iconlist;
		read(RD,$iconlist,-s$CF{'icls'});
		close(RD);
		
		my@items;
		my%group;
		
		my$i=0;
		my$j=0;
		$AT{'x'}=6;
		my$cols=$AT{'x'};
		for(&parseMir0x($iconlist)){
			$i++;
			my%DT=%{$_};
=pod
			if($DT{'cmd'}){
				if('PAGE-BREAK'eq$DT{'cmd'}){
					
				}elsif('COPY'eq$DT{'cmd'}){
					if('BEGIN'eq$DT{'swt'}){
						push(@items,'<P>'
							.qq(<INPUT type="text" name="$i-cmd" value="$DT{'cmd'}">\n)
							.qq(<INPUT type="text" name="$i-swt" value="$DT{'swt'}">\n)
						.'</P>');
						push(@items,qq(<FIELDSET>));
					}elsif('END'eq$DT{'swt'}){
						push(@items,'<P>'
							.qq(<INPUT type="text" name="$i-cmd" value="$DT{'cmd'}">\n)
							.qq(<INPUT type="text" name="$i-swt" value="$DT{'swt'}">\n)
						.'</P>');
						push(@items,qq(</FIELDSET>));
					}elsif('SET'eq$DT{'swt'}){
						push(@items,'<P>'
							.qq(<INPUT type="text" name="$i-cmd" value="$DT{'cmd'}">\n)
							.qq(<INPUT type="text" name="$i-swt" value="$DT{'swt'}">\n)
							.qq(<INPUT type="text" name="$i-name" value="$DT{'name'}">\n)
							.qq(<INPUT type="text" name="$i-item" value="$DT{'item'}">\n)
							.qq(<INPUT type="text" name="$i-value" value="$DT{'value'}">\n)
						.'</P>');
					}
				}
				next;
			}
=cut
			
			if('item'eq$DT{'type'}){
				my$item='<TD>'
					.qq(<INPUT type="hidden" name="$i-type" value="$DT{'type'}">\n)
					.qq(<IMG name="icon$i" id="icon$i" title="$i" src="$CF{'icon'}$DT{'value'}"><BR>\n)
					.qq(<INPUT type="text" name="$i-name" value="$DT{'name'}"><BR>\n)
					.qq(<INPUT type="text" name="$i-value" value="$DT{'value'}")
					.qq( onchange="changeIcon($i,this.value)"></TD>\n);
				if($j<$cols){ #グループ内1-5桁
					$j++;
				}else{ #グループ内6桁目：改行
					$item.="</TR><TR>\n";$j=1;
				}
				push(@items,$item);
			}elsif('startGroup'eq$DT{'type'}){
				$group{$i}=$DT{'name'};
				push(@items,qq(\n<TABLE class="icon" id="iconTable$i" style="display:none">\n)
					.qq(<CAPTION style="text-align:center">)
					.qq(<INPUT type="hidden" name="$i-type" value="$DT{'type'}">\n)
					.qq(GROUP: <INPUT type="text" name="$i-name" value="$DT{'name'}"></CAPTION>\n)
					.qq(<COL span="$cols"><TR>\n));
				$j=1;
			}elsif('endGroup'eq$DT{'type'}){
				push(@items,($j>1?"</TR><TR>\n":'')
					.qq(<TD colspan="$cols"><INPUT type="hidden" name="$i-type" value="$DT{'type'}">)
					.qq(<BUTTON onclick="alert('まーだだよ')">アイコンを追加する</BUTTON></TD>\n</TR></TABLE>\n));
				$i+=100;
				$j=0;
			}
		}
		print$AT{'head'};
		print<<"_HTML_";
<SCRIPT type="text/javascript">
var presentTable=null;
var iconDir="$CF{'icon'}";
function showTable(newTable){
	presentTable&&(document.getElementById(presentTable).style.display='none');
	document.getElementById('iconTable'+newTable).style.display='block';
	presentTable='iconTable'+newTable;
}
function changeIcon(number,value){
	document.getElementById('icon'+number).src=iconDir+value;
}
</SCRIPT>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
_HTML_
		print qq(<TABLE class="icon" style="float:left;margin-left:1em;text-align:left">\n);
		print map{qq(<TR><TD onclick="showTable($_)" title="$_">$group{$_}</TD></TR>\n)}
			sort{$a<=>$b}keys%group;
		print qq(</TABLE>\n);
		print@items;
		print<<"_HTML_";
<P style="float:clear">
<INPUT name="mode" type="hidden" value="icong">
<INPUT name="phase" type="hidden" value="2">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
_HTML_
		print&getFooter;
		exit;
	}else{
		my@events;
		for(map{m/^((\d+)-(\w+))$/o;[$1,$2,$3]}grep{m/^\d+-\w+$/o}keys%IN){
			$events[$_->[1]]->{$_->[2]}=$IN{$_->[0]};
		}
		
		my@tmp=@events;undef@events;
		for(@tmp){'HASH'eq ref$_&& push(@events,$_)}
		
		print$AT{'head'};
		print"<PRE>".generateEalis3qw(@events)."</PRE>";
		print<<"_HTML_";
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
_HTML_
		print&getFooter;
		exit;
	}
	exit;
}

sub generateEalis3qw{
	my@list;
	my$max=1;
	for(@_){
		my%DT=%{$_};
		if($DT{'cmd'}){
		}elsif('item'eq$DT{'type'}){
			$max=length$DT{'value'}if$max<length$DT{'value'};
			push(@list,$DT{'value'},$DT{'name'});
		}elsif('startGroup'eq$DT{'type'}){
			push(@list,'**',$DT{'name'});
		}elsif('endGroup'eq$DT{'type'}){
		}
	}
	return wantarray?@list:join('',
	map{sprintf("\t\t%-${max}s\t%s\n",$list[$_*2],$list[$_*2+1])}(0..@list/2));
}

#-------------------------------------------------
# Mireille0.x Parser and Generator
#

=head2 Mireille0.x形式アイコンリストの解析と生成

Mireille0.x形式は主にMireilleやMarldiaで用いられるアイコンリスト形式で、
少ない処理でHTMLに書き出すために、もとからHTMLの断片として作られたリスト形式である。
HTML断片という性格から幅広い拡張性を持つが、ともすれば煩雑になりやすい。
そのため、正規表現が実装されていない言語でこのリスト形式を扱うのは難しいと思われる。

=over 4

=cut

sub parseMir0x{
	my$iconlist=shift;
	my@events;
	for($iconlist=~/.*/go){
		if(/<!--\s*%(?:(BEGIN|END|SET)_)?(VENDOR|COPY1|PAGE-BREAK)(?:_(NAME|URL|LINK))?(?:\s+(\S.*?))?\s*-->/o){

=item MireilleIconListCommand

 /<!--\s*%(?:(BEGIN|END)_)?([-A-Z0-9]+)(?:_([A-Z0-9]+))?(?:\s+(\S.*?))?\s*-->/o
 イベント：アイコンリストの命令を発見した
 現在存在する命令の形式は以下のよう

swt:  $1: 'BEGIN','END','SET'
name: $2: 'VENDOR','COPY1','PAGE-BREAK'
item: $3: 'NAME','URL','LINK'
value:$4: 命令の引数

=cut

			if('PAGE-BREAK'eq$2){
				#改ページ処理を。
				push(@events,{cmd=>'PAGE-BREAK'});
			}elsif($1&&('BEGIN'eq$1||'END' eq$1)){
#				'VENDOR'eq$2||'COPY1'eq$2||next;
#上は暗黙の仮定とする
#将来拡張する際に注意すること
				push(@events,{cmd=>'COPY',swt=>$1,name=>$2});
				'BEGIN'eq$1&&$4&& push(@events,{cmd=>'COPY',swt=>'SET',name=>$2,item=>'NAME',value=>$4});
			}elsif($3&&$4){
				push(@events,{cmd=>'COPY',swt=>'SET',name=>$2,item=>$3,value=>$4});
			}
			next
		}
		
		if(/^\s*<OPTION ([^>]*)\bvalue=(["'])(.+?)\2([^>]*)>([^<]+)(<\/OPTION>)?$/io){

=item OPTION要素

 /^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(<\/OPTION>)?$/io
 <TD><IMG $1src="$CF{'iconDir'}$3" alt="$5"$4><BR>$5</TD>\n
 イベント：一つのアイコンを発見

=cut

			push(@events,{type=>'item',value=>$3,pre=>$1,suf=>$4,name=>$5});
		}elsif(/^<OPTGROUP ([^>]*)\blabel=(["'])(.+?)\2(.*)>$/io){

=item OPTGOUP要素始

 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 イベント：OPTGROUP内に入った

=cut

			push(@events,{type=>'startGroup',name=>$3,pre=>$1,suf=>$4});
		}elsif(/<\/OPTGROUP>/io){#</OPTGROUP>

=item OPTGOUP要素終

 /OPTGROUP/io
 イベント：OPTGROUP外に出た

=cut

			push(@events,{type=>'endGroup'});
		}
		next;
	}

=back

=cut

	undef$iconlist;
	return@events;
}
sub generateMir0x{
	die"未実装";
	my@list;
	for(@_){
		my%DT=%{$_};
		if('item'eq$DT{'type'}){
		}elsif('startGroup'eq$DT{'type'}){
		}elsif('endGroup'eq$DT{'type'}){
			next;
		}
	}
	return@list;
}


#-------------------------------------------------
# アイコン（タグ）
sub icont{
	&loadcfg;
	unless($IN{'icon'}){#アイコンリスト編集
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my$icon;
		read(RD,$icon,-s$CF{'icls'});
		close(RD);
		$icon=~s/\t/\ \ /go;
		$icon=~s/[\x0D\x0A]*$//o;
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">アイコンリスト編集モード</H2>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<P><TEXTAREA name="icon" cols="100" rows="15">$icon</TEXTAREA></P>
<P><LABEL accesskey="r" for="renew">アイコン見本更新(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icont">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
	exit;
	}else{#アイコンリスト書き込み Tag
		study$IN{'icon'};
		$IN{'icon'}=~tr/\n//s;
		$IN{'icon'}=~s/(\n)*$/\n/;

		open(WR,"+>>$CF{'icls'}")||die"Can't write iconlist($CF{'icls'})[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $IN{'icon'};
		close(WR);

		unless($IN{'renew'}){
			&menu('アイコンリスト書き込み完了');
		}else{
			&iconsmp;
			&menu('アイコンリスト・見本書き込み完了');
		}
	}
	exit;
}

#-------------------------------------------------
# アイコン（＃）
sub icons{
	&loadcfg;
	unless($IN{'icon'}){
		#アイコンリストSharp編集画面
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">アイコンリスト編集モード</H2>
<FORM accept-charset="euc-jp" name="iconedit" method="post" action="$AT{'manage'}">
<P><TEXTAREA name="icon" cols="100" rows="15">
ASDF
		
		open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
		eval{flock(RD,1)};
		my@icon=<RD>;
		close(RD);
		
		my$optg=0;
		
		for(@icon){
			
			if($_=~m{^\s*<OPTION .*?\bvalue=(["'])(.+?)\1.*?>([^<]*)(</OPTION>)?$}io){
				if($optg==1){print"\ \ ";}
				elsif($optg==2){print"#\n";$optg=0;}
				print"$2#$3\n";
				next;
			}elsif($_=~m{<OPTGROUP .*\blabel=(["'])(.+?)\1.*>}io){
				($2)||($optg=0);
				$optg=1;
				print"#$2\n";
				next;
			}elsif($_=~m{</OPTGROUP>}io){
				print"#\n";
				$optg=2;
				next;
			}else{
				print"$_";
			}
		}
		
		print<<"ASDF";
</TEXTAREA></P>
<P><LABEL accesskey="r" for="renew">アイコン見本更新(<SPAN class="ak">R</SPAN>):
<INPUT name="renew" id="renew" type="checkbox" value="renew" checked></LABEL></P>
<INPUT name="mode" type="hidden" value="icons">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
		
		exit;
	}else{
		#アイコンリスト書き込み
#		study$IN{'icon'};
		$IN{'icon'}=~tr/\n//s;
#		$IN{'icon'}=~s/&/&#38;/go;
#		$IN{'icon'}=~s/"/&#34;/go;
#		$IN{'icon'}=~s/'/&#39;/go;
#		$IN{'icon'}=~s/</&#60;/go;
#		$IN{'icon'}=~s/>/&#62;/go;
		my@icon=split("\n","$IN{'icon'}");
		
=icon Sharp
 GroupName
^\s*\#\s*(.*)$
 IconName
^\s*([^#])\s*#\s*(.*)$
=cut
		
		open(WR,"+>>$CF{'icls'}")||die"Can't write iconlist($CF{'icls'})[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		my$optg=0;
		for(@icon){
			if($_=~/^\s*\#\s*(.*)$/o){
				#アイコングループ
				($optg==1)&&(print WR "</OPTGROUP>\n");
				($1)||($optg=0,next);
				print WR qq[<OPTGROUP label="$1">\n];
				$optg=1;
				next;
			}elsif($_=~/^\s*([^#]+(?:#\d+)?)\s*\#\s*(.+)$/o){
				#アイコン項目
				($optg==1)&&(print WR "\ \ ");
				print WR qq[<OPTION value="$1">$2</OPTION>\n];
				next;
			}else{
				print WR "$_\n";
			}
		}
		($optg==1)&&(print WR "</OPTGROUP>\n");
		close(WR);
		
		unless($IN{'renew'}){
			&menu('アイコンリスト書き込み完了');
		}else{
			&iconsmp;
			&menu('アイコンリスト・見本書き込み完了');
		}
		exit;
	}
}

#-------------------------------------------------
# アイコン見本更新
sub iconsmp{
	&loadcfg('index','style');

=item

OPTION
 ^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$
 <TD><IMG $1src="$CF{'icon'}$2" alt=\"$1\"$3><BR>$1</TD>

#OPTGOUP
 ^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$
 <TABLE $1summary="$2"$3>
 OPTGROUP内に入った

#/OPTGOUP
 {^</OPTGROUP>$}{</TR></TABLE>}
 OPTGROUP外に出た

=cut

	open(RD,"<$CF{'icls'}")||die"Can't read iconlist($CF{'icls'})[$!]";
	eval{flock(RD,1)};
	
	my$j=0;
	my@others=();
	$AT{'x'}=6;
	my%CR;
	my@icon=();
	my$table=''; #optgroup一つをこれに一時的に格納する
	
	for(<RD>){
		if($_=~m{^\s*<OPTION (.*)value=(["'])(.+?)\2([^>]*)>([^<]*)(</OPTION>)?$}io){
			#アイコン
			if(!$j){
				#others
				push(@others,(@others%$AT{'x'}?'':"</TR>\n<TR>\n")
				.qq(<TD><IMG $1src="$CF{'icon'}$3" alt="$5"$4><BR>$5</TD>\n));
				next;
			}
			$table.=qq(<TD><IMG $1src="$CF{'icon'}$3" alt="$5"$4><BR>$5</TD>\n);
			if($j<$AT{'x'}){
				#グループ内1-5桁
				$j++;
			}else{
				#グループ内6桁目：改行
				$table.="</TR>\n<TR>\n";
				$j=1;
			}
			next;
		}elsif($_=~m{^<OPTGROUP (.*)label=(["'])(.+?)\2(.*)>$}io){
			#アイコングループ始
			$table=<<"_HTML_";
<TABLE $1cellspacing="0" class="icon" summary="$3"$4>
<CAPTION>$3</CAPTION>
<COL span="$AT{'x'}" width="110">
<TR>
_HTML_
			$j=1;
		}elsif($_=~/OPTGROUP/io){#</OPTGROUP>
			#アイコングループ終
			my$copy='';
			if($CR{'VENDOR_LINK'}&&$CR{'COPY1_LINK'}){
				$copy="&#169;$CR{'COPY1_LINK'} &gt;&gt; by$CR{'VENDOR_LINK'}";
			}elsif($CR{'VENDOR_LINK'}){
				$copy="by$CR{'VENDOR_LINK'}";
			}elsif($CR{'COPY1_LINK'}){
				$copy="&#169;$CR{'COPY1_LINK'}";
			}
			$table.=($j>1?"</TR>\n<TR>\n":'').<<"_HTML_";
<TH colspan="$AT{'x'}" class="foot">$copy</TH>
</TR>
</TABLE>

_HTML_
			$j=0;
			push(@icon,$table);
			next;
		}elsif($_=~/<!--\s*%([A-Z0-9]+_)?(VENDOR|COPY1)(_[A-Z0-9]+)?(?:\s+(.*?))?\s*-->/o){

=item

$1: 'BEGIN_','END_'
$2: 'VENDOR','COPY1'
$3: '_NAME','_URL','_LINK'
$4: 

=cut

			if('BEGIN_'eq$1){
				$CR{$2.'_NAME'}='';$CR{$2.'_URL'}='';$CR{$2.'_LINK'}='';
				if($4){$CR{$2.'_NAME'}=$4;}else{next;}
			}elsif('END_'eq$1){
				$CR{$2.'_NAME'}='';$CR{$2.'_URL'}='';$CR{$2.'_LINK'}='';next;
			}elsif($3){
				if('_NAME'eq$3){
					$CR{$2.'_NAME'}=$4;
					($CR{$2.'_LINK'})&&(next);
				}elsif('_URL'eq$3){
					$CR{$2.'_URL'}=$4;
				}elsif('_LINK'eq$3){
					$CR{$2.'_LINK'}=$4;
					next;
				}
			}else{next;}
			if($CR{$2.'_NAME'}&&$CR{$2.'_URL'}){
				$CR{$2.'_LINK'}=qq(<A href="$CR{$2.'_URL'}" title=")
				.(('VENDOR'eq$2)?'製作者':'一次著作権者').qq(">$CR{$2.'_NAME'}</A>);
			}elsif($CR{$2.'_NAME'}){
				$CR{$2.'_LINK'}=$CR{$2.'_NAME'};
			}
			next;
		}
	}
	close(RD);
	
	($j)&&(print WR "</TR></TABLE>\n");
	
	#その他の処理
	if($#others>-1){
		$table=<<"_HTML_";
<TABLE cellspacing="0" class="icon" summary="Others">
<CAPTION>その他</CAPTION>
<COL span="$AT{'x'}" width="110">
@others
</TR>
</TABLE>

_HTML_
		push(@icon,$table);
	}
	undef$table;
	
	open(WR,'+>>icon.html')||die"Can't write iconsample(icon.html)[$!]";
	eval{flock(WR,2)};
	truncate(WR,0);
	seek(WR,0,0);
	print WR <<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">
<LINK rel="start" href="$CF{'home'}">
<LINK rel="index" href="index.cgi">
<TITLE>: Mireille Icon List :</TITLE>
</HEAD>
<BODY style="margin-top:1em">
$CF{'pghead'}
$CF{'menu'}
<H2 class="mode">アイコン見本</H2>\n$CF{'iched'}
@icon
$CF{'icfot'}
$CF{'pgfoot'}
<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_blank"
 title="Airemix - Mireille -">Airemix Mireille</A> <VAR>$CF{'Manage'}</VAR> -</DIV>
</BODY>
</HTML>
_HTML_
	close(WR);

	&menu("アイコン見本更新完了");
}

#-------------------------------------------------
# index.cgiの設定
sub config{
my@required=(
 'name'		=>'サイトの名前'
,'home'		=>'サイトトップページのURL'
,'title'	=>'この掲示板のタイトル（TITLE要素）'
,'pgtitle'	=>'この掲示板のタイトル（ページのヘッダーで表示）'
,'icls'		=>'アイコンリスト'
,'style'	=>'スタイルシート'
,'icon'		=>'アイコンのディレクトリ'
,'icct'		=>'アイコンカタログCGI'
,'help'		=>'ヘルプファイル'
,'navjs'	=>'記事ナビJavaScript'
,'log'		=>'ログディレクトリ'
,'gzip'		=>'gzipの場所'
);
		my@implied=(
 'admps'	=>'管理者パスワード（全ての記事を編集・削除できます 25文字以上推奨）'
,'tags'		=>'使用を許可するタグ（半角スペース区切り）'
,'strong'	=>'強調する記号と対応するCSSのクラス（半角スペース区切りで「記号 クラス 記号・・・」）'
,'newnc'	=>'投稿後*****秒以内の記事にNewマークをつける'
,'newuc'	=>'読んだ記事でも???秒間は「未読」状態を維持する'
,'new'		=>'投稿後*****秒以内の記事につけるNewマーク'
,'page'		=>'通常モードでの1ページあたりのスレッド数'
,'delpg'	=>'削除・修正モードでの1ページあたりのスレッド数'
,'logmax'	=>'最大スレッド数'
,'maxChilds'=>'一スレッドあたりの最大子記事数を制限する'
,'sekitm'	=>'検索できる項目（"項目のname 選択字の名前 "をくりかえす）'
,'prtitm'	=>'親記事の項目(+color +email +home +icon +ra +hua cmd +subject)'
,'chditm'	=>'子記事の項目(+color +email +home +icon +ra +hua cmd)'
,'cokitm'	=>'Cookieの項目(color email home icon)'
,'conenc'	=>'圧縮転送のやり方(Content-Encodingの方法)'
,'ckpath'	=>'Cookieを登録するPATH(path=/ といった形で)'
);
		my@select=(
 'colway'	=>'色の選択方法','input INPUTタグ select SELECTタグ'
,'delold'	=>'古い記事スレッドの削除方法','gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除'
,'delthr'	=>'記事スレッドの削除方法','gzip GZIP圧縮 rename ファイル名変更 unlink ファイル削除'
,'sort'		=>'記事の並び順','number スレッド番号順 date 投稿日時順'
,'prtwrt'	=>'新規投稿フォームをIndexに表示','0 表示しない 1 表示する'
,'mailnotify'=>'新規/返信 があったときに指定アドレスにメールする','0 使わない 1 使う'
,'readOnly'	=>'掲示板を閲覧専用にする','0 読み書きOK 1 閲覧専用'
,'use304'	=>'更新がないときに「304 Not Modified」を渡すか否か'
,'useLastModified'=>'常に「Last-Modified」を渡すか否か'
);
		my@design=(
 'colorList'=>'色リスト'
,'iched'	=>'アイコンリストのヘッダー'
,'icfot'	=>'アイコンリストのフッター'
);
	unless($IN{'name'}){
		my$message='';
		unless(&loadcfg){
			$message=<<'_HTML_';
<H2>index.cgiの読み込みでエラーが発生しました</H2>
<P>index.cgiが破損している可能性があります<BR>
このまま実行すれば、configを上書きして設定しなおせます</P>
_HTML_
		}
		for(%CF){
			$CF{"$_"}=~s/\t/\ \ /go;
			$CF{"$_"}=~s/&/&#38;/go;
			$CF{"$_"}=~s/"/&#34;/go;
			$CF{"$_"}=~s/'/&#39;/go;
			$CF{"$_"}=~s/</&#60;/go;
			$CF{"$_"}=~s/>/&#62;/go;
		}
		print<<"ASDF";
$AT{'head'}

<H2 class="mode">index.cgi編集モード</H2>
$message
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<TABLE style="margin:1em">
<COL style="text-align:left;width:600px"><COL style="text-align:left;width:200px">

<TBODY>
<TR><TH colspan="2"><H3 class="list">稼動させる前に確認すること</H2></TH></TR>
ASDF
		my$i=0;
		#稼動させる前に確認すること
		for($i=0;$i<$#required;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$required[$i+1]：</TH>
<TD><INPUT name="$required[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$required[$i]"}"></TD>
</TR>
ASDF
		}

		print<<"ASDF";
<TR>
<TH class="item">タイムゾーン（「JST-9」のように）：</TD>
<TD><INPUT name="TZ" type="text" style="ime-mode:disabled" value="$ENV{'TZ'}"></TD>
</TR>
</TBODY>

<TBODY>
<TR><TH colspan="2"><H3 class="list">必要に応じて変更</H2></TH></TR>
ASDF
		#必要に応じて変更
		for($i=0;$i<$#implied;$i+=2){
			print<<"ASDF";
<TR>
<TH class="item">$implied[$i+1]：</TH>
<TD><INPUT name="$implied[$i]" type="text" style="ime-mode:inactive;width:200px" value="$CF{"$implied[$i]"}"></TD>
</TR>
ASDF
		}

		#選択型
		for($i=0;$i<$#select;$i+=3){
			print<<"ASDF";
<TR>
<TH class="item">$select[$i+1]：</TH>
<TD>
<SELECT name="$select[$i]">
ASDF
			my$name=$select[$i+2];
			my@label=split(/ /o,$select[$i+2]);
			for(my$j=0;$j<$#label;$j+=2){
				if($label[$j]eq$CF{$select[$i]}){
					print<<"ASDF";
<OPTION value="$label[$j]" selected="selected">$label[$j+1]</OPTION>
ASDF
				}else{
					print<<"ASDF";
<OPTION value="$label[$j]">$label[$j+1]</OPTION>
ASDF
				}
			}
		print<<"ASDF";
</SELECT>
</TD>
</TR>
ASDF
		}
		print<<"ASDF";
</TBODY>

<TBODY>
<TR><TH colspan="2"><H3 class="list">専用アイコン</H2></TH></TR>
<TR>
<TH class="item">専用アイコン機能：</TD>
ASDF
		$i=<<"ASDF";
<TD>
<LABEL for="exiconon">使う<INPUT id="exiconon" name="exicon" type="radio" value="1" checked></LABEL>
<LABEL for="exiconof">使わない<INPUT id="exiconof" name="exicon" type="radio" value="0"></LABEL>
</TD>
</TR>
<TR>
ASDF
		$i=~s/(value=\"$CF{'exicon'}\")/$1 checked="checked"/o;
		print$i;
		my@IC=keys%IC;
		for(0..($#IC+5)){
			my$key='';my$val='';
			if($_<=$#IC){
				$key=$IC[$_];
				$val=$IC{$IC[$_]}
			}
			print<<"ASDF";
<TR>
<TH class="item">パスワード：<INPUT name="ICN$_" type="text" style="ime-mode:disabled" value="$key"></TD>
<TD>ファイル名：<INPUT name="ICV$_" type="text" style="ime-mode:disabled" value="$val"></TD>
</TR>
ASDF
		}
		print<<"ASDF";
<TR><TH colspan="2"><H3 class="list">Mireille内のHTMLデザイン</H2></TH></TR>
ASDF
		#Mireille内のHTMLデザイン
		for($i=0;$i<$#design;$i+=2){
			print<<"ASDF";
<TR><TH class="item" colspan="2">$design[$i+1]：</TH></TR>
<TR><TD colspan="2"><TEXTAREA name="$design[$i]" cols="130" rows="7" style="ime-mode:inactive;width:800px">$CF{$design[$i]}</TEXTAREA></TD></TR>
ASDF
		}
		print<<"ASDF";
</TABLE>
<P>
<INPUT name="mode" type="hidden" value="config">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
	}else{
		for(keys%IN){
			$IN{"$_"}=~s/(\n)*$//;
			$IN{"$_"}=~s/^_CONFIG_$/(_CONFIG_)/gmo;
		}
		
		open(RD,"<$AT{'manage'}")||die"Can't read manage($AT{'manage'})[$!]";
		eval{flock(RD,1)};
		my$config=<RD>;
		close(RD);

		$config.=<<"ASDF";

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Index File -
#
# \$$CF{'Manage'}\$
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
require 5.004;
use strict;
use vars qw(\%CF \%IC);
\$|=1;

#-------------------------------------------------
# 稼動させる前に確認すること

ASDF
		my$i=0;
		for($i=0;$i<$#required;$i+=2){
			$config.=<<"ASDF";
#$required[$i+1]
\$CF{\'$required[$i]\'}=\'$IN{"$required[$i]"}\';
ASDF
		}
		$config.=<<"ASDF";
#タイムゾーン（「JST-9」のように）
\$ENV{'TZ'}=\'$IN{'TZ'}\';

#-------------------------------------------------
# 必要に応じて変更

ASDF
		for($i=0;$i<$#implied;$i+=2){
			$config.=<<"ASDF";
#$implied[$i+1]
\$CF{\'$implied[$i]\'}=\'$IN{"$implied[$i]"}\';
ASDF
		}
		for($i=0;$i<$#select;$i+=3){
			$config.=<<"ASDF";
#$select[$i+1] ($select[$i+2])
\$CF{\'$select[$i]\'}=\'$IN{"$select[$i]"}\';
ASDF
		}
		$config.=<<"ASDF";
#専用アイコン機能 (ON 1 OFF 0)
\$CF{'exicon'}=\'$IN{'exicon'}\';
#専用アイコン列挙
#\$IC{'PASSWORD'}='FILENAME'; #NAME
#\$IC{'hae'}='mae.png'; #苗
#\$IC{'hie'}='mie.png'; #贄
#\$IC{'hue'}='mue.png'; #鵺
#\$IC{'hee'}='mee.png'; #姐
#\$IC{'hoe'}='moe.png'; #乃絵
#例：コマンドに"icon=hoe"と入れると乃絵さん専用の'moe.png'が使えます
#手入力するときは「\$IC{'hoe'}='moe.png'; #乃絵」のように、最初の「#」を取るのを忘れずに
ASDF
		for(my$i=0;defined$IN{"ICN$i"};$i++){
			($IN{"ICN$i"}&&$IN{"ICV$i"})||(next);
			$config.=qq{\$IC{\'$IN{"ICN$i"}\'}=\'$IN{"ICV$i"}\';\n};
		}
		$config.=<<"ASDF";

#-------------------------------------------------
# Mireille内のHTMLデザイン

ASDF
		for($i=0;$i<$#design;$i+=2){
			$config.=<<"ASDF";
#-----------------------------
# $design[$i+1]
\$CF{\'$design[$i]\'}=<<'_CONFIG_';
$IN{$design[$i]}
_CONFIG_

ASDF
		}
		$config.=<<'ASDF';
#-------------------------------------------------
# 実行 or 読み込み？

if($CF{'program'}eq __FILE__){
	#直接実行だったら動き出す
	require 'core.cgi';
	require 'style.pl';
	&main;
}

#-------------------------------------------------
# 初期設定
BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\n"
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
ASDF
		$config.=<<"ASDF";
	\$CF{'Index'}=qq\$$CF{'Manage'}\$;
	getlogin||umask(0); #nobody権限で作ったファイルをユーザが消せるように
}

1;
__END__
ASDF
		open(WR,'+>>index.cgi')||die"Can't write index.cgi[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $config;
		close(WR);
		
		&menu('index.cgiに書き込み完了');
	}
	exit;
}

#-------------------------------------------------
# CSSの編集
sub css{
	unless($IN{'file'}){
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">スタイルシートファイル選択</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSSファイル名<INPUT name="file" type="text" style="ime-mode:disabled" value="$IN{'file'}">（拡張子は入力しない）<BR>
例：$CF{'style'}なら、styleとだけ入力する<BR>
万が一のセキュリティ確保のためですので、あしからず</P>
<P>
<INPUT name="mode" type="hidden" value="css">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
	}elsif(!$IN{'css'}){
		open(RD,"<$IN{'file'}.css")||die"Can't read css($IN{'file'}.css)[$!]";
		eval{flock(RD,1)};
		my$css=join('',<RD>);
		close(RD);
		
		study$css;
		$css=~/\@charset\s*[\"\']([\-\w]*)[\"\']/io;
		$IN{'code'}=$1;
		($IN{'code'}=~/Shift_JIS/io)&&($css=sjis2euc($css));
		$css=~s/\t/\ \ /go;
		$css=~s/&/&#38;/go;
		$css=~s/"/&#34;/go;
		$css=~s/'/&#39;/go;
		$css=~s/</&#60;/go;
		$css=~s/>/&#62;/go;
		
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">スタイルシート編集モード</H2>
<FORM accept-charset="euc-jp" name="cssedit" method="post" action="$AT{'manage'}">
<P>CSSファイル名:$IN{'file'}.css<INPUT name="file" type="hidden" value="$IN{'file'}"><P>
<P><TEXTAREA name="css" cols="100" rows="15">$css</TEXTAREA><P>
<P>
<INPUT name="code" type="hidden" value="$IN{'code'}">
<INPUT name="mode" type="hidden" value="css">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
	}else{
		$IN{'css'}=~s/(\n)*$/\n/o;
		if($IN{'code'}=~/Shift_JIS/i){
			$IN{'css'}=euc2sjis($IN{'css'});
		}
		open(WR,"+>>$IN{'file'}\.css")||die"Can't write css($IN{'file'}.css)[$!]";
		eval{flock(WR,2)};
		truncate(WR,0);
		seek(WR,0,0);
		print WR $IN{'css'};
		close(WR);
		
		&menu('css書き込み完了');
	}
	exit;
}

#-------------------------------------------------
# ログ管理
sub log{
	unless($IN{'type'}){
		#ログ管理初期メニュー
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">ログ管理モード</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>バックアップ削除</LEGEND>
<LABEL for="back"><INPUT name="type" id="back" type="radio" value="3" accesskey="y" checked="checked"
>バックアップファイルを削除する(<SPAN class="ak">Y</SPAN>)</LABEL>
<PRE style="text-align:center">ファイル名変更型削除やログの増大のときにできたバックアップファイルを一掃します</PRE>
</FIELDSET>

<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>記事スレッドを削除</LEGEND>
<FIELDSET style="padding:0.5em;width:90%">
<LEGEND>削除するファイルの指定</LEGEND>

<P style="text-align:left"><INPUT name="type" type="radio" value="1" accesskey="y"
>スレッド番号<INPUT name="str" type="text" size="3" style="ime-mode:disabled" value=""
>から<INPUT name="end" type="text" size="3" style="ime-mode:disabled" value=""
>まで削除する(<SPAN class="ak">Y</SPAN>)<BR>
前の□に何も入れなかった場合は、1〜□を削除し、<BR>
後の□に何も入れなかった場合は、□から最新を残してそれより昔のものをを削除します<BR>
かなり危険なコマンドでもあるので、必ず実行前にバックアップをとるようにしましょう</P>

<P style="text-align:left"><INPUT name="type" type="radio" value="2" accesskey="y"
>最新から<INPUT name="save" type="text" size="3" style="ime-mode:disabled" value=""
>個残して、それ以外を削除する(<SPAN class="ak">Y</SPAN>)<BR>
ここでいう「最新」とはスレッド番号の最も大きい物、のことです<BR>
必ず実行前にバックアップをとるようにしましょう</P>
</FIELDSET>


<FIELDSET style="padding:0.5em;width:50%">
<LEGEND accesskey="c">削除方式</LEGEND>
<LABEL for="rename">ファイル名変更：<INPUT name="del" id="rename" type="radio" value="rename" checked></LABEL>
<LABEL for="unlink">ファイル削除：<INPUT name="del" id="unlink" type="radio" value="unlink"></LABEL>
</FIELDSET>

<P><LABEL for="push"><INPUT id="push" name="push" type="checkbox" value="1">スレッド番号をつめる</LABEL>
<BR>スレッド番号を１から順番に変更します</P>
</FIELDSET>

<P><INPUT name="mode" type="hidden" value="log">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
@{[&getFooter]}
ASDF
	}elsif($IN{'type'}=~/^\d$/){
		#ログ管理第一段階
		print<<"_HTML_";
$AT{'head'}
<H2 class="mode">ログ管理モード</H2>
<FORM accept-charset="euc-jp" name="logedit" method="post" action="$AT{'manage'}">
_HTML_
		if($IN{'type'}==1){
			#□〜□型指定
			if(!$IN{'str'}&&!$IN{'end'}){
				print<<"_HTML_";
<P>開始スレッド番号と終了スレッド番号が共に入力されていません<BR>
戻って指定しなおしてください</P>
_HTML_
			}else{
				my$delete;
				if($IN{'str'}&&$IN{'end'}){
					$delete="$IN{'str'}から$IN{'end'}まで";
				}elsif(!$IN{'str'}){
					$delete="最初から$IN{'end'}まで";
				}elsif(!$IN{'end'}){
					$delete="$IN{'str'}から最新まで";
				}
				print<<"_HTML_";
<P>本当に、$deleteを@{[('unlink'eq$IN{'del'})?'ファイル削除':'ファイル名変更']}で削除してよろしいですか？
<INPUT name="str" type="hidden" size="3" value="$IN{'str'}" readonly>
<INPUT name="end" type="hidden" size="3" value="$IN{'end'}" readonly>
<INPUT name="type" type="hidden" value="a">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
_HTML_
			}
		}elsif($IN{'type'}==2){
			#1〜(最新-□)型指定
			&loadcfg;
			my@file=&logfiles;
			my$i=$#file-$IN{'save'}+1;
			print<<"ASDF";
<P>本当に、最新から<INPUT name="save" type="text" size="3" value="$IN{'save'}" readonly
>個残して@{[('unlink'eq$IN{'del'})?'ファイル削除':'ファイル名変更']}で削除してよろしいですか？<BR>
スレッド番号$file[$#file]から$file[$IN{'save'}]までの、$i件を削除します
<INPUT name="type" type="hidden" value="b">
<INPUT name="del" type="hidden" value="$IN{'del'}">
</P>
ASDF
		}elsif($IN{'type'}==3){
				#バックアップ削除
				print<<"ASDF";
<P>本当に、バックアップファイルを一掃してよろしいですか？</P>
<INPUT name="type" type="hidden" value="c">
ASDF
		}else{
			exit;
		}
		
		print<<"ASDF";
<BR>
<P>
<INPUT name="mode" type="hidden" value="log">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT name="push" type="hidden" value="$IN{'push'}">
ログ詰め: @{[$IN{'push'}?'する':'しない']}</P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
</FORM>
<P><A href="$AT{'manage'}" title="管理">間違えたので最初からやり直す</A></P>
@{[&getFooter]}
ASDF
	}elsif($IN{'type'}=~/^\w$/){
		&loadcfg;
		if('c'eq$IN{'type'}){
			my$file=unlink<$CF{'log'}*.bak>;
			$file.=unlink<$CF{'log'}*.bak.cgi>;
			$file.=unlink<$CF{'log'}*.bak.pl>;
			$file.=unlink<$CF{'log'}*.gz>;
			$file.=unlink<$CF{'log'}*.gz.cgi>;
			$file.=unlink<$CF{'log'}*.bz2.cgi>;
			&menu("$file個のバックアップファイルを削除しました");
		}
		my@file=&logfiles;#(4,3,2,1)
		if($IN{'type'}eq'a'){
			if($IN{'str'}&&$IN{'end'}){
			}elsif(!$IN{'str'}){
				$IN{'str'}=1;
			}elsif(!$IN{'end'}){
				$IN{'end'}=$file[0];
			}
		}elsif($IN{'type'}eq'b'){
			$IN{'str'}=$file[$#file];
			$IN{'end'}=$file[$IN{'save'}];
		}else{
			exit;
		}

		my$file=0;
		if('unlink'eq$IN{'del'}){
			for($IN{'str'}..$IN{'end'}){
				(unlink"$CF{'log'}$_.cgi")||(next);
				$file++;
			}
		}else{
			for($IN{'str'}..$IN{'end'}){
				(rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi"))||(next);
				$file++;
			}
		}
		
		if($IN{'push'}){
			open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
			eval{flock(ZERO,2)};
			truncate(ZERO,0);
			seek(ZERO,0,0);
			my@zero=();
			while(<ZERO>){
				chomp$_;push(@zero,$_);
			}
			my@zer0=split("\t",$zero[0]);
			my@zer1=split(/ /,$zero[1]);
			my@zer2=split(/ /,$zero[2]);
			my@zerC=();
			my$zerD='';
			my$i=1;
			for(@file){
				rename("$CF{'log'}$_.cgi","$CF{'log'}$i.cgi")||die"Can't rename log($_.cgi->$i)[$!]";
				$zerC["$i"]=$zer2["$_"];
				$zerD.="$_=$i;";
				$i++;
			}
			$zerC[0]=0;
			chop$zerD;#最後の' '削り
			
			truncate(ZERO,0);
			seek(ZERO,0,0);
			print ZERO "@zer0\n";
			print ZERO "@zer1\n";
			print ZERO "@zerC\n";
			print ZERO "$zerD\n";#ファイル名変更のログ
			close(ZERO);
			
			&menu("ログ$IN{'str'}〜$IN{'end'}のファイル$file個を削除完了<BR>ログ詰め成功");
		}
		
		&menu("ログ$IN{'str'}〜$IN{'end'}のファイル$file個を削除完了");
	}
	
	exit;
}

#-------------------------------------------------
# 0.cgi（記事情報管理ファイル）の回復
sub zero{
	unless($IN{'recover'}){
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">記事情報ファイル回復モード</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">
<P>記事情報ファイルをリカバリすると、既存の情報は失われます<BR>
それでもよろしいですか？
<INPUT name="mode" type="hidden" value="zero">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><LABEL accesskey="r" for="recover">回復する
<INPUT name="recover" id="recover" type="checkbox" value="1"></LABEL></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
		exit;
	}else{
		&loadcfg;
		my@file=&logfiles;
		my@zer2=();	
		for(@file){
			$zer2[$_-$file[$#file]]=(stat("$CF{'log'}$_.cgi"))[9];
		}
		unshift(@zer2,$file[$#file]-1);
		
		open(ZERO,"+>>$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$!]";
		eval{flock(ZERO,2)};
		truncate(ZERO,0);
		seek(ZERO,0,0);
		print ZERO <<"ASDF";
Mir12=\t;\ttitle=\t記事情報ファイルを回復しました;\tname=\tMireille;\tcolor=\t#fd0;\ttime=\t$^T;\t

@zer2
ASDF
		close(ZERO);
		&menu("記事情報ファイル回復完了");
	}
	exit;
}


#-------------------------------------------------
# 管理CGI自体の管理
sub manage{
	unless($IN{'manage'}){
		print<<"ASDF";
$AT{'head'}
<H2 class="mode">管理CGIの管理</H2>
<FORM accept-charset="euc-jp" name="zero" method="post" action="$AT{'manage'}">

<FIELDSET style="padding:0.5em;width:25em;text-align:left">
<LEGEND accesskey="m">やること(<SPAN class="ak">M</SPAN>)</LEGEND>
<LABEL accesskey="r" for="rename"><INPUT name="manage" type="radio" id="rename" value="rename"
 checked>管理CGIファイル名変更(<SPAN class="ak">R</SPAN>)</LABEL>
<BR>
　
<LABEL accesskey="n" for="filename">変更後のファイル名(<SPAN class="ak">N</SPAN>)：
&#34;<INPUT name="filename" type="text" id="filename" value="">.cgi&#34;</LABEL>
<BR>
<LABEL accesskey="u" for="unlink"><INPUT name="manage" type="radio" id="unlink" value="unlink"
>管理CGIファイルを削除(<SPAN class="ak">U</SPAN>)</LABEL>
</FIELDSET>

<INPUT name="mode" type="hidden" value="manage">
<INPUT name="pass" type="hidden" value="$IN{'pass'}"></P>
<P><INPUT type="submit" accesskey="s" class="submit" value="OK"></P>
@{[&getFooter]}
ASDF
		exit;
	}else{
		if('rename'eq$IN{'manage'}){
			($IN{'filename'})||(&menu('変更後のファイル名が入力されていませんでした'));
			(rename(__FILE__,"$IN{'filename'}.cgi"))||(die"変更失敗\n$!\nできないのかもしれない");
			&menu(qq(ファイル名を<A href="$IN{'filename'}.cgi">$IN{'filename'}.cgi</A>に変更しました));
		}elsif('unlink'eq$IN{'manage'}){
			(unlink(__FILE__))||(die"削除失敗\n$!\nできないのかもしれない");
			&menu("管理CGIを削除しました");
		}
	}
	exit;
}


#-------------------------------------------------
# config読み込み
#
sub loadcfg{
	my%cfg;
	for(@_){$cfg{$_}=1;}
	if($cfg{'index'}&&$cfg{'style'}){
		(require 'index.cgi')&&(require 'style.pl');
	}elsif($cfg{'style'}){
		require 'style.pl';
	}else{
		require 'index.cgi';
	}
}

#-------------------------------------------------
# ログファイル名配列の取得
#
sub logfiles{
	$CF{'Index'}||&loadcfg;
	opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$!]";
	my@file=sort{$b<=>$a}map{m/^(?!0)(\d+)\.cgi$/o}readdir(DIR);
	closedir(DIR);
	return@file;
}

#-------------------------------------------------
# フッターの生成
#
sub getFooter{
	return<<"_HTML_";
<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="Footer" width="90%"><TR>
<TD nowrap>■■■■■■■</TD>
<TH width="100%"><H1 class="head" align="right"><A href="index.cgi">BACK to INDEX</A></H1></TH>
</TR></TABLE></DIV>

<DIV class="AiremixCopy">- <A href="http://www.airemix.com/" target="_blank" title="Airemix - Mireille -">Airemix Mireille</A>
<VAR title="times:@{[times]}">$CF{'Manage'}</VAR> -</DIV>
</BODY>
</HTML>
_HTML_
}


#------------------------------------------------------------------------------#
# jcode.pl: Perl library for Japanese character code conversion
# Copyright (c) 1992-2000 Kazumasa Utashiro <utashiro@iij.ad.jp>
#  ftp://ftp.iij.ad.jp/pub/IIJ/dist/utashiro/perl/
sub sjis2euc{
	my$s=$_[0];
	$s=~s<([\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc]|[\xa1-\xdf])>
	[
		my($c1,$c2)=unpack('CC',$1);
		if(0xa1<=$c1&&$c1<=0xdf){
			$c2=$c1;$c1=0x8e;
		}elsif(0x9f<=$c2){
			$c1=$c1*2-($c1>=0xe0?0xe0:0x60);$c2+=2;
		}else{
			$c1=$c1*2-($c1>=0xe0?0xe1:0x61);$c2+=0x60+($c2<0x7f);
		}
		pack('CC',$c1,$c2);
	]ego;
	return$s;
}

sub euc2sjis{
	my$s=$_[0];
	$s=~s<([\xa1-\xfe]{2}|\x8e[\xa1-\xdf]|\x8f[\xa1-\xfe]{2})>
	[
		my($c1,$c2)=unpack('CC',$1);
		if($c1==0x8e){#SS2
			substr($1,1,1);
		}elsif($c1==0x8f){#SS3
			"\x81\xac";
		}elsif($c1 % 2){
			pack('CC',($c1>>1)+($c1<0xdf?0x31:0x71),$c2-0x60-($c2<0xe0));
		}else{
			pack('CC',($c1>>1)+($c1<0xdf?0x30:0x70),$c2-2);
		}
	]ego;
	return$s;
}

#------------------------------------------------------------------------------#
# BEGIN

BEGIN{
	# Mireille Error Screen 1.4
	unless(%CF){
		$CF{'program'}=__FILE__;
		$SIG{'__DIE__'}=sub{
			if($_[0]=~/^(?=.*?flock)(?=.*?unimplemented)/){return}
			print"Content-Language: ja-JP\nContent-type: text/plain; charset=euc-jp\n"
			."\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.4 (o__)o// *\n\n";
			print"ERROR: $_[0]\n"if@_;
			print join('',map{"$_\t: $CF{$_}\n"}grep{$CF{"$_"}}qw(Manage Index Style Core Exte))
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
	$CF{'Manage'}=q$Revision$;
	$CF{'style'} = 'style.css';

	__FILE__=~/([^\/\\:]+)$/o;
	$AT{'manage'}=$1;
	$AT{'head'}=<<"_HTML_";
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<!--DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"-->
<HTML lang="ja-JP">
<HEAD>
<META http-equiv="Content-type" content="text/html; charset=euc-jp">
<META http-equiv="Content-Script-Type" content="text/javascript">
<META http-equiv="Content-Style-Type" content="text/css">
<META http-equiv="MSThemeCompatible" content="yes">
<LINK rel="stylesheet" href="$CF{'style'}" media="screen" type="text/css">
<TITLE>Mireille Administrative Tools</TITLE>
</HEAD>

<BODY>

<DIV class="center"><TABLE align="center" border="0" cellspacing="0" class="head" summary="Header" width="90%"><TR>
<TH width="100%"><H1 class="head">Mireille Administrative Tools</H1></TH>
<TD nowrap>■■■■■■■</TD>
</TR></TABLE></DIV>
_HTML_
}

1;
__END__
