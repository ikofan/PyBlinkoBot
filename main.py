import os
import logging
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.utils.request import Request
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# (日志和环境变量加载部分保持不变)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_CHAT_ID = int(os.getenv("AUTHORIZED_CHAT_ID"))
BLINKO_API_URL = os.getenv("BLINKO_API_URL")
BLINKO_API_KEY = os.getenv("BLINKO_API_KEY")

# 为媒体组设置一个收集延迟（秒）
MEDIA_GROUP_COLLECTION_DELAY = 1.5


# --- Blinko API 交互部分 ---

def get_blinko_headers(is_json=True):
    headers = {"Authorization": f"Bearer {BLINKO_API_KEY}"}
    if is_json:
        headers["Content-Type"] = "application/json"
    return headers


def upload_file(file_path: str, file_name: str) -> dict | None:
    api_endpoint = f"{BLINKO_API_URL.rstrip('/')}/api/file/upload"
    headers = get_blinko_headers(is_json=False)
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            response = requests.post(api_endpoint, headers=headers, files=files)
            response.raise_for_status()
            response_data = response.json()
            if "filePath" in response_data and "fileName" in response_data:
                logger.info(f"文件上传成功 upload done: {response_data.get('fileName')}")
                return response_data
            else:
                logger.error(f"文件上传成功，但响应中缺少关键信息: {response_data}")
                return None
    except requests.exceptions.RequestException as e:
        logger.error(f"上传附件失败 upload failed: {e} - Response: {e.response.text if e.response else 'N/A'}")
        return None
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def create_note(content: str, attachments: list[dict] = None) -> bool:
    api_endpoint = f"{BLINKO_API_URL.rstrip('/')}/api/v1/note/upsert"
    headers = get_blinko_headers()
    payload = {"content": content, "type": 0, "attachments": attachments if attachments else []}
    try:
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        logger.info(f"成功创建笔记。")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"创建笔记失败: {e} - Response: {e.response.text if e.response else 'N/A'}")
        return False


# --- Telegram Bot 处理器 ---

def process_media_group(context: CallbackContext) -> None:
    job = context.job
    media_group_id = job.context['media_group_id']
    original_message = job.context['original_message']
    media_group_data = context.bot_data.get('media_groups', {}).pop(media_group_id, None)
    if not media_group_data or not media_group_data.get('messages'):
        return

    messages = media_group_data['messages']
    reply_message = original_message.reply_text(f"正在处理包含 {len(messages)} 个文件的消息...")

    caption = ""
    for msg in messages:
        if msg.caption:
            caption = msg.caption
            break
    if not caption:
        caption = "来自 Telegram 的文件" if len(messages) == 1 else "来自 Telegram 的媒体组"

    attachment_objects = []
    for i, msg in enumerate(messages):
        # --- MODIFICATION #1: 增加对视频和音频文件的识别 ---
        file_obj, file_name = None, None
        if msg.document:
            file_obj, file_name = msg.document, msg.document.file_name
        elif msg.photo:
            file_obj, file_name = msg.photo[-1], f"{msg.photo[-1].file_id}.jpg"
        elif msg.video:
            file_obj, file_name = msg.video, msg.video.file_name
        elif msg.audio:
            file_obj, file_name = msg.audio, msg.audio.file_name
        else:
            continue

        reply_message.edit_text(f"正在上传第 {i + 1}/{len(messages)} 个文件...")

        temp_path = f"./{file_name}"
        try:
            tg_file = context.bot.get_file(file_obj.file_id)
            tg_file.download(temp_path)

            upload_result = upload_file(temp_path, file_name)
            if upload_result:
                attachment_objects.append({
                    "name": upload_result.get("fileName"),
                    "path": upload_result.get("filePath"),
                    "size": upload_result.get("size"),
                    "type": upload_result.get("type")
                })
            else:
                logger.error(f"媒体组中文件 {file_name} 上传失败。")
        except Exception as e:
            logger.error(f"处理媒体组中文件 {file_name} 时出错: {e}")
            if os.path.exists(temp_path):
                os.remove(temp_path)

    if not attachment_objects:
        reply_message.edit_text("保存失败：所有文件都上传失败。")
        return

    reply_message.edit_text("所有文件上传成功，正在创建最终笔记...")
    success = create_note(content=caption, attachments=attachment_objects)

    if success:
        reply_message.edit_text("已保存")
    else:
        reply_message.edit_text("保存失败：笔记创建失败。")


def handle_text(update: Update, context: CallbackContext) -> None:
    reply_message = update.message.reply_text("收到，正在保存...")
    success = create_note(content=update.message.text)
    if success:
        reply_message.edit_text("已保存")
    else:
        reply_message.edit_text("保存失败")


def handle_file(update: Update, context: CallbackContext) -> None:
    if update.message.media_group_id:
        media_group_id = update.message.media_group_id
        if 'media_groups' not in context.bot_data:
            context.bot_data['media_groups'] = {}
        if media_group_id not in context.bot_data['media_groups']:
            context.bot_data['media_groups'][media_group_id] = {
                'messages': [update.message],
                'original_message': update.message
            }
        else:
            context.bot_data['media_groups'][media_group_id]['messages'].append(update.message)
        job_context = {
            'media_group_id': media_group_id,
            'original_message': context.bot_data['media_groups'][media_group_id]['original_message']
        }
        job_name = str(media_group_id)
        existing_jobs = context.job_queue.get_jobs_by_name(job_name)
        for job in existing_jobs:
            job.schedule_removal()
        context.job_queue.run_once(
            process_media_group,
            MEDIA_GROUP_COLLECTION_DELAY,
            context=job_context,
            name=job_name
        )
    else:
        virtual_group_id = f"single_{update.message.message_id}"
        context.bot_data.setdefault('media_groups', {})[virtual_group_id] = {
            'messages': [update.message],
            'original_message': update.message
        }
        job_context = {'media_group_id': virtual_group_id, 'original_message': update.message}
        context.job_queue.run_once(process_media_group, 0.1, context=job_context)


def error_handler(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def main() -> None:
    if not all([TELEGRAM_BOT_TOKEN, AUTHORIZED_CHAT_ID, BLINKO_API_URL, BLINKO_API_KEY]):
        logger.error("环境变量不完整，请检查 .env 文件。")
        return
    request_kwargs = {
        'connect_timeout': 10,
        'read_timeout': 60,
    }
    updater = Updater(TELEGRAM_BOT_TOKEN, request_kwargs=request_kwargs)
    dispatcher = updater.dispatcher
    authorized_filter = Filters.user(user_id=AUTHORIZED_CHAT_ID)

    # --- MODIFICATION #2: 扩大监听范围，增加 Filters.video 和 Filters.audio ---
    all_media_filters = (Filters.document | Filters.photo | Filters.video | Filters.audio)
    dispatcher.add_handler(MessageHandler(authorized_filter & all_media_filters & ~Filters.command, handle_file))
    # --- 修改结束 ---

    dispatcher.add_handler(MessageHandler(authorized_filter & Filters.text & ~Filters.command, handle_text))
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    logger.info("机器人已启动 Bot started...")
    updater.idle()


if __name__ == '__main__':
    main()