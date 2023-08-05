# pybi

pybi 是一个使用 Python 直观简洁声明语句的BI可视化报告库。使用 pybi，你可以创建灵活强大的 BI 式交互报告。生成的报告只有一个 html 文件，用户只需要使用浏览器打开就能看到所有的交互效果，无须 Python 环境。



## 例子








## 功能

- 



## 安装

```
pip install pybi-next
```



pybi 依赖 Python 这些第三方库(开发者需要安装)：

- [pandas](https://pandas.pydata.org/)


## 使用
```python
import pybi as pbi
import pandas as pd

# pandas 加载数据
df = pd.DataFrame({"name": ["a", "b"], "age": [1, 2]})

# 设置好数据源
data = pbi.set_source("data", df)

# 下拉框，pybi中称为切片器
pbi.add_slicer(data["name"])
pbi.add_table(data)

pbi.to_html("example.html")
```


## 前端核心功能使用了这些库(开发者与用户都无须关心)：
- [sql.js]([sql.js](https://github.com/sql-js/sql.js/))
- [echarts]([Apache ECharts](https://echarts.apache.org/zh/index.html))
- [Vue.js - The Progressive JavaScript Framework | Vue.js (vuejs.org)](https://vuejs.org/)
- [A Vue 3 UI Framework | Element Plus (element-plus.org)](https://element-plus.org/zh-CN/)
- [plotly](https://plotly.com/javascript/)



