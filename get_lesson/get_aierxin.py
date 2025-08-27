import subprocess
import sys
import shutil

# m3u8 视频地址（你提供的链接）
m3u8_url = "https://cd12-ccd1-3.play.bokecc.com/flvs/606E693D99DE632E/2025-08-24/0E0E640BDE28CE94F3342D97BB1D6DF8-20.m3u8?t=1756265297&key=2DBA67911AB0A131D67A9F7835EB2180&tpl=10&tpt=112&custom_id=app_pc_12069879271"

# 输出文件名
output_file = "output.mp4"

# 检查 ffmpeg 是否安装
if not shutil.which("ffmpeg"):
    print("❌ 请先安装 ffmpeg 再运行此脚本")
    sys.exit(1)

# 调用 ffmpeg 下载并合并视频
cmd = [
    "ffmpeg",
    "-i", m3u8_url,   # 输入 m3u8 地址
    "-c", "copy",     # 不转码，直接拷贝
    "-bsf:a", "aac_adtstoasc",  # 处理音频头，避免部分播放器不兼容
    output_file
]

print("开始下载视频，请稍等...")
result = subprocess.run(cmd)

if result.returncode == 0:
    print(f"✅ 下载完成，保存为 {output_file}")
else:
    print("❌ 下载失败，请检查链接是否过期或加密")
