#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Core File -
#
 $CF{'correv'}=qq$Revision$;
# "This file is written in euc-jp, CRLF." 空
# Scripted by NARUSE Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.004;
use Fcntl qw(:DEFAULT :flock);
use strict;
use vars qw(%CF %IC %IN %CK %Z0 @zer2 @file);

INIT:{
  if($0=~m{core.cgi$}o){
    #直接実行だったら動き出す
    &locate($ENV{'CONTENT_LENGTH'});
  }
  DIR:{
    ($CF{'log'})||die"Undefined LogDir!";
    (-e"$CF{'log'}")&&(last DIR);
    (mkdir"$CF{'log'}",0777)&&(last DIR);
    die"Can't read/write/create LogDir!";
  }
  sysopen(ZERO,"$CF{'log'}0.cgi",O_CREAT|O_WRONLY)||die"Can't write log0!";
  print ZERO <<"ASDF";
Mir1=	0-0;	subject=	Welcome to Mireille;	name=	System;	time=	999499209;	body=	LOGディレクトリ及び0.cgiが正常に設置されていなかったようです自動的に設置しなおしました;	
ASDF
  close(ZERO);
}

#-------------------------------------------------
# MARD SWITCH
#
#モードごとの振り分け
MAIN:{
  #記事表示
  (&getfm)||(last MAIN);
  #記事書き込み
  (defined$IN{'body'})&&(&write);
  #返信
  ($IN{'i'})&&(&res);
  #新規書き込み
  if(defined$IN{'j'}){&getck;&header;&prtfrm(\%CK,'j'=>0);&footer;}
  #検索
  (defined$IN{'seek'})&&(&seek);
  #記事修正リストor実行
  if(defined$IN{'rvs'}){($IN{'rvs'})||(&rvsmenu);&revise;}
  #記事削除リストor実行
  if(defined$IN{'del'}){($IN{'del'})||(&rvsmenu);&delete;}
  #ヘルプ
  (defined$IN{'help'})&&(&locate($CF{'help'}));
  #ホーム
  (defined$IN{'home'})&&(&locate($CF{'home'}));
  #記事表示
  last MAIN;
  exit;
}

#------------------------------------------------------------------------------#
# MARD ROUTINS
#
# MAIN:直下のサブルーチン群

