# watt-monitor

CTセンサーで計測した電力消費量を Grafana Cloud に送信し続けるスクリプト。

Raspberry Pi上での動作を前提としており、GPIO経由のMCP3008（ADC）を使用する。
送信には OTLP/HTTP JSON プロトコルを使用する。

## 構成

| ファイル | 役割 |
|---------|------|
| `sensor.py` | センサー読み取り・電力計算ロジック |
| `monitor.py` | 計測値を Grafana Cloud に送信するメインスクリプト |
| `poll.py` | 計測値を標準出力に表示（動作確認用） |
| `probe.py` | 架空データを Grafana Cloud に送信（疎通確認用） |
| `otlp.py` | OTLP/HTTP JSON 送信の実装 |

## セットアップ

```sh
git clone https://github.com/106-/watt-monitor.git
cd watt-monitor
cp monitor.env.sample monitor.env
```

`monitor.env` を編集して Grafana Cloud の接続情報を設定する。
値は Grafana Cloud ポータルの **Connections → OpenTelemetry** から取得できる。

```sh
make sync
```

## 使い方

```sh
make poll    # センサーの値をポーリング表示
make probe   # Grafana Cloud への疎通確認（架空データ送信）
make install # systemdサービスとしてインストール・起動
```

## daemon化

`make install` が以下を自動で行う。

1. `uv sync` で依存パッケージをインストール
2. `monitor.service.tmpl` から実行環境に合わせたサービスファイルを生成
3. `/etc/systemd/system/monitor.service` にコピーして有効化・起動

アンインストールは `make uninstall`。
