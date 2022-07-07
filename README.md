# 比特币溯源平台接口说明

1.获取一笔交易的所有输入（付款）账户及金额

URL：/btc/getTransactionInputs

请求参数示例：

txid=01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "inputs": [
            {"address": "1C93genTN1DfhNrd899XazNuw2vHnfhjXU", "balance": 30, "isMalicious": true}, ...
        ]
    }
}
```



2.获取一笔交易的所有输出（收款）用户及金额

URL：/btc/getTransactionOutputs

请求参数示例：

txid=01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "outputs": [
            {"address": "1C93genTN1DfhNrd899XazNuw2vHnfhjXU", "balance": 30, "isMalicious": true}, ...
        ]
    }
}
```



3.获取一笔交易的所有输入交易

URL：/btc/getInputTransactions

请求参数示例：

txid=01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "isRisky": true}, ...
        ]
    }
}
```



4.判定一个账户是否在已知的恶意地址集合里

URL：/btc/isMaliciousAccount

请求参数示例：

address=1rkH7DtWxS6eY72bqoJSE8usfWccYQqnZ

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "isMalicious": true,
        "abuses": [
            {
                "message": "This bitcoin address is used by criminals in Netherlands for scams and extortion",
                "translatedMessage": "这个比特币地址被荷兰的犯罪分子用于诈骗和勒索",
                "info": "用户Yao于2021-06-15 14:34:26上传"
            }, ...
        ]
    }
}
```



5.获取以指定账户的所有交易

URL：/btc/getAllTransactionsOfAccount

请求参数示例：

address=1C93genTN1DfhNrd899XazNuw2vHnfhjXU

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {
                "balance": 0.04702268,
                "isRisky": true,
                "time": "2021-05-26 17:59:29",
                "txid": "4987ea6dc28626edf75de59f9e58f32a00835a4fece000917c24bc468797c8ef"
            }, ...
        ]
    }
}
```



6.获取最新的N个区块里面所包含的交易

URL：/btc/getLatestTransactions

请求参数示例：

blockCount=1

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "isRisky": true}, ...
        ]
    }
}
```



7.获取与一个地址存在交易关系的所有恶意账户

URL：/btc/getRelevantMaliciousAccounts

请求参数示例：

address=1MGgC7NiRZ4urzH3oyQFKor7tgRRnUAPWx

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "maliciousAccounts": [
            {
                "address": "1C93genTN1DfhNrd899XazNuw2vHnfhjXU", 
                "abuses": [
                    {
                        "message": "This bitcoin address is used by criminals in Netherlands for scams and extortion",
                        "translatedMessage": "这个比特币地址被荷兰的犯罪分子用于诈骗和勒索",
                        "info": "用户Yao于2021-06-15 14:34:26上传"
                    }, ...
                ]
            }, ...
        ]
    }
}
```



8.获取一个账户所有未花出去的交易输出

URL：/btc/getUnspentTransactionOutputsOfAccount

请求参数示例：

address=13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txOutputs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "vout": 1}, ...
        ]
    }
}
```



9.获取最近N个区块的大额交易（例如最近20个取款里面的前30笔大额交易）

URL：/btc/getLatestLargeBalanceTransactions

请求参数示例：

blockCount=20&transactionCount=30

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 11000.0, "time": "2016-05-02 18:59:05"}, ...
        ]
    }
}
```



10.获取最近N个区块里面的风险交易

URL：/btc/getLatestRiskyTransactions

请求参数示例：

blockCount=20

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 11000.0, "time": "2016-05-02 18:59:05"}, ...
        ]
    }
}
```



11.提交恶意用户信息

URL：/btc/addMaliciousAccount

请求参数示例：

address=13AM4VW2dhxYgXeQepoHkHSQuy6NgaEb94&message=这是一个恶意用户，请在交易时注意资金安全！&abuser=Yao

返回结果示例：

```json
{
    "code": 200,
    "message": "添加成功！",
    "data": {}
}
```





12.查询最新N个区块里面的交易总量

URL：/btc/getLatestTransactionCount

请求参数示例：

blockCount=20

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txCount": 35784
    }
}
```



13.查询最新N个区块里面的大额交易总量

URL：/btc/getLatestLargeBalanceTransactionCount

请求参数示例：

blockCount=20&minBalance=2000

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txCount": 35784
    }
}
```



14.查询最新N个区块里面的出现的用户数量（出于效率考虑结果并不精确，仅用于估算）

URL：/btc/getLatestActiveAddressCount

请求参数示例：