#-------------------------------------------------
# Index 記事表示
#
#sub index{
  my$new=0;
  #-----------------------------
  #Cookie取得＆書き込み
  if(&getck){
    &wrtcook(\%CK);
  }else{
    $CK{'time'}=$^T-$CF{'newnc'};
  }

  #-----------------------------
  # HTTP,HTML,PAGEヘッダーを表示
  &header;

  #-----------------------------
  #ページ処理
  &logfiles($CF{'sort'});
  if($IN{'read'}){
    my%FILE;my$i=1;my$j=1;
    for(@file){
      $FILE{"$_"}="$i";
      (++$j>$CF{'page'})||(next);
      $i++;$j=1;
    }
    $IN{'page'}=$FILE{"$IN{'read'}"};
  }
  my$max=int(($#file-1)/$CF{'page'})+1;
  ($max<$IN{'page'})&&($IN{'page'}=$max);
  ($IN{'page'})||($IN{'page'}=1);

  #-----------------------------
  #新規投稿フォームを表示する（設定による）
  if($CF{'prtwrt'}){
    &prtfrm(\%CK,'j'=>0);
  }
  print"$CF{'note'}";

  #-----------------------------
  #記事情報
  my@new=();my%NEW;
  for(1..$#zer2){
    my$No=$_+$zer2[0];
    ($zer2[$_]>$CK{'time'})||(next);
    unshift(@new,qq{<a href="$CF{'index'}?read=$No#$No" class="new">$No</a>});
    $NEW{"$No"}=1;
  }
  my$info="<p>";
  #20件まで
  if($#new>19){
    $info.=qq{未読記事のあるスレッド[ @new[0..20] .. ]<br>\n};
  }elsif($#new>-1){
    $info.=qq{未読記事のあるスレッド[ @new[0..$#new] ]<br>\n};
  }

  my@i=@file;@i=splice(@i,($IN{'page'}-1)*$CF{'page'},$CF{'page'});
  (($i[0]!=0)&&(!$i[$#i]))&&(pop@i);

  $info.="このページのスレッド<br>\n[ ";
  $new=0;
  for(@i){
    $new++;
    if($NEW{"$_"}){
      $info.=qq{<a href="#$_" title="Alt+$new"><span class="new">$_</span></a> };
    }else{
      $info.=qq{<a href="#$_" title="Alt+$new">$_</a> };
    }
  }
  $info.="]</p>\n";
  print$info;

  #-----------------------------
  #ページ選択TABLEを表示
  my$pgslct=&pgslct($max);
  print"$pgslct";

  #-----------------------------
  #記事表示
  $new=0;
  if($#file){
    #既に稼動中のとき
    my$i=1;
#    if($CF{'prtres'}){
#      for(@i){
#        $new+=&article('i'=>$_,'ak'=>$i++,%CK);
#      }
#    }else{
      for(@i){
        $new+=&article('i'=>$_,'ak'=>$i++);
      }
#    }
  }else{
    #log0のみ つまり設置直後のとき
#    if($CF{'prtres'}){
#      &article('i'=>0,'ak'=>1,%CK);
#    }else{
      &article('i'=>0,'ak'=>1);
#    }
  }

  #-----------------------------
  #未読記事お知らせ機能
  ($new)&&(print"<p><span class=\"new\">このページに未読記事が$new件ありました♪</span></p>\n");
  print$info;

  #-----------------------------
  #ページ選択TALBEとフッター
  print"$pgslct";
  &footer;

  exit;
#}


#-------------------------------------------------
# 記事書き込み
#
sub write{
  #-----------------------------
  #エラー表示
  my@error;
  ($IN{'name'})||(push(@error,"<span style=\"color:#f00\">名前</span>"));
  ($IN{'body'})||(push(@error,"<span style=\"color:#f00\">本文</span>"));
  ($IN{'pass'}||($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'})))
   ||(push(@error,'<span style="color:#f00">パスワード</span>'));

  if($#error>-1){
    my$error=join('と',@error);
    &header;
    print<<"_HTML_";
<h2 class="mode">- Write Error -</h2>
<p>$errorをちゃんと入力してください</p>
_HTML_
    &rvsij(\%IN);
    &footer;
  }
  
  SUBJECT:{
    #subject周りの処理
    if($IN{'j'}){
      ($CF{'chditm'}=~m/\bsubject\b/o)||(last SUBJECT);
    }else{
      ($CF{'prtitm'}=~m/\bsubject\b/o)||(last SUBJECT);
    }
    unless($IN{'subject'}){
      $IN{'subject'}=$IN{'body'};
      $IN{'subject'}=~s/<br>/\n/o;
    }
    my$i=substr($IN{'subject'},0,80);
    $i=~m/(.{0,80})/o;
    $i=$1;
    if($i=~/\x8F$/o){
      chop$i;
    }elsif($i=~tr/\x8E\xA1-\xFE//%2){
      $i.=substr($IN{'subject'},80,1);
    }
    $IN{'subject'}=$i;
  }
  
  #-----------------------------
  #専用アイコン機能。config.plで設定する。
  if($CF{'exicon'}&&$IN{'cmd'}){
    my%EX=split(/[=&;]/o,$IN{'cmd'});
    #custom.plで指定したアイコンパスに合致すれば。
    ($IC{"$EX{'icon'}"})&&($IN{'icon'}=$IC{"$EX{'icon'}"});

=item 持ち込みアイコン

#    ($EX{'bring'})&&($IN{'icon'}=$EX{'bring'});
持ち込みアイコンを真に稼動させるためには$CF{'icon'}=''としないと、
意味がありません
しかし、画像持込は大きな画像を貼られるというわかりやすいもののほかにも、
使い方によっては利用者の情報を収集することができるという危険があるので、[
信用の置ける人しか来ない場所で無い限り使わないほうがいいです

モジュールImage::sizeを用いることによって、サイズ制限をかけることが出来るかもしれません
これならとりあえず安全性は増しますが、CGIを使われると投稿者の情報が流出する、、
という可能性が依然残っているため、無制限にすることは出来ないでしょう

=cut

  }

  #-----------------------------
  #$IN{'cook'}がONならCookieの書き込み
  COOKIE:{
    ($IN{'cook'})||(last COOKIE);
    ($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'}))&&(last COOKIE);
    &getck;
    &wrtcook(\%IN);
  }


  #-----------------------------
  #書き込みデータ準備
  sysopen(ZERO,"$CF{'log'}0.cgi",O_RDWR)||die"Can't write log0!";
  flock(ZERO,LOCK_EX);
  my@zero=();
  while(<ZERO>){
    chomp$_;push(@zero,$_);
  }
  ($zero[0]=~/^Mir1=\t/o)||(die"ログ形式がMir1型以外です");
  %Z0=($zero[0]=~m/([^\t]*)=\t([^\t]*);\t/go);
  my@zer1=split(/ /,$zero[1]);
  @zer2=split(/ /,$zero[2]);
  $IN{'newps'}=&mircrypt($^T,$IN{'pass'});
  
  #-----------------------------
  &logfiles('number');
  if($IN{'i'}){
    (($IN{'i'}>$file[0]+1)||($IN{'i'}<1))&&($IN{'i'}=$file[0]+1);
  }
  
  if((length$IN{'j'})xor($IN{'i'})){
    #新規・返信書き込み
    my$i=$IN{'i'};
    my$j=$IN{'j'};
    ($i)||($i='\\d+');
    (length$j)||($j='\\d+');
    if($zero[1]=~/($i):$ENV{'CONTENT_LENGTH'}:($j)/){
      
      &header;
  print<<"_HTML_";
<h2 class="mode">- 多重投稿排除 -</h2>
<p style="margin:0.6em">以下の内容は第$1番スレッドの$2番目と同一内容だと思われます<br>
同一内容でない場合は、下のフォームで少し修正してから投稿してください。</p>
<table summary="BackMenu" width="300"><tr>
<colgroup span="2" width="150">
<td><form action="$CF{'index'}" method="get">
<input type="submit" class="button" accesskey="b" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="掲示板に戻る(B)">
</form></td>
<td><form action="$CF{'home'}" method="get">
<input type="submit" class="button" accesskey="h" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="$CF{'name'}に戻る(H)">
</form></td>
</tr></table>
_HTML_
      &rvsij(\%IN,'i'=>$1,'j'=>$2);
      &footer;
    }elsif(!defined$IN{'i'}){ #((!defined$IN{'i'})&&($IN{'j'}eq'0'))
      #-----------------------------
      #新規書き込み
      if($CF{'logmax'}>0){
        #古い記事スレッドファイルを ファイル名変更/削除 する
        if($#file>=$CF{'logmax'}){
          my$del=0;
          if($CF{'autodel'}eq'unlink'){
            #削除
            for($file[$#file-1]..$file[$CF{'logmax'}-1]){
              $del++;
              unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog!";
            }
          }else{
            #ファイル名変更
            for($file[$#file-1]..$file[$CF{'logmax'}-1]){
              $del++;
              rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")
               ||die"Can't rename oldlog!";
            }
          }
          splice(@zer2,1,$del);
          $zer2[0]=$file[$CF{'logmax'}-1];
        }
      }

      $IN{'i'}=$file[0]+1;
      $IN{'j'}=0;
      sysopen(WR,"$CF{'log'}$IN{'i'}.cgi",O_CREAT|O_WRONLY)||die"Can't write log$IN{'i'}!";
      flock(WR,LOCK_EX);
    print WR "Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t";
      for($CF{'prtitm'}=~m/\+([a-z\d]+)\b/go){
        print WR qq($_=\t$IN{"$_"};\t);
      }
      print WR "\n";
      close(WR);
    }elsif($IN{'i'}){ #($IN{'i'})&&(!defined$IN{'j'})
      #-----------------------------
      #返信書き込み
      sysopen(RW,"$CF{'log'}$IN{'i'}.cgi",O_CREAT|O_RDWR)||die"Can't write log$IN{'i'}!";
      flock(RW,LOCK_EX);
      seek(RW,0,0);
      my@log=<RW>;
      $IN{'j'}=$#log+1;
      seek(RW,0,2);
    print RW "Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$^T;\tbody=\t$IN{'body'};\t";
      for($CF{'chditm'}=~m/\+([a-z\d]+)\b/go){
        print RW qq($_=\t$IN{"$_"};\t);
      }
      print RW "\n";
      close(RW);
    }
    
    #-----------------------------
    #ログ管理ファイル、0.plに書き込み
    #新規・返信の時には投稿情報を保存
    ($#zer1>2)&&(splice(@zer1,2));
    unshift(@zer1,"$IN{'i'}:$ENV{'CONTENT_LENGTH'}:$IN{'j'}");
    my$No=$IN{'i'}-$zer2[0];
    ($No>0)||(die"ZER2のデータが不正です 'i':$IN{'i'},'zer2':$zer2[0]");
    $zer2[$No]=$^T;
    truncate(ZERO,0);
    seek(ZERO,0,0);
    print ZERO <<"_HTML_";
Mir1=\t$IN{'i'}-$IN{'j'};\tsubject=\t$IN{'subject'};\tname=\t$IN{'name'};\ttime=\t$^T;\t
@zer1
@zer2
_HTML_
    
    #-----------------------------
    #MailNotify
    
    #新規/返信があった場合はメールを送る
    if($CF{'mailnotify'}){
      require'notify.pl';
      (&mailnotify(%IN))||(print ZERO 'MailNotify Failed.\n');
    }
  }elsif(($IN{'i'})&&(defined$IN{'j'})){
    #-----------------------------
    #修正書き込み
    sysopen(RW,"$CF{'log'}$IN{'i'}.cgi",O_RDWR)||die"Can't write log$IN{'i'}!";
    flock(RW,LOCK_EX);
    my@log=<RW>;
    chomp$log[$IN{'j'}];
    my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

    if($CF{'maspas'}&&($IN{'oldps'}eq$CF{'maspas'})){
      #MasterPassによる
      if($IN{'pass'}){
        #Pass変更
        $IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
      }else{
        $IN{'newps'}=$DT{'pass'};
      }
      $IN{'pass'}='';
    }else{
      #UserPassによる
      unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
        &header;
        print qq[<h2 class="mode">Password Error</h2>\n];
        &rvsij(\%IN);
        &footer;
        exit;
      }
      $IN{'newps'}=&mircrypt($DT{'time'},$IN{'pass'});
    }

    #書き込み
    $log[$IN{'j'}]
    ="Mir1=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'newps'};\ttime=\t$DT{'time'};\tbody=\t$IN{'body'};\t";
    if($IN{'j'}eq'0'){
      #親記事
      for($CF{'prtitm'}=~m/\+([a-z\d]+)\b/go){
        $log[$IN{'j'}].=qq($_=\t$IN{"$_"};\t);
      }
    }else{
      #子記事
      for($CF{'chditm'}=~m/\+([a-z\d]+)\b/go){
        $log[$IN{'j'}].=qq($_=\t$IN{"$_"};\t);
      }
    }
    $log[$IN{'j'}].="\n";
    
    truncate(RW,0);
    seek(RW,0,0);
    print RW join('',@log);
    close(RW);
  }else{
    #-----------------------------
    #Something Wicked happened!
    &header;
    print<<'_HTML_';
<h2 class="mode">Something Wicked happened!</h2>
<pre>何か邪悪なことが起きました
掲示板に未知のバグが存在するか、
設置に問題があるか、
不正な投稿である可能性があります。
管理人にこのエラーが発生したことを伝えてください。
ErrorCode:"WriteSwitch'ELSE'"
_HTML_
    for(keys%IN){
      print"$_\t$IN{$_}\n";
    }
    print'</pre>';
    &footer;
  }
  close(ZERO); #ここでやっと書き込み終了

  #-----------------------------
  #書き込み成功＆「自由に修正をどうぞ」
  &header;
  print<<"_HTML_";
<h2 class="mode">- 書き込み完了 -</h2>
<p style="margin:0.6em">以下の内容で第$IN{'i'}番スレッドの$IN{'j'}番目に書き込みました。<br>
これでよければそのままTOPや掲示板に戻ってください。<br>
修正したい場合は以下のフォームで修正して投稿してください。</p>
<table summary="BackMenu" width="300"><tr>
<colgroup span="2" width="150">
<td><form action="$CF{'index'}" method="get">
<input type="submit" class="button" accesskey="b" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="掲示板に戻る(B)">
</form></td>
<td><form action="$CF{'home'}" method="get">
<input type="submit" class="button" accesskey="h" onFocus="this.className='buttonover'" onBlur="this.className='button'" onMouseOver="this.className='buttonover'" onMouseOut="this.className='button'" value="$CF{'name'}に戻る(H)">
</form></td>
</tr></table>
_HTML_
  &rvsij(\%IN);
  &footer;

  exit;
}


#-------------------------------------------------
# 記事修正・削除メニュー
#
sub rvsmenu{
  &getck;
  &header;
  my$mode='';
  if(defined$IN{'rvs'}){$mode='rvs';print qq[<h2 class="mode">- 記事編集モード -</h2>\n];}
  elsif(defined$IN{'del'}){$mode='del';print qq[<h2 class="mode">- 記事削除モード -</h2>\n];}
  else{print qq[<h2 class="mode">Something Wicked happend!</h2>];&footer;}
  ($_[0])&&(print"<p>$_[0]</p>\n");

  &logfiles('number');
  my$max=int(($#file-1)/$CF{'delpg'})+1;
  ($max<$IN{'page'})&&($IN{'page'}=$max);
  my@i=@file;
  @i=splice(@i,($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});

  my$pgslct=&pgslct($max,"$mode");
  print<<"_HTML_";
$pgslct

<form id="List" method="post" action="$CF{'index'}">
<table cellspacing="0" class="list" summary="List" width="550">
<col width="50">
<col width="170">
<col width="330">
<tr><td colspan="2"><span class="ak">P</span>assword: <input name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
</td>
<td>
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">　
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="キャンセル">
</td></tr>
_HTML_

  for(@i){
    my$i=$_;
    my$j=-1;
    (-e"$CF{'log'}$i.cgi")||(next);
    ($i)||(next);
    sysopen(RD,"$CF{'log'}$i.cgi",O_RDONLY)||die"Can't open log$i!";
    flock(RD,LOCK_SH);
    print'<tr><td colspan="6"><hr></td></tr>';
    my$count="<a href=\"$CF{'index'}?read=$i#$i\">第$i号</a>";
    while(<RD>){
      $j++;
      ($_=~/^Mir1=\tdel;\t/o)&&(next);
      my%DT=($_=~m/([^\t]*)=\t([^\t]*);\t/go);
      ($j)&&($count="Res $j");
      my$No="$i-$j";
      my$date=&date($DT{'time'});
      $DT{'body'}=($DT{'body'}=~/(.*)<br>/o)?$1:'';
      $DT{'body'}=~s/<[^>]*>//go;
      my$i=substr($DT{'body'},0,100);
      if($i=~/\x8F$/o){
        chop$i;
      }elsif($i=~tr/\x8E\xA1-\xFE//%2){
       $i.=substr($DT{'body'},100,1);
      }
      $DT{'body'}=$i;
      print<<"_HTML_";
<tr>
<td align="right">$count</td>
<td align="left">$DT{'titke'}</td>
<td align="right">by $DT{'name'}</td>
</tr>
<tr>
<td><input type="radio" name="$mode" value="$No"></td>
<td align="right">$date</td>
<td align="right">$DT{'body'}</td>
</tr>
_HTML_
    }
    close(RD);
  }
  print"</table></form>\n";

  print"$pgslct";
  &footer;

  exit;
}


#-------------------------------------------------
# 記事を修正
#

#たとえ$IN{'pass'}が渡されなくても、GetCookieでCookieを参照し、
#もしそこで得られた$CK{'pass'}がパスワードと一致すれば修正モードに通す、
#というようにして利便性の向上を図っている。
#当然パスワードが一致しなければ入力するように要請する。
sub revise{
  ($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});

  sysopen(RD,"$CF{'log'}$IN{'i'}.cgi",O_RDONLY)||die"Can't open log$IN{'i'}!";
  flock(RD,LOCK_SH);
  my@log=<RD>;
  close(RD);
    my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

  if($IN{'pass'}){
    #INで送られてきた？
    if(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
      #合っていれば処理へ
    }elsif($CF{'maspas'}&&($IN{'pass'}eq$CF{'maspas'})){
      #Revise Main Routin
      &header;
      print qq[<h2 class="mode">- 第$IN{'i'}番の$IN{'j'}の修正モード -</h2>\n];
      $DT{'i'}="$IN{'i'}";
      $DT{'j'}="$IN{'j'}";
      $DT{'pass'}='';
      $DT{'oldps'}="$IN{'pass'}";
      &rvsij(\%DT);
      &footer;
      exit;
    }else{
      &rvsmenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。");
    }
  }else{
    #Cookieにある？
    &getck;
    $IN{'pass'}=$CK{'pass'};

    #-----------------------------
    unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
      #無いなら入力して
      &header;
      print<<"_HTML_";
<h2 class="mode">- 第$IN{'i'}番の$IN{'j'}のパスワード認証 -</h2>
<form accept-charset="euc-jp" id="Revise" method="post" action="$CF{'index'}">
<table cellspacing="2" summary="Revise" width="550">
<col width="50">
<col width="170">
<col width="330">
<p style="margin:0.6em">パスワードを入力してください</p>
<p style="margin:0.6em"><span class="ak">P</span>assword:
<input name="pass" type="password" accesskey="p" size="12" style="ime-mode:disabled" value="$CK{'pass'}">
<input type="hidden" name="rvs" value="$IN{'rvs'}"></p>
<p style="margin:0.6em">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">　
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="キャンセル">
</p>
_HTML_
      &footer;
      exit;
    }
  }
  #Revise Main Routin
  &header;
  print qq[<h2 class="mode">- 第$IN{'i'}番の$IN{'j'}の修正モード -</h2>\n];
  $DT{'i'}="$IN{'i'}";
  $DT{'j'}="$IN{'j'}";
  $DT{'pass'}="$IN{'pass'}";
  $DT{'oldps'}="$IN{'pass'}";
  &rvsij(\%DT);
  &footer;

  exit;
}


#-------------------------------------------------
# 記事削除

sub delete{
  ($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});

  sysopen(RD,"$CF{'log'}$IN{'i'}.cgi",O_RDONLY)||die"Can't open log$IN{'i'}!";
  flock(RD,LOCK_SH);
  my@log=<RD>;
  close(RD);
  my%DT=($log[$IN{'j'}]=~m/([^\t]*)=\t([^\t]*);\t/go);

  SWITCH:{
    if($CF{'maspas'}&&($IN{'pass'}eq$CF{'maspas'})){
      if(($IN{'j'}eq'0')&&(!$IN{'type'})){
        #無いなら入力して
        &header;
        print<<"_HTML_";
<h2 class="mode">- 第$IN{'i'}番スレッドの削除 -</h2>
<form accept-charset="euc-jp" id="Delete" method="post" action="$CF{'index'}">
<fieldset style="padding:0.5em;width:60%">
<legend>スレッドの削除方法を選んでください</legend>
_HTML_
        my$i=<<"_HTML_";
<td>
<label for="mark">親記事の本文のみ削除<input id="mark" name="del" type="radio" value="$IN{'del'}-1"></label>
<label for="$CF{'del'}">記事スレッドを削除<input id="$CF{'del'}" name="del" type="radio" value="$IN{'del'}-2"></label>
_HTML_
        $i=~s/(id=\"$CF{'del'}\")/$1 checked="checked"/o;
        print<<"_HTML_";
$i
</fieldset>

<p style="margin:0.6em">
<input name="pass" type="hidden"  value="$IN{'pass'}">
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">　
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="キャンセル">
</p>
_HTML_
        &footer;
        exit;
      }
      (($IN{'j'}eq'0')&&($IN{'type'}==2))&&(last SWITCH);
    }else{
      (&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'}))
       ||(&rvsmenu("入力されたパスワードが第$IN{'i'}番の$IN{'j'}のものと合致しません。"));
      (($IN{'j'}eq'0')&&($#log==0))&&(last SWITCH);
    }
    
    #mark
    $log[$IN{'j'}]=~s/^Mir1=\t([^\t]*);\t/Mir1=\tdel;\t/go;
    my$data=join('',@log);
    
    sysopen(WR,"$CF{'log'}$IN{'i'}.cgi",O_WRONLY|O_TRUNC)||die"Can't write log$IN{'i'}!";
    flock(WR,LOCK_EX);
    print WR $data;
    close(WR);
    &rvsmenu("第$IN{'i'}番の$IN{'j'}を削除しました。('mark')");
  }
  #親記事削除
  if($CF{'del'}eq'unlink'){
    #削除
    unlink"$CF{'log'}$IN{'i'}.cgi"||die"Can't delete log$IN{'i'}!";
    &rvsmenu("第$IN{'i'}番スレッドを削除しました。('unlink')");
  }elsif($CF{'del'}eq'rename'){
    #ファイル名変更
    rename("$CF{'log'}$IN{'i'}.cgi","$CF{'log'}$IN{'i'}.cgi.bak")||die"Can't rename log$IN{'i'}!";
    &rvsmenu("第$IN{'i'}番スレッドを削除しました。('rename')");
  }
  exit;
}


#-------------------------------------------------
# 全文検索機能
#

#まだAND,OR検索のような高度な機能は実装していない
#ちなみに「全文」というのは偽りでなく、文字通り「全文字列」である
#index関数を使うことにより高速化を図っている、、つもり。
sub seek{
  &header;
  print qq[<h2 class="mode">- 検索モード -</h2>];
  if(length$IN{'seek'}){
    #-----------------------------
    #検索結果表示
    my$j='';
    &logfiles('number');
    for(@file){
      ($_)||(last);
      sysopen(RD,"$CF{'log'}$_.cgi",O_RDONLY)||die"Can't open log$_!";
      flock(RD,LOCK_SH);
      my$log=join('',<RD>);
      close(RD);
      (index($log,$IN{'seek'})>-1)&&($j.=qq{<a href="$CF{'index'}?read=$_#$_">No.$_</a>\n});
    }
    print"<p>「$IN{'seek'}」で検索した結果、<br>";
    if($j){print"以下のスレッドで検索単語を発見しました♪</p>$j";
    }else{print'<p>検索単語は発見できませんでした</p>';}
  }
  print<<"_HTML_";
<form accept-charset="euc-jp" id="seek" method="post" action="$CF{'index'}">
<p>検索する単語(<span class="ak">W</span>)
<input type="text" name="seek" id="seek" class="blur" accesskey="w" style="ime-mode:active;width:200px;" onFocus="this.className='focus'" onBlur="this.className='blur'" value="$IN{'seek'}">
</p>
<p>
<input type="submit" class="submit" accesskey="s" onFocus="this.className='submitover'" onBlur="this.className='submit'" onMouseOver="this.className='submitover'" onMouseOut="this.className='submit'" value="OK">　
<input type="reset" class="reset" onFocus="this.className='resetover'" onBlur="this.className='reset'" onMouseOver="this.className='resetover'" onMouseOut="this.className='reset'" value="キャンセル">
</p>
</form>
<h2 class="mode">注意</h2>
<pre style="text-align:center">
この検索システムは労力軽減のため、
現在全ての項目に対し一括して判定を行っています。
よって名前にヒットしたのか、コメントにヒットしたのかは現在わかりません。

また、その単語がスレッド内のどこに出てきたかは考えていません。
ブラウザのページ内検索機能などを使ってください^^;;
</pre>
_HTML_
  &footer;

  exit;
}


#------------------------------------------------------------------------------#
# HTTP,HTML,Pageヘッダーをまとめて出力する
#
sub header{
  print<<"_HTML_";
Content-type: text/html; charset=euc-jp
Content-Language: ja
_HTML_

#GZIP圧縮転送もかけられるときはかける
#CSS非対応のIE3以下やNN4は外部CSSを読み込ませない
  #GZIP Switch
  if((-x$CF{'gzip'})&&($ENV{'HTTP_ACCEPT_ENCODING'}=~/gzip/io)){
    print"Content-encoding: gzip\n\n";
    open(STDOUT,"| $CF{'gzip'} -1 -c")||die"Can't use GZIP!";
    print"<!-- gzip enable -->\n";
  }else{print"\n<!-- gzip disable -->\n";}

  print<<'_HTML_';
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="ja">
<head>
<meta http-equiv="Content-type" content="text/html; charset=euc-jp">
<meta http-equiv="Content-Script-Type" content="text/javascript">
<meta http-equiv="Content-Style-Type" content="text/css">
_HTML_
  #CSS Switch
  CSS:{
    if($ENV{'HTTP_USER_AGENT'}=~m/MSIE 3/o){
      #IE3はNG
      last CSS;
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4.*compatible}o){
      #Mozilla/4互換は通す
    }elsif($ENV{'HTTP_USER_AGENT'}=~m{Mozilla/4}o){
      #Netscape4はダメ
      last CSS;
    }
    #それ以外には一応渡しておく
    print qq{<link rel="stylesheet" type="text/css" href="$CF{'style'}" media="screen" title="DefaultStyle">\n};
  }
  #LastPost
  unless(%Z0){
    sysopen(ZERO,"$CF{'log'}0.cgi",O_RDONLY)||die"Can't write log0!";
    flock(ZERO,LOCK_SH);
    my@zero=<ZERO>;
    close(ZERO);
    ($zero[0]=~/^Mir1=\t/o)||(die"ログ形式がMir1型以外です");
    %Z0=($zero[0]=~m/([^\t]*)=\t([^\t]*);\t/go);
    @zer2=split(/ /,$zero[2]);
  }
  my$date=&date($Z0{'time'});
  print<<"_HTML_";
<link rel="start" href="$CF{'home'}">
<link rel="index" href="$CF{'index'}">
<link rel="help" href="$CF{'help'}">
<title>$CF{'title'}</title>
</head>
<body>
<p class="lastpost">
<a href="index.cgi?read=$Z0{'Mir1'}#$Z0{'Mir1'}">Lastpost: $date $Z0{'name'}</a></p>
$CF{'head'}
$CF{'menu'}
_HTML_
#  eval qq{print<<"_HTML_";\n$CF{'menu'}\n_HTML_};
}


#-------------------------------------------------
# 記事編集中継
#
sub rvsij{
  my%DT=%{shift()};
  while(my$key=shift()){$DT{$key}=shift();}

  #データを戻す
  $DT{'body'}=~s/<br>/\n/go;#"<br>"2"\n"
  $DT{'body'}=~s/<\/?a[^>]*>//go;#ClearAnchors
  $DT{'body'}=~s/</&#60;/go;
  $DT{'body'}=~s/>/&#62;/go;

  if($DT{'j'}){
    #子記事
    &chdfrm(\%DT);
  }else{
    #親記事
    &prtfrm(\%DT);
  }
}


#-------------------------------------------------
# 記事返信
#
sub res{
  &getck;
  &header;

  print qq[<h2 class="mode">- Response Mode -</h2>\n];
  (&article('i'=>$IN{'i'},'ak'=>1,'res'=>1)eq'del')&&(print"This thread$IN{'i'} is deleted.");

  &chdfrm(\%CK,'i'=>$IN{'i'},'ak'=>1);
  &footer;
  exit;
}


#-------------------------------------------------
# 記事表示
#

#このサブルーチン一回で1スレッドを出力する
#RESフォームを付属させるかは設定次第、、
#のはずだったが、アイコンリストの肥大化に伴ない、
#JavaScriptによる打開策確定まで停止中。。
sub article{
  #このスレッド共通の情報
  my%DT=@_;
  my$new=0;
  $DT{'j'}=-1;
  
  sysopen(RD,"$CF{'log'}$DT{'i'}.cgi",O_RDONLY)||die"Can't open log$DT{'i'}!";
  flock(RD,LOCK_SH);
  while(<RD>){
    $DT{'j'}++;
    if($DT{'j'}eq'0'){
      #親記事
      &artprt(\%DT);
    }else{
      #子記事
      ($_=~/^Mir1=\tdel;\t/o)&&(next);#削除記事除外
      &artchd(\%DT);
    }
  }
  close(RD);
  ($DT{'j'}<0)&&(return);
  #記事フッタ
  &artfot(\%DT);
  return$new;#未読記事の件数を返す
}


#-------------------------------------------------
# ページ選択TABLE
#
sub pgslct{
  my$i=$IN{'page'}-1;
  my$j=$IN{'page'}+1;
  my$k='';
  my@page=();
  my@key=('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9ページのAccessKey
  ($_[1])&&($k=";$_[1]");

  #page表示調節
  my$per=20;
  my$hal=int($per/2);
  my$str=0;
  my$end=0;

  #どこからどこまで
  if($_[0]<=$per){
    $str=1;
    $end=$_[0];
  }elsif($IN{'page'}-$hal<1){
    #1-10
    $str=1;
    $end=$per;
    ($end>$_[0])&&($end=$_[0]);
  }elsif($IN{'page'}+$hal>=$_[0]){
    #(max-10)-max
    $str=$_[0]-$per+1;
    $end=$_[0];
  }else{
    $str=$IN{'page'}-$hal+1;
    $end=$IN{'page'}+$hal;
  }

  #配列へ
  for($str..$end){
    ($_==$IN{'page'})&&(push(@page,qq(<strong class="pgsl">$_</strong>)),next);
    if($key[$_]){
      push(@page,qq(<a accesskey="$key[$_]" href="$CF{'index'}?page=$_$k">$_</a>));
    }else{
      push(@page,qq(<a href="$CF{'index'}?page=$_$k">$_</a>));
    }
  }

  #最初と最後
  ($str!=1)&&(unshift(@page,qq(<a accesskey="&#60;" href="$CF{'index'}?page=1$k">1</a>&lt;&lt;)));
  ($end!=$_[0])&&(push(@page,qq(&gt;&gt;<a accesskey="&#62;" href="$CF{'index'}?page=$_[0]$k">$_[0]</a>)));

  #ひとつ前後
  $i=($IN{'page'}==1)?'[最新]':qq[<a accesskey="," href="$CF{'index'}?page=$i$k">&#60; 後の</a>];
  $j=($_[0]-$IN{'page'})?qq[<a accesskey="." href="$CF{'index'}?page=$j$k">昔の &#62;</a>]:'[最古]';

  #いざ出力
  return<<"_HTML_";
<table cellspacing="0" class="pgsl" summary="PageSelect">
<col style="width:3.5em">
<col>
<col style="width:3.5em">
<tr><td>$i</td>
<td>[ @page ]</td>
<td>$j</td>
</tr>
</table>
_HTML_
}


#-------------------------------------------------
# Locationで転送
#
sub locate{
  my$i;
  if($_[0]=~/^http:/o){
    $i=$_[0];
  }elsif($_[0]=~/\?/o){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=sprintf('%s?%s',$_[0]);
  }elsif($_[0]){
    $i=sprintf('http://%s%s/',$ENV{'SERVER_NAME'},
    substr($ENV{'SCRIPT_NAME'},0,rindex($ENV{'SCRIPT_NAME'},'/')));
    $i.=$_[0];
  }
  print<<"_HTML_";
Location: $i
Content-Type: text/html
Pragma: no-cache
Cache-Control: no-cache

<!DOCTYPE html PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html>
<head>
<meta http-equiv="Refresh" content="0;URL=$i">
<title>301 Moved Permanently</title>
</head>
<body>
<h1>: Mireille :</h1>
<p>And, please go <a href="$i">here</A>.</p>
<p>Location: $i</p>
<p>Mireille <var>$CF{'corver'}</var>.<br>
Copyright &#169;2001 <a href="http://airemix.site.ne.jp/" target="_blank" title="Airemix">Airemix</a>. All rights reserved.</p>
</body>
</html>
_HTML_
  exit;
}

#------------------------------------------------------------------------------#
# Sub Routins
#

#-------------------------------------------------
# Form内容取得
#

#MethodがHEADならばLastModifedを出力して、
#最後の投稿時刻を知らせる
sub getfm{
  my$i='';
  my%DT;
  if($ENV{'REQUEST_METHOD'}eq'HEAD'){ #forWWWD
    my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'last');
    print"Last-Modified: $last\n";
    print"Content-Type: text/plain\n\n";
    exit;
  }elsif($ENV{'REQUEST_METHOD'}eq'POST'){
    read(STDIN,$i,$ENV{'CONTENT_LENGTH'});
  }elsif($ENV{'REQUEST_METHOD'}eq'GET'){
    $i=$ENV{'QUERY_STRING'};
  }

  if(length$i>262114){
    #サイズ制限
    &header;
    print"いくらなんでも量が多すぎます\n$i";
    &footer;
    exit;
  }elsif(length$i>0){
    # EUC-JP文字
#   $ascii='[\x00-\x7F]'; # 1バイト EUC-JP文字
    my$ascii='[\x09\x0A\x0D\x20-\x7E]'; # 1バイト EUC-JP文字改
    my$twoBytes='(?:[\x8E\xA1-\xFE][\xA1-\xFE])'; # 2バイト EUC-JP文字
    my$threeBytes='(?:\x8F[\xA1-\xFE][\xA1-\xFE])'; # 3バイト EUC-JP文字
    my$character="(?:$ascii|$twoBytes|$threeBytes)"; # EUC-JP文字
    
    #入力を展開してハッシュに入れる
    for(split(/[&;]/o,$i)){
      my($i,$j)=split('=',$_,2);
      (defined$j)||($DT{$i}='',next);
      study$j;
      $j=~tr/+/\ /;
      $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
      $j=($j=~m/($character*)/o)?"$1":'';
      $j=~s/\t/\ \ /go;
      $j=~s/"/&#34;/go;
      $j=~s/&(#?\w+;)?/($1)?"&$1":'&#38;'/ego;
      $j=~s/'/&#39;/go;
  
      if($CF{'tags'}&&('body'eq$i)){
        #本文のみタグを使ってもいい設定にもできる
        my$tags=$CF{'tags'};
        $j=~s/</&#60;\t/go;
        $j=~s/>/&#62;\t/go;
        $j=~s{&#60;\t(/?)(\w+)([^\t]*)&#62;\t}
         {my($a,$b,$c)=($1,$2,$3);($tags=~m/\b$2\b/io)?"<$a$b>":"&#60;$a$b$c&#62;"}ego;
        $j=~tr/\00\t//d;
      }else{
        $j=~s/</&#60;/go;
        $j=~s/>/&#62;/go;
      }
  
      $j=~s/\x0D\x0A/<br>/go;$j=~s/\x0D/<br>/go;$j=~s/\x0A/<br>/go;
      $j=~s/(<br>)+$//o;
      $DT{$i}=$j;
    }
  }

  #外部入力の汚染除去
  if(defined$DT{'body'}){#記事書き込み
    #HTTP URL 正規表現
    my$http_URL_regex =
   q{\b(?:https?|shttp)://(?:(?:[-_.!~*'()a-zA-Z0-9;:&=+$,]|%[0-9A-Fa-f}.
   q{][0-9A-Fa-f])*@)?(?:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)}.
   q{*[a-zA-Z](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.}.
   q{[0-9]+)(?::[0-9]*)?(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f]}.
   q{[0-9A-Fa-f])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-}.
   q{Fa-f])*)*(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f}.
   q{])*(?:;(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*)}.
   q{*)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])}.
   q{*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*}.
   q{)?};
    #FTP URL 正規表現
    my$ftp_URL_regex =
   q{\bftp://(?:(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*} .
   q{(?::(?:[-_.!~*'()a-zA-Z0-9;&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)?@)?(?} .
   q{:(?:[a-zA-Z0-9](?:[-a-zA-Z0-9]*[a-zA-Z0-9])?\.)*[a-zA-Z](?:[-a-zA-} .
   q{Z0-9]*[a-zA-Z0-9])?\.?|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(?::[0-9]*)?} .
   q{(?:/(?:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*(?:/(?} .
   q{:[-_.!~*'()a-zA-Z0-9:@&=+$,]|%[0-9A-Fa-f][0-9A-Fa-f])*)*(?:;type=[} .
   q{AIDaid])?)?(?:\?(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9} .
   q{A-Fa-f])*)?(?:#(?:[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]|%[0-9A-Fa-f][0-9A} .
   q{-Fa-f])*)?};
    #MAIL 正規表現
    my$mail_regex=
   q{(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\}
   .q{\[\]\000-\037\x80-\xff])|"[^\\\\\x80-\xff\n\015"]*(?:\\\\[^\x80-\xff][}
   .q{^\\\\\x80-\xff\n\015"]*)*")(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x}
   .q{80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff])|"[^\\\\\x80-}
   .q{\xff\n\015"]*(?:\\\\[^\x80-\xff][^\\\\\x80-\xff\n\015"]*)*"))*@(?:[^(}
   .q{\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,;:".\\\\\[\]\0}
   .q{00-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[^\x80-\xff])*}
   .q{\])(?:\.(?:[^(\040)<>@,;:".\\\\\[\]\000-\037\x80-\xff]+(?![^(\040)<>@,}
   .q{;:".\\\\\[\]\000-\037\x80-\xff])|\[(?:[^\\\\\x80-\xff\n\015\[\]]|\\\\[}
   .q{^\x80-\xff])*\]))*};

    #必須
    $DT{'body'}=~s{($http_URL_regex|$ftp_URL_regex|($mail_regex))}
    {my($org,$mail)=($1,$2);(my$tmp=$org)=~s/"/&#34;/go;
    '<a class="user" href="'.($mail ne''?'mailto:':'')."$tmp\" target=\"_blank\">$org</a>"}ego;
    $IN{'body'}=($DT{'body'}=~/(.+)/o)?"$1":'';
    $IN{'name'}=($DT{'name'}=~/(.{1,100})/o)?"$1":'';
    $IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
    if($DT{'pass'}eq$CF{'maspas'}){
      $IN{'pass'}=$CF{'maspas'};
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    if($DT{'oldps'}eq$CF{'maspas'}){
      $IN{'oldps'}=$CF{'maspas'};
    }else{
      $IN{'oldps'}=($DT{'oldps'}=~/(.{1,24})/o)?"$1":'';
    }
    (($DT{'i'}=~/(\d+)/o)&&$1)&&($IN{'i'}=$1);
    ($DT{'j'}=~/(\d+)/o)&&($IN{'j'}=$1);

    if($IN{'j'}eq'0'){
      #親記事
      for($CF{'prtitm'}=~m/\b([a-z\d]+)\b/go){
        if('color'eq$_){
          $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
        }elsif('email'eq$_){
          $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
          $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
        }elsif('home'eq$_){
          $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
          $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
        }elsif('icon'eq$_){
          $IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
        }elsif('cmd'eq$_){
          ($DT{'cmd'}=~/(.+)/o)&&($IN{'cmd'}="$1");
        }elsif(('ra'eq$_)||('hua'eq$_)){
          next;
        }else{
          $IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
        }
      }
      
    }elsif($IN{'i'}){
      #子記事
      for($CF{'chditm'}=~m/\b([a-z\d]+)\b/go){
        if('color'eq$_){
          $IN{'color'}=($DT{'color'}=~/([\#\w\(\)\,]{1,20})/o)?"$1":'';
        }elsif('email'eq$_){
          $DT{'email'}=($DT{'email'}=~/(.{1,200})/o)?"$1":'';
          $IN{'email'}=($DT{'email'}=~/($mail_regex)/o)?"$1":'';
        }elsif('home'eq$_){
          $DT{'home'}=($DT{'home'}=~/(.{1,200})/o)?"$1":'';
          $IN{'home'}=($DT{'home'}=~/($http_URL_regex)/o)?"$1":'';
        }elsif('icon'eq$_){
          $IN{'icon'}=($DT{'icon'}=~/([\w\.\~\-\%\/]+)/o)?"$1":'';
        }elsif('cmd'eq$_){
          ($DT{'cmd'}=~/(.+)/o)&&($IN{'cmd'}="$1");
        }elsif(('ra'eq$_)||('hua'eq$_)){
          next;
        }else{
          $IN{"$_"}=($DT{"$_"}=~/(.+)/o)?"$1":'';
        }
      }
    }else{
      die"Something Wicked happened!";
    }
  }elsif($DT{'i'}){
  #返信
    $IN{'i'}=($DT{'i'}=~/(\d+)/o)?$1:undef;
  }elsif(defined$DT{'j'}){
  #新規書き込み
    $IN{'j'}=($DT{'j'}=~/(\d+)/o)?$1:0;
  }elsif(defined$DT{'seek'}){
  #検索
    $IN{'seek'}=($DT{'seek'}=~/(.+)/o)?"$1":'';
  }elsif(defined$DT{'del'}){
  #記事削除リストor実行
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
    if($DT{'pass'}eq$CF{'maspas'}){
      $IN{'pass'}=$CF{'maspas'};
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    $IN{'del'}=($DT{'del'}=~/(\d+\-\d+(-\d)?)/o)?"$1":'';
  }elsif(defined$DT{'rvs'}){
  #記事修正リストor実行
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
    if("$DT{'pass'}"eq"$CF{'maspas'}"){
      $IN{'pass'}="$CF{'maspas'}";
    }else{
      $IN{'pass'}=($DT{'pass'}=~/(.{1,24})/o)?"$1":'';
    }
    $IN{'rvs'}=($DT{'rvs'}=~/(\d+\-\d+)/o)?"$1":'';
  }elsif(defined$DT{'help'}){
  #説明
    return($IN{'help'}=1);
  }elsif(defined$DT{'home'}){
  #ホーム
    return($IN{'home'}=1);
  }elsif(defined$DT{'new'}){
  #新規書き込み
    $IN{'j'}=0;
  }elsif(defined$DT{'res'}){
  #返信書き込み
    (($DT{'res'}=~/(\d+)/o)&&$1)&&($IN{'i'}=$1);
  }elsif(defined$DT{'compact'}){
    #携帯端末モード
    require './compact.cgi';
  }elsif($DT{'read'}){
  #ログ読み
      (($DT{'read'}=~/(\d+)/o)&&$1)&&($IN{'read'}=$1);
  }else{
  #ページ
    $IN{'page'}=(($DT{'page'}=~/(\d+)/o)&&$1)?$1:1;
  }
  $IN{'ra'}=($ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?"$1":'';
  $IN{'hua'}=($ENV{'HTTP_USER_AGENT'}=~/([^\t]+)/o)?"$1":'';
  return%IN;
}

#-------------------------------------------------
# Cookieを取得する
#
sub getck{
  ($ENV{'HTTP_COOKIE'}=~/(.+)/o)||(return undef);
  my$cookie="$1";
  for(split('; ',$cookie)){
    my($i,$j)=split('=',$_,2);
    ('Mireille'ne$i)&&(next);
    $j=~s/%([0-9A-Fa-f]{2})/pack('H2',$1)/ego;
    %CK=split("\t",$j);
    last;
  }
  return%CK;
}

#-------------------------------------------------
# Cookie書き込み
#
sub wrtcook{
  my%DT=%{shift()};
  for(keys%CK){
    (length$DT{"$_"})||($DT{"$_"}=$CK{"$_"});
  }
  my$cook='';
  my$time=0;
  my$expire=0;
  if($CK{'expire'}>$^T){
    #期限内
    $time=$CK{'time'};
    $expire=$CK{'expire'};
  }elsif($CK{'expire'}>0){
    #期限切れ
    $time=$CK{'expire'}-$CF{'newuc'};
    $expire=$^T+$CF{'newuc'};
    $CK{'time'}=$time;
  }else{
    #新規
    $time=$^T;
    $expire=$^T+$CF{'newuc'};
    $CK{'time'}=$^T-$CF{'newnc'};
  }
    $cook="name\t$DT{'name'}\tpass\t$DT{'pass'}\ttime\t$time\texpire\t$expire";
  for($CF{'cokitm'}=~m/\b([a-z\d]+)\b/go){
    $cook.=qq(\t$_\t$DT{$_});
  }
  $cook=~s{(\W)}{'%'.unpack('H2',$1)}ego;
  my$gmt=&datef(($^T+20000000),'gmt');
  print"Set-Cookie: Mireille=$cook; expires=$gmt\n";
}

#-------------------------------------------------
# フォーマットされた日付取得を返す
sub datef{
  unless($_[1]){
  }elsif($_[1]eq'gmt'){
   # Cookie用
    return sprintf("%s, %02d-%s-%d %s GMT",(split/\s+/o,gmtime($_[0]))[0,2,1,4,3]);
  }elsif($_[1]eq'last'){
   # LastModified用
    return sprintf("%s, %02d %s %s %s GMT",(split/\s+/o,gmtime($_[0]))[0,2,1,4,3]);
  }
  return&date;
}

#-------------------------------------------------
# 記事スレッドファイルのリストを取得
#

#ログファイル名を取得し、
#その番号又は更新日時に基づいて並び替えて
#ファイル名番号のリストを返す
sub logfiles{
  undef@file;
  opendir(DIR,$CF{'log'});
  for(readdir(DIR)){
    (($_=~/^(\d+).cgi$/io)&&($1))&&(push(@file,"$1"));
  }
  closedir(DIR);
  
  if($_[0]eq'date'){
    #日付順 'date'
    @file=sort{$zer2[$b-$zer2[0]]<=>$zer2[$a-$zer2[0]] or $b<=>$a}@file;
  }else{
    #記事番号順 'number'
    @file=sort{$b<=>$a}@file;
  }
  push(@file,0);
  return@file;
}

#-------------------------------------------------
# パスワード暗号化
sub mircrypt{
  srand($_[0]);
  my$m='abcdefghijklmnopqrstuvwxyz.0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  my$n=substr($m,int(rand(64)),1);
  $n.=substr($m,int(rand(64)),1);
  my$pass='';
  for($_[1]=~m/(.{1,8})/go){
    (length$_)||(next);
    $_=crypt($_,$n);
    substr($_,0,2,'');
    $pass.=$_;
  }
  ($_[2])||(return$pass);
  $IN{'newps'}=$pass;
  ($IN{'newps'}eq$_[2])&&(return 1);#OK
  return undef;#NG
}


1;
__END__
