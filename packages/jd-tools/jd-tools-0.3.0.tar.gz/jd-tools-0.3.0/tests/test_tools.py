# -*- coding: utf8 -*-
# 文件:  test_tools.py
# 日期:  2022/9/16 13:09
import datetime
import unittest
import decimal
from src.jd_tools import *


class TestJdTools(unittest.TestCase):

    def test_001_get_filename(self):
        logger.debug(f'测试 JdTools.get_filename')

        filename = JdTools.get_filename('学员', excel2010=True)
        logger.info(f"返回值 filename = [{filename}]")
        self.assertEqual(filename[:2], '学员')
        self.assertEqual(filename[-5:], '.xlsx')

        filename = JdTools.get_filename('老师', no_ext=True)
        logger.info(f"返回值 filename = [{filename}]")
        self.assertEqual(filename[:2], '老师')
        self.assertNotEqual(filename[-5:], '.xlsx')

        filename = JdTools.get_filename('员工', no_ext=True, no_ms=True)
        logger.info(f"返回值 filename = [{filename}]")
        self.assertEqual(filename[:2], '员工')
        self.assertNotEqual(filename[-5:], '.xlsx')

    def test_002_decimal(self):
        logger.debug(f'测试 JdTools.decimal')

        money = decimal.Decimal('1265.62500')
        wanted = decimal.Decimal('1265.63')
        tmp = decimal.Decimal(1500) / decimal.Decimal(32) * decimal.Decimal(27)
        logger.debug(f"money={money}, wanted={wanted}, tmp={tmp}")
        self.assertEqual(tmp, money)

        fee = JdTools.decimal(tmp)
        logger.debug(f"wanted={wanted}, tmp={tmp}, fee={fee} (after JdTools.decimal)")
        self.assertEqual(fee, wanted)

        pay = JdTools.decimal(2500.55)
        logger.debug(f"pay={pay}")
        self.assertEqual(pay, decimal.Decimal('2500.55'))

        pay = JdTools.decimal(2500.65)
        logger.debug(f"pay={pay}")
        self.assertEqual(pay, decimal.Decimal('2500.65'))

        float_val = 1500 / 32 * 27
        tmp = JdTools.decimal(float_val)    # test float -> decimal
        logger.debug(f"float1={float_val}, ---> JdTools.decimal({float_val})=tmp={tmp}")
        self.assertEqual(tmp, wanted)

        self.assertEqual(JdTools.decimal(None), JdTools.decimal(""), f"None==''")
        self.assertEqual(JdTools.decimal(None), 0, f"None==0")

        lst = []
        num, passed = JdTools.decimal(lst, result=True)
        self.assertFalse(passed, f"不支持的类型(list)无法转 decimal")
        self.assertEqual(num, lst)

    def test_003_compare_time(self):
        time1 = '08:00-09:00'
        time2 = '08:30-09:30'
        ret = JdTools.compare_time(time1, time2)
        self.assertFalse(ret, f"{time1} and {time2} 时间段冲突")

        time1 = '08:00-09:00'
        time2 = '09:00-10:30'
        ret = JdTools.compare_time(time1, time2)
        self.assertTrue(ret, f"{time1} and {time2} 时间段不冲突")

        time1 = '08:00-09:00'
        time2 = '09:30-11:00'
        ret = JdTools.compare_time(time1, time2)
        self.assertTrue(ret, f"{time1} and {time2} 时间段不冲突")

    def test_004_humanize_date_delta(self):
        day1 = datetime.datetime(2022, 9, 17)
        day2 = datetime.date(2022, 10, 20)

        ret = humanize_date_delta(day1, day2)
        logger.debug(f"humanize_date_delta: ret={ret}")
        self.assertEqual(ret, '1个月')

        some_day = datetime.datetime(2020, 8, 17)
        self.assertEqual(humanize_date_delta(some_day, day1), "2年")

        three = datetime.datetime(2022, 9, 20)
        self.assertEqual(humanize_date_delta(day1, three), "3天")

        self.assertEqual(humanize_date_delta(day2, day2), "", msg="同一天，返回空")

        # wrong
        self.assertEqual(humanize_date_delta(day1, dict(wrong=True)), "", "异常场景")
        self.assertEqual(humanize_date_delta(day1, some_day), "", "start > end， 返回空")

    def test_005_get_date(self):
        """
        测试 JdTools.get_date 获取 日期字符串
        :return:
        """
        dd = datetime.datetime.today()

        ret = JdTools.get_date()
        ret1 = JdTools.get_date()
        logger.debug(f"ret={ret}")
        logger.debug(f"ret={ret1}")

        fmt = '%Y%m%d_%H%M%S'
        time_str = datetime.datetime.strftime(dd, fmt)
        size = len(time_str)
        self.assertEqual(time_str, ret[: size])
        self.assertEqual(time_str, ret1[: size])

    def test_006_get_filename(self):
        """
        测试 JdTools.get_filename 获取 文件名
        :return:
        """
        ret = JdTools.get_filename('员工', no_ms=False)
        logger.debug(f"ret={ret}")
        ret = JdTools.get_filename('员工', no_ext=True)
        logger.debug(f"ret={ret}")
        ret = JdTools.get_filename('', no_ext=True)
        logger.debug(f"ret={ret}")


if __name__ == '__main__':
    unittest.main()
