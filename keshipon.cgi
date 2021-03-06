#!/usr/local/bin/perl

use utf8;
use strict;
use warnings;
use Encode;

binmode STDOUT => ':utf8';
binmode STDERR => ':utf8';

BEGIN {
	$SIG{__DIE__} = sub {
		return if $^S;

		print "Status: 500 Internal Server Error\n"
		      , "Content-Type: text/plain; charset=UTF-8\n"
		      , "\n";

		local $_;
		($_ = shift) =~ s/[\r\n]*$//;
		print; CORE::die;
	};
}

my $enc = find_encoding('utf8');
my %c;
my $c = 0;
my $line_c = 0;
my %F = get_query();
my $quality = exists $F{q} && $F{q} !~ /\D/ ? $F{q} : 60;
my $over = exists $F{o} ? 1 : 0;
my $ascii = exists $F{a} ? 1 : 0;
my $line = exists $F{l} ? 1 : 0;
my $random = exists $F{r} ? 1 : 0;
my $source = $F{s};
if (!$source) {
	$quality = 20 unless exists $F{q} && $F{q} !~ /\D/;
	$ascii = 1;
	$source = <<"_SOURCE_";
s にソースを、 q に何%ケシポンするかを指定してね
o を指定するとケシポンで上書きするよ
a を指定するとアスキー文字(半角の英数記号だよ)はケシポンしないよ
p に文字列を指定すると好きな文字でケシポンできるよ

l を指定すると順番にケシポン文字を使うよ
r を指定するとランダムにケシポン文字を使うよ
l も r も指定しないとソースの文字ごとに決まった順番でケシポン文字を使うよ

データはUTF-8で送ってね

詳しくはこちら → http://github.com/Uchimata/keshipon/tree/master

_SOURCE_
}
my @pon = $F{p} ? split //, $F{p} : qw(
鷹	麟	鱗	鷺
鑑	鷲
驚	襲	灘	讃	驍
艦	躍	露	顧	魔	鶴	轟	纏
懸	欄	競	籍	議	護	譲	醸	響	鐘	騰	巌	耀	馨	纂
瀬	爆	璽	簿	繰	臓	羅	藻	覇	識	譜	警	霧	離	鏡	韻	願	鶏	鯨	髄	麗	艶	蘭	鯛	鵬	蟹	蹴	蘇	櫓	瀧	麓	寵	曝	瀕	麒
懲	曜	濫	癖	癒	瞬	礎	穫	簡	糧	織	繕	繭	職	臨	藩	襟	覆	観	贈	鎖	鎮	難	額	顔	題	類	顕	翻	騎	験	騒	闘	燿	穣	藍	藤	鎌	雛	鯉	麿	韓	叢	鎧	蹟	鵜	鞭	櫂	儲	禮
償	優	厳	嚇	懇	擬	擦	濯	燥	爵	犠	環	療	矯	礁	縮	績	繊	翼	聴	覧	謙	講	謝	謹	謄	購	轄	醜	鍛	霜	頻	鮮	齢	嶺	曙	檀	燦	瞭	瞳	磯	霞	鞠	駿	鴻	戴	鍋	鍵	闇	燭	藁	篠	濡	瞥	螺	臆	鍬	檎	輿	壕	瓢	曖	檜
儒	凝	壇	墾	壁	壊	壌	奮	嬢	憲	憶	憾	憩	懐	擁	操	整	曇	機	橋	樹	激	濁	濃	燃	獲	獣	磨	積	穏	築	篤	糖	縛	縦	縫	緯	繁	膨	興	薪	薦	薄	薫	薬	融	衡	衛	親	諮	謀	諭	謡	賢	頼	輸	還	避	鋼	錯	錘	錠	録	錬	隣	隷	頭	館	龍	叡	橘	澪	燎	蕗	錦	鮎	黛	錫	錐	醒	膳	謂	憐	燕	蹄	窺	樫	鞘	醍	醐	縞	輯	鋸	薙	諦	鴨	橙	蕾	薗
億	儀	劇	勲	噴	器	嘱	墜	墳	審	寮	導	履	幣	弊	影	徹	憤	慰	慮	慶	憂	戯	撮	撤	摩	撲	撃	敵	敷	暴	暫	標	横	権	槽	歓	潔	潤	澄	潮	潜	潟	熟	熱	盤	確	監	稿	穂	稼	窮	窯	箱	範	縁	緩	線	編	締	緊	縄	罷	膚	舗	舞	蔵	衝	褒	課	請	談	調	論	誕	諸	諾	謁	賓	賜	賠	賦	質	賞	賛	趣	踏	輪	輩	輝	遷	遺	遵	選	鋭	鋳	閲	震	霊	養	餓	駐	魅	黙	凜	嬉	慧	憧	槻	毅	熙	璃	蕉	蝶	誼	諄	諒	遼	醇	駒	黎	撞	蕪	鞍	蕃	稽	魯	磐	畿	廟	劉	蔽	蕎	撫	誰	鋒	播	駈	撒	蝦	蕨	篇	歎	糊	幡	諏	駕	樟	凛
像	僚	僕	境	増	墨	塾	奪	嫡	察	寡	寧	層	彰	徳	徴	慢	態	慕	慣	憎	摘	旗	暮	暦	構	模	概	様	歌	歴	漁	漆	漸	滴	漂	漫	漏	演	漬	獄	疑	磁	碑	種	穀	稲	端	管	箇	算	精	維	綱	網	綿	緑	緒	練	総	罰	聞	腐	膜	複	製	語	誤	誌	誓	説	認	誘	読	豪	踊	遭	適	遮	酵	酷	酸	銀	銃	銑	銅	銘	銭	閣	閥	関	際	障	隠	雑	雌	需	静	領	駆	駅	駄	髪	魂	鳴	鼻	嘉	暢	榛	槙	樺	漱	熊	爾	瑠	瑳	碧	碩	綜	綸	綺	綾	緋	翠	聡	肇	蔦	輔	颯	魁	鳳	遙	窪	閤	槍	鳶	斡	蔭	箔	嶋	綴	裳	蔓	鞄	箕	貌	漕	膏	嘗	頗	竪	蜜	賑	榎	實	榮	槇
催	傑	債	傷	傾	働	僧	勢	勧	嗣	嘆	園	塊	塑	塗	奨	墓	夢	嫁	嫌	寝	寛	幕	幹	廉	微	慎	慨	想	愁	意	愚	愛	感	慈	戦	損	搬	携	搾	摂	数	新	暇	暖	暗	業	楽	棄	楼	歳	殿	源	準	溶	滅	滑	滞	漢	滝	溝	漠	煙	照	煩	献	猿	痴	盟	睡	督	碁	禍	福	禁	禅	稚	節	絹	継	続	罪	置	署	群	義	聖	腹	腰	腸	艇	蒸	蓄	虜	虞	裏	裸	褐	解	触	該	試	詩	詰	話	詳	誇	誠	誉	豊	賃	資	賄	賊	跳	跡	践	路	載	較	辞	農	遠	遣	違	酪	酬	鈴	鉛	鉄	鉱	鉢	隔	雅	零	雷	電	靴	預	頒	頑	飼	飾	飽	塩	鼓	嵩	嵯	暉	椰	椿	楊	楓	楠	滉	瑚	瑞	瑶	睦	禎	稔	稜	舜	蒔	蒼	蓉	蓮	裟	詢	靖	頌	鳩	獅	蓋	鼎	塞	禽	蒲	牒	塙	詮	蜂	葦	蒙	頓	煎	僅	窟	楕	蓑	詫	溜	煤	腎	裾	馴	隙	碗	嘩	蒐	馳	詣	幌	楯	傭	跨	羨	碓	楚	煌	圓	稟
傍	備	偉	傘	割	創	勝	募	勤	博	善	喚	喜	喪	喫	圏	堤	堪	報	堅	場	塔	塁	堕	塀	塚	奥	婿	媒	富	寒	尊	尋	就	属	帽	幅	幾	廃	廊	弾	御	復	循	悲	惑	愉	慌	惰	扉	掌	提	揚	換	握	揮	援	揺	搭	敢	散	敬	晩	普	景	晴	暁	晶	替	暑	最	朝	期	棋	棒	森	棺	植	検	棚	極	棟	欺	款	殖	減	渡	測	港	湖	湯	滋	温	湿	満	湾	渦	焼	無	焦	然	煮	営	猶	琴	番	畳	疎	痘	痛	痢	登	短	硝	硫	硬	税	程	童	筆	等	筋	筒	答	策	粧	結	絶	絡	絞	紫	給	統	絵	着	腕	脹	落	葉	葬	蛮	衆	街	裁	裂	裕	補	装	覚	評	訴	詐	診	詔	詞	詠	証	象	貴	買	貸	費	貯	貿	賀	超	越	距	軸	軽	遂	遇	遊	運	遍	過	道	達	遅	酢	量	鈍	開	間	閑	陽	隊	階	随	隅	雄	集	雇	雲	雰	順	項	飲	飯	歯	凱
);

