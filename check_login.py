from DrissionPage import ChromiumPage
import time


def check_xhs_login():
    """检查小红书是否已登录"""
    print("=" * 60)
    print("小红书登录检查工具")
    print("=" * 60)
    print()

    # 创建浏览器实例
    page = ChromiumPage()

    try:
        print("正在打开小红书网站...")
        page.get('https://www.xiaohongshu.com')

        # 等待页面加载
        time.sleep(3)

        # 检查是否已登录的多种方式
        is_logged_in = False

        # 方法1: 检查是否有用户头像（更精确的判断）
        # 先检查是否有登录弹窗或按钮，如果有说明未登录
        try:
            # 先检查登录弹窗（优先级最高）
            login_popup_selectors = [
                'css:.login-modal',
                'css:.login-popup',
                'css:[class*="login-modal"]',
                'css:[class*="login-popup"]',
                'css:.auth-modal',
                'css:[class*="auth-popup"]',
            ]

            popup_found = False
            for selector in login_popup_selectors:
                try:
                    popup = page.ele(selector, timeout=1)
                    if popup:
                        print("✗ 检测到登录弹窗，未登录")
                        popup_found = True
                        break
                except:
                    continue

            if popup_found:
                is_logged_in = False
            else:
                # 检查是否有手机号输入框（登录弹窗的标志）
                try:
                    phone_input = page.ele('css:input[placeholder*="手机号"]', timeout=1)
                    if phone_input:
                        print("✗ 检测到手机号输入框，有登录弹窗")
                        is_logged_in = False
                    else:
                        # 没有登录弹窗，再检查用户头像
                        avatar_selectors = [
                            'css:.user-avatar img',
                            'css:.avatar img',
                            'css:.user-info .avatar img',
                        ]
                        for selector in avatar_selectors:
                            try:
                                avatar = page.ele(selector, timeout=1)
                                if avatar:
                                    # 检查头像是否在顶部导航栏（已登录用户的头像位置）
                                    avatar_html = str(avatar.html) if hasattr(avatar, 'html') else ''
                                    if avatar_html:
                                        print("✓ 检测到用户头像，已登录")
                                        is_logged_in = True
                                        break
                            except:
                                continue
                except:
                    pass
        except:
            pass

        # 方法2: 检查页面内容中是否有登录相关文本
        if not is_logged_in:
            try:
                page_text = page.ele('css:body').text
                login_keywords = ['手机号登录', '验证码登录', '密码登录', '立即登录', '登录/注册']
                if any(keyword in page_text for keyword in login_keywords):
                    print("✗ 检测到登录相关文本，未登录")
                    is_logged_in = False
                else:
                    # 检查是否有手机号输入框（登录弹窗常见元素）
                    phone_inputs = page.eles('css:input[placeholder*="手机号"], css:input[type="tel"]', timeout=1)
                    if phone_inputs:
                        print("✗ 检测到手机号输入框，有登录弹窗")
                        is_logged_in = False
                    else:
                        print("✓ 未检测到登录相关元素")
                        is_logged_in = True
            except:
                pass

        # 方法3: 使用JavaScript检查cookie或localStorage
        if not is_logged_in:
            try:
                js_check = """
                // 检查是否有登录相关的cookie
                const cookies = document.cookie;
                const hasLoginCookie = cookies.includes('web_session') || 
                                       cookies.includes('user_id') || 
                                       cookies.includes('login') ||
                                       cookies.includes('xhsTracker');
                
                // 检查localStorage
                const hasUserInfo = localStorage.getItem('user_info') !== null ||
                                   localStorage.getItem('user') !== null ||
                                   localStorage.getItem('userId') !== null;
                
                // 检查sessionStorage
                const hasSessionUser = sessionStorage.getItem('user') !== null;
                
                return hasLoginCookie || hasUserInfo || hasSessionUser;
                """
                result = page.run_js(js_check)
                if result:
                    print("✓ 检测到登录凭证，已登录")
                    is_logged_in = True
                else:
                    print("✗ 未检测到登录凭证")
            except Exception as e:
                print(f"JavaScript检查失败: {e}")

        print()

        if is_logged_in:
            print("=" * 60)
            print("检查完成：已登录")
            print("3秒后自动关闭浏览器...")
            print("=" * 60)
            time.sleep(3)
        else:
            print("=" * 60)
            print("检查完成：未登录")
            print("请手动登录小红书账号")
            print("登录完成后按回车键关闭浏览器...")
            print("=" * 60)
            input()

    except Exception as e:
        print(f"检查过程中出错: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键关闭...")

    finally:
        page.quit()
        print("浏览器已关闭")


if __name__ == '__main__':
    check_xhs_login()
