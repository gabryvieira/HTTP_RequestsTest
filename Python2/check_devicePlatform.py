import os
import platform

def get_devicePlatform():
    platform_dev = platform.system()
    platform_release = platform.release()
    return platform_dev, platform_release