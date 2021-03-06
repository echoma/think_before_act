# 概要设计

## 目标

### 计划支持的特性

* 基于红黑树的key-value，可指定范围遍历，可指定过期时间。
* 高可用方案：只能是多主集群，保证数据一致性，数据永不丢失。
* 读写分离方案：支持异步从库，但不保证数据一致性。
* 支持分布式事务，保证ACID。
* 支持对key级别的读锁、写锁。
* 可定制化的集群leader选举方案，方便适应复杂的网络环境。
* 集群中的节点可随时增加，并在同步完数据后才提供服务。
* 集群中加入节点时，同步的速度可以调整，避免出现大的网络毛刺。
* 支持两种形式的内存分配：预分配 和 实时分配。
* 提供脏读接口，不需要等待事务完成就直接返回当前结果。
* 可限制key/value的大小，防止过大的节点进入系统。

### 会有如下限制

* 集群中数据量太大可能会导致新加入的节点或者从故障中恢复的节点无法快速提供服务。
* 永远不会提供异步同步集群，因为redis已经提供了这样的功能，并且数据结构丰富太多。
* 新节点加入集群时，有可能会同步全量数据，如果数据量很大，网络带宽有限，那同步可能要花费不少时间。

## 实现路径

* [一期](phase_1.md)
  + 实现单机key-value内存数据库，简单的增删改查。
  + 实现按更新时间排序的索引，通过这个索引支持过期、增量同步。

* 二期
  + 提供兼容redis的接口。
  + 编写基本的持续集成用例+性能评测。

* 三期
  + 实现多主集群（Two-Phase-Commit）
  + 实现最简单的leader选举方案
  + 更新集群测试用例+性能评测

* 四期
  + 实现灾害恢复节点的动态加入
  + 更新集群灾害测试用例+性能评测

* 五期
  + 实现分布式事务接口
  + 更新测试用例+性能评测

* 六期
  + 实现异步从库
  + 更新测试用例+性能评测

* 七期
  + 实现key级别的读、写锁，实现脏读接口
  + 编写测试用例+性能评测

## 多主集群的设计

* 使用 Two Phase Commit 来完成多主写操作的完全同步。
* 一条记录在被更新的过程中，是禁止读写的。所有的读写请求要被hold住。
* 读操作是完全内存一瞬间的操作，是原子的，所以不存在读的过程中有写操作插入的问题。
* 我们的分布式事务启动时必须给定了完整的事务语句，系统可以分析并锁定相关记录。
* 集群里的各个节点使用TCP或unix套接字通信，保证数据传输的完整性，使用心跳测活。
* 集群里的每一台机器都跟其他所有机器维持了连接，集群太大会是个负担。
* 多个事务或这写操作是会被并发执行的，但我们保证来自同一个客户端的读写操作一定是被顺序执行的。
* 当节点重新加入集群时，随便跟集群里任何一台机器进行同步即可。
* 内存里维护了一张按更新时间排序的红黑树，新节点将按照时间进行同步。对于一个因为断线恢复而迅速重新加入集群的节点来说，同步速度是非常快的。

## 请求的处理过程

* 只要不是脏读请求，任意的读、写请求，都是要等待行锁释放的。写请求还要等待其他集群的确认。

* 服务器收到可读通知后的伪代码如下：

```python
if 解析到一个完整命令:
  解析命令内容，生成任务对象cmd
  if 有要等待的key:
    生成等待对象，挂在相应的key下面
    等待所有key完成或超时
    if 等待超时:
      取消本次操作
      end
  if 有写操作:
    向其他服务器发送确认请求
    等待所有服务器确认或超时
    if 其他服务器要求取消或超时:
      取消本次操作
      end
  执行写操作
```