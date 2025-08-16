# 1. ベースイメージ
FROM python:3.11-slim

# 2. 作業ディレクトリ
WORKDIR /app

# 3. 必要なライブラリをコピー
COPY requirements.txt ./

# 4. ライブラリをインストール
RUN pip install --no-cache-dir -r requirements.txt

# 5. コードをコピー
COPY . .

# 6. Railwayで起動コマンド
CMD ["python", "stream.py"]
