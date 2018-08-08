# -*- coding: utf8 -*-

POP3 = {
    'server': 'pop3.sina.com',
    'user': 'm15210521936@sina.com',
    'password': 'msc920521'
}

DATABASE = {
    'host': '127.0.0.1',
    'port': 27017,
    'user': 'watcher',
    'password': 'watcher',
    'database': 'watcher',
    'db': 'MongoDB',
}

DEF_SEVIRITY_RULE = {
    'model': 'KEYWORD',
    'field': '级别',
    'values': ['紧急', '主要', '次要', '警告', '正常'],
}

DEF_SEVIRITY_KEYWORDS = [
    'PROCESS WARNING;批处理运行失败;Status: No answer;Status: Bad;本日调度失败;不可用;分区利用率超过90%;故障中 级别: Disaster;故障中 级别: High;级别：紧急;- 故障 -;级 别：紧急;',
    '>=95%;告警级别：5;- 严重 -;>=96%;>=90%;严重:;故障中 级别: Average;故障中 级别: Warning;故障中 级别: information;故障中 级别: Not classified;',
    '告警级别：4;- 错误 - ;UAT;SIT;>=85%;>=80%;警告:;',
    '告警级别：3;告警级别：2;>=75%;>=70%;- 警告 - ;10.1.188.9;up;',
    '恢复;告警级别：1;信息;状态: 故障已恢复;设备告警结束;Nagios;'
]

DEF_KEYVALUE_RULE = {
    'model': 'KEYVALUE',
    'delimiters': [':', '：'],
    'fields': [
        {
            'field': '服务器名',
            'alias': ['服务器', 'server'],
            'value_re': '\w+',
        },
        {
            'field': 'IP地址',
            'alias': ['服务器IP', 'IP', 'IP地址'],
            'value_re': '\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}',
        },
        {
            'field': '故障描述',
            'alias': ['故障名称'],
            'value_re': '.*',
        },
    ]
}
