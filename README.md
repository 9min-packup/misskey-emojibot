# Misskey Emoji-Bot

Misskey の絵文字とデコレーションの更新を通知する Bot です。API として、絵文字一覧取得ではなくモデレーションログ取得を利用しているのが特徴です。<br><br>

Misskey 2023.12.2 での動作を確認していますが、API の変更が頻繁に起こるため、それ以外のバージョンでは動作の保証はできません。<br><br>

この Bot は一般ユーザーが作成するものではなく、サーバー管理者が作成してモデレーションに活用することを想定しています。

-   Bot アカウントに管理者権限を付与する必要があります。
-   アクセストークンに適切な権限を与える必要があります。（アクセストークンの取得方法については後述します。）<br><br>

アクセストークンに必要な権限は以下の通りです。

```js
"permission": [
        "read:account",
        "write:notes",
        "read:drive",
        "write:drive",
        "read:admin:show-moderation-log",
        "read:admin:emoji",
        "write:admin:emoji"
    ]
```

非常に簡易的に作成しましたので、何か不具合があるかもしれません。利用はあくまで自己責任で。<br><br>

## 使い方

使用するには Python の実行環境が必要です。（環境構築についてはここでは割愛します。）また、`requests` パッケージが必要なので `pip` であらかじめインストールしておいてください。

```
pip install requests
```

<br>

リポジトリを Clone したら、まず `config_example.json` を `config.json` に リネームしてください。その後、 `config.json` の中身に設定内容を記載します。 `config.json` の例は以下の通りです。

```js
{
    "host": "example.tld",
    "token": "XXXXXXXXXXXXXXXX",
    "moderation_logs_limit": 5,
    "running_interval_seconds": 60,
    "visibility": {
        "add": "public",
        "update": "home",
        "delete": "home"
    },
    "use_cw": {
        "add": false,
        "update": false,
        "delete": false
    },
    "local_only": true,
    "reaction_acceptance": null,
    "messages": {
        "emoji_add": "新しい絵文字が追加されました。",
        "emoji_add_user": "追加したユーザー",
        "emoji_update": "絵文字が更新されました。",
        "emoji_update_user": "更新したユーザー",
        "emoji_delete": "絵文字が削除されました。",
        "emoji_delete_user": "削除したユーザー",
        "decoration_add": "新しいアバターデコレーションが追加されました。",
        "decoration_add_user": "追加したユーザー",
        "decoration_update": "アバターデコレーションが更新されました。",
        "decoration_update_user": "更新したユーザー",
        "decoration_delete": "アバターデコレーションが削除されました。",
        "decoration_delete_user": "削除したユーザー"
    }
}
```

-   `host` には Misskey サーバーのドメインを記載してください。
-   `token` には取得したアクセストークンを記載してください。
-   `moderation_logs_limit` は一度に取得するモデレーションログの数で、最大値は 100 です。適宜調節してください。（数値を増やしたとしても、取得するのは絵文字 Bot 起動後に作成されたログのみです）
-   `running_interval_seconds` は Bot が動作する時間間隔（秒）です。お好みで調節してください。
-   `visibility` は絵文字またはデコレーションが更新されたときのノートの公開範囲です。`public`, `home`, `followers` を指定できます。`add` は追加時の公開範囲、`update` は更新時の公開範囲、`delete` は削除時の公開範囲です。
-   `use_cw` は絵文字またはデコレーションが更新されたときのノートに CW をかけるかの設定です。`true` か `false` かを指定できます。`add` は追加時、`update` は追加時、`delete` は削除時の指定です。
-   `local_only` は絵文字またはデコレーションが更新されたときのノートの連合をオフにするかどうかの設定です。`true` か `false` かを設定でき、`true` にすると連合オフになります。
-   `reaction_acceptance` は Bot のノートにつけられるリアクションの種類の指定です。`null（全て許可）`, `likeOnly（いいねのみ）`, `likeOnlyForRemote（リモートからはいいねのみ）`, `nonSensitiveOnly（非センシティブのみ）`, `nonSensitiveOnlyForLocalLikeOnlyForRemote（リモートからは非センシティブのみ）`のいずれかを指定できます。
-   `messages` は各種メッセージの設定です。お好みで変更してください。

<br>
設定が完了したら、以下のコマンドで Bot を実行します。運が良ければ動きます。

```
python run.py
```

<br>
動作確認ができたら、あとは Linux サーバーなどでサービスに登録してぐるぐる動かせば OK です。<br><br>

## アクセストークンの取得

最新バージョンでは GUI 上でのアクセストークン発行で大丈夫なようですが、バージョン 2023.12.2 だと GUI 上では必要な権限を付与できないようですので、MiAuth か API を叩いてアクセストークンを取得する必要があります。<br><br>

自分の環境では MiAuth を利用したアクセストークン取得がうまくいきませんでしたので、API を叩いてアプリを登録したのち取得する方法（旧式）を採用しています。（いずれ必要がなくなるかもしれませんが、旧式も記録として残した方がいいと思うのであえて残します。）<br><br>

リポジトリ内の `tools` ディレクトリにアクセストークン取得用のスクリプトを格納してありますので、 `tools` ディレクトリ内で作業してください。<br>

`tools` ディレクトリ内に `app_config_example.json` ファイルがありますので、まずはこれを `app_config.json` にリネームしてください。その後、 `app_config.json` の中身に設定内容を記載します。 `app_config.json` の例は以下の通りです。

```js
{
    "host": "example.tld",
    "app_name": "EmoijBot",
    "description": "絵文字とデコレーションの更新を通知します",
    "permission": [
        "read:account",
        "write:notes",
        "read:drive",
        "write:drive",
        "read:admin:show-moderation-log",
        "read:admin:emoji",
        "write:admin:emoji"
    ]
}
```

<br>

-   `host` には Misskey サーバーのドメインを記載してください。
-   `app_name` には登録するアプリの名前を記載してください。
-   `description` には登録するアプリの説明を記載してください。
-   `permission` には上記の通り記載してください。
    <br><br>

`app_config.json` の設定が終わったら。`create_app.py` を実行してください。うまくいけば `アプリ作成完了` と表示されます。

```
python create_app.py
```

<br>

次に `create_session.py` を実行してください。うまくいけば `セッション作成完了` と表示されます。成功すると url が表示されるので、 Bot 用アカウントでログインした状態で url にアクセスし、認証してください。

```
python create_session.py
```

<br>

最後に `create_token.py` を実行してトークンを取得します。成功すると アクセストークンが表示されます。うまくいかない場合は `create_session.py` からやり直してください。

```
python create_token.py
```

<br>

（取得した情報は `tools/data` フォルダ内にログとして保存されます。アクセストークンは `token_info.json` 内に保存されます。）<br><br>

以上でトークン取得は完了です。お疲れ様でした。<br><br>

## 雑記

絵文字 Bot というよりかは、実はモデレーションログを取得して通知する Bot です。絵文字とデコレーション以外も通知したり、通知先をノートでなく他のところ（Discord とか）にすればモデレーションに活かせそうですね。いろいろ工夫してもよさそうです。
