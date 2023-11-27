import schedule
import time
import subprocess
from discord_webhook import DiscordWebhook
import logging

# Discord Webhook URL 和仓库路径作为参数传递
DISCORD_WEBHOOK_URL = "你的DISCORD_WEBHOOK_URL"
REPO_PATH = "/home/zhifan/bounty-targets-data" #你要监控的github仓库，需要克隆到本地

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_RETRIES = 3
RETRY_INTERVAL = 60  # 重试间隔时间（秒）

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

def send_notification(commit_info, webhook_url, retries=0):
    try:
        webhook = DiscordWebhook(url=webhook_url)
        max_length = 1800
        chunks = [commit_info[i:i + max_length] for i in range(0, len(commit_info), max_length)]

        for chunk in chunks:
            message_content = f"GitHub 仓库更新:\n```diff\n{chunk}\n```"
            webhook.content = message_content
            webhook.execute()

        logging.info("成功发送 Discord 通知。")
    except Exception as e:
        logging.exception("发送 Discord 通知时发生错误")

        if retries < MAX_RETRIES:
            logging.info(f"等待 {RETRY_INTERVAL} 秒后进行重试...")
            time.sleep(RETRY_INTERVAL)
            send_notification(commit_info, webhook_url, retries=retries + 1)
        else:
            logging.error("达到最大重试次数，放弃重试。")

def update_and_notify():
    try:
        logging.info("更新并通知中...")
        git_pull(REPO_PATH)
        commit_info = get_git_updates(REPO_PATH)

        if commit_info:
            send_notification(commit_info, DISCORD_WEBHOOK_URL)

    except Exception as e:
        logging.exception(f"发生错误: {e}")

# 初始运行一次
update_and_notify()

# 设置每30分钟执行一次
schedule.every(30).minutes.do(update_and_notify)

while True:
    schedule.run_pending()
    time.sleep(1)
