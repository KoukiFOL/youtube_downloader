from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from .forms import YouTubeDownloadForm
import yt_dlp
import os

def download_view(request):
    if request.method == 'POST':
        form = YouTubeDownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            format = form.cleaned_data['format']

            ydl_opts = {
                'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio',
                'outtmpl': '%(title)s.%(ext)s',  # 保存するファイルの名前
                'postprocessors': []  # 初期化
            }

    # MP3形式の場合のポストプロセッサ
            if format == 'mp3':
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                })

    # MP4形式の場合のポストプロセッサ（映像と音声のマージ）
            if format == 'mp4':
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                })
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                    # MP3の場合、拡張子を確認
                    if format == 'mp3':
                        filename = filename.replace('.webm', '.mp3')

                    # ファイルをレスポンスとして返す
                    response = HttpResponse(open(filename, 'rb'), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
                    os.remove(filename)
                    return response
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
    else:
        form = YouTubeDownloadForm()

    return render(request, 'download_form.html', {'form': form})