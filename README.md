# Mithril Backend Homework

這是一個 backend service, 用 python 的 Flask framework 完成。簡略地提供以下功能：
 
 - 使用者註冊
 - 使用者登入
 - 發圖 (必續先登入)
 - 拿取圖片資料 (必先先登入)(可以利用query的方式拿到特定使用者發的圖)


## Quick Run

為了讓服務可以運行，會需要兩個 docker service:

 - mysql server container
 - flask  backend service container

且 mysql server container 要能讓 flask container 在 continer 內部連接到。

為了讓服務都順利地建立起來，請跑以下的 script:

``` bash
$ ./run.sh
```

這個 script 會自動建立這兩個 service 且跑起來。一些可以設定的變數定義在了 script 的開頭。

如果跑出類似 
`Error response from daemon: network with name mithrik-hw-net already exists` 
錯誤時，代表我重複創建了一個已存在的 docker network，為了避免將我的 docker container 隨意加入您的 network，請去 script 的開頭將 MY\_NETWORK\_NAME 改名。

如果是重複跑了多次 run.sh 也會遇到相同問題。那麼請手動刪除 network MY\_NETWORK\_NAME，然後再跑一次。

 
## Build and Run Image

這個 service 可以用 docker 的方式讓他在 host 上執行。可以使用提供的 Makefile 來執行 make build 與 make run 即可。

在 make run 時需要提供兩個參數, 分別是：

 - env=xxx 
 	這個是要傳入 image 的環境變數列表，請參考下面的 Environment Variable 章節
 - net-name
 	這是一個 docker network name，為了讓我們的 service 與 mysql docker server 在同一個 host 時可以在 container 內互相連結到所需傳入的參數。
 	

## Environment Variable

需要提供兩個 environment variable

 - DB\_URI
 	這是讓 flask 可以連到我們 database 的參數。  
 	` example: mysql+pymysql://root:password@mysqlhost:3306/testing?charset=utf8 `
 	
 	這邊的 mysqlhost 可以是其他任何有 mysql server 的 host, 或是其他在相同 docker network 中的 container name。
 	
 - SECRET_KEY
 	這是一個在 flask server 中使用到的秘密字串。
 	

## entrypoints.py

整個 service 的入口。他會先利用 sqlalchemy 建立所需要的 table (如果存在就不用創建)。接者用 gunicorn 來啟用我們的服務。gunicorn logging 設定可以參考 gunicorn.conf
 	
 	
## APIs

所有的 api 交換格式都定義為 json。  
因此 POST 時請記得在 header 加入 `'Content-Type': 'application/json'`

所有的回傳格式都統一如下：

``` json
{
	"message": "messages",
	"code": 10,
	"data": ...
}
```

所有回傳的資料都會放在 data 中。以下所有的 response 也都是在 data 之下的格式。  
Request 就沒統一的格式。因此以下每個 API 的 request 就不是包含在任何格式下的 object。

### POST /api/user/register 使用者註冊

- request body:
	
	``` json
	{
		"username": "Rory",
		"password": "12345",
	}
	```

- response status:
	- 200 : 成功
	- 400 : request body 格式錯誤
	- 409 : 使用者已經存在

### POST /api/user/login 使用者登入

- request body:
	
	``` json
	{
		"username": "Rory",
		"password": "12345",
	}
	```
- response body:

	``` json
	{
		"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...."
	}
	```

- response status:
	- 200 : 成功
	- 400 : request body 格式錯誤
	- 404 : 使用者不存在
	- 401 : 密碼錯誤

### JWT token status code

因為關於 picture 的 api 會限制一定要使用者登入，因此我們會需要 JWT Token 來驗證使用者身份。我們需要利用 /api/user/login 的 token 放入 http header 中：

```
"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...."
```

如果 token 有問題則會遇到以下 status code:

- response status:
	- 403 : header 中沒有 Authorization
	- 401, code=8 : token 過期了，需重新登入
	- 401, code=9 : token 不合法
	
	
### POST /api/picture 使用者發圖

- request body:
	
	``` json
	{
		"data": "\9klelwrwewerwer..." # base64 encode image string
	}
	```

- response status:
	- 201 : 創建成功
	- 400, code=2 : request body 格式錯誤
	- 400, code=6 : data 不是 base64 encode
	- 500, code=10, 上傳圖片失敗

### GET /api/picture?page=1&limit=20&username=Rory 使用者取圖

- query arguments
	- limit: 每頁幾張圖，如果不給 limit 參數則預設為 20
	- page: 第幾頁，如果不給 page 參數則預設為 1
	- username: 要取得哪個使用者發的圖，如果不給 username 參數則預設為所有的圖

- response body:

	``` json
	{
		"total": 100,
		"page": 1,
		"limit": 20,
		"pictures": {
			"id": 1,  # picture id
			"username": "Rory",
			"data": "\9klelwrwewerwer...", # base64 encode image string
		}
	}
	```

- response status:
	- 200 : 成功
	- 400, code=11 : query 參數錯誤
 	

## File Structure and Functionality

所有 backend server 相關的 code 都在 server 資料夾底下。auth 與 picture 囊括了兩個主要的功能。

- auth module : 處理使用者相關功能
 	- model : 定義 User Model 欄位與 user 物件。User 物件還處理了 password 加密與 JWT Token 的處理 function。
 	- view : 處理 user 的 api 邏輯
 	- utils : 輔助 view 中處理的 function
 	- login_required decorator : 負責先判斷 Authorization header 合法性的 decorator

- picture module : 處理發圖與取圖相關功能
   - model: 定義 Picture Model 欄位與物件。
   - view : 處理 Picture 的 api 邏輯
   - utils : 輔助 view 中處理的 function

- app file : init_app function 來產生我們主要的 server app。
- config file : 定義一些基本設定
- extensions file : 主要匯入第三方插件。這邊這次只放入 Flask-SQLAlchemy
- exceptions file : 自訂一些 exceptions
- responses file : 定義我們的回傳 class 與格式
- routes : 控制 routing 與相對應的 view handler
	