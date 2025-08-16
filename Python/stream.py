import os
import time
from collections import deque
from dotenv import load_dotenv
import tweepy

# ----------------------------
# 環境変数読み込み
# ----------------------------
load_dotenv()
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

if not all([consumer_key, consumer_secret, access_token, access_token_secret, bearer_token]):
    raise RuntimeError("環境変数が正しく設定されていません")

# ----------------------------
# Tweepyクライアント認証
# ----------------------------
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    wait_on_rate_limit=True
)

my_id = client.get_me().data.id

# ----------------------------
# ホロライブJPメンバー
# ----------------------------
usernames = [
    'tokino_sora', 'robocosan', 'azki_hololive', 'sakuramiko35', 'suisei_hoshimati',
    'yozoramel', 'akirosenthal', 'haatoakari', 'shirakamifubuki', 'natsuiromatsuri',
    'minatoaqua', 'nakiriayame', 'yuzukichoco', 'oozorasubaru', 'murasakishion',
    'ookamimio', 'nekomataokayu', 'inugamikorone',
    'usadapekora', 'shiranuiflare', 'shiroganenoel', 'houshoumarine',
    'amanekanatach', 'tsunomakiwatame', 'tokoyamitowa', 'himemoriluna',
    'yukihanalamy', 'momosuzunene', 'shishirobotan', 'omarupolka',
    'laplus_yami', 'takanelui', 'hakuikoyori', 'kazamairoha'
]

# ユーザー名→IDのキャッシュ
user_id_to_username = {}
chunk_size = 100
for i in range(0, len(usernames), chunk_size):
    chunk = usernames[i:i+chunk_size]
    users = client.get_users(usernames=chunk)
    if users.data:
        for user in users.data:
            user_id_to_username[str(user.id)] = user.username
    time.sleep(1)

user_ids = list(user_id_to_username.keys())

# ----------------------------
# カスタム引用文言
# ----------------------------
custom_quotes = {
    'tokino_sora': "そらちゃんの配信告知！ みんなでそらともになろう♪",
    'robocosan': "ロボ子さんのハイテク配信スタート！ 未来を感じよう！",
    'azki_hololive': "AZKiさんの歌声が響く配信！ バーチャルディーバのステージへ！",
    'sakuramiko35': "みこちのエリート配信にぇ！ 巫女パワー全開だよ！",
    'suisei_hoshimati': "すいちゃんの星のような配信！ 彗星のごとく輝け☆",
    'yozoramel': "メルちゃんの甘い配信！ ヴァンパイアの魅力に吸い込まれちゃう？",
    'akirosenthal': "アキちゃんのダンス配信！ エルフの優雅さを堪能しよう！",
    'haatoakari': "はあちゃまのクレイジー配信！ 予測不能の楽しさ！",
    'shirakamifubuki': "ふぶきさんの狐耳配信！ 白上さんパワーで元気チャージ！",
    'natsuiromatsuri': "まつりちゃんの元気配信！ 祭りの熱気を感じよう！",
    'minatoaqua': "あくあさんのメイド配信！ 完璧なサービスをお届け！",
    'nakiriayame': "あやめさんの鬼配信！ 百鬼の笑顔に癒されよう！",
    'yuzukichoco': "チョコ先生のセクシー配信！ 癒しの時間ですよ～",
    'oozorasubaru': "すばるさんの元気配信！ シュバシュバ全力でいくぜ！",
    'murasakishion': "しおんさんの魔法配信！ 紫咲のブラックマジックに注意！",
    'ookamimio': "みおさんの狼配信！ 大神の優しさを感じて！",
    'nekomataokayu': "おかゆさんの猫配信！ ねこまたのんびりタイム♪",
    'inugamikorone': "ころねさんのわんこ配信！ ド葛本社の元気をお届け！",
    'usadapekora': "ぺこらさんのうさぎ配信！ 笑いの渦に巻き込まれぺこ！",
    'shiranuiflare': "フレアさんのエルフ配信！ 不知火の炎のように熱く！",
    'shiroganenoel': "ノエルさんの騎士配信！ 団長の力強さを体感！",
    'houshoumarine': "マリン船長の海賊配信！ 宝探しの冒険へ出航！",
    'amanekanatach': "かなたさんの天使配信！ 天音の歌声に癒されよう！",
    'tsunomakiwatame': "わためさんの羊配信！ 角巻のラップで盛り上がれ！",
    'tokoyamitowa': "とわ様の悪魔配信！ 常闇の魅力に落ちろ！",
    'himemoriluna': "ルーナ姫の配信！ 姫森の甘い世界へようこそ！",
    'yukihanalamy': "ラミィさんの雪女配信！ 雪花のクールビューティー！",
    'momosuzunene': "ねねさんのスーパー配信！ 桃鈴の明るさで元気に！",
    'shishirobotan': "ぼたんさんのライオン配信！ 獅白の強さを味わえ！",
    'omarupolka': "ポルカさんのキツネ配信！ 尾丸のサーカスショー！",
    'laplus_yami': "ラプラスさんの闇配信！ ラプラスダークネスの秘密を解け！",
    'takanelui': "ルイさんの鷹配信！ 鷹嶺のエレガントタイム！",
    'hakuikoyori': "こよりさんの科学配信！ 博衣のラボで実験しよう！",
    'kazamairoha': "いろはさんの侍配信！ 風真の剣道精神を感じろ！"
}

# ----------------------------
# 投稿バッファ
# ----------------------------
tweet_queue = deque()

# ----------------------------
# ストリーミングクラス
# ----------------------------
class HololiveStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        if tweet.author_id == my_id:
            return
        if any(word in tweet.text.lower() for word in ['配信', 'stream', '生放送']):
            tweet_queue.append(tweet)

# ----------------------------
# バッファ処理関数
# ----------------------------
def process_queue():
    while True:
        if tweet_queue:
            tweet = tweet_queue.popleft()
            author = user_id_to_username.get(str(tweet.author_id), None)
            if not author:
                # キャッシュにない場合は取得
                try:
                    user = client.get_user(id=tweet.author_id).data
                    author = user.username
                    user_id_to_username[str(tweet.author_id)] = author
                except Exception:
                    author = "unknown"
            quote_text = custom_quotes.get(author, f"ホロメン配信告知！ @{author} の配信をお知らせ♪")
            try:
                client.create_tweet(text=quote_text, quote_tweet_id=tweet.id)
                print(f"Quoted tweet: {tweet.id} from @{author}")
                time.sleep(5)  # Rate Limit対策
            except tweepy.TweepyException as e:
                print(f"投稿エラー: {e}")
                time.sleep(30)
        else:
            time.sleep(1)

# ----------------------------
# ストリーム開始
# ----------------------------
stream = HololiveStream(bearer_token)

# 既存ルール削除
rules = stream.get_rules().data or []
for rule in rules:
    stream.delete_rules(rule.id)

# 新ルール追加
stream.add_rules([tweepy.StreamRule(f"from:{uid}") for uid in user_ids])

# ストリームを非同期で開始
import threading
threading.Thread(target=process_queue, daemon=True).start()
stream.filter(tweet_fields=['author_id', 'text'])
