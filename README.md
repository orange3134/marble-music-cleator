# Marble Music Creator

Blender でマーブルミュージック動画を作る作業を簡単にする補助アドオンです。

<img src="https://github.com/user-attachments/assets/b6e0437a-ccae-4095-9230-8d14fd006224" width="25%">
<img src="https://github.com/user-attachments/assets/c3367b84-ea5c-4c0a-b252-01764403ffb9" width="25%">

## 使い方

<img src="https://github.com/user-attachments/assets/c54ad029-0256-4898-8776-bde64a3a4b6c" width="50%">

marble_music_creator.py を Blender のアドオンとしてインストールしてください。  
ビューポートのメニューに Marble Music Creator が追加されます。

**Target Object**　- ボールのオブジェクトを選んでください。  
**Prefab Object** - 板のオブジェクトを選んでください。  
**Collection Of Instance** - 複製されたオブジェクトを入れるコレクションを選んでください。（無しなら複製元と同じコレクションになります。）  
**Position Offset** - 板をボールからどれくらい離れた位置に配置するかを決めます。ボールの半径より少し大きめにしてください。  
**Random Rotation Angle** - ボールの進行方向に対して板を傾ける角度の最大値を決めます。

ボールと板にリジッドボディを設定してください。  
シーケンサーに音楽ファイルを配置してください。  
タイムラインを再生しながら音楽に合わせて**Duplicate Prefab**ボタンを押してください。  
ボタンを押す度にボールの進行方向に板が配置され、ボールが跳ねます。

## サンプル

sample フォルダに入っている blend ファイルを参照してください。

## 既知の問題

- ボールが以前に配置した板にあたってしまうことがある
  - 板の角度は単純にランダムで、ボールの以前の軌道を一切考慮していないためです。  
    手動で板の角度を調整して対応してください。
