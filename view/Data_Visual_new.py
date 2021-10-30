from flask_web.Get_Data import get_Data
from pylab import *
import pyecharts.options as opts
from pyecharts.charts import Bar, Line, Pie, Boxplot, Page
from pyecharts.faker import Faker


Data = get_Data()

############################################################################
##第一部分(各地区房屋数量和单位面积租金比)
data_one = np.array(Data.get_Unit_Num_Ratio()).reshape(12,3)
x_data = [col[0] for col in data_one]       #地区名称
y_data_one = [col[1] for col in data_one]   #房屋数量
y_data_two = [col[2] for col in data_one]   #单位面积租金比

bar = (
    Bar(init_opts=opts.InitOpts(width="1000px", height="500px")) #初始化
    .add_xaxis(xaxis_data=x_data)

    .add_yaxis(
        series_name='房屋数量',
        y_axis=y_data_one,
        label_opts=opts.LabelOpts(is_show=True)
    )

    .extend_axis(
        yaxis=opts.AxisOpts(
            name="单位面积租金比",type_="value",min_=0,max_=80,interval=10,
            axislabel_opts=opts.LabelOpts(formatter="{value} 元/m²"),
        )
    )

    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="数量",type_="value",
            min_=0,max_=1400,interval=200,
            axislabel_opts=opts.LabelOpts(formatter="{value} 个"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
)

line = (
    Line()
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name="单位面积租金比",
        yaxis_index=1,
        y_axis=y_data_two,
        label_opts=opts.LabelOpts(is_show=True),
    )
)
bar.overlap(line).render("Charts_of_one.html")

############################################################################
##第二部分(各租金价格区间的房源数量占比)
data_two = Data.get_Rent_Section()

x_data = np.array(['1千元以下','1千元~2千元','2千元~3千元','3千元~4千元','4千元~5千元','5千元~6千元','6千元以上'])
data_pair = list(zip(x_data,data_two))
pie = (
    Pie()
    .add(
        series_name='饼图-圆环图示例',
        data_pair=data_pair,
        radius=["40%", "75%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="各租金价格区间的房源数量占比",
            pos_left="250"
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",  #图例垂直放置
            pos_top="15%",      # 图例位置调整
            pos_left="5%"
        ),
    )
    # 标签内容格式器: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    .render("Charts_of_two.html")
)

############################################################################
##第三部分(各地区租金箱型图)
data_thr = Data.get_Region_Rent()
x_data = ['从化','南沙','增城','天河','海珠','番禺','白云','花都','荔湾','越秀','黄埔']
y_data = data_thr
boxplot = (
    Boxplot()

    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(series_name='', y_axis=Boxplot.prepare_data(y_data))

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title='各地区租金箱型图',
            pos_left='350',
            pos_top='5',
            title_textstyle_opts=opts.TextStyleOpts(
                font_family='KaiTi', font_size=20, color='black',
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            name='地区',type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="数量", type_="value",
            min_=0, max_=10000, interval=2000,
            axislabel_opts=opts.LabelOpts(formatter="{value} 元"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    .render("Charts_of_thr.html")
)

############################################################################
##第四部分(房屋室厅数量分布、房屋朝向分布、有小区管理或拎包入住说明的房屋数量)
#房屋室厅数量分布
page = Page()
data_for = np.array(Data.get_Room_Hall()).reshape(9,3)
y_data = [int(col[2]) for col in data_for]    #室厅数量,这里需要类型转换,Bar不接受numpy.int32类型的值
x_data = []  #室厅
for col in data_for:
    x_data.append("{}室{}厅".format(col[0],col[1]))

bar1 = (
    Bar(init_opts=opts.InitOpts(width="500px", height="300px"))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name='房屋数量',
        y_axis=y_data,
        label_opts=opts.LabelOpts(is_show=True)
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            name_rotate=45,axislabel_opts={"rotate": 45},
            name="室/厅",type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="房屋数量",type_="value",
            min_=0,max_=800,interval=100,
            axislabel_opts=opts.LabelOpts(formatter="{value} 个"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),

    )

    # .render("Charts_of_for.html")
)
page.add(bar1)

# # 房屋朝向分布
data_fiv = np.array(Data.get_Orientations()).reshape(10,2)
x_data = [col[0] for col in data_fiv]
y_data = [int(col[1]) for col in data_fiv]
print(type(x_data[0]))
print(type(y_data[0]))
bar2 = (
    Bar(init_opts=opts.InitOpts(width="500px", height="300px"))
    .add_xaxis(xaxis_data=x_data)
    .add_yaxis(
        series_name='房屋数量',
        y_axis=y_data,
        label_opts=opts.LabelOpts(is_show=True)
    )
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            name_rotate=45,axislabel_opts={"rotate": 45},
            name="朝向",type_="category",
            axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
        ),
        yaxis_opts=opts.AxisOpts(
            name="房屋数量",type_="value",
            min_=0,max_=1400,interval=200,
            axislabel_opts=opts.LabelOpts(formatter="{value} 个"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    .set_colors("#439B78")
    # .render("Charts_of_fiv.html")
)
page.add(bar2)

#小区管理标签的房屋
data_six = int(np.array(Data.get_Note_one()))
data_min = 2973 - data_six

data_label = ["是","否"]
pie1 = (
    Pie()
    .add(
        series_name='',
        data_pair=list(zip(data_label,[data_six,data_min])),
        radius=['0%','40%'],
        center=['30%','40%']
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="是否为小区管理",
            pos_left="210",
            pos_top="35",
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",  #图例垂直放置
            pos_top="15%",      # 图例位置调整
            pos_left="5%",
        ),
    )

    # 标签内容格式器: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    # .render("note_pie_one.html")
)
page.add(pie1)

#拎包入住的房屋
data_sev = int(np.array(Data.get_Note_two()))
data_min = 2973 - data_sev

data_label = ["是","否"]
pie2 = (
    Pie()
    .add(
        series_name='',
        data_pair=list(zip(data_label,[data_sev,data_min])),
        radius=['0%','40%'],
        center=['30%','30%']
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="是否为拎包入住",
            pos_left="210",
            pos_top="10",
        ),
        legend_opts=opts.LegendOpts(
            orient="vertical",  #图例垂直放置
            pos_top="10%",      # 图例位置调整
            pos_left="5%",
        ),
    )

    # 标签内容格式器: {a}（系列名称），{b}（数据项名称），{c}（数值）, {d}（百分比）
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
    # .render("note_pie_two.html")
)
page.add(pie2)
page.render("Charts_of_page.html")

Data.close_Conn()