# yama-playlists.json

[枚方線](https://vrchat.com/home/world/wrld_bdc2f3b1-b1a9-4fc9-8124-0f97fe51e3fa/info) で使用するプレイリストの管理プロジェクト

## ファイル

- playlists.json
    - 手動で管理する生データ
    - URL は動画IDが分かれば何でもOK（余計なパラメータはあとで削除される）
    - タイトルは省略可

## プレイリストの正規化

```bash
make convert
```

- URL を正規化する
    - `https://www.youtube.com/watch?v=3RHGMf3H0Lw&list=PLV1VKKSui4LHOq1DWre3xHYZuCsu7pOVe&index=3` → `https://www.youtube.com/watch?v=3RHGMf3H0Lw`
- タイトルを取得する
    - タイトルが空の場合はタイトルを取得して埋める
