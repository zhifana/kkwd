import schedule
import time
import subprocess
from discord_webhook import DiscordWebhook
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

# Discord Webhook URL 和仓库路径作为参数传递
DISCORD_WEBHOOK_URL = "你的DISCORD_WEBHOOK_URL"
REPO_PATH = "/home/zhifan/bounty-targets-data" #你要监控的github仓库，需要克隆到本地

def git_pull(repo_path):
    try:
        subprocess.run(["git", "pull", "origin", "main"], cwd=repo_path, check=True)
        logging.info("Git pull 成功。")
    except subprocess.CalledProcessError as e:
        logging.error(f"从git拉取时发生错误: {e}")
        raise

def get_git_updates(repo_path):
    try:
        commit_info = subprocess.check_output(
            ["git", "show", "--pretty=format:%H%n%an%n%ad%n%s", "--no-merges"],
            cwd=repo_path, text=True
        )
        return commit_info
    except subprocess.CalledProcessError as e:
        logging.error(f"检索git更新时发生错误: {e}")
        raise

def send_notification(commit_info, webhook_url):
    try:
        # 设置 Discord Webhook
        webhook = DiscordWebhook(url=webhook_url)

        # 分割消息内容
        max_length = 1800
        chunks = [commit_info[i:i + max_length] for i in range(0, len(commit_info), max_length)]

        for chunk in chunks:
            # 将提交信息作为消息内容
            message_content = f"GitHub 仓库更新:\n```diff\n{chunk}\n```"

            # 设置消息内容
            webhook.content = message_content

            # 执行 Webhook
            webhook.execute()

        logging.info("成功发送 Discord 通知。")
    except Exception as e:
        logging.exception("发送 Discord 通知时发生错误")
        raise

def update_and_notify():
    try:
        logging.info("更新并通知中...")
        git_pull(REPO_PATH)
        commit_info = get_git_updates(REPO_PATH)

        if commit_info:
            send_notification(commit_info, DISCORD_WEBHOOK_URL)

    except Exception as e:
        logging.exception(f"发生错误: {e}")
        raise  # 将异常重新抛出，以便退出当前循环

# 无限循环
while True:
    try:
        # 初始运行一次
        update_and_notify()

        # 设置每30分钟执行一次
        schedule.every(30).minutes.do(update_and_notify)

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception as e:
        logging.exception(f"主循环中发生错误: {e}")
        logging.info("重新运行脚本...")
