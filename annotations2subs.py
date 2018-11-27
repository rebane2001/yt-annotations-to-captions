import xml.etree.ElementTree
from datetime import timedelta
import srt
import sys

if not len(sys.argv) == 3:
    print("YouTube XML Annotations -> SRT Captions converter")
    print("Use youtube-dl with the --write-annotations option to download an annotations file")
    print("Usage: " + sys.argv[0] + " annotations.xml captions.srt")
    quit()

annotations = xml.etree.ElementTree.parse(sys.argv[1]).getroot()
captions = []
caption_index = 0

for annotation in annotations[0]:
    for annotation_text in annotation.findall('TEXT'):
        caption_index += 1
        caption_text = annotation_text.text
        caption_time = annotation.findall(
            'segment')[0].findall('movingRegion')[0]
        caption_starttime = timedelta(minutes=int(caption_time[0].attrib['t'].split(":")[0]),seconds=int(caption_time[0].attrib['t'].split(":")[1].split(".")[0]),milliseconds=int(caption_time[0].attrib['t'].split(":")[1].split(".")[1]))
        caption_endtime = timedelta(minutes=int(caption_time[1].attrib['t'].split(":")[0]),seconds=int(caption_time[1].attrib['t'].split(":")[1].split(".")[0]),milliseconds=int(caption_time[1].attrib['t'].split(":")[1].split(".")[1]))
        captions.append(srt.Subtitle(index=caption_index, start=caption_starttime, end=caption_endtime, content=caption_text))

with open(sys.argv[2], "w", encoding="UTF-8") as cap_file:
    cap_file.write(srt.compose(captions))