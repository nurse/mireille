#!/usr/local/bin/perl

#------------------------------------------------------------------------------#
# 'Mireille' Bulletin Board System
# - Mireille Core File -
#
# $Revision$
# "This file is written in euc-jp, CRLF." ��
# Scripted by NARUSE,Yui.
#------------------------------------------------------------------------------#
# $cvsid = q$Id$;
require 5.005;
#use strict;
#use vars qw(%CF %IC %IN %CK);
my(%Z0,@zer2,@file);

=head1 "Mireille" Bulletin Board System

=begin :comment

# core.cgi��ñ�ε�ư������ȡ�location��ķ�Ф���CGI��
# ���ε�ǽ��Ȥ��ˤϾ�ιԤ� # �� #=item �ȥ����ȥ����Ȥ��Ƥ�������
if($CF{'program'}eq __FILE__){
	#ľ�ܼ¹Ԥ��ä���ư���Ф�
	&locate($ENV{'QUERY_STRING'});
 }

=end :comment

=cut


#-------------------------------------------------
# MAIN SWITCH
#
sub main{
    #-----------------------------
    #Encoding Checker
    my$message='The encoding of "%s" is not "%s" but "%s"!';
    my%enc=(130=>'shift_jis',164=>'euc-jp',27 =>'iso-2022-jp',227=>'utf-8',48=>'utf-16be',66=>'utf-16le');
    for(keys%{$CF{'_HiraganaLetterA'}}){
	my$chr=ord$CF{'_HiraganaLetterA'}->{$_};
	if($enc{$chr}){
	    lc$CF{'encoding'}eq$enc{$chr}||die sprintf($message,$_,$CF{'encoding'},$enc{$chr});
#		}elsif($chr==12354){
	    #Perl Native�ʤΤϡ�����äƤ�Τ��狼��ʤ����饹�롼����
#		}else{
	    #̤�ΤΥ��󥳡��ǥ��󥰤Ϥ�äȤ狼��ʤ��Τ�̵�뤹��
	}
    }
	
    #-----------------------------
    #���ե���������Ȥ��롩
    defined$CF{'log'}||die q($CF{'log'} is Undefined);
    unless(-e"$CF{'log'}0.cgi"){
	-e"$CF{'log'}0.pl"&&die'�����0.pl���ĤäƤ��ޤ� �Զ���������';
	!-e"$CF{'log'}"&&!mkdir("$CF{'log'}",0777)&&die"Can't read/write/create LogDir($CF{'log'})[$?:$!]";
	open(ZERO,'+>>'."$CF{'log'}0.cgi")||die"Can't write log(0.cgi)[$?:$!]";
	eval{flock(ZERO,2)};
	if(!-s"$CF{'log'}0.cgi"){
	    print ZERO "Mir12=\t0-0;\tsubject=\tWelcome to Mireille;\tname=\tMireilleSystem;\ttime=\t$^T;\t"
		."body=\tLOG�ǥ��쥯�ȥ�ڤ�0.cgi������������֤���Ƥ��ʤ��ä��١����֤��ʤ����ޤ���<BR>"
		."���Υ�å�������ɽ������Ƥ����硢���Ǥ�Mireille�ˤ������˼�ư���֤���Ƥ��ޤ�<BR>"
		."�ʤ������Υ�å������Ͽ�����Ƥ�����ȡ���ưŪ�˾��Ǥ��ޤ�;\t";
	}
	close(ZERO);
    }

    #-----------------------------
    #�⡼�ɤ��Ȥο���ʬ��
    &getParam;
	
    if($CF{'readOnly'}&&$IN{'_isEditing'}){
	#�������ѥ⡼��
	&showUserError('���ߤ��ηǼ��Ĥϱ������ѥ⡼�ɤ����ꤵ��Ƥ��ޤ�');
    }else{
	#�����񤭹���
	defined$IN{'body'}&&&writeArticle;
	#�ֿ�
	$IN{'i'}&&&showResponseMode;
	#�����񤭹���
	defined$IN{'j'}&&(&showHeader,&getCookie,&prtfrm,(print&getFooter),exit);
	#���������ꥹ��or�¹�
	defined$IN{'rvs'}&&(index($IN{'rvs'},'-')+1?&rvsArticle:&showRvsMenu);
	#��������ꥹ��or�¹�
	defined$IN{'del'}&&(index($IN{'del'},'-')+1?&delArticle:&showRvsMenu);
    }
    #����
    defined$IN{'rss'}&&&rss;
    #����
    defined$IN{'seek'}&&&showArtSeek;
    #�إ��
    defined$IN{'help'}&&(require($CF{'help'}?$CF{'help'}:'help.pl'))&&exit;
    #��������
    defined$IN{'icct'}&&require($CF{'icct'}?$CF{'icct'}:'iconctlg.cgi')&&&iconctlg&&exit;
    #�ۡ���
    defined$IN{'home'}&&&locate($CF{'home'});
    #����ɽ��
    &showCover;
    exit;
}


#------------------------------------------------------------------------------#
# MAIN ROUTINS
#
# mainľ���Υ��֥롼����

