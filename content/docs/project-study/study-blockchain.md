---
title: "Nakamoto共识（Go语言）学习"
description: "Nakamoto共识（Go语言）学习工具，10步构建完整区块链系统"
weight: 10
aliases:
  - /docs/blog/study-blockchain/
---

# Nakamoto共识（Go语言）10天项目学习

从零开始，用 10 个渐进步骤构建一个完整的比特币式区块链系统。涵盖区块、PoW、序列化、持久化、CLI、UTXO交易、钱包、Merkle树和P2P网络。目标是让你不仅能写一个区块链，还能在面试中把 Nakamoto 共识讲清楚。

> 仓库：[Kunyanli230/Learn_ProofOfWork](https://github.com/Kunyanli230/Learn_ProofOfWork)  ·  10 步  ·  Go 语言

> 本项目的目标是从零构建一个完整的 Nakamoto 共识区块链系统

---

## 项目介绍

这是一个 Go 语言实现的 Nakamoto 共识教学项目，从最基础的 Block 结构开始，逐步加入工作量证明、序列化、BoltDB 持久化、命令行接口、UTXO 交易模型、钱包、Merkle 树和 P2P 多节点网络，最终形成一个完整的分布式共识系统。

## 前置要求

建议具备 Go 基础语法、`crypto/sha256`、`encoding/gob`、数据库和网络编程的基本概念。不需要区块链背景，每一步都有详细代码和说明。

- Go 基础语法与错误处理
- `crypto/sha256` 哈希计算
- `encoding/gob` 序列化
- BoltDB 嵌入式 KV 数据库
- `flag` 命令行参数解析
- ECDSA 椭圆曲线签名（`crypto/ecdsa`）
- `net` 包 TCP 网络编程
- 基础数据结构（链表、树、哈希）

## Level 1：能跑能演示

能启动 3 个节点，完成钱包创建、创世区块生成、交易发送和节点同步，看到完整的区块链输出。

### 达标标准

能从零写 Block + Blockchain 并输出区块信息。

### 证明方式

能画出 Block 结构体和链式连接关系。

### 下一层目标

加入 PoW 挖矿。

## Level 2：面试级理解

能讲清区块结构、PoW 挖矿原理、UTXO 模型、Merkle 树验证、P2P 节点同步协议和 Nakamoto 共识的完整工作流程。

### 达标标准

能把项目讲成 Block → PoW → BoltDB → CLI → UTXO 的工程演化。

### 证明方式

能回答每个模块为什么需要前一个模块。

### 下一层目标

准备 UTXO、签名和网络同步追问。

## Level 3：抗追问能力

能回答为什么 PoW 需要 targetBit=16、UTXO vs Account 模型区别、Merkle 树如何防篡改、网络分区时 Nakamoto 共识如何收敛。

### 达标标准

能解释网络分区时节点如何重新同步。

### 证明方式

能把回答落到源码入口：`handleVersion`、`handleInv`、`sendBlock`。

### 下一层目标

把核心模块背到可以复刻。

## Level 4：可独立复刻

能关掉文档，从零复刻核心模块：Block、PoW、BoltDB、Transaction、Wallet、MerkleTree 和 P2P 网络。

### 达标标准

能从零写出最小可运行的区块链系统。

### 证明方式

能还原目录结构、Block 结构体、PoW 验证和 P2P 通信协议。

### 下一层目标

把项目抽象成分布式共识设计框架。

## Level 5：分布式共识大师

能把 Nakamoto 共识抽象成通用的异步 BFT 前置知识，理解中本聪共识的最终性、分叉选择和概率确认。

### 达标标准

能从项目上升到通用异步BFT方法论。

### 证明方式

能主动讨论 PoW、最长链规则、概率最终性和 51% 攻击。

### 下一层目标

进入异步 BFT 学习。

## 学习方法

先看前言建立地图，再用知识学习逐章理解 10 个模块，用项目拆解按 10 天追源码，最后用面试模拟和场景还原训练表达。

1. 前言：确认目标和学习深度
2. 知识学习：逐章理解 10 个模块
3. 项目拆解：按 10 天追源码
4. 面试模拟：用卡片训练回答结构
5. 场景还原：用端到端和故障题训练追问

## 最终产出

- 一张 Bitcoin/Nakamoto 核心链路图
- Block 结构体 + PoW + UTXO 的完整关系图
- 5 条简历亮点
- 15 道高频面试追问答案
- 一份 10 步复刻路线图
- 一套 Nakamoto 共识通用回答框架

---

# 知识学习

## 第1章：区块与链

### Block 结构体包含哪些字段？每个字段的作用是什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

区块是区块链最基本的存储单元。一个完整的区块包含以下核心字段：

- **Height**：区块高度，从 1 开始自增
- **PrevBlockHash**：前一个区块的 SHA256 哈希值，形成链式连接
- **Data**：区块中存储的交易数据（字节数组）
- **Timestamp**：区块创建时间戳（Unix 时间）
- **Hash**：当前区块的哈希值

这些字段共同保证了区块链的不可篡改性：修改任何历史区块的数据，都会导致后续所有区块的 Hash 变化。

**Level 2：源码分析**

源码在 `001-block/core/Block.go`：

```go
type Block struct {
    Height        int64    // 区块高度
    PrevBlockHash []byte   // 上一个区块 Hash
    Data          []byte   // 交易数据
    Timestamp     int64    // 时间戳
    Hash          []byte   // 当前区块 Hash
}

// SetHash 拼接所有属性后计算 SHA256
func (block *Block) SetHash() {
    heightBytes := IntTOHex(block.Height)
    timeBytes := []byte(strconv.FormatInt(block.Timestamp, 2))
    blockBytes := bytes.Join([][]byte{heightBytes,
        block.PrevBlockHash, block.Data, timeBytes, block.Hash}, []byte{})
    hash := sha256.Sum256(blockBytes)
    block.Hash = hash[:]
}
```

在 `Blockchain.go` 中，Blockchain 用内存切片存储所有区块：

```go
type Blockchain struct {
    Blocks []*Block // 有序区块切片
}
```

**Level 3：深入追问**

**Q: 为什么 Block 的 Hash 不直接存储而是通过 SetHash() 计算？**

Hash 是区块所有数据的摘要，必须依赖内容动态计算。如果直接存储固定的 Hash，就失去了数据完整性校验的意义。

**Q: 创世区块的 PrevBlockHash 为什么是全 0？**

创世区块是链的第一个区块，没有前驱。全 0（`make([]byte, 32)`）是区块链领域的约定，表示这是整条链的起点。

</div>
</details>

### Blockchain 的 AddBlocktoBlockchain 方法做了什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

这个方法负责将新交易数据打包成区块，并追加到区块链末端。核心流程：

1. 调用 `NewBlock(data, height, preHash)` 创建新区块
2. 将新区块 append 到 Blocks 切片

注意：这一步中链表是内存中的，重启即丢失。后面会引入持久化。

**Level 2：源码分析**

```go
// Blockchain.go
func (blc *Blockchain) AddBlocktoBlockchain(
    data string, height int64, preHash []byte) {
    newBlock := NewBlock(data, height, preHash)
    blc.Blocks = append(blc.Blocks, newBlock)
}

func CreateBlockchainWithGenesisBlock() *Blockchain {
    genesisBlock := CreateGenesisBlock("Genesis Data ...")
    return &Blockchain{[]*Block{genesisBlock}}
}
```

**Level 3：深入追问**

**Q: 如果不用切片存储区块，还有什么方案？**

生产环境（如 Bitcoin Core）采用 leveldb/rocksdb 等 KV 数据库，以 Hash 为 key、序列化后的 Block 为 value。这样只需要存储 Tip（链末端 Hash）即可遍历整条链。本项目 004-Persistence 步骤实现了这一点。

**Q: 内存切片方案的问题是什么？**

- 重启丢失所有区块数据
- 大链（数十万区块）内存压力大
- 无法做并发安全的区块操作

</div>
</details>

#### 自检题

- **Block 结构体包含哪几个字段？** — Height, PrevBlockHash, Data, Timestamp, Hash。
- **创世区块有什么特殊之处？** — PrevBlockHash 是全 0（32 字节），Height 为 1。
- **SetHash() 的哈希输入包含哪些数据？** — 高度字节 + 上一区块 Hash + 交易数据 + 时间戳 + 当前 Hash。
- **内存存储区块链的最大问题是什么？** — 重启丢失所有数据，且大链内存压力大。

---

## 第2章：工作量证明（PoW）

### PoW 的核心原理是什么？targetBit 的作用？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

工作量证明（Proof of Work）是 Nakamoto 共识的核心机制。原理很简单：

- 找到一个值（nonce），使区块的 SHA256 哈希值小于目标值（target）
- target 越小，找到满足条件的 nonce 越难
- targetBit=16 意味着 256 位哈希的前 16 位必须为 0

PoW 的三大作用：**竞争记账权**（谁先找到 nonce 谁出块）、**防篡改**（改历史区块需要重算所有后续 nonce）、**安全基础**（51% 攻击需要控制全网 51% 算力）。

**Level 2：源码分析**

源码在 `002-PoW/core/ProofOfWork.go`：

```go
const targetBit = 16

type ProofOfWork struct {
    Block  *Block
    target *big.Int   // 目标值：hash < target 才算成功
}

func NewProofOfWork(block *Block) *ProofOfWork {
    target := big.NewInt(1)
    target = target.Lsh(target, 256-targetBit) // 左移 240 位
    return &ProofOfWork{block, target}
}

func (pow *ProofOfWork) Run() ([]byte, int64) {
    nonce := 0
    var hashInt big.Int
    var hash [32]byte
    for {
        dataBytes := pow.prepareData(nonce)
        hash = sha256.Sum256(dataBytes)
        hashInt.SetBytes(hash[:])
        if pow.target.Cmp(&hashInt) == 1 { break } // 找到了！
        nonce++
    }
    return hash[:], int64(nonce)
}
```

**Level 3：深入追问**

**Q: targetBit=16 意味着什么难度？**

target = 1 << 240 = 2^240。哈希值范围 0~2^256-1，所以满足 hash < 2^240 的概率约为 2^240/2^256 = 1/2^16 = 1/65536。平均需要尝试约 65536 次 nonce。

**Q: 为什么 PoW 不影响区块链的可用性？**

PoW 只在创建新区块时执行。验证区块只需要一次哈希对比：`hashInt.Cmp(pow.target) == 1`，O(1) 复杂度。这就是"易验证、难计算"的非对称特性。

</div>
</details>

### prepareData 拼接了哪些数据？Nonce 在哪里？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

挖矿时，需要将区块的关键属性拼接成字节数组，然后计算 SHA256。这个过程就是 `prepareData` 的职责。Nonce 是唯一变化的变量——通过不断改变 Nonce 来寻找满足条件的哈希。

**Level 2：源码分析**

```go
func (pow *ProofOfWork) prepareData(nonce int) []byte {
    return bytes.Join([][]byte{
        pow.Block.PrevBlockHash,
        pow.Block.Data,
        IntTOHex(pow.Block.Timestamp),
        IntTOHex(int64(targetBit)),
        IntTOHex(int64(nonce)),      // ← nonce
        IntTOHex(int64(pow.Block.Height)),
    }, []byte{})
}
```

**Level 3：深入追问**

**Q: Nonce 溢出怎么办？**

int64 的 Nonce 最大约 9.22×10^18。在当前 targetBit=16 下足够，但在 Bitcoin 主网 targetBit 动态调整的情况下，矿工还会改动 timestamp 或 coinbase 交易的 extraNonce 来获得更多搜索空间。

</div>
</details>

#### 自检题

- **PoW 的三大作用是什么？** — 竞争记账权（出块激励）、防篡改（改历史需要重算所有 nonce）、安全基础（51% 攻击）。
- **targetBit=16 时，平均需要尝试多少次 nonce？** — 约 65536 次（2^16）。
- **验证 PoW 需要多大计算量？** — O(1)，一次哈希比较即可。
- **Nonce 溢出时矿工会怎么办？** — 改动 timestamp 或使用 extraNonce 扩展搜索空间。

---

## 第3章：序列化

### 为什么需要 Blocks 序列化？gob 是什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

序列化是将内存中的结构体转换为可在网络传输或存储的字节数组。在区块链中有两个关键用途：

- **持久化存储**：将 Block 写入数据库（BoltDB）需要序列化
- **网络传输**：多节点间同步区块时需要序列化

Go 的 `encoding/gob` 是标准库自带的二进制序列化方案，比 JSON 更紧凑，比 protobuf 零依赖。

**Level 2：源码分析**

源码在 `003-Serialize/core/Block.go`：

```go
func (block *Block) Serialize() []byte {
    var result bytes.Buffer
    encoder := gob.NewEncoder(&result)
    err := encoder.Encode(block)
    if err != nil { log.Panic(err) }
    return result.Bytes()
}

func DeserializeBlock(blockBytes []byte) *Block {
    var block Block
    decoder := gob.NewDecoder(bytes.NewReader(blockBytes))
    err := decoder.Decode(&block)
    if err != nil { log.Panic(err) }
    return &block
}
```

使用方式（main.go）：

```go
block := BLC.NewBlock("Test", 1, make([]byte, 32))
bytes := block.Serialize()
block = BLC.DeserializeBlock(bytes)
// block.Nonce 和 block.Hash 被完整恢复
```

**Level 3：深入追问**

**Q: gob vs JSON vs protobuf？**

- gob：零依赖，二进制格式，Go 原生支持，但跨语言差
- JSON：可读性好，跨语言强，但体积大、性能差
- protobuf：高性能、小体积、跨语言，但需要 .proto 文件和编译步骤
- Bitcoin 使用自定义二进制格式（CompactSize + 固定长度），比 gob 更紧凑

**Q: gob 注册类型的重要性？**

gob 默认能序列化内置类型和导出的结构体字段。如果有接口类型，必须用 `gob.Register()` 注册具体类型。

</div>
</details>

#### 自检题

- **序列化在区块链中有哪两个关键用途？** — 持久化存储（写入数据库）和网络传输（多节点同步）。
- **gob 相比 JSON 的优势是什么？** — 二进制格式更紧凑，Go 原生支持，零外部依赖。
- **Serialize 和 DeserializeBlock 分别返回什么？** — Serialize 返回 []byte，DeserializeBlock 返回 *Block。
- **gob 序列化时有什么注意事项？** — 字段必须导出（首字母大写），接口类型需要 gob.Register 注册。

---

## 第4章：持久化存储（BoltDB）

### BoltDB 如何替换内存存储？Blockchain 结构体发生了什么变化？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

持久化是区块链走向生产环境的关键一步。BoltDB 是一个 Go 实现的嵌入式 KV 数据库，事务支持 ACID，适合单机场景。

- 替换前：`Blockchain{Blocks []*Block}` —— 内存切片
- 替换后：`Blockchain{Tip []byte, DB *bolt.DB}` —— 只存末端 Hash + 数据库句柄

需要遍历整条链时，使用 **迭代器模式**——从 Tip 开始，沿着 PrevBlockHash 反向遍历所有区块。

**Level 2：源码分析**

源码在 `004-Persistence/core/Blockchain.go`：

```go
const dbName = "blockchain.db"
const blockTableName = "blocks"

type Blockchain struct {
    Tip []byte     // 最新区块的 Hash
    DB  *bolt.DB   // BoltDB 实例
}

func CreateBlockchainWithGenesisBlock() *Blockchain {
    db, _ := bolt.Open(dbName, 0600, nil)
    var blockHash []byte
    db.Update(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(blockTableName))
        if b == nil { b, _ = tx.CreateBucket([]byte(blockTableName)) }
        genesisBlock := CreateGenesisBlock("Genesis Data ...")
        b.Put(genesisBlock.Hash, genesisBlock.Serialize())
        b.Put([]byte("l"), genesisBlock.Hash) // "l" 键存最新 Hash
        blockHash = genesisBlock.Hash
        return nil
    })
    return &Blockchain{blockHash, db}
}
```

**Level 3：深入追问**

**Q: 为什么从内存切片改为只存 Tip？**

生产环境的区块链可能有数十万区块，全量加载到内存不可行。只存 Tip 可以 O(1) 获取最新区块，迭代器按需读取历史区块。

**Q: BoltDB 为什么适合区块链？**

- ACID 事务保证数据一致性
- B+ 树索引，按 Hash 查询 O(log N)
- 嵌入进程内，零运维
- MVCC 支持并发读

</div>
</details>

### BlockchainIterator 是如何工作的？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

迭代器模式允许从最新区块（Tip）开始，沿着 `PrevBlockHash` 链反向遍历所有区块。每次调用 `Next()` 返回当前区块，并将 `CurrentHash` 更新为前一个区块的 Hash。

**Level 2：源码分析**

```go
type BlockchainIterator struct {
    CurrentHash []byte
    DB          *bolt.DB
}

func (iter *BlockchainIterator) Next() *Block {
    var block *Block
    iter.DB.View(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(blockTableName))
        currentBlockBytes := b.Get(iter.CurrentHash)
        block = DeserializeBlock(currentBlockBytes)
        iter.CurrentHash = block.PrevBlockHash // 回退一步
        return nil
    })
    return block
}
```

**Level 3：深入追问**

**Q: 如何知道遍历结束了？**

当 `PrevBlockHash` 为全 0 时，说明到达了创世区块。Printchain 中用 `big.NewInt(0).Cmp(&blockHashInt) == 0` 判断。

</div>
</details>

#### 自检题

- **持久化后 Blockchain 结构体包含哪两个字段？** — Tip（最新区块 Hash）和 DB（BoltDB 实例）。
- **迭代器遍历到创世区块时如何判断结束？** — PrevBlockHash 为全 0。
- **BoltDB 中如何存储最新区块的 Hash？** — 用 key="l" 存储，每次添加区块时更新。

---

## 第5章：命令行接口（CLI）

### CLI 模块的设计思路？flag 包如何实现子命令？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

CLI（命令行接口）让用户通过终端命令与区块链交互。Go 的 `flag` 标准库支持子命令定义和参数解析。

核心设计：

1. 使用 `os.Args[1]` 判断子命令（如 addBlock、printchain）
2. 每个子命令都有独立的 `flag.FlagSet` 管理参数
3. 未识别的命令打印 Usage 帮助

**Level 2：源码分析**

源码在 `005-cli/main.go`：

```go
func main() {
    addBlockCmd := flag.NewFlagSet("addBlock", flag.ExitOnError)
    printChainCmd := flag.NewFlagSet("printchain", flag.ExitOnError)

    flagAddBlockData := addBlockCmd.String("data", "Hello Chain", "交易数据")

    switch os.Args[1] {
    case "addBlock":
        addBlockCmd.Parse(os.Args[2:])
    case "printchain":
        printChainCmd.Parse(os.Args[2:])
    default:
        printUsage()
        os.Exit(1)
    }
}
```

**Level 3：深入追问**

**Q: flag vs cobra？**

flag 是 Go 标准库，零依赖，适合简单场景。cobra 是 Kubernetes 使用的 CLI 框架，支持嵌套子命令、自动帮助生成、bash 补全等，适合复杂 CLI 应用。

</div>
</details>

#### 自检题

- **CLI 使用 Go 的哪个标准库？** — flag。
- **如何实现 addBlock 子命令？** — flag.NewFlagSet("addBlock", flag.ExitOnError) 创建独立 FlagSet，用 os.Args[1] 匹配。

---

## 第6章：持久化+CLI 整合

### 整合后的项目目录结构是怎样的？依赖关系是什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

经过前几步的积累，项目形成了清晰的模块化结构：

- **core/**：区块结构、区块链、PoW、交易
- **crypto/**：钱包、Base58、签名
- **store/**：BoltDB 持久化、迭代器
- **node/**：CLI 命令解析
- **network/**：P2P 通信
- **config/**：配置文件
- **logger/**：日志
- **pool/**：交易池

通过 go build 编译为可执行文件，通过子命令控制流程。

**Level 2：源码分析**

```bash
# CLI 用法例子
go build -o bc.exe main.go
./bc.exe createblockchain "任意数据"
./bc.exe addblock -data "Send 100 USDT to KY"
./bc.exe printchain
```

**Level 3：深入追问**

**Q: CLI 模式下如何管理数据库？**

每个命令都需要打开和关闭 BoltDB。在 010 多节点模式中，每个节点有独立的数据库文件（如 blockchain_3000.db），通过 NODE_ID 环境变量区分。

</div>
</details>

#### 自检题

- **项目有哪些核心目录？** — core、crypto、store、node、network、config、logger、pool。
- **go build -o bc.exe main.go 的作用是什么？** — 编译 Go 项目为可执行文件 bc.exe。

---

## 第7章：UTXO 交易模型

### UTXO 模型和 Account 模型有什么区别？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

UTXO（Unspent Transaction Output）是 Bitcoin 使用的交易模型：

- 每笔交易引用之前的未花费输出，作为新交易的输入
- 交易输出被花费后就不可再引用
- 余额 = 所有未花费输出的总和（没有显式的"余额"字段）

对比 Account 模型（如 Ethereum）：

- Account 模型维护全局账户余额，转账直接加减
- UTXO 模型需要遍历所有历史交易来验证资金来源

UTXO 的优势：并行验证（每笔交易独立）、隐私性更好、防双花更简单。

**Level 2：源码分析**

源码在 `007-transaction/core/Transaction.go`：

```go
type Transaction struct {
    TxHash []byte      // 交易哈希
    Vins   []*TXInput   // 输入（引用之前的 UTXO）
    Vouts  []*TXOutput  // 输出（产生新 UTXO）
}

type TXInput struct {
    TxHash    []byte  // 引用的交易 Hash
    Vout      int     // 引用的输出索引
    ScriptSig string  // 解锁脚本（签名）
}

type TXOutput struct {
    Value       int64  // 金额
    ScriptPubKey string  // 锁定脚本（地址）
}
```

Coinbase 交易（挖矿奖励）：

```go
func NewCoinbaseTransaction(address string) *Transaction {
    txInput := &TXInput{[]byte{}, -1, "Genesis Block"}
    txOutput := &TXOutput{10, address}
    return &Transaction{[]byte{}, []*TXInput{txInput}, []*TXOutput{txOutput}}
}
```

**Level 3：深入追问**

**Q: 如何判断交易是 Coinbase 交易？**

Coinbase 交易的特征：Vins 长度为 1，且 Vins[0].TxHash 为空（0 长度）、Vout 为 -1。这是挖矿奖励交易，没有实际输入。

**Q: UTXO 模型的"找零"怎么实现？**

如果 A 有 10 BTC 的 UTXO，发送 3 BTC 给 B，需要创建两个输出：输出 1：3 BTC → B；输出 2：7 BTC → A（找零）。输入总额 - 输出总额 = 矿工费。

</div>
</details>

### FindSpendableUTXOs 方法的逻辑是什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

这个方法负责查找一个地址所有可花费的 UTXO 并计算总余额。核心思路：遍历区块链上所有交易的所有输出，过滤出"未被花费"且"属于该地址"的输出。

**Level 2：源码分析**

```go
func (blockchain *Blockchain) FindSpendableUTXOs(
    from string, amount int, txs []*Transaction,
) (int64, map[string][]int) {
    // 遍历所有未花费输出，累加直到满足 amount
    // 返回：总可用金额 + 可花费 UTXO 集合
}
```

**Level 3：深入追问**

**Q: UTXO 集合查找性能优化？**

遍历全链查找 UTXO 非常慢。Bitcoin Core 维护单独的 UTXO Set（chainstate leveldb），010-network 步骤中也实现了 UTXOSet.ResetUTXOSet()。

</div>
</details>

#### 自检题

- **UTXO 模型和 Account 模型的核心区别？** — UTXO 引用历史输出，无显式余额；Account 维护全局账户余额。
- **交易的三要素是什么？** — TxHash（交易哈希）、Vins（输入）、Vouts（输出）。
- **Coinbase 交易的特殊标记是什么？** — Vins[0].TxHash 长度为 0 且 Vout 为 -1。
- **找零输出是如何生成的？** — 输入总额减去转账金额，生成一个输出回到发送方地址。

---

## 第8章：钱包（Wallet）

### 钱包地址是如何生成的？Base58 编码的作用？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

钱包是区块链的身份标识。钱包地址的生成流程：

1. **ECDSA 密钥对**：crypto/ecdsa + P256 曲线生成私钥和公钥
2. **SHA256 → RIPEMD160**：公钥先 SHA256 再 RIPEMD160，得到 20 字节哈希
3. **添加版本号**：前面加 0x00 版本字节
4. **校验和**：双 SHA256 取前 4 字节
5. **Base58 编码**：拼接后编码为可读地址

Base58 与 Base64 的区别：去掉了容易混淆的字符（0、O、I、l、+、/），更适合人工阅读和输入。

**Level 2：源码分析**

源码在 `008-Wallet/crypto/wallet.go`：

```go
func NewWallet() *Wallet {
    privateKey, publicKey := newKeyPair()
    return &Wallet{privateKey, publicKey}
}

func newKeyPair() (ecdsa.PrivateKey, []byte) {
    curve := elliptic.P256()
    private, _ := ecdsa.GenerateKey(curve, rand.Reader)
    pubKey := append(private.PublicKey.X.Bytes(),
        private.PublicKey.Y.Bytes()...)
    return *private, pubKey
}

func (w *Wallet) GetAddress() []byte {
    ripemd160Hash := Ripemd160Hash(w.PublicKey)
    version_ripemd160Hash := append([]byte{0x00}, ripemd160Hash...)
    checksumBytes := CheckSum(version_ripemd160Hash)
    bytes := append(version_ripemd160Hash, checksumBytes...)
    return Base58Encode(bytes)
}
```

Base58 编码（`crypto/base58.go`）去掉了易混淆字符：

```go
var b58Alphabet = []byte("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
```

**Level 3：深入追问**

**Q: 为什么需要双哈希（SHA256 + RIPEMD160）？**

SHA256 提供强抗碰撞性，RIPEMD160 将 32 字节哈希压缩到 20 字节，减少地址长度。中本聪选择 RIPEMD160 可能是为了避免 SHA256 在签名验证中的潜在弱点。

**Q: 校验和的作用？**

防止用户输入错误地址。如果地址中一个字符被误输入，重新计算的校验和会不匹配，可以检测出错误。

</div>
</details>

### Wallets 集合如何管理多个钱包？gob 序列化有什么坑？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

一个用户可能有多个钱包（多个密钥对）。Wallets 集合使用 `map[string]*Wallet` 管理，key 为地址，value 为钱包对象。通过 gob 序列化保存到 `wallets.dat` 文件。

**Level 2：源码分析**

```go
type Wallets struct {
    WalletsMap map[string]*Wallet
}

func (w *Wallets) SaveWallets() {
    var content bytes.Buffer
    encoder := gob.NewEncoder(&content)
    encoder.Encode(&w)
    ioutil.WriteFile(walletFile, content.Bytes(), 0644)
}
```

**Wallet 的 GobEncode/GobDecode**：由于 `ecdsa.PrivateKey` 包含未导出字段，gob 默认无法序列化。需要自定义 `GobEncode()` 和 `GobDecode()` 方法，手动序列化私钥 D 和公钥字节。

**Level 3：深入追问**

**Q: gob 为什么序列化不了 ecdsa.PrivateKey？**

ecdsa.PrivateKey 内部包含椭圆曲线对象（elliptic.Curve），该接口有未导出方法和字段，gob 拒绝编码。自定义 GobEncode/GobDecode 是标准解决方案。

</div>
</details>

#### 自检题

- **钱包地址生成的 5 步流程是什么？** — ECDSA密钥对 → SHA256+RIPEMD160 → 版本号 → 校验和 → Base58编码。
- **Base58 和 Base64 的核心区别？** — Base58 去掉了 0 O I l + / 等易混淆字符。
- **为什么需要自定义 GobEncode？** — ecdsa.PrivateKey 包含未导出字段，gob 默认无法序列化。

---

## 第9章：默克尔树（Merkle Tree）

### Merkle 树的结构和用途？叶子节点的哈希如何计算？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

默克尔树是一种二叉树结构，叶子节点存储交易哈希，非叶子节点存储左右子节点哈希拼接后再哈希的值。

核心用途：

- **高效验证**：只需 O(log N) 个哈希值即可验证某笔交易是否在区块中（SPV 验证）
- **防篡改**：任何交易的修改都会改变 Merkle Root
- **轻节点**：手机钱包只需下载区块头（含 Merkle Root）即可验证交易

**Level 2：源码分析**

源码在 `009-MerkleTree/core/merkle_tree.go`：

```go
type MerkleTree struct {
    RootNode *MerkleNode
}

type MerkleNode struct {
    Left  *MerkleNode
    Right *MerkleNode
    Data  []byte
}

func NewMerkleNode(left, right *MerkleNode, data []byte) *MerkleNode {
    if left == nil && right == nil {
        hash := sha256.Sum256(data)   // 叶子节点：直接哈希
        return &MerkleNode{Data: hash[:]}
    }
    prevHashes := append(left.Data, right.Data...)
    hash := sha256.Sum256(prevHashes) // 非叶子：拼接后哈希
    return &MerkleNode{left, right, hash[:]}
}
```

奇数个叶子节点的处理：复制最后一个节点使其成对。

**Level 3：深入追问**

**Q: Merkle Proof 如何工作？**

验证某笔交易在区块中，只需提供：该交易的哈希 + 从叶子到根路径上所有兄弟节点的哈希。验证者从交易的哈希开始，逐层与兄弟哈希拼接计算，最终比对 Merkle Root 是否一致。

**Q: 为什么 Bitcoin 使用双 SHA256（SHA256(SHA256(x))）？**

双哈希可以防止长度扩展攻击（length-extension attack）。SHA256 的 Merkle-Damgård 结构存在此弱点，双哈希是简单有效的防御。

</div>
</details>

#### 自检题

- **Merkle 树的两个核心用途？** — 高效 SPV 验证（O(log N)）和防篡改（Merkle Root）。
- **叶子节点和非叶子节点的哈希计算有何不同？** — 叶子直接 SHA256(data)，非叶子 SHA256(leftHash + rightHash)。
- **奇数个叶子怎么处理？** — 复制最后一个节点使其成对。

---

## 第10章：P2P 网络与 Nakamoto 共识

### 多节点通信包含哪些协议命令？version、inv、getblocks、getdata、block 的作用？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

Nakamoto 共识的 P2P 网络使用简单的 TCP 协议，自定义了以下命令：

- **version**：节点启动时发送，交换版本号和链高度
- **inv**（inventory）：通知对等节点自己有哪些区块哈希
- **getblocks**：请求对方发送区块哈希列表
- **getdata**：请求特定区块的完整数据
- **block**：发送完整区块数据

消息格式：`COMMANDLENGTH 字节命令名 + gob 序列化的结构体`

**Level 2：源码分析**

源码在 `010-network/network/Server.go`：

```go
func handleConnection(conn net.Conn, bc *store.Blockchain) {
    request, _ := ioutil.ReadAll(conn)
    command := bytesToCommand(request[:COMMANDLENGTH])
    switch command {
    case COMMAND_VERSION:
        handleVersion(request, bc)
    case COMMAND_ADDR:
        handleAddr(request, bc)
    case COMMAND_BLOCK:
        handleBlock(request, bc)
    case COMMAND_INV:
        handleInv(request, bc)
    case COMMAND_GET_BLOCKS:
        handleGetBlocks(request, bc)
    case COMMAND_GETDATA:
        handleGetData(request, bc)
    }
}
```

**Level 3：深入追问**

**Q: 节点同步的完整流程是什么？**

1. 新节点启动 → sendVersion(knowNodes[0], bc)
2. 主节点收到 version → 比较 BestHeight → 如果对方更高，sendGetBlocks
3. 主节点 sendInv 发送区块哈希列表
4. 新节点收到 inv → sendGetData 逐个请求区块
5. 主节点 sendBlock 逐个发送完整区块

**Q: 为什么使用 TCP 自定义协议而不是 HTTP/gRPC？**

P2P 网络需要长连接（持续同步区块和交易），HTTP 请求-响应模式不适合。gRPC 增加依赖，对于教学项目来说，直接 TCP + gob 更透明。

</div>
</details>

### Nakamoto 共识的三个核心规则是什么？

<details class="qa-answer">
<summary class="qa-answer-toggle">查看答案</summary>

<div class="qa-answer-body">

**Level 1：基础理解**

Nakamoto 共识通过三条规则实现去中心化一致性：

1. **PoW 出块**：节点竞争解决哈希难题，第一个解决的广播新区块
2. **最长链规则**：节点始终在最长链上挖矿。如果收到更长的链，切换过去
3. **概率最终性**：区块被确认的次数越多，被回滚的概率越低（6 次确认在 Bitcoin 被认为是安全的）

**Level 2：源码分析**

version 处理中的高度比较体现了最长链规则：

```go
func handleVersion(request []byte, bc *store.Blockchain) {
    bestHeight := bc.GetBestHeight()
    foreignerBestHeight := payload.BestHeight
    if bestHeight > foreignerBestHeight {
        sendVersion(payload.AddrFrom, bc) // 我更高，告诉对方
    } else if bestHeight < foreignerBestHeight {
        sendGetBlocks(payload.AddrFrom)    // 对方更高，请求同步
    }
}
```

**Level 3：深入追问**

**Q: 网络分区时 Nakamoto 共识如何收敛？**

分区期间各自出块形成分叉。网络恢复后，最长链规则让所有节点自动收敛到最长链。短链上的区块成为"孤块"。

**Q: 51% 攻击如何工作？**

攻击者控制全网 51% 以上算力后，可以秘密构建比公开链更长的链。公开后，全网节点切换到攻击者的链，回滚公开链上的交易。这就是为什么 Bitcoin 需要 6 次确认——让攻击者在概率上不可能追上线。

</div>
</details>

#### 自检题

- **P2P 网络有哪 5 个核心协议命令？** — version, inv, getblocks, getdata, block。
- **节点同步的 5 步流程？** — sendVersion → handleVersion → sendInv → sendGetData → sendBlock。
- **Nakamoto 共识的三条核心规则？** — PoW 出块、最长链规则、概率最终性。
- **handleVersion 中如何实现最长链规则？** — 比较 BestHeight，对方更高时 sendGetBlocks，自己更高时 sendVersion。

---

# 项目拆解（10 天）

> 仓库：LeoninCS/GoClub  ·  10 天

## 学习方法论

- **增量式学习**：每天在上一天代码基础上加一个模块，让复杂度线性增长而非指数爆炸。
- **源码导向**：每个知识点都绑定具体文件和代码行数，形成可追踪的知识图谱。
- **面试视角**：每天拆解的不是代码而是面试表达——这段代码怎么讲才能让面试官听懂。
- **动手验证**：每天有命令行操作和自检题，确保"看到了"变成"能跑了"。

## 面试答题框架

1. 先给结论
2. 解释业务场景
3. 指出源码入口
4. 展开核心链路
5. 补充风险和扩展

## 完成评分尺

- **能画图**：Block结构、PoW流程、UTXO链路都能在白板上画清楚。
- **能指代码**：每个亮点都有文件路径和函数名支撑。
- **能讲权衡**：UTXO vs Account、PoW vs PoS、BoltDB vs LevelDB。
- **能接追问**：追问能回到共识安全、分叉处理和概率最终性。

---

### Day 1：区块与链

**目标：** 理解 Block 结构体和 Blockchain 的链式存储，跑通创世区块和新区块的添加。

**核心关注点：**

- Block 结构体
- SetHash 哈希计算
- Blockchain 内存存储
- CreateGenesisBlock

**源码入口：** `001-block/core/Block.go`、`001-block/core/Blockchain.go`、`001-block/core/utils.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">Block 结构体的设计为什么选择这些字段？</summary>

<div class="qa-answer-body">

Block 的结构是从 Bitcoin 白皮书简化而来的。Height 用于定位，PrevBlockHash 形成链，Data 存交易，Timestamp 提供时间序，Hash 是完整性摘要。这 5 个字段已经能支撑一个基本的区块链。

阅读 `001-block/core/Block.go` 中的 Block 结构体定义和 SetHash 方法。注意 SetHash 中如何拼接所有字段。

**面试表达：** Block 是区块链的原子单元，5 个字段通过 SHA256 形成不可篡改的链式结构。改任何历史区块的数据都会改变该区块的 Hash，从而破坏后续所有区块的 PrevBlockHash 链。

</div>
</details>

**今日任务：**

- 画出 Block 结构体五字段图
- 手写 NewBlock 和 CreateGenesisBlock 的代码
- 解释为什么 PrevBlockHash 在创世区块中为全0
- 跑通 main.go 并观察区块输出

**自检题：**

- **Block 结构体包含哪 5 个字段？** — Height、PrevBlockHash、Data、Timestamp、Hash。
- **创世区块的 Height 是多少？** — Height = 1，PrevBlockHash 为 make([]byte, 32)。
- **SetHash 的输入包含什么？** — 高度、前一个 Hash、数据、时间戳、当前 Hash。

---

### Day 2：工作量证明

**目标：** 掌握 PoW 挖矿原理，理解 targetBit 和 nonce 的关系。

**核心关注点：**

- ProofOfWork 结构体
- target 计算
- Run() 挖矿循环
- IsValid 验证

**源码入口：** `002-PoW/core/ProofOfWork.go`、`002-PoW/core/Block.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">PoW 挖矿循环中做了哪些事？</summary>

<div class="qa-answer-body">

nonce 从 0 开始自增，每次迭代计算 `SHA256(prepareData(nonce))`，和 target 比较。如果 hash < target，挖矿成功；否则 nonce++ 继续尝试。

`ProofOfWork.go:Run()` 中，先用 `prepareData(nonce)` 拼接数据，再计算 SHA256，用 `hashInt.SetBytes(hash[:])` 和 `target.Cmp` 比较。

**面试表达：** PoW 的核心是"找到一个 nonce 使区块哈希小于目标值"。这是易验证（O(1)）、难计算（O(2^n)）的非对称操作，构成了比特币的安全基础。

</div>
</details>

**今日任务：**

- 画 PoW 挖矿流程图
- 解释 targetBit=16 的含义（平均尝试次数）
- 手写 NewProofOfWork 的 target 计算
- 跑通挖矿并观察 nonce 值

**自检题：**

- **PoW 的目标是什么不等式？** — hashInt < pow.target（区块哈希小于目标值）。
- **targetBit=16 时平均尝试多少次？** — 约 2^16 = 65536 次。
- **IsValid 做了什么验证？** — 比较 block.Hash 对应的 big.Int 是否小于 target。

---

### Day 3：序列化

**目标：** 理解 gob 序列化/反序列化机制，为持久化和网络传输打基础。

**核心关注点：**

- gob Encode/Decode
- Serialize/DeserializeBlock
- bytes.Buffer 使用

**源码入口：** `003-Serialize/core/Block.go`、`003-Serialize/main.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">为什么序列化是持久化和网络传输的桥梁？</summary>

<div class="qa-answer-body">

内存中的 Block 结构体不能直接写入磁盘或通过网络发送。序列化将其转化为字节数组，反序列化则是逆过程。gob 是 Go 标准库的二进制序列化方案。

`Block.Serialize()` 创建 gob.Encoder，编码 block 到 bytes.Buffer。`DeserializeBlock()` 创建 gob.Decoder，从字节流解码回 *Block。

**面试表达：** 序列化让不可传输的结构体变成可传输的字节流。在区块链中，序列化后的 Block 才能持久化到数据库（BoltDB）和通过 P2P 网络传输。

</div>
</details>

**今日任务：**

- 手写 Serialize 和 DeserializeBlock
- 对比 gob、JSON、protobuf 的优劣
- 验证序列化前后 Nonce 和 Hash 恢复正确

**自检题：**

- **gob.NewEncoder 的输出写到哪里？** — bytes.Buffer，最终转成 []byte。
- **Serialize 返回什么类型？DeserializeBlock 接受什么类型？** — Serialize 返回 []byte，DeserializeBlock 接受 []byte。

---

### Day 4：持久化存储

**目标：** 用 BoltDB 替换内存存储，掌握迭代器模式遍历区块链。

**核心关注点：**

- BoltDB 桶机制
- Blockchain 新结构体
- 迭代器 Next()
- Printchain 输出

**源码入口：** `004-Persistence/core/Blockchain.go`、`004-Persistence/core/Blockchainiterator.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">BoltDB 的 Bucket 是什么？</summary>

<div class="qa-answer-body">

Bucket 是 BoltDB 中的"表"概念。本项目用 blocks 桶存储所有区块，用 key="l" 存最新区块 Hash。`bolt.Open(dbName, 0600, nil)` 打开数据库。

`CreateBlockchainWithGenesisBlock` 在事务中先创建 Bucket，再写入创世区块并设 key="l"。`AddBlocktoBlockchain` 在事务中写入新区块并更新 key="l"。

**面试表达：** BoltDB 是 Go 的嵌入式 KV 数据库。区块链用 Hash 作为 key、序列化后的 Block 作为 value 存储。迭代器从 Tip 沿着 PrevBlockHash 反向遍历全链。

</div>
</details>

**今日任务：**

- 画 BoltDB 存储结构图
- 手写 BlockchainIterator.Next()
- 理解 key='l' 的作用
- 跑通 printchain 输出所有区块

**自检题：**

- **BoltDB 中用哪个 key 存储最新区块 Hash？** — key='l'。
- **迭代器 Next() 如何更新 CurrentHash？** — CurrentHash = block.PrevBlockHash。
- **如何判断遍历结束？** — PrevBlockHash 为全 0（big.NewInt(0).Cmp(&hashInt) == 0）。

---

### Day 5：CLI 模块

**目标：** 用 flag 包搭建命令行接口，支持 addBlock 和 printchain 子命令。

**核心关注点：**

- flag.NewFlagSet
- os.Args 解析
- 子命令路由

**源码入口：** `005-cli/main.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">flag.NewFlagSet 如何实现子命令？</summary>

<div class="qa-answer-body">

每个子命令创建独立的 FlagSet，用 `os.Args[1]` switch-case 分发。addBlock 子命令通过 `-data` 参数传入交易数据。

`flag.NewFlagSet("addBlock", flag.ExitOnError)` 创建独立 FlagSet，`addBlockCmd.String("data", ...)` 注册参数。

**面试表达：** CLI 是用户与区块链交互的入口。本项目用 Go 标准库 flag 实现子命令路由，生产环境推荐用 cobra 框架。

</div>
</details>

**今日任务：**

- 手写 addBlock 和 printchain 子命令
- 理解 os.Args[1:] 的参数解析
- 跑通 go build 编译可执行文件

**自检题：**

- **flag.NewFlagSet 的第一个参数是什么？** — 子命令名称（如 "addBlock"）。
- **flag.ExitOnError 的作用？** — 解析失败时直接退出程序。

---

### Day 6：持久化+CLI

**目标：** 整合持久化存储和 CLI，形成完整的本地区块链命令行工具。

**核心关注点：**

- createblockchain 命令
- addblock 持久化
- 迭代器输出
- 模块化目录

**源码入口：** `006-Persistence_cli/main.go`、`006-Persistence_cli/node/CLI.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">整合后 CLI 支持哪些命令？</summary>

<div class="qa-answer-body">

createblockchain：创建区块链并写入创世区块。addblock -data：添加新区块。printchain：打印所有区块信息。getbalance -address：查询地址余额。send：发送交易。

CLI 模块在 node/CLI.go 中实现完整命令路由，每个命令打开 BoltDB → 执行操作 → 关闭数据库。

**面试表达：** 整合后的 CLI 是一个完整的本地区块链工具。用户可以创建区块链、添加区块数据、查看全链状态，是理解区块链工作流程的最小闭环。

</div>
</details>

**今日任务：**

- 跑通 createblockchain → addblock → printchain 全流程
- 画出模块间依赖关系图
- 理解 CLI 中 BoltDB 的打开/关闭逻辑

**自检题：**

- **createblockchain 命令做了什么？** — 创建 BoltDB 数据库并写入创世区块。
- **CLI 模块在哪个目录？** — node/ 目录。

---

### Day 7：UTXO 交易模型

**目标：** 掌握 UTXO 交易模型的输入/输出结构，理解 Coinbase 交易和找零机制。

**核心关注点：**

- Transaction 结构体
- TXInput/TXOutput
- UTXO 查找
- NewCoinbaseTransaction

**源码入口：** `007-transaction/core/Transaction.go`、`007-transaction/core/Transaction_UTXO.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">UTXO 与 Account 模型的设计差异？</summary>

<div class="qa-answer-body">

UTXO 记录每笔交易"输入引用谁"和"输出给谁"，没有全局余额。Account 维护全局账户余额表。UTXO 的优势是并行验证和隐私性。

`Transaction` 结构体包含 TxHash + Vins + Vouts。Coinbase 交易无输入引用（Vout=-1）。普通交易用 `NewSimpleTransaction(from, to, amount)` 创建。

**面试表达：** UTXO 模型是 Bitcoin 的核心创新。每笔交易消费之前的 UTXO 并产生新的 UTXO，没有显式余额，但去中心化验证更简单。

</div>
</details>

**今日任务：**

- 画出 UTXO 交易链路图
- 手写 NewCoinbaseTransaction
- 理解 FindSpendableUTXOs 的查找逻辑
- 跑通转账和找零

**自检题：**

- **Transaction 的三要素是什么？** — TxHash、Vins（输入）、Vouts（输出）。
- **Coinbase 交易的 Vout 为什么是 -1？** — 表示没有引用之前的输出，是挖矿奖励。
- **找零输出是什么？** — 输入总额减去转账金额，输出回发送方地址。

---

### Day 8：钱包

**目标：** 实现 ECDSA 密钥对、Base58 地址编码和钱包集合管理。

**核心关注点：**

- ECDSA P256 密钥对
- SHA256+RIPEMD160
- Base58 编码
- Wallets 管理

**源码入口：** `008-Wallet/crypto/wallet.go`、`008-Wallet/crypto/base58.go`、`008-Wallet/crypto/Wallets.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">钱包地址的完整生成链路？</summary>

<div class="qa-answer-body">

私钥 → 公钥（ECDSA P256）→ SHA256 → RIPEMD160 → 加版本号 → 双 SHA256 取前4字节做校验和 → Base58 编码 → 最终地址。

`Wallet.GetAddress()` 依次调用 Ripemd160Hash、CheckSum、Base58Encode。Wallets 集合用 gob 序列化到 wallets.dat。

**面试表达：** 钱包地址通过多步哈希和编码生成：SHA256 做一层哈希保证均匀分布，RIPEMD160 压缩长度，双 SHA256 校验和防输入错误，Base58 编码提高可读性。

</div>
</details>

**今日任务：**

- 手写地址生成流程
- 理解 Base58 字母表设计
- 解释 GobEncode 为什么需要自定义
- 跑通 createwallet 和 addresslists

**自检题：**

- **地址生成的 5 步流程？** — ECDSA密钥对 → SHA256+RIPEMD160 → 版本号 → 校验和 → Base58编码。
- **Base58 去掉了哪些字符？** — 0 O I l + / 等易混淆字符。
- **为什么需要 GobEncode/GobDecode？** — ecdsa.PrivateKey 含未导出字段，gob 默认不支持。

---

### Day 9：Merkle 树

**目标：** 理解 Merkle 树的结构、构建算法和 SPV 验证原理。

**核心关注点：**

- MerkleNode/MerkleTree
- 叶子节点哈希
- 奇数节点处理
- Merkle Root

**源码入口：** `009-MerkleTree/core/merkle_tree.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">Merkle 树如何构建？叶子节点和内部节点有什么区别？</summary>

<div class="qa-answer-body">

将所有交易哈希作为叶子节点 → 两两成对拼接后 SHA256 生成父节点 → 逐层上构建直到只剩一个根节点。叶子节点是直接 SHA256(data)，内部节点是 SHA256(leftHash + rightHash)。

`NewMerkleTree()` 先用 `NewMerkleNode(nil, nil, datum)` 创建叶子，再循环两两归并。奇数时复制最后一个节点。

**面试表达：** Merkle 树用 O(log N) 的证明大小验证交易在区块中。Bitcoin 的 SPV 节点只需下载区块头和 Merkle 证明即可确认交易存在。

</div>
</details>

**今日任务：**

- 手画 Merkle 树构建过程
- 理解奇偶节点处理
- 跑通 CLI 验证 Merkle Root
- 解释 SPV 轻节点原理

**自检题：**

- **叶子节点和内部节点的哈希算法有何不同？** — 叶子：SHA256(data)，内部：SHA256(leftHash+rightHash)。
- **奇数个叶子如何处理？** — 复制最后一个节点使其成对。
- **Merkle Proof 需要 O(?) 个哈希值？** — O(log N)。

---

### Day 10：P2P 网络与共识

**目标：** 实现三节点 Nakamoto 共识，理解 version/inv/getblocks 协议和最长链规则。

**核心关注点：**

- TCP 自定义协议
- 5 个命令处理
- version 高度比较
- 最长链规则
- 3 节点拓扑

**源码入口：** `010-network/network/Server.go`、`010-network/network/Server_handle.go`、`010-network/network/Server_send.go`、`010-network/main.go`

#### 知识点

<details class="qa-answer">
<summary class="qa-answer-toggle">三节点 Nakamoto 共识如何启动和同步？</summary>

<div class="qa-answer-body">

启动 3 个节点（3000主节点、3001钱包节点、3002矿工节点）。非主节点启动时向主节点 sendVersion，主节点比较高度后决定同步方向。所有区块通过 inv→getdata→block 流程同步。

`StartServer()` 首先判断 `nodeAddress != knowNodes[0]`，非主节点初始化后向主节点发送 version 请求同步。

**面试表达：** Nakamoto 共识通过 PoW + 最长链规则实现去中心化一致性。P2P 网络用 version/inv/getblocks/block 协议同步区块，保证了全网状态的最终一致。

</div>
</details>

**今日任务：**

- 启动 3 个节点并验证同步
- 画出 version → inv → getdata → block 的协议流
- 解释最长链规则如何应对分叉
- 整理 Nakamoto 共识的完整面试回答

**自检题：**

- **5 个 P2P 协议命令是什么？** — version, inv, getblocks, getdata, block。
- **handleVersion 如何实现最长链规则？** — 比较 BestHeight，低方向高方请求同步。
- **Nakamoto 共识的 3 条核心规则？** — PoW 出块、最长链规则、概率最终性。

---

# 面试模拟

## 项目介绍话术

<details class="qa-answer">
<summary class="qa-answer-toggle">请介绍一下你用 Go 实现的区块链系统</summary>

<div class="qa-answer-body">

**答案：** 这是一个基于 Go 语言从零实现的 Nakamoto 共识教学项目。核心包括 5 层：数据层用 BoltDB 做持久化存储、共识层用 PoW + 最长链规则、交易层用 UTXO 模型、安全层用 ECDSA 签名和 Merkle 树、网络层用 TCP 自定义协议实现 P2P 多节点同步。项目从 Block 结构体开始，逐步加入 PoW、序列化、持久化、CLI、UTXO 交易、钱包、Merkle 树和 P2P 网络，共 10 个渐进步骤。最终可以实现 3 节点组网、区块同步、交易广播和完整的 Nakamoto 共识。

**源码入口：** `010-network/network/Server.go`, `007-transaction/core/Transaction.go`, `004-Persistence/core/Blockchain.go`

**追问：** 你负责哪些模块？最大挑战是什么？PoW 难度如何调整？

</div>
</details>

---

## 区块与链

<details class="qa-answer">
<summary class="qa-answer-toggle">Block 结构体包含哪些字段？每个字段的作用？</summary>

<div class="qa-answer-body">

**答案：** Height 区块高度从 1 自增；PrevBlockHash 前一个区块的 SHA256 哈希形成链式连接；Data 存储交易数据字节数组；Timestamp 区块创建 Unix 时间戳；Hash 当前区块的 SHA256 哈希值。这 5 个字段保证了区块链的数据完整性和不可篡改性。

**源码入口：** `001-block/core/Block.go`

**追问：** 创世区块的特殊性？为什么 PrevBlockHash 不能随机生成？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">为什么区块链叫链？它是如何连接起来的？</summary>

<div class="qa-answer-body">

**答案：** 每个区块通过 PrevBlockHash 引用前一个区块的哈希值。如果修改某个区块的数据，它的 Hash 就会改变，导致下一个区块的 PrevBlockHash 不匹配，形成连锁反应。要篡改一个历史区块，必须重新计算该区块和所有后续区块的 PoW。

**源码入口：** `001-block/core/Blockchain.go`

**追问：** 重新计算所有后续区块需要多少算力？最长链规则下如何保护历史数据？

</div>
</details>

---

## PoW 共识

<details class="qa-answer">
<summary class="qa-answer-toggle">PoW 的核心原理是什么？</summary>

<div class="qa-answer-body">

**答案：** 找到 nonce 使区块哈希 SHA256 小于 target。target = 1 << (256-targetBit)，targetBit=16 意味着前 16 位必须是 0。nonce 从 0 开始自增尝试，平均需要 2^16 次。验证只需 O(1) 一次哈希比较。这种非对称性是 PoW 安全性的基础。

**源码入口：** `002-PoW/core/ProofOfWork.go`

**追问：** difficulty 和 targetBit 的关系？Bitcoin 如何动态调整难度？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">PoW 和 PoS 的区别？</summary>

<div class="qa-answer-body">

**答案：** PoW 靠算力竞争出块权（工作量证明），PoS 靠质押代币量竞争（权益证明）。PoW 安全模型是物理算力不可伪造，但能源消耗大。PoS 节能但可能导致富人更富和 nothing-at-stake 问题。这是两套完全不同的安全假设。

**源码入口：** `002-PoW/core/ProofOfWork.go`

**追问：** PoW 在什么情况下不再安全？51% 攻击的具体成本？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">最长链规则如何工作？网络分区时会怎样？</summary>

<div class="qa-answer-body">

**答案：** 节点始终在最长链上挖矿。分区期间各自出块形成分叉。网络恢复后，所有节点自动收敛到最长链，短链上的区块沦为孤块。基于工作量选择链，链越长意味着投入的算力越多，越可信。

**源码入口：** `010-network/network/Server_handle.go`

**追问：** 6 次确认为什么被认为是安全的？概率性最终性和确定最终性的区别？

</div>
</details>

---

## UTXO 交易

<details class="qa-answer">
<summary class="qa-answer-toggle">UTXO 模型和 Account 模型的区别？各有什么优劣？</summary>

<div class="qa-answer-body">

**答案：** UTXO 消费之前的输出产生新输出没有显式余额类似现金交易。Account 维护全局余额表类似银行转账。UTXO 的优势：并行验证（每笔交易独立）、隐私性更好（难以关联多笔交易）、防双花更简单。Account 的优势：简单直观、状态管理方便、适合智能合约。

**源码入口：** `007-transaction/core/Transaction.go`

**追问：** Ethereum 为什么选 Account？Bitcoin 为什么没选？哪些场景适合 UTXO？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">Coinbase 交易是什么？它的特殊标志是什么？</summary>

<div class="qa-answer-body">

**答案：** Coinbase 是每个区块的第一笔交易，也是挖矿奖励。特殊标志：Vins 长度为 1 且 Vins[0].TxHash 为空（0 长度）、Vout 为 -1。没有实际输入来源，凭空产生币。这是新币生成的唯一方式。

**源码入口：** `007-transaction/core/Transaction.go:NewCoinbaseTransaction`

**追问：** Bitcoin 的减半机制？第 21 万个区块后奖励变成多少？

</div>
</details>

---

## 持久化存储

<details class="qa-answer">
<summary class="qa-answer-toggle">为什么用 BoltDB 而不是 MySQL 或 Redis？</summary>

<div class="qa-answer-body">

**答案：** BoltDB 是嵌入式 KV 数据库，零运维零配置适合单机场景。ACID 事务保证数据一致性。B+ 树索引按 Hash 查询 O(log N)。MySQL 需要独立部署运维复杂，Redis 是内存数据库不适合做持久化总账。

**源码入口：** `004-Persistence/core/Blockchain.go`

**追问：** 生产环境用什么数据库？为什么 Bitcoin Core 用 LevelDB？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">迭代器模式如何遍历区块链？时间复杂度和空间复杂度？</summary>

<div class="qa-answer-body">

**答案：** 迭代器从 Tip 沿着 PrevBlockHash 反向遍历。空间 O(1)（只存 CurrentHash）、时间每步 O(log N)（BoltDB B+ 树查询）。直到 PrevBlockHash 为全 0 结束。

**源码入口：** `004-Persistence/core/Blockchainiterator.go`

**追问：** 如果需要正向遍历怎么办？给 Block 加 NextHash 字段的代价？

</div>
</details>

---

## 密码学

<details class="qa-answer">
<summary class="qa-answer-toggle">钱包地址的完整生成流程？每一步的安全作用？</summary>

<div class="qa-answer-body">

**答案：** ECDSA P256 生成密钥对 → SHA256 哈希公钥 → RIPEMD160 压缩到 20 字节防长度扩展攻击 → 加 0x00 版本号 → 双 SHA256 取前 4 字节做校验和防输入错误 → Base58 编码去掉易混淆字符提高可读性。

**源码入口：** `008-Wallet/crypto/wallet.go`

**追问：** 为什么要双哈希（SHA256+RIPEMD160）？Base58 为什么比 Base64 更适合钱包地址？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">Merkle 树在区块链中的作用？SPV 验证如何工作？</summary>

<div class="qa-answer-body">

**答案：** Merkle 树把区块中所有交易哈希组织成二叉树。任何交易的修改都会改变 Merkle Root 实现防篡改。SPV 节点只需下载区块头和 O(log N) 个兄弟哈希即可验证交易存在不需要全量下载全节点数据。

**源码入口：** `009-MerkleTree/core/merkle_tree.go`

**追问：** Merkle Proof 的验证过程？为什么需要双 SHA256？

</div>
</details>

---

## P2P 网络

<details class="qa-answer">
<summary class="qa-answer-toggle">P2P 网络的 5 个协议消息及其作用？</summary>

<div class="qa-answer-body">

**答案：** version 交换节点版本和链高度实现握手。inv 广播自己拥有的区块哈希列表。getblocks 请求对方发送区块哈希。getdata 请求下载特定完整区块。block 发送完整区块数据。消息格式 COMMANDLENGTH 字节命令 + gob 序列化 payload。

**源码入口：** `010-network/network/Server.go`

**追问：** 为什么用 TCP 自定义协议而不是 HTTP/gRPC？消息粘包怎么处理？

</div>
</details>

<details class="qa-answer">
<summary class="qa-answer-toggle">新节点如何加入网络并同步整条链？</summary>

<div class="qa-answer-body">

**答案：** 启动时初始化空数据库 → sendVersion 到已知主节点 → 主节点 handleVersion 比较高度 → 主节点 sendInv 发送哈希列表 → 新节点 sendGetData 逐个请求区块 → 主节点 sendBlock 逐个发送完整区块 → 新节点逐块验证写入本地数据库。

**源码入口：** `010-network/network/Server_send.go`

**追问：** 如果同步到一半网络断了怎么办？断点续传如何实现？

</div>
</details>

---

# 速查附录

| 知识点 | 要点 |
|---|---|
| Block 五字段 | Height + PrevBlockHash + Data + Timestamp + Hash |
| PoW targetBit | target = 1 << (256-16)，hash < target 即成功 |
| 创世区块 PrevBlockHash | make([]byte, 32) 全 0，是链的起点 |
| gob 序列化 | Go 原生二进制编码，零依赖，encode/decode Block |
| BoltDB key='l' | 存储最新区块 Hash，每次出块更新 |
| 迭代器终止 | PrevBlockHash 为全 0 时，big.NewInt(0).Cmp == 0 |
| UTXO vs Account | UTXO 无余额字段、引用历史输出；Account 维护余额表 |
| Coinbase 标志 | Vins长度=1 且 TxHash长度为0 且 Vout=-1 |
| Base58 字母表 | 123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz |
| 地址生成 5 步 | ECDSA→SHA256→RIPEMD160→版本号+校验和→Base58 |
| Merkle 奇数叶子 | 复制最后一个节点使其成对 |
| SPV 验证 | O(log N) 个哈希证明交易存在 Merkle 树中 |
| P2P 5 协议 | version / inv / getblocks / getdata / block |
| 最长链规则 | 比较 BestHeight，始终在最长链上挖矿 |
| Nakamoto 共识 | PoW+最长链+概率最终性 |
| handleVersion | bestHeight > foreigner → sendVersion；< → sendGetBlocks |
| 51% 攻击 | 控制 >50% 算力构建私密长链替换公开链 |
| 6 次确认 | 每个区块确认后，攻击者需要追上 6 个区块几乎不可能 |
| 校验和 | 双 SHA256 取前 4 字节，防地址输入错误 |
| gob 问题 | ecdsa.PrivateKey 未导出字段需自定义 GobEncode |

---

# 场景还原

## 端到端流程：创建区块链 → 添加区块 → 查看全链

本地单机区块链完整操作流程：

| 步骤 | 操作位置 | 说明 |
|---|---|---|
| 创建区块链 | `./bc.exe createblockchain "Genesis Data"` | — |
| BoltDB 初始化 | `bolt.Open(blockchain.db, 0600, nil)` | 创建 blocks Bucket，写入创世区块，设置 key='l' |
| 添加新区块 | `./bc.exe addblock -data "Send 100 to KY"` | — |
| PoW 挖矿 | `ProofOfWork.Run()` | nonce 递增直到 hash < target |
| 序列化 + 存储 | `block.Serialize() → b.Put(hash, bytes)` | 更新 key='l' 为新区块 Hash |
| 查看全链 | `./bc.exe printchain` | 迭代器从 Tip 开始反向输出所有区块 |

---

## 故障场景：BoltDB 文件损坏

数据库文件被意外删除或损坏：

| 影响 | 详情 | 修复方式 |
|---|---|---|
| 区块链数据丢失 | BoltDB 文件损坏后无法打开数据库。blockchain.db 文件丢失。 | 重新运行 createblockchain 创建新区块链。在 010-network 网络模式中，损坏的节点从其他节点重新同步。 |

---

## 故障场景：网络分区

Nakamoto 共识如何应对分叉：

| 影响 | 详情 | 修复方式 |
|---|---|---|
| 双分叉 | 网络分区期间各区域各自出块形成两条链。 | 网络恢复后，所有节点比较 BestHeight，自动切换到最长链。短链上的区块成为孤块。 |
| 51% 算力攻击 | 攻击者秘密构建自己的链超过全网最长链。 | 增加确认次数（如 6 次确认）让攻击者在概率上不可能追上。在 targetBit 较高时攻击成本极高。 |
