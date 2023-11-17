import random


def ua_generate():
    app_info = 'ZhihuHybrid osee2unifiedRelease/16416 osee2unifiedReleaseVersion/9.26.0'

    devices_android = [
        'Samsung Galaxy S21', 'Google Pixel 6', 'OnePlus 9 Pro', 'Xiaomi Mi 11', 'Huawei P40 Pro'
    ]

    devices_ios = [
        'iPhone 14 Pro', 'iPhone 13', 'iPad Pro', 'iPhone 15', 'iPhone SE'
    ]

    android_os_versions = ['Android 13', 'Android 12', 'Android 11']
    ios_os_versions = ['iOS 17', 'iOS 16', 'iOS 15']

    user_agents = []


    if random.random() < 0.5:  # Randomly select Android or iOS
        device = random.choice(devices_android)
        os_version = random.choice(android_os_versions)
        fuck_ua = f"{app_info} Mozilla/5.0 (Android; Mobile; {device} Android {os_version}) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        return fuck_ua
    else:
        device = random.choice(devices_ios)
        os_version = random.choice(ios_os_versions)
        fuck_ua = f"{app_info} Mozilla/5.0 (iPhone; CPU iPhone OS {os_version.replace('iOS ', '').replace('.', '_')} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        return fuck_ua