"""
This module contains report builders for model. Only for internal use, do not show them in the doc.
"""

# pylint: disable=too-many-lines
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=missing-docstring
# pylint: disable=consider-using-enumerate
# pylint: disable=too-many-instance-attributes
# pylint: disable=no-member
# pylint: disable=too-many-branches
# pylint: disable=invalid-name
# pylint: disable=protected-access
# pylint: disable=broad-except
# pylint: disable=consider-using-f-string
# pylint: disable=too-few-public-methods
# pylint: disable=duplicate-string-formatting-argument
import logging
import time
import html
import base64
from io import BytesIO, StringIO
from urllib.parse import quote
from threading import Lock
try:
    from jinja2 import Environment, PackageLoader
except BaseException as error:
    logging.getLogger(__name__).error("%s: %s", error.__class__.__name__, str(error))
    pass
try:
    from IPython.core.display import HTML, display
except BaseException as error:
    logging.getLogger(__name__).error("%s: %s", error.__class__.__name__, str(error))
    pass
import numpy as np
from htmlmin.main import minify
import pandas
from hana_ml import dataframe
from hana_ml.algorithms.pal.preprocessing import Sampling


class TemplateUtil(object):
    def __init__(self):
        pass
    __ENV = None
    try:
        __ENV = Environment(loader=PackageLoader('hana_ml.visualizers', 'templates'))
    except BaseException as error:
        logging.getLogger(__name__).error("%s: %s", error.__class__.__name__, str(error))
        pass
    __SECTION_METADATA = {
        'container': '<div class="section">{}</div>',
        'name': '<h3 class="text-left section_name">{}</h3>',
        'content': '<div class="section_content">{}</div>',
        'content_style': '<div class="section_content" style="text-align:center">{}</div>'
    }

    __TAB_METADATA = {
        'id': 1,
        'lock': Lock(),
        # {nav_id} {nav_items}
        'nav': '<ul id="{}" class="nav nav-tabs" role="tablist">{}</ul>',
        # {nav_item_id} {nav_item_title}
        'nav_active_item': '<li class="nav-item"><a class="nav-link active" href="#{}" role="tab" data-toggle="tab">{}</a></li>',
        'nav_item': '<li class="nav-item"><a class="nav-link" href="#{}" role="tab" data-toggle="tab">{}</a></li>',
        # {pane_id} {pane_items}
        'pane': '<div id="{}" class="tab-content">{}</div>',
        # {pane_item_id} {pane_item_content}
        'pane_active_item': '<div class="tab-pane fade show active" id="{}">{}</div>',
        'pane_item': '<div class="tab-pane fade" id="{}">{}</div>'
    }

    __TABLE_METADATA = {
        'container': '<table class="table table-bordered table-hover">{}</table>',
        'head_container': '<thead>{}</thead>',
        'body_container': '<tbody>{}</tbody>',
        'row_container': '<tr>{}</tr>',
        'head_column': '<th>{}</th>',
        'body_column': '<td>{}</td>'
    }

    __ECHART_METADATA = {
        'id': 1,
        'id_prefix': 'echarts',
        'container': '<div id="{}" style="height:500px;margin-top:10px"></div>',
        'lock': Lock()
    }

    @staticmethod
    def generate_echart(chart_id):
        return TemplateUtil.__ECHART_METADATA['container'].format(chart_id)

    @staticmethod
    def construct_tab_item_data(title, content):
        return {
            'title': title,
            'content': content
        }

    @staticmethod
    def get_echart_id():
        lock = TemplateUtil.__ECHART_METADATA['lock']
        lock.acquire()

        echart_id = TemplateUtil.__ECHART_METADATA['id']
        TemplateUtil.__ECHART_METADATA['id'] = echart_id + 1

        lock.release()

        return '{}_chart_{}'.format(
            TemplateUtil.__ECHART_METADATA['id_prefix'], echart_id)

    @staticmethod
    def get_tab_id():
        lock = TemplateUtil.__TAB_METADATA['lock']
        lock.acquire()

        tab_id = TemplateUtil.__TAB_METADATA['id']
        TemplateUtil.__TAB_METADATA['id'] = tab_id + 1

        lock.release()

        return tab_id

    @staticmethod
    def generate_tab(data):
        # data = [{'title': '','content': ''},{...}]
        element_id = TemplateUtil.get_tab_id()
        nav_id = 'nav_{}'.format(element_id)
        pane_id = 'pane_{}'.format(element_id)
        nav_html = ''
        pane_html = ''
        for i in range(0, len(data)):
            pane = data[i]
            pane_item_id = '{}_{}'.format(pane_id, i)
            if i == 0:
                nav_html = nav_html + \
                    TemplateUtil.__TAB_METADATA['nav_active_item'].format(pane_item_id, pane['title'])
                pane_html = pane_html + \
                    TemplateUtil.__TAB_METADATA['pane_active_item'].format(pane_item_id, pane['content'])
            else:
                nav_html = nav_html + \
                    TemplateUtil.__TAB_METADATA['nav_item'].format(pane_item_id, pane['title'])
                pane_html = pane_html + \
                    TemplateUtil.__TAB_METADATA['pane_item'].format(pane_item_id, pane['content'])

        nav_html = TemplateUtil.__TAB_METADATA['nav'].format(nav_id, nav_html)
        pane_html = TemplateUtil.__TAB_METADATA['pane'].format(pane_id, pane_html)

        tab_html = nav_html + pane_html

        return tab_html, nav_id

    @staticmethod
    def generate_table_html(data: dataframe.DataFrame, column_names=None, table_name=None):
        column_data = []

        for column in data.columns:
            column_data.append(list(data.collect()[column]))

        formatted_data = []
        for i in range(0, data.count()):
            row_data = []
            for j in range(0, len(data.columns)):
                origin_data = column_data[j][i]
                if isinstance(origin_data, str):
                    row_data.append(html.escape(origin_data))
                else:
                    row_data.append(origin_data)
            formatted_data.append(row_data)

        if column_names:
            return TemplateUtil.generate_table(column_names, formatted_data, table_name)
        else:
            return TemplateUtil.generate_table(data.columns, formatted_data, table_name)

    @staticmethod
    def generate_table(columns, data, table_name=None):
        columns_html = ''
        for column in columns:
            columns_html += TemplateUtil.__TABLE_METADATA['head_column'].format(column)
        row_html = TemplateUtil.__TABLE_METADATA['row_container'].format(columns_html)
        head_html = TemplateUtil.__TABLE_METADATA['head_container'].format(row_html)
        if table_name:
            head_html = "<title>{}</title>".format(table_name) + head_html
        rows_html = ''
        for row_data in data:
            columns_html = ''
            for column_data in row_data:
                columns_html += TemplateUtil.__TABLE_METADATA['body_column'].format(column_data)
            rows_html += TemplateUtil.__TABLE_METADATA['row_container'].format(columns_html)
        body_html = TemplateUtil.__TABLE_METADATA['body_container'].format(rows_html)

        return TemplateUtil.__TABLE_METADATA['container'].format(head_html + body_html)

    @staticmethod
    def generate_section(section_name, section_content, section_content_style=False):
        section_name = TemplateUtil.__SECTION_METADATA['name'].format(section_name)
        if section_content_style:
            section_content = TemplateUtil.__SECTION_METADATA['content_style'].format(section_content)
        else:
            section_content = TemplateUtil.__SECTION_METADATA['content'].format(section_content)
        return TemplateUtil.__SECTION_METADATA['container'].format(section_name + section_content)

    @staticmethod
    def get_template(template_name):
        return TemplateUtil.__ENV.get_template(template_name)

    @staticmethod
    def generate_html_file(filename, content):
        file = open(filename, 'w', encoding="utf-8")
        file.write(content)
        file.close()

    @staticmethod
    def get_notebook_iframe(src_html):
        iframe = """
            <iframe
                width="{width}"
                height="{height}"
                srcdoc="{src}"
                frameborder="0"
                allowfullscreen>
            </iframe>
        """.format(
            width='100%',
            height='800px',
            src=html.escape(src_html),
        )
        return iframe

    @staticmethod
    def convert_pandas_to_html(df):
        return df.to_html()\
            .replace('\n', '').replace('  ', '')\
            .replace(' class="dataframe"', 'class="table table-bordered table-hover"')\
            .replace('border="1"', '')\
            .replace(' style="text-align: right;"', '')\
            .replace('<th></th>', '<th style="width: 10px">#</th>')\
            .replace('</thead><tbody>', '')\
            .replace('<thead>', '<tbody>')


