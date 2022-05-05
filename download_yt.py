from pytube import YouTube

import PySimpleGUI as sg
import requests 

sg.theme('DarkRed1')

layout = [
		[sg.Column([[sg.Text('Paste video URL', key = '-INPUTTITLE-')]]),
		sg.Column([[sg.Input(key = '-INPUT-')]]),
		sg.Column([[sg.Button('Search', key = '-SEARCH-')]])],
		[sg.Text('Tittle:', key = '-TITLE-')],
		[sg.Multiline('Description:', key = '-DESCRIPTION-', size = (40,20), no_scrollbar = True, disabled = True)],
		[sg.Frame('1080p', layout = [[sg.Button('Download', key = '-1080DOWN-')],[sg.Text('Size:', key = '-1080SIZE-')]], size = (305,90))],
		[sg.Frame('720p', layout = [[sg.Button('Download', key = '-720DOWN-')],[sg.Text('Size:', key = '-720SIZE-')]], size = (305,90))],
		[sg.Frame('Audio', layout = [[sg.Button('Download', key = '-AUDIODOWN-')],[sg.Text('Size:', key = '-AUDIOSIZE-')]], size = (305,90))],
		[sg.Text('Progress:', key = '-PROGRESSTEXT-')],
		[sg.ProgressBar(100, key = '-PROGRESSBAR-', size = (50,20), bar_color = ("Red", "White"))]
]
window = sg.Window('Not my Video Downloader', layout)
progressbar = window['-PROGRESSBAR-']
video = False

def update_progress(stream, chunk, bytes):
	total = round(stream.filesize / 1048576)
	done = total - round(bytes / 1048576)
	window['-PROGRESSTEXT-'].update(f'Progress: {done} / {total}') 
	window['-PROGRESSBAR-'].update((done / total) * 100) 

def finished(stream, path):
	window['-PROGRESSTEXT-'].update('Done!') 
	window['-PROGRESSBAR-'].update(100) 

while True: 
	event, values = window.read(timeout = 50)
	if event == sg.WIN_CLOSED:
		print('Goodbye!')
		break

	if event == '-SEARCH-':
		url = values['-INPUT-']
		r = requests.get(url)
		if r.status_code == 200:
			video = YouTube(url, on_complete_callback = finished, on_progress_callback = update_progress)
			window['-TITLE-'].update(f'Title: {video.title}')
			window['-DESCRIPTION-'].update(f'Description: {video.description}')
			print(video.streams)
			if video.streams.filter(res = '1080p', file_extension='mp4'):
				highres = video.streams.filter(res = '1080p', file_extension='mp4')[0]
			if video.streams.filter(res = '720p', file_extension='mp4'):
				midres = video.streams.filter(res = '720p', file_extension='mp4')[0]
			if video.streams.get_audio_only():
				audio = video.streams.get_audio_only()
			window['-1080SIZE-'].update(f'Size: {round(highres.filesize / 1048576)}Mb')
			window['-720SIZE-'].update(f'Size: {round(midres.filesize / 1048576)}Mb')
			window['-AUDIOSIZE-'].update(f'Size: {round(audio.filesize / 1048576)}Mb')
			window['-PROGRESSBAR-'].update(0) 
		else:
			video = False
		window['-PROGRESSTEXT-'].update('Progress: ') 
		window['-PROGRESSBAR-'].update(0)
	if video:
		if event == '-1080DOWN-':
			download_path = sg.popup_get_folder('Download',no_window = True) 
			highres.download(output_path = download_path)
		elif event == '-AUDIODOWN-':
			download_path = sg.popup_get_folder('Download',no_window = True) 
			audio.download(output_path = download_path)
		elif event == '-720DOWN-':
			download_path = sg.popup_get_folder('Download',no_window = True) 
			midres.download(output_path = download_path)

window.close()