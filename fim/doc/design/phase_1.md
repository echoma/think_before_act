# 一期工作细化

## 数据结构、算法

### 存储树

* 一个红黑树，用户要求保存的数据都在这个树里。

* 元素结构如下：

| 名称 | 类型 | 描述 |
| -------- | -------- | -------- |
| key | string* | 用来排序的字段。使用自定义的内存分配器 |
| data | string* | 存储当前的值 |
| data_pending | string* | 存储正在更新中的新值 |
| lock | uint8 | 用户锁，是两个位。第0位是读锁，第1位是写锁 |
| updated_timestamp | double | 最近更新的时间戳 |
| expiring_timestamp | double | 将在何时过期 |
| rlocked_timestamp | double | 事务读锁的锁定时间 |
| wlocked_timestamp | double | 事务写锁的锁定时间 |
| waiting_task | list[task*] | 正在等待该节点

* 使用元素的key做排序。

* 该红黑树显然是可以指定key的范围进行遍历的。

* 关于事务读写锁：

  - 二阶段提交过程中，发起者在收到确认前是只做写锁的。因为这之前各个服务的数值一定是一致的，可以读取。
  - 二阶段提交过程中，发起者一旦收到确认就要加读锁+写锁，接收者收到第一次请求就要读写锁都加。

### 存储树的更新时间索引

* 一个红黑树，存储了上面[存储树](#存储树)的更新时间索引

* 元素结构如下：

| 名称 | 类型 | 描述 |
| -------- | -------- | -------- |
| updated_timestamp | double | 对应元素的时间戳 |
| element | element* | 对应元素的指针 |

* 集群中其他节点通过本节点同步数据时，本节点将根据更新时间来进行同步。

### 存储扫描

* 使用一个定时器，缓慢的对存储树进行遍历。

* 遍历中，当某个元素已经过期时，如果节点是可删除的状态，则将会删除该节点，否则计数。

### 任务

* 每个客户端请求的命令都会转换为一个任务。每个任务可能会涉及一个或者多个key。

* 每个任务(task)有以下属性：

| 字段 | 类型 | 说明 |
| -------- | -------- | -------- |
| id | uint32 | 工作ID |
| type | uint32 | 类型。0-读，1-写，2-事务，3-脏读 |
| state | uint32 | 状态。0-未处理，10-处理中，20-等待资源，30-处理完毕 |
| cmd-list | array[string*, condition-fulfilled] | 涉及的key的列表，按命令里出现的先后顺序 |
| query-node-list | array[id, condition-fulfilled] | 正在二阶段提交时各节点的确认状态 |

### 开发相关

* 可动态调整的日志级别。

* 不同的模块可设置不同的日志级别。

* 日志可输出到多种对象：滚动文件(rotate file)、网络地址(UDP)、文件(file)

* 进程是否常驻，是否打开coredump。

## 本期涉及配置项

| 分类 | 名称 | 类型 | 说明 |
| -------- | -------- | -------- | -------- |
| 存储树 | max-size | int64_t | 存储树的最大元素个数 |
| | alloc-type | uint32_t | 内存分配类型。0-默认的new/delete，1-固定大小预分配 |
| | fixed-pre-alloc-step | int64_t | 使用预分配时，每次分配多少块。默认是全部。 |
| | data-alloc-type | uint32_t | 元素携带的数据的分配类型。|
| | fixed-pre-data-alloc-step | int64_t | 使用预分配时，每次分配多少块。默认是全部。 |
| 存储扫描 | interval | int32_t | 多少毫秒扫描一次 |
| | max-scan-count | int32_t | 每次扫描最多多少个元素 |
| 开发 | log-level | int32_t | 日志输出级别（各模块分开列） |
| | log-type | uint32_t | 日志输出类型。0-标准输出、1-滚动文件、2-UDP地址、3-管道设备 |
| | log-path | string | 日志输出目标。滚动文件的文件夹路径、UDP的ipv4/6地址、管道设备文件路径 |
| | proc-daemon | uint32_t | 后台常驻进程。1-是 |
| | proc-core | int64_t | 将corelimit调整到多大 |

## 本期工作内容梳理

* [ ] ut_config和全局配置变量
* [ ] ut_rbtree模板其对应的allocator
* [ ] ut_rbtree