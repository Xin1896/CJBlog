#!/usr/bin/env python3
"""
应用测试脚本
用于测试 Flask 应用的基本功能
"""

import requests
import time
import sys

def test_app():
    """测试应用功能"""
    base_url = "http://localhost:5000"
    
    print("🧪 开始测试优雅博客应用...")
    print(f"📍 测试地址: {base_url}")
    print("=" * 50)
    
    # 测试首页
    print("1. 测试首页...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("   ✅ 首页访问正常")
            if "优雅博客" in response.text:
                print("   ✅ 页面内容正确")
            else:
                print("   ❌ 页面内容异常")
        else:
            print(f"   ❌ 首页访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 首页访问异常: {e}")
        return False
    
    # 测试关于页面
    print("\n2. 测试关于页面...")
    try:
        response = requests.get(f"{base_url}/about", timeout=10)
        if response.status_code == 200:
            print("   ✅ 关于页面访问正常")
        else:
            print(f"   ❌ 关于页面访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 关于页面访问异常: {e}")
    
    # 测试联系页面
    print("\n3. 测试联系页面...")
    try:
        response = requests.get(f"{base_url}/contact", timeout=10)
        if response.status_code == 200:
            print("   ✅ 联系页面访问正常")
        else:
            print(f"   ❌ 联系页面访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 联系页面访问异常: {e}")
    
    # 测试搜索页面
    print("\n4. 测试搜索页面...")
    try:
        response = requests.get(f"{base_url}/search", timeout=10)
        if response.status_code == 200:
            print("   ✅ 搜索页面访问正常")
        else:
            print(f"   ❌ 搜索页面访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 搜索页面访问异常: {e}")
    
    # 测试登录页面
    print("\n5. 测试登录页面...")
    try:
        response = requests.get(f"{base_url}/login", timeout=10)
        if response.status_code == 200:
            print("   ✅ 登录页面访问正常")
        else:
            print(f"   ❌ 登录页面访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 登录页面访问异常: {e}")
    
    # 测试注册页面
    print("\n6. 测试注册页面...")
    try:
        response = requests.get(f"{base_url}/register", timeout=10)
        if response.status_code == 200:
            print("   ✅ 注册页面访问正常")
        else:
            print(f"   ❌ 注册页面访问失败: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 注册页面访问异常: {e}")
    
    # 测试搜索功能
    print("\n7. 测试搜索功能...")
    try:
        response = requests.get(f"{base_url}/search?q=技术", timeout=10)
        if response.status_code == 200:
            print("   ✅ 搜索功能正常")
        else:
            print(f"   ❌ 搜索功能异常: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 搜索功能测试异常: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 基本功能测试完成！")
    print("\n📝 测试结果说明:")
    print("   - 如果所有测试都通过，说明应用运行正常")
    print("   - 如果有测试失败，请检查应用是否正常启动")
    print("   - 确保应用在 http://localhost:5000 上运行")
    
    return True

def wait_for_app():
    """等待应用启动"""
    base_url = "http://localhost:5000"
    max_attempts = 30
    attempt = 0
    
    print("⏳ 等待应用启动...")
    
    while attempt < max_attempts:
        try:
            response = requests.get(base_url, timeout=5)
            if response.status_code == 200:
                print("✅ 应用已启动，开始测试...")
                return True
        except requests.exceptions.RequestException:
            pass
        
        attempt += 1
        print(f"   尝试 {attempt}/{max_attempts}...")
        time.sleep(2)
    
    print("❌ 应用启动超时，请检查应用是否正常运行")
    return False

if __name__ == '__main__':
    print("🚀 优雅博客应用测试工具")
    print("=" * 50)
    
    # 检查应用是否已启动
    if not wait_for_app():
        sys.exit(1)
    
    # 执行测试
    test_app()