#-------------------------------------------------
# ɽ��ɽ��
#
sub showCover{
    #-----------------------------
    #�Ƽ�������
    &getCookie;
    &logfiles($CF{'sort'});
    !@file&&$file[$#file-1]&&push(@file,0);
    %Z0||&getZeroInfo;
	
    #-----------------------------
    # Cookie�񤭹���
    &setCookie(\%CK);
	
    #-----------------------------
    #$IN{'page'}������
    unless($IN{'read'}){
	#ľ��page�����
	$IN{'page'}=1if$IN{'page'}>($#file-1)/$CF{'page'}+1;
    }elsif($IN{'read'}<$file[$#file-1]){
	#�Ť����뵭��
	$IN{'page'}=int(($#file-1)/$CF{'page'})+1;
    }elsif($file[0]<$IN{'read'}){
	#̤��ε���
    }else{
	#�����äݤ���������
	my$thread=$CF{'page'};
	for(@file){
	    if($_==$IN{'read'}){
		$IN{'page'}=int($thread/$CF{'page'});
		last;
	    }
	    ++$thread;
	}
    }
	
    #-----------------------------
    #��������
    my%NEW;
    my@view=map{$NEW{"$_"}=qq(<A href="$CF{'index'}?read=$_#art$_" class="new">$_</A>)}
    grep{$zer2[$_-$zer2[0]]>$CK{'time'}}grep{$_>$zer2[0]}@file;
	
    #-----------------------------
    #̤�ɵ����Τ��륹��å�
    my$unread='';
    if(@view){
	# 20 : ̤�ɵ����Τ��륹��åɤ��������ɽ�����륹��åɿ��ξ��
	$unread=sprintf'<P>̤�ɵ����Τ��륹��å�[ %s ]</P>',$#view>20?"@view[0..20] ..":"@view[0..$#view]";
    }
	
    #-----------------------------
    #���Υڡ����Υ���å�
    my$this='';
    @view=splice(@{[@file]},($IN{'page'}-1)*$CF{'page'},$CF{'page'});
    $#view&&!$view[$#view]&&pop@view;
    for(0..$#view){
	$this.=sprintf'<A href="#art%d" title="Alt+%d">%s</A> '
	    ,$view[$_],$_+1,(sprintf$NEW{"$view[$_]"}?'<SPAN class="new">%d</SPAN>':'%d',$view[$_]);
    }
	
    #-----------------------------
    #�ڡ�������TABLE�����
    my$pageSelector=&pageSelector($#file,$CF{'page'});
	
    #-----------------------------
    # HTTP,HTML,PAGE�إå�����ɽ��
    &showHeader;
	
    #-----------------------------
    #������ƥե������ɽ�����������ˤ���
    $CF{'prtwrt'}&&&prtfrm;
    print$CF{'note'};
    #�����ʥӥܥ���
    &artnavi('button');
	
    #-----------------------------
    #��������ɽ����
    print&getArticoleInfomationA(unread=>$unread,pageSelector=>$pageSelector,this=>$this);
	
    #-----------------------------
    #����ɽ��
    if(0 ne$view[0]){
	#���˲�ư��ΤȤ�
	#Threads Body
	my$unreads=1;
	for(0..$#view){
	    $unreads+=&showArticle(i=>$view[$_],ak=>($_+1)
				   ,-maxChildsShown=>$CF{'maxChildsShown'},-unreads=>$unreads);
	}
    }else{
	#log0�Τ� �Ĥޤ�����ľ��ΤȤ�
	&showArticle(i=>0,ak=>1);
    }
    #-----------------------------
    #��������ɽ����
    print&getArticoleInfomationB(unread=>$unread,pageSelector=>$pageSelector,view=>$#view,this=>$this);
	
    #-----------------------------
    #�����ʥ�
    &artnavi;
	
    #-----------------------------
    #�եå�
    print&getFooter;
    exit;
}


#-------------------------------------------------

=head2 �����񤭹���

=head3 �񤭹��ߤξ���

=over

=item ����

C<(length$IN{'j'}xor$IN{'i'})>

=item �����Ƶ���

C<(!defined$IN{'i'}&&$IN{'j'}eq 0)>

=item �����ҵ���

C<($IN{'i'}&&!defined$IN{'j'})>

=item ����

C<($IN{'i'}&&defined$IN{'j'})>

=item �����Ƶ���

C<($IN{'i'}&&$IN{'j'}eq 0)>

=item �����ҵ���

C<($IN{'i'}&&$IN{'j'}ne 0)>

=back

=cut

sub writeArticle{
    
    {
	open(ENV,'>>'."$CF{'log'}env.log")||die"Can't write log(0.cgi)[$?:$!]";
	flock(ENV,2);
	my $log = '';
	for(qw/REMOTE_ADDR REMOTE_HOST HTTP_USER_AGENT HTTP_CLIENT_IP HTTP_FORWARDED HTTP_SP_HOST HTTP_FORWARDED HTTP_X_FORWARDED_FOR HTTP_FROM HTTP_HOST HTTP_VIA HTTP_REFERER HTTP_X_LOCKING REQUEST_METHOD QUERY_STRING/){
	    $ENV{$_} or next;
	    $log .= qq{$_ => "$ENV{$_}", };
	}
	$log .= "\n";
	print ENV $log;
	close ENV;
    }

    'POST'eq$ENV{'REQUEST_METHOD'} or die 'wa: Something Wicked happend!';
    'Mozilla/4.0 (compatible; MSIE 4.01; Windows 95)'eq$ENV{'HTTP_USER_AGENT'} and die 'wa: Something Wicked happend!';
    $IN{'body'} =~ /^[\x21-\x7e]*$/o and die 'wa: Something Wicked happend!';
#    gethostbyaddr(pack('C4',split('\.',$ENV{'REMOTE_ADDR'})),2) or die 'wa: Something Wicked happend!';
    
    
    #-----------------------------
    #���ޥ�ɤ��ɤ߹���
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
    #����åɤΥ�å�
    if($EX{'lockThread'}&&$IN{'i'}){
	open(FILE,'+<'."$CF{'log'}$IN{'i'}.cgi")
	    ||die"Can't read/write log($IN{'i'};.cgi)[$?:$!]";
	eval{flock(FILE,2)};
	seek(FILE,0,0);
	my@log=map{/^([^\x0D\x0A]*)/o}<FILE>;
		
	my$isLocked=!index($log[$#log],"Mir12=\tLocked");
	my$lockedBy=$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*lockedBy=(\S+)[ ;]/o?$1:'';
		
	#���¤�����å�
	if($CF{'admps'}and$IN{'pass'}eq$CF{'admps'}||$IN{'oldps'}eq$CF{'admps'}){
	    $lockedBy='Admin';
	}elsif($isLocked&&'ThreadBuilder'ne$lockedBy){
	    die'���̥桼�����Ϥ��Υ���åɤΥ�å������Ǥ��ޤ���';
	}else{
	    #�Ƶ����Υѥ����
	    my%DT=$log[0]=~/([^\t]*)=\t([^\t]*);\t/go;
	    &mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})||die'���ʤ��Ϥ��Υ���åɤ��å��Ǥ��ޤ���';
	    $lockedBy='ThreadBuilder';
	}
		
	#��å����ץ����
	my$option='';
	my@options=('revise','delete');
	$EX{'lockThread'}=' '.lc($EX{'lockThread'}).' ';
	if(index($EX{'lockThread'},' all ')+1){
	    $option=join" ",@options;
	}else{
	    $option=join" ",grep{index($EX{'lockThread'}," $_ ")+1}@options;
	}
	$option.=" lockedBy=$lockedBy";
		
	#��å�
	if($isLocked){
	    #��å�����Ƥ�����ϲ����pop
	    index(pop@log,"Mir12=\tLocked")&&die'Mireille�Υ���åɥ�å���ǽ�˥Х�������ޤ���';
	}else{
	    #����Ƥ��ʤ����ϥ�å����뢪push
	    push(@log,"Mir12=\tLocked:$option;\t");
	}
	truncate(FILE,0);
	seek(FILE,0,0);
	print FILE map{"$_\n"}@log;
	close(FILE);
		
	#�����⡼�ɤ˰�ư
	$IN{'page'}=1;
	$IN{'rvs'}='';
	&showRvsMenu(sprintf"��$IN{'i'}�֥���åɤΥ�å�%s����",$isLocked?'���':'');
    }
	
    #-----------------------------
    #���ޥ�ɤν���

=head2 ���ޥ�ɤǻȤ�����

=head3 �����������

=over

=item ���ѥ�������

C<< icon = <password> >>

=item ���л��ꥢ������

C<< absoluteIcon = <absoluteUrl> >>

=item ���л��ꥢ������

C<< relativeIcon = <relativeUrl> >>
�����л���δ���$CF{'icon'}�Ǥ���

=back

=head3 ��������ꥹ�Ȥ��ɤ߹���

C<< iconlist = [ nolist | economy ] >>

=over

=item nolist

��������ꥹ�Ȥ��ɤ߹��ޤʤ���

=item economy

��������ꥹ�Ȥ��ɤ߹��ऱ��ɡ�ɽ�����ʤ���

=back


=head3 �ֽ�̾�Τ�ȡפ����

C<< signature = <seed of signature> >>

=head3 usetag

!SELECTABLE()�ǵ��Ĥ��Ƥ����ϰ���ǻȤ����������٤롣

=head3 notag

������Ȥ�ʤ���

=head3 noautolink

URI��ư��󥯤�Ȥ�ʤ���

=head3 noartno

�����ֹ��󥯤�Ȥ�ʤ���

=head3 nostrong

��綯Ĵ��Ȥ�ʤ���

=head3 ��������Ĵ��

=over

=item dnew

��������������򹹿����ޤ���

=item znew

����åɤκǽ��ѹ������򹹿����ޤ���

=item renew

dnew��znew��Ʊ���˹Ԥ��ޤ���

=back

=head3 lockArticle

�������å����ޤ���

=over

=item lockThread

C<< lockThread = [ all | revise | delete ] >>

����åɤ��å����ޤ���
�����ѥ���ɤ����Ƶ����Υѥ���ɤ�Ȥäơ�
��å�����������åɤ��ֿ�����ȥ�å��Ǥ��ޤ�
���ץ�������ꤷ�ʤ����ϡ����Υ���åɤ��Ф����ֿ�����å�����ޤ���

=item all

���ƤΥ��ץ����򥪥�

=item revise

�������å�

=item delete

������å�

=back

=head3 Note.

C<key=value;key=value>�η����ǥ��ޥ��������Ϥ���
key�ڤ�value��[=;]��ޤ�ǤϤʤ�ʤ�
��Q:���������url��[=;]���ޤޤ�뤳�ȤäƤ��롩��
��A:cgi����Ѥ��Ƥ���Ϥ��뤫��͡�����

C<key1="value1;value1";key2=value2;>
��Mireille1.2.2.16�Ǥϴ����̤�˲�ᤷ�Ƥ���ʤ��櫓�Ǥ���

1.2.2.16���ߤǤϤ����餯����Ŭ���ʽ����Ǥ⤤������ɡ�
�ܳ�Ū�˥��ޥ�ɤ�Ƚ�������ʤ�Marldia�Υ��ޥ�ɼ�����ä����٤���
�ޤ��������ʳ��˥��ޥ�ɤΥͥ����פ��Ĥ��ʤ��Τǡ�����^^;;

Marldia�ϥǡ������ݻ��ʤɤ�Ŭ���Ǥ⤤�����Ȥ⤢�äơ�
�빽�������ޥ�ɤ�Ĥ��Ƥ����ꤹ��Τǡ�
�嵭�Τ褦�ʤ�Τ�Ȥ�ɬ���������뤫�⤷��ʤ����ᡢ
ǰ�Τ����б������Ƥ���ΤǤ����ɤ͡�

=cut

    my@settings=qw(icon iconlist absoluteIcon relativeIcon signature);
    my@writeSettings=qw(usetag notag noautolink noartno nostrong);
    my@oneTimeCommands=qw(dnew znew renew lockArticle);
	
    defined$EX{$_}&&!$EX{$_}&&($EX{$_}=1)for@writeSettings,@oneTimeCommands;
    $IN{'cmd'}=join(';',(map{"$_=$EX{$_}"}grep{$EX{$_}}@settings),(grep{$EX{$_}}@writeSettings));
	
    #���ѥ�������ǽ��
    #���ꤷ����������ѥ���ɤ����פ���С�
    $IN{'icon'}=$IC{$EX{'icon'}}if$CF{'exicon'}&&$IC{$EX{'icon'}};
	
    #���л��ꥢ������
    $IN{'icon'}=''if$CF{'absoluteIcon'}&&$EX{'absoluteIcon'};
    #���л��ꥢ������
    $IN{'icon'}=$EX{'relativeIcon'}if$CF{'relativeIcon'}&&$EX{'relativeIcon'};
	
    #renew��dnew&&znew
    $EX{'dnew'}=$EX{'znew'}=1if$EX{'renew'};
	
    #-----------------------------
    #���顼ɽ��
    {
	my@error=();
	my@message=();
	$IN{'name'}||push(@error,'̾��');
	$IN{'body'}||push(@error,'��ʸ');
	$IN{'pass'}||($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'})
	    or push(@error,'�ѥ����')&&push(@message,'�ѥ���ɤ�8ʸ���ʾ塢128ʸ���ʲ��Ǥʤ���Фʤ�ޤ���');
	if($CF{'ngWords'}&&!@error){

=head2 CONFIG::NG���

  $CF{'ngWords'}='�С��� ������ �ɡ��� �ޤ̤���';
  $CF{'ngWordsItems'}='body=��ʸ subject=��̾ name=̾�� email=�᡼�륢�ɥ쥹 home ��ʬ��Web�����ȤΥ��ɥ쥹';
  $CF{'ngWordsMessage'}='NG��ɤ˰��ä����äƤ����';

=head3 ngWords

Ⱦ�ѥ��ڡ������ڤ�ǡ�NG��ɤ����

=head3 ngWordsItems

NG��ɤ��ޤޤ�뤫Ĵ�٤���ܡ�
������C<< <�ץ�����ι���̾>=<ɽ����ι���̾> >>�Ȥ��ä�����

=head3 ngWordsMessage

NG��ɤ򸫤Ĥ����Ȥ���ɽ�������å�����

=cut

	    my@ngWords=split(/\s+/o,$CF{'ngWords'});
	    my%item=($CF{'ngWordsItems'}||'body=��ʸ subject=��̾ name=̾��')=~/(\w+)=(\S+)/go;
	    for(keys%item){
		my$item=$IN{$_};
		my$err=$item{$_};
		study$item;
		for(@ngWords){
		    MirString->match($item,$_)||next;
		    push(@error,$err);
		    last;
		}
		@error&&last;
	    }
	    push(@message,$CF{'ngWordsMessage'}||'Ŭ�ڤǤʤ�ʸ�����ޤ���ƤʤΤǵ��䤵��ޤ�����')if@error;
	}
	if(@error){
	    &showHeader;
	    print<<"_HTML_";
<H2 class="heading2">- Write Error -</H2>
<P>@{[join('��',map{qq(<SPAN style="color:#f00">$_</SPAN>)}@error)]}����������Ϥ��Ƥ�������</P>
_HTML_
	    printf'<P>%s</P>',join'<BR>',@message if@message;
	    %CK=%IN;
	    &rvsij;
	    print&getFooter;
	    exit;
	}
    }
	
    #-----------------------------
    #��ʸ�ν���
    #form->data�Ѵ�
    unless(defined$IN{'body'}&&length$IN{'body'}){
	$IN{'body'}='';
    }elsif($CF{'tags'}&&'ALLALL'eq$CF{'tags'}){
	#ALLALL������OK��â����Ĵ��̵����URI��ư��󥯤�̵����
	#�����ǥ�󥯤�ĥ�ä��ꡢ��Ĵ���Ƥ����Τ���Ť˥�󥯡���Ĵ���Ƥ��ޤ��ޤ�����
    }else{
	#��ʸ�Τߥ�����ȤäƤ⤤������ˤ�Ǥ���
	my$attrdel=0;#°����ä�/�ä��ʤ�(1/0)
	my$str=$IN{'body'};
	study$str;
	$str=~tr/"'<>/\01-\04/;
	$str=~s/&(#?\w+;)/\05$1/go;
	
	#��������
	if($CF{'tags'}&&!$EX{'notag'}){
	    my$tag_regex_='[^\01-\04]*(?:\01[^\01]*\01[^\01-\04]*|\02[^\02]*\02[^\01-\04]*)*(?:\04|(?=\03)|$(?!\n))';
	    my$comment_tag_regex='\03!(?:--[^-]*-(?:[^-]+-)*?-(?:[^\04-]*(?:-[^\04-]+)*?)??)*(?:\04|$(?!\n)|--.*$)';
	    my$text_regex='[^\03]*';
			
	    my$tags=$CF{'tags'};
	    my%tagCom=map{/(!\w+)(?:\(([^()]+)\))?/o;$1," $2 "||''}($tags=~/!\w+(?:\([^()]+\))?/go);
	    if($tagCom{'!SELECTABLE'}){
		$tags.=' '.join(' ',grep{$tagCom{'!SELECTABLE'}=~/ $_ /o}grep{/\w+/}split(/\s+/,$EX{'usetag'}));
	    }elsif(defined$tagCom{'!SELECTABLE'}){
		$tags='\w+';
	    }
	    
	    my$result='';
	    #�⤷ BR������ A�����ʤ�����Υ��������Ϻ���������ʤ����ˤϡ� 
	    #$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
	    #$result .= $tag_tmp if $tag_tmp =~ /^<\/?(BR|A)(?![\dA-Za-z])/io;
	    my$remain=join('|',grep{/^(?:\\w\+|\w+)$/o}split(/\s+/o,$tags));
	    #�դ� FONT������ IMG�����ʤ�����Υ�������������������ˤϡ� 
	    #$tag_tmp = $2; �θ�ˡ����Τ褦�ˤ��� $tag_tmp �� $result �˲ä���褦�ˤ���ФǤ��ޤ��� 
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
	    #���ĥ���̵��orCommand:notag
	}
	
	#�����ֹ��󥯡�>>No.12-6��
	$str=~s{(\04\04No\.(\d+)(-\d+)?)}{<A class="autolink" href="$CF{'index'}?read=$2#art$2$3">$1</A>}go
	    if$CF{'noartno'}||!$EX{'noartno'};
		
	#��綯Ĵ
	if($CF{'strong'}&&!$EX{'nostrong'}){
	    my%ST=map{(my$s=$_)=~tr/"'<>&/\01-\05/;$s}($CF{'strong'}=~/(\S+)\s+(\S+)/go);
	    if($CF{'strong'}=~/^ /o){
		#��ĥ��綯Ĵ
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
		#���ܸ�綯Ĵ
		for(keys%ST){$str=~s[^(\Q$_\E.*)$][<STRONG  clAss="$ST{$_}"  >$1</STRONG>]gm;}
	    }
	}
		
	#URI��ư���
	if($CF{'noautolink'}||!$EX{'noautolink'}){
	    #[-_.!~*'()a-zA-Z0-9;:&=+$,]	->[!$&-.\w:;=~]
	    #[-_.!~*'()a-zA-Z0-9:@&=+$,]	->[!$&-.\w:=@~]
	    #[-_.!~*'()a-zA-Z0-9;/?:@&=+$,]	->[!$&-/\w:;=?@~]
	    #[-_.!~*'()a-zA-Z0-9;&=+$,]		->[!$&-.\w;=~]
	    #http URL ������ɽ��
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
	    #ftp URL ������ɽ��
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
	    #�᡼�륢�ɥ쥹������ɽ����
	    #"aaa@localhost"�ʤɤ�Ǽ��Ĥǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τǡ�
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
	    #�²�ư��
	    my$href_regex=qr{($http_URL_regex|$ftp_URL_regex|($mail_regex))};
	    my@isMail=('<A class="autolink" href="mailto:','<A class="autolink" href="');
	    $str=~s{((?:\G|>)[^<]*?)$href_regex}{$1$isMail[!$3]$2" target="_blank">$2</A>}go;
	    if($str=~/<(?:XMP|PLAINTEXT|SCRIPT)(?![0-9A-Za-z])/io){
		#XMP/PLAINTEXT/SCRIPT����������Ȥ�
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
    $IN{'body'}=~s/\t/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/go;
    $IN{'body'}=~s/((?:\G|>)[^<]*?) /$1&nbsp;/go;
    $IN{'body'}=~s/\n/<BR>/go;
	
    #-----------------------------
    #�񤭹���ǡ�����������
    my$crcOfThisArticle=&getCRC32($IN{'body'});
    $IN{'_Signature'}=&getSignature($EX{'signature'}||$IN{'pass'},$EX{'signature'});
	
    #-----------------------------
    #ZERO����μ���
    open(ZERO,'+<'."$CF{'log'}0.cgi")||die"Can't read/write log(0.cgi)[$?:$!]";
    eval{flock(ZERO,2)};
    seek(ZERO,0,0);
    my@zero=map{/^([^\x0D\x0A]*)/o}<ZERO>;
    index($zero[0],"Mir12=\t")&&die'ZERO�Υ�������Mir12���ʳ��Ǥ�';
    %Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
	
    #-----------------------------
    #@zer1�١����Ӥ餷�к�(?)
    #120�ð����@zer1�����������ؤ�ä����������
    my@zer1=split(/\s+/o,$zero[1]);
    @zer1>4&&$zer1[$#zer1]=~/\d+:\w+:\d+\[(\d+)\]/o&&$1+3600>$^T&&&showUserError('������������');
	
    #-----------------------------
    #���ߤ�����Υꥹ�Ȥ����
    &logfiles('number');
    $IN{'i'}=$file[0]+1if$IN{'i'}&&$IN{'i'}>$file[0]+1;
	
    #-----------------------------
    #@zer2�Υ��顼����
    if(@file){
	my@tmp=$zero[2]?split(/\s/o,$zero[2]):(0);
	@zer2=map{$tmp[$_-$tmp[0]]or(stat("$CF{'log'}$_.cgi"))[9]or$_}($tmp[0]+1)..$file[0];
	unshift@zer2,$tmp[0];
    }else{
	die'���餫�ʥХ� - @file���ɤ�˺��';
    }
	
    #-----------------------------
    #�񤭹��ߤ����������ĥ����������
    &exprewrt(); # doEvent('BeforeWriteArticle');
	
    #-----------------------------
    #���褤��
    unless($IN{'_ArticleType'}&2){
	#�������ֿ��񤭹���
	$IN{'_NewPassword'}=&mircrypt($^T,$IN{'pass'});
	$EX{'znew'}=1;
	if($IN{'i'}&&$zero[1]=~/($IN{'i'}):$crcOfThisArticle:([1-9]\d*)/
	   or length$IN{'j'}&&$zero[1]=~/(\d+):$crcOfThisArticle:($IN{'j'})/){
	    &showHeader;
	    print<<"_HTML_";
<H2 class="heading2">- ¿����ơ� -</H2>
<DIV class="center">
<P style="margin:0.6em">����Ƥ��줿���������Ƥ�<A href="$CF{'index'}?read=$1#art$1-$2" title="�����������ǧ����">��$1�֥���åɤ�$2����</A>��Ʊ�����Ƥ��Ȼפ��ޤ�<BR>
�����������ǧ���ơ�Ʊ�����ƤǤʤ����ϡ����Υե�����Ǿ����������Ƥ�����Ƥ��ƤߤƤ���������</P>
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="$CF{'index'}?read=$1#art$1-$2" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
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
	    #�����񤭹���
	    if($CF{'logmax'}>0&&@file>$CF{'logmax'}){
		#�Ť���������åɥե������ �ե�����̾�ѹ�/��� ����

=begin :comment

# ������ʬ�Ϥ��󤬤餬��䤹���Τǥ�⡣

@file��C<(101,100,99,95,91,������,3,2,1,0)>�Ȥ��ä�����
���ν��֤Ͼ�˹߽硣
�Ǹ��ɬ����������ե������ɽ�� 0 ����롣

@zer2��C<(1 1000000 10000001 ������ 1200000)>�Ȥ��ä�����
�ǽ�ο����ϵ����ֹ��@zer2�Ǥ�ź�����Ȥ��б���ɽ����
����Offset��100�ʤ鵭���ֹ�159�ξ����$zer2[59]�ˤ��롣

�ե����뤬�����������Ȥ��˵�������åɥե������������ݤˤϡ�
�嵭����Ĥ������Ʊ�����������������ʤ���Фʤ�ʤ���
���λ�����������åɥե����뤬������줿���Ȥˤ�äơ�
@file���꡹����������Ǥ����ǽ�������뤳�Ȥ���ա�
@zer2�ϵ������������Ƥ��Ƥ�Ϣ�֤ˤʤäƤ��롣

���ʤߤˡ�
$file[$#file-1] �Ϥ��λ��������뵭���Τ����ǵ�������å��ֹ椬�Ǥ⾮������ΤΡ���������å��ֹ��
$file[$CF{'logmax'}-1] �ϵ�������å��ֹ椬�Ǥ��礭����ΤΡ���������å��ֹ�򤢤�魯��
$file[$CF{'logmax'}-2] �Ϻ�����줿��˻Ĥä���������åɤΤ�����
�Ǥ⵭������å��ֹ椬�����ʤ�ΤΡ���������å��ֹ�򤢤�魯��

��äơ�C<$file[$CF{'logmax'}-2]-$file[$#file-1]>�Ϥ��λ����������ٵ������򤢤�魯��
#���浭������åɤ��������Ƥ����硢�ºݤ˺������뵭������åɿ��Ȥϰۤʤ롣

��
@file�ˤ�0.cgi���ޤޤ�Ƥ���Τǰ��¿����
�ޤ�@file�ˤϤ��줫���ɲä��뿷����åɤ��ʤ��Τǰ�ľ��ʤ�

=end :comment

=cut

		splice(@zer2,1,$file[$CF{'logmax'}-2]-$file[$#file-1]);
		&delThread($CF{'delold'},splice(@file,$CF{'logmax'}-1,@file-$CF{'logmax'}))
		    #($#file-1)-($CF{'logmax'}-1)+1=@file-$CF{'logmax'}���Ȥ�������
		    ||die"\$CF{'delold'}�����꤬�۾�Ǥ�($CF{'delold'})";
		$zer2[0]=$file[$CF{'logmax'}-2]-1;
	    }
	    $IN{'i'}=$file[0]+1;
	    open(FILE,'+>>'."$CF{'log'}$IN{'i'}.cgi")||die"Can't write log($IN{'i'})[$?:$!]";
	    eval{flock(FILE,2)};
	    die"�񤭹��߽�����˳����ޤ�ޤ���($CF{'log'}$IN{'i'}.cgi)"if-s"$CF{'log'}$IN{'i'}.cgi";
	    truncate(FILE,0);
	    seek(FILE,0,0);
	    print FILE "Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$^T;\t"
		."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
		.join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}($CF{'prtitm'}=~/\+(\w+)\b/go))."\n";
	    close(FILE);
	}else{
	    #-----------------------------
	    #�ֿ��񤭹���
	    open(FILE,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
	    eval{flock(FILE,2)};
	    seek(FILE,0,0);
	    my$line;
	    $line=$_ while<FILE>;
			
	    #����åɤΥ�å�
	    index($line,"Mir12=\tLocked")||&showUserError('���Υ���åɤϥ�å�����Ƥ���');
			
	    $IN{'j'}=$.; #$.-1+1
	    seek(FILE,0,2);
	    if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
		#�ѥ���ɤ������ѥ��ΤȤ��Ϻ���ҵ��������¤������äƤ��Ƥ���ƽ����
	    }elsif($CF{'maxChilds'}&&$IN{'j'}>$CF{'maxChilds'}){
		&showUserError('���˺���ҵ��������¤�ۤ��Ƥ���');
	    }
	    print FILE (!chomp$line&&++$IN{'j'}?"\n":'')
		."Mir12=\t;\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$^T;\t"
		."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
		.join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}$CF{'chditm'}=~/\+(\w+)\b/go)."\n";
	    close(FILE);
	}
		
	#-----------------------------
	#MailNotify
	if($CF{'mailnotify'}){
	    #����/�ֿ������ä����ϥ᡼�������
	    require'notify.pl';
	    &mailnotify(%IN);
	}
		
    }else{
	#-----------------------------
	#�����񤭹���
	open(FILE,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
	eval{flock(FILE,2)};
	seek(FILE,0,0);
	my@log=map{/^([^\x0D\x0A]*)/o}<FILE>;
	$#log<$IN{'j'}&&die'wa1: Something Wicked happend!';
	$log[$IN{'j'}]||die'wa2: Something Wicked happend!';
	my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
		
	#PasswordCheck
	if($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){
	    #MasterPass�ˤ��
	    if($IN{'pass'}){
		#Pass�ѹ�
		$IN{'oldps'}=$IN{'pass'};
	    }else{
		#Pass���Τޤ�
		$IN{'_NewPassword'}=$DT{'pass'};
	    }
	}else{
	    #UserPass�ˤ��
	    unless(&mircrypt($DT{'time'},$IN{'oldps'},$DT{'pass'})){
		&showHeader;
		print qq(<H2 class="heading2">Password Error</H2>\n);
		%CK=%IN;
		&rvsij;
		print&getFooter;
		exit;
	    }
	    index($log[$IN{'j'}],"Mir12=\tdel")||&showUserError("��$IN{'i'}�֤�$IN{'j'}�ϴ��˺������Ƥ���");
	    index($log[$IN{'j'}],"Mir12=\tlock")||&showUserError("��$IN{'i'}�֤�$IN{'j'}�ϥ�å�����Ƥ���");
	    $log[$#log]=~/Mir12=\tLocked(?:\S+ )*revise[ ;]/o&&&showUserError('���Υ���åɤϸǤ���å�����Ƥ���');
	    #Pass�ѹ�
	    $IN{'oldps'}=$IN{'pass'};
	}
		
	#�����Υ�å�
	$IN{'Mir12'}='lock:'if$EX{'lockArticle'};
		
	unless($IN{'_NewPassword'}){
	    #Pass�ѹ��������ѹ�
	    $DT{'time'}=$^T if$EX{'dnew'};
	    $IN{'_NewPassword'}=&mircrypt($DT{'time'},$IN{'pass'});
	}
	#�񤭹���
	$log[$IN{'j'}]=
	    "Mir12=\t$IN{'Mir12'};\tname=\t$IN{'name'};\tpass=\t$IN{'_NewPassword'};\ttime=\t$DT{'time'};\t"
	    ."body=\t$IN{'body'};\tsignature=\t$IN{'_Signature'};\t"
	    .join('',map{"$_=\t$IN{$_};\t"}grep{defined$IN{$_}}
		  ((!$IN{'j'}?$CF{'prtitm'}:$CF{'chditm'})=~/\+(\w+)\b/go));
	truncate(FILE,0);
	seek(FILE,0,0);
	print FILE map{"$_\n"}@log;
	close(FILE);
    }
	
    if($EX{'znew'}){
	#-----------------------------
	#�������ե����롢0.cgi�˽񤭹���
	#�������ֿ��λ��ˤ���ƾ������¸
	$#zer1=3if$#zer1>3; #(3+2=)5��@zer1����¸���
	unshift(@zer1,sprintf"%d:%s:%d[%d]",$IN{'i'},$crcOfThisArticle,$IN{'j'},$^T);
	my$num=$IN{'i'}-$zer2[0];
	$num>0||die"ZER2�Υǡ����������Ǥ� 'i':$IN{'i'},'zer2':$zer2[0]";
	$zer2[$num]=$^T;
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
    close(ZERO); #�����Ǥ�äȽ񤭹��߽�λ
	
    #-----------------------------
    #$IN{'cook'}��ON�ʤ�Cookie�ν񤭹���
    if($IN{'cook'}){
	unless($CF{'admps'}&&$IN{'oldps'}eq$CF{'admps'}){#�����ѥ��λ���Cookie��¸���ʤ�
	    &setCookie(\%IN);
	}
    }
	
    #-----------------------------
    #�񤭹����������ּ�ͳ�˽�����ɤ�����
    my$writeType=$IN{'_ArticleType'}&2?'��ľ��':'�񤭹���';
    &showHeader;
    print<<"_HTML_";
<H2 class="heading2">- $writeType��λ -</H2>
<DIV class="writingMessage">
<P>�ʲ������Ƥ���$IN{'i'}�֥���åɤ�$IN{'j'}���ܤ˽񤭹��ߤޤ�����<BR>
����Ǥ褱��Ф��Τޤ�TOP��Ǽ��Ĥ���äƤ���������<BR>
�������������ϰʲ��Υե�����ǽ���������Ƥ��Ƥ���������</P>

<DIV class="box"><P class="heading3">--- PREVIEW ---</P>
<P class="body" style="color:$IN{'color'}">$IN{'body'}</P></DIV>

<TABLE border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="$CF{'index'}?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
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
# �����ֿ�
#
sub showResponseMode{
    &getCookie;
    &showHeader;
    print<<'_HTML_';
<H2 class="heading2">- �����ֿ��⡼�� -</H2>
<DIV id="threadBox">
<H3 class="heading3">���Υ���åɤκ��ޤǤ�����</H3>
_HTML_
    my%status=&showArticle(i=>$IN{'i'},ak=>1,res=>1);
    print"This thread$IN{'i'} is deleted."if$status{'-isDeleted'};
    print<<'_HTML_';
</DIV>
<P id="paragraphThreadBox">
<LABEL for="inpDivHeight">�Ȥι⤵:
<INPUT type="text" id="inpDivHeight" value="400px"></LABEL>
<INPUT type="button" class="button" onclick="setDivHeight();return false" value="�⤵����">
<INPUT type="button" class="button" id="inpDivBorder" onclick="switchDivBorder(this);return false" value="�Ȥ򶹤��">
</P>
<SCRIPT type="text/javascript">
<!--
/* ========== �Ȥι⤵���� ========== */
function setDivHeight(){
	if(!document.getElementById)return false;
	if(!threadBox.style||!threadBox.style.height)return false;
	inpDivBorder.value='�Ȥ򹭤���';
	threadBox.style.height=inpDivHeight.value=inpDivHeight.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
	threadBox.style.overflow='auto';
	return true;
}

/* ========== �Ȥ򹭤����궹�᤿�� ========== */
function switchDivBorder(self){
	if(!document.getElementById)return false;
	if(!threadBox.style||typeof(threadBox.style.overflow)=='undefined')return false;
	
	var value=inpDivHeight.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
	if(threadBox.style.height==value){
		self.value='�Ȥ򶹤��';
		threadBox.style.height='auto';
		threadBox.style.overflow='visible';
	}else{
		self.value='�Ȥ򹭤���';
		threadBox.style.height=value
		threadBox.style.overflow='auto';
	}
	return true;
}

/* ========== �Ȥ����� ========== */
function initDiv(){
	if(!document.getElementById)return false;
	if(!threadBox.style||!threadBox.style.height)return false;
	inpDivBorder.value='�Ȥ򹭤���';
	threadBox.style.height=inpDivHeight.value=inpDivHeight.value.match(/([1-9]\d*)/)?RegExp.$1+'px':'400px';
	threadBox.style.overflow='auto';
	return true;
}

/* ==========  ========== */
//initDiv();
var threadBox=document.getElementById('threadBox');
var inpDivBorder=document.getElementById('inpDivBorder');
var inpDivHeight=document.getElementById('inpDivHeight');
-->
</SCRIPT>

_HTML_
    if($status{'-isAvailable'}){
	$CK{'i'}=$IN{'i'};
	$CK{'ak'}=1;
	&chdfrm;
    }else{
	printf'<P class="note">���ε�������å�No.%d��%s���ᡢ�ֿ����뤳�ȤϤǤ��ޤ���</P>',$IN{'i'},
	($status{'-isLocked'}?'��å�����Ƥ���'
	 :$status{'-isOverflowed'}?'����ҵ�������Ķ���Ƥ���'
	 :'��Ⱦ����ͳ��');
    }
    print&getFooter;
    exit;
}


#-------------------------------------------------

=head2 ���������������˥塼

=head3 ����

  $ ����ν����η��

=cut

sub showRvsMenu{
    &getCookie;
    &showHeader;
    my$mode='';
    #�⡼��ʬ��
    if(defined$IN{'rvs'}){$mode='rvs';print qq(<H2 class="heading2">- ���������⡼�� -</H2>\n);}
    elsif(defined$IN{'del'}){$mode='del';print qq(<H2 class="heading2">- ��������⡼�� -</H2>\n);}
    else{print qq(<H2 class="heading2">rmn: Something Wicked happend!</H2>).&getFooter;exit;}
    #��������-Cover�����
    if($_[0]){
	print<<"_HTML_";
<DIV class="center">
<H3 class="heading3">$_[0]</H3>
<TABLE align="center" border="0" cellspacing="0" summary="BackMenu">
<COL span="2" width="150">
<TR><TD><FORM action="$CF{'index'}?read=$IN{'i'}#art$IN{'i'}-$IN{'j'}" method="get">
<INPUT type="submit" class="button" accesskey="q" value="�Ǽ��Ĥ����(Q)">
</FORM></TD>
<TD><FORM action="$CF{'home'}" method="get">
<INPUT type="submit" class="button" accesskey="h" value="$CF{'name'}�����(H)">
</FORM></TD>
</TR></TABLE>
</DIV>
_HTML_
    }
    #������
    &logfiles('number');
    my$pageSelector=&pageSelector($#file,$CF{'delpg'},$mode);
    my@thisPage=splice(@{[@file]},($IN{'page'}-1)*$CF{'delpg'},$CF{'delpg'});
    $thisPage[$#thisPage]==0&&pop@thisPage;
    print<<"_HTML_";
<DIV class="center">$pageSelector</DIV>

<FORM id="List" method="post" action="$CF{'index'}">
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
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</TD></TR>
_HTML_
    #������åɤ���
    for(@thisPage){
	$_&&-e"$CF{'log'}$_.cgi"||next;
	my$i=$_;
	my$j=-1;
	open(FILE,'<'."$CF{'log'}$i.cgi")||die"Can't read log($i.cgi)[$?:$!]";
	eval{flock(FILE,1)};
	my$count=qq(<A href="$CF{'index'}?read=$i#art$i">��$i��</A>);
	#��������
	while(<FILE>){
	    $j++;
	    index($_,"Mir12=\tdel;\t")||next;
	    if(!index($_,"Mir12=\tLocked")){
		print<<"_HTML_";
<TR class="child">
<TH align="right">LOCKED</TH>
<TD align="right" colspan="2">���Υ���åɤϥ�å�����Ƥ��ޤ�</TD>
</TR>
_HTML_
		last;
	    }
	    my%DT=/([^\t]*)=\t([^\t]*);\t/go;
	    $count="Res $j"if$j;
	    my$num="$i-$j";
	    my$date=&date($DT{'time'});
	    #��ʸ�ν̤����
	    $DT{'body'}=~s/<BR\b[^>]*>/��/go;
	    $DT{'body'}=MirString->getTruncated($DT{'body'},60);
	    my$level=!$j?'parent':'child';
	    print<<"_HTML_";
<TR class="$level">
<TH align="right">$count</TH>
<TH align="left">$DT{'subject'}</TH>
<TD align="right">by $DT{'name'}</TD>
</TR>
<TR>
<TD><INPUT type="radio" name="$mode" value="$num"></TD>
<TD align="right">$date</TD>
<TD align="right">$DT{'body'}</TD>
</TR>
_HTML_
	}
	close(FILE);
    }
    print"</TABLE></DIV></FORM>\n";
    print qq(<DIV class="center">$pageSelector</DIV>);
    print&getFooter;
    exit;
}


#-------------------------------------------------

=head2 ��������

=head3 ����

  $ �������뵭����"120-4"�ʤɡ�

=cut

sub rvsArticle{
    ($IN{'i'},$IN{'j'})=split('-',$IN{'rvs'});
    open(FILE,'<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read log($IN{'i'}.cgi)[$?:$!]";
    eval{flock(FILE,1)};
    my@log=map{/^([^\x0D\x0A]*)/o}<FILE>;
    close(FILE);
    my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
    %DT||die"��$IN{'i'}�֥���åɤˤ�$IN{'j'}�ʤ�Ƥ���ޤ���";

=begin :comment

���Ȥ�$IN{'pass'}���Ϥ���ʤ��Ƥ⡢GetCookie��Cookie�򻲾Ȥ���
�⤷����������줿$CK{'pass'}���ѥ���ɤȰ��פ���н����⡼�ɤ��̤���
�Ȥ����褦�ˤ����������θ����ޤäƤ��롣
�����ѥ���ɤ����פ��ʤ�������Ϥ���褦���������롣

=end :comment

=cut

    if($IN{'pass'}){
	#IN�������Ƥ�����
	$IN{'oldps'}=$IN{'pass'};
	if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
	    #ADMINpassOK
	    $IN{'pass'}='';
	    #������
	}else{
	    index($DT{'Mir12'},'lock')+1&&&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�ϥ�å�����Ƥ��ޤ���");
	    #���¤�����å�
	    if($log[$#log]=~/Mir12=\tLocked:(?:\S+ )*revise[ ;]/o){
		$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*lockedBy=(\S+)[ ;]/o;
		'ThreadBuilder'eq$1||&showRvsMenu('���Υ���åɤϸǤ���å�����Ƥ��ޤ���');
		my%parent=$log[0]=~/([^\t]*)=\t([^\t]*);\t/go;
		&mircrypt($parent{'time'},$IN{'pass'},$parent{'pass'})
		    or&showRvsMenu('���Υ���åɤϸǤ���å�����Ƥ��ޤ���');
	    }
	    &mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
		or&showRvsMenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���");
	    #INpassOK
	    #������
	}
    }else{
	#Cookie��Ĵ�٤����˥�å�����Ƥ��뤫�ɤ��������å�
	index($DT{'Mir12'},'lock')+1&&&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�ϥ�å�����Ƥ��ޤ���");
	$log[$#log]=~/Mir12=\tLocked:(?:\S+ )*revise[ ;]/o
	    and&showRvsMenu('���Υ���åɤϸǤ���å�����Ƥ��ޤ���');
		
	#Cookie�ˤ��롩
	&getCookie;
	$IN{'oldps'}=$IN{'pass'}=$CK{'pass'};
	#-----------------------------
	unless(&mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})){
	    #̵���ʤ����Ϥ���
	    &showHeader;
	    print<<"_HTML_";
<H2 class="heading2">- ��$IN{'i'}�֤�$IN{'j'}�Υѥ����ǧ�� -</H2>
<FORM accept-charset="$CF{'encoding'}" id="Revise" method="post" action="$CF{'index'}">
<TABLE cellspacing="2" summary="Revise" width="550">
<COL width="50">
<COL width="170">
<COL width="330">
<P style="margin:0.6em">�ѥ���ɤ����Ϥ��Ƥ�������</P>
<P style="margin:0.6em"><SPAN class="ak">P</SPAN>assword:
<INPUT name="pass" type="text" accesskey="p" size="12" style="ime-mode:inactive" value="$CK{'pass'}">
<INPUT name="rvs" type="hidden" value="$IN{'rvs'}"></P>
<P style="margin:0.6em">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</p>
_HTML_
	    print&getFooter;
	    exit;
	}
	#CKpassOK
	#������
    }
    #Revise Main Routin
    &showHeader;
    print qq(<H2 class="heading2">- ��$IN{'i'}�֤�$IN{'j'}�ν����⡼�� -</H2>\n);
    %CK=%DT;
    @CK{qw(i j pass oldps)}=@IN{qw(i j pass oldps)};
    &rvsij;
    print&getFooter;
    exit;
}


#-------------------------------------------------

=head2 �������

=head3 ����

  $ ������뵭���Ⱥ����ˡ��"120-4-1"�ʤɡ�

=cut

sub delArticle{
    ($IN{'i'},$IN{'j'},$IN{'type'})=split('-',$IN{'del'});
    open(FILE,'+<'."$CF{'log'}$IN{'i'}.cgi")||die"Can't read/write log($IN{'i'}.cgi)[$?:$!]";
    eval{flock(FILE,2)};
    seek(FILE,0,0);
    my@log=map{/^([^\x0D\x0A]*)/o}<FILE>;
    my%DT=$log[$IN{'j'}]=~/([^\t]*)=\t([^\t]*);\t/go;
    #���ʬ��
  SWITCH:{
	if($CF{'admps'}&&$IN{'pass'}eq$CF{'admps'}){
	    #AdminPassOK
	    if($IN{'j'}==0&&!$IN{'type'}){
		#���������ˡ̵���ʤ����Ϥ���
		&showHeader;
		print<<"_HTML_";
<H2 class="heading2">- ��$IN{'i'}�֥���åɤκ�� -</H2>
<FORM accept-charset="$CF{'encoding'}" id="Delete" method="post" action="$CF{'index'}">
<FIELDSET style="padding:0.5em;width:60%">
<LEGEND>����åɤκ����ˡ������Ǥ�������</LEGEND>
<TD>
<LABEL for="mark">�Ƶ�������ʸ�Τߺ��<INPUT id="mark" name="del" type="radio" value="$IN{'del'}-1" checked></LABEL>
<LABEL for="$CF{'delthr'}">��������åɤ���<INPUT id="$CF{'delthr'}" name="del" type="radio" value="$IN{'del'}-2"></LABEL>
</FIELDSET>

<P style="margin:0.6em">
<INPUT name="pass" type="hidden" value="$IN{'pass'}">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" value="����󥻥�">
</P>
_HTML_
		print&getFooter;
		exit;
	    }
	    $IN{'j'}==0&&$IN{'type'}==2&&last SWITCH;
	}else{
	    #����Pass
	    index($log[$IN{'j'}],"Mir12=\tdel")||&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�ϴ��˺������Ƥ��ޤ���");
	    index($log[$IN{'j'}],"Mir12=\tlock")||&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�ϥ�å�����Ƥ��ޤ���");
	    $log[$#log]=~/Mir12=\tLocked:(?:\S+ )*delete[ ;]/o
		and&showRvsMenu('���Υ���åɤϸǤ���å�����Ƥ��ޤ���');
	    &mircrypt($DT{'time'},$IN{'pass'},$DT{'pass'})
		or&showRvsMenu("���Ϥ��줿�ѥ���ɤ���$IN{'i'}�֤�$IN{'j'}�Τ�Τȹ��פ��ޤ���");
	    $IN{'j'}==0&&$#log==0&&last SWITCH;
	}
		
	#mark
	$log[$IN{'j'}]=~s/^Mir12=\t([^\t]*);\t/Mir12=\tdel;\t/go;
	truncate(FILE,0);
	seek(FILE,0,0);
	print FILE map{"$_\n"}@log;
	close(FILE);
	&showRvsMenu("��$IN{'i'}�֤�$IN{'j'}�������ޤ�����");
    }
    close(FILE);
    #�Ƶ������
    &delThread($CF{'delthr'},$IN{'i'});
    &showRvsMenu("��$IN{'i'}�֥���åɤ������ޤ�����($CF{'delthr'})");
    exit;
}


#-------------------------------------------------
# ��ʸ������ǽ
#
sub showArtSeek{
    &showHeader;
    print qq(<H2 class="heading2">- �����⡼�� -</H2>);
    my%SK=split(/\s+/o,$CF{'sekitm'});
	
    if(length$IN{'seek'}){
	#-----------------------------
	#���������ɽ��
	my$result='';
	my$item='ALL'eq$IN{'item'}?'':";\t$IN{'item'}";
	my$seek=quotemeta$IN{'seek'};
		
	&logfiles('number');
		
	if('i'eq$IN{'every'}){
	    #����åɤ��ȸ���
	    for(@file){
		$_||last;
		open(FILE,'<'."$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$?:$!]";
		eval{flock(FILE,1)};
		my$thread;
		read(FILE,$thread,-s"$CF{'log'}$_.cgi");
		close(FILE);
		MirString->matchedItem($thread,$item,$seek)||next;
		$result.=qq(<A href="$CF{'index'}?read=$_#art$_">No.$_</A>\n);
	    }
	}else{
	    #�������ȸ���
	    for(@file){
		$_||last;
		open(FILE,'<'."$CF{'log'}$_.cgi")||die"Can't read log($_.cgi)[$?:$!]";
		eval{flock(FILE,1)};
		my$thread;
		read(FILE,$thread,-s"$CF{'log'}$_.cgi");
		close(FILE);
		index($thread,$IN{'seek'})+1||next;
		my$i=$_;
		for(MirString->matchedItems($thread,$item,$seek)){
		    $result.=qq(<A href="$CF{'index'}?read=$i#art$i-$_">No.$i-$_</A>\n);
		}
	    }
	}
	print<<"_HTML_";
<P>��<STRONG>$IN{'seek'}</STRONG>�פ�<STRONG>$SK{$IN{'item'}}</STRONG>��<STRONG>@{[
'i'eq$IN{'every'}?'����å�':'�Ƶ���']}����</STRONG>�˸���������̡�<BR>
@{[$result?"�ʲ��Υ���åɤǸ���ñ���ȯ�����ޤ�����<BR>$result":"����ñ���ȯ���Ǥ��ޤ���Ǥ���"]}<BR>
�����ä����֡�@{[join'+',(times)[0,1]]}��</P>
_HTML_
    }
	
    print<<"_HTML_";
<FORM accept-charset="$CF{'encoding'}" id="seek" method="post" action="$CF{'index'}">
<DIV class="center"><TABLE cellspacing="2" summary="�����ե�����" style="margin: 1em auto">
<TR>
<TH class="item">
<LABEL accesskey="m" for="item">�����������(<SPAN class="ak">M</SPAN>)</LABEL></TH>
<TD><SELECT name="item" id="item">
_HTML_
    my$select=join('',map{qq(<OPTION value="$_">$SK{$_}</OPTION>)}($CF{'sekitm'}=~/(\w+) \S+/go));
    $select=~s/(value="$IN{'item'}")/$1 selected/io;
    print<<"_HTML_";
$select</SELECT>
</TD>
</TR>
<TR>
<TH class="item"><LABEL accesskey="k" for="seek">��������ñ��(<SPAN class="ak">K</SPAN>)</LABEL></TH>
<TD><INPUT type="text" name="seek" id="seek" style="ime-mode:active;width:200px;" value="$IN{'seek'}"></TD>
</TR>
<TR>
<TH class="item">��������ñ��</TH>
<TD>
_HTML_
    my%DT=qw(i ����åɤ��� j �Ƶ�������);
    $select=join('',map{qq(<LABEL accesskey="$_" for="every$_"><INPUT type="radio" name="every" id="every$_")
			.qq( value="$_">$DT{$_}(<SPAN class="ak">\u$_</SPAN>)</LABEL>\n)}('i','j'));
    $select=~s/(value="$IN{'every'}")/$1 checked/io;
    print<<"_HTML_";
$select
</TD>
</TR>
<TR>
<TD colspan="2">
<INPUT type="submit" class="submit" accesskey="s" value="OK">��
<INPUT type="reset" class="reset" accesskey="r" value="����󥻥�">
</TD>
</TR>
</TABLE>
</DIV>
<DIV class="center"><TABLE class="note"><TR><TD>
<UL class="note">
<LI>���ԤǤϸ���ʸ���������ɽ����Ȥ����ȤϽ���ޤ���</LI>
<LI>�֥饦���Ρ֤��Υڡ������⸡���פ�Ȥ��С�<BR>�ɤ���õ������ñ�줬����Τ���狼��ޤ��͡�</LI>
</UL></TD></TR></TABLE></DIV>
</FORM>
_HTML_
    print&getFooter;
    exit;
}


#-------------------------------------------------
# �桼�����������顼
#
sub showUserError{
    my$message=shift();
    &showHeader;
    print<<"_HTML_";
<H2 class="heading2">- ���顼��ȯ�����ޤ��� -</H2>
<P>�����ؤ򤫤��ƿ������������ޤ���<BR>
<span class="warning">$message</span>���ᡢ<BR>����ʽ�����³�Ԥ��뤳�Ȥ��Ǥ��ޤ���Ǥ���<BR>
�ʲ���ǰ�Τ��ả���Ϥ��줿�ǡ��������󤷤Ƥ����ޤ�<BR>
���פʾ��󤬤����硢��¸���Ƥ����ơ��ޤ��ε������Ƥ��Ƥ�������</P>
<TABLE border="1" summary="�桼���������ѿ���ɽ�����Ƥ���">
<CAPTION>��������ä�����</CAPTION>
_HTML_
    for(grep{/^[^_]/o&&defined$IN{$_}&&length$IN{$_}}keys%IN){
	$IN{$_}=~s/<BR>/\n/go;
	printf"<TR><TH>%s</TH><TD><XMP>%s</XMP></TD>\n",$_,$IN{$_};
    }
    print'</TABLE>';
    print&getFooter;
    exit;
}


#-------------------------------------------------

=head2 RDF Site Saummary

=head3 ����

=cut

sub rss{
    my $maxItem = 15;
    my$link = $CF{'home'};
    $link = $ENV{'SERVER_NAME'} if $link eq '/';
    
    my %item =();
    my @logfiles = &logfiles('date');
    for( 0 .. ( $maxItem > $#logfiles ? $#logfiles : $maxItem-1 ) ){
    	my $i = $logfiles[$_];
	-e"$CF{'log'}$i.cgi"||next;
	
	open(FILE,'<'."$CF{'log'}$i.cgi")||die"Can't read log($i.cgi)[$?:$!]";
	eval{flock(FILE,1)};
	my@articles=<FILE>;
	close(FILE);
	
	my $title = '';
	for( 0, reverse( (@articles-$maxItem) .. $#articles )){
	    my $j = $_;
	    my %DT = ($articles[$_] =~ /([^\t]*)=\t([^\t]*);\t/go);
	    $DT{'i'} = $i;
	    $DT{'j'} = $j;
	    $DT{'_uri'} = "$CF{'self'}?read=$DT{'i'}#art$DT{'i'}-$DT{'j'}";
	    $DT{'_date'} = &datef($DT{'time'}, 'dateTime');
	    if($DT{'subject'}){
		$DT{'_title'} = "$i-$j ".$DT{'subject'};
	    	$title = $DT{'subject'};
	    }elsif($DT{'title'}){
		$DT{'_title'} = "$i-$j ".$DT{'title'};
	    	$title = $DT{'title'};
	    }else{
		$DT{'_title'} = "$i-$j ".$title;
	    }
	    $item{$DT{'time'}} = \%DT;
	}
    }
    my @latestArticles = map{$item{$_}}sort{$b<=>$a}keys%item;
    $#latestArticles = $maxItem - 1 if @latestArticles > $maxItem;
    
    my $output = <<"EOF";
<rdf:RDF 
  xmlns="http://purl.org/rss/1.0/"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xml:lang="ja">
 <channel rdf:about="$CF{'self'}">
  <title>$CF{'title'}</title>
  <link>$link</link>
  <description>$CF{'pgtitle'}</description>
  <items>
   <rdf:Seq>
EOF
    for(@latestArticles){
	$output .= <<EOF;
  <rdf:li rdf:resource="$_->{'_uri'}" />
EOF
    }
    $output .= <<EOF;
   </rdf:Seq>
  </items>
 </channel>

EOF
    for(@latestArticles){
	#��ʸ�ν̤����
	my $title = MirString->getTruncated($_->{'_title'},90);
	my $description = $_->{'body'};
	$description =~ s/<BR\b[^>]*>/��/go;
	$description = MirString->getTruncated($description,450);
	$output .= <<"EOF";
 <item rdf:about="$_->{'_uri'}">
  <title>$title</title>
  <link>$_->{'_uri'}</link>
  <description>$description</description>
  <dc:date>$_->{'_date'}</dc:date> 
 </item>

EOF
    }
    $output .= " </rdf:RDF>\n";
    
    my$die = $SIG{'__DIE__'};
    $SIG{'__DIE__'} = '';
    # Encode
    my$flag=0;
    eval q{
      use Encode;
      Encode::from_to( $output, $CF{'encoding'}, 'utf-8' );
      $flag=1;
      };
    unless( $flag ){
	# Jcode
	eval q{
	  use Jcode;
	  $output = Jcode->new( $output, $CF{'encoding'} )->utf8;
	  $flag=1;
	  };
    }
    $SIG{'__DIE__'} = $die;
    
    my $encoding = $flag ? 'utf-8' : $CF{'encoding'};
    print <<"EOF";
Status: 200 OK
Cache-Control: private
Date: @{[&datef($^T,'rfc1123')]}
Content-Language: ja-JP
Content-type: application/rss+xml; charset=$encoding

<?xml version="1.0" encoding="$encoding" ?>
EOF
    print $output;
    exit;
}


#-------------------------------------------------

=head2 Location��ž��

=head3 ����

  ;
  $ �������URL�����ФǤ����ФǤ��

=cut

sub locate{
    my$i=$_[0];
    $i||die'"Stay here."';
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
Content-type: text/html; charset=$CF{'encoding'}

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
# mainľ���Υ��֥롼���󷲤����

#-------------------------------------------------
# Form���Ƽ���
#
sub getParam{
    my%option=@_;
	
    my$params;
    my@params=();
    #��������
    unless($ENV{'REQUEST_METHOD'}){
	@params=@ARGV;
    }elsif('HEAD'eq$ENV{'REQUEST_METHOD'}){ #forWWWD
	#Method��HEAD�ʤ��LastModifed����Ϥ��ơ�
	#�Ǹ����ƻ�����Τ餻��
	my$last=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
	print"Status: 200 OK\nLast-Modified: $last\n"
	    ."Content-Type: text/plain\n\nLast-Modified: $last";
	exit;
    }elsif('POST'eq$ENV{'REQUEST_METHOD'}){
	read(STDIN,$params,$ENV{'CONTENT_LENGTH'});
    }elsif('GET'eq$ENV{'REQUEST_METHOD'}){
	$params=$ENV{'QUERY_STRING'};
    }
	
    #������ϥå����
    unless($params){
    }elsif(length$params>262114){ # 262114:�����������ξ��(byte)
	#����������
	&showHeader;
	print"������ʤ�Ǥ��̤�¿�����ޤ�\n$params";
	print&getFooter;
	exit;
    }elsif(length$params>0){
	#���Ϥ�Ÿ��
	@params=split(/[&;]/o,$params);
    }
	
    #���Ϥ�Ÿ�����ƥϥå���������
    my%DT;
    while(@params){
	my($i,$j)=split('=',shift(@params),2);
	$i=~/([a-z][-.:\w]*)/o||next;$i=$1;
	defined$j||($DT{$i}='')||next;
	study$j;
	$j=~tr/+/\ /;
	$j=~s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
	$j=MirString->getValidString($j);
	#�ᥤ��ե졼��β��Ԥ�\x85�餷�����ɡ��б�����ɬ�פʤ���͡�
	$j=~s/\x0D\x0A/\n/go;$j=~tr/\r/\n/;
	if(!$option{'noescape'}&&'body'ne$i){
	    #��ʸ�ʳ������̥����ػ�
	    $j=~s/\t/&nbsp;&nbsp;/go;
	    $j=~s/&(#?\w+;)?/$1?"&$1":'&#38;'/ego;
	    $j=~s/"/&#34;/go;
	    $j=~s/'/&#39;/go;
	    $j=~s/</&#60;/go;
	    $j=~s/>/&#62;/go;
	    $j=~s/\n+$//o;
	    $j=~s/\n/<BR>/go;
	}#��ʸ�ϸ�ǤޤȤ��
	$DT{$i}=$j;
    }
    return%DT if$option{'nofiltering'};
	
    #�����α�������
    $IN{'ra'}=($ENV{'REMOTE_ADDR'}&&$ENV{'REMOTE_ADDR'}=~/([\d\:\.]{2,56})/o)?$1:'';
    $IN{'hua'}=MirString->getValidString($ENV{'HTTP_USER_AGENT'});
    $IN{'hua'}=~tr/\x09\x0A\x0D/\x20\x20\x20/;
	
    if(defined$DT{'body'}){
	#�����񤭹���
	#http URL ������ɽ��
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
	#�᡼�륢�ɥ쥹������ɽ����
	#"aaa@localhost"�ʤɤ�WWW��ǡ֥᡼�륢�ɥ쥹�פȤ��ƻȤ��Ȥϻפ��ʤ��Τǡ�
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
		
	#body�������ɬ�ܹ��ܤν���
	if($DT{'i'}&&$DT{'i'}=~/([1-9]\d*)/o){
	    $IN{'i'}=$1;
	    if(defined$DT{'j'}&&$DT{'j'}=~/^(0|[1-9]\d*)/o){
		#����{��|��}����
		$IN{'j'}=$1;
		unless($DT{'oldps'}){
		}elsif($DT{'oldps'}eq$CF{'admps'}){
		    $IN{'oldps'}=$CF{'admps'};
		}elsif($DT{'oldps'}=~/(.{8,128})/o){
		    $IN{'oldps'}=$1;
		}
		$IN{'_ArticleType'}=!$IN{'j'}?2:3;
	    }else{
		#�����ҵ���
		$IN{'_ArticleType'}=1;
	    }
	}else{
	    #�����Ƶ���
	    $IN{'j'}=0;
	    $IN{'_ArticleType'}=0;
	}

=begin :comment

# ��������

0: �����Ƶ���
1: �����ҵ���
2: �����Ƶ���
3: �����ҵ���

=end :comment

=cut

	$IN{'name'}=MirString->getTruncated($DT{'name'},40);
	$IN{'cook'}=($DT{'cook'}=~/(.)/o)?'on':'';
	unless($DT{'pass'}){
	}elsif($DT{'pass'}eq$CF{'admps'}){
	    $IN{'pass'}=$CF{'admps'};
	}elsif($DT{'pass'}=~/(.{8,128})/o){
	    $IN{'pass'}=$1;
	}
		
	{ #�ե���������ƽ���
	    for($CF{$IN{'_ArticleType'}&1?'chditm':'prtitm'}=~/\b(\w+)\b/go){
		if('color'eq$_){
		    $IN{'color'}=$DT{'color'}=~/([\#\w\(\)\,]{1,20})/o?$1:'';
		}elsif('email'eq$_){
		    $IN{'email'}=$DT{'email'}=~/($mail_regex)/o?$1:'';
		    $IN{'email'}=~s/\@/&#64;/;
		}elsif('home'eq$_){
		    $IN{'home'}=$DT{'home'}=~/($http_URL_regex)/o?$1:'';
		}elsif('icon'eq$_){
		    $IN{'icon'}=$DT{'icon'}=~/(.+)/o?$1:'';
		}elsif('cmd'eq$_){
		    $IN{'cmd'}=$DT{'cmd'}=~/(.+)/o?$1:'';
		}elsif('subject'eq$_){
		    $IN{'subject'}=MirString->getTruncated($DT{'subject'}?$DT{'subject'}:$DT{'body'},70);
		}elsif('ra'eq$_||'hua'eq$_){
		    next;
		}else{
		    $IN{"$_"}=($DT{"$_"}=~/(.+)/o)?$1:'';
		}
	    }
	}
	#body�ν����ϴ���Ū��&writeArticle�ǹԤ�
	$IN{'body'}=$DT{'body'}=~/(.*\S)/os?$1:'';
	$IN{'_isEditing'}=1;
    }elsif(defined$DT{'new'}){
	#�����񤭹���
	$IN{'j'}=0;
	$IN{'_isEditing'}=1;
    }elsif(defined$DT{'res'}){
	#�ֿ��񤭹���
	$IN{'i'}=$1 if$DT{'res'}=~/([1-9]\d*)/o;
	$IN{'_isEditing'}=1;
    }elsif(defined$DT{'seek'}){
	#����
	$IN{'seek'}=($DT{'seek'}=~/(.+)/o)?$1:'';
	my%SK=split(/\s+/o,$CF{'sekitm'});
	$DT{'item'}=($DT{'item'}=~/(.+)/o)?$1:'';
	$IN{'item'}=($SK{$DT{'item'}})?$DT{'item'}:'ALL';
	$IN{'every'}=($DT{'every'}=~/([ij])/o)?$1:'i';
    }elsif(defined$DT{'del'}){
	#��������ꥹ��or�¹�
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
	#���������ꥹ��or�¹�
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
	#�������󥫥���
	$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
	return($IN{'icct'}=1);
    }elsif(defined$DT{'rss'}){
	#RSS
	return($IN{'rss'}=1);
    }elsif(defined$DT{'help'}){
	#�إ��
	return($IN{'help'}=1);
    }elsif(defined$DT{'home'}){
	#�ۡ���
	return($IN{'home'}=1);
    }elsif(defined$DT{'compact'}){
	#����ü���⡼��
	require'compact.cgi';
	exit;
    }elsif($DT{'read'}){
	#���ɤ�
	$IN{'read'}=$1 if$DT{'read'}=~/([1-9]\d*)/o;
	$IN{'page'}=1; #read�ǻ��ꤵ�줿�ͤ����������Ȥ��Τ���
    }else{
	#�ڡ���
	$IN{'read'}=0;
	$IN{'page'}=($DT{'page'}&&$DT{'page'}=~/([1-9]\d*)/o)?$1:1;
    }
    return%IN;
}


#------------------------------------------------------------------------------#

=head2 HTTP,HTML,Page�إå�����ޤȤ�ƽ��Ϥ���

=head3 ����

  ;
  % ���Ϥ���HTML�Υ��ץ����

=cut

sub showHeader{
    my$lastModified;
    if($CF{'use304'}&&$ENV{'HTTP_IF_MODIFIED_SINCE'}){
	my$client=(&parse_date($ENV{'HTTP_IF_MODIFIED_SINCE'}))[0];
	my$server=(stat("$CF{'log'}0.cgi"))[9];
	if($client&&$server<=$client){
	    print<<"_HTML_";
Status: 304 Not Modified
Date: @{[&datef($^T,'rfc1123')]}
Content-Language: ja-JP
Content-type: text/html; charset=$CF{'encoding'}

_HTML_
	    exit;
	}
	$lastModified=&datef($server,'rfc1123');
    }else{
	$lastModified=&datef((stat("$CF{'log'}0.cgi"))[9],'rfc1123');
    }
    my%DT=@_;
	
    #-----------------------------
    #����
	
    #Header
    $DT{'head'}||=$CF{'head'};
    #Skyline
    $DT{'skyline'}||=&getLastpost;
	
    #-----------------------------
    #HTML�񤭽Ф�
    print<<"_HTML_";
Status: 200 OK
Cache-Control: private
Date: @{[&datef($^T,'rfc1123')]}
Content-Language: ja-JP
Content-type: text/html; charset=$CF{'encoding'}
_HTML_
    print"Last-Modified: $lastModified\n"if$CF{'useLastModified'};
    #GZIP Switch
    my$status=qq(<META http-equiv="Last-Modified" content="$lastModified">\n);
    $status.=join''
	,map{qq(<META http-equiv="Set-Cookie" content="$_">\n)}split("\n",$CF{'-setCookie'})if$CF{'-setCookie'};
	
    $CF{'conenc'}="|$CF{'gzip'} -cfq9"if!defined$CF{'conenc'}||'|gzip -cfq9'eq$CF{'conenc'}and$CF{'gzip'};
    if($CF{'conenc'}&&$ENV{'HTTP_ACCEPT_ENCODING'}&&index($ENV{'HTTP_ACCEPT_ENCODING'},'gzip')+1or$CF{'forceGZIP'}){
	#���ifʸ��gzip����Ǥ����Ƥ���ΤϡȻ��͡�
	#gzip/compress�ʳ����б����Ƥ�֥饦���ϵ��ʤ��ᡢ���Ѥؤμ��פ����ʤ��Ȼפ��뤿���
	#$CF{'conenc'}�������ǽ�ˤ��Ƥ���Τϡ�GZIP����ž����ON/OFF�ڤ��ؤ��Τ��ᡢ������
	if(!$CF{'forceGZIP'}&&$ENV{'SERVER_NAME'}#�����к�
	   and	1+index($ENV{'SERVER_SOFTWARE'},'WhizBanner') #infoseek��
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

=begin :comment

		#memo. cgi����mod_gzip���Ƥ���ʤ��äݤ�
		}elsif($ENV{'SERVER_SOFTWARE'}&&index($ENV{'SERVER_SOFTWARE'},'mod_gzip')+1){
			print"\n";
			$status.="<!-- did't use gzip because this server is using mod_gzip -->";

=end :comment

=cut

	}else{
	    print"Content-encoding: gzip\n\n";
	    if(!open(STDOUT,$CF{'conenc'})){
		#GZIP���Ի��Υ��顼��å�����
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
	    #GZIP����ž���򤫤�����Ȥ��Ϥ�����
	    print' 'x 2048if$ENV{'HTTP_USER_AGENT'}&&index($ENV{'HTTP_USER_AGENT'},'MSIE')+1; #IE�ΥХ��к�
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
# �ǿ�����Ƥξ�������
#
sub getLastpost{
    %Z0||&getZeroInfo;
    my$date=&date($Z0{'time'});
    my$dateNow="Date:\t\t".&datef($^T,'dateTime')
	."\nLast-Modified:\t".&datef((stat("$CF{'log'}0.cgi"))[9],'dateTime');
    return sprintf qq(<P class="lastpost" title="%s"><A href="$CF{'index'}?read=%s#art%s">Lastpost: %s %s</A></P>)
	,$dateNow,$Z0{'Mir12'},$Z0{'Mir12'},$date,$Z0{'name'};
}

#-------------------------------------------------
# ZERO����ե�������ɤ߹���
#
sub getZeroInfo{
    open(ZERO,'<'."$CF{'log'}0.cgi")||die"Can't read log(0.cgi)[$?:$!]";
    eval{flock(ZERO,1)};
    my@zero=map{/^([^\x0D\x0A]*)/o}<ZERO>;
    close(ZERO);
    $zero[0]&&index($zero[0],"Mir12=\t")&&die'ZERO�Υ�������Mir12���ʳ��Ǥ�';
    %Z0=($zero[0]=~/([^\t]*)=\t([^\t]*);\t/go);
    @zer2=$zero[2]?split(/\s/o,$zero[2]):(0);
}


#-------------------------------------------------

=head2 ��������åɥե�����Υꥹ�Ȥ����

=head3 ����

  ;
  $ ��������åɥե�����ꥹ�Ȥν���(date|number)

=head3 ����

���ե�����̾���������
�����ֹ����Ϲ��������˴�Ť����¤��ؤ���
�ե�����̾�ֹ�Υꥹ�Ȥ��֤���

=cut

sub logfiles{
    undef@file;
    opendir(DIR,$CF{'log'})||die"Can't read directory($CF{'log'})[$?:$!]";
    my@list=grep{int$_}map{/^(\d+)\.cgi$/o}readdir(DIR);
    closedir(DIR);
    if('date'eq$_[0]){
	#���ս� 'date'
	%Z0||&getZeroInfo;
	my@list=grep{$_>$zer2[0]}@list;
	my@tmp=map{$zer2[$_-$zer2[0]]}@list;
	@file=@list[sort{$tmp[$b]<=>$tmp[$a]or$list[$b]<=>$list[$a]}0..$#list];
    }else{
	#�����ֹ�� 'number'
	@file=sort{$b<=>$a}@list;
    }
    push(@file,0);
    return@file;
}


#-------------------------------------------------

=head2 �ڡ�������TABLE

=head3 ����

  $ �����ǲ�����åɤ���Ρ�
  $ 1�ڡ���������Υ���åɿ�
  ;
  $ �⡼�ɤ��ݻ�(rvs,del)
  $ ľ�����٤�ڡ�����
  $ following / preceding�ǻȤ�ʸ�����arrayRef

=cut

sub pageSelector{
    my$thds=shift||1;
    my$page=shift||1;
    my$mode=$_[0]?"$_[0];page":'page';@_&&shift;
    my$max=$_[0]||20;@_&&shift; #ľ�����٤�ڡ�����
    my$pageText=$_[0]?shift: #�ڡ������쥯���Ѥ�ʸ��
	['[�ǿ�]',qq(<A accesskey="," href="$CF{'index'}?%s=%d">&#60; ���</A>)
	 ,'[�Ǹ�]',qq(<A accesskey="." href="$CF{'index'}?%s=%d">�Τ� &#62;</A>)];@_&&shift;

	
    #pageɽ��Ĵ��
    my$half=int($max/2);
    my$str; #$str�ڡ����ܤ���
    my$end; #$end�ڡ����ܤޤ�Ϣ³����ľ�����٤�褦��ɽ��
    my$pags=int(($thds-1)/$page)+1;
    my@key=map{qq( accesskey="$_")}('0','!','&#34;','#','$','%','&#38;','&#39;','(',')');#1-9�ڡ�����AccessKey
	
    #�ɤ�����ɤ��ޤ�
    if($pags<=$max){
	$str=1;
	$end=$pags;
    }elsif($IN{'page'}-$half<=1){
	#1-10
	$str=1;
	$end=$max;
    }elsif($IN{'page'}+$half>=$pags){
	#(max-10)-max
	$str=$pags-$max+1;
	$end=$pags;
    }else{
	$str=$IN{'page'}-$half+1;
	$end=$IN{'page'}+$half-1;
    }
	
    #�����
    my@page=map{$_==$IN{'page'}?qq(<STRONG class="current">$_</STRONG>)
	    :sprintf qq(<A href="$CF{'index'}?%s=%d"%s>%d</A>),$mode,$_,$key[$_]?$key[$_]:'',$_}$str..$end;
	
    #����ȺǸ�
    unshift(@page,qq(<A accesskey="&#60;" href="$CF{'index'}?$mode=1">1</A> ..))		if$str!=1;
    push(@page,qq(.. <A accesskey="&#62;" href="$CF{'index'}?$mode=$pags">$pags</A>))	if$end!=$pags;
	
    #following / preceding
    my$following=$IN{'page'}==$str?
	$pageText->[0]:sprintf$pageText->[1],$mode,$IN{'page'}-1;
    my$preceding=$IN{'page'}==$end?
	$pageText->[2]:sprintf$pageText->[3],$mode,$IN{'page'}+1;
	
    #��������
    return &getPageSelectorSkin($following,join("\n",@page),$preceding,$str,$end,$pags,$mode);
}


#-------------------------------------------------

=head2 ����ɽ��

=head3 ����

  % ���Ϥ��뵭���ξ���

=cut

sub showArticle{
    #���Υ���åɶ��̤ξ���
    my%DT=@_;
    $DT{'j'}=-1;
    $DT{'-maxChildsShown'}=-1if!defined$DT{'-maxChildsShown'};
    $DT{'-unreads'}||=1;
    $DT{'-isLocked'}=0;
	
    -e"$CF{'log'}$DT{'i'}.cgi"||return -isDeleted=>1;
	
    open(FILE,'<'."$CF{'log'}$DT{'i'}.cgi")||die"Can't read log($DT{'i'}.cgi)[$?:$!]";
    eval{flock(FILE,1)};
    my@articles=<FILE>;
    close(FILE);
	
    my$maxChildsShown=$DT{'-maxChildsShown'}>-1?int(abs($DT{'-maxChildsShown'})):$#articles;
    my$horizon=$#articles-$maxChildsShown;
	
    #read�⡼�ɤλ�������
    $horizon=0if$IN{'read'}&&$IN{'read'}==$DT{'i'};
	
    for(@articles){
	unless(++$DT{'j'}){
	    #�Ƶ���
	    $DT{'-unreads'}=&artprt(\%DT,$_);
	    print<<"_HTML_"if$horizon>0;
<P class="overflowMessage">�ҵ�������¿�����ᡢ�ǿ���$maxChildsShown��Τ�ɽ�����ޤ���
��������ε�����<A href="$CF{'index'}?res=$DT{'i'}">�ֿ��⡼��</A>�Ǹ��뤳�Ȥ��Ǥ��ޤ���</P>
_HTML_
	}else{
	    #�ҵ���
	    $DT{'j'}>$horizon||next;
	    index($_,"Mir12=\tdel")||next;
	    index($_,"Mir12=\tLocked")||++$DT{'-isLocked'}&&last;
	    $DT{'-unreads'}=&artchd(\%DT,$_);
	}
    }
    $DT{'-isOverflowed'}=$CF{'maxChilds'}&&$DT{'j'}>=$CF{'maxChilds'}?1:0;
    $DT{'-isAvailable'}=not$DT{'-isLocked'}+$DT{'-isOverflowed'};
    #�����եå�
    &artfot(\%DT)if$DT{'j'}+1;
    return wantarray?map{$_,$DT{$_}}grep{/^-/o}keys%DT:$DT{'-unreads'};
}


#-------------------------------------------------
# Cookie���������
#
sub getCookie{
    %CK=();
    if($ENV{'HTTP_COOKIE'}){
	my$char=MirString->getCharRegexp;
	for($ENV{'HTTP_COOKIE'}=~/(?:^|; )Mireille=([^;]*)/go){
	    s/%([\dA-Fa-f]{2})/pack('H2',$1)/ego;
	    my%DT=/(\w+)\t($char*?)(?:\t|$)/go;
	    for(keys%DT){
		defined$CK{$_}&&$CK{'lastModified'}>=$DT{'lastModified'}&&next;
		$CK{$_}=$DT{$_};
	    }
	}
    }
    %CK=%{&verifyCookie(\%CK)};
    return%CK;
}


#-------------------------------------------------
=head2 Cookie��Ĵ��

=head3 ����

\% Ĵ�٤�ϥå���Υ�ե����

=cut

sub verifyCookie{
    my%DT=%{shift()};
    #���ּ��������
    unless($CK{'expire'}){
	#����
	$DT{'time'}||=0;
	$DT{'expire'}=$^T+$CF{'newuc'};
    }elsif($CK{'expire'}>$^T){
	#������
	$DT{'time'}=$CK{'time'};
	$DT{'expire'}=$CK{'expire'};
    }else{
	#�����ڤ�
	$DT{'time'}=$CK{'expire'}-$CF{'newuc'};
	$DT{'expire'}=$^T+$CF{'newuc'};
    }
    $DT{'lastModified'}=$^T;
    return\%DT;
}


#-------------------------------------------------

=head2 Cookie�񤭹���

=head3 ����

\% Cookie�˽񤭹������Ƥ���ĥϥå���Υ�ե���󥹡�name��time����Ĥ��ȡ�

=cut

sub setCookie{
    my%DT=%{shift()};
    $DT{'name'}||$DT{'time'}||return undef;
    unless($DT{'lastModified'}){
	#������Cookie�����%DT
	&getCookie unless%CK;
	$DT{$_}=$CK{$_}for grep{!exists$DT{$_}}keys%CK;
    }
    my$setCookie='';
    my$expires=$^T+33554432; #33554432=2<<24; #33554432�Ȥ����������ä˰�̣�Ϥʤ������ʤߤ˰�ǯ�Ⱦ���
    $DT{'time'}||=$^T;
    if($CF{'ckpath'}){
	my$cookie='';
	for("lastModified time expire"=~/(\w+)/go){
	    $cookie.=sprintf"%s\t%s\t",$_,defined$DT{$_}?$DT{$_}:'';
	}
	$cookie=~s/(\W)/'%'.unpack('H2',$1)/ego;
	$setCookie.=sprintf'Mireille=%s; expires=%s',$cookie,&datef($expires,'cookie');
	$setCookie.="\n";
	for("lastModified name pass $CF{'cokitm'}"=~/(\w+)/go){
	    $cookie.=sprintf"%s\t%s\t",$_,defined$DT{$_}?$DT{$_}:'';
	}
	$cookie=~s/(\W)/'%'.unpack('H2',$1)/ego;
	$setCookie.=sprintf'Mireille=%s; expires=%s; %s',$cookie,&datef($expires,'cookie'),$CF{'ckpath'};
    }else{
	for("lastModified time expire name pass $CF{'cokitm'}"=~/(\w+)/go){
	    $cookie.=sprintf"%s\t%s\t",$_,defined$DT{$_}?$DT{$_}:'';
	}
	$cookie=~s/(\W)/'%'.unpack('H2',$1)/ego;
	$setCookie.=sprintf'Mireille=%s; expires=%s',$cookie,&datef($expires,'cookie');
    }
    if(!defined$CF{'set_cookie_by_meta_tags'}&&index($ENV{'SERVER_NAME'},'tok2.com')+1){
	#tok2�к�
	$CF{'set_cookie_by_meta_tags'}=1;
	$CF{'-setCookie'}=$setCookie;
    }else{
	print"Set-Cookie: $_\n"for split("\n",$setCookie);
    }
    return$setCookie;
}


#-------------------------------------------------

=head2 �ե����ޥåȤ��줿���ռ������֤�

=head3 ����

  $ time�����λ���
  ;
  $ ���Ϸ���(cookie|last|dateTime)
  $ ������$CF{'timeOffset'}��Ʊ��������

=cut

sub datef{
    my$time=shift;
    my$type=shift;
    gmtime$time||return 0;
    unless($type){
    }elsif('cookie'eq$type){
	# Netscape��Cookie��
	return sprintf("%s, %02d-%s-%d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
    }elsif('rfc1123'eq$type){
	# RFC1123 'Thu, 01 Jan 1970 00:00:00 GMT'
	return sprintf("%s, %02d %s %d %s GMT",(split(/\s+/o,gmtime$time))[0,2,1,4,3]);
    }elsif('dateTime'eq$type){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
	my$timeOffset=@_?shift:$CF{'timeOffset'}||&cfgTimeZone($ENV{'TZ'});
	my($sec,$min,$hour,$day,$mon,$year,$wday)=gmtime($time+$timeOffset)or return 0;
	return sprintf"%04d-%02d-%02dT%02d:%02d:%02d%s",$year+1900,$mon+1,$day,$hour,$min,$sec,
	$timeOffset?sprintf'%s%02d:%02d',($timeOffset>0?'+':'-'),$timeOffset/3600,$timeOffset%3600/60:'Z';
    }
    return&date($time);
}


#-------------------------------------------------

=head2 �����ॾ����μ���

�����ॾ�����Ķ��ѿ�TZ����������ơ�%CF�����ꤹ��
¾�δؿ��Ϥ���$CF{'timezone'},$CF{'timeOffset'}��Ȥäơ�
gmtime()����μ¤˴�˾���ϰ�λ���򻻽ФǤ���

=head3 ����

$ $ENV{'TZ'}

=cut

sub cfgTimeZone{
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

=head2 ���դ����

=head3 Arguments

  $ ����

=head3 Return Value

  $jd,$year,$mon,$day,$hour,$min,$sec,$unix

=head3 �б����շ���

RFC1123, ANSI C����, ISO9601 dateTime

=head3 See Also

=over

=item RFC1123���������դ����

  http://www.faireal.net/articles/3/16/

=back

=cut

sub parse_date{
    my$date=shift();
    my($day,$mon,$year,$hour,$min,$sec);
    my$months='(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)';
    my%month=qw(Jan 1 Feb 2 Mar 3 Apr 4 May 5 Jun 6 Jul 7 Aug 8 Sep 9 Oct 10 Nov 11 Dec 12);
    if($date=~/\w+,?\s*(\d+)(?:-|\s+)($months)(?:-|\s+)(\d+) (\d+):(\d+):(\d+)\s*GMT/o){
	# RFC1123 'Thu, 01 Jan 1970 00:00:00 GMT'
	($year,$mon,$day,$hour,$min,$sec)=map{int}($3,$month{$2},$1,$4,$5,$6);
    }elsif($date=~/\w+\s+($months)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)/o){
	#gmtime() 'Thu Jan  1 00:00:00 1970'
	($year,$mon,$day,$hour,$min,$sec)=map{int}($6,$month{$1},$2,$3,$4,$5);
    }elsif($date=~/(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:Z|([-+])(\d{2})(?::(\d{2})))?/o){
	# ISO 8601 dateTime (CCYY-MM-DDThh:mm:ss+09:00)
	($year,$mon,$day,$hour,$min,$sec)=map{int}($1,$2,$3,$4,$5,$6);
	'+'eq$7?($hour-=$8,$9 and$min-=$9):($hour+=$8,$9 and$min+=$9)if$7&&$8;
    }else{
	return 0;
    }
    $mon||return 0;
    my($_Y,$_M,$_day)=($year,$mon,$hour/24+$min/1440+$sec/86400);
    if($mon<3){
	$_Y-=1;
	$_M+=12;
    }
    my$jd=int(365.25*($_Y+4716))+int(30.6001*($_M+1))+2-int($_Y/100)+int($_Y/400)+$day+$_day-1524.5;
    my$unix=((int($jd-$_day-2440587.5)*24+$hour)*60+$min)*60+$sec;
    return$jd,$year,$mon,$day,$hour,$min,$sec,$unix;
}


#-------------------------------------------------

=head2 �ѥ���ɰŹ沽

=head3 ����

  $ ����μ��time���������
  $ �Ź沽����ʸ����
  ;
  $ ��٤�ѥ����

=cut

sub mircrypt{
    srand($_[0]);
    my$salt=join('',('a'..'z','.',0..9,'/','A'..'Z')[rand(64),rand(64)]);
    my$pass='';
    for($_[1]=~/.{1,8}/go){
	length$_||next;
	$pass.=substr(crypt($_,$salt),2);
    }
    return defined$_[2]?($_[2]&&$_[2]eq$pass?1:undef):$pass;
}


# ------------------------------------------ #

=head2 CRC32���������

based on 2000/06/26 crc32.pl 1.1.0 digiz

=head3 ����

  $ CRC32��Ȥꤿ��ʸ����
  ;
  $ 32bit��10�ʿ����ߤ������˿���

=cut

my@crc32;
sub getCRC32{
    @crc32=map{my$a=$_;$a=$a&1?($a>>1&0x7fffffff)^0xedb88320:$a>>1&0x7fffffff for 0..7;$a}0..255unless@crc32;
    my$word=shift;
    my$r=0xffffffff;
    $r=$r>>8&0xffffff^$crc32[$r&255^$_]for unpack"C*",$word;
    $r^=0xffffffff;
    return@_?$r:sprintf('%08X',$r);
}


#-------------------------------------------------
# ��̾������
#
sub getSignature{
    my$word=shift;
    my$canUseSpecial=shift()&&$CF{'signatureSpecial'};
    my$signature;
    if($canUseSpecial&&$CF{'signatureSpecial'}=~/(?:^|\s+)\Q$word\E\s+(\S+)/o){
	$signature='!'.$1;
    }else{
	my@salt=('.','/',0..9,'A'..'Z','a'..'z');
	my$salt=join'',map{$salt[(ord chop$word)%64]}0,1;
	$signature=&getCRC32(substr(crypt(&getCRC32($word),$salt),2));
    }
    return$signature;
}


#-------------------------------------------------
# ��̾��������ɽ������
#
my%signatureCacheView;
sub getSignatureView{
    my$data=shift;
    my$signature;
    if($data->{signature}=~/!(.+)/o){
	#�ü��̾
	$signature=$1;
    }elsif($signatureCacheView{$data->{signature}.' '.$data->{name}}){
	#����å���
	$signature=$signatureCacheView{$data->{signature}.' '.$data->{name}};
    }else{
	unless($Z0{'Serial'}){
	    srand();
	    $Z0{'Serial'}=1+int(rand(-2+2**32));
	}
	srand($Z0{'Serial'}^&getCRC32($data->{name},1));
	my@salt=('.','/',0..9,'A'..'Z','a'..'z');
	my$saltForSignatureView=join'',map{$salt[rand 64]}0,1;
	$signature=substr(crypt($data->{signature},$saltForSignatureView),2);
	$signatureCacheView{$data->{signature}.' '.$data->{name}}=$signature;
    }
    return$signature;
}


#-------------------------------------------------

=head2 ���������Ѥ�IMG����

=head3 ����

  $ ������������ä��ϥå���ؤΥ�ե����
  ;
  $ �ɤΤ褦�ʷ����֤���������

=head3 �֤�������

��-!keyword!-�פΤ褦�ʷ����Ǥ�
����Ū�ˤϰʲ��ΤȤ���

=over

=item -!src!-

�ǥ��쥯�ȥ�̾+�ե�����̾��IMGsrc����

=item -!dir!-

�ǥ��쥯�ȥ�̾

=item -!file!-

�ե�����̾

=back

=cut

sub getIconTag{
    my$data=shift;
    my$text=shift||'<IMG src="-!src!-" alt="" title="-!dir!-+-!file!-">';
    my%DT=(dir=>$CF{'icon'},file=>$data->{'icon'});
    if($CF{'absoluteIcon'}&&$data->{'cmd'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
	#���л��ꥢ������
	$DT{'dir'}='';
	$DT{'file'}||=$1;
    }elsif($CF{'relativeIcon'}&&$data->{'cmd'}=~/(?:^|;)relativeIcon=([^;:.]*(?:\.[^;:.]+)*)/o){
	#���л��ꥢ������
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

=head2 ��������ꥹ��

=head3 ����

  $ �ǥե���Ȼ���ˤ�������������ե�����̾�����줿�񤭴�����ǽ���ѿ�
  ;
  $ SELECT�������ɲä�����°��
  $ ��ĥ���ޥ��

=head3 ʣ����������ꥹ��

$CF{'icls'}�κǽ�ΰ�ʸ����' '��Ⱦ�Ѷ���ˤ��ä����ʣ���ꥹ�ȥ⡼�ɤˤʤ�ޤ���
����Ū�����Ф��ȡ�

=over

=item ñ��Ȥߤʤ������

  'icon.txt'
  'icon1.txt icon2.txt' #=> "icon1.txt icon2"�Ȥ����ƥ����ȥե�������Ȥߤʤ��ޤ�
  '"icon.txt" "exicon.txt"'

=item ʣ���Ȥߤʤ������

  ' "icon.txt" "exicon.txt"'
  ' "icon.txt" exicon.txt'
  ' icon.txt exicon.txt'

=back

=cut

sub iptico{
    my$opt=$_[1]?" $_[1]":'';
    if($CF{'-CacheIconList'}&&('reset'ne$_[2])){
	#����å���Ǥ���$CF{'-CacheIconList'}���֤�
	return$CF{'-CacheIconList'};
    }
	
    #��������ꥹ���ɤ߹���
    my$iconlist='';
    if($CK{'cmd'}=~/\biconlist=nolist(;|$)/o){
	#`icon=nolist`�ǥ�������ꥹ�Ȥ��ɤ߹��ޤʤ�
    }elsif($CF{'icls'}=~/^ /o){
	#ʣ����������ꥹ���ɤ߹���
	for($CF{'icls'}=~/("[^"\\]*(?:\\.[^"\\]*)*"|\S+)/go){
	    $_||next;
	    my$tmp;
	    open(FILE,'<'.$_)||die"Can't open multi-iconlist($_).";
	    eval{flock(FILE,1)};
	    read(FILE,$tmp,-s$_);
	    close(FILE);
	    $iconlist.=$tmp;
	}
    }else{
	#ñ�쥢������ꥹ���ɤ߹���
	open(FILE,'<'.$CF{'icls'})||die"Can't open single-iconlist.";
	eval{flock(FILE,1)};
	read(FILE,$iconlist,-s$CF{'icls'});
	close(FILE);
    }
	
    #���򥢥�����η����SELECT���������
    my$isEconomy=$CK{'cmd'}=~/(?:^|;)iconlist=economy(?:\s*;|$)/o;
    my$isAbsolute=0;
    my$isDisabled='';
    unless(@_){
    }elsif($CF{'exicon'}&&($CK{'cmd'}=~/(?:^|;)icon=([^;]*)/o)&&$IC{$1}){
	#�ѥ���ɷ�
	$_[0]=$IC{$1};
	if($isEconomy){
	    $iconlist=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}else{
	    $iconlist.=qq(<OPTION value="$_[0]" selected>���ѥ�������</OPTION>\n);
	}
    }elsif($CF{'absoluteIcon'}&&$CK{'cmd'}=~/(?:^|;)absoluteIcon=([^;]*)/o){
	#���л��ꥢ������
	$_[0]=$1;
	$isAbsolute=1;
	$isDisabled=1;
	$iconlist=qq(<OPTION value="$_[0]" selected>���л���</OPTION>\n)if$isEconomy;
    }elsif($CF{'relativeIcon'}&&$CK{'cmd'}=~/(?:^|;)relativeIcon=([^;:.]*(\.[^;:.]+)*)/o){
	#���л��ꥢ������
	$_[0]=$1;
	$iconlist=qq(<OPTION value="$1" selected>���л���</OPTION>\n)if$isEconomy;
	$isDisabled=1;
    }elsif($_[0]and$iconlist=~s/^(.*value=(["'])$_[0]\2)(.*)$/$1 selected$3/imo){
	$iconlist="$1 selected$3"if$isEconomy;
	#	}elsif($_[0]and$canUseUnlistedCookieIcon){
	#		#Cookie����¸���줤�륢�����󤬥�������ꥹ�Ȥ�̵���Ȥ�
	#		$iconlist=($isEconomy?$iconlist:'').qq(<OPTION value="$_[0]" selected>COOKIE</OPTION>\n);
    }elsif($iconlist=~s/value=(["'])(.*?)\1/value=$1$2$1 selected/io){
	$_[0]=$2;
    }
    $_[0]=$CF{'icon'}.$_[0]unless$isAbsolute;
    $isDisabled&&=' disabled';
    $CF{'-CacheIconList'}=<<"_HTML_";
<SELECT name="icon" id="icon" onchange="document.images['Preview'].src='$CF{'icon'}'+this.value;document.images['Preview'].title='$CF{'icon'}'+'+'+this.value;oPreview.style.visibility=oIcon.value?'visible':'hidden';"$opt$isDisabled>
$iconlist</SELECT>
_HTML_
    return$CF{'-CacheIconList'};
}


#-------------------------------------------------

=head2 ���顼�ꥹ���ɤ߹���

=head3 ����

  $ �ǥե���Ȼ���ˤ�������̾

=cut

sub iptcol{
    if('input'eq$CF{'colway'}){
	return<<"_HTML_";
<INPUT type="text" name="color" id="color" maxlength="20" style="ime-mode:disabled"
 title="Color&#10;��ʸ�ο������Ϥ��ޤ�&#10;��#0f0��#00ff00��rgb(0,255,0)��WebColor(green�Ȥ�)&#10;�Τɤη����Ǥ�Ȥ��ޤ�" value="$_[0]">
_HTML_
    }else{
	my$list=$CF{'colorList'}=~/\S/o?$CF{'colorList'}:<<"_HTML_";#1.2.5�ʲ��Ȥθߴ����Τ���
<OPTION value="#000000" style="color:#000000">��Black</OPTION>
<OPTION value="#696969" style="color:#696969">��DimGray</OPTION>
<OPTION value="#808080" style="color:#808080">��Gray</OPTION>
<OPTION value="#A9A9A9" style="color:#A9A9A9">��DarkGray</OPTION>
<OPTION value="#C0C0C0" style="color:#C0C0C0">��Silver</OPTION>
<OPTION value="#D3D3D3" style="color:#D3D3D3">��LightGrey</OPTION>
<OPTION value="#D8BFD8" style="color:#D8BFD8">��Thistle</OPTION>
<OPTION value="#DCDCDC" style="color:#DCDCDC">��Gainsboro</OPTION>
<OPTION value="#F5F5DC" style="color:#F5F5DC">��Beige</OPTION>
<OPTION value="#F5F5F5" style="color:#F5F5F5">��WhiteSmoke</OPTION>
<OPTION value="#E6E6FA" style="color:#E6E6FA">��Lavender</OPTION>
<OPTION value="#FAF0E6" style="color:#FAF0E6">��Linen</OPTION>
<OPTION value="#FDF5E6" style="color:#FDF5E6">��Oldlace</OPTION>
<OPTION value="#FFE4E1" style="color:#FFE4E1">��Mistyrose</OPTION>
<OPTION value="#F0FFF0" style="color:#F0FFF0">��Honeydew</OPTION>
<OPTION value="#FFF5EE" style="color:#FFF5EE">��Seashell</OPTION>
<OPTION value="#FFF0F5" style="color:#FFF0F5">��LavenderBlush</OPTION>
<OPTION value="#F0F8FF" style="color:#F0F8FF">��AliceBlue</OPTION>
<OPTION value="#F8F8FF" style="color:#F8F8FF">��GhostWhite</OPTION>
<OPTION value="#FFFAF0" style="color:#FFFAF0">��FloralWhite</OPTION>
<OPTION value="#F5FFFA" style="color:#F5FFFA">��Mintcream</OPTION>
<OPTION value="#FFFAFA" style="color:#FFFAFA">��Snow</OPTION>
<OPTION value="#FFFFE0" style="color:#FFFFE0">��LightYellow</OPTION>
<OPTION value="#E0FFFF" style="color:#E0FFFF">��LightCyan</OPTION>
<OPTION value="#FFFFF0" style="color:#FFFFF0">��Ivory</OPTION>
<OPTION value="#F0FFFF" style="color:#F0FFFF">��Azure</OPTION>
<OPTION value="#FFFFFF" style="color:#FFFFFF">��White</OPTION>
<OPTION value="#9370DB" style="color:#9370DB">��MediumPurple</OPTION>
<OPTION value="#6A5ACD" style="color:#6A5ACD">��SlateBlue</OPTION>
<OPTION value="#483D8B" style="color:#483D8B">��DarkSlateBlue</OPTION>
<OPTION value="#7B68EE" style="color:#7B68EE">��MediumSlateBlue</OPTION>
<OPTION value="#BA55D3" style="color:#BA55D3">��MediumOrchid</OPTION>
<OPTION value="#9932CC" style="color:#9932CC">��DarkOrchid</OPTION>
<OPTION value="#8A2BE2" style="color:#8A2BE2">��BlueViolet</OPTION>
<OPTION value="#9400D3" style="color:#9400D3">��DarkViolet</OPTION>
<OPTION value="#4B0082" style="color:#4B0082">��Indigo</OPTION>
<OPTION value="#000080" style="color:#000080">��Navy</OPTION>
<OPTION value="#00008B" style="color:#00008B">��DarkBlue</OPTION>
<OPTION value="#0000CD" style="color:#0000CD">��MediumBlue</OPTION>
<OPTION value="#0000FF" style="color:#0000FF">��Blue</OPTION>
<OPTION value="#191970" style="color:#191970">��MidnightBlue</OPTION>
<OPTION value="#00BFFF" style="color:#00BFFF">��DeepSkyBlue</OPTION>
<OPTION value="#00CED1" style="color:#00CED1">��DarkTurquoise</OPTION>
<OPTION value="#1E90FF" style="color:#1E90FF">��DodgerBlue</OPTION>
<OPTION value="#4169E1" style="color:#4169E1">��RoyalBlue</OPTION>
<OPTION value="#4682B4" style="color:#4682B4">��SteelBlue</OPTION>
<OPTION value="#6495ED" style="color:#6495ED">��CornflowerBlue</OPTION>
<OPTION value="#87CEFA" style="color:#87CEFA">��LightSkyblue</OPTION>
<OPTION value="#5F9EA0" style="color:#5F9EA0">��CadetBlue</OPTION>
<OPTION value="#87CEEB" style="color:#87CEEB">��SkyBlue</OPTION>
<OPTION value="#B0E0E6" style="color:#B0E0E6">��PowderBlue</OPTION>
<OPTION value="#ADD8E6" style="color:#ADD8E6">��LightBlue</OPTION>
<OPTION value="#708090" style="color:#708090">��SlateGray</OPTION>
<OPTION value="#778899" style="color:#778899">��LightSlateGray</OPTION>
<OPTION value="#B0C4DE" style="color:#B0C4DE">��LightSteelBlue</OPTION>
<OPTION value="#008080" style="color:#008080">��Teal</OPTION>
<OPTION value="#008B8B" style="color:#008B8B">��DarkCyan</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Aqua</OPTION>
<OPTION value="#00FFFF" style="color:#00FFFF">��Cyan</OPTION>
<OPTION value="#2F4F4F" style="color:#2F4F4F">��DarkSlateGray</OPTION>
<OPTION value="#AFEEEE" style="color:#AFEEEE">��PaleTurquoise</OPTION>
<OPTION value="#7FFFD4" style="color:#7FFFD4">��Aquamarine</OPTION>
<OPTION value="#66CDAA" style="color:#66CDAA">��MediumAquamarine</OPTION>
<OPTION value="#3CB371" style="color:#3CB371">��MediumSeagreen</OPTION>
<OPTION value="#2E8B57" style="color:#2E8B57">��SeaGreen</OPTION>
<OPTION value="#48D1CC" style="color:#48D1CC">��MediumTurquoise</OPTION>
<OPTION value="#40E0D0" style="color:#40E0D0">��Turquoise</OPTION>
<OPTION value="#20B2AA" style="color:#20B2AA">��LightSeagreen</OPTION>
<OPTION value="#00FA9A" style="color:#00FA9A">��MediumSpringGreen</OPTION>
<OPTION value="#00FF7F" style="color:#00FF7F">��SpringGreen</OPTION>
<OPTION value="#006400" style="color:#006400">��DarkGreen</OPTION>
<OPTION value="#008000" style="color:#008000">��Green</OPTION>
<OPTION value="#00FF00" style="color:#00FF00">��Lime</OPTION>
<OPTION value="#32CD32" style="color:#32CD32">��LimeGreen</OPTION>
<OPTION value="#228B22" style="color:#228B22">��ForestGreen</OPTION>
<OPTION value="#90EE90" style="color:#90EE90">��LightGreen</OPTION>
<OPTION value="#98FB98" style="color:#98FB98">��PaleGreen</OPTION>
<OPTION value="#7CFC00" style="color:#7CFC00">��LawnGreen</OPTION>
<OPTION value="#7FFF00" style="color:#7FFF00">��Chartreuse</OPTION>
<OPTION value="#ADFF2F" style="color:#ADFF2F">��GreenYellow</OPTION>
<OPTION value="#9ACD32" style="color:#9ACD32">��YellowGreen</OPTION>
<OPTION value="#6B8E23" style="color:#6B8E23">��Olivedrab</OPTION>
<OPTION value="#556B2F" style="color:#556B2F">��DarkOlivegreen</OPTION>
<OPTION value="#8FBC8B" style="color:#8FBC8B">��DarkSeaGreen</OPTION>
<OPTION value="#808000" style="color:#808000">��Olive</OPTION>
<OPTION value="#FFFF00" style="color:#FFFF00">��Yellow</OPTION>
<OPTION value="#FAFAD2" style="color:#FAFAD2">��LightGoldenrodYellow</OPTION>
<OPTION value="#FAEBD7" style="color:#FAEBD7">��AntiqueWhite</OPTION>
<OPTION value="#FFF8DC" style="color:#FFF8DC">��Cornsilk</OPTION>
<OPTION value="#FFEFD5" style="color:#FFEFD5">��PapayaWhip</OPTION>
<OPTION value="#FFEBCD" style="color:#FFEBCD">��BlanchedAlmond</OPTION>
<OPTION value="#FFFACD" style="color:#FFFACD">��LemonChiffon</OPTION>
<OPTION value="#FFE4C4" style="color:#FFE4C4">��Bisque</OPTION>
<OPTION value="#FFDAB9" style="color:#FFDAB9">��PeachPuff</OPTION>
<OPTION value="#F5DEB3" style="color:#F5DEB3">��Wheat</OPTION>
<OPTION value="#FFE4B5" style="color:#FFE4B5">��Moccasin</OPTION>
<OPTION value="#FFDEAD" style="color:#FFDEAD">��NavajoWhite</OPTION>
<OPTION value="#EEE8AA" style="color:#EEE8AA">��PaleGoldenrod</OPTION>
<OPTION value="#D2B48C" style="color:#D2B48C">��Tan</OPTION>
<OPTION value="#DEB887" style="color:#DEB887">��Burlywood</OPTION>
<OPTION value="#E9967A" style="color:#E9967A">��DarkSalmon</OPTION>
<OPTION value="#FA8072" style="color:#FA8072">��Salmon</OPTION>
<OPTION value="#F0E68C" style="color:#F0E68C">��Khaki</OPTION>
<OPTION value="#FFA07A" style="color:#FFA07A">��LightSalmon</OPTION>
<OPTION value="#BDB76B" style="color:#BDB76B">��DarkKhaki</OPTION>
<OPTION value="#F4A460" style="color:#F4A460">��SandyBrown</OPTION>
<OPTION value="#FF7F50" style="color:#FF7F50">��Coral</OPTION>
<OPTION value="#FF6347" style="color:#FF6347">��Tomato</OPTION>
<OPTION value="#CD853F" style="color:#CD853F">��Peru</OPTION>
<OPTION value="#A0522D" style="color:#A0522D">��Sienna</OPTION>
<OPTION value="#D2691E" style="color:#D2691E">��Chocolate</OPTION>
<OPTION value="#8B4513" style="color:#8B4513">��SaddleBrown</OPTION>
<OPTION value="#DAA520" style="color:#DAA520">��Goldenrod</OPTION>
<OPTION value="#B8860B" style="color:#B8860B">��DarkGoldenrod</OPTION>
<OPTION value="#FFD700" style="color:#FFD700">��Gold</OPTION>
<OPTION value="#FFA500" style="color:#FFA500">��Orange</OPTION>
<OPTION value="#FF8C00" style="color:#FF8C00">��DarkOrange</OPTION>
<OPTION value="#FF4500" style="color:#FF4500">��OrangeRed</OPTION>
<OPTION value="#800000" style="color:#800000">��Maroon</OPTION>
<OPTION value="#8B0000" style="color:#8B0000">��DarkRed</OPTION>
<OPTION value="#FF0000" style="color:#FF0000">��Red</OPTION>
<OPTION value="#B22222" style="color:#B22222">��Firebrick</OPTION>
<OPTION value="#A52A2A" style="color:#A52A2A">��Brown</OPTION>
<OPTION value="#CD5C5C" style="color:#CD5C5C">��IndianRed</OPTION>
<OPTION value="#F08080" style="color:#F08080">��LightCoral</OPTION>
<OPTION value="#BC8F8F" style="color:#BC8F8F">��RosyBrown</OPTION>
<OPTION value="#FF1493" style="color:#FF1493">��DeepPink</OPTION>
<OPTION value="#C71585" style="color:#C71585">��MediumVioletRed</OPTION>
<OPTION value="#DC143C" style="color:#DC143C">��Crimson</OPTION>
<OPTION value="#FF69B4" style="color:#FF69B4">��HotPink</OPTION>
<OPTION value="#DA70D6" style="color:#DA70D6">��Orchid</OPTION>
<OPTION value="#DB7093" style="color:#DB7093">��PaleVioletred</OPTION>
<OPTION value="#FFB6C1" style="color:#FFB6C1">��LightPink</OPTION>
<OPTION value="#FFC0CB" style="color:#FFC0CB">��Pink</OPTION>
<OPTION value="#800080" style="color:#800080">��Purple</OPTION>
<OPTION value="#8B008B" style="color:#8B008B">��DarkMagenta</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Fuchsia</OPTION>
<OPTION value="#FF00FF" style="color:#FF00FF">��Magenta</OPTION>
<OPTION value="#EE82EE" style="color:#EE82EE">��Violet</OPTION>
<OPTION value="#DDA0DD" style="color:#DDA0DD">��Plum</OPTION>
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

=head2 ��������åɥե�������

=head3 ����

  $ �������
  @ �������ե�����ε�������å��ֹ�Υꥹ��

=cut

sub delThread{
    my($type,@del)=@_;
    my$file=0;
    if('gzip'eq$type&&$CF{'gzip'}){
	#GZIP����
	for(@del){
	    $_||next;
	    `$CF{'gzip'} -fq9 "$CF{'log'}$_.cgi"`;
	    ($?==0)||die"$?:Can't use gzip($CF{'gzip'}) oldlog($_.cgi)[$?:$!]";
	    $file++;
	}
    }elsif('unlink'eq$type){
	#���
	for(@del){
	    $_||next;
	    unlink"$CF{'log'}$_.cgi"||die"Can't delete oldlog($_.cgi)[$?:$!]";
	    $file++;
	}
    }elsif('rename'eq$type){
	#�ե�����̾�ѹ�
	for(@del){
	    $_||next;
	    if(-e"$CF{'log'}$_.bak.cgi"){
		#���礦���ʤ�����Ť��ΤϺ�������㤦
		unlink"$CF{'log'}$_.bak.cgi"||die"Can't unlink old-old log($CF{'log'}$_.bak.cgi)[$?:$!]";
	    }
	    rename("$CF{'log'}$_.cgi","$CF{'log'}$_.bak.cgi")||die"Can't rename oldlog($_.cgi)[$?:$!]";
	    $file++;
	}
    }elsif($type=~/!(.*)/o){
	#�ü�
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

=head2 �����Խ����

=head3 ��ư�ǤĤ���������ä�

����Ȥ��ơ������Ȥ��ƻȤ���ʳ���'<','>'��¸�ߤ��ƤϤʤ�ޤ���
���˽񤭹��ޤ�������°�����<>��&#60;&#62;�ˤʤäƤ��뤳�ȤȤ��ޤ���

�ޤ������λ�����¸�ߤ��륿���ϡ�

=over

=item 1. ���ѼԤ����Ϥ�������

$CF{'tag'}�ǵ��Ĥ��줿������

=item 2. ��ư��󥯤ˤ�륿��

C<< /<A class="autolink"[^>]*>/ >>�˥ޥå�������

=item 3. �����ֹ��󥯤ˤ�륿��

C<< /<A class="autolink"[^>]*>/ >>

=item 4. ��綯Ĵ�ˤ�륿��

C<< /<STRONG  clAss="[^"]*"[^>]*>/ >>

=back

���Τ�����1.��["'<>]�򥨥������פ���2.��3.�� 4.�Ϻ�����ޤ���

�ޤ�2.��3.�ˤĤ��ƤϺ���˺ݤ��ưʲ����ꤷ�ޤ���

=over

=item A���������Ƥˤ�[<>]����ʤ�

=item ��ư���1���åȤ�ɬ��C<< /<A class="autolink" [^>]*>([^<]+)<\/A>/ >>�˥ޥå�����

=item ��󥯤����оݤ�C<&>�򥨥������פ����ݤ�C<&#38;>�ǥ��������פ���

=back

���餫�η��Ǥ��β��꤬���줿��硢���������ʤ����Ȥ䡢������������Ǥ��ʤ���ǽ��������ޤ���

=cut

sub rvsij{
    #�ǡ������᤹
    $CK{'body'}=~s/<BR\b[^>]*>/\n/gio;
    $CK{'body'}=~s/&nbsp;/ /go;
    $CK{'body'}=~s/&/&#38;/go;

    #data->form�Ѵ�
    if('ALLALL'eq$CF{'tags'}){
    }else{
	my$str=$CK{'body'};
	#�����ֹ��󥯡�>>No.12-6��
	$str=~s{<A class="autolink"[^>]*>&#38;#62;&#38;#62;(No\.(\d+)(-\d+)?)</A>}{&#62;&#62;$1}go;
	#A����
	$str=~s{<A class="autolink" [^>]*>([^<]+)</A>}{my$tmp=$1;$tmp=~s/&#38;#38;/&#38;/g;$tmp}ego;
		
	{ #STRONG����
	    my@floor;
	    $str=~s{(<(\/?)STRONG\b([^>]*)>)}
	    {
		if(!$2){ #��������
		    if($3=~/^\s+cl[aA]ss="[^"]*"(?:\x20\x20)?$/o){push(@floor,1);'';}
		    else{push(@floor,0);$1;}
		}else{ #�Ĥ�����
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
    #�ҵ������Ƶ���
    '0'eq$CK{'j'}?&prtfrm:&chdfrm;
}



#-----------------------------------------------------------------
# String Class
#
{package MirString;
    my$char;
    my$eucpre;
    my$eucpost;
    if($::CF{'encoding'}=~/euc(?:-jp)?/io){
	# EUC-JPʸ��
	$char=qr((?:
			[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� EUC-JPʸ����
			|(?:[\x8E\xA1-\xFE][\xA1-\xFE])	# 2�Х��� EUC-JPʸ��
			|(?:\x8F[\xA1-\xFE]{2})			# 3�Х��� EUC-JPʸ��
		))x;
	#�������ѥ�����ޥå�������
	$eucpre=qr{(?<!\x8F)};
	$eucpost=qr{(?=
			(?:[\xA1-\xFE][\xA1-\xFE])*	# JIS X 0208 �� 0ʸ���ʾ�³����
			(?:[\x00-\x7F\x8E\x8F]|\z)	# ASCII, SS2, SS3 �ޤ��Ͻ�ü
		)}x;
    }elsif($::CF{'encoding'}=~/utf-?8/io){
	# UTF-8ʸ��
	$char=qr((?:
			[\x09\x0A\x0D\x20-\x7E]			# 1�Х��� UTF-8 ʸ��
			|(?:[\xC2-\xDF][\x80-\xBF])		# 2�Х��� UTF-8 ʸ��
			|(?:[\xE0-\xEF][\x80-\xBF]{2})	# 3�Х��� UTF-8 ʸ��
			|(?:[\xF0-\xF7][\x80-\xBF]{3})	# 4�Х��� UTF-8 ʸ��
			|(?:[\xF8-\xFB][\x80-\xBF]{4})	# 5�Х��� UTF-8 ʸ��
			|(?:[\xFD-\xFE][\x80-\xBF]{5})	# 6�Х��� UTF-8 ʸ��
		))x;
    }else{
	#use encoding���Ȥ���
	$char=qr([\W\w]);
    }
    # �������ޥå�������
    sub match{
	my$class=shift;
	my$str=shift;
	my$regex=shift;
	if($eucpre){
	    return$str=~/$eucpre$regex$eucpost/?1:0;
	}else{
	    return index($str,$regex)+1?1:0;
	}
    }
    # Mireille������key=value�򸡺�
    sub matchedItem{
	my$class=shift;
	my$str=shift;
	my$item=shift;
	my$seek=shift;
	if($eucpre){
	    return$str=~/$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t/?1:0;
	}else{
	    return$str=~/$item=\t[^\t]*$seek[^\t]*;\t/?1:0;
	}
    }
    # Mireille������key=value�򸡺����ƥꥹ�Ȥ��֤�
    sub matchedItems{
	my$class=shift;
	my$str=shift;
	my$item=shift;
	my$seek=shift;
	my$j=0;
	if($eucpre){
	    return map{$j+=tr/\n//}$str=~/(\G.*?$item=\t[^\t]*$eucpre$seek$eucpost[^\t]*;\t)/gs;
	}else{
	    return map{$j+=tr/\n//}$str=~/(\G.*?$item=\t[^\t]*$seek[^\t]*;\t)/gs;
	}
    }
    # ���Υ��󥳡��ɤ�������ʸ��������
    sub getValidString{
	my$class=shift;
	@_||die'Not enough arguments for MirString::getValidString';
	return shift=~/($char+)/?$1:'';
    }
    # ���Υ��󥳡��ɤ�������ʸ����ɽ������ɽ�������
    sub getCharRegexp{
	my$class=shift;
	return$char;
    }
    #-------------------------------------------------

=head2 ʸ��������������ʸ�����Ĺ�����ڤ�ͤ��

=head3 ����

  $ $str
  $ ʸ��������

=cut

    sub getTruncated{
	my$class=shift;
	my$str=shift;
	my$length=shift;
		
	$str=~/^\s*(\S.*?)\s*$/mo;
	($str=$1)=~s/<[^>]*>?//go;
	$str=~tr/\x09\x0A\x0D<>/\x20/s;
		
	if(length$str>$length){
	    #ʸ�����¥����С�
	    $length-=2;
	    $str=~/((?:[\x00-\x7F]{1,2}|$char){0,$length})/;
	    $1=~/([^&]*(?:&#?\w+;[^&]*)*)/o;
	    $str="$1..";
	}
	return$str;
    }
}



#-------------------------------------------------
# �������
#
BEGIN{
    $CF{'index'}||='index.cgi';
    $CF{'encoding'}||='euc-jp';
    $CF{'self'} = sprintf( 'http://%s%s/%s', $ENV{'SERVER_NAME'},
 			  substr($ENV{'SCRIPT_NAME'}, 0, rindex($ENV{'SCRIPT_NAME'},'/')), $CF{'index'});
    # Mireille Error Screen 1.2.2
    unless($CF{'program'}){
	$CF{'program'}=__FILE__;
	$SIG{'__DIE__'}=$ENV{'REQUEST_METHOD'}?sub{
	    index($_[0],'flock')+1 and index($_[0],'unimplemented')+1 and return;
	    print "Status: 200 OK\nContent-Language: ja-JP\nContent-type: text/html; charset=$CF{'encoding'}\n\n"
		. "<HTML>\n<HEAD>\n"
		.qq(<META http-equiv="Content-type" content="text/html; charset=$CF{'encoding'}">\n)
		. "<TITLE>Mireille Error Screen 1.2.2</TITLE>\n"
		. "</HEAD>\n<BODY>\n\n<PRE>\t:: Mireille ::\n   * Error Screen 1.2.2 (o__)o// *\n\n";
	    print "ERROR: $_[0]\n"if@_;
	    printf"%-20.20s : %s\n",$_,$CF{$_} for grep{$CF{$_}}qw(Index Style Core Exte);
	    print "\n";
	    printf"%-20.20s : %s\n",$_,$CF{$_} for grep{$CF{$_}}qw(index log icon icls style);
	    print "\n";
	    printf"%-20.20s : %s\n",$$_[0],$$_[1]
		for([PerlVer=>$]],[PerlPath=>$^X],[BaseTime=>$^T],[OSName=>$^O],[FileName=>$0],[__FILE__=>__FILE__]);
	    print "\n = = = ENVIRONMENTAL VARIABLE = = =\n";
	    printf"%-20.20s : %s\n",$_,$ENV{$_} for grep{$ENV{$_}}
		qw(CONTENT_LENGTH QUERY_STRING REQUEST_METHOD SERVER_NAME HTTP_HOST SCRIPT_NAME OS SERVER_SOFTWARE);
	    print "\n+#      Airemix Mireille     #+\n+#  http://www.airemix.com/  #+\n</PRE>\n</BODY>\n</HTML>\n";
	    exit;
	}:sub{
	    index($_[0],'flock')+1 and index($_[0],'unimplemented')+1 and return;
	    print@_?"ERROR: $_[0]":'ERROR';
	    exit;
	};
    }
    $CF{'_HiraganaLetterA'}->{'Core'}='��';
    # Version
    $CF{'Version'}=join('.',q$Mireille: 1_2_13 $=~/\d+[a-z]?/go);
    ($CF{'Core'}=q$Revision$)=~/(\d+((?:\.\d+)*))/o;
    $CF{'CoreRevision'}=$1;
    my$subver=$2;
    if(q$State$!~/^State: (.*) $/o){
    }elsif('Rel'eq$1){
    }elsif('Stab'eq$1){
	$CF{'Version'}.=$subver;
    }elsif('Exp'eq$1){
	$CF{'Version'}.=$subver.'��';
    }else{
	$CF{'Version'}.=$subver;
    }
}
1;
__END__
