# Pythonのバージョン（軽量版）
FROM python:3.11-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール（OS側）
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# サーバー起動コマンド（開発用サーバーを使用）
# ※個人利用・VPN内なので、静的ファイル扱いが楽なrunserverを使います
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]