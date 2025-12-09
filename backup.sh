#!/bin/bash

# === 設定エリア ===
# Djangoプロジェクトの場所
PROJECT_DIR="/home/ubuntu/my_django_project"
# バックアップ先（さっき作った暗号化リモートの名前）
REMOTE_NAME="secret-box"
# 一時保存場所
TEMP_DIR="/tmp/backup_temp"
DATE=$(date +%Y%m%d-%H%M)
ZIP_NAME="backup-$DATE.zip"

# === 処理開始 ===
mkdir -p $TEMP_DIR

# 1. データベース (db.sqlite3) をコピー
# ※Dockerの外にあるファイルをそのままコピーします
cp $PROJECT_DIR/db.sqlite3 $TEMP_DIR/

# 2. 画像 (mediaフォルダ) をコピー
cp -r $PROJECT_DIR/media $TEMP_DIR/

# 3. まとめて圧縮 (zip)
# zipコマンドがない場合に備えてインストール
sudo apt-get install zip -y > /dev/null
cd /tmp
zip -r $ZIP_NAME backup_temp

# 4. 暗号化してGoogleドライブへ転送
rclone copy /tmp/$ZIP_NAME $REMOTE_NAME:/

# 5. お掃除（サーバー内のゴミを消す）
rm -rf $TEMP_DIR
rm /tmp/$ZIP_NAME

# 6. 古いバックアップを消す（Googleドライブ上で30日以上前のものを削除）
rclone delete $REMOTE_NAME:/ --min-age 30d