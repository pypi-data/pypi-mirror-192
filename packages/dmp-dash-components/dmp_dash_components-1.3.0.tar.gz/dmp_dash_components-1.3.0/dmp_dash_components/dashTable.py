from dash import html
from .AntdButton import *
from .AntdCheckbox import *

class dashTable(html.Div):
    """
    A component to generate dash table. It inheritated keyword arguments form
    dash.html.Div unless specified.
    - data (pandas.DataFrame)
      For non-text data, sort the inputs into the formats below
          - Hyperlink: {'type': 'A', 'href': 'xxxx', 'text': 'xxxx', 'disabled': False}
    - column_mapping (dict, optional)
      {'label': 'text_to_show_in_tHead', 'className': 'class_to_apply', 'style': {}, 'rowspan': False}
    - checkedRows (dict, optional)
      In case there exists a checkbox column
      {'columnaName': ['var1', 'var2']}
    """

    def __init__(self,
                 data=None,
                 column_mapping={},
                 drop_columns=[],
                 *args, **kwargs):
        html.Div.__init__(self, *args, **kwargs)
        if column_mapping:
            rowSpans = {}
            rowspanColumns = {k: v for k, v in column_mapping.items() if v.get('rowSpan') is True}
            if len(rowspanColumns.keys()) > 0:
                for k, v in rowspanColumns.items():
                    if not v.get('rowGroup'):
                        data[k + '_'] = data[k].apply(lambda x: str(x)).tolist()
                        rowSpans[k] = dict(data[k + '_'].value_counts())
                    else:
                        data[k + '_'] = data.apply(lambda x: '_'.join([x[col] for col in v.get('rowGroup')]),axis=1)
                        rowSpans[k] = dict(data[k + '_'].value_counts())
                    data.loc[data.duplicated(subset=[k + '_']), [k + '_']] = ''
                for c in rowspanColumns:
                    data[c] = data.apply(
                        lambda x: dashTable.sortRowSpan(c, x, rowSpans),
                        axis=1)
                data = data.drop(columns=[x + '_' for x in rowspanColumns])

        if drop_columns:
            data = data.drop(columns=drop_columns)
        tHeads, tRows, columnClassNames, columnStyles = [], [], {}, {}
        cols = list(data.columns)
        for i in range(len(cols)):
            columnId, columnName, colContent = cols[i], cols[i], cols[i]
            columnClassName = ['ant-table-cell', '{}-cell'.format(cols[i])]
            columnStyle = None
            if column_mapping.get(columnId):
                if column_mapping[columnId].get('label'):
                    colContent = column_mapping[columnId]['label']
                if column_mapping[columnId].get('className'):
                    columnClassName.append(
                        column_mapping[columnId]['className'])
                if column_mapping[columnId].get('style'):
                    columnStyle = column_mapping[columnId]['style']
                    columnStyles[columnId] = columnStyle
            columnClassName = ' '.join([x.lower() for x in columnClassName if x])
            columnClassNames[columnId] = columnClassName
            thead = html.Th(colContent, className=columnClassName,
                            style=columnStyle)
            tHeads.append(thead)
        values = data.to_dict('records')
        for j in range(len(values)):
            row, tr, td = values[j], [], ''
            for k, v in row.items():
                columnId, columnContent = k, v
                columnStyle = columnStyles.get(columnId)
                columnClassName = columnClassNames.get(columnId)
                if type(columnContent) == dict:
                    if columnContent.get('rowSpan') is not None:
                        if columnContent.get('rowSpan') > 0:
                            td = html.Td(
                                self.sortCellContent(columnContent['content']),
                                className=columnClassName,
                                style=columnStyle,
                                rowSpan=columnContent.get('rowSpan')
                            )
                            tr.append(td)
                    else:
                        td = html.Td(
                            self.sortCellContent(columnContent),
                            className=columnClassName,
                            style=columnStyle)
                        tr.append(td)
                else:
                    td = html.Td(
                        columnContent,
                        className=columnClassName,
                        style=columnStyle)
                    tr.append(td)
            tr = html.Tr([x for x in tr if x], className='ant-table-row')
            tRows.append(tr)

        table_wrapper = html.Div(
            html.Table(
                [
                    html.Thead(
                        html.Tr(tHeads),
                        className='ant-table-thead'
                    ),
                    html.Tbody(
                        tRows,
                        className='ant-table-tbody'
                    )
                ],
                className='ant-table w-100'
            ),
            className='ant-table-content w-100'
        )
        self.children = table_wrapper

    @staticmethod
    def sortRowSpan(col, df, rowSpansDt):
        if not df[col + '_']:
            return {'rowSpan': 0}
        else:
            return {
                'content': df[col],
                'rowSpan': rowSpansDt[col][df[col + '_']]
            }

    @staticmethod
    def sortCellContent(cell):
        if type(cell) in [str, int, float]:
            return cell
        elif type(cell) is list:
            return ', '.join(cell)
        elif type(cell) is dict:
            if cell.get('type') == 'A':
                if cell.get('disabled') is True:
                    return cell['text']
                else:
                    return html.A(
                        cell['text'],
                        href=cell['href'],
                        target='_blank')
            if cell.get('type') == 'Button':
                return AntdButton(
                    cell['text'],
                    type=cell['btnType'] if cell.get('btnType') else 'primary',
                    id=cell['id'] if cell.get('id') else str(cell['text']),
                    style=cell['style'] if cell.get('style') else None,
                    className=cell['className'] if cell.get('className') else None,
                    nClicks=cell['nClicks'] if cell.get('nClicks') else 0
                )
            if cell.get('type') == 'CheckBox':
                return AntdCheckbox(
                        label=cell['text'],
                        id=cell['id'] if cell.get('id') else str(cell['text']),
                        checked=cell['checked'] if cell.get('checked') is True else False
                    )