class EchartsUtil(object):
    def __init__(self):
        pass

    __LINE_TOOLTIP = {
        'trigger': 'axis'
    }

    __PIE_TOOLTIP = {
        'trigger': 'item',
        'formatter': '{a} <br/>{b} : {c} ({d}%)'
    }

    __BAR_TOOLTIP = {
        'trigger': 'axis',
        'axisPointer': {
            'type': 'shadow'
        }
    }

    __LINE_GRID = {
        'left': '5%',
        'right': '2%',
        'containLabel': 'true',
        'show': 'true'
    }

    __BAR_GRID = {
        'left': '3%',
        'right': '4%',
        'bottom': '3%',
        'containLabel': 'true'
    }

    __BAR_XAXIS = {
        'type': 'value',
        'boundaryGap': [0, 0.01]
    }

    __LINE_TOOLBOX = {
        'feature': {
            'saveAsImage': {'title': 'Save as Image'}
        }
    }

    __COLORS = ['dodgerblue', 'forestgreen', 'firebrick']

    __BAR_COLOR = __COLORS[0]

    @staticmethod
    def generate_line_default_option():
        title = {
            'text': '',
            'top': 0,
            'left': 'center'
        }

        legend = {
            'orient': 'vertical',
            'left': '70%',
            'top': -4,
            'data': []
        }

        x_axis = {
            'type': 'value',
            'boundaryGap': 'false',
            'name': '',
            'nameLocation': 'middle',
            'nameTextStyle': {
                'color': 'black',
                'fontSize': 16,
                'padding': 10
            }
        }

        y_axis = {
            'type': 'value',
            'name': '',
            'nameLocation': 'middle',
            'nameTextStyle': {
                'color': 'black',
                'fontSize': 16,
                'padding': 30
            }
        }

        y_data = {
            'name': '',
            'type': 'line',
            'data': [],
            'color': ''
        }

        series = []

        return title, legend, x_axis, y_axis, y_data, series

    @staticmethod
    def generate_pie_default_option():
        # title = {
        #     'text': '',
        #     'top': 0,
        #     'left': 'center'
        # }

        legend = {
            # 'type': 'scroll',
            'orient': 'horizontal',
            'left': 'left',
            'data': []
        }

        series = [
            {
                'name': '',
                'type': 'pie',
                'radius': '55%',
                'center': ['50%', '60%'],
                'data': [],
                'emphasis': {
                    'itemStyle': {
                        'shadowBlur': 10,
                        'shadowOffsetX': 0,
                        'shadowColor': 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]

        return legend, series

    @staticmethod
    def generate_bar_default_option():
        y_axis = {
            'type': 'category',
            'data': None
        }

        series = [
            {
                'type': 'bar',
                'data': None
            }
        ]

        return y_axis, series

    @staticmethod
    def generate_load_line_js(chart_id, chart_text, chart_data):
        title, legend, x_axis, y_axis, y_data, series = EchartsUtil.generate_line_default_option()

        title['text'] = chart_text['label']
        x_axis['name'] = chart_text['xlabel']
        y_axis['name'] = chart_text['ylabel']

        legend['data'] = []

        for data in chart_data:
            y_data_copy = y_data.copy()

            if (chart_text['title'] == 'ROC') and (
                    data['label'] == 'Random model'):
                y_data_copy['smooth'] = 'false'
                y_data_copy['itemStyle'] = {
                    'normal': {
                        'lineStyle': {
                            'type': 'dotted'
                        }
                    }
                }

            legend['data'].append(data['label'])
            y_data_copy['name'] = data['label']
            y_data_copy['color'] = EchartsUtil.__COLORS[data['color_index']]

            temp = []
            for index in range(0, len(data['x'])):
                temp.append([data['x'][index], data['y'][index]])
            y_data_copy['data'] = temp

            series.append(y_data_copy)

        option = {}
        option['title'] = title
        option['tooltip'] = EchartsUtil.__LINE_TOOLTIP
        option['legend'] = legend
        option['grid'] = EchartsUtil.__LINE_GRID
        option['toolbox'] = EchartsUtil.__LINE_TOOLBOX
        option['xAxis'] = x_axis
        option['yAxis'] = y_axis
        option['series'] = series

        js_str = '''
            var {id} = echarts.init(document.getElementById('{id}'));\n
            var {id}_option = {option};\n
            {id}.setOption({id}_option);\n
        '''.format(id=chart_id, option=option)

        return js_str.replace("'true'", "true").replace("'false'", "false")

    @staticmethod
    def generate_load_bar_js(chart_id, data_names, data_values):
        y_axis, series = EchartsUtil.generate_bar_default_option()
        y_axis['data'] = data_names
        series[0]['data'] = data_values

        option = {}
        option['tooltip'] = EchartsUtil.__BAR_TOOLTIP
        option['grid'] = EchartsUtil.__BAR_GRID
        option['xAxis'] = EchartsUtil.__BAR_XAXIS
        option['yAxis'] = y_axis
        option['series'] = series
        option['color'] = EchartsUtil.__BAR_COLOR

        js_str = '''
            var {id} = echarts.init(document.getElementById('{id}'));\n
            var {id}_option = {option};\n
            {id}.setOption({id}_option);\n
        '''.format(id=chart_id, option=option)

        return js_str.replace("'true'", "true").replace("'false'", "false")

    @staticmethod
    def generate_load_heatmap_js(chart_id, title, name_list, label_list, z_max, x_y_z_list):
        option = {
            'xAxis': {
                'type': 'category',
                'data': name_list,
                'name': label_list[0],
                'nameLocation': 'center',
                'splitArea': {
                    'show': 'true'
                }
            },
            'yAxis': {
                'type': 'category',
                'data': name_list,
                'name': label_list[1],
                'nameLocation': 'center',
                'splitArea': {
                    'show': 'true'
                }
            },
            'visualMap': {
                'min': 0,
                'max': z_max,
                # 'left': 'right',
                # 'top': 'center',
                'orient': 'horizontal',
                'left': 'center',
                'bottom': '-%',
                'calculable': 'true',
                'realtime': 'false',
                'splitNumber': 4,
                'inRange': {
                    'color': [
                        '#e0f3f8',
                        '#abd9e9',
                        '#74add1',
                        '#4575b4',
                    ]
                }
            },
            'series': [
                {
                    'name': title,
                    'type': 'heatmap',
                    'data': x_y_z_list,
                    'label': {
                        'show': 'true',
                        'color': 'black'
                    },
                    'emphasis': {
                        'itemStyle': {
                            'shadowBlur': 10,
                            'shadowColor': 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }

        js_str = '''
              var {id} = echarts.init(document.getElementById('{id}'));\n
              var {id}_option = {option};\n
              {id}.setOption({id}_option);\n
          '''.format(id=chart_id, option=option)

        return js_str.replace("'true'", "true").replace("'false'", "false")

    @staticmethod
    def generate_load_pie_js(chart_id, data_names, data_values):
        legend, series = EchartsUtil.generate_pie_default_option()

        for index in range(0, len(data_names)):
            series[0]['data'].append({
                'value': data_values[index],
                'name': data_names[index]
            })

        legend['data'] = data_names

        option = {}
        option['tooltip'] = EchartsUtil.__PIE_TOOLTIP
        option['legend'] = legend
        option['series'] = series

        js_str = '''
              var {id} = echarts.init(document.getElementById('{id}'));\n
              var {id}_option = {option};\n
              {id}.setOption({id}_option);\n
          '''.format(id=chart_id, option=option)

        return js_str.replace("'true'", "true").replace("'false'", "false")


class PlotUtil(object):
    def __init__(self):
        pass

    __LOCK = Lock()

    @staticmethod
    def plot_to_str(generated_plt, image_format='svg'):
        """Quickscope the plot to a base64 encoded string.
        Args:
            generated_plt: The pyplot module.
            image_format: png or svg.
        Returns:
            A base64 encoded version of the plot in the specified image format.
        """
        if image_format not in ["svg", "png", "pdf"]:
            raise ValueError('Image format can only: png or svg.')
        mime_types = {"png": "image/png", "svg": "image/svg+xml", "pdf": "application/pdf"}

        PlotUtil.__LOCK.acquire()
        try:
            if image_format == "svg":
                image_str = StringIO()
                generated_plt.savefig(image_str, format=image_format)
                image_str.seek(0)
                result_string = image_str.getvalue()
            elif image_format == "pdf":
                image_bytes = BytesIO()
                generated_plt.savefig(image_bytes, format=image_format)
                image_bytes.seek(0)
                base64_data = base64.b64encode(image_bytes.getvalue())
                result_string = "data:{mime_type};base64,{image_data}".format(
                    mime_type=mime_types[image_format], image_data=quote(base64_data))
            else:
                image_bytes = BytesIO()
                generated_plt.savefig(image_bytes, dpi=800, format=image_format)
                image_bytes.seek(0)
                base64_data = base64.b64encode(image_bytes.getvalue())
                result_string = "data:{mime_type};base64,{image_data}".format(
                    mime_type=mime_types[image_format], image_data=quote(base64_data))
                result_string = '<img src="{}">'.format(result_string)
            # generated_plt.close()
        except RuntimeError:
            raise RuntimeError('Failed to transform image object to string!')
        finally:
            # generated_plt.close()
            PlotUtil.__LOCK.release()

        return result_string


class StatisticReportBuilder(object):
    def __init__(self):
        self.__statistic_table = None

        self.__classes = {}
        self.__map = {}
        self.__auc = None

        self.__html_table1_columns = ['CLASS', 'PRECISION', 'RECALL', 'F1-SCORE', 'SUPPORT']
        self.__html_table1_data = []
        self.__html_table2_columns = ['STAT NAME', 'STAT VALUE', 'CLASS']
        self.__html_table2_data = []

        self.__generated_html = None

    def set_statistic_table(self, statistic_table: dataframe.DataFrame):
        self.__statistic_table = statistic_table

    def __clear(self):
        self.__classes = {}
        self.__map = {}
        self.__auc = None

        self.__html_table1_data = []
        self.__html_table2_data = []
        self.__generated_html = None

    def __transform_data_format(self, pandas_df: pandas.DataFrame):
        names = list(pandas_df['STAT_NAME'])
        values = list(pandas_df['STAT_VALUE'])
        class_names = list(pandas_df['CLASS_NAME'])

        for index in range(0, len(names)):
            name = str(names[index])
            value = str(values[index])
            class_name = str(class_names[index])

            if name == 'AUC':
                self.__auc = value
                self.__html_table2_data.append(['AUC', value, class_name])
            elif name in ('PRECISION', 'RECALL', 'F1_SCORE', 'SUPPORT'):
                self.__classes[class_name] = class_name
                self.__map[name + class_name] = value
            else:
                self.__html_table2_data.append([name, value, class_name])

        classes = list(self.__classes.keys())
        for index in range(0, len(classes)):
            data = []
            class_name = classes[index]
            data.append(class_name)
            data.append(self.__map.get('PRECISION' + class_name))
            data.append(self.__map.get('RECALL' + class_name))
            data.append(self.__map.get('F1_SCORE' + class_name))
            data.append(self.__map.get('SUPPORT' + class_name))

            self.__html_table1_data.append(data)

    def build(self):
        self.__clear()
        if isinstance(self.__statistic_table, dataframe.DataFrame):
            self.__transform_data_format(self.__statistic_table.collect())
        else:
            self.__transform_data_format(self.__statistic_table)
        table1_html = TemplateUtil.generate_table(
            self.__html_table1_columns, self.__html_table1_data)
        table2_html = TemplateUtil.generate_table(
            self.__html_table2_columns, self.__html_table2_data)

        section_html = '<h5><span>SCORING TABLE</span></h5><br>' +\
            table1_html + '<br><h5><span>STATS TABLE</span></h5>' + table2_html

        self.__generated_html = section_html

    def get_generated_html(self):
        return self.__generated_html


class ParameterReportBuilder(object):
    def __init__(self, param_columns=None, display_columns=None):
        self.__parameter_table = None

        self.__html_table_data = []
        self.__generated_html = None
        self.param_columns = param_columns
        self.display_columns = display_columns

        self.__parameter_table_columns = ['PARAM_NAME', 'INT_VALUE', 'DOUBLE_VALUE', 'STRING_VALUE']
        self.__html_table_columns = ['PARAM NAME', 'INT VALUE', 'DOUBLE VALUE', 'STRING VALUE']

        if param_columns is not None:
            self.__parameter_table_columns = param_columns
        if display_columns is  not None:
            self.__html_table_columns = display_columns

    def get_table_columns(self):
        return self.__parameter_table_columns.copy()

    def set_parameter_table(self, parameter_table: pandas.DataFrame):
        self.__parameter_table = parameter_table

    def __clear(self):
        self.__html_table_data = []
        self.__generated_html = None

    def __transform_data_format(self, pandas_df: pandas.DataFrame):
        cols = []
        for key in range(0, len(self.__parameter_table_columns)):
            cols.append(list(pandas_df[self.__parameter_table_columns[key]]))

        for index in range(0, len(cols[0])):
            data = []
            for idx in cols:
                data.append(str(idx[index]))
            self.__html_table_data.append(data)

    def build(self):
        self.__clear()
        self.__transform_data_format(self.__parameter_table)
        table_html = TemplateUtil.generate_table(
            self.__html_table_columns, self.__html_table_data)
        section_html = table_html
        self.__generated_html = section_html
    def get_generated_html(self):
        return self.__generated_html


class ConfusionMatrixReportBuilder(object):
    def __init__(self):
        self.__confusion_matrix_table = None
        self.__generated_html = None
        self.__generated_js = None

    def set_confusion_matrix_table(self, confusion_matrix_table: dataframe.DataFrame):
        self.__confusion_matrix_table = confusion_matrix_table

    def __clear(self):
        self.__generated_html = None
        self.__generated_js = None

    @staticmethod
    def get_confusion_matrix_data(pandas_df: pandas.DataFrame):
        class_names = list(np.unique(pandas_df['ACTUAL_CLASS']))
        classname_index_map = {}
        for i in range(0, len(class_names)):
            classname_index_map[class_names[i]] = i
        confusion_matrix_list = []
        actual_class_list = list(pandas_df['ACTUAL_CLASS'])
        predicted_class_list = list(pandas_df['PREDICTED_CLASS'])
        count_list = list(pandas_df['COUNT'])
        for i in range(0, len(predicted_class_list)):
            confusion_matrix_list.append([classname_index_map[predicted_class_list[i]], classname_index_map[actual_class_list[i]], count_list[i]])
        return class_names, max(count_list), confusion_matrix_list

    def build(self):
        self.__clear()
        pandas_df = None
        if isinstance(self.__confusion_matrix_table, dataframe.DataFrame):
            pandas_df = self.__confusion_matrix_table.collect()
        else:
            pandas_df = self.__confusion_matrix_table
        classname_list, z_max, x_y_z_list = ConfusionMatrixReportBuilder.get_confusion_matrix_data(pandas_df)
        title = 'Confusion Matrix'
        name_list = classname_list
        label_list = ['Predicted label', 'True label']
        chart_id = TemplateUtil.get_echart_id()
        # section_html = TemplateUtil.generate_echart(chart_id)
        height = len(name_list) * 100 + 200
        section_html = '<div style="height:800px;width:100%;overflow: scroll;margin-top:10px"><div id="{}" style="height:{}px;width:{}px;"></div></div>'.format(chart_id, height, height)
        load_chart_js = EchartsUtil.generate_load_heatmap_js(chart_id, title, name_list, label_list, z_max, x_y_z_list)

        self.__generated_html = section_html
        self.__generated_js = load_chart_js

    def get_generated_html_and_js(self):
        return self.__generated_html, self.__generated_js


class VariableImportanceReportBuilder(object):
    def __init__(self):
        self.__variable_importance_table = None
        self.__generated_html = None
        self.__generated_js = None

    def set_variable_importance_table(self, variable_importance_table):
        self.__variable_importance_table = variable_importance_table.sort_values(by=['IMPORTANCE'])

    def __clear(self):
        self.__generated_html = None
        self.__generated_js = None

    def build(self):
        self.__clear()
        pandas_df = None
        if isinstance(self.__variable_importance_table, dataframe.DataFrame):
            pandas_df = self.__variable_importance_table.collect()
        else:
            pandas_df = self.__variable_importance_table
        pandas_df["IMPORTANCE"] = pandas.to_numeric(pandas_df['IMPORTANCE'])
        pandas_df = pandas_df[pandas_df['IMPORTANCE'] > 0]
        data_names = list(pandas_df['VARIABLE_NAME'])
        data_values = list(pandas_df['IMPORTANCE'])
        height = 400
        if len(data_names) > 13:
            height = 35 * len(data_names)
        chart_id = TemplateUtil.get_echart_id()
        chart1_html = '<div style="height:800px;width:100%;overflow: scroll;margin-top:10px"><div id="{}" style="height:{}px;"></div></div>'.format(chart_id, height + 50)
        load_chart1_js = EchartsUtil.generate_load_pie_js(
            chart_id, data_names=data_names, data_values=data_values)
        chart_id = TemplateUtil.get_echart_id()
        chart2_html = '<div style="height:800px;width:100%;overflow: scroll;margin-top:10px"><div id="{}" style="height:{}px;"></div></div>'.format(chart_id, height)
        load_chart2_js = EchartsUtil.generate_load_bar_js(
            chart_id, data_names=data_names, data_values=data_values)

        data = []
        data.append(
            TemplateUtil.construct_tab_item_data(
                'Pie Chart', chart1_html))
        data.append(
            TemplateUtil.construct_tab_item_data(
                'Bar Chart', chart2_html))

        tab_html, nav_id = TemplateUtil.generate_tab(data)
        section_html = tab_html

        load_chart_js = '''
            {js_1}
            $(function(){{
                $('{id}').on('shown.bs.tab', function (e) {{
                    var activeTab_name = $(e.target).text();
                    if (activeTab_name === '{name1}')
                    {{
                        {js_1}
                    }}
                    else
                    {{
                        {js_2}
                    }}
                }});
            }});
        '''.format(id='#{} a[data-toggle="tab"]'.format(nav_id),
                   name1='Pie Chart',
                   js_1=load_chart1_js,
                   js_2=load_chart2_js)

        self.__generated_html = section_html
        self.__generated_js = load_chart_js

    def get_generated_html_and_js(self):
        return self.__generated_html, self.__generated_js


class MetricReportBuilder(object):
    def __init__(self):
        self.__metric_table = None
        self.__table_map = {}

        self.__roc_chart_html = None
        self.__load_roc_chart_js = ''

        self.__cumgain_chart_html = None
        self.__load_cumgain_chart_js = ''

        self.__lift_chart_html = None
        self.__load_lift_chart_js = ''

        self.__cumlift_chart_html = None
        self.__load_cumlift_chart_js = ''

        self.__generated_html = None
        self.__generated_js = None

    def set_metric_table(self, metric_table: dataframe.DataFrame):
        self.__metric_table = metric_table
        self.__split_multi_tables()
        self.__transform_data_format()

    def set_roc_sampling(self, sampling: Sampling):
        self.transform_roc_data_format(sampling)

    def set_cumgain_sampling(self, sampling: Sampling, random_sampling: Sampling, perf_sampling: Sampling):
        self.transform_cumgain_data_format(sampling, random_sampling, perf_sampling)

    def set_lift_sampling(self, sampling: Sampling, random_sampling: Sampling, perf_sampling: Sampling):
        self.transform_lift_data_format(sampling, random_sampling, perf_sampling)

    def set_cumlift_sampling(self, sampling: Sampling, random_sampling: Sampling, perf_sampling: Sampling):
        self.transform_cumlift_data_format(sampling, random_sampling, perf_sampling)

    __METRIC_COLUMN_NAMES = [
        'ROC_TPR', 'ROC_FPR',
        'CUMGAINS', 'RANDOM_CUMGAINS', 'PERF_CUMGAINS',
        'LIFT', 'RANDOM_LIFT', 'PERF_LIFT',
        'CUMLIFT', 'RANDOM_CUMLIFT', 'PERF_CUMLIFT'
    ]

    __ROC_DESC = {
        'title': 'ROC',
        'label': 'ROC Curve',
        'xlabel': 'False Positive Rate (FPR)',
        'ylabel': 'True Positive Rate (TPR)'
    }

    __CUM_GAIN_DESC = {
        'title': 'Cumulative Gains',
        'label': 'Cumulative Gains Curve',
        'xlabel': 'Population',
        'ylabel': 'True Positive Rate (TPR)'
    }

    __CUM_LIFT_DESC = {
        'title': 'Cumulative Lift',
        'label': 'Cumulative Lift Curve',
        'xlabel': 'Population',
        'ylabel': 'Lift'
    }

    __LIFT_DESC = {
        'title': 'Lift',
        'label': 'Lift Curve',
        'xlabel': 'Population',
        'ylabel': 'Interval Lift'
    }

    @staticmethod
    def __get_roc_chart_data(x, y):# pylint: disable=invalid-name
        return [
            {
                'x': x,
                'y': y,
                'label': 'model',
                'color_index': 0
            },
            {
                'x': [0, 1],
                'y': [0, 1],
                'label': 'Random model',
                'color_index': 2
            }
        ]

    @staticmethod
    def __get_chart_data(x, y, random_x, random_y, perf_x, perf_y):# pylint: disable=invalid-name
        return [
            {
                'x': x,
                'y': y,
                'label': 'model',
                'color_index': 0
            },
            {
                'x': perf_x,
                'y': perf_y,
                'label': 'Perfect model',
                'color_index': 1
            },
            {
                'x': random_x,
                'y': random_y,
                'label': 'Random model',
                'color_index': 2
            }
        ]

    @staticmethod
    def __generate_chart_code(chart_text, chart_data):
        chart_id = TemplateUtil.get_echart_id()
        chart_html = TemplateUtil.generate_echart(chart_id)
        load_chart_js = EchartsUtil.generate_load_line_js(
            chart_id, chart_text=chart_text, chart_data=chart_data)
        return chart_html, load_chart_js

    def __split_multi_tables(self):
        for name in MetricReportBuilder.__METRIC_COLUMN_NAMES:
            self.__table_map[name] = self.__metric_table.filter("NAME='{}'".format(name))

    def transform_roc_data_format(self, roc_sampling=None):
        tpr_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[0])
        fpr_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[1])

        if tpr_table.shape[0] == 0 or fpr_table.shape[0] == 0:
            return

        if roc_sampling:
            tpr_table = roc_sampling.fit_transform(data=tpr_table)
            fpr_table = roc_sampling.fit_transform(data=fpr_table)

        roc_chart_data = self.__get_roc_chart_data(
            list(fpr_table.select('Y').sort('Y').collect()['Y']),
            list(tpr_table.select('Y').sort('Y').collect()['Y']))

        self.__roc_chart_html, self.__load_roc_chart_js = MetricReportBuilder.__generate_chart_code(
            MetricReportBuilder.__ROC_DESC, roc_chart_data)

    def transform_cumgain_data_format(self, sampling=None, random_sampling=None, perf_sampling=None):
        cumgain_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[2])
        random_cumgain_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[3])
        perf_cumgain_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[4])

        if cumgain_table.shape[0] == 0:
            return

        if sampling:
            cumgain_table = sampling.fit_transform(data=cumgain_table)
        if random_sampling:
            random_cumgain_table = random_sampling.fit_transform(data=random_cumgain_table)
        if perf_sampling:
            perf_cumgain_table = perf_sampling.fit_transform(data=perf_cumgain_table)

        cumgain_chart_data = self.__get_chart_data(
            list(cumgain_table.select('X').collect()['X']), list(cumgain_table.select('Y').collect()['Y']),
            list(random_cumgain_table.select('X').collect()['X']), list(random_cumgain_table.select('Y').collect()['Y']),
            list(perf_cumgain_table.select('X').collect()['X']), list(perf_cumgain_table.select('Y').collect()['Y']))

        self.__cumgain_chart_html, self.__load_cumgain_chart_js = MetricReportBuilder.__generate_chart_code(
            MetricReportBuilder.__CUM_GAIN_DESC, cumgain_chart_data)

    def transform_lift_data_format(self, sampling=None, random_sampling=None, perf_sampling=None):
        lift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[5])
        random_lift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[6])
        perf_lift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[7])

        if lift_table.shape[0] == 0:
            return

        if sampling:
            lift_table = sampling.fit_transform(data=lift_table)
        if random_sampling:
            random_lift_table = random_sampling.fit_transform(data=random_lift_table)
        if perf_sampling:
            perf_lift_table = perf_sampling.fit_transform(data=perf_lift_table)

        lift_chart_data = self.__get_chart_data(
            list(lift_table.select('X').collect()['X']), list(lift_table.select('Y').collect()['Y']),
            list(random_lift_table.select('X').collect()['X']), list(random_lift_table.select('Y').collect()['Y']),
            list(perf_lift_table.select('X').collect()['X']), list(perf_lift_table.select('Y').collect()['Y']))

        self.__lift_chart_html, self.__load_lift_chart_js = MetricReportBuilder.__generate_chart_code(
            MetricReportBuilder.__LIFT_DESC, lift_chart_data)

    def transform_cumlift_data_format(self, sampling=None, random_sampling=None, perf_sampling=None):
        cumlift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[8])
        random_cumlift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[9])
        perf_cumlift_table = self.__table_map.get(MetricReportBuilder.__METRIC_COLUMN_NAMES[10])

        if cumlift_table.shape[0] == 0:
            return

        if sampling:
            cumlift_table = sampling.fit_transform(data=cumlift_table)
        if random_sampling:
            random_cumlift_table = random_sampling.fit_transform(data=random_cumlift_table)
        if perf_sampling:
            perf_cumlift_table = perf_sampling.fit_transform(data=perf_cumlift_table)

        cumlift_chart_data = self.__get_chart_data(
            list(cumlift_table.select('X').collect()['X']), list(cumlift_table.select('Y').collect()['Y']),
            list(random_cumlift_table.select('X').collect()['X']), list(random_cumlift_table.select('Y').collect()['Y']),
            list(perf_cumlift_table.select('X').collect()['X']), list(perf_cumlift_table.select('Y').collect()['Y']))

        self.__cumlift_chart_html, self.__load_cumlift_chart_js = MetricReportBuilder.__generate_chart_code(
            MetricReportBuilder.__CUM_LIFT_DESC, cumlift_chart_data)

    def __transform_data_format(self):
        self.transform_roc_data_format()
        self.transform_cumgain_data_format()
        self.transform_lift_data_format()
        self.transform_cumlift_data_format()

    def build(self, sampling=False):
        data = []
        if self.__roc_chart_html:
            data.append(
                TemplateUtil.construct_tab_item_data(
                    MetricReportBuilder.__ROC_DESC['title'],
                    self.__roc_chart_html))
        if self.__cumgain_chart_html:
            data.append(
                TemplateUtil.construct_tab_item_data(
                    MetricReportBuilder.__CUM_GAIN_DESC['title'],
                    self.__cumgain_chart_html))
        if self.__cumlift_chart_html:
            data.append(
                TemplateUtil.construct_tab_item_data(
                    MetricReportBuilder.__CUM_LIFT_DESC['title'],
                    self.__cumlift_chart_html))
        if self.__lift_chart_html:
            data.append(
                TemplateUtil.construct_tab_item_data(
                    MetricReportBuilder.__LIFT_DESC['title'],
                    self.__lift_chart_html))

        tab_html, nav_id = TemplateUtil.generate_tab(data)
        section_html = tab_html

        load_chart_js = '''
            {js_1}
            $(function(){{
                $('{id}').on('shown.bs.tab', function (e) {{
                    var activeTab_name = $(e.target).text();
                    if (activeTab_name === '{name1}')
                    {{
                        {js_1}
                    }}
                    else if (activeTab_name === '{name2}')
                    {{
                        {js_2}
                    }}
                    else if (activeTab_name === '{name3}')
                    {{
                        {js_3}
                    }}
                    else
                    {{
                        {js_4}
                    }}
                }});
            }});
        '''.format(id='#{} a[data-toggle="tab"]'.format(nav_id),
                   name1=MetricReportBuilder.__ROC_DESC['title'],
                   name2=MetricReportBuilder.__LIFT_DESC['title'],
                   name3=MetricReportBuilder.__CUM_LIFT_DESC['title'],
                   js_1=self.__load_roc_chart_js,
                   js_2=self.__load_lift_chart_js,
                   js_3=self.__load_cumlift_chart_js,
                   js_4=self.__load_cumgain_chart_js)

        if sampling:
            return section_html, load_chart_js

        self.__generated_html = section_html
        self.__generated_js = load_chart_js
        return None

    def get_generated_html_and_js(self):
        return self.__generated_html, self.__generated_js


