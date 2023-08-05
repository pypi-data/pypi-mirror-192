# -*- coding: utf8 -*-
# 文件:  test_cfg.py
# 日期:  2022/9/11 23:52
import unittest
from src.jd_tools.cfg import Cfg
from src.jd_tools.logs import logger


class TestCfg(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cfg = Cfg("test.ini")

    def test_001_sections(self):
        logger.debug(f'测试 读取配置文件， 函数 section ...')
        ret = self.cfg.sections()
        logger.debug(f'配置文件段数量 {len(ret)}, {ret}')
        self.assertEqual(True, isinstance(ret, list))

    def test_002_section_run(self):
        logger.debug(f"测试 [run] section 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.is_token_server, 0)
        self.assertEqual(cfg.is_create_menu, 1)
        self.assertEqual(cfg.sandbox, 0)
        self.assertEqual(cfg.wx_test, 0)
        self.assertEqual(cfg.start_face_server, 1)
        self.assertEqual(cfg.start_card_server, 1)
        self.assertEqual(cfg.cyt_web_server, 1)
        self.assertEqual(cfg.http_port, 80)
        self.assertEqual(cfg.http_host, '0.0.0.0')
        self.assertEqual(cfg.ws_port, 45168)
        self.assertEqual(cfg.ws_async_mode, 9)
        self.assertEqual(cfg.send_error_email, 1)
        self.assertEqual(cfg.show_rsp, 1)
        self.assertEqual(cfg.show_template(), 0)

    def test_003_section_db(self):
        logger.debug(f"测试 [db] section 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.is_mysql, 1)
        self.assertEqual(cfg.host, '127.0.0.1')
        self.assertEqual(cfg.port, 3306)
        self.assertEqual(cfg.database, 'my_db')
        self.assertEqual(cfg.user, 'my_user')
        self.assertEqual(cfg.password, 'my_password#db')

    def test_004_section_redis(self):
        logger.debug(f"测试 [redis] section 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.redis_host, 'localhost')
        self.assertEqual(cfg.redis_port, 6379)
        self.assertEqual(cfg.redis_pwd, 'redis_password')

    def test_005_section_face_recognize(self):
        logger.debug(f"测试 人脸识别 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.face.host, 'localhost')
        self.assertEqual(cfg.face.port, 85004)
        self.assertEqual(cfg.face.output, 1)
        self.assertEqual(cfg.face_heat_beat(), 1)

    def test_006_section_card_recognize(self):
        logger.debug(f"测试 刷卡 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.card.host, 'localhost')
        self.assertEqual(cfg.card.port, 85005)
        self.assertEqual(cfg.card.output, 0)

    def test_007_section_tasks(self):
        logger.debug(f"测试 [tasks] section 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.task_backup_db, 1)
        self.assertEqual(cfg.task_wx_token, 1)

    def test_008_section_gzh(self):
        logger.debug(f"测试 [gzh] section 配置参数")
        cfg = self.cfg
        self.assertEqual(cfg.gzh_openid, 'o6sF76Ox756xNaWt1b2g6CT24c7d')
        self.assertEqual(cfg.gzh_company_id, 9846)

    def test_008_get_v(self):
        logger.debug(f"测试 自定义 section [rabbitmq] 配置参数")
        cfg = self.cfg
        section_mq = 'rabbitmq'
        self.assertEqual(cfg.str_val('host', section_mq), '10.13.14.15')
        self.assertEqual(cfg.get_val('port', section_mq), 5672)
        self.assertEqual(cfg.get_val('username', section_mq), 'admin')
        self.assertEqual(cfg.get_val('password', section_mq), 'your_password#hh')

    def test_009_wrong_file(self):
        wrong_file = Cfg("no-file.ini")
        # self.assertIsNone(wrong_file.__startup_cfg)
        self.assertNotEqual(wrong_file.is_create_menu, 1)
        self.assertEqual(wrong_file.sections(), [])
        self.assertNotEqual(wrong_file.str_val('host', 'rabbitmq'), '10.13.14.15')
        self.assertEqual(wrong_file.str_val('host', 'rabbitmq'), '')
        
    def test_010_str_val(self):
        """测试 [run] section 配置参数
        """
        cfg = self.cfg
        section_mq = 'rabbitmq'
        self.assertEqual('admin', cfg.str_val('username', section_mq), "str_val 过滤注释(#)")


if __name__ == '__main__':
    unittest.main()
