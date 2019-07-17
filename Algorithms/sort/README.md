# 一、排序模块测试方式
- 根目录下搭建virtualenv环境，通过requirements.txt文件同步依赖库
- 运行
```python
# 切换目录
cd DevNote/Algorithms/sort
# 运行测试
python3 base/run.py
```

# 二、各排序方法
## BubbleSort 冒泡排序
相邻元素进行比较进行排序

## SelectSort 选择排序
每轮循环找到未排序的元素中最小的元素放到已排好元素的最后

## InsertSort 插入排序
第一次循环保证[0,1]有序，第二次循环保证[0,2]有序，即是说每次循环找出一个新的元素插入到已排序的数组中它该排序的位置上