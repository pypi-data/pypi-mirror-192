# -*- coding:utf-8 -*-
# =============================================================================
# 文件:  test_avatar.py
# 日期:  2022/11/10 15:41
# 作者:  WXG
# 版权:  2015-2022 君迪 版权所有
# 描述:  
# =============================================================================
import unittest
import os
from src.jd_tools.jd_avatar import Avatar, AvatarDirMgr
from src.jd_tools.logs import logger
from src.jd_tools.tools import JdPath
from src.jd_tools.oper_file import copy_file
from appdir import basedir


class TestAvatar(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        ad = AvatarDirMgr()
        ad.basedir = os.path.join(basedir, 'tests/images')
        ad.tmpdir = 'tmp'
        logger.debug(f"basedir: [{ad.basedir}], tmpdir: [{ad.tmpdir}]")
    
        ad.register_module('user', 'head')
        ad.register_module('student')
        
        cls.ad = ad
    
    def test_001_create(self):
        """测试 文件上传管理模块
        """
        ad = self.ad
        
        module = 'user'
        av = Avatar(module)
        fp = av.new_file('user001.jpg', some_id=5)
        img_url = av.url
        logger.debug(f"new file url, img_url={img_url}")
        
        new_f = os.path.join(ad.basedir, f"head/{module}/5/user001.jpg")
        new_f = JdPath.slash(new_f)

        new_url = f"/head/{module}/5/user001.jpg"
        new_url = JdPath.slash(new_url)
        self.assertEqual(new_url, img_url)
        self.assertEqual(new_f, JdPath.slash(fp))

    def test_002_create(self):
        """测试 文件上传管理模块, 临时目录
        """
        ad = self.ad
    
        module = 'user'
        av = Avatar(module)
        fp = av.new_file('user001.jpg')
        img_url = av.url
        logger.debug(f"new file url, img_url={img_url}")
    
        new_f = os.path.join(ad.basedir, f"tmp/del_{module}")
        new_f = JdPath.slash(new_f)

        new_url = f"/tmp/del_{module}"
        new_url = JdPath.slash(new_url)
        self.assertTrue(new_url in img_url)
        fp1 = JdPath.slash(fp)
        logger.debug(f"文件路径：{fp1}")
        self.assertTrue(new_f in fp1)
        
        copy_file(os.path.join(basedir, 'tests/images/105.jpg'), fp1)
        
        # 移动文件
        Avatar.move_to_normal(module, img_url, 66)
        

if __name__ == '__main__':
    unittest.main()
