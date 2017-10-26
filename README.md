Trading System
=========

#Overview
Built the trading system with Tornado, SQLAlchemy, and SQLite for backend and ReactJS for frontend

#Features
+ Users be able to trade through their trading accounts. 
+	For a trade to be approved, the sum of that individual’s trading and checking account must be greater than 20% of the trade value. 
+	The client can be informed of the approval status of the trades they request.
+ Approved trades should be reflected in the adjusted account balance. 
+ For declined trades, the client should be notified of how much money should be deposited into their accounts to satisfy the requirement for trade approval. 

#how to run

### 

```
cd app
pip install -r requirements.txt
cd frontend
npm install
cd ../backend
python server.py
```


#Run test
```
python test.py
```
