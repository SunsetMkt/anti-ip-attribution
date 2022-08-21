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
import sys

import git
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


def get_git_hash():
    '''获取Git提交'''
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.object.hexsha
    return str(sha)


def get_head_comment(config, filename='', description=''):
    '''获取头部注释'''
    comment = ''
    comment += '# ' + config['config']['description'] + '\n'
    comment += '# ' + config['config']['name'] + ' ' + \
        filename + ' ' + config['config']['version'] + \
        ' ' + get_git_hash() + '\n'
    comment += '# ' + config['config']['url'] + '\n'
    comment += '# ' + description + '\n'
    return comment


def seprate_comma(string):
    '''分割字符串'''
    return string.split(',')


def check_rules(config):
    '''检查规则是否有误'''
    rules = config['config']['rules']
    # 预期中可用的规则方法
    expected_methods = ['DOMAIN', 'DOMAIN-SUFFIX',
                        'DOMAIN-KEYWORD', 'IP-CIDR', 'GEOIP', 'DST-PORT', 'IP-CIDR6']
    # 容易出错的规则方法
    questioned_methods = ['SRC-IP-CIDR', 'SRC-PORT', 'RULE-SET', 'MATCH']
    # 预期中可用的规则部分
    expected_rules = ['DIRECT', 'REJECT', 'no-resolve']
    # rules中不需要出现IP类关键词，生成脚本会按需自动添加
    should_not_appear_rules = ['IP', 'IP归属地']
    for rule in rules:
        rule = rule.strip()
        print(rule)
        # 检查空行
        if rule == '':
            print('规则空行')
            return False
        else:
            print('非空行')
        # 检查逗号分隔
        length = len(seprate_comma(rule))
        print('length: ' + str(length))
        if length == 1:
            print('规则不完整？没有逗号分隔？：' + rule)
            return False
        elif length == 2:
            pass
        elif length == 3:
            pass
        else:
            print('规则有误？逗号分隔超过三个部分：' + rule)
            return False
        # 检查规则方法
        method = seprate_comma(rule)[0]
        print('method: ' + method)
        if method not in expected_methods and method not in questioned_methods:
            print('规则方法有误？：' + rule)
            return False
        if method.upper() in questioned_methods:
            print('规则方法有误？' + method + '可能是常见错误：' + rule)
            return False
        if method not in expected_methods and method.upper() in expected_methods:
            print('规则方法未大写？：' + rule)
            return False
        # 检查规则部分
        if length == 3:
            print('length == 3')
            this_rule = seprate_comma(rule)[2]
            print('rule: ' + this_rule)
            if this_rule not in expected_rules:
                print('规则有误？' + this_rule + '是预期之外的规则：' + rule)
                return False
            for should_not_appear_rule in should_not_appear_rules:
                if should_not_appear_rule in this_rule.upper():
                    print('规则有误？rules中不需要出现“IP归属地”类规则描述：' + rule)
                    return False
    return True


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
    config = read_yaml('rules.yaml')
    print(get_head_comment(config, 'generate.py', '配置文件生成脚本'))
    print('=====================')
    print('开始生成配置文件...')
    print('=====================')
    print(config)
    print('=====================')
    print('检查规则是否有误...')
    if check_rules(config):
        print('规则检查通过！')
        print('=====================')
        print('生成parser.yaml...')
        generate_parser(config)
        print('=====================')
        print('生成rule-provider.yaml...')
        generate_rule_provider(config)
        print('=====================')
        print('生成surge.list...')
        generate_surge(config)
        print('=====================')
        print('生成quantumultx.list...')
        generate_quantumultx(config)
        print('=====================')
        print('生成配置文件完成！')
    else:
        print('规则检查未通过！')
        print('=====================')
        print('请检查规则是否有误！')
        print('生成配置文件失败！')
        sys.exit(1)
