# 石头记数据化

需要数据化的对象有很多，每种对象也有很多属性。对象之间的关系也有很多种，也需要定义。

对象多种多样，人物、物品、饮食、诗词、事件，这些全部数据化是需要很多时间的，需要分批进行。第一期先把人物和人物之间的关系搞好搞全。

## 第一期，人物及人物关系

### 数据表：family 家族

属性：
* 名称：金陵贾家、金陵贾家连宗、金陵王家、金陵王家连宗、金陵史家、金陵薛家、北静王等等
* 发源地：金陵
* 先居地：京城

### 数据表：character 人物

属性：
* name 称呼：通常就是姓名，但也有特例，比如袭人，姓花，原名金花。小红，姓林，原名红玉。
* deduce 是推理出的人物：有些人物按推算应该会有，但未出现在小说中。例如贾母和史湘云之间应该有很多级直系亲属，但小说未做交代。
* gender 性别
* age 大致年龄：以30回左右的年龄为基准
* age_note 大致年龄注解：
* sort_age 排序年龄：用于程序计算排序，不会用于展示
* sort_position 排序地位：用于程序计算排序，不会用于展示
* family_name 姓
* given_name 名
* old_name 原名
* old_family 原属家族
* current_family 现属家族
* employee 是否家族仆人
* job 工作
* generation 在所有家族中拉横是第几代
* nick_1 诨名1：凤辣子、呆霸王、二木头
* `nick_note_1` 诨名1注解
* nick_2 诨名2：凤姐
* `nick_note_2`诨名2注解
* nick_3 诨名3：凤哥
* `nick_note_3`诨名3注解
* nick_4 诨名4：
* `nick_note_4`诨名4注解
* title_1 尊名1：琏二夫人、薛大爷、二姑娘
* `title_note_1` 尊名1注解
* title_2 尊名2：琏二奶奶
* `title_note_2`尊名2注解
* title_3 尊名3：
* `title_note_3`尊名3注解
* title_4 尊名4：
* `title_note_4`尊名4注解
* `first_action_chapter` 首次活动回目：本人活动出场回目
* `first_action_note` 首次活动注解
* `first_refer_chapter`首次提及回目：本人未出场，但先被别人提到了
* `first_refer_note` 首次提及注解
* `first_name_chapter` 首次称呼回目：人物的名字出现位置可能和首次出场不同，也可能和首次提及回目不同
* `first_name_note`首次称呼注解
* die_chapter 死亡回目
* die_note 死亡注解
* salary 俸银、月例

### 数据表：character_job 人物的工作

属性：
* family 家族
* job 工作
* serve 侍奉对象
* pay 月例
* pay_note 月例注释

### 数据表：kinship_type 亲属关系类型

血缘类型的只记录一级直系亲属。

属性：
* type 类型：`parent_child` 父母子女、`couple` 夫妻
* `sub_type` 子类型：`adoption` 是否收养、`assistant` 夫妻为正房or偏房
* note 注解
* male_subject 男主称谓：父亲、丈夫
* female_subject 女主称谓：母亲、无
* male_object 男宾称谓：儿子or养子、无
* femail_object 女宾称谓：女儿or养女、大太太or姨太太

### 数据表：kinship 亲属关系

血缘关系的，年长者为主，年幼者为宾。

夫妻关系的，夫为主，妻为宾。

属性：
* subject 主的称呼：贾母、贾政
* object 宾的称呼：贾政、王夫人
* type 关系类型：父母子女、夫妻
* sub_type
* note 注解

### 特性：人物关系图

根据人物关系画图出来，只涵盖四大家族的人。

其他达官显贵（林如海、北静王之类）、闲杂人员（刘姥姥、蒋雨涵、柳湘莲之类）就不显示了。

节点一定都是主子，鼠标浮在主子上时可以显示他的基本信息、名下的仆人。

### 特性：人物表

按家族一个个列出来，数数看多少人物（推算出的人物不列出来）。

每个家族，先列主子，再列仆人，鼠标浮在某个人头上可以显示基本信息。

