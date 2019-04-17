from init import create_app
from quart import jsonify
from utils import logfmt

app = create_app()

@app.route('/')
async def get_index():
    d = {
        "name": "合同管理",
        "id": '7',
        "img": 'icon-hetongguanli-',
        "children": [
            {
                "path": '/annual_contract',
                "name": "全年合同统计表",
                "id": '7-1', 
            }, {
                "path": '/week_contract',
                "name": "周合同统计表",
                "id": '7-2',
            }, {
                "path": '/conduct_statistics',
                "name": "在建项目统计表",
                "id": '7-3',
            }, {
                "path": '/contractList',
                "name": "合同列表",
                "id": '7-4',
            }, {
                "path": '/contracDetails',
                "name": "合同详情",
                "id": '7-5',
            }
        ]
    }
    app.logger.debug(logfmt(d))
    return jsonify({'test': 1})
