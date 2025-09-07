# .sqlの書き方講座
---

## 1. `.sql` ファイルとは？

* **SQL文をまとめて保存したテキストファイル**
* データベース（MySQL, PostgreSQL, SQLite など）に対して、一括で実行できるスクリプト
* 例えるなら「料理のレシピカード」。コマンドが順番に書いてあって、DBに渡すとその通りに調理してくれる

---

## 2. 基本構成

`.sql`ファイルは、**SQL文をセミコロン(;)で区切って並べるだけ**。

```sql
-- コメント: データベース作成
CREATE DATABASE sample_db;

-- コメント: テーブル作成
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT
);

-- コメント: データ挿入
INSERT INTO users (name, age) VALUES ('Alice', 25);
INSERT INTO users (name, age) VALUES ('Bob', 30);

-- コメント: データ確認
SELECT * FROM users;
```

ポイント：

* `--` から始めると**コメント**（メモ書き）
* SQL文の最後には **セミコロン(;)**
* 大文字小文字は区別されないけど、慣例的に **SQLキーワードは大文字** で書く

---

## 3. よく使う基本文

#### (1) データベース操作

```sql
CREATE DATABASE sample_db;
DROP DATABASE sample_db;
```

#### (2) テーブル作成・削除

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
DROP TABLE users;
```

#### (3) データ操作

```sql
-- データ追加
INSERT INTO users (id, name, age) VALUES (1, 'Alice', 25);

-- データ取得
SELECT * FROM users;
SELECT name FROM users WHERE age > 20;

-- データ更新
UPDATE users SET age = 26 WHERE name = 'Alice';

-- データ削除
DELETE FROM users WHERE id = 1;
```

---

## 4. 実行方法

環境によって違うけど、代表例：

* **PostgreSQL**

  ```bash
  psql -U ユーザ名 -d データベース名 -f script.sql
  ```

* **MySQL**

  ```bash
  mysql -u ユーザ名 -p データベース名 < script.sql
  ```

---

## 5. よくある注意点

* `DROP` 文は取り返しがつかない → 本番環境では特に注意
* コメントをしっかり書くと後で自分も他人も助かる
* 複数文をまとめて書くときは、**順番が大事**（テーブル作成前にデータ挿入しようとするとエラー）

---

💡まとめ
`.sql`ファイルは「データベースに渡すレシピ」。

* **コメントで分かりやすく**
* **SQL文はセミコロンで区切る**
* **実行順序に気をつける**


# SQLの読み出し方法講座
## model.py・schema.pyの説明
- model.py: DBのテーブル構造を定義 (SQLAlchemyモデル)
  - 例え：病院カルテ台帳の設計図
- schema.py: APIの入出力データ構造を定義 (Pydanticモデル)
　- 例え：申し込みフォームの設計図
## CRUD
### Create
- 基本コマンド：
  ```sql
  INSERT INTO テーブル名 (列名1, 列名2) VALUES (値1, 値2);
  ```
### Read
- 基本コマンド：
  ```sql
  SELECT * FROM テーブル名;
  ```
- 特定の列を指定する場合：
  ```sql
  SELECT 列名1, 列名2 FROM テーブル名;
  ```
- 条件をつける場合：
  ```sql
  SELECT * FROM テーブル名 WHERE 条件;
  ```
  - 例：年齢が30以上の患者を取得
  ```sql
  SELECT * FROM patients WHERE age >= 30;
  ```
  - 例：登録日が2025年9月1日以降の患者を取得
  ```sql
  SELECT * FROM patients WHERE created_at >= '2025-09-01';
  ```
    - 日時のフォーマットはDBによって異なる場合がある。PostgreSQLではISO 8601形式（'YYYY-MM-DD'や'YYYY-MM-DDTHH:MM:SS'）が一般的。
  - 例：名前に'A'が含まれる患者を取得
  ```sql
  SELECT * FROM patients WHERE name LIKE '%A%';
  ```
### Update
- 基本コマンド：
  ```sql
  UPDATE テーブル名 SET 列名1 = 値1, 列名2 = 値2 WHERE 条件;
  ```
### Delete
- 基本コマンド：
  ```sql
  DELETE FROM テーブル名 WHERE 条件;
  ```

---
# その他のメモ
## データベースとテーブルの違い

### 1. データベース (Database)

* **役割**: データを入れる「大きな箱」や「フォルダ」
* 中にはたくさんのテーブルを入れられる
* 例えば「社員管理システム用のデータベース」「顧客情報データベース」など用途ごとに分ける

📂 フォルダに例えると：

* データベース = パソコンの中の「プロジェクトフォルダ」
* フォルダの中に色々な表（テーブル）をしまっているイメージ

---

### 2. テーブル (Table)

* **役割**: 実際にデータを行と列で保存する「表」
* 一つのテーブルは「特定の種類のデータ」に対応する
* 例: 社員一覧のテーブル、製品一覧のテーブル、注文履歴のテーブル

📊 Excelに例えると：

* テーブル = 1つのExcelシート（社員一覧表とか、商品一覧表とか）
* 列 = 名前・年齢・部署 などの項目
* 行 = 1人の社員や1つの商品といった具体的なデータ

---

### 3. 関係性イメージ

図にすると：

```
📂 データベース (company_db)
 ├── 📊 テーブル employees (社員)
 │      ├── id | name  | age | dept
 │      ├── 1  | Alice | 25  | HR
 │      └── 2  | Bob   | 30  | IT
 │
 ├── 📊 テーブル products (商品)
 │      ├── id | name   | price
 │      ├── 1  | PC     | 1000
 │      └── 2  | Mouse  | 50
 │
 └── 📊 テーブル orders (注文)
        ├── id | employee_id | product_id | date
        └── 1  | 2           | 1          | 2025-09-02
```

* **データベース**: 全体の箱 (`company_db`)
* **テーブル**: その中の表（社員・商品・注文）

---

### 4. まとめ

* **データベース = フォルダ**
* **テーブル = フォルダの中のExcelシート（表）**
* 実際のデータはテーブルに保存される
* データベースはテーブルたちをまとめる器