class _UnifiedClassificationReportBuilder(object):
    def __init__(self, param_columns=None, display_columns=None):
        self.__statistic_report_builder = StatisticReportBuilder()
        self.__scoring_statistic_report_builder = StatisticReportBuilder()
        self.__parameter_report_builder = ParameterReportBuilder(param_columns, display_columns)
        self.__optimal_parameter_report_builder = ParameterReportBuilder()
        # self.__training_data: dataframe.DataFrame = None
        self.__confusion_matrix_report_builder = ConfusionMatrixReportBuilder()
        self.__variable_importance_report_builder = VariableImportanceReportBuilder()
        self.__metric_report_builder = MetricReportBuilder()
        self.__scoring_metric_report_builder = MetricReportBuilder()
        # self.__model: dataframe.DataFrame = None

        self.__all_html = None
        self.__all_js = None

        self.__report_html = None
        self.__iframe_report_html = None
        self.__report_sampling_html = None
        self.__iframe_report_sampling_html = None
        self.roc_sampling = None
        self.other_samplings = None

    def __clear_data(self):
        self.__all_html = ''
        self.__all_js = ''

    def _set_statistic_table(self, statistic_table):
        if statistic_table is not None and statistic_table.shape[0] > 0:
            self.__statistic_report_builder.set_statistic_table(statistic_table)
            self.__statistic_report_builder.build()

        return self

    def _set_scoring_statistic_table(self, statistic_table):
        if statistic_table is not None and statistic_table.shape[0] > 0:
            self.__scoring_statistic_report_builder.set_statistic_table(statistic_table)
            self.__scoring_statistic_report_builder.build()

        return self

    def _set_parameter_table(self, parameter_table: pandas.DataFrame):
        if parameter_table is not None and parameter_table.empty is False:
            self.__parameter_report_builder.set_parameter_table(parameter_table)
            self.__parameter_report_builder.build()

        return self

    def _set_optimal_parameter_table(self, parameter_table: pandas.DataFrame):
        if parameter_table is not None and parameter_table.empty is False:
            self.__optimal_parameter_report_builder.set_parameter_table(parameter_table)
            self.__optimal_parameter_report_builder.build()

        return self

    # def set_training_data(self, data: dataframe.DataFrame):
    #     if data and data.count() > 0:
    #         self.__training_data = data
    #     else:
    #         raise Exception('Training data is empty.')
    #
    #     return self

    def _set_confusion_matrix_table(self, confusion_matrix_table):
        if confusion_matrix_table is not None and confusion_matrix_table.shape[0] > 0:
            self.__confusion_matrix_report_builder.set_confusion_matrix_table(confusion_matrix_table)
            self.__confusion_matrix_report_builder.build()

        return self

    def _set_variable_importance_table(self, variable_importance_table):
        if variable_importance_table is not None and variable_importance_table.shape[0] > 0:
            self.__variable_importance_report_builder.set_variable_importance_table(variable_importance_table)
            self.__variable_importance_report_builder.build()

        return self

    def _set_metric_table(self, metric_table):
        if metric_table and metric_table.shape[0] > 0:
            self.__metric_report_builder.set_metric_table(metric_table)
            self.__metric_report_builder.build()
        if self.roc_sampling or self.other_samplings:
            other_samplings = self.other_samplings
            self.__metric_report_builder.set_roc_sampling(self.roc_sampling)

            if other_samplings is None:
                other_samplings = {}

            self.__metric_report_builder.set_cumgain_sampling(
                other_samplings.get('CUMGAINS'),
                other_samplings.get('RANDOM_CUMGAINS'),
                other_samplings.get('PERF_CUMGAINS'))

            self.__metric_report_builder.set_lift_sampling(
                other_samplings.get('LIFT'),
                other_samplings.get('RANDOM_LIFT'),
                other_samplings.get('PERF_LIFT'))

            self.__metric_report_builder.set_cumlift_sampling(
                other_samplings.get('CUMLIFT'),
                other_samplings.get('RANDOM_CUMLIFT'),
                other_samplings.get('PERF_CUMLIFT'))

        return self

    def _set_scoring_metric_table(self, metric_table):
        if metric_table and metric_table.shape[0] > 0:
            self.__scoring_metric_report_builder.set_metric_table(metric_table)
            self.__scoring_metric_report_builder.build()
        if self.roc_sampling or self.other_samplings:
            other_samplings = self.other_samplings
            self.__scoring_metric_report_builder.set_roc_sampling(self.roc_sampling)

            if other_samplings is None:
                other_samplings = {}

            self.__scoring_metric_report_builder.set_cumgain_sampling(
                other_samplings.get('CUMGAINS'),
                other_samplings.get('RANDOM_CUMGAINS'),
                other_samplings.get('PERF_CUMGAINS'))

            self.__scoring_metric_report_builder.set_lift_sampling(
                other_samplings.get('LIFT'),
                other_samplings.get('RANDOM_LIFT'),
                other_samplings.get('PERF_LIFT'))

            self.__scoring_metric_report_builder.set_cumlift_sampling(
                other_samplings.get('CUMLIFT'),
                other_samplings.get('RANDOM_CUMLIFT'),
                other_samplings.get('PERF_CUMLIFT'))

        return self

    # def load_model(self, model: dataframe.DataFrame):
    #     if model and model.count() > 0:
    #         self.__model = model
    #     else:
    #         raise Exception('Model is empty.')
    #
    #     return self

    def __add_html(self, generated_html):
        if generated_html:
            self.__all_html = self.__all_html + generated_html

    def __add_js(self, generated_js):
        if generated_js:
            self.__all_js = self.__all_js + generated_js

    def _render_report(self, metric_sampling=False):
        if self.roc_sampling or self.other_samplings:
            metric_sampling = True
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.__clear_data()

        statistic_body_html = self.__statistic_report_builder.get_generated_html()
        scoring_statistic_body_html = self.__scoring_statistic_report_builder.get_generated_html()
        if scoring_statistic_body_html is None:
            scoring_statistic_body_html = 'If you want to view the scoring statistics, please call the score function.'
        parameter_body_html = self.__parameter_report_builder.get_generated_html()
        optimal_parameter_body_html = self.__optimal_parameter_report_builder.get_generated_html()
        confusion_matrix_body_html, load_chart_js = self.__confusion_matrix_report_builder.get_generated_html_and_js()
        self.__add_js(load_chart_js)

        # sample_html = ''
        # if self.__training_data.count() >= 10:
        #     sample_html = TemplateUtil.convert_pandas_to_html(self.__training_data.head(10).collect())
        # else:
        #     sample_html = TemplateUtil.convert_pandas_to_html(self.__training_data.collect())

        variable_importance_body_html, load_chart_js = self.__variable_importance_report_builder.get_generated_html_and_js()
        self.__add_js(load_chart_js)

        metrics_body_html = ''
        if metric_sampling:
            metrics_body_html, load_chart_js = self.__metric_report_builder.build(sampling=True)
        else:
            metrics_body_html, load_chart_js = self.__metric_report_builder.get_generated_html_and_js()
        self.__add_js(load_chart_js)

        scoring_metrics_body_html = ''
        if metric_sampling:
            scoring_metrics_body_html, scoring_load_chart_js = self.__scoring_metric_report_builder.build(sampling=True)
        else:
            scoring_metrics_body_html, scoring_load_chart_js = self.__scoring_metric_report_builder.get_generated_html_and_js()
        if scoring_metrics_body_html is None:
            scoring_metrics_body_html = 'If you want to view the scoring metrics, please call the score function.'
        self.__add_js(scoring_load_chart_js)

        # model_html = TemplateUtil.generate_table_html(self.__model, ['ROW INDEX', 'PART INDEX', 'MODEL CONTENT'])

        template = TemplateUtil.get_template('unified_classification_model_report.html')
        report_html = template.render(
            title='Unified Classification',
            start_time=start_time,
            statistic=statistic_body_html,
            scoring_statistic=scoring_statistic_body_html,
            parameter=parameter_body_html,
            optimal_parameter=optimal_parameter_body_html,
            # sample=sample_html,
            confusion_matrix=confusion_matrix_body_html,
            variable_importance=variable_importance_body_html,
            metrics=metrics_body_html,
            scoring_metrics=scoring_metrics_body_html,
            # model=model_html,
            load_echarts_js=self.__all_js)

        if metric_sampling is False:
            self.__report_html = minify(report_html, remove_all_empty_space=True, remove_comments=True)
            self.__iframe_report_html = TemplateUtil.get_notebook_iframe(self.__report_html)
        else:
            self.__report_sampling_html = minify(report_html, remove_all_empty_space=True, remove_comments=True)
            self.__iframe_report_sampling_html = TemplateUtil.get_notebook_iframe(self.__report_sampling_html)

    def set_metric_samplings(self, roc_sampling: Sampling = None, other_samplings: dict = None):
        """
        Set metric samplings to report builder.

        Parameters
        ----------
        roc_sampling : :class:`~hana_ml.algorithms.pal.preprocessing.Sampling`, optional
            ROC sampling.

        other_samplings : dict, optional
            Key is column name of metric table.

                - CUMGAINS
                - RANDOM_CUMGAINS
                - PERF_CUMGAINS
                - LIFT
                - RANDOM_LIFT
                - PERF_LIFT
                - CUMLIFT
                - RANDOM_CUMLIFT
                - PERF_CUMLIFT

            Value is sampling.

        Examples
        --------
        Creating the metric samplings:

        >>> roc_sampling = Sampling(method='every_nth', interval=2)

        >>> other_samplings = dict(CUMGAINS=Sampling(method='every_nth', interval=2),
                              LIFT=Sampling(method='every_nth', interval=2),
                              CUMLIFT=Sampling(method='every_nth', interval=2))
        >>> model.set_metric_samplings(roc_sampling, other_samplings)
        """
        self.roc_sampling = roc_sampling
        self.other_samplings = other_samplings

    def build_report(self):
        """
        Build model report.
        """

        raise NotImplementedError # to be implemented by subclass

    @property
    def report(self):
        if self.__iframe_report_sampling_html:
            return self.__iframe_report_sampling_html
        else:
            return self.__iframe_report_html

    def generate_html_report(self, filename, metric_sampling=False):
        """
        Save model report as a html file.

        Parameters
        ----------
        filename : str
            Html file name.

        metric_sampling : bool, optional
            Whether the metric table needs to be sampled.
        """
        if self.roc_sampling or self.other_samplings:
            metric_sampling = True
        if (self.__report_html is None) and (self.__report_sampling_html is None):
            raise Exception('To generate a report, you must call the build_report method firstly.')

        if metric_sampling:
            if self.__report_sampling_html:
                TemplateUtil.generate_html_file('{}_unified_classification_model_report.html'.format(filename), self.__report_sampling_html)
            else:
                TemplateUtil.generate_html_file('{}_unified_classification_model_report.html'.format(filename), self.__report_html)
        else:
            if self.__report_html:
                TemplateUtil.generate_html_file('{}_unified_classification_model_report.html'.format(filename), self.__report_html)
            else:
                TemplateUtil.generate_html_file('{}_unified_classification_model_report.html'.format(filename), self.__report_sampling_html)

    def generate_notebook_iframe_report(self, metric_sampling=False):
        """
        Render model report as a notebook iframe.

        Parameters
        ----------
        metric_sampling : bool, optional
            Whether the metric table needs to be sampled.
        """
        if self.roc_sampling or self.other_samplings:
            metric_sampling = True
        if (self.__iframe_report_html is None) and (self.__iframe_report_sampling_html is None):
            raise Exception('To generate a report, you must call the build_report method firstly.')

        print('\033[31m{}'.format('In order to review the unified classification model report better, '
                                  'you need to adjust the size of the left area or hide the left area temporarily!'))
        if metric_sampling:
            if self.__iframe_report_sampling_html:
                display(HTML(self.__iframe_report_sampling_html))
            else:
                display(HTML(self.__iframe_report_html))
        else:
            if self.__iframe_report_html:
                display(HTML(self.__iframe_report_html))
            else:
                display(HTML(self.__iframe_report_sampling_html))