main();
exit;


sub main {
	my $last_c = $c;
	my @keshipon = keshipon(split(//, $source));
	while (check_quality(length $source)) {
		@keshipon = keshipon(@keshipon);
		last if $last_c == $c;
		$last_c = $c;
	}

	print <<"_HTML_", @keshipon;
Content-Type: text/plain; charset=UTF-8

_HTML_
}

sub keshipon {
	my ($cc, $t, $l) = (0, 0, length($#pon));
	map {
		if (/./ && !$c{++$cc} && check_quality($cc) && int rand(101) <= $quality) {
			$c{$cc} = ++$c;

			$t = hex unpack('H*', $enc->encode($_));
			$_ = $ascii && $t < 128 ? $_ : $over ? do {
				$t = $line ? $line_c++ : substr($t, -$l, $l);
				$t -= $#pon while $t > $#pon;
				$pon[$random ? rand $#pon : $t];
			} : do {
				$random ? do { random($_,$t) } : do {
					my $s = '';
					my $n = 0;
					my $z = 5 - $quality / 25;
					my $a = int(substr($t, -1, 1) / $z)+1;
					my $b = int(substr($t, -2, 1) / $z)+1 || 5-int($a/$z)+1;
					my $p = substr($t, -$l, $l);
					my $q = 0;
					for my $x (-$a .. $b) {
						if ($x == 0) { $s .= $_; next; }
						if ($n > length $t) { $t *= 7; $n = 0; }
						$q = $line ? $x : substr($t, $n++, 1);
						$p += $#pon while $p+$q < $#pon;
						$p -= $#pon while $p+$q > $#pon;
						$s .= $pon[$p+$q];
					}
					$s;
				}
			}
		}

		$_;
	} @_;
}

sub check_quality { $_[0] ? int($c/$_[0]*100)+1 <= $quality : 0 }

sub random {
	my ($s, $t) = @_;
	my $a = int rand $quality/10;
	my $b = int rand $quality/10;
	for my $x (-$a .. $b) {
		$s = $x >= 0 ? $s . $pon[($t+$x <= $#pon ? $t+$x : rand @pon)]
		             : $pon[($t+$x <= $#pon ? $t+$x : rand @pon)] . $s;
	}
	return $s;
}

sub get_query {
	$ENV{'QUERY_STRING'} ||= '';

	die "あまりにでかいよ\n" if length $ENV{'QUERY_STRING'} > 1024 * 1024;

	my $buffer = $ENV{'QUERY_STRING'};

	return map {
		s/%([a-fA-F\d]{2})/pack('H2', $1)/eg;
		$_ = $enc->decode($_);
	} map {
		(split /=/, $_, 2)[0,1]
	} split /&/, $buffer;
}
