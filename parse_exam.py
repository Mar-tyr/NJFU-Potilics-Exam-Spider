# -*- coding: UTF-8 -*-
from lxml import etree
import re
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def is_question(s):
    return not re.match(u'^\\d+、', s) == None


def is_answer(s):
    return not re.match(u'^[A-Z]+$', s) == None


def is_judge_answer(s):
    return not re.match(u'^true|false$', s) == None


def parse_one_page_by_title(rootdir, index, single_dict, multiple_dict, judge_dict):
    with open('{}/{}.html'.format(rootdir, index), 'r') as fp:
        wb_data = fp.read()
    html = etree.HTML(wb_data)

    single = html.xpath('//div[@id="myForm:j_idt190:0:j_idt191_content"]')[0]

    choiceTitles = single.xpath('span[@class="choiceTitle"]')
    choiceTitles = filter(is_question, [item.xpath('string(.)') for item in choiceTitles])
    questions = [item.split('、', 1)[1] for item in choiceTitles]
    answers = filter(is_answer, single.xpath(
        'div[@style="margin-left: 30px;"]/span[@style="color:green;font-weight: bold;"]/text()'))

    option_groups = single.xpath('div[@style="margin-left: 30px;"]')
    option_groups = [option_groups[i * 2].xpath('span[@class="choiceTitle"]/text()') for i in
                     range(len(option_groups) / 2)]

    if not len(questions) == len(answers):
        print 'Single', index, len(questions), len(answers)

    for i, question in enumerate(questions):
        if question not in single_dict:
            single_dict[question] = {'options': option_groups[i], 'answer': answers[i]}

    multiple = html.xpath('//div[@id="myForm:j_idt190:1:j_idt191_content"]')[0]

    choiceTitles = multiple.xpath('span[@class="choiceTitle"]')
    choiceTitles = filter(is_question, [item.xpath('string(.)') for item in choiceTitles])
    questions = [item.split('、', 1)[1] for item in choiceTitles]
    answers = filter(is_answer, multiple.xpath(
        'div[@style="margin-left: 30px;"]/span[@style="color:green;font-weight: bold;"]/text()'))

    option_groups = multiple.xpath('div[@style="margin-left: 30px;"]')
    option_groups = [option_groups[i * 2].xpath('span[@class="choiceTitle"]/text()') for i in
                     range(len(option_groups) / 2)]

    if not len(questions) == len(answers):
        print 'Multiple', index, len(questions), len(answers)

    for i, question in enumerate(questions):
        if question not in multiple_dict:
            multiple_dict[question] = {'options': option_groups[i], 'answer': answers[i]}

    judge = html.xpath('//div[@id="myForm:j_idt190:2:j_idt191_content"]')[0]

    choiceTitles = judge.xpath('span[@class="choiceTitle"]')
    choiceTitles = filter(is_question, [item.xpath('string(.)') for item in choiceTitles])
    questions = [item.split('、', 1)[1] for item in choiceTitles]
    answers = filter(is_judge_answer, judge.xpath(
        'div[@style="margin-left: 30px;"]/span[@style="color:green;font-weight: bold;"]/text()'))

    if not len(questions) == len(answers):
        print 'Judge', index, len(questions), len(answers)

    for i, question in enumerate(questions):
        if question not in judge_dict:
            judge_dict[question] = answers[i]


def parse_exam(rootdir, start_index, end_index):
    single_dict = {}
    multiple_dict = {}
    judge_dict = {}
    for i in range(start_index, end_index):
        parse_one_page_by_title(rootdir, i, single_dict, multiple_dict, judge_dict)
    return {'single': single_dict, 'multiple': multiple_dict, 'judge': judge_dict}


def print_question_num(examfile):
    with open(examfile, 'r') as fp:
        exam_dict = json.load(fp)
    print 'single num:{} multiple num:{} judge num:{}'.format(len(exam_dict['single']), len(exam_dict['multiple']),
                                                              len(exam_dict['judge']))


if __name__ == '__main__':
    exam_type = 'marx'
    exam_dict = parse_exam(exam_type, 0, 600)
    print 'single num:{} multiple num:{} judge num:{}'.format(len(exam_dict['single']), len(exam_dict['multiple']),
                                                              len(exam_dict['judge']))
    with open('{}.json'.format(exam_type), 'w') as fp:
        json.dump(exam_dict, fp, indent=2, ensure_ascii=False)