class _UnifiedRegressionReportBuilder(object):
    def __init__(self, param_columns=None, display_columns=None):
        self.__parameter_report_builder = ParameterReportBuilder(param_columns, display_columns)
        self.__optimal_parameter_report_builder = ParameterReportBuilder()
        self.__statistic_table: dataframe.DataFrame = None
        self.__scoring_statistic_table: dataframe.DataFrame = None
        self.__variable_importance_report_builder = VariableImportanceReportBuilder()
        # self.__training_data: dataframe.DataFrame = None
        # self.__model: dataframe.DataFrame = None

        self.__all_html = None

        self.__report_html = None
        self.__iframe_report_html = None
        self.__all_js = None

    def __clear_data(self):
        self.__all_html = ''
        self.__all_js = ''

    def _set_statistic_table(self, statistic_table):
        if statistic_table and statistic_table.shape[0] > 0:
            self.__statistic_table = statistic_table

        return self

    def _set_scoring_statistic_table(self, statistic_table):
        if statistic_table and statistic_table.shape[0] > 0:
            self.__scoring_statistic_table = statistic_table

        return self

    def _set_parameter_table(self, parameter_table: pandas.DataFrame):
        if parameter_table is not None and parameter_table.empty is False:
            self.__parameter_report_builder.set_parameter_table(parameter_table)
            self.__parameter_report_builder.build()

        return self

    def _set_optimal_parameter_table(self, parameter_table: pandas.DataFrame):
        if parameter_table is not None and parameter_table.empty is False:
            self.__optimal_parameter_report_builder.set_parameter_table(parameter_table)
            self.__optimal_parameter_report_builder.build()

        return self

    def _set_variable_importance_table(self, variable_importance_table):
        if variable_importance_table is not None and variable_importance_table.shape[0] > 0:
            self.__variable_importance_report_builder.set_variable_importance_table(variable_importance_table)
            self.__variable_importance_report_builder.build()

        return self

    def __add_html(self, generated_html):
        if generated_html:
            self.__all_html = self.__all_html + generated_html

    def __add_js(self, generated_js):
        if generated_js:
            self.__all_js = self.__all_js + generated_js

    def _render_report(self):
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.__clear_data()

        statistic_body_html = None
        if self.__statistic_table:
            statistic_body_html = TemplateUtil.generate_table_html(self.__statistic_table, ['STAT NAME', 'STAT VALUE'])
        scoring_statistic_body_html = None
        if self.__scoring_statistic_table:
            scoring_statistic_body_html = TemplateUtil.generate_table_html(self.__scoring_statistic_table, ['STAT NAME', 'STAT VALUE'])
        if scoring_statistic_body_html is None:
            scoring_statistic_body_html = 'If you want to view the scoring statistics, please call the score function.'
        parameter_body_html = self.__parameter_report_builder.get_generated_html()
        optimal_parameter_body_html = self.__optimal_parameter_report_builder.get_generated_html()

        # sample_html = ''
        # if self.__training_data.count() >= 10:
        #     sample_html = TemplateUtil.convert_pandas_to_html(self.__training_data.head(10).collect())
        # else:
        #     sample_html = TemplateUtil.convert_pandas_to_html(self.__training_data.collect())
        # model_html = TemplateUtil.generate_table_html(self.__model, ['ROW INDEX', 'PART INDEX', 'MODEL CONTENT'])
        variable_importance_body_html, load_chart_js = self.__variable_importance_report_builder.get_generated_html_and_js()
        self.__add_js(load_chart_js)
        template = TemplateUtil.get_template('unified_regression_model_report.html')
        self.__report_html = template.render(
            title='Unified Regression',
            start_time=start_time,
            statistic=statistic_body_html,
            scoring_statistic=scoring_statistic_body_html,
            parameter=parameter_body_html,
            optimal_parameter=optimal_parameter_body_html,
            variable_importance=variable_importance_body_html,
            load_echarts_js=self.__all_js)

            # sample=sample_html)
            # model=model_html)
        self.__report_html = minify(self.__report_html, remove_all_empty_space=True, remove_comments=True)
        self.__iframe_report_html = TemplateUtil.get_notebook_iframe(self.__report_html)

    def build_report(self):
        """
        Build model report.
        """

        raise NotImplementedError # to be implemented by subclass

    @property
    def report(self):
        return self.__iframe_report_html

    def generate_html_report(self, filename):
        """
        Save model report as a html file.

        Parameters
        ----------
        filename : str
            Html file name.
        """
        if self.__report_html is None:
            raise Exception('To generate a report, you must call the build_report method firstly.')

        TemplateUtil.generate_html_file('{}_unified_regression_model_report.html'.format(filename), self.__report_html)

    def generate_notebook_iframe_report(self):
        """
        Render model report as a notebook iframe.
        """
        if self.__iframe_report_html is None:
            raise Exception('To generate a report, you must call the build_report method firstly.')

        print('\033[31m{}'.format('In order to review the unified regression model report better, '
                                  'you need to adjust the size of the left area or hide the left area temporarily!'))
        display(HTML(self.__iframe_report_html))
