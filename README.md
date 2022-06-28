# 蒙特卡洛树搜索(MCTS)实现五子棋AI

这是我尝试的第一个强化学习项目🥺

我最初的想法就是做一个五子棋AI，一开始用的是DQN算法，太痛苦了嘤，黑白双方都摆烂了，从上往下从左往右依次填棋盘直到有一方获胜💦

有可能是激活函数损失函数选的不好，也有可能是换成CNN就会有改善，不过之后没有仔细研究了，换了新的算法尝试实现五子棋AI，即如题所说蒙特卡洛树搜索。

那么，简单介绍一下蒙特卡洛树。要用它来做决策，先要做一定量的“训练”：

## 选择

当下一步（子结点）有多种选择时，根据上线置信区间（Upper Confidence Bound, UCB）来确定下一步如何走。计算公式如下：

$$\mathrm{UCB}(n_i) = \frac{V(n_i)}{N(n_i)} + c \sqrt{\frac{\ln{\sum N(n)}}{N(n_i)}}$$

$V(n_i)$是结点$n_i$获得的总价值，$N(n_i)$是被访问的总次数，$\sum N(n)$是与$n_i$拥有共同父结点的结点的访问次数总和，$c$ 是一个常数，一般取$\sqrt{2}$。如果某个点从未被访问过，则认为它的UCB为无穷大。

不难看出，这个公式实现了“经验”与“探索”的平衡。

## 结点扩展

为叶结点增加若干子结点。我查阅的不少资料都说可以不必一次性将所有可能性全部添加上，但是我不太能理解这个做法，所以我在我的程序实现中一次性全部添加。

事实上，我并没有添加所有的可能性，而是仅考虑存在的棋子周围的区域。根据经验，我们下五子棋几乎都会挨着已经下过的子落子，很少会出现间隔一位的情况，所以这么做是很合理的，同时也节约了大量时间。

## 模拟

也叫rollout或者playout，大概是MCTS最玄学的地方了，扩展完成之后选择一个子结点，开始**随机**自我对弈直到游戏结束，获取奖励/惩罚。

## 回溯

叶结点获得奖励/惩罚后，原路返回到根结点并沿途更新所有结点的价值。因为是对弈游戏，所以这棵树是一层黑一层白的，因此回溯的时候相邻层获得的价值是不同的。

多说一句，我最开始以为蒙特卡洛树跟神经网络一样需要训练参数并保存下来的，经过别的大佬提醒才知道是从当前状态开始实时搜索的🤣不知道会不会有人跟我犯一样的错误捏👀

用伪代码整理一下思路：
```python
while not is_ended():
    play_stone_by_human()
    for _ in range(max_searches)：
        while current_node is not leaf_node:
            choose(child_with_highest_UCB)
        if current_node is visited:
            expand_current_node()
            random_choose(children_node)
        reward = rollout_result()
        back_propagate(reward)
    play_stone_by_AI()
```

好啦，现在按照伪代码把各种类的方法写出来就可以了！

## 效果

首先是reward设定的问题，如果我没理解错的话，传统的MCTS的reward应当是，获胜为1，失败为0。但是这样的效果不太好，因为轻视失败，导致AI经常不知道阻拦对手的三连，所以我把失败的reward调整成-1，这样AI就知道要防一下三连了。

自己跟AI下了几局，基本上打得有来有回。~~（听说放图片需要图床，才学会写markdown这次就不捣鼓了，下次一定www）~~

## 特性

太慢了💦我专业不是计算机所以算法之类的不是特别了解，我不清楚这么慢是因为python慢还是数据结构不好还是别的什么原因，有大佬知道的话教教我🥺

默认每下一步搜索10000局，大约需要50秒💦确实有点慢了。

还有，个人感觉AI开局下得一般般，越到中间越厉害。

## Bug

偶尔会出现“该结点已经扩展过”的警告，我没弄懂是什么原因，不过似乎对AI下棋没有影响所以就没改了。

## 未来版本

听说AlphaGo Zero用的是MCTS+CNN，正好要放暑假了试一试，也不知道会不会像DQN那样寄了💦个人感觉reward可以用NN来解决，不过具体算法之后再研究叭，这次就到这里🎉

btw，有任何建议哪怕特别细节的建议都可以提喔！谢谢佬们！！
