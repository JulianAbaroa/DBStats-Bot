import asyncio
import paths
import os

TEXT_CHANNEL_ID = 1405331337254146048

async def download_attachments(bot, channel, limit=None):
    """Descarga todos los attachments históricos del canal que no estén en PROCESSED_DIRECTORY."""
    os.makedirs(paths.CARNAGES_DIRECTORY, exist_ok=True)
    os.makedirs(paths.PROCESSED_DIRECTORY, exist_ok=True)

    downloaded_files = []

    async for message in channel.history(limit=limit, oldest_first=True):
        for attachment in message.attachments:
            processed_path = os.path.join(paths.PROCESSED_DIRECTORY, attachment.filename)
            if os.path.exists(processed_path):
                continue  # ya procesado
            carnage_path = os.path.join(paths.CARNAGES_DIRECTORY, attachment.filename)
            if not os.path.exists(carnage_path):
                try:
                    await attachment.save(carnage_path)
                    print(f"[INFO] File '{attachment.filename}' saved in '{carnage_path}'")
                except Exception as e:
                    print(f"[ERROR] Failed to download '{attachment.filename}': {e}")
                    continue
            downloaded_files.append(carnage_path)

    return downloaded_files

async def run_dbstats_multiple(files, channel=None, send_feedback=True):
    """Ejecuta DBStats.exe pasándole todos los archivos descargados como argumentos."""
    if not files:
        print("[INFO] No new files to process with DBStats.")
        return

    cmd = [paths.DBSTATS_PATH]
    print(f"[INFO] Launching DBStats.")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout_bytes, stderr_bytes = await proc.communicate()
    stdout_text = stdout_bytes.decode(errors='ignore')
    stderr_text = stderr_bytes.decode(errors='ignore')

    if send_feedback and channel:
        await channel.send(f"DBStats finished with return code {proc.returncode}.")
        if stdout_text:
            await channel.send(f"**DBStats stdout:**\n```{stdout_text[:1900]}```")
        if stderr_text:
            await channel.send(f"**DBStats stderr:**\n```{stderr_text[:1900]}```")

    print(f"[OK] DBStats returncode: {proc.returncode}")

async def check_channel_history_and_process(bot, limit=None):
    """Descarga todos los archivos históricos pendientes y luego los procesa con DBStats."""
    await bot.wait_until_ready()

    channel = bot.get_channel(TEXT_CHANNEL_ID)
    if channel is None:
        try:
            channel = await bot.fetch_channel(TEXT_CHANNEL_ID)
        except Exception as e:
            print(f"[ERROR] Could not fetch channel {TEXT_CHANNEL_ID}: {e}")
            return

    print(f"[INFO] Starting history scan for attachments in channel: {TEXT_CHANNEL_ID}")
    files_to_process = await download_attachments(bot, channel, limit=limit)
    print(f"[INFO] Total files to process with DBStats: {len(files_to_process)}")
    await run_dbstats_multiple(files_to_process, channel=channel)

async def handle_message(bot, message):
    """Procesa un único mensaje entrante con attachments en el canal configurado."""
    if message.author.id == bot.user.id:
        return

    if message.channel.id != TEXT_CHANNEL_ID:
        return  # ignorar mensajes de otros canales

    if not message.attachments:
        return  # ignorar mensajes sin archivos

    os.makedirs(paths.CARNAGES_DIRECTORY, exist_ok=True)
    os.makedirs(paths.PROCESSED_DIRECTORY, exist_ok=True)

    downloaded_files = []

    for attachment in message.attachments:
        processed_path = os.path.join(paths.PROCESSED_DIRECTORY, attachment.filename)
        if os.path.exists(processed_path):
            print(f"[INFO] File '{attachment.filename}' already processed, skipping.")
            continue

        carnage_path = os.path.join(paths.CARNAGES_DIRECTORY, attachment.filename)
        if not os.path.exists(carnage_path):
            try:
                await attachment.save(carnage_path)
                print(f"[INFO] File '{attachment.filename}' saved in '{carnage_path}'")
            except Exception as e:
                print(f"[ERROR] Failed to download '{attachment.filename}': {e}")
                continue

        downloaded_files.append(carnage_path)

    if downloaded_files:
        await run_dbstats_multiple(downloaded_files, channel=message.channel, send_feedback=True)