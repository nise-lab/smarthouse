# Smart House
## 初期設定
前提
+ ruby
  + invoker
+ python3

### julius のセットアップ
```
$ sh julius_intalize.sh
```

## 実行
```
$ source bin/activate
$ invoker start
```

## 音声認識のテスト
```
$ sh ./julius_test_for_xxx.sh
```

音声を拾えるか確認

## 設定ファイル
調子悪いときに、パロメータをいじる場所

### 音声認識
+ julius/julius.conf
+ julius/julius.words (euc-jp なので注意)

### 音声
+ Procfile

引数、環境変数 を確認

### 家電が動かない
+ house-daemon/house_sections.json
+ house-daemon/io_parts.json

定義が正しいか確認
