# behave: 用Python实现的行为树

使用 `behave`, 你可以这样定义一个行为树:

````python
tree = (
    is_greater_than_10 >> wow_large_number
    | is_between_0_and_10 >> count_from_1
    | failer * repeat(3) * doomed
)

bb = tree.blackboard(10)
while bb.tick() == RUNNING:
    pass

````


### Import from behave:

````python
from behave import condition, action, FAILURE
````

### 定义条件节点

条件由函数定义，返回`bool`值. 
函数接收任意数量的参数

````python
@condition
def is_greater_than_10(x):
    return x > 10

@condition
def is_between_0_and_10(x):
    return 0 < x < 10

````

### 定义动作节点

动作函数返回 `SUCCESS`, `FAILURE`, `RUNNING` 状态. 
`None`默认为`SUCCESS`.

````python
@action
def wow_large_number(x):
    print("WOW, %d is a large number!" % x)

@action
def doomed(x):
    print("%d is doomed" % x)
    return FAILURE
````

你可以用装饰器来定义动作节点

* `yield FAILURE` 动作执行失败. 
* `yield`，`yield RUNNING` , `yield None` 动作执行成功
* 当迭代完成，也相当于`SUCCESS`

```python
@action
def count_from_1(x):
    for i in range(1, x):
        print("count", i)
        yield
    print("count", x)

````

### 定义序列器节点

````python
seq = is_greater_than_10 >> wow_large_number
````

### 定义选择器节点

````python
sel = is_greater_than_10 | is_between_0_and_10
````

### 装饰器节点

````python
from behave import repeat, forever, succeeder

decorated_1 = forever(count_from_1)
decorated_2 = succeeder(doomed)
decorated_3 = repeat(10)(count_from_1)
````

出于可读性的考虑，你也可以使用链式风格：

````python
from behave import repeat, forever, succeeder, failer

composite_decorator = repeat(3) * repeat(2)   # It's identical to repeat(6)

decorated_1 = forever * count_from_1
decorated_2 = succeeder * doomed
decorated_3 = repeat(10) * count_from_1
decorated_4 = failer * repeat(10) * count_from_1
````

### 将所有节点组合成完整的行为树

````python
tree = (
    is_greater_than_10 >> wow_large_number
    | is_between_0_and_10 >> count_from_1
    | failer * repeat(3) * doomed
)
````

每个节点本身就是一棵树。
而一棵大树是由许多子树组成的。
To iterate the tree:

````python
# 创建一个运行实例
bb = tree.blackboard(5) 

# 现在让树做它的工作，直到工作完成
state = bb.tick()
print("state = %s\n" % state)
while state == RUNNING:
    state = bb.tick()
    print("state = %s\n" % state)
assert state == SUCCESS or state == FAILURE
````

Output:

````
count 1
state = Running

count 2
state = Running

count 3
state = Running

count 4
state = Running

count 5
state = Success
````

## 等等，我提到过调试器吗？

为了调试树，你需要:

* 定义一个debugger函数
* 通过调用`tree.debug(debugger, arg1, arg2...)` 来创建blackboard.

````python
def my_debugger(node, state):
    print("[%s] -> %s" % (node.name, state))

# 创建一个启用了调试器的黑板
bb = tree.debug(my_debugger, 5)

# 现在让树做它的工作，直到工作完成
state = bb.tick()
print("state = %s\n" % state)
while state == RUNNING:
    state = bb.tick()
    print("state = %s\n" % state)
assert state == SUCCESS or state == FAILURE
````

Output:

````
[ is_greater_than_10 ] -> Failure
[ BeSeqence ] -> Failure
[ is_between_0_and_10 ] -> Success
count 1
[ count_from_1 ] -> Running
[ BeSeqence ] -> Running
[ BeSelect ] -> Running
state = Running

count 2
[ count_from_1 ] -> Running
[ BeSeqence ] -> Running
[ BeSelect ] -> Running
state = Running

count 3
[ count_from_1 ] -> Running
[ BeSeqence ] -> Running
[ BeSelect ] -> Running
state = Running

count 4
[ count_from_1 ] -> Running
[ BeSeqence ] -> Running
[ BeSelect ] -> Running
state = Running

count 5
[ count_from_1 ] -> Success
[ BeSeqence ] -> Success
[ BeSelect ] -> Success
state = Success

````

太乱了？让我们把一些注释放到树上。

````python
tree = (
    (is_greater_than_10 >> wow_large_number) // "if x > 10, wow"
    | (is_between_0_and_10 >> count_from_1) // "if 0 < x < 10, count from 1"
    | failer * repeat(3) * doomed // "if x <= 0, doomed X 3, and then fail"
)
````

`my_debugger`也做点小改动

````python
def my_debugger(node, state):
    if node.desc:
        print("[%s] -> %s" % (node.desc, state))
````

重试:

````
[ if x > 10, wow ] -> Failure
count 1
[ if 0 < x < 10, count from 1 ] -> Running
state = Running

count 2
[ if 0 < x < 10, count from 1 ] -> Running
state = Running

count 3
[ if 0 < x < 10, count from 1 ] -> Running
state = Running

count 4
[ if 0 < x < 10, count from 1 ] -> Running
state = Running

count 5
[ if 0 < x < 10, count from 1 ] -> Success
state = Success
````

## 运行测试用例 [nose](https://nose.readthedocs.org/en/latest/)

````
nosetests test
````
