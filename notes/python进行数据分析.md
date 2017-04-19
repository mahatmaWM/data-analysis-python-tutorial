python进行数据分析

本书讲了numpy和pandas的使用，例子值得看看。
pandas很方便处理数据，参看第九章联邦选取的例子，基本上可以将pandas处理的数据的流程学会，
其中处理透视表的方法是使用比较多的数据处理方式。split-apply-combine.





df["grade"].cat.categories = ["very good", "good", "very bad"]来对categories取一些更有意义的名称，
categories类型的排序和string类型不一样，有本身先后顺序。

* pandas-ply
另外本书也讲了时间序列数据的处理方式。

画图：seaboard能画的图不多。这个网站可以方便画图https://plot.ly/alpha/workspace/





第四章     numpy的操作

常用的数组算法、数据合并/链接、将条件逻辑表述为数组表达式、数据的分组运算（聚合、转换函数应用）。
数组ndarray对象（在内存中保存为数据、dtype、形状shape元组、跨度）其属性有shape、dtype、ndim。
有几种方法来创建一个ndarray，数组和标量之间的运算，矢量化操作就免去了for循环，大小相等的数组间运算都将
应用到元素级别，而大小不相等的数组间运算都会用到广播的技术。
有了一个数组，就要介绍获取数组子集的方法。按照索引取出一个切片，而二维数组的获取[行列都可以是向量标识]。
利用数组进行数据处理，np.where方法是x if condition else y的函数表达，巧用它可以简化代码量，
另外mesh grid、布尔型数组的any、all等方法的使用，数组集合的交并差的操作。
当然也可以利用numpy进行矩阵分解等一系列操作。
数组的reshape操作仅仅改变shape元组的值，也就是数组的重塑或者散开操作。
数组在aixs=0或者1的方向上进行合并或者拆分操作。
数组元素的重复操作，tile和repeat函数都做这个事情，但是两者重复的方法是不一样的。
数组的take、put操作也是元素的获取设置方法，对应按索引获取元素一样。
[::-1]反序一个列表的技巧，argsort间接排序，返回元素升序排序后数值在原数组的下标，
防止改变原始数据，但又可以升序输出arr[argsort(arr)]，lexsort指定参考排序。



pandas的操作

用 [行、列] 索引获取元素，但是推荐用df.loc(行、列标签)或者用df.iloc(行、列integer位置)来取数据，
注意这里行列都可以与一些布尔类型数据结合用，df.ix是两者的混用，但是不推荐使用。

concat、join、merge三个函数的使用。
combine-first函数与np.where使用方法类似。
对于grouping相关的操作依照groupby-apply-combine的流程，先用groupby将数据分好组（数据行数没有减少），
然后后续的apply函数是作用在每一个分组数据里面，这些函数包括（aggregate聚合类函数：每个分组聚合成一行结果；
transform函数：根据定义的lambda函数，每行数据都做相应的变化（注意使用aggregate、transform函数时，
传入的函数产生的结果要么是可以广播的标量要么是相同大小的数组）；filter函数：过滤出符合条件的结果）。
nlargest、nsmallest、nth，以及cumcount返回在各组中排序的次序。这些动作对原始数据的index会有改变。
注意index的作用以及reindex、set-index、reset-index的使用，多级index的使用。
pd.get-dummies的使用