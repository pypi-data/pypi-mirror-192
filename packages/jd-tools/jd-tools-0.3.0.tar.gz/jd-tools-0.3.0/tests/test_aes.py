# -*- coding:utf-8 -*-
# 文件:  test_aes.py
# 日期:  2022/9/8 9:39
import random
import string
import unittest
from src.jd_tools import *


class TestAES(unittest.TestCase):

    def test_001_aes_gcm(self):
        logger.debug(f'测试 AES GCM 加解密函数 ...')
        
        aes_key = "H05YTS141TX04OHB195GPJ88PI15ZB97"
        associated_data = None
        nonce = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        data = '{"lang":"zh-CN","pageNumber":1,"pageSize":10,"cycleId":"1522973936269266945"}'
        logger.debug(f"原始数据：{data}")
        logger.debug(f"nonce = {nonce}")

        cipher_data = aes_gcm_encrypt(aes_key, data, associated_data=associated_data, nonce=nonce)
        logger.debug(f"aes_gcm_encrypt 加密数据：{cipher_data}")

        de_data = aes_gcm_decrypt(aes_key, cipher_data, nonce, associated_data)
        logger.debug(f"aes_gcm_decrypt 解密数据：{de_data}")
        self.assertEqual(de_data, data)

        de_data = aes_decrypt(nonce, cipher_data, associated_data, aes_key)
        logger.debug(f"aes_decrypt 解密数据：{de_data}")

    def test_002_get_ip(self):
        ip = get_ip()
        logger.debug(f"get_ip: [{ip}]")
        self.assertIsNotNone(ip)

    def test_003_get_hostname(self):
        host = get_hostname()
        logger.debug(f"get_hostname: [{host}]")
        self.assertIsNotNone(host)

    def test_004_jd_concat(self):
        """
        测试 jd_concat， 网关 + 路径 构成请求 url
        :return:
        """
        gate_way = 'https://api.weixin.qq.com/cgi-bin'
        path = '/qrcode/create?access_token=TOKEN'
        expect = gate_way + path
        res = jd_concat(gate_way, path)
        logger.debug(res)
        self.assertEqual(expect, res)

        gate_way = 'https://api.weixin.qq.com/cgi-bin/'
        path = '/qrcode/create?access_token=TOKEN'
        res = jd_concat(gate_way, path)
        logger.debug(res)
        self.assertEqual(expect, res)

        gate_way = 'https://api.weixin.qq.com/cgi-bin'
        path = 'qrcode/create?access_token=TOKEN'
        res = jd_concat(gate_way, path)
        logger.debug(res)
        self.assertEqual(expect, res)

    def test_005_core_request(self):
        """
        测试 core.request
        :return:
        """
        c = Core(logger=logger)
        status_code, message = c.request('https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=TOKEN',
                                         RequestType.POST)
        self.assertEqual(200, status_code)

        c = Core(logger=logger, gate_way='https://api.weixin.qq.com/cgi-bin')
        status_code, message = c.request('menu/create?access_token=ACCESS_TOKEN', RequestType.POST)
        self.assertEqual(200, status_code)
        

if __name__ == '__main__':
    unittest.main()
