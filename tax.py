import numpy as np
import matplotlib.pyplot as plt

# 上市前每股申报价值（元/股）
pre_price = 1.1111

# 多次授予各次行权价格 （数组形式）
# 使用 [授予股数, 行权价格] 格式
# 如是RSU，行权价格为0
options = [[10000, 0.1], [5000, 0.2]]

# 上市前行权需要缴纳的税金
@np.vectorize
def pre_tax(sale):
  """
  Args:
    sale: 持股平台减持价格（元/股）

  Returns:
    需交纳税金
  """
  return income_tax(income(pre_price, options)) + cap_tax(all_option(options) * (sale - pre_price))

# 上市后行权需要缴纳的税金

@np.vectorize
def post_tax(buy, sale):
  """
  Args:
    buy: 上市后行权每股市价（元/股）
    sale: 持股平台减持价格（元/股）

  Returns:
    需交纳税金
  """
  return income_tax(income(buy, options)) + cap_tax(all_option(options) * (sale - buy))

# 计算行权时总收益
def income(price, option_arr):
  m = 0
  for option in option_arr:
    m += option[0] * (price - option[1])
  return m

# 计算股权总数
def all_option(option_arr):
  n = 0
  for option in option_arr:
    n += option[0]
  return n

# 个人所得税计算
def income_tax(x):
  if x < 0:
    return 0
  elif x < 36000:
    return x*.03
  elif x < 144000:
    return x*.1 - 2520
  elif x < 300000:
    return x*.2 - 16920
  elif x < 420000:
    return x*.25 - 31920
  elif x < 660000:
    return x*.3 - 52920
  elif x < 960000:
    return x*.35 - 85920
  else:
    return x*.45 - 181920

# 资本利得税计算
def cap_tax(x):
  if x < 0:
    return 0
  return .2 * x

# 作图比较两种方式需要的税金
def plot_compare(min_buy_price, max_buy_price, min_sale_price, max_sale_price):
  buy = np.arange(min_buy_price, max_buy_price, 0.025)
  sale = np.arange(min_sale_price, max_sale_price, 0.025)
  buy, sale = np.meshgrid(buy, sale)
  pre_tax_v = pre_tax(sale)
  post_tax_v = post_tax(buy, sale)
  fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

  ax.plot_surface(buy, sale, pre_tax_v, alpha=0.5)
  ax.plot_surface(buy, sale, post_tax_v, alpha=0.5)
  ax.set_xlabel('Buy price')
  ax.set_ylabel('Sale price')
  ax.set_zlabel('Tax')
  plt.show()

if __name__ == '__main__':
  # 可以直接计算上市后行权需要交纳的税金
  # 上市后行权每股市价（元/股）
  buy_price = 1
  # 持股平台减持价格（元/股）
  sale_price = 3
  print(f'上市前行权需交纳税金{pre_tax(sale_price)}')
  print(f'上市后行权需交纳税金{post_tax(buy_price, sale_price)}')

  # ---------------------------------------------
  # 也可以作图对比两种方式所需要的税金
  # 对比中最高/最低上市后行权每股市价
  min_buy_price = 0.5
  max_buy_price = 20
  # 对比中最高/最低持股平台减持价格
  min_sale_price = 0.5
  max_sale_price = 20

  plot_compare(min_buy_price, max_buy_price, min_sale_price, max_sale_price)
