# 石头记百科

红楼梦里的人物、食品、用具、事件非常多，可以建立一个数据库了。

所有这些对象之间都是可以建立关系的，比如人物之间的关系，人物跟事件的关系，人物跟用具之间的关系。

如果有个工具可以快查会很好，如果能提供某种视图那就更好（比如人物族谱、人物事件图）。

## 思考

应该先做一个引擎，通过引擎为各类小说添加

## 数据侧

### 引擎数据

数据分为`对象`类、`认知`类、`关系`类。

任何对象之间、对象和认知之间都可以具有某种关系。

- 对象
  - 原生
    - 动物
      - 人
        - 出场人物
    - 植物
    - 天体
    - 矿物
    - 山川
  - 加工品
    - 食品
    - 药物
    - 家居
    - 服饰
    - 建筑
- 认知
  - 年代
  - 性别
  - 家族
  - 代际
  - 政治
    - 官阶
  - 地理
    - 城镇乡村
  - 事件
  - 章回
  - 文化
- 关系
  - 属性：主 拥有 宾 这个属性
  - 生育：主 生育了 宾
  - 雇佣：主 雇佣了 宾
  - 前世：主 是 宾 的前世
  - 拥有：主 是 宾 的拥有者
  - 参与：主 参与了 宾 的过程
  - 包含：主 包含了 宾

### 小说数据

每本小说都可以录入自己的数据。

为了搜索和查询，还要根据录入的数据生成一些数据。比如某人属于某个家族，那他生育的人也都是属于这个家族。如果A雇佣了B，则A的家族也是雇佣了B。

## 技术侧

语言肯定是首选node了，估计要用嵌入式db，比如[nedb](https://github.com/louischatriot/nedb)。想了想，如果要支持在一个简单网页里使用，就不能用node了。node只能在编辑数据的程序时使用。

引擎数据直接通过配置自动加载。

然后加载某个小说的录入数据，然后自动计算搜索数据。

编辑端：基本的小说录入数据的增删改查，使用nwjs来做，可以生成小说的搜索数据。

查看端：使用搜索数据进行查询，就是普通网页。



