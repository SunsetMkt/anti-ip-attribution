#! /usr/bin/env python3
# 针对部分网站显示IP归属地的分流规则
# anti-ip-attribution generate.py
# https://github.com/lwd-temp/anti-ip-attribution
# 从rules.yaml生成配置文件，由Actions调用。
# 读取文件：
# rules.yaml 配置文件
# parser-header.yaml parser.yaml的生成模板
# 输出文件：
# parser.yaml 适用于Clash for Windows的配置文件预处理功能，详见https://docs.cfw.lbyczf.com/contents/parser.html
# rule-provider.yaml 适用于Clash的Rule Provider功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider
# surge.list Surge分流规则
# quantumultx.list QuantumultX分流规则
import os

import yaml


def read_yaml(file):
    '''读取YAML文件'''
    with open(file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml(config, filename):
    '''保存YAML文件'''
    with open(filename, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False)


def get_yaml_string(config):
    '''获取YAML字符串'''
    return yaml.dump(config, default_flow_style=False)


def save_string(string, filename):
    '''保存字符串'''
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(string)


def get_head_comment(config, filename='', description=''):
    '''获取头部注释'''
    comment = ''
    comment += '# ' + config['config']['description'] + '\n'
    comment += '# ' + config['config']['name'] + ' ' + \
        filename + config['config']['version'] + '\n'
    comment += '# ' + config['config']['url'] + '\n'
    comment += '# ' + description + '\n'
    return comment


def seprate_comma(string):
    '''分割字符串'''
    return string.split(',')


def generate_parser(config):
    '''生成parser.yaml'''
    head = read_yaml('parser-header.yaml')
    print(head)
    comment = get_head_comment(
        config, 'parser.yaml', '适用于Clash for Windows的配置文件预处理功能，详见https://docs.cfw.lbyczf.com/contents/parser.html')
    rules = []
    for rule in config['config']['rules']:
        rule = rule.strip()
        if len(seprate_comma(rule)) == 2:
            rules.append(rule+',IP归属地')
        else:
            rules.append(rule)
    head['parsers'][0]['yaml']['prepend-rules'] = rules
    output = get_yaml_string(head)
    output = comment + output
    save_string(output, os.path.join('generated', 'parser.yaml'))


def generate_rule_provider(config):
    '''生成rule-provider.yaml'''
    comment = get_head_comment(
        config, 'rule-provider.yaml', '适用于Clash的Rule Provider功能，详见https://lancellc.gitbook.io/clash/clash-config-file/rule-provider')
    rules = config['config']['rules']
    output = {}
    output['payload'] = rules
    output = comment + get_yaml_string(output)
    save_string(output, os.path.join('generated', 'rule-provider.yaml'))


def generate_surge(config):
    '''生成surge.list'''
    comment = get_head_comment(
        config, 'surge.list', 'Surge分流规则')
    rules = ''
    for rule in config['config']['rules']:
        rules += rule + '\n'
    output = comment + rules
    save_string(output, os.path.join('generated', 'surge.list'))


def generate_quantumultx(config):
    '''生成quantumultx.list'''
    comment = get_head_comment(
        config, 'quantumultx.list', 'QuantumultX分流规则')
    rules = ''
    for rule in config['config']['rules']:
        rule = rule.strip()
        if len(seprate_comma(rule)) == 2:
            rules += rule + ',IP\n'
        else:
            rules += rule + '\n'
    output = comment + rules
    save_string(output, os.path.join('generated', 'quantumultx.list'))


if __name__ == '__main__':
    print('开始生成配置文件...')
    config = read_yaml('rules.yaml')
    print(config)
    print('生成parser.yaml...')
    generate_parser(config)
    print('生成rule-provider.yaml...')
    generate_rule_provider(config)
    print('生成surge.list...')
    generate_surge(config)
    print('生成quantumultx.list...')
    generate_quantumultx(config)
    print('生成配置文件完成！')
