# -*- coding: utf8 -*-
# =============================================================================
# 文件:  test_validate.py
# 日期:  2021/4/29 13:18
# 作者:  王秀国
# 版本:  1.0
# 版权:  (C)Copyright 2016-2021, 君迪
# 描述:  财艺通
# =============================================================================
import datetime
import decimal
import unittest
from assertpy import assert_that
from src.jd_tools.param_check.validate import *
from src.jd_tools import logger, JdCheck, JdTools, DT_LONG
from src.jd_tools.param_check.errcode import *


class TestValidator(unittest.TestCase):

    def test_validation(self):

        name, validations, errors = validation('客户名称, 1-50', 'name', who='str')
        assert_that(name).is_equal_to('客户名称')

        name, validations, errors = validation('客户名称, 1a-50a', 'name', who='str')
        assert_that(name).is_equal_to('客户名称')

        name, validations, errors = validation('联系人, 20, opt', 'person', who='str')
        assert_that(name).is_equal_to('联系人')

        # date='充值日期, must'
        name, validations, errors = validation('充值日期, must', 'date', who='date')
        assert_that(name).is_equal_to('充值日期')

        # fee='学费 >= 0, p2'       大于等于0， 小数点后2位
        name, validations, errors = validation('学费  >= 0,  p2', 'fee', who='decimal')
        assert_that(name).is_equal_to('学费')

        # fee='学费 any'            可以转换为 Decimal 的任何值
        name, validations, errors = validation('学费 any', 'fee', who='decimal')
        assert_that(name).is_equal_to('学费')

        # state='状态 , in[0, 1]'    属于某个集合
        name, validations, errors = validation('状态 , in[0, 1]', 'state', who='int')
        assert_that(name).is_equal_to('状态')

    def test_verify_01(self):
        obj = dict(name='123', short_name='1234567890', person='联系人', remark='4')
        ret = verify(
            obj, s=dict(name='客户名称, 1-50', short_name='简名, 1-10', person='联系人, 20', remark='备注, 140, opt'))
        assert_that(ret['code']).is_equal_to(0)

        # fee='学费 >= 0'           大于等于0
        obj = dict(fee=14.56)
        ret = verify(obj, s=dict(fee='学费 >= 0'))
        assert_that(ret['code']).is_equal_to(0)

        obj = dict(title='title', content='content', class_id=20, wx_uid='-123')
        ret = verify(
            obj, str=dict(title='作业标题, 1-20', content='作业内容, 1-1000'),
            int=dict(is_release='是否发布, d0', wx_uid='微信用户ID', class_id='班级ID>0')
        )
        logger.debug(f'obj=%s' % obj)
        logger.debug(f'ret=%s' % ret)
        assert_that(ret['code']).is_not_equal_to(0)

        # In 测试
        obj = dict(is_use_fee=1)
        ret = verify(obj, int=dict(is_use_fee='是否扣费, in[0, 1]'))
        assert_that(ret['code']).is_equal_to(0)
        # print(ret)

        obj = dict(money='45.654')
        ret = verify(
            obj, decimal=dict(money='金额')
        )
        assert_that(ret['code']).is_not_equal_to(0)
        # print(ret)

        obj = dict(money=-45.65)
        ret = verify(
            obj, decimal=dict(money='金额any')
        )
        assert_that(ret['code']).is_equal_to(0)

        obj = dict(join_date='2020-4-5')
        ret = verify(
            obj, date=dict(join_date='登记日期')
        )
        assert_that(ret['code']).is_equal_to(0)

        obj = dict()
        ret = verify(
            obj, date=dict(join_date='登记日期')
        )
        assert_that(ret['code']).is_not_equal_to(0)
        # print(ret)

        obj = dict()
        ret = verify(
            obj, date=dict(join_date='登记日期, opt')
        )
        assert_that(ret['code']).is_equal_to(0)

    def test_verify_02(self):
        logger.debug('执行测试用例 test_verify2')
        obj = dict(dateVal='2022-1-1 - 2022-1-31')
        ret = JdCheck.verify(obj, dateRange=dict(dateVal='时间段'))
        assert_that(ret['code']).is_equal_to(0)
        assert_that(obj['d1']).is_equal_to(datetime.datetime(2022, 1, 1))
        logger.debug(f'obj=%s' % obj)

    def test_verify_03(self):
        obj = dict(dateVal='2022-1-1 - 2022-1-31')
        ret = JdCheck.verify(obj, str=dict(remark='备注,200'))
        assert_that(ret['code']).is_equal_to(0)
        assert_that('remark' not in obj).is_true()

    def test_verify_04(self):
        # 测试 日期 不加时分秒
        dd = '2022-01-01'
        obj = dict(some_date=dd)
        ret = JdCheck.verify(obj, date=dict(some_date='考勤日期, must, no-hms'))
        logger.info(ret)
        assert_that(ret['code']).is_equal_to(0)
        assert_that(JdTools.datetime_to_str(obj['some_date'], DT_LONG)).is_equal_to(dd + ' 00:00:00')

    def test_verify_05(self):
        # 测试 日期 must
        dd = '2022-01-01'
        obj = dict(end_date=dd, start_date=None)
        ret = JdCheck.verify(obj, date=dict(start_date='开始时间, must', end_date='结束时间,opt'))
        logger.info(ret)
        assert_that(ret['code']).is_not_equal_to(0)
        # assert_that(JdTools.datetime_to_str(obj['some_date'])).is_equal_to(dd)

        obj = {'schedule_type': 2, 'start_date': '', 'end_type': 1, 'course_id': 0, 'course_name': '【校区一】',
               'week': '6', 'minutes': 1020, 'room_id': 0, 'room': None, 'class_id': 14798, 'teacher_id': 3345,
               'teacher': '谭老师', 'time': '14:00', 'hour': 14, 'm': 0, 'className': '南屏教学点-艺术团10级班',
               'short_name': '艺术团', 'num': 2, 'otherTeacher': [], 'company_id': 281, 'role_id': 845, 'uid': 1062,
               'last_uid': 1062, 'is_creator': 1, 'recorder': '15919137775', 'last_u': '15919137775', 'is_copy': 0,
               'type': 1, 'end_date': None}
        ret = JdCheck.verify(
            obj, str=dict(short_name='班级简称, 6', time='开课时间, 15', week='星期, 20'),
            int=dict(class_id='班级ID', minutes='分钟', teacher_id='老师ID, d0',
                     room_id='教室ID, d0', schedule_type='排课类型', is_copy='是否克隆, d0,in[0,1]',
                     course_id='课程表id, d0', end_type='结束方式, d0,in[0,1,2]', num='课节总数, d0',
                     type='调课方式, d1'),
            date=dict(start_date='开始时间, must', end_date='结束时间,opt'))
        logger.info(ret)
        assert_that(ret['code']).is_not_equal_to(0)

    def test_verify_06(self):
        logger.debug(f"测试 in 模式， [ 和 ] 不匹配")
        obj = dict(type=3, mode=2)
        ret = JdCheck.verify(obj, int=dict(type='类型,in[1,', mode='模式,d0,in[0,1,2]'))
        logger.info(ret)
        assert_that(ret['code']).is_not_equal_to(0)
        
    def test_verify_07(self):
        logger.debug(f"测试 decimal, 未填写opt时，都是必填参数")
        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        ret = JdCheck.verify(obj, decimal=dict(some='模式, ppt未填写some字段，报错！'))
        logger.info(f"ret={ret}, obj={obj}")
        assert_that(ret['code']).is_not_equal_to(0)
        assert ERR_PUB_NEED == ret['code']
        
    def test_verify_08(self):
        logger.debug(f"测试 int 语法错误")
        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        ret = JdCheck.verify(obj, int=dict(value='value8'), student_id="学员")
        logger.info(f"ret={ret}, obj={obj}")
        assert_that(ret['code']).is_not_equal_to(0)
        assert ERR_SYNTAX == ret['code']
    
    def test_verify_str_09(self):
        logger.debug(f"测试 str 校验， 可选字符")
        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        ret = JdCheck.verify(obj, str=dict(room='room8,20'))
        logger.info(f"ret={ret}, obj={obj}")
        assert 0 == ret['code']
        assert obj.get('room8') is None

    def test_verify_str_10(self):
        logger.debug(f"测试 str 校验， 默认值 ds——空字符串('') <==> d0")
        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(str=dict(room='room8,20,ds'), date=dict(date="日期,opt,ds"), int=dict(age="年龄,ds"),
                      decimal=dict(fee="现金,ds"))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        assert 0 == ret['code']
        assert obj.get('room') == ""
        assert obj.get('date') is None
        assert obj.get('age') == 0
        assert obj.get('fee') == 0
        self.assertEqual(0, obj.get('fee'), 'decimal=dict(fee="现金,ds"): ***check*** fee == 0')

    def test_verify_ppt_11(self):
        logger.debug(f"测试 ppt 自定义提示")
        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(str=dict(room='room8,1-20,ppt需要教室'))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        assert ERR_PUB_NEED == ret['code']
        self.assertEqual(ret['msg'], '需要教室')

        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(date=dict(date="日期,ppt 需要日期"))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ERR_PUB_NEED, ret['code'])
        self.assertEqual(ret['msg'], '需要日期')

        obj = dict(value=3)
        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(int=dict(age="年龄,ppt 需要年龄"))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ERR_PUB_NEED, ret['code'])
        self.assertEqual(ret['msg'], '需要年龄')

        obj = dict(age='7a3')
        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(int=dict(age="年龄,ppt 需要年龄"))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ERR_PUB_NUM_INT, ret['code'])
        self.assertEqual(ret['msg'], '需要年龄')

        logger.debug(f"输入参数 obj={obj}")
        kwargs = dict(decimal=dict(fee="现金,ppt 需要现金"))
        ret = JdCheck.verify(obj, **kwargs)
        logger.debug(f"待校验参数：kwargs={kwargs}")
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ERR_PUB_NEED, ret['code'])
        self.assertEqual(ret['msg'], '需要现金')

    def test_012_jd_check_decimal_gte0(self):
        obj = dict(fee='7a3')
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal_gte0(obj, fee='收费方式金额')
        logger.info(f"ret={ret}, obj={obj}")
        self.assertNotEqual(ret['code'], 0)

        obj = dict(fee=-299)
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal_gte0(obj, fee='收费方式金额')
        logger.info(f"ret={ret}, obj={obj}")
        self.assertNotEqual(ret['code'], 0)

        obj = dict(fee=400.455)
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal_gte0(obj, fee='收费方式金额')
        logger.info(f"ret={ret}, obj={obj}")
        self.assertNotEqual(ret['code'], 0)
        # ===以上为异常场景============================================

        obj = dict(fee=308.65)
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal_gte0(obj, fee='收费方式金额')
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ret['code'], 0)
        self.assertEqual(obj['fee'], decimal.Decimal('308.65'))

        obj = dict(fee='608.75')
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal_gte0(obj, fee='收费方式金额')
        logger.info(f"ret={ret}, obj={obj}")
        self.assertEqual(ret['code'], 0)
        self.assertEqual(obj['fee'], decimal.Decimal('608.75'))

    def test_013_jd_check_decimal(self):
        obj = dict(fee='-608.75')
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal(obj, 'fee', '收费方式金额')
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertEqual(ret['code'], 0)
        self.assertEqual(obj['fee'], decimal.Decimal('-608.75'))

        obj = dict(fee='7a3')
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal(obj, 'fee', '收费方式金额')
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertNotEqual(ret['code'], 0)

        obj = dict(fee='1200.145')
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.decimal(obj, 'fee', '收费方式金额')
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertNotEqual(ret['code'], 0)
        self.assertEqual(obj['fee'], decimal.Decimal('1200.15'))
        
    def test_014_jd_check_verify(self):
        obj = dict()
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.verify(obj, time=dict(time="时刻,ds"))
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertEqual(0, ret['code'])
        self.assertIsNone(obj['time'], "默认值为None")

    def test_015_jd_check_verify(self):
        """
        {time: "22:00:00"}  -> 时间校验及转换
        """
        obj = dict(time="22:00:00")
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.verify(obj, time=dict(time="时刻,ds"))
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertEqual(0, ret['code'])
        self.assertEqual(datetime.time(22), obj['time'], "时刻值相等")

        obj = dict(time=datetime.time(22))
        logger.debug(f"参数校验前obj={obj}")
        ret = JdCheck.verify(obj, time=dict(time="时刻,ds"))
        logger.info(f"参数校验后obj={obj}, ret={ret}")
        self.assertEqual(0, ret['code'])
        self.assertEqual(datetime.time(22), obj['time'], "时刻值相等")


if __name__ == '__main__':
    unittest.main()