blockCount=20

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "addressCount": 35784
    }
}
```



15.获取以指定账户作为付款方的所有交易

URL：/btc/getPayerTransactionsOfAccount

请求参数示例：

address=1C93genTN1DfhNrd899XazNuw2vHnfhjXU

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 100, "isRisky": true}, ...
        ]
    }
}
```



16.获取以指定账户作为收款方的所有交易

URL：/btc/getPayeeTransactionsOfAccount

请求参数示例：

address=1C93genTN1DfhNrd899XazNuw2vHnfhjXU

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 100, "isRisky": true}, ...
        ]
    }
}
```



17.获取指定时间段内的交易数量

URL：/btc/getTransactionCount

请求参数示例：

startTime=1231469744&endTime=1231606762（秒数时间戳）

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txCount": 35784
    }
}
```



18.获取指定时间段内的活跃地址数量

URL：/btc/getActiveAddressCount

请求参数示例：

startTime=1231469744&endTime=1231606762（秒数时间戳）

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "addressCount": 35784
    }
}
```



19.获取比特币兑换法币的汇率（每15分钟更新一次）

URL：/btc/getExchangeRates

请求参数示例：无

返回结果示例：

```json
{
    "code": 200,
    "data": {
        "exchangeRates": {
            "AUD": 50302.89,
            "BRL": 207150.52,
            "CAD": 47201.24,
            "CHF": 34997.37,
            "CLP": 28466497.96,
            "CNY": 248653.15,
            "DKK": 237567.47,
            "EUR": 31996.34,
            "GBP": 27611.09,
            "HKD": 302656.1,
            "INR": 2831643.32,
            "ISK": 4725053.28,
            "JPY": 4258577.43,
            "KRW": 43546755.85,
            "NZD": 53411.55,
            "PLN": 143774.16,
            "RUB": 2865428.76,
            "SEK": 323970.55,
            "SGD": 51608.72,
            "THB": 1218581.76,
            "TRY": 329005.96,
            "TWD": 1083092.8,
            "USD": 38995.24
        }
    },
    "message": "查询成功！"
}
```



20.获取缓存的最近N个区块的大额交易（默认为最近50个区块的前300笔交易，每十分钟更新一次）

URL：/btc/getCachedLargeBalanceTransactions

请求参数示例：无

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 11000.0, "time": "2016-05-02 18:59:05"}, ...
        ]
    }
}
```



21.获取缓存的最近N个区块里面的风险交易（默认为最近50个区块，每十分钟更新一次）

URL：/btc/getCachedRiskyTransactions

请求参数示例：无

返回结果示例：

```json
{
    "code": 200,
    "message": "查询成功！",
    "data": {
        "txs": [
            {"txid": "01029eafde580cdd722dcac60845dad0024f8d85ffb1638bbb184f3cda316de8", "balance": 11000.0, "time": "2016-05-02 18:59:05"}, ...
        ]
    }
}
```



22.获取最近24小时里面每小时的交易数量（数组顺序按时间从远到近）

URL：/btc/getTransactionCountInRecentHours

请求参数示例：无

返回结果示例：

```json
{
    "code": 200,
    "data": {
        "addressCounts": [
            {"21:00": 32463},
            ...
            {"20:00": 71275}
        ]
    },
    "message": "查询成功！"
}
```



23.获取最近24小时里面每小时的活跃地址数量（数组顺序按时间从远到近）

URL：/btc/getActiveAddressCountInRecentHours

请求参数示例：无

返回结果示例：

```json
{
    "code": 200,
    "data": {
        "txCounts": [
            {"21:00": 32463},
            ...
            {"20:00": 71275}
        ]
    },
    "message": "查询成功！"
}
```



24.获取交易的回溯树

URL：/btc/getInputTransactionTree

请求参数示例：

txid=8a00216f331b643addde5c19282feaf4f979701c5494836faacf1efbdc225eb6&depth=3&riskyOnly=1（如果不需要过滤非风险交易则riskyOnly=0）

返回结果示例：

```json
{
    "code": 200,
    "data": {
        "tree": {
            "children": [
                {
                    "children": [
                        {
                            "isRisky": true,
                            "name": "8f4d83231716d22810e7485e158c1c5864d286e607b3a2c447987dbdb17952cc"
                        }
                    ],
                    "isRisky": true,
                    "name": "f2098b434ea01c3463c29f62cfaefb389e46d4e85f32c34a5b8a7f975853f211"
                }
            ],
            "isRisky": true,
            "name": "8a00216f331b643addde5c19282feaf4f979701c5494836faacf1efbdc225eb6"
        }
    },
    "message": "查询成功！"
}
```